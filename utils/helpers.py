import logging
import re
from datetime import datetime

def setup_logging(level=logging.INFO):
    """
    Configures the logging level and format.
    """
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def clean_text(text, remove_urls=True, remove_html=True, remove_special_chars=True):
    """
    Cleans the given text by removing URLs, HTML tags, and special characters.
    """
    if remove_html:
        text = re.sub(r'<.*?>', '', text)
    if remove_urls:
        text = re.sub(r'http\S+', '', text)
    if remove_special_chars:
        text = re.sub(r'[^\w\s]', '', text)
    return text

def format_datetime(date_time=None, date_format="%Y-%m-%d %H:%M:%S"):
    """
    Formats the given datetime object or the current datetime if none is provided.
    """
    if date_time is None:
        date_time = datetime.now()
    return date_time.strftime(date_format)

def split_text_into_sentences(text):
    """
    Splits the given text into a list of sentences based on Japanese punctuation.
    """
    sentences = re.split(r'(?<=[。！？])\s*', text)
    return sentences

def split_text_into_posts(text, max_length=280):
    """
    Splits the given text into a list of posts, each not exceeding the specified maximum length.
    This function ensures that the split respects word boundaries and does not break text mid-word.
    """
    sentences = split_text_into_sentences(text)
    posts = []
    current_post = ""

    for sentence in sentences:
        # Attempt to add the next sentence to the current post.
        next_post = f"{current_post} {sentence}".strip()
        # If adding the next sentence would exceed the max_length, finalize the current post and start a new one.
        if len(next_post) <= max_length:
            current_post = next_post
        else:
            if current_post:  # Ensure the current post is not empty before adding it to the list of posts.
                posts.append(current_post)
                logging.debug(f"Added post: {current_post} (Length: {len(current_post)})")
            current_post = sentence

    # Add the final post if it's not empty.
    if current_post:
        posts.append(current_post)
        logging.debug(f"Added final post: {current_post} (Length: {len(current_post)})")

    return posts
