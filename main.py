import asyncio
import logging
from dotenv import load_dotenv
from ai.content_generator import generate_content  # async_content_generatorから変更
from api.x_api_client import post_to_x
from db.database import check_and_update_post_history
from utils.helpers import setup_logging

async def main():
    setup_logging()
    logging.info("Starting content generation process.")
    
    content = generate_content()  # awaitを削除
    if content and await check_and_update_post_history(content):  # awaitを保持
        await post_to_x(content)  # awaitを保持
    else:
        logging.warning("Duplicate content detected or no content generated. Skipping posting.")

if __name__ == "__main__":
    asyncio.run(main())
