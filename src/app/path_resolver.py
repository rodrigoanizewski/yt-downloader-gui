"""
Path resolution utility for PyInstaller compatibility.

This module provides utilities for resolving application paths correctly
in both development (Python script) and production (PyInstaller executable)
environments.
"""

import os
import sys


def get_base_path() -> str:
    """
    Get the base directory of the application.
    
    Handles both development and PyInstaller environments:
    - PyInstaller executable: Returns the directory containing the .exe file
    - Python script: Returns the directory containing the main.py script
    
    Returns:
        str: The absolute path to the application base directory
        
    Example:
        >>> base_path = get_base_path()
        >>> yt_dlp_path = os.path.join(base_path, "bin", "yt-dlp.exe")
    """
    if getattr(sys, "frozen", False):
        # Running as PyInstaller compiled executable
        # sys.executable points to the .exe file
        return os.path.dirname(sys.executable)
    else:
        # Running as Python script
        # __file__ points to this module, need to go up to src/
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_bin_path(executable_name: str) -> str:
    """
    Get the full path to an executable in the bin directory.
    
    Args:
        executable_name: Name of the executable (e.g., "yt-dlp.exe", "ffmpeg.exe")
        
    Returns:
        str: The absolute path to the executable
        
    Example:
        >>> yt_dlp_path = get_bin_path("yt-dlp.exe")
        >>> ffmpeg_path = get_bin_path("ffmpeg.exe")
    """
    base_path = get_base_path()
    return os.path.join(base_path, "bin", executable_name)


def get_assets_path(asset_name: str) -> str:
    """
    Get the full path to an asset in the assets directory.
    
    Args:
        asset_name: Name of the asset file or relative path (e.g., "style.qss", "icons/download.png")
        
    Returns:
        str: The absolute path to the asset
        
    Example:
        >>> style_path = get_assets_path("style.qss")
        >>> icon_path = get_assets_path("icons/download.png")
    """
    base_path = get_base_path()
    return os.path.join(base_path, "assets", asset_name)
