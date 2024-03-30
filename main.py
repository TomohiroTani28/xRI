import asyncio
import logging
from ai.content_generator import generate_content
from api.x_api_client import post_to_x
from db.database import check_and_update_post_history
from utils.helpers import setup_logging

async def main():
    setup_logging()
    logging.info("Starting content generation process.")

    content = await generate_content()
    if content and await check_and_update_post_history(content):
        await post_to_x(content)
    else:
        # Breaking the long line (E501) by using implicit string concatenation
        logging.warning(
            "Duplicate content detected or no content generated. "
            "Skipping posting."
        )

if __name__ == "__main__":
    asyncio.run(main())
