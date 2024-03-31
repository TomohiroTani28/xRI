from transformers import pipeline, set_seed
import logging
import os

# It's important to replace 'EleutherAI/gpt-neo-2.7B' with a model better suited for your needs,
# such as 'gpt2-medium', 'EleutherAI/gpt-j-6B', or even 'gpt3' if you have access through OpenAI's API.
model_name = "EleutherAI/gpt-j-6B"

# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        # Setting the seed for reproducibility
        set_seed(42)
        
        generation_pipeline = pipeline("text-generation", model=model_name, token=hf_token, device=0)
        
        prompts = [
            "インドネシアの不動産市場に関する最新情報",
            "インドネシアでの不動産投資のメリット",
            "インドネシアの不動産投資成功事例",
            "インドネシアでの不動産投資機会",
            "インドネシアの不動産市場の未来"
        ]

        contents = []
        for prompt in prompts:
            generated_outputs = generation_pipeline(prompt, max_length=280, num_return_sequences=1, stop_token=".")
            for output in generated_outputs:
                content = output['generated_text'].strip()
                if len(content) > 0 and len(content) <= 280:
                    contents.append(content)
                    break  # Move to the next prompt after successful generation

            if len(contents) >= 5:  # Stop if we've generated enough content
                break

        return contents if contents else ["Content generation failed."]
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return ["Content generation encountered an error."]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    contents = generate_content()
    for content in contents:
        print(f"Generated content: {content} (Length: {len(content)})")