import logging
from transformers import AutoTokenizer, pipeline
import torch
import os
import traceback

logging.basicConfig(level=logging.INFO)

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    logging.error("HF_TOKEN not set. Please set the environment variable.")
    exit(1)

os.environ["TRANSFORMERS_CACHE"] = "./transformers_cache_dir"

def setup_llama2_pipeline():
    model_name = "elyza/ELYZA-japanese-Llama-2-13b"  # 正しいモデル名に更新
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model_pipeline = pipeline(
        "text-generation",
        model=model_name,
        tokenizer=tokenizer,
        torch_dtype=torch.float16,
        device=-1
    )
    return model_pipeline

def generate_text_with_llama2(prompt, generation_pipeline):
    try:
        sequences = generation_pipeline(
            prompt,
            do_sample=True,
            max_length=200,
            top_k=50,
            temperature=0.7,
            num_return_sequences=1,
            truncation=True
        )
        return sequences[0]["generated_text"]
    except Exception as e:
        logging.error(f"Error in text generation: {traceback.format_exc()}")
        return "Error in generation."

async def main():
    prompts = ["2024年のインドネシアの不動産市場のトレンドについて分析してください。"]
    generation_pipeline = setup_llama2_pipeline()
    for prompt in prompts:
        result = generate_text_with_llama2(prompt, generation_pipeline)
        logging.info(f"Generated text: {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
