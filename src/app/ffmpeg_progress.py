"""
FFmpeg progress tracking utilities.

This module provides utilities for parsing FFmpeg progress output and 
calculating encoding progress percentage based on video duration.
"""

import re
from typing import Optional, Tuple


def parse_ffmpeg_time(time_str: str) -> Optional[int]:
    """
    Parse FFmpeg time format (HH:MM:SS.ms or frames) to seconds.
    
    FFmpeg progress output includes "out_time=HH:MM:SS.ms" entries that show
    the current position in the output file being encoded.
    
    Args:
        time_str: Time string in format "HH:MM:SS.ms" (e.g., "00:01:23.45")
        
    Returns:
        Total seconds as integer, or None if parsing fails
        
    Example:
        >>> parse_ffmpeg_time("00:01:23.45")
        83
        >>> parse_ffmpeg_time("00:00:05.99")
        5
    """
    try:
        # Match HH:MM:SS.ms format
        match = re.match(r"(\d+):(\d+):(\d+(?:\.\d+)?)", time_str)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = float(match.group(3))
            total_seconds = int(hours * 3600 + minutes * 60 + seconds)
            return total_seconds
    except (ValueError, AttributeError):
        pass
    
    return None


def extract_ffmpeg_progress_time(line: str) -> Optional[str]:
    """
    Extract the time value from FFmpeg progress output line.
    
    FFmpeg writes progress information in this format:
    out_time=HH:MM:SS.ms
    
    Args:
        line: A single line of FFmpeg output
        
    Returns:
        Time string (e.g., "00:01:23.45"), or None if not found
        
    Example:
        >>> extract_ffmpeg_progress_time("out_time=00:01:23.45")
        "00:01:23.45"
        >>> extract_ffmpeg_progress_time("frame=150")
        None
    """
    match = re.search(r"out_time=(\d+:\d+:\d+(?:\.\d+)?)", line)
    if match:
        return match.group(1)
    return None


def calculate_ffmpeg_progress(
    current_time_seconds: int, total_duration_seconds: int
) -> Optional[int]:
    """
    Calculate FFmpeg encoding progress as a percentage.
    
    Args:
        current_time_seconds: Current encoding position in seconds
        total_duration_seconds: Total video duration in seconds
        
    Returns:
        Progress percentage (0-100), or None if duration is invalid
        
    Example:
        >>> calculate_ffmpeg_progress(30, 120)
        25
        >>> calculate_ffmpeg_progress(60, 120)
        50
        >>> calculate_ffmpeg_progress(120, 120)
        100
    """
    if total_duration_seconds <= 0:
        return None
    
    progress = (current_time_seconds / total_duration_seconds) * 100
    # Clamp to 100 in case of rounding
    return min(int(progress), 100)


def is_ffmpeg_progress_line(line: str) -> bool:
    """
    Check if a line is an FFmpeg progress output line.
    
    Args:
        line: A single line of output
        
    Returns:
        True if the line contains FFmpeg progress information
        
    Example:
        >>> is_ffmpeg_progress_line("out_time=00:01:23.45")
        True
        >>> is_ffmpeg_progress_line("[Merger] Merging formats")
        False
    """
    return "out_time=" in line and "=" in line
