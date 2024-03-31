import torch
from transformers import AutoTokenizer, pipeline
import logging
import random
import os

# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        # Specify the model to use (Assuming 'model' variable is already set to the desired model ID)
        model = "EleutherAI/gpt-neo-2.7B"  # 例としてGPT-Neoを使用; Llama2の適切な代替を選択してください
        # Load the tokenizer using the Hugging Face token for authentication
        tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=hf_token)
        
        # Initialize the pipeline for text generation with the model
        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1,  # Use CPU for execution, as M1 Macs do not support CUDA.
        )

        prompts = [
            "インドネシアの不動産市場に関する最新情報",
            "インドネシアでの不動産投資のメリット",
            "インドネシアの不動産投資成功事例",
            "インドネシアでの不動産投資機会",
            "インドネシアの不動産市場の未来"
        ]

        
        selected_prompt = random.choice(prompts)
        # Generate content with the selected prompt
        generated_outputs = generation_pipeline(selected_prompt, max_length=250, num_return_sequences=1, truncation=True)
        content = generated_outputs[0]['generated_text']
        return content
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return None