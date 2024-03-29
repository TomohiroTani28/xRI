import requests
import logging
import os

def post_to_x(content):
    api_url = "https://api.x.com/2/tweets"
    headers = {"Authorization": f"Bearer {os.getenv('X_API_KEY')}"}
    data = {"text": content}
    
    try:
        response = requests.post(api_url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        logging.info("Content successfully posted to X.")
    except requests.exceptions.RequestException as e:
        logging.error("Failed to post content to X: %s", e, exc_info=True)
