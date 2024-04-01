import asyncio
import logging
import json
from requests_oauthlib import OAuth1Session
from typing import List
from config import Config

async def post_to_twitter(contents: List[str]):
    config = Config()
    api_url = config.twitter_api_url
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_token_secret = config.access_token_secret

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

    for content in contents:
        await asyncio.sleep(config.post_interval)
        payload = json.dumps({"text": content})
        headers = {"Content-Type": "application/json"}

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: oauth.post(api_url, data=payload, headers=headers))

        if response.status_code == 201:
            logging.info("Content successfully posted to Twitter.")
        else:
            await handle_error(response)

async def handle_error(response):
    error_message = "Failed to post content to Twitter."
    try:
        error_details = response.json().get('errors', [])
        error_message += " " + "; ".join([error.get('message', 'Unknown error') for error in error_details])
    except Exception as e:
        error_message += f" Additionally, failed to parse JSON response: {str(e)}"
    logging.error(error_message)

    if response.status_code >= 500:
        retry_after = int(response.headers.get('Retry-After', 60))
        logging.warning(f"Server error occurred. Retrying after {retry_after} seconds.")
        await asyncio.sleep(retry_after)
        await post_to_twitter([error_message])
    elif response.status_code == 401:
        logging.error("Authentication error occurred. Please check your credentials.")
    elif response.status_code >= 400:
        logging.error("Client error occurred. Terminating process.")
        raise Exception(error_message)