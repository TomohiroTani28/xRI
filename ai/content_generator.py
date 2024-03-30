from transformers import AutoTokenizer, pipeline
import torch
import logging
import random

def generate_content():
    try:
        model = "meta-llama/Llama-2-7b-chat-hf"
        tokenizer = AutoTokenizer.from_pretrained(model)
        
        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        prompts = [
            "インドネシアの不動産市場についての最新情報",
            "インドネシアでの不動産投資のメリット",
            "インドネシア不動産投資の成功事例",
            "インドネシアの不動産投資のチャンス",
            "インドネシアの不動産市場の将来性"
        ]
        
        selected_prompt = random.choice(prompts)
        generated_outputs = generation_pipeline(selected_prompt, max_length=250, num_return_sequences=1)
        content = generated_outputs[0]['generated_text']
        return content
    except Exception as e:
        logging.error(f"Failed to generate content with Llama2: {e}")
        return None
