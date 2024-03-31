import logging
import os
import replicate
import asyncio

logging.basicConfig(level=logging.INFO)

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    logging.error("REPLICATE_API_TOKEN not set. Please set the environment variable.")
    exit(1)

replicate.api_token = REPLICATE_API_TOKEN

async def generate_content_with_llama2(prompt):
    try:
        response = await replicate.predictions.create(
            version="meta/llama-2-70b-chat",
            input={
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 500,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
            }
        )
        if response and 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['text'].strip()
        else:
            return "No content generated."
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return None

async def main():
    prompts = [
        "2024年のインドネシアの不動産市場のトレンドについて分析してください。",
        # Add more prompts as necessary
    ]
    for prompt in prompts:
        content = await generate_content_with_llama2(prompt)
        if content:
            logging.info(f"Generated content for prompt '{prompt}': {content}")
        else:
            logging.info(f"Failed to generate content for prompt '{prompt}'.")

if __name__ == "__main__":
    asyncio.run(main())
