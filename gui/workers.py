from PyQt6.QtCore import QThread, pyqtSignal
from transcriber import transcribe
from translator import GeminiTranslator, DeepTranslatorWrapper
from core.video_utils import extract_audio, cleanup_temp_audio

class TranscriptionWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, file_path, source_lang, device):
        super().__init__()
        self.file_path = file_path
        self.source_lang = source_lang
        self.device = device

    def run(self):
        audio_path = self.file_path
        is_video = self.file_path.endswith((".mp4", ".mkv"))
        temp_audio_path = None

        try:
            if is_video:
                temp_audio_path = extract_audio(self.file_path)
                if not temp_audio_path:
                    self.error.emit("Failed to extract audio from video.")
                    return
                audio_path = temp_audio_path
                audio_path = extract_audio(self.file_path)
                if not audio_path:
                    self.error.emit("Failed to extract audio from video.")
                    return

            result = transcribe(audio_path, self.source_lang, self.device)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            if temp_audio_path:
                cleanup_temp_audio(temp_audio_path)

class TranslationWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text, source_lang="auto", target_lang="en", translator="Gemini"):
        super().__init__()
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translator_name = translator

    def run(self):
        try:
            if self.translator_name.lower() == "gemini":
                translator = GeminiTranslator()
                result = translator.translate(self.text, target_lang=self.target_lang)
            else:
                translator = DeepTranslatorWrapper(
                    self.translator_name,
                    source=self.source_lang,
                    target=self.target_lang
                )
                result = translator.translate(self.text)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))