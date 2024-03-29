from dotenv import load_dotenv
import os

load_dotenv()

# Removed AI_API_KEY
X_API_KEY = os.getenv("X_API_KEY")
DATABASE_PATH = os.getenv("DATABASE_PATH")
