import ffmpeg
import os

def extract_audio(video_path):
    """
    Extracts audio from a video file and saves it as a temporary .wav file.

    Args:
        video_path: The path to the video file.

    Returns:
        The path to the extracted audio file.
    """
    audio_path = "temp_audio.wav"
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True)
        )
        return audio_path
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e.stderr.decode()}")
        return None

def cleanup_temp_audio(audio_path):
    """
    Deletes the temporary audio file.
    """
    if os.path.exists(audio_path):
        os.remove(audio_path)