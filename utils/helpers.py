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

def split_text_into_posts(text, max_length=280):
    """テキストを自然な区切りで分割し、各ポストが280文字を超えないようにします。"""
    posts = []
    while text:
        if len(text) <= max_length:
            posts.append(text)
            break
        cut_off = text.rfind(' ', 0, max_length)
        if cut_off == -1:  # スペースが見つからない場合は、max_lengthで強制的に分割
            cut_off = max_length
        posts.append(text[:cut_off])
        text = text[cut_off:].strip()
    return posts