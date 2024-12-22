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

class CompanyListView(APIView):
    """
    API endpoint to fetch all companies.
    """

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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