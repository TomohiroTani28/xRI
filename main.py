import logging
from dotenv import load_dotenv
from ai.content_generator import generate_content
from api.x_api_client import post_to_x
from db.database import check_and_update_post_history
from utils.helpers import setup_logging

def main():
    setup_logging()
    logging.info("Starting content generation process.")
    
    content = generate_content()
    if content and check_and_update_post_history(content):
        post_to_x(content)
    else:
        logging.warning("Duplicate content detected or no content generated. Skipping posting.")

if __name__ == "__main__":
    main()
