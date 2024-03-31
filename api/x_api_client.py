import asyncio
import logging
import json
from requests_oauthlib import OAuth1Session
import os

async def post_to_x(content):
    api_url = "https://api.twitter.com/2/tweets"
    # 環境変数から認証情報を取得
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    # OAuth1Session オブジェクトを使用して認証
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

    # リクエストボディを JSON でエンコード
    payload = json.dumps({"text": content})
    headers = {"Content-Type": "application/json"}

    # 非同期処理のためにrun_in_executorを使用してリクエストを送信
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: oauth.post(api_url, headers=headers, data=payload))
    
    try:
        response.raise_for_status()
        logging.info("Content successfully posted to Twitter.")
    except Exception as e:
        logging.error(f"Failed to post content to Twitter: {e}")
