from telegram import Update
from telegram.ext import CallbackContext
from commands.start import handle_start
from commands.help import handle_help
from commands.chat import handle_chat
from commands.distill import handle_distill
from handlers.error_handler import handle_error
from commands.other_commands import handle_prompt

from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext

def add_command_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", handle_start))
    dispatcher.add_handler(CommandHandler("help", handle_help))
    dispatcher.add_handler(CommandHandler("chat", handle_chat))
    dispatcher.add_handler(CommandHandler("prompt", handle_prompt))
    dispatcher.add_handler(CommandHandler("distill", handle_distill))

    # Add the message handler to handle all non-command messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    dispatcher.add_error_handler(handle_error)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    user = update.message.from_user  # Get the user object
    user_name = user.full_name if user.full_name else user.username  # Use full name or username

    # Store the message with the user's name in chat_data for distillation
    if "messages" not in context.chat_data:
        context.chat_data["messages"] = []
    context.chat_data["messages"].append(f"{user_name}: {text}")

    # Limit stored messages to the last 30
    context.chat_data["messages"] = context.chat_data["messages"][-30:]
