import os
from faster_whisper import WhisperModel
from core.config import WHISPER_MODEL

def format_time(seconds):
    """Converts seconds to SRT time format (HH:MM:SS,ms)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def transcribe(audio_path: str, source_lang: str, device: str) -> str:
    """
    Transcribes the given audio file using faster-whisper.

    Args:
        audio_path: Path to the audio file.
        source_lang: Source language of the audio.
        device: The device to run the model on ("cpu" or "cuda").

    Returns:
        The transcribed text.
    """
    model = WhisperModel(
        WHISPER_MODEL,
        device=device,
        compute_type="int8",
        download_root="models/"
    )

    lang_code = source_lang if source_lang != "Auto" else None
    segments, info = model.transcribe(audio_path, beam_size=5, language=lang_code)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    srt_content = []
    for i, segment in enumerate(segments):
        start_time = format_time(segment.start)
        end_time = format_time(segment.end)
        srt_content.append(f"{i + 1}")
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(segment.text.strip())
        srt_content.append("")

    return "\n".join(srt_content)