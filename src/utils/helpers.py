def format_message(message: str) -> str:
    """Format the message for better readability."""
    return message.strip().capitalize()

def validate_input(user_input: str) -> bool:
    """Validate user input to ensure it meets criteria."""
    return bool(user_input and len(user_input) > 1)

def extract_command(text: str) -> str:
    """Extract the command from the text."""
    return text.split()[0] if text else ''