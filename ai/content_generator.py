from transformers import pipeline, set_seed
import logging
import os

# This script has been updated to remove the use of `stop_token`,
# as it's not universally supported across models in the generation pipeline.
# Instead, we post-process the generated text to ensure it meets our requirements.

model_name = "rinna/japanese-gpt2-medium"  # A model optimized for Japanese text generation.

# Load the Hugging Face token from an environment variable.
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        set_seed(42)  # For reproducibility.

        # Initialize the generation pipeline with the specified model.
        generation_pipeline = pipeline(
            "text-generation",
            model=model_name,
            token=hf_token,
            device=-1  # Use CPU. Change to a GPU index if available and desired.
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
            content = post_process_content(generated_output[0]['generated_text'])

            if content:  # Check if the post-process content is valid.
                contents.append(content)
                if len(contents) >= 5:  # Stop if sufficient content is generated.
                    break

        return contents if contents else ["Content generation failed."]
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return ["Content generation encountered an error."]

def post_process_content(content):
    """
    Post-processes generated content to fit within Twitter's character limit,
    ensuring it ends logically for readability.
    """
    # Truncate to the nearest sentence end within character limit.
    if len(content) > 280:
        content = content[:280].rsplit('。', 1)[0] + '。'
    return content

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    contents = generate_content()
    for content in contents:
        print(f"Generated content: {content} (Length: {len(content)})")
