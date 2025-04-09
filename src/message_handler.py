from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
import gpt_integration
from telegram import ParseMode  # Import ParseMode for formatting
import os
import dotenv
import logging
import history

logger = logging.getLogger(__name__)

def handle_error(update, context):
    """Log the error and notify the user."""
    logger.error(f'Update {update} caused error {context.error}')
    context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred. Please try again later.")

def handle_prompt(update, context):
    new_prompt = ' '.join(context.args)
    dotenv.set_key(dotenv.find_dotenv(), "GPT_PROMPT", new_prompt)
    dotenv.load_dotenv()
    update.message.reply_text(f"New prompt set: {new_prompt}")


def handle_distill(update, context):
    chat_id = update.effective_chat.id
    messages = context.chat_data.get("messages", [])[-30:]  # Get the last 30 messages
    if not messages:
        update.message.reply_text("No messages available to distill.")
        return

    gpt = gpt_integration.GPTIntegration()
    distilled_summary = gpt.distill_discussion(messages)
    context.bot.send_message(
        chat_id=chat_id,
        text=distilled_summary,
        parse_mode=ParseMode.HTML,
        )

def handle_chat(update, context):
    # Extract the text following the /chat command
    user_message = ' '.join(context.args)
    if not user_message:
        update.message.reply_text("Please provide a message after the /chat command.")
        return

    # Send the extracted message to the GPT model
    gpt_response = gpt_integration.GPTIntegration().send_message(user_message)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=gpt_response,
        parse_mode=ParseMode.HTML
        )

def handle_help():
    commands_description = {
        "/start": "Initialize the bot interaction and receive a welcome message.",
        "/help": "Get a description of all available commands and their functionalities.",
        "/chat": "Send a message to the GPT model and receive a response.",
        "/mode": "Set the mode for responses from the bot.",
        "/prompt": "Set a custom prompt for the GPT model.",
        "/distill": "Summarize the last 30 messages in the chat.",
    }

    help_text = "Available Commands:\n"
    for command, description in commands_description.items():
        help_text += f"{command}: {description}\n"

    return help_text.strip()

def handle_start(update, context):
    welcome_message = "Welcome to the GPT Telegram Bot! Type /help to see the available commands."
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

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
    chat_id = update.effective_chat.id

    # Load message history if not already loaded
    if "messages" not in context.chat_data:
        context.chat_data["messages"] = history.load_message_history(chat_id)

    # Check if the message is a reply to the bot's message
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        # Preserve the context by including the replied message
        replied_text = update.message.reply_to_message.text
        gpt_input = f"Context: {replied_text}\nUser: {text}"

        # Send the message to GPT
        gpt_response = gpt_integration.GPTIntegration().send_message(gpt_input)
        context.bot.send_message(
            chat_id=chat_id,
            text=gpt_response,
            parse_mode=ParseMode.HTML
        )
        return

    # Store the message with the user's name in chat_data for distillation
    context.chat_data["messages"].append(f"{user_name}: {text}")
    # Limit stored messages to the last 30
    context.chat_data["messages"] = context.chat_data["messages"][-30:]
    # Save the updated message history to the file
    history.save_message_history(chat_id, context.chat_data["messages"])
