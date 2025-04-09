# Telegram Distill Bot

A Telegram chatbot that integrates with GPT models to provide interactive conversations, custom prompts, and message distillation.

## Features

- **Interactive Chat**: Chat with the bot using GPT-based responses.
- **Custom Prompts**: Set and save custom prompts for personalized interactions.
- **Message Distillation**: Summarize the last 30 messages in a chat.
- **Error Handling**: Graceful error handling with user notifications.
- **Logging**: Logs are saved to `bot.log` in UTF-8 encoding and printed to the console.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd telegram_distill_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with the following content:
   ```
   TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
   OPENAI_API_KEY=<your-openai-api-key>
   GEMINI_API_KEY=<your-gemini-api-key>
   GPT_PROMPT=<default-gpt-prompt>
   GEMINI_MODEL=gemini-2.0-flash
   ```

4. **Run the bot**:
   ```bash
   python src/bot.py
   ```

## Commands

- `/start`: Initialize the bot and receive a welcome message.
- `/help`: Get a list of available commands and their descriptions.
- `/chat <message>`: Send a message to the GPT model and receive a response.
- `/prompt <new_prompt>`: Set or view the custom prompt for the chat.
- `/distill`: Summarize the last 30 messages in the chat.

## Logging

- Logs are saved to `bot.log` with a maximum size of 5 MB and up to 3 backup files.
- Log format: `YYMMDD HHMMSS.ms [LEVEL] Message`.

## Project Structure

```
telekoteria_bot
├── src
│   ├── bot.py                # Main entry point for the bot
│   ├── storage.py            # Handles message and prompt storage
│   ├── message_handler.py    # Handles Telegram message and command processing
│   ├── gpt_integration.py    # Integrates with GPT models
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── .gitignore                # Ignored files and directories
├── README.md                 # Project documentation
└── message_histories/        # Stores chat message histories
    └── <chat_id>.json        # JSON files for each chat
└── prompt_histories/         # Stores chat-specific prompts
    └── <chat_id>.txt         # Text files for each chat
```

## Requirements

- Python 3.7+
- `python-telegram-bot`
- `google-genai`
- `python-dotenv`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.