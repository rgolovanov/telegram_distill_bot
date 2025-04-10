from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
import gpt_integration
from telegram import ParseMode  # Import ParseMode for formatting
import os
import dotenv
import logging
import storage
import traceback
import random

logger = logging.getLogger(__name__)

def handle_error(update, context):
    """Log the error and notify the user."""
    logger.error(f'Update {update} caused error {context.error}')
    context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred. Please try again later.")

def error_handling_decorator(func):
    """Decorator to handle errors in handler functions."""
    def wrapper(update, context):
        text = update.message.text
        user = update.message.from_user  # Get the user object
        user_name = user.full_name if user.full_name else user.username  # Use full name or username
        chat_id = update.effective_chat.id
        logging.info(f"{chat_id} | Received message from {user_name}: {text}")

        try:
            return func(update, context)
        except Exception as e:
            msg = f"Error in {func.__name__}: {e}\n{traceback.format_exc()}"
            logging.error(msg)
            if update and update.effective_chat:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"An unexpected error occurred. Please try again later."
                )
    return wrapper

@error_handling_decorator
def handle_prompt(update, context):
    chat_id = update.effective_chat.id

    current_prompt = context.chat_data.get("prompt", storage.load_chat_prompt(chat_id))

    new_prompt = ' '.join(context.args)
    if not new_prompt:
        # If no new prompt is provided, show the current prompt
        update.message.reply_text(f"Current prompt: {current_prompt}")
        new_prompt = current_prompt
    else:
        storage.save_chat_prompt(chat_id, new_prompt)

    context.chat_data["prompt"] = new_prompt
    update.message.reply_text(f"New prompt set: {new_prompt}")

@error_handling_decorator
def handle_distill(update, context):
    chat_id = update.effective_chat.id

    messages = context.chat_data.get("messages", [])[-30:]  # Get the last 30 messages
    if not messages:
        update.message.reply_text("No messages available to distill.")
        return

    logging.info(f"Distilling discussion for chat {chat_id} with messages: {messages}")
    gpt = gpt_integration.GPTIntegration()
    prompt = context.chat_data.get("prompt", storage.load_chat_prompt(chat_id))
    distilled_summary = gpt.distill_discussion(prompt=prompt, messages=messages)
    context.bot.send_message(
        chat_id=chat_id,
        text=distilled_summary,
        parse_mode=ParseMode.HTML,
        )

@error_handling_decorator
def handle_chat(update, context):
    # Extract the text following the /chat command
    chat_id = update.effective_chat.id
    user_message = ' '.join(context.args)
    if not user_message:
        update.message.reply_text("Please provide a message after the /chat command.")
        return

    # Send the extracted message to the GPT model
    prompt = context.chat_data.get("prompt", storage.load_chat_prompt(chat_id))
    gpt_response = gpt_integration.GPTIntegration().send_message(prompt=prompt, message=user_message)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=gpt_response,
        parse_mode=ParseMode.HTML
        )

@error_handling_decorator
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

@error_handling_decorator
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

@error_handling_decorator
def handle_message(update: Update, context: CallbackContext):
    logger.info(f"Received message in chat {update.effective_chat.id}: {update.message.text}")
    text = update.message.text
    user = update.message.from_user  # Get the user object
    user_name = user.full_name if user.full_name else user.username  # Use full name or username
    chat_id = update.effective_chat.id

    # Load message history if not already loaded
    if "messages" not in context.chat_data:
        context.chat_data["messages"] = storage.load_message_history(chat_id)

    # Check if the message is a reply to the bot's message
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        # Preserve the context by including the replied message
        replied_text = update.message.reply_to_message.text
        gpt_input = f"Context: {replied_text}\nUser: {text}"
        # Send the message to GPT
        prompt = context.chat_data.get("prompt", storage.load_chat_prompt(chat_id))
        gpt_response = gpt_integration.GPTIntegration().send_message(prompt=prompt, message=gpt_input)
        update.message.reply_text(gpt_response, parse_mode=ParseMode.HTML)

    # Check if the bot was mentioned by @username
    elif f"@{context.bot.username}" in text:
        prompt = context.chat_data.get("prompt", storage.load_chat_prompt(chat_id))
        gpt_response = gpt_integration.GPTIntegration().send_message(prompt=prompt, message=text)
        update.message.reply_text(gpt_response, parse_mode=ParseMode.HTML)

    # Check if the word "бот" is present in the message
    elif "бот" in text.lower():
        if random.random() < 0.9:  # 80% probability to reply
            prompt = context.chat_data.get("prompt", storage.load_chat_prompt(chat_id))
            gpt_response = gpt_integration.GPTIntegration().send_message(prompt=prompt, message=text)
            update.message.reply_text(gpt_response, parse_mode=ParseMode.HTML)
    # For plain messages, reply randomly with a lower probability
    elif random.random() < 0.3:
        prompt = context.chat_data.get("prompt", storage.load_chat_prompt(chat_id))
        gpt_response = gpt_integration.GPTIntegration().send_message(prompt=prompt, message=text)
        update.message.reply_text(gpt_response, parse_mode=ParseMode.HTML)

    # Store the message with the user's name in chat_data for distillation
    context.chat_data["messages"].append(f"{user_name}: {text}")
    # Limit stored messages to the last 30
    context.chat_data["messages"] = context.chat_data["messages"][-30:]
    # Save the updated message history to the file
    storage.save_message_history(chat_id, context.chat_data["messages"])
