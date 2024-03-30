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
        
        # Initialize the pipeline for text generation
        # As of now, we maintain synchronous execution here as the transformers pipeline
        # does not natively support asynchronous execution.
        # Adjust the device parameter according to your setup. For M1 Macs, CPU execution is more common.
        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1,  # Use CPU for execution, as M1 Macs do not support CUDA.
        )

        prompts = [
            "Latest information about the real estate market in Indonesia",
            "Benefits of investing in real estate in Indonesia",
            "Success stories of real estate investment in Indonesia",
            "Opportunities for real estate investment in Indonesia",
            "Future of the real estate market in Indonesia"
        ]
        
        selected_prompt = random.choice(prompts)
        # Generate content with the selected prompt
        generated_outputs = generation_pipeline(selected_prompt, max_length=250, num_return_sequences=1, truncation=True)
        content = generated_outputs[0]['generated_text']
        return content
    except Exception as e:
        logging.error(f"Failed to generate content with Llama2: {e}")
        return None
