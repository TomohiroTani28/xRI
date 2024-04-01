import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List
from config import Config
from ai.quality_checker import check_content_quality
from ai.data_enrichment import enrich_content_with_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def setup_llama2_pipeline():
    config = Config()
    model_name = config.model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto", offload_folder="offload")
    model = model.to(device)
    return model, tokenizer

def generate_text_with_llama2(prompt: str, model, tokenizer, max_length: int = 500, num_beams: int = 3, top_p: float = 0.9, temperature: float = 0.7) -> str:
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        output = model.generate(**inputs, max_new_tokens=max_length, num_beams=num_beams, early_stopping=True, top_p=top_p, temperature=temperature)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text
    except Exception as e:
        logging.error(f"Error in text generation: {e}")
        return "Error in generation."

async def generate_content(prompts: List[str]):
    model, tokenizer = setup_llama2_pipeline()
    generated_texts = []
    for prompt in prompts:
        result = generate_text_with_llama2(prompt, model, tokenizer)
        generated_texts.append(result)
        logging.info(f"Generated text: {result}")
    
    checked_texts = await check_content_quality(generated_texts)
    enriched_texts = await enrich_content_with_data(checked_texts)
    return enriched_texts