import logging
from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

async def analyze_sentiment(text: str) -> int:
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    sentiment_score = torch.argmax(outputs.logits).item()
    return sentiment_score