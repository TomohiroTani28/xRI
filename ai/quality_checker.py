import logging
from typing import List
from ai.sentiment_analysis import analyze_sentiment

async def check_content_quality(generated_texts: List[str]) -> List[str]:
    checked_texts = []
    for text in generated_texts:
        sentiment_score = await analyze_sentiment(text)
        if sentiment_score < 0:
            logging.warning(f"Negative sentiment detected in generated text: {text}")
            continue
        checked_texts.append(text)
    return checked_texts