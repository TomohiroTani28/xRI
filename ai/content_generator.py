from transformers import pipeline, set_seed
import logging
import os

# Adjust the model based on your specific needs and access.
model_name = "rinna/japanese-gpt2-medium"  # This model is specifically trained on Japanese text.

# Load the Hugging Face token from an environment variable.
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        set_seed(42)  # Ensure reproducibility

        # Initialize the generation pipeline with the specified model.
        generation_pipeline = pipeline(
            "text-generation",
            model=model_name,
            token=hf_token,
            device=-1  # Use CPU; adjust if GPU is available.
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
            generated_output = generation_pipeline(prompt, max_length=280, num_return_sequences=1, truncation=True)
            content = refine_content(generated_output[0]['generated_text'])

            if content:  # Ensure content is non-empty and refined
                contents.append(content)
                if len(contents) == len(prompts):  # Check if content for all prompts is generated
                    break

        return contents if contents else ["Unable to generate content."]
    except Exception as e:
        logging.error(f"Content generation failed: {e}")
        return ["Content generation encountered an error."]

def refine_content(content):
    """
    Refines the generated content to ensure it fits Twitter's character limit
    and ends in a complete sentence for coherency.
    """
    # Japanese punctuation marks for sentence ending
    punctuation = "。！？"
    
    # Trim content to the last complete sentence within the character limit
    if len(content) > 280:
        for i in range(280, 0, -1):
            if content[i] in punctuation:
                return content[:i+1]
        return content[:280]  # Fallback to simple truncation if no punctuation found
    return content

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    contents = generate_content()
    for content in contents:
        print(f"Generated content: {content} (Length: {len(content)})")
