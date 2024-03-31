from transformers import pipeline, set_seed
import logging
import os
import re

model_name = "rinna/japanese-gpt2-medium"
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        set_seed(42)
        generation_pipeline = pipeline(
            "text-generation",
            model=model_name,
            token=hf_token,
            device=-1,  # Use CPU
            truncation=True
        )

        prompts = [
            "インドネシアの不動産市場に関する最新情報",
            "インドネシアでの不動産投資のメリット",
            "インドネシアの不動産投資成功事例",
            "インドネシアでの不動産投資機会",
            "インドネシアの不動産市場の未来"
        ]

        contents = []
        for prompt in prompts:
            generated_output = generation_pipeline(prompt, max_length=280, num_return_sequences=1)
            content = refine_generated_text(generated_output[0]['generated_text'])
            if content:
                contents.append(content)
                if len(contents) >= 5:
                    break

        return contents if contents else ["Unable to generate content."]
    except Exception as e:
        logging.error(f"Content generation failed: {e}")
        return ["Content generation encountered an error."]

def refine_generated_text(text):
    # Split the text by Japanese full stops and keep up to the last full stop within character limit
    sentences = re.split(r'(。)', text)
    refined_text, current_length = "", 0
    for i in range(0, len(sentences)-1, 2):  # Process sentence and its delimiter as one unit
        if current_length + len(sentences[i] + sentences[i+1]) <= 280:
            refined_text += sentences[i] + sentences[i+1]
            current_length += len(sentences[i] + sentences[i+1])
        else:
            break
    return refined_text

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    contents = generate_content()
    for content in contents:
        print(f"Generated content: {content} (Length: {len(content)})")
