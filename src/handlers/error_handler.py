import logging

logger = logging.getLogger(__name__)

def handle_error(update, context):
    """Log the error and notify the user."""
    logger.error(f'Update {update} caused error {context.error}')
    context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred. Please try again later.")