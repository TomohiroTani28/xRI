from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import logging
import os

# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")

def generate_content():
    try:
        model_name = "EleutherAI/gpt-neo-2.7B"
        model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_token)
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
        
        generation_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1,  # Use CPU
        )

        # Refine prompts to encourage concise output
        prompts = [
            "Briefly describe the current state of Indonesia's real estate market.",
            "What's a major benefit of investing in Indonesian real estate?",
            "Share a short success story in Indonesian real estate investment.",
            "Highlight an opportunity in Indonesian real estate right now.",
            "Predict the future of Indonesia's real estate market in a few sentences."
        ]

        contents = []
        for prompt in prompts:
            generated_output = generation_pipeline(prompt, max_length=60, num_return_sequences=1, truncation=True)
            content = generated_output[0]['generated_text'].strip()
            # Further checks to ensure conciseness and relevance could be implemented here
            if len(content) <= 280:
                contents.append(content)
            if len(contents) >= 5:
                break

        return contents if contents else ["Content generation failed."]
    except Exception as e:
        logging.error(f"Failed to generate content: {e}")
        return ["Content generation encountered an error."]
