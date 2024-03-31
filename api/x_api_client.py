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
        
        if response.status_code == 201:  # Successfully created
            logging.info("Content successfully posted to Twitter.")
        else:
            try:
                # Attempt to raise status to trigger exception for handling
                response.raise_for_status()
            except Exception as e:
                error_message = f"Failed to post content to Twitter: {e}"
                # Attempt to extract detailed error information
                try:
                    response_body = response.json()
                    error_details = response_body.get('errors', [])
                    for error in error_details:
                        detail = error.get('detail', 'No detailed error message provided.')
                        error_message += f" Error detail: {detail}"
                except Exception as json_parse_error:
                    error_message += " Additionally, failed to parse JSON response."
                logging.error(error_message)
            else:
                # Log as successful only if no exceptions are raised and status is not 201
                logging.info("Post successful, but received unexpected status code.")
