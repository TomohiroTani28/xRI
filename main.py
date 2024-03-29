import asyncio
import logging
from dotenv import load_dotenv
# 非同期版の関数をインポート
from ai.async_content_generator import generate_content
from api.async_x_api_client import post_to_x
from db.async_database import check_and_update_post_history
from utils.helpers import setup_logging

async def main():
    setup_logging()
    logging.info("Starting content generation process.")
    
    content = await generate_content()
    if content and await check_and_update_post_history(content):
        await post_to_x(content)
    else:
        logging.warning("Duplicate content detected or no content generated. Skipping posting.")

if __name__ == "__main__":
    asyncio.run(main())
