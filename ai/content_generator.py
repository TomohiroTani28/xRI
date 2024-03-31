from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import logging
import random
import os

# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        model_name = "EleutherAI/gpt-neo-2.7B"
        # モデルとトークナイザーを個別に読み込む
        model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=hf_token)
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
        
        # 読み込んだモデルとトークナイザーを使用してpipelineを設定
        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1,  # CPUを使用
        )

        prompts = [
            "インドネシアの不動産市場に関する最新情報",
            "インドネシアでの不動産投資のメリット",
            "インドネシアの不動産投資成功事例",
            "インドネシアでの不動産投資機会",
            "インドネシアの不動産市場の未来"
        ]

        contents = []
        for _ in range(5):  # 5つの独立したポストを生成
            selected_prompt = random.choice(prompts)
            generated_output = generation_pipeline(selected_prompt, max_length=280, num_return_sequences=1, truncation=True)
            content = generated_output[0]['generated_text'].strip()
            if len(content) <= 280:
                contents.append(content)
            if len(contents) >= 5:  # 生成したポストが5つに達したら終了
                break

        return contents
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return []
