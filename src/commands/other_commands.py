import os

def handle_prompt(update, context):
    new_prompt = ' '.join(context.args)

    os.environ["GPT_PROMPT"] = new_prompt

    update.message.reply_text(f"New prompt set: {new_prompt}")