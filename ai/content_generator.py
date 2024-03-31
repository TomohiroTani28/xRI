import logging
from transformers import AutoTokenizer, pipeline
import torch
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Set up Hugging Face authentication
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    logging.error("HF_TOKEN not set. Please set the environment variable.")
    exit(1)

os.environ["TRANSFORMERS_CACHE"] = "./transformers_cache_dir"  # Optional: Set a cache directory for transformers

def setup_llama2_pipeline():
    """
    Setup the Llama 2 pipeline for text generation.
    """
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    generation_pipeline = pipeline(
        "text-generation",
        model=model_name,
        tokenizer=tokenizer,
        torch_dtype=torch.float16,
        device=0 if torch.cuda.is_available() else -1  # Use GPU if available
    )
    return generation_pipeline

def generate_text_with_llama2(prompt, generation_pipeline):
    """
    Generate text using the Llama 2 model.
    """
    try:
        sequences = generation_pipeline(
            prompt,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=generation_pipeline.tokenizer.eos_token_id,
            max_length=200
        )
        return sequences[0]["generated_text"]
    except Exception as e:
        logging.error(f"Failed to generate text: {e}")
        return None

def main():
    """
    Main function to generate text based on given prompts.
    """
    prompts = [
        "2024年のインドネシアの不動産市場のトレンドについて分析してください。",
        # Add additional prompts as needed
    ]
    
    generation_pipeline = setup_llama2_pipeline()
    
    for prompt in prompts:
        generated_text = generate_text_with_llama2(prompt, generation_pipeline)
        if generated_text:
            logging.info(f"Generated content for prompt '{prompt}':\n{generated_text}\n")
        else:
            logging.error(f"Failed to generate content for prompt '{prompt}'.")

if __name__ == "__main__":
    main()
