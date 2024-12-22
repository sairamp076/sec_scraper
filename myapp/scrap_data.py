import requests
from bs4 import BeautifulSoup
import os
from myapp.models import *


# Create a directory to store the filings


def download_sec_filings(cik, num_filings=5):
    """
    Download SEC 10-K filings for a given company CIK (Central Index Key).
    Args:
        cik (str): The CIK number of the company.
        num_filings (int): Number of filings to download.
    """
    base_url = "https://www.sec.gov"
    search_url = f"{base_url}/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K&count={num_filings}&output=atom"
    
    # Send a request to EDGAR
    headers = {"User-Agent": "YourName YourEmail@example.com"}
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch filings.")
        return

    # Parse the response to extract links to filings
    soup = BeautifulSoup(response.content, features="xml")
    entries = soup.find_all("entry")
    
    for idx, entry in enumerate(entries, start=1):
        filing_url = entry.find("filing-href").text.replace("-index.html", ".txt")
        filing_response = requests.get(filing_url, headers=headers)
        if filing_response.status_code == 200:
            os.makedirs(f"sec_filings/{cik}", exist_ok=True)
            file_path = f"sec_filings/{cik}/filing_{idx}.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(filing_response.text)
            Company.objects.filter(cik=cik).update(downloaded = True)
            print(f"Downloaded filing {idx}: {file_path}")
        else:
            print(f"Failed to download filing {idx}")

# # Example usage
# if __name__ == "__main__":
#     company_cik = "0000320193"  # Example: Apple Inc.'s CIK
#     download_sec_filings(company_cik, num_filings=3)
