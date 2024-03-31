import asyncio
import logging
from dotenv import load_dotenv
from ai.content_generator import generate_content
from api.x_api_client import post_to_x
from db.database import check_and_update_post_history
from utils.helpers import setup_logging, split_text_into_posts, clean_text

load_dotenv()

async def main():
    setup_logging()
    logging.info("Starting content generation process.")
    
    content = generate_content()
    if content:
        content = clean_text(content)
        posts = split_text_into_posts(content)
        for post in posts:
            if await check_and_update_post_history(post):
                await post_to_x([post])
            else:
                logging.warning("Duplicate content detected. Skipping posting.")
    else:
        logging.warning("No content generated. Skipping posting.")

if __name__ == "__main__":
    asyncio.run(main())
