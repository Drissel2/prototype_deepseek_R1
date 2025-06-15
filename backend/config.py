import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MODEL_PATH: str = os.getenv('MODEL_PATH', './model')
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 5000))
    MAX_LENGTH: int = int(os.getenv('MAX_LENGTH', 256))
    TEMPERATURE: float = float(os.getenv('TEMPERATURE', 0.7))

settings = Settings()
