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
    
    try:
        content = generate_content()
        if content:
            logging.debug(f"Original content: {content[:100]}...")  # Provides a snapshot of the generated content
            content = clean_text(content)
            posts = split_text_into_posts(content)
            for post in posts:
                logging.info(f"Attempting to post: {post[:50]}... (Length: {len(post)})")
                if await check_and_update_post_history(post):
                    try:
                        await post_to_x([post])
                        logging.info("Post successful.")
                    except Exception as e:
                        logging.error(f"Failed during posting to Twitter: {e}")
                else:
                    logging.warning("Duplicate content detected. Skipping posting.")
    except Exception as e:
        logging.error(f"An overall error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
