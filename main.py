import asyncio
import logging
from dotenv import load_dotenv
# from ai.content_generator import generate_content  # 古いインポート文を削除
from ai.content_generator import main as generate_content  # 新しいインポート文
from api.x_api_client import post_to_x
from db.database import check_and_update_post_history
from utils.helpers import setup_logging, clean_text, split_text_into_posts

load_dotenv()

async def main():
    setup_logging()
    logging.info("Starting content generation process.")
    
    await generate_content()  # 修正: generate_contentの実行
    
    # 以下のコードは、必要に応じて使用
    # contents = generate_content()  # この行は非同期関数を直接呼び出せないため、修正が必要
    # for content in contents:
    #     logging.debug(f"Generated content: {content}")  # Log the entire generated content for deeper analysis
    #     cleaned_content = clean_text(content)
    #     posts = split_text_into_posts(cleaned_content)
    #     for post in posts:
    #         logging.info(f"Prepared to post: '{post}' (Length: {len(post)})")
    #         if len(post) > 280:
    #             logging.error("Prepared post exceeds Twitter's character limit.")
    #             continue  # Skip attempting to post if it exceeds the limit
    #         if await check_and_update_post_history(post):
    #             await post_to_x([post])
    #         else:
    #             logging.warning("Duplicate content detected. Skipping posting.")

if __name__ == "__main__":
    asyncio.run(main())  # 非同期関数を適切に実行
