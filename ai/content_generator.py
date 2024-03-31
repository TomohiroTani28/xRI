from transformers import pipeline, set_seed
import logging
import os
import re

# Choose a model that's optimized for the language and type of content you're generating.
# For Japanese text, consider models specifically trained on Japanese language datasets.
model_name = "rinna/japanese-gpt2-medium"  # A model trained on Japanese text

# Load the Hugging Face token from the environment variable
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        set_seed(42)  # For reproducibility

        # Initialize the text generation pipeline with the specified model
        generation_pipeline = pipeline(
            "text-generation",
            model=model_name,
            token=hf_token,
            device=-1  # Use -1 for CPU, or specify GPU index
        )

        # Define prompts in Japanese to guide the content generation
        prompts = [
            "インドネシアの不動産市場に関する最新情報",
            "インドネシアでの不動産投資のメリット",
            "インドネシアの不動産投資成功事例",
            "インドネシアでの不動産投資機会",
            "インドネシアの不動産市場の未来"
        ]

        contents = []
        for prompt in prompts:
            # Generate content based on each prompt
            generated_output = generation_pipeline(
                prompt,
                max_length=280,  # Aim for Twitter's character limit
                num_return_sequences=1,
                stop_token="。"  # Stop at the end of a sentence (using Japanese period)
            )
            content = refine_generated_text(generated_output[0]['generated_text'])

            if content:
                contents.append(content)

            if len(contents) >= 5:  # Exit loop once sufficient content is generated
                break

        return contents if contents else ["Content generation failed."]
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return ["Content generation encountered an error."]

def refine_generated_text(text):
    """
    Refines generated text to ensure it is suitable for Twitter, focusing on the Japanese context.
    """
    # Truncate to the last complete sentence if over the limit
    if len(text) > 280:
        sentences = re.split(r'(。|\？|\！)\s', text)  # Split by Japanese sentence-ending punctuation
        text = ''.join(sentences[:2]) + sentences[2] if len(sentences) > 2 else text
    return text[:280]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    contents = generate_content()
    for content in contents:
        print(f"Generated content: {content} (Length: {len(content)})")
