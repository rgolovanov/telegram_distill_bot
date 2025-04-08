import openai
import os

class GPTIntegration:
    def __init__(self, api_key=None):
        # Use the provided API key or fetch it from environment variables
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key for GPT model is not provided.")

        self.client = openai.OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
            )

    def send_message(self, message, mode="normal"):
        """
        Sends a message to the GPT model and returns the response.
        :param message: The input message to send to the GPT model.
        :param mode: The mode to use as a prompt (e.g., normal, angry, funny).
        :return: The GPT model's response.
        """
        try:
            response = self.client.responses.create(
                model=os.getenv("GPT_MODEL"),  # Replace with the desired GPT engine
                instructions=os.getenv("OPENAI_PROMPT"),
                input=message
            )
            return response.output_text.strip()
        except Exception as e:
            return f"Error communicating with GPT model: {str(e)}"

    def distill_discussion(self, messages):
        """
        Summarizes a discussion based on a list of messages.
        :param messages: A list of messages from the discussion.
        :return: A summary of the discussion.
        """
        try:
            response = self.client.responses.create(
                model=os.getenv("GPT_MODEL"),  # Replace with the desired GPT engine
                instructions=os.getenv("OPENAI_PROMPT"),
                input=f"Summarize the following discussion and use emojies and simple formatted text using only these HTML tags: <b>, <i>, <s>, <u>. Split summary by logical sections. {messages}"
            )
            return response.output_text
        except Exception as e:
            return f"Error summarizing discussion: {str(e)}"