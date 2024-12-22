from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer
from django.http import JsonResponse
from django.views import View
import json
from myapp.scrap_data import download_sec_filings
from myapp.integrations import process_data

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CompanyListView(APIView):
    """
    API endpoint to fetch all companies.
    """

    def get(self, request):
        companies = [
            {"id": 1, "ticker": "AAPL", "title": "Apple Inc.", "cik": "0000320193", "downloaded": True},
            {"id": 2, "ticker": "MSFT", "title": "MICROSOFT CORP", "cik": "0000789019", "downloaded": True},
            {"id": 3, "ticker": "NVDA", "title": "NVIDIA CORP", "cik": "0001045810", "downloaded": True},
            {"id": 4, "ticker": "AMZN", "title": "AMAZON COM INC", "cik": "0001018724", "downloaded": True},
            {"id": 5, "ticker": "GOOGL", "title": "Alphabet Inc.", "cik": "0001652044", "downloaded": True},
            {"id": 6, "ticker": "META", "title": "Meta Platforms, Inc.", "cik": "0001326801", "downloaded": True},
            {"id": 7, "ticker": "TSLA", "title": "Tesla, Inc.", "cik": "0001318605", "downloaded": False},
            {"id": 8, "ticker": "AVGO", "title": "Broadcom Inc.", "cik": "0001730168", "downloaded": True},
            {"id": 9, "ticker": "BRK-B", "title": "BERKSHIRE HATHAWAY INC", "cik": "0001067983", "downloaded": True},
            {"id": 10, "ticker": "WMT", "title": "Walmart Inc.", "cik": "0000104169", "downloaded": False},
            {"id": 11, "ticker": "LLY", "title": "ELI LILLY & Co", "cik": "0000059478", "downloaded": False},
            {"id": 12, "ticker": "JPM", "title": "JPMORGAN CHASE & CO", "cik": "0000019617", "downloaded": True},
            {"id": 13, "ticker": "V", "title": "VISA INC.", "cik": "0001403161", "downloaded": True},
            {"id": 14, "ticker": "SPY", "title": "SPDR S&P 500 ETF TRUST", "cik": "0000884394", "downloaded": False},
            {"id": 15, "ticker": "MA", "title": "Mastercard Inc", "cik": "0001141391", "downloaded": False},
            {"id": 16, "ticker": "NVO", "title": "NOVO NORDISK A S", "cik": "0000353278", "downloaded": False},
            {"id": 17, "ticker": "ORCL", "title": "ORACLE CORP", "cik": "0001341439", "downloaded": True},
            {"id": 18, "ticker": "XOM", "title": "EXXON MOBIL CORP", "cik": "0000034088", "downloaded": False},
            {"id": 19, "ticker": "UNH", "title": "UNITEDHEALTH GROUP INC", "cik": "0000731766", "downloaded": False},
            {"id": 20, "ticker": "COST", "title": "COSTCO WHOLESALE CORP /NEW", "cik": "0000909832", "downloaded": False},
            {"id": 21, "ticker": "HD", "title": "HOME DEPOT, INC.", "cik": "0000354950", "downloaded": False},
            {"id": 22, "ticker": "PG", "title": "PROCTER & GAMBLE Co", "cik": "0000080424", "downloaded": False},
            {"id": 23, "ticker": "NFLX", "title": "NETFLIX INC", "cik": "0001065280", "downloaded": False},
            {"id": 24, "ticker": "JNJ", "title": "JOHNSON & JOHNSON", "cik": "0000200406", "downloaded": False},
            {"id": 25, "ticker": "BAC", "title": "BANK OF AMERICA CORP /DE/", "cik": "0000070858", "downloaded": False},
            {"id": 26, "ticker": "CRM", "title": "Salesforce, Inc.", "cik": "0001108524", "downloaded": False},
            {"id": 27, "ticker": "ABBV", "title": "AbbVie Inc.", "cik": "0001551152", "downloaded": False},
            {"id": 28, "ticker": "SAP", "title": "SAP SE", "cik": "0001000184", "downloaded": False},
            {"id": 29, "ticker": "ASML", "title": "ASML HOLDING NV", "cik": "0000937966", "downloaded": False},
            {"id": 30, "ticker": "RCIT", "title": "REELCAUSE INC", "cik": "0002008670", "downloaded": False},
            {"id": 31, "ticker": "KO", "title": "COCA COLA CO", "cik": "0000021344", "downloaded": False},
            {"id": 32, "ticker": "CVX", "title": "CHEVRON CORP", "cik": "0000093410", "downloaded": False},
            {"id": 33, "ticker": "TMUS", "title": "T-Mobile US, Inc.", "cik": "0001283699", "downloaded": False},
            {"id": 34, "ticker": "MRK", "title": "Merck & Co., Inc.", "cik": "0000310158", "downloaded": False},
            {"id": 35, "ticker": "WFC", "title": "WELLS FARGO & COMPANY/MN", "cik": "0000072971", "downloaded": False},
            {"id": 36, "ticker": "CSCO", "title": "CISCO SYSTEMS, INC.", "cik": "0000858877", "downloaded": False},
            {"id": 37, "ticker": "TM", "title": "TOYOTA MOTOR CORP/", "cik": "0001094517", "downloaded": False},
            {"id": 38, "ticker": "NOW", "title": "ServiceNow, Inc.", "cik": "0001373715", "downloaded": False},
            {"id": 39, "ticker": "BX", "title": "Blackstone Inc.", "cik": "0001393818", "downloaded": False},
            {"id": 40, "ticker": "ACN", "title": "Accenture plc", "cik": "0001467373", "downloaded": False},
            {"id": 41, "ticker": "PEP", "title": "PEPSICO INC", "cik": "0000077476", "downloaded": False},
            {"id": 42, "ticker": "AXP", "title": "AMERICAN EXPRESS CO", "cik": "0000004962", "downloaded": False},
            {"id": 43, "ticker": "MCD", "title": "MCDONALDS CORP", "cik": "0000063908", "downloaded": False},
            {"id": 44, "ticker": "IBM", "title": "INTERNATIONAL BUSINESS MACHINES CORP", "cik": "0000051143", "downloaded": False},
            {"id": 45, "ticker": "QQQ", "title": "INVESCO QQQ TRUST, SERIES 1", "cik": "0001067839", "downloaded": False},
            {"id": 46, "ticker": "BABA", "title": "Alibaba Group Holding Ltd", "cik": "0001577552", "downloaded": False},
            {"id": 47, "ticker": "AZN", "title": "ASTRAZENECA PLC", "cik": "0000901832", "downloaded": False},
            {"id": 48, "ticker": "MS", "title": "MORGAN STANLEY", "cik": "0000895421", "downloaded": False},
            {"id": 49, "ticker": "LIN", "title": "LINDE PLC", "cik": "0001707925", "downloaded": False},
            {"id": 50, "ticker": "DIS", "title": "Walt Disney Co", "cik": "0001744489", "downloaded": False},
            {"id": 51, "ticker": "TMO", "title": "THERMO FISHER SCIENTIFIC INC.", "cik": "0000097745", "downloaded": False},
            {"id": 52, "ticker": "AMD", "title": "ADVANCED MICRO DEVICES INC", "cik": "0000002488", "downloaded": False},
            {"id": 53, "ticker": "NVS", "title": "NOVARTIS AG", "cik": "0001114448", "downloaded": False},
            {"id": 54, "ticker": "ADBE", "title": "ADOBE INC.", "cik": "0000796343", "downloaded": False},
            {"id": 55, "ticker": "ABT", "title": "ABBOTT LABORATORIES", "cik": "0000001800", "downloaded": False},
            {"id": 56, "ticker": "PM", "title": "Philip Morris International Inc.", "cik": "0001413329", "downloaded": False},
            {"id": 57, "ticker": "ISRG", "title": "INTUITIVE SURGICAL INC", "cik": "0001035267", "downloaded": False},
            {"id": 58, "ticker": "SHEL", "title": "Shell plc", "cik": "0001306965", "downloaded": False},
            {"id": 59, "ticker": "INTU", "title": "INTUIT INC.", "cik": "0000896878", "downloaded": False},
            {"id": 60, "ticker": "CAT", "title": "CATERPILLAR INC", "cik": "0000018230", "downloaded": False},
            {"id": 61, "ticker": "GS", "title": "GOLDMAN SACHS GROUP INC", "cik": "0000886982", "downloaded": False},
            {"id": 62, "ticker": "GE", "title": "GENERAL ELECTRIC CO", "cik": "0000040545", "downloaded": False},
            {"id": 63, "ticker": "QCOM", "title": "QUALCOMM INC/DE", "cik": "0000804328", "downloaded": False},
            {"id": 64, "ticker": "HSBC", "title": "HSBC HOLDINGS PLC", "cik": "0001089113", "downloaded": False},
            {"id": 65, "ticker": "SBUX", "title": "STARBUCKS CORP", "cik": "0000829224", "downloaded": False},
            {"id": 66, "ticker": "BIDU", "title": "BAIDU, INC.", "cik": "0001329099", "downloaded": False},
            {"id": 67, "ticker": "SYY", "title": "SYSCO CORP", "cik": "0000089154", "downloaded": False},
            {"id": 68, "ticker": "GEHC", "title": "GE HEALTHCARE TECHNOLOGIES INC.", "cik": "0001960174", "downloaded": False},
            {"id": 69, "ticker": "FIS", "title": "FISERV, INC.", "cik": "0001020922", "downloaded": False},
            {"id": 70, "ticker": "MELI", "title": "MercadoLibre, Inc.", "cik": "0001288776", "downloaded": False},
        ]
        
        return Response(companies, status=status.HTTP_200_OK)

    
class ProcessCIDView(View):
    def post(self, request):
        try:
            # Parse the JSON body
            # Get 'cid' from query parameters
            cid = request.GET.get('cid')
            
            if not cid:
                return JsonResponse({"error": "Missing 'cid' parameter"}, status=400)
            
            # Call the function with the provided 'cid'
            result = download_sec_filings(cid, num_filings=3)
            
            # Return a success response
            return JsonResponse({"message": result}, status=200)
        except Exception as e:
            return JsonResponse({"error":f"error downloading fillings {e}"},status = 500)


class AnalyseCIDView(View):
    def post(self, request):
        try:
            # Parse the JSON body
            # Get 'cid' from query parameters
            cid = request.GET.get('cid')
            
            if not cid:
                return JsonResponse({"error": "Missing 'cid' parameter"}, status=400)
            
            
            
            # Call the function with the provided 'cid'
            result = process_data(cid)
            
            # Return a success response
            return JsonResponse({"message": result}, status=200)
        except Exception as e:
            return JsonResponse({"error":f"error analysing fillings {e}"},status = 500)