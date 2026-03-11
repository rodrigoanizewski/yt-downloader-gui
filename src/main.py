"""
Project: yt-downloader-gui
Author: ukr
Version: 1.0.0
License: MIT
Repository: https://github.com/uikraft-hub/yt-downloader-gui
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from app.main_window import YTDGUI
from app.path_resolver import get_base_path


def main():
    """
    Main application entry point.

    Initializes the Qt application and starts the main event loop.
    """
    # Create Qt application
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("yt-downloader-gui")
    app.setApplicationVersion("1.0.0")

    # Determine application base directory
    # Handles both PyInstaller executable and Python script environments
    base_dir = get_base_path()

    # Create and show main window
    window = YTDGUI(base_dir)
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
