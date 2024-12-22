import requests
import pandas as pd
from django.core.management.base import BaseCommand
from myapp.models import Company

class Command(BaseCommand):
    help = 'Import companies data from SEC'

    def handle(self, *args, **kwargs):
        headers = {'User-Agent': "email@address.com"}

        # Fetch company tickers from SEC
        response = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=headers
        )
        company_data = response.json()

        # Convert JSON data to DataFrame
        company_df = pd.DataFrame.from_dict(company_data, orient='index')

        # Add leading zeros to CIK
        company_df['cik_str'] = company_df['cik_str'].astype(str).str.zfill(10)

        # Iterate through the DataFrame and save each record to the database
        for _, row in company_df.iterrows():
            Company.objects.update_or_create(
                cik=row['cik_str'],
                defaults={
                    'ticker': row['ticker'],
                    'title': row['title'],
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully imported companies!'))
