import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

# Gemini model
GEMINI_MODEL = "gemini-3.1-flash-lite"

# Number of chunks retrieved for each question
TOP_K = 3