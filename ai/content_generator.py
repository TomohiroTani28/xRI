from llama import Llama
import logging
import random
import asyncio

async def generate_content():
    try:
        prompts = [
            "インドネシアの不動産市場についての最新情報",
            "インドネシアでの不動産投資のメリット",
            "インドネシア不動産投資の成功事例",
            "インドネシアの不動産投資のチャンス",
            "インドネシアの不動産市場の将来性"
        ]
        llama = Llama()
        # 非同期版のメソッドを仮定しています
        content = await llama.generate_async(prompt=random.choice(prompts), length=250)
        return content
    except Exception as e:
        logging.error(f"Failed to generate content with Llama2: {e}")
        return None
