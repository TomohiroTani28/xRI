import asyncio
import logging
from dotenv import load_dotenv
from ai.content_generator import generate_content
from api.x_api_client import post_to_x
from db.database import check_and_update_post_history
from utils.helpers import setup_logging

# .envファイルから環境変数を読み込む
load_dotenv()

async def main():
    setup_logging()
    logging.info("Starting content generation process.")
    
    content = generate_content()
    if content:
        if await check_and_update_post_history(content):
            await post_to_x(content)
        else:
            logging.warning("Duplicate content detected. Skipping posting.")
    else:
        logging.warning("No content generated. Skipping posting.")

if __name__ == "__main__":
    asyncio.run(main())
