import sys
from typing import Optional
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QComboBox,
    QFileDialog,
    QLabel,
    QStatusBar,
)
from transcriber import transcribe
from translator import GeminiTranslator
from .workers import TranscriptionWorker, TranslationWorker
from core.video_utils import extract_audio, cleanup_temp_audio
from core.subtitle_converter import srt_to_vtt, srt_to_ass, srt_to_txt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AniSubsAI")
        self.setGeometry(100, 100, 800, 600)
        self.setAcceptDrops(True)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.setup_ui()

    def setup_ui(self):
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        file_button = QPushButton("Select Media File")
        file_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(file_button)
        self.main_layout.addLayout(file_layout)

        # Language selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Source Language:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([
            "Auto", "en", "ja", "fr", "de", "es", "ru", "ko", "zh", "it", "pt"
        ])
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        self.main_layout.addLayout(lang_layout)

        # Device selection
        device_layout = QHBoxLayout()
        device_label = QLabel("Device:")
        self.device_combo = QComboBox()
        self.device_combo.addItems(["cpu", "cuda"])
        device_layout.addWidget(device_label)
        device_layout.addWidget(self.device_combo)
        self.main_layout.addLayout(device_layout)

        # Transcribe button
        transcribe_button = QPushButton("Transcribe")
        transcribe_button.clicked.connect(self.transcribe_audio)
        self.main_layout.addWidget(transcribe_button)

        # Transcription result
        self.transcription_text = QTextEdit()
        self.transcription_text.setReadOnly(True)
        self.main_layout.addWidget(self.transcription_text)

        # Save transcription button
        save_transcription_button = QPushButton("Save Transcription")
        save_transcription_button.clicked.connect(self.save_transcription)
        self.main_layout.addWidget(save_transcription_button)

        # Translate button
        translate_button = QPushButton("Translate")
        translate_button.clicked.connect(self.translate_text)
        self.main_layout.addWidget(translate_button)

        # Translator selection
        translator_layout = QHBoxLayout()
        translator_label = QLabel("Translator:")
        self.translator_combo = QComboBox()
        self.translator_combo.addItems([
            "Gemini", "Google", "DeepL", "Microsoft", "MyMemory"
        ])
        translator_layout.addWidget(translator_label)
        translator_layout.addWidget(self.translator_combo)
        self.main_layout.addLayout(translator_layout)

        # Target language selection
        target_lang_layout = QHBoxLayout()
        target_lang_label = QLabel("Target Language:")
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems([
            "en", "ja", "fr", "de", "es", "ru", "ko", "zh", "it", "pt"
        ])
        target_lang_layout.addWidget(target_lang_label)
        target_lang_layout.addWidget(self.target_lang_combo)
        self.main_layout.addLayout(target_lang_layout)

        # Translation result
        self.translation_text = QTextEdit()
        self.translation_text.setReadOnly(True)
        self.main_layout.addWidget(self.translation_text)

        # Save translation button
        save_translation_button = QPushButton("Save Translation")
        save_translation_button.clicked.connect(self.save_translation)
        self.main_layout.addWidget(save_translation_button)
    def select_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Media File",
            "",
            "All Media Files (*.mp3 *.wav *.mp4 *.mkv);;Audio Files (*.mp3 *.wav);;Video Files (*.mp4 *.mkv)",
        )
        if self.file_path:
            self.file_label.setText(self.file_path)

    def transcribe_audio(self):
        if hasattr(self, "file_path"):
            source_lang = self.lang_combo.currentText()
            device = self.device_combo.currentText()
            self.status_bar.showMessage("Transcribing...")
            self.worker = TranscriptionWorker(self.file_path, source_lang, device)
            self.worker.finished.connect(self.on_transcription_finished)
            self.worker.error.connect(self.on_worker_error)
            self.worker.start()

    def on_transcription_finished(self, transcription):
        self.transcription_text.setText(transcription)
        self.status_bar.showMessage("Transcription complete.", 5000)

    def translate_text(self):
        transcribed_text = self.transcription_text.toPlainText()
        if transcribed_text:
            translator = self.translator_combo.currentText()
            source_lang = self.lang_combo.currentText()
            target_lang = self.target_lang_combo.currentText()
            self.status_bar.showMessage("Translating...")
            self.worker = TranslationWorker(
                transcribed_text,
                source_lang=source_lang,
                target_lang=target_lang,
                translator=translator
            )
            self.worker.finished.connect(self.on_translation_finished)
            self.worker.error.connect(self.on_worker_error)
            self.worker.start()

    def on_translation_finished(self, translation):
        self.translation_text.setText(translation)
        self.status_bar.showMessage("Translation complete.", 5000)

    def on_worker_error(self, error_message):
        self.status_bar.showMessage(f"Error: {error_message}", 5000)

    def save_transcription(self):
        self.save_file(self.transcription_text.toPlainText())

    def save_translation(self):
        self.save_file(self.translation_text.toPlainText())

    def save_file(self, content):
        if not content:
            self.status_bar.showMessage("Nothing to save.", 5000)
            return

        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "SRT Files (*.srt);;VTT Files (*.vtt);;ASS Files (*.ass);;Text Files (*.txt)",
        )

        if file_path:
            try:
                if "vtt" in selected_filter:
                    content = srt_to_vtt(content)
                elif "ass" in selected_filter:
                    content = srt_to_ass(content)
                elif "txt" in selected_filter:
                    content = srt_to_txt(content)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status_bar.showMessage(f"File saved to {file_path}", 5000)
            except Exception as e:
                self.status_bar.showMessage(f"Error saving file: {e}", 5000)

    def dragEnterEvent(self, a0: Optional[QDragEnterEvent]) -> None:
        if a0 and a0.mimeData() and a0.mimeData().hasUrls():
            self.central_widget.setStyleSheet("background-color: #2a2a2a; border: 2px dashed #4a00e0;")
            a0.accept()
        elif a0:
            a0.ignore()

    def dragLeaveEvent(self, a0: Optional[QDragLeaveEvent]) -> None:
        self.central_widget.setStyleSheet("")

    def dropEvent(self, a0: Optional[QDropEvent]) -> None:
        self.central_widget.setStyleSheet("")
        if a0 and a0.mimeData() and a0.mimeData().urls():
            files = [u.toLocalFile() for u in a0.mimeData().urls()]
            if files:
                self.file_path = files[0]
                self.file_label.setText(self.file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())