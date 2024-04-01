import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.model_name = "elyza/ELYZA-japanese-Llama-2-13b"
        self.twitter_api_url = "https://api.twitter.com/2/tweets"
        self.consumer_key = os.environ.get("CONSUMER_KEY")
        self.consumer_secret = os.environ.get("CONSUMER_SECRET")
        self.access_token = os.environ.get("ACCESS_TOKEN")
        self.access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
        self.post_interval = 600
        self.media_dir = "media"
        self.hashtags = ["#インドネシア不動産", "#海外不動産投資", "#不動産投資"]