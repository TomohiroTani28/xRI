import aiohttp
import asyncio
import logging
import os

async def post_to_x(content):
    api_url = "https://api.x.com/2/tweets"
    headers = {"Authorization": f"Bearer {os.getenv('X_API_KEY')}"}
    data = {"text": content}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(api_url, json=data, headers=headers) as response:
                await response.raise_for_status()
                logging.info("Content successfully posted to X.")
        except aiohttp.ClientError as e:
            logging.error(f"Failed to post content to X: {e}")
