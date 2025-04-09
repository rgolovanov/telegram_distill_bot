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
        with open(chat_file, "r") as file:
            logger.info(f"Loading message history for chat {chat_id} from {chat_file}.")
            return json.load(file)
    return []

def save_message_history(chat_id, messages):
    """Save message history for a specific chat to a file."""
    try:
        os.makedirs(MESSAGE_HISTORY_DIR, exist_ok=True)  # Ensure the directory exists
        chat_file = os.path.join(MESSAGE_HISTORY_DIR, f"{chat_id}.json")
        with open(chat_file, "w") as file:
            json.dump(messages, file, indent=4)
        logger.info(f"Message history for chat {chat_id} saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save message history for chat {chat_id}: {e}")
