import logging
import re
from datetime import datetime
from typing import List
import os
import random
from config import Config
from utils.hashtag_optimizer import optimize_hashtags

def setup_logging(level=logging.INFO):
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def clean_text(text, remove_urls=True, remove_html=True, remove_special_chars=True):
    text = str(text)
    if remove_html:
        text = re.sub(r'<.*?>', '', text)
    if remove_urls:
        text = re.sub(r'http\S+', '', text)
    if remove_special_chars:
        text = re.sub(r'[^\w\s]', '', text)
    return text

def format_datetime(date_time=None, date_format="%Y-%m-%d %H:%M:%S"):
    if date_time is None:
        date_time = datetime.now()
    return date_time.strftime(date_format)

def split_text_into_sentences(text):
    sentences = re.split(r'(?<=[。！？])\s*', text)
    return sentences

def split_text_into_posts(text, max_length=280):
    sentences = split_text_into_sentences(text)
    posts = []
    current_post = ""

    for sentence in sentences:
        next_post = f"{current_post} {sentence}".strip()
        if len(next_post) <= max_length:
            current_post = next_post
        else:
            if current_post:
                posts.append(current_post)
                logging.debug(f"Added post: {current_post} (Length: {len(current_post)})")
            current_post = sentence

    if current_post:
        posts.append(current_post)
        logging.debug(f"Added final post: {current_post} (Length: {len(current_post)})")

    return posts

def add_media(posts: List[str]) -> List[str]:
    config = Config()
    media_dir = config.media_dir
    if not os.path.exists(media_dir):
        logging.warning(f"Media directory '{media_dir}' does not exist. Skipping media addition.")
        return posts

    media_files = os.listdir(media_dir)
    if not media_files:
        logging.warning("No media files found in the media directory. Skipping media addition.")
        return posts

    new_posts = []
    for post in posts:
        media_file = random.choice(media_files)
        media_path = os.path.join(media_dir, media_file)
        post += f"\n\nMedia: {media_path}"
        new_posts.append(post)

    return new_posts

def add_hashtags(posts: List[str]) -> List[str]:
    config = Config()
    hashtags = config.hashtags

    new_posts = []
    for post in posts:
        hashtag_str = " ".join([f"#{hashtag}" for hashtag in hashtags])
        post += f"\n{hashtag_str}"
        new_posts.append(post)

    return new_posts

async def analyze_post_performance():
    # TODO: Twitter APIを使用して投稿のパフォーマンスを分析する
    pass