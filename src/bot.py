from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from message_handler import add_command_handlers

import dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

dotenv.load_dotenv()

print(dotenv.dotenv_values())

# Configure logging
log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# File handler
file_handler = RotatingFileHandler('bot.log', maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

def main():
    logging.info("Bot is starting...")
    updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)

    dispatcher = updater.dispatcher

    # Command handlers
    add_command_handlers(dispatcher)

    # Start polling for updates
    updater.start_polling()
    logging.info("Bot is polling for updates...")
    updater.idle()
    logging.info("Bot has stopped.")

if __name__ == '__main__':
    main()