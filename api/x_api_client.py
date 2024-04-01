import asyncio
import logging
import json
from requests_oauthlib import OAuth1Session
import os
import random

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
        await asyncio.sleep(random.randint(1, 5))
        payload = json.dumps({"text": content})
        headers = {"Content-Type": "application/json"}

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: oauth.post(api_url, data=payload, headers=headers))

        if response.status_code == 201:
            logging.info("Content successfully posted to Twitter.")
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 900))
            logging.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            await asyncio.sleep(retry_after)
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
