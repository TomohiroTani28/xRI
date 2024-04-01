import asyncio
import logging
from ai.content_generator import generate_content
from api.twitter_client import post_to_twitter
from utils.helpers import setup_logging, clean_text, split_text_into_posts, add_media, add_hashtags, optimize_hashtags, analyze_post_performance
from utils.interaction import setup_auto_reply, schedule_qa_sessions
from utils.content_manager import review_content, edit_content

def prepare_posts(content):
    cleaned_content = clean_text(content)
    posts = split_text_into_posts(cleaned_content)
    posts = add_media(posts)
    posts = add_hashtags(posts)
    posts = optimize_hashtags(posts)
    return posts

async def main():
    setup_logging()
    logging.info("Starting content generation process.")

    prompts = [
        "2024年のインドネシアの不動産市場のトレンドについて分析してください。",
        "インドネシアの不動産投資に関する注意点を教えてください。",
        "インドネシアの不動産投資の魅力は何ですか?",
        "インドネシアの不動産市場における将来の見通しを教えてください。",
        "インドネシアの不動産投資で成功するためのコツを教えてください。"
    ]

    generated_texts = await generate_content(prompts)
    reviewed_texts = [await review_content(text) for text in generated_texts]
    edited_texts = [await edit_content(text) for text in reviewed_texts if text]

    for content in edited_texts:
        logging.debug(f"Generated content: {content}")
        posts = prepare_posts(content)

        for post in posts:
            logging.info(f"Prepared to post: '{post}' (Length: {len(post)})")
            if len(post) > 280:
                logging.error("Prepared post exceeds Twitter's character limit.")
                continue
            await post_to_twitter([post])

    await setup_auto_reply()
    await schedule_qa_sessions()
    await analyze_post_performance()

if __name__ == "__main__":
    asyncio.run(main())