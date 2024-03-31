import logging
import os
import replicate
import asyncio

# Ensure replicate and asyncio are installed via pip

logging.basicConfig(level=logging.INFO)

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    logging.error("REPLICATE_API_TOKEN not set. Please set the environment variable.")
    exit(1)

replicate.api_token = REPLICATE_API_TOKEN

async def generate_content_with_llama2(prompt):
    """
    Generate content using the Llama 2 API via the replicate client.
    """
    try:
        response = await replicate.predictions.create(
            model="meta/llama-2-70b-chat",
            input={
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 500,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
            },
            version="e3cbd1da23f3c76e9f4454f26f8bd6a7bcf01c540763655efb2fb49cd097e5ee",
        )
        # Process and return the generated content
        return response['text']
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return "Failed to generate content."

async def main():
    prompts = [
        "2024年のインドネシアの不動産市場のトレンドについて分析してください。",
        "現在、インドネシアの不動産セクターで最良の投資機会は何ですか？",
        "2024年にインドネシアで優勢になる不動産開発プロジェクトの予測を提供してください。",
        "インドネシアの経済成長とその不動産市場との関係について説明してください。",
    ]

    for prompt in prompts:
        content = await generate_content_with_llama2(prompt)
        if content:
            logging.info(f"Generated content for prompt '{prompt}': {content}")
        else:
            logging.error(f"Failed to generate content for prompt '{prompt}'.")

if __name__ == "__main__":
    asyncio.run(main())
