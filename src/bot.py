from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from utils.config import load_config
from handlers.message_handler import add_command_handlers
from handlers.error_handler import handle_error

def main():
    config = load_config()
    updater = Updater(token=config['TELEGRAM_BOT_TOKEN'], use_context=True)

    dispatcher = updater.dispatcher

    # Command handlers
    add_command_handlers(dispatcher)

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()