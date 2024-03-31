import torch
from transformers import AutoTokenizer, pipeline
import logging
import random
import os

# Hugging Faceのトークンを環境変数から読み込む
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        # 使用するモデルを指定（'model'変数は既に希望のモデルIDに設定されていると想定）
        model = "EleutherAI/gpt-neo-2.7B"  # GPT-Neoを例に使用; Llama2の適切な代替を選択してください
        # 認証用のHugging Faceトークンを使用してトークナイザーを読み込む
        tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=hf_token)
        
        # モデルを使用してテキスト生成用のパイプラインを初期化
        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1,  # 実行にCPUを使用（M1 MacはCUDAをサポートしていません）
        )

        prompts = [
            "インドネシアの不動産市場についての最新情報",
            "インドネシアの不動産への投資の利点",
            "インドネシアの不動産投資の成功事例",
            "インドネシアでの不動産投資の機会",
            "インドネシアの不動産市場の将来"
        ]
        
        selected_prompt = random.choice(prompts)
        # 選択されたプロンプトでコンテンツを生成
        generated_outputs = generation_pipeline(selected_prompt, max_length=250, num_return_sequences=1, truncation=True)
        content = generated_outputs[0]['generated_text']
        return content
    except Exception as e:
        logging.error(f"コンテンツ生成に失敗しました: {e}")
        return None
