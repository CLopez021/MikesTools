"""
Utility functions for SRT file generation
"""

def format_timestamp(milliseconds):
    """Convert milliseconds to SRT timestamp format (HH:MM:SS,mmm)"""
    seconds = milliseconds / 1000
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(milliseconds % 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt(transcript):
    """
    Generate SRT file content from AssemblyAI transcript using word-level timing.
    Each word gets its own caption entry with precise timestamps.
    """
    srt_content = []
    
    if not hasattr(transcript, 'words') or not transcript.words:
        return ""
    
    # Create one SRT entry per word
    for i, word in enumerate(transcript.words, 1):
        start_time = format_timestamp(word.start)
        end_time = format_timestamp(word.end)
        
        srt_content.append(f"{i}")
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(word.text)
        srt_content.append("")  # Empty line between subtitles
    
    return '\n'.join(srt_content)

