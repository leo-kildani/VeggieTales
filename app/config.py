# config.py file
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI')

    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')