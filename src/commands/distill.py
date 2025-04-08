from gpt_integration import GPTIntegration
from telegram import ParseMode  # Import ParseMode for formatting


def handle_distill(update, context):
    chat_id = update.effective_chat.id
    messages = context.chat_data.get("messages", [])[-30:]  # Get the last 30 messages
    if not messages:
        update.message.reply_text("No messages available to distill.")
        return

    gpt = GPTIntegration()
    distilled_summary = gpt.distill_discussion(messages)
    context.bot.send_message(
        chat_id=chat_id,
        text=distilled_summary,
        parse_mode=ParseMode.MARKDOWN,  # Use Markdown formatting
        )