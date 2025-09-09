import re

def srt_to_vtt(srt_content):
    """Converts SRT content to VTT format."""
    vtt_content = "WEBVTT\n\n"
    # Replace SRT's comma decimal separator with a period for VTT
    vtt_content += srt_content.replace(",", ".")
    return vtt_content

def srt_to_ass(srt_content):
    """Converts SRT content to ASS format."""
    ass_header = """[Script Info]
Title: AniSubsAI Generated Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_content = ass_header
    # Regex to capture SRT components
    srt_pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n", re.DOTALL)
    for match in srt_pattern.finditer(srt_content):
        start_time = match.group(2).replace(",", ".")[:-1]  # Convert to H:MM:SS.cs
        end_time = match.group(3).replace(",", ".")[:-1]
        text = match.group(4).replace("\n", "\\N")
        ass_content += f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    return ass_content

def srt_to_txt(srt_content):
    """Converts SRT content to a plain text format."""
    # Remove timestamps and sequence numbers, leaving only the dialogue
    return "\n".join(re.findall(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n(.*?)\n\n", srt_content, re.DOTALL))