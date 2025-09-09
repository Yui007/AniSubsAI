from deep_translator import (
    GoogleTranslator,
    DeeplTranslator,
    MicrosoftTranslator,
    MyMemoryTranslator,
)

class DeepTranslatorWrapper:
    def __init__(self, translator_name="Google", source="auto", target="en"):
        self.translator_name = translator_name.lower()
        self.source = self._map_language(source)
        self.target = self._map_language(target)
        self.translator = self._get_translator()

    def _map_language(self, lang_code):
        if lang_code == "Auto":
            return "auto"
        # Add other mappings here if needed, e.g., for specific dialects
        # For now, we'll assume the codes are mostly compatible.
        # The main issue is often with 'auto' and specific language names.
        if lang_code == "ja":
            return "japanese"
        if lang_code == "en":
            return "english"
        if lang_code == "ko":
            return "korean"
        if lang_code == "zh":
            return "chinese (simplified)"
        return lang_code

    def _get_translator(self):
        if self.translator_name == "google":
            return GoogleTranslator(source=self.source, target=self.target)
        elif self.translator_name == "deepl":
            # Note: DeepL requires an API key for the formal/informal split feature.
            # This basic implementation does not use an API key.
            return DeeplTranslator(source=self.source, target=self.target)
        elif self.translator_name == "microsoft":
            # Note: Microsoft Translator may require an API key for high volume usage.
            return MicrosoftTranslator(source=self.source, target=self.target)
        elif self.translator_name == "mymemory":
            return MyMemoryTranslator(source=self.source, target=self.target)
        else:
            # Default to Google Translate if the name is unrecognized
            return GoogleTranslator(source=self.source, target=self.target)

    def translate(self, text: str) -> str:
        translation = self.translator.translate(text)
        if isinstance(translation, list):
            return " ".join(translation)
        return translation or ""