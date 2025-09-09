from google import genai
from google.generativeai import types
from core.config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiTranslator:
    """
    A translator class that uses the Gemini API to translate text.
    """
    def __init__(self):
        """
        Initializes the GeminiTranslator.
        """
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL

    def translate(self, text: str, target_lang: str = "en") -> str:
        """
        Translates the given text to the target language.

        Args:
            text: The text to translate.
            target_lang: The target language.

        Returns:
            The translated text.
        """
        prompt = f"Translate the following text to {target_lang} and only return the translated text with timestamps, without any introductory text:\n\n{text}"
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text or ""