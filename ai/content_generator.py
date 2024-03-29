from llama import Llama
import logging

def generate_content():
    try:
        llama = Llama()
        content = llama.generate(prompt="インドネシアの不動産投資についての情報", length=250)
        return content
    except Exception as e:
        logging.error(f"Failed to generate content with Llama2: {e}")
        return None
