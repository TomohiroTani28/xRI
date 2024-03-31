from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import logging
import random
import os

# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        model_name = "EleutherAI/gpt-neo-2.7B"
        model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_token)
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
        
        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1,  # Use CPU
        )

        # Each prompt is designed to generate concise content likely to fit within a single Twitter post
        prompts = [
            "Brief update on Indonesia's real estate market",
            "Key benefit of real estate investment in Indonesia",
            "A success story in Indonesia's real estate investment",
            "Current opportunity in Indonesian real estate investment",
            "Forecast for Indonesia's real estate market"
        ]

        contents = []
        for prompt in prompts:
            generated_output = generation_pipeline(prompt, max_length=250, num_return_sequences=1, truncation=True)
            content = generated_output[0]['generated_text'].strip()
            if len(content) <= 280:  # Ensure content fits within Twitter's character limit
                contents.append(content)

        return contents
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return []
