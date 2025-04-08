import gpt_integration

def handle_chat(update, context):
    # Extract the text following the /chat command
    user_message = ' '.join(context.args)
    if not user_message:
        update.message.reply_text("Please provide a message after the /chat command.")
        return

    # Send the extracted message to the GPT model
    gpt_response = gpt_integration.GPTIntegration().send_message(user_message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=gpt_response)