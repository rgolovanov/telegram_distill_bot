def handle_help():
    commands_description = {
        "/start": "Initialize the bot interaction and receive a welcome message.",
        "/help": "Get a description of all available commands and their functionalities.",
        "/chat": "Send a message to the GPT model and receive a response.",
        "/mode": "Set the mode for responses from the bot.",
        "/check": "Fact-check a user message."
    }

    help_text = "Available Commands:\n"
    for command, description in commands_description.items():
        help_text += f"{command}: {description}\n"

    return help_text.strip()