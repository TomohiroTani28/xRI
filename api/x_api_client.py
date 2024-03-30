import asyncio
import logging
from requests_oauthlib import OAuth1Session  # OAuth1Sessionをインポート
import os

async def post_to_x(content):
    api_url = "https://api.twitter.com/2/tweets"  # Twitter APIのURLに変更
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

    data = {"text": content}
    
    # 非同期処理のためにrun_in_executorを使用
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: oauth.post(api_url, data={"text": content}))
    
    try:
        response.raise_for_status()
        logging.info("Content successfully posted to X.")
    except Exception as e:
        logging.error(f"Failed to post content to X: {e}")

# 必要に応じて、.envファイルや環境変数の設定方法を更新して、
# CONSUMER_KEY、CONSUMER_SECRET、ACCESS_TOKEN、ACCESS_TOKEN_SECRETが含まれるようにしてください。
