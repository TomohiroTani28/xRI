import logging
import os
import replicate
import asyncio

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Retrieve the Replicate API token from the environment variable
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    logging.error("REPLICATE_API_TOKEN not set. Please set the environment variable.")
    exit(1)

# Set the Replicate API token for authentication
replicate.api_token = REPLICATE_API_TOKEN

async def generate_content_with_llama2(prompt):
    """
    Generate content using the Llama 2 API via the replicate client.
    """
    try:
        # Perform the prediction using the Llama 2 model
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
        # Check for the presence of text in the response
        if 'text' in response:
            return response['text'].strip()
        else:
            return "Content generation successful, but no text was returned."
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return "Failed to generate content due to an exception."

async def main():
    # Define the prompts for content generation
    prompts = [
        "2024年のインドネシアの不動産市場のトレンドについて分析してください。",
        "現在、インドネシアの不動産セクターで最良の投資機会は何ですか？",
        "2024年にインドネシアで優勢になる不動産開発プロジェクトの予測を提供してください。",
        "インドネシアの経済成長とその不動産市場との関係について説明してください。",
    ]

    # Iterate through the prompts and generate content for each
    for prompt in prompts:
        content = await generate_content_with_llama2(prompt)
        if content:
            logging.info(f"Generated content for prompt '{prompt}': {content}")
        else:
            logging.error(f"Failed to generate content for prompt '{prompt}'.")

if __name__ == "__main__":
    asyncio.run(main())
