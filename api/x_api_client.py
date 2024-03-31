import asyncio
import logging
import json
from requests_oauthlib import OAuth1Session
import os
import time

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
        elif response.status_code == 429:
            try:
                retry_after = int(response.headers.get('Retry-After', 900))  # Default to 15 minutes if header is missing
                logging.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
            except ValueError:
                logging.error("Failed to parse 'Retry-After' header. Retrying after default period.")
                time.sleep(900)  # Default wait time of 15 minutes
        else:
            error_message = f"Failed to post content to Twitter: Status Code {response.status_code}"
            try:
                response_body = response.json()
                if 'errors' in response_body:
                    error_details = "; ".join([f"Error: {error.get('message')}" for error in response_body['errors']])
                    error_message += f"; Error detail: {error_details}"
                else:
                    error_message += "; No error details provided by API."
            except Exception as e:
                error_message += f"; Additionally, failed to parse JSON response: {str(e)}"
            logging.error(error_message)
