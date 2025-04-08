def handle_start(update, context):
    welcome_message = "Welcome to the GPT Telegram Bot! Type /help to see the available commands."
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)