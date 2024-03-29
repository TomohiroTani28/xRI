import requests
import logging
import os

def generate_content():
    api_url = "https://example.com/generate"
    headers = {"Authorization": f"Bearer {os.getenv('AI_API_KEY')}"}
    data = {"prompt": "インドネシアの不動産投資についての情報", "length": 250}
    
    try:
        response = requests.post(api_url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("content")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to generate content: {e}")
        return None
