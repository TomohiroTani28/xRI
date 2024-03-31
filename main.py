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
            logging.debug(f"Generated content: {content}")  # Log the entire generated content for deeper analysis
            content = clean_text(content)
            posts = split_text_into_posts(content)
            for post in posts:
                logging.info(f"Prepared to post: '{post}' (Length: {len(post)})")  # More detailed log before posting
                if len(post) > 280:
                    logging.error("Prepared post exceeds Twitter's character limit.")
                    continue  # Skip attempting to post if it exceeds the limit
                if await check_and_update_post_history(post):
                    try:
                        await post_to_x([post])
                        logging.info("Post successful.")
                    except Exception as e:
                        logging.error(f"Failed during posting to Twitter: {e}")
                else:
                    logging.warning("Duplicate content detected. Skipping posting.")
        else:
            logging.warning("No content generated. Skipping posting.")
    except Exception as e:
        logging.error(f"An overall error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
