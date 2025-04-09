import os
import json

import logging

logger = logging.getLogger(__name__)

MESSAGE_HISTORY_DIR = "message_histories"

def load_message_history(chat_id):
    """Load message history for a specific chat from a file."""
    os.makedirs(MESSAGE_HISTORY_DIR, exist_ok=True)  # Ensure the directory exists
    chat_file = os.path.join(MESSAGE_HISTORY_DIR, f"{chat_id}.json")
    if os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as file:
            logging.info(f"Loading message history for chat {chat_id} from {chat_file}.")
            return json.load(file)
    return []

def save_message_history(chat_id, messages):
    """Save message history for a specific chat to a file."""
    try:
        os.makedirs(MESSAGE_HISTORY_DIR, exist_ok=True)  # Ensure the directory exists
        chat_file = os.path.join(MESSAGE_HISTORY_DIR, f"{chat_id}.json")
        with open(chat_file, "w", encoding="utf-8") as file:
            json.dump(messages, file, indent=4)
        logging.info(f"Message history for chat {chat_id} saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save message history for chat {chat_id}: {e}")

PROMPT_HISTORY_DIR = "prompt_histories"
DEFAULT_GPT_PROMPT = os.getenv("GPT_PROMPT", "You are a helpful assistant.")

def load_chat_prompt(chat_id):
    """Load the prompt for a specific chat from a file."""
    os.makedirs(PROMPT_HISTORY_DIR, exist_ok=True)  # Ensure the directory exists
    prompt_file = os.path.join(PROMPT_HISTORY_DIR, f"{chat_id}.txt")
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as file:
            logging.info(f"Loading prompt for chat {chat_id} from {prompt_file}.")
            return file.read().strip()
    return DEFAULT_GPT_PROMPT

def save_chat_prompt(chat_id, prompt):
    """Save the prompt for a specific chat to a file."""
    try:
        os.makedirs(PROMPT_HISTORY_DIR, exist_ok=True)  # Ensure the directory exists
        prompt_file = os.path.join(PROMPT_HISTORY_DIR, f"{chat_id}.txt")
        with open(prompt_file, "w", encoding="utf-8") as file:
            logging.info(f"Saving prompt for chat {chat_id} to {prompt_file}.")
            file.write(prompt)
    except Exception as e:
        logger.error(f"Failed to save prompt for chat {chat_id}: {e}")
