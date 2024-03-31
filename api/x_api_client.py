import asyncio
import logging
import json
from requests_oauthlib import OAuth1Session
import os

async def post_to_x(contents):  # 変更: 単一のcontentから複数のcontentsへ
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

    for content in contents:  # 複数のcontentsをループで処理
        payload = json.dumps({"text": content})
        headers = {"Content-Type": "application/json"}

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: oauth.post(api_url, data=payload, headers=headers))
        
        try:
            response.raise_for_status()
            logging.info("Content successfully posted to Twitter.")
        except Exception as e:
            error_message = f"Failed to post content to Twitter: {e}"
            try:
                response_body = response.json()
                error_message += f" Response: {response_body}"
            except Exception as json_error:
                error_message += " Failed to parse JSON response."
            logging.error(error_message)
