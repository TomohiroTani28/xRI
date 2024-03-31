from transformers import pipeline, set_seed
import logging
import os
import re
from datetime import datetime
import random

model_name = "rinna/japanese-gpt2-medium"
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    set_seed(42)
    generation_pipeline = pipeline(
        "text-generation",
        model=model_name,
        token=hf_token,
        device=-1,  # Use CPU
        truncation=True
    )

    date_str = datetime.now().strftime("%Y年%m月%d日")
    base_prompts = [
        "インドネシアの不動産市場に関する最新情報",
        "インドネシアでの不動産投資のメリット",
        "インドネシアの不動産投資成功事例",
        "インドネシアでの不動産投資機会",
        "インドネシアの不動産市場の未来"
    ]
    prompts = [f"{prompt} - {date_str}" for prompt in base_prompts]

    contents = []
    for prompt in prompts:
        max_length = random.randint(240, 280)
        generated_output = generation_pipeline(prompt, max_length=max_length, num_return_sequences=1)
        content = refine_generated_text(generated_output[0]['generated_text'])
        if content:
            contents.append(content)
            if len(contents) >= 5:
                break

    return contents if contents else ["Unable to generate content."]

def refine_generated_text(text):
    if len(text) > 280:
        sentences = re.split(r'([。！？])', text)
        refined_text, current_length = "", 0
        for i in range(0, len(sentences) - 1, 2):
            if current_length + len(sentences[i] + sentences[i + 1]) <= 280:
                refined_text += sentences[i] + sentences[i + 1]
                current_length += len(sentences[i] + sentences[i + 1])
            else:
                break
        text = refined_text
    return text

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    contents = generate_content()
    for content in contents:
        print(f"Generated content: {content} (Length: {len(content)})")
