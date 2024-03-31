import asyncio
import logging
import json
from requests_oauthlib import OAuth1Session
import os

async def post_to_x(contents):
    api_url = "https://api.twitter.com/2/tweets"
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

    for content in contents:
        payload = json.dumps({"text": content})
        headers = {"Content-Type": "application/json"}

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: oauth.post(api_url, data=payload, headers=headers))
        
        if response.status_code == 201:
            logging.info("Content successfully posted to Twitter.")
        else:
            error_message = f"Failed to post content to Twitter: Status Code {response.status_code}"
            try:
                response_body = response.json()
                if 'errors' in response_body:
                    for error in response_body['errors']:
                        detail = error.get('detail', 'No detailed error message provided.')
                        error_message += f"; Error detail: {detail}"
                else:
                    error_message += "; No error details provided by API."
            except Exception:
                error_message += "; Failed to parse JSON response."
            logging.error(error_message)
