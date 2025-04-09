from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from message_handler import add_command_handlers

import dotenv
import os

dotenv.load_dotenv()

print(dotenv.dotenv_values())

def main():
    updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)

    dispatcher = updater.dispatcher

    # Command handlers
    add_command_handlers(dispatcher)

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()