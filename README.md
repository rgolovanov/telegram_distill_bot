# Telegram GPT Chatbot

This project is a Telegram chatbot that integrates with a GPT model to provide interactive conversations and various command functionalities.

## Features

- **Interactive Chat**: Users can chat with the bot, which utilizes a GPT model to generate responses.
- **Command Handlers**: The bot supports several commands:
  - `/start`: Initializes the bot interaction and provides a welcome message.
  - `/help`: Lists all available commands and their functionalities.
  - `/chat`: Sends user messages to the GPT model and returns the generated response.
  - Additional commands for setting modes and fact-checking messages.

## Project Structure

```
telegram-gpt-chatbot
├── src
│   ├── bot.py                # Main entry point for the Telegram bot
│   ├── gpt_integration.py    # Handles integration with the GPT model
│   ├── commands              # Contains command handlers
│   │   ├── start.py          # /start command handler
│   │   ├── help.py           # /help command handler
│   │   ├── chat.py           # /chat command handler
│   │   └── other_commands.py  # Additional command handlers
│   ├── utils                 # Utility functions and configurations
│   │   ├── config.py         # Loads environment variables and configurations
│   │   ├── logger.py         # Sets up logging for the application
│   │   └── helpers.py        # Contains utility functions
│   └── handlers              # Message and error handling
│       ├── message_handler.py # Logic for handling incoming messages
│       └── error_handler.py   # Error handling logic
├── requirements.txt          # Lists project dependencies
├── .env                      # Stores environment variables
├── .gitignore                # Specifies files to ignore in version control
└── README.md                 # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd telegram-gpt-chatbot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in the `.env` file. Make sure to include your API keys for the GPT model.

4. Run the bot:
   ```
   python src/bot.py
   ```

## Usage

- Start a conversation with the bot by sending the `/start` command.
- Use the `/help` command to see a list of available commands.
- Engage in a chat using the `/chat` command followed by your message.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.