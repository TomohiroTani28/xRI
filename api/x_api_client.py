import asyncio
import logging
from requests_oauthlib import OAuth1Session
import os
import json

async def post_to_x(content):
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

    headers = {"Content-Type": "application/json"}
    payload = {"text": content}

    # run_in_executor を使用して非同期にリクエストを送信
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: oauth.post(api_url, json=payload, headers=headers))
    
    try:
        response.raise_for_status()
        logging.info("Content successfully posted to Twitter.")
    except Exception as e:
        logging.error(f"Failed to post content to Twitter: {e}")
