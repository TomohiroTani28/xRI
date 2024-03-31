import asyncio
import logging
import os
import replicate

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Set your Replicate API token
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    logging.error("REPLICATE_API_TOKEN not set. Please set the environment variable.")
    exit(1)

# Set the Replicate API token for authentication
replicate.api_token = REPLICATE_API_TOKEN

# Prompts for content generation
prompts = [
    "2024年のインドネシアの不動産市場のトレンドについて分析してください。",
    "現在、インドネシアの不動産セクターで最良の投資機会は何ですか？",
    "2024年にインドネシアで優勢になる不動産開発プロジェクトの予測を提供してください。",
    "インドネシアの経済成長とその不動産市場との関係について説明してください。",
]

async def generate_content_with_llama2(prompt):
    """
    Generate content using the Llama 2 API via the Replicate client.
    """
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
        # Assume the response structure contains a 'choices' list with the generated content
        if response and 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['text'].strip()
        else:
            return "No content generated."
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return None

async def main():
    """
    Generate content for each prompt using Llama 2 API.
    """
    tasks = [generate_content_with_llama2(prompt) for prompt in prompts]
    responses = await asyncio.gather(*tasks)
    
    for prompt, content in zip(prompts, responses):
        if content:
            logging.info(f"Generated content for prompt '{prompt}': {content}")
        else:
            logging.error(f"Failed to generate content for prompt '{prompt}'.")

if __name__ == "__main__":
    asyncio.run(main())
