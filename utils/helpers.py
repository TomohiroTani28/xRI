import logging
import re
from datetime import datetime

def setup_logging(level=logging.INFO):
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def clean_text(text, remove_urls=True, remove_html=True, remove_special_chars=True):
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
    """テキストを文に分割します。日本語テキストを考慮して、句点を基準に分割します。"""
    sentences = re.split(r'(?<=[。！？])\s*', text)
    return sentences

def split_text_into_posts(text, max_length=280):
    sentences = split_text_into_sentences(text)
    posts = []
    current_post = ""

    for sentence in sentences:
        # Check if adding the next sentence exceeds the limit
        next_post = f"{current_post} {sentence}".strip()
        if len(next_post) <= max_length:
            current_post = next_post
        else:
            if current_post:  # Avoid appending empty strings
                posts.append(current_post)
                logging.debug(f"Added post: {current_post} (Length: {len(current_post)})")  # Enhanced debug log
            current_post = sentence

    # Adding the last portion if it's not empty
    if current_post:
        posts.append(current_post)
        logging.debug(f"Added final post: {current_post} (Length: {len(current_post)})")  # Enhanced debug log

    return posts
