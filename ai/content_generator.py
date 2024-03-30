import torch
from transformers import AutoTokenizer, pipeline
import logging
import random
import os

# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        # Specify the model to use
        model = "meta-llama/Llama-2-7b-chat-hf"
        # Load the tokenizer using the Hugging Face token for authentication
        tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=hf_token)
        
        # Initialize the pipeline for text generation with optimized settings
        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.float16,  # Use float16 for faster computation
            # Optimize model loading based on the available device (GPU/CPU)
            device=0 if torch.cuda.is_available() else -1,
        )

        prompts = [
            "Latest information about the real estate market in Indonesia",
            "Benefits of investing in real estate in Indonesia",
            "Success stories of real estate investment in Indonesia",
            "Opportunities for real estate investment in Indonesia",
            "Future of the real estate market in Indonesia"
        ]
        
        selected_prompt = random.choice(prompts)
        # Generate content with the selected prompt, ensuring efficient memory use
        generated_outputs = generation_pipeline(selected_prompt, max_length=250, num_return_sequences=1, truncation=True)
        content = generated_outputs[0]['generated_text']
        return content
    except Exception as e:
        logging.error(f"Failed to generate content with Llama2: {e}")
        return None
