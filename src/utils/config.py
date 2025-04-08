from dotenv import load_dotenv
import os

load_dotenv()

def load_config():
    """
    Loads environment variables from a .env file and returns them as a dictionary.
    """
    load_dotenv()  # Load variables from .env file
    config = {key: value for key, value in os.environ.items() if key.isupper()}
    if not config.get("TELEGRAM_BOT_TOKEN"):
        raise ValueError("TELEGRAM_BOT_TOKEN is not set in the environment variables.")
    if not config.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    return config