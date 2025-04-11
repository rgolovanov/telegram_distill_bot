from google import genai
import os
from functools import cache
import logging

class GPTIntegration:

    @cache
    def get_cached_instance(chat_id):
        return GPTIntegration(chat_id)

    def __init__(self, chat_id):
        logging.warn(f"Initializing GPTIntegration for chat {chat_id}.")
        # Use the provided API key or fetch it from environment variables
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key for GPT model is not provided.")

        self.chat_id = chat_id
        self.client = genai.Client(api_key=self.api_key)
        self.chat = self.client.chats.create(model="gemini-2.0-flash")
        self.prompt = ""

    def send_message(self, prompt, message):
        """
        Sends a message to the GPT model and returns the response.
        :param message: The input message to send to the GPT model.
        :param mode: The mode to use as a prompt (e.g., normal, angry, funny).
        :return: The GPT model's response.
        """
        try:
            if self.prompt != prompt:
                logging.info(f"Updating prompt for chat {self.chat_id}.")
                self.prompt = prompt
                message = f"{prompt}.\n{message}"

            response = self.chat.send_message(message)
            return response.text.strip()
        except Exception as e:
            return f"Error communicating with GPT model: {str(e)}"

    def distill_discussion(self, prompt, messages):
        """
        Summarizes a discussion based on a list of messages.
        :param messages: A list of messages from the discussion.
        :return: A summary of the discussion.
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents="Сделай краткую выжимку, оставив только самое важное. " + prompt + " ".join(messages))
            return response.text.strip()
        except Exception as e:
            return f"Error summarizing discussion: {str(e)}"
