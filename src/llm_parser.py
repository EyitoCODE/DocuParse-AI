import openai
import json
import os
from dotenv import load_dotenv

# Load API key from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_lease_data(raw_text):
    """
    Sends raw lease text to OpenAI to extract structured JSON data.
    """
    prompt = f"""
    You are an expert real estate data extraction assistant. 
    Review the following lease agreement text and extract the key information into a strict JSON format.
    
    Required JSON keys:
    - "tenant_name" (string)
    - "rent_amount" (number)
    - "lease_start_date" (string, format YYYY-MM-DD)
    - "lease_end_date" (string, format YYYY-MM-DD)
    
    If a value cannot be found, use null.
    
    Lease Text:
    {raw_text[:4000]} 
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You output strict, valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.0 # Setting temperature to 0.0 ensures deterministic, factual output
        )
        
        json_output = response.choices[0].message.content
        return json.loads(json_output)
        
    except Exception as e:
        print(f"LLM Parsing Error: {e}")
        return {"tenant_name": None, "rent_amount": None, "lease_start_date": None, "lease_end_date": None}