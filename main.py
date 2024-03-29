import logging
from dotenv import load_dotenv
from ai.content_generator import generate_content
from api.x_api_client import post_to_x
from db.database import check_and_update_post_history

# 環境変数の読み込み
load_dotenv()

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting content generation process.")
    try:
        content = generate_content()
        if content and check_and_update_post_history(content):
            post_to_x(content)
            logging.info("Content successfully posted to X.")
        else:
            logging.warning("Duplicate content detected or no content generated. Skipping posting.")
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
