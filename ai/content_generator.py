from transformers import AutoTokenizer, pipeline
import logging
import random
import os

# 環境変数から Hugging Face トークンを取得
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        model = "meta-llama/Llama-2-7b-chat-hf"
        tokenizer = AutoTokenizer.from_pretrained(model, token=hf_token)  # use_auth_token を token に変更
        
        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.float16,
            device_map="auto",
            token=hf_token
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
