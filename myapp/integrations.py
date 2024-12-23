import requests
import os
import time
import json
import re

# Replace with your API key
GROQ_API_KEY = "VznREyhuYFjCooWQmKv4jjLuZjkEVnrH"

def analyze_filing(file_path):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    with open(file_path, "r", encoding="utf-8") as file:
        filing_text = file.read()

    data = {
        "model": "mistral-small-latest",
        "response_format" : { "type": "json_object" }  ,
        "messages": [
            {
                "role": "user",
                "content": "hi You are an expert in financial analysis. Analyze the following SEC 10-K filing and summarize key insights, risks, and financial trends and store main values in key value pairs in json and write to seperate json:\n\n the key value pairs should be in following format mainly risks "+filing_text
            }
        ]
    }

    retries = 0
    max_retries = 5
    backoff_factor = 2  # Exponential backoff
    while retries < max_retries:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            res = response.json()
            message = json.loads(res['choices'][0]['message']['content'])
            #json_data = extract_json_from_text(message)
            #if json_data:
             #   return json_data  # Return JSON object after successful extraction
            return message
        else:
            print(f"Error: {response.status_code}, Message: {response.text}")
            return None  # Return None if there's an error

        retries += 1
        time.sleep(backoff_factor ** retries)  # Exponential backoff

    print("Max retries exceeded.")
    return None  # If max retries reached, return None

def process_data(cid):
    # Directory containing downloaded filings
    filings_dir = f"sec_filings/{cid}"

    for file_name in os.listdir(filings_dir):
        file_path = os.path.join(filings_dir, file_name)
        print(f"\nAnalyzing {file_name}...\n")
        result = analyze_filing(file_path)
        if result:
            print(f"Analysis:\n{json.dumps(result, indent=4)}\n")
        return result

def extract_json_from_text(text):
    # Extract the JSON part from the text using regex
    match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
        try:
            json_data = json.loads(json_str)  # Convert the JSON string to a Python object
            return json_data  # Return the valid JSON object
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No JSON block found in the text.")
        return None

