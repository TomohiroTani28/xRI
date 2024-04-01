import logging
from typing import List
import aiohttp

async def fetch_real_estate_data(location: str) -> dict:
    url = f"https://api.example.com/real-estate-data?location={location}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(f"Failed to fetch real estate data for {location}. Status: {response.status}")
                return {}

async def enrich_content_with_data(generated_texts: List[str]) -> List[str]:
    enriched_texts = []
    for text in generated_texts:
        location = extract_location(text)
        if location:
            data = await fetch_real_estate_data(location)
            if data:
                text += f"\n\nReal Estate Data for {location}:\n{format_data(data)}"
        enriched_texts.append(text)
    return enriched_texts

def extract_location(text: str) -> str:
    # TODO: 文章から場所を抽出するロジックを実装する
    return "Jakarta"

def format_data(data: dict) -> str:
    formatted_data = ""
    for key, value in data.items():
        formatted_data += f"{key}: {value}\n"
    return formatted_data