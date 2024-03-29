import logging
import re
from datetime import datetime

def setup_logging(level=logging.INFO):
    """
    アプリケーション全体のロギング設定をカスタマイズ可能な方法で初期化します。
    デフォルトではINFOレベルでログを記録します。
    
    Parameters:
        level (logging.LEVEL): ロギングレベル。
    """
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def clean_text(text, remove_urls=True, remove_html=True, remove_special_chars=True):
    """
    与えられたテキストから不要な文字やマークアップを条件に応じて削除します。
    
    Parameters:
        text (str): クリーニングするテキスト。
        remove_urls (bool): URLを削除するかどうか。
        remove_html (bool): HTMLタグを削除するかどうか。
        remove_special_chars (bool): 特殊文字を削除するかどうか。
    
    Returns:
        str: クリーニングされたテキスト。
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
    指定された日付と時刻をフォーマットします。指定がない場合は現在の日付と時刻を使用します。
    
    Parameters:
        date_time (datetime.datetime, optional): フォーマットする日付と時刻。
        date_format (str): 日付と時刻のフォーマット文字列。
    
    Returns:
        str: フォーマットされた日付と時刻の文字列。
    """
    if date_time is None:
        date_time = datetime.now()
    return date_time.strftime(date_format)

# 使用例
if __name__ == "__main__":
    setup_logging()

    example_text = "<p>This is a <a href='https://example.com'>link</a>.</p> Visit https://example.com for more info."
    cleaned_text = clean_text(example_text, remove_urls=False)  # URLを残してクリーニング
    logging.info(f"Cleaned text with URLs: {cleaned_text}")

    specific_datetime = datetime(2020, 1, 1, 12, 0)
    formatted_date = format_datetime(specific_datetime)
    logging.info(f"Formatted specific datetime: {formatted_date}")
