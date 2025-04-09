from google import genai
import os

class GPTIntegration:
    def __init__(self, api_key=None):
        # Use the provided API key or fetch it from environment variables
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key for GPT model is not provided.")

        self.client = genai.Client(api_key=self.api_key)

    def send_message(self, message, mode="normal"):
        """
        Sends a message to the GPT model and returns the response.
        :param message: The input message to send to the GPT model.
        :param mode: The mode to use as a prompt (e.g., normal, angry, funny).
        :return: The GPT model's response.
        """
        try:
            response = self.client.models.generate_content(
                model=os.getenv("GEMINI_MODEL"), contents=os.getenv("GPT_PROMPT") + message)
            return response.text.strip()
        except Exception as e:
            return f"Error communicating with GPT model: {str(e)}"

    def distill_discussion(self, messages):
        """
        Summarizes a discussion based on a list of messages.
        :param messages: A list of messages from the discussion.
        :return: A summary of the discussion.
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents="Сделай краткую выжимку, оставив только самое важное. " + os.getenv("GPT_PROMPT") + " ".join(messages))
            return response.text.strip()
        except Exception as e:
            return f"Error summarizing discussion: {str(e)}"