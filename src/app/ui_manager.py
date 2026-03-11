"""
Handles creation and management of the UI.
"""

import os
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt

if TYPE_CHECKING:
    from .main_window import YTDGUI


class UIManager:
    """Handles creation and management of the UI."""

    def __init__(self, main_app: "YTDGUI"):
        self.main_app = main_app
        self.main_app.icons = {}
        self.main_app.video_favicon_pixmap = None

    def _load_stylesheet(self) -> None:
        """Load and apply the application stylesheet."""
        try:
            style_path = os.path.join(self.main_app.base_dir, "assets", "style.qss")
            if os.path.exists(style_path):
                with open(style_path, "r") as f:
                    self.main_app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    def _set_window_icon(self) -> None:
        """Set the application window icon if available."""
        try:
            icon_path = os.path.join(self.main_app.base_dir, "favicon.ico")
            if os.path.exists(icon_path):
                self.main_app.setWindowIcon(QIcon(icon_path))
        except Exception:
            # Silently continue if icon cannot be loaded
            pass

    def _load_icons(self) -> None:
        """Load application icons from assets directory."""
        self.main_app.icons = {
            "download": self.load_icon(
                os.path.join(self.main_app.base_dir, "assets", "download.png")
            ),
            "activity": self.load_icon(
                os.path.join(self.main_app.base_dir, "assets", "activity.png")
            ),
        }

        # Load video favicon for playlist/channel selection dialogs
        try:
            vf_path = os.path.join(
                self.main_app.base_dir, "assets", "video-favicon.png"
            )
            if os.path.exists(vf_path):
                self.main_app.video_favicon_pixmap = QPixmap(vf_path).scaled(
                    16,
                    16,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            else:
                self.main_app.video_favicon_pixmap = None
        except Exception:
            self.main_app.video_favicon_pixmap = None

    def load_icon(self, path: str) -> QIcon:
        """
        Load an icon from the specified path.

        Args:
            path: File path to the icon image

        Returns:
            QIcon object (empty if loading fails)
        """
        try:
            if os.path.exists(path):
                return QIcon(QPixmap(path))
        except Exception:
            pass
        return QIcon()

    def create_menubar(self) -> None:
        """Create the application menu bar with File and Help menus."""
        menubar = self.main_app.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # Login action for cookie-based authentication
        login_action = QAction("Login", self.main_app)
        login_action.triggered.connect(self.main_app.login_manager.open_login)
        file_menu.addAction(login_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("Exit", self.main_app)
        exit_action.triggered.connect(self.main_app.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        # About dialog
        about_action = QAction("About", self.main_app)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self) -> None:
        """Display application about dialog."""
        about_text = (
            "yt-downloader-gui\n"
            "Version 1.0.0\n\n"
            "Developed by ukr\n\n"
            "A professional YouTube video and audio downloader\n"
            "with support for playlists and channels.\n\n"
            "Report bugs via our support channel."
        )

        QMessageBox.information(self.main_app, "About yt-downloader-gui", about_text)

    def create_sidebar(self) -> QWidget:
        """
        Create navigation sidebar with application pages.

        Returns:
            Widget containing sidebar navigation buttons
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Application title header
        header = QLabel("yt-downloader-gui")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        layout.addSpacing(20)

        # Navigation buttons
        nav_buttons = [("Download", "download"), ("Activity", "activity")]

        for name, icon_key in nav_buttons:
            btn = QPushButton(name)

            # Set icon if available
            icon = self.main_app.icons.get(icon_key)
            if icon:
                btn.setIcon(icon)
                btn.setIconSize(QSize(32, 32))

            # Connect to page switching
            btn.clicked.connect(lambda checked, n=name: self.switch_page(n))
            layout.addWidget(btn)

        # Push buttons to top
        layout.addStretch()

        return widget

    def switch_page(self, name: str) -> None:
        """
        Switch to the specified page in the main content area.

        Args:
            name: Name of the page to switch to ("Download" or "Activity")
        """
        if name == "Download":
            self.main_app.stack.setCurrentWidget(self.main_app.download_page)
        elif name == "Activity":
            self.main_app.stack.setCurrentWidget(self.main_app.activity_page)

        self.main_app.update_status(f"{name} section active")

    def create_download_page(self) -> QWidget:
        """
        Create the main download configuration page.

        Returns:
            Widget containing download configuration controls
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # URL input section
        url_label = QLabel("Enter YouTube URL (or Playlist/Channel URL):")
        url_label.setObjectName("header_label")
        layout.addWidget(url_label)

        self.main_app.url_entry = QLineEdit()
        self.main_app.url_entry.setPlaceholderText(
            "https://www.youtube.com/watch?v=..."
        )
        layout.addWidget(self.main_app.url_entry)

        # Save location section
        save_path_label = QLabel("Save Location:")
        save_path_label.setObjectName("header_label")
        layout.addWidget(save_path_label)

        path_layout = QHBoxLayout()
        self.main_app.path_entry = QLineEdit(readOnly=True)
        self.main_app.path_entry.setPlaceholderText("Select folder to save downloads")
        path_layout.addWidget(self.main_app.path_entry)

        browse_btn = QPushButton("Browse Folder")
        browse_btn.clicked.connect(self.main_app.select_save_path)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # Download mode section
        mode_label = QLabel("Download Mode:")
        mode_label.setObjectName("header_label")
        layout.addWidget(mode_label)

        self.main_app.mode_combo = QComboBox()
        download_modes = [
            "Single Video",  # Download single video
            "MP3 Only",  # Extract audio only
            "Playlist Video",  # Download playlist videos
            "Playlist MP3",  # Extract audio from playlist
            "Channel Videos",  # Download channel videos
            "Channel Videos MP3",  # Extract audio from channel videos
            "Channel Shorts",  # Download channel shorts
            "Channel Shorts MP3",  # Extract audio from channel shorts
        ]
        self.main_app.mode_combo.addItems(download_modes)
        self.main_app.mode_combo.currentTextChanged.connect(self.mode_changed)
        layout.addWidget(self.main_app.mode_combo)

        # Video quality section (hidden for audio-only modes)
        self.main_app.video_quality_label = QLabel("Video Quality:")
        self.main_app.video_quality_label.setObjectName("header_label")
        self.main_app.video_quality_combo = QComboBox()
        quality_options = [
            "Best Available",  # Highest quality available
            "4320p 8K",  # 8K resolution
            "2160p 4K",  # 4K resolution
            "1440p 2K",  # 2K resolution
            "1080p Full HD",  # Full HD
            "720p HD",  # HD
            "480p Standard",  # Standard definition
            "360p Medium",  # Low quality
        ]
        self.main_app.video_quality_combo.addItems(quality_options)

        layout.addWidget(self.main_app.video_quality_label)
        layout.addWidget(self.main_app.video_quality_combo)

        # Initialize visibility based on default mode
        self.mode_changed(self.main_app.mode_combo.currentText())

        # =====================================================================
        # EDITING FEATURES SECTION
        # =====================================================================
        editing_label = QLabel("Video Editing Options (Advanced):")
        editing_label.setObjectName("header_label")
        layout.addWidget(editing_label)

        # Preset selector
        preset_layout = QHBoxLayout()
        preset_text = QLabel("Preset:")
        self.main_app.preset_combo = QComboBox()
        
        from .editing_config import get_preset_names, get_preset
        
        preset_names = get_preset_names()
        self.main_app.preset_combo.addItems(preset_names)
        self.main_app.preset_combo.setCurrentText("YouTube Edit")
        self.main_app.preset_combo.currentTextChanged.connect(
            self._on_preset_changed
        )
        
        preset_layout.addWidget(preset_text)
        preset_layout.addWidget(self.main_app.preset_combo)
        layout.addLayout(preset_layout)

        # Container format selection
        container_layout = QHBoxLayout()
        container_text = QLabel("Container:")
        self.main_app.container_combo = QComboBox()
        
        from .editing_config import CONTAINERS, CONTAINER_DESCRIPTIONS
        
        self.main_app.container_combo.addItems(list(CONTAINERS.keys()))
        self.main_app.container_combo.setCurrentText("MP4")
        self.main_app.container_combo.currentTextChanged.connect(
            self._on_container_changed
        )
        
        container_layout.addWidget(container_text)
        container_layout.addWidget(self.main_app.container_combo)
        layout.addLayout(container_layout)

        # Video codec selection
        codec_layout = QHBoxLayout()
        codec_text = QLabel("Video Codec:")
        self.main_app.video_codec_combo = QComboBox()
        
        from .editing_config import VIDEO_CODECS
        
        codec_names = list(VIDEO_CODECS.keys())
        self.main_app.video_codec_combo.addItems(codec_names)
        self.main_app.video_codec_combo.setCurrentText("H264")
        self.main_app.video_codec_combo.currentTextChanged.connect(
            self._on_codec_changed
        )
        
        codec_layout.addWidget(codec_text)
        codec_layout.addWidget(self.main_app.video_codec_combo)
        layout.addLayout(codec_layout)

        # Audio export selection
        audio_layout = QHBoxLayout()
        audio_text = QLabel("Audio Export:")
        self.main_app.audio_export_combo = QComboBox()
        
        from .editing_config import AUDIO_EXPORT_OPTIONS
        
        audio_names = list(AUDIO_EXPORT_OPTIONS.keys())
        self.main_app.audio_export_combo.addItems(audio_names)
        self.main_app.audio_export_combo.setCurrentText("AAC")
        self.main_app.audio_export_combo.currentTextChanged.connect(
            self._on_audio_export_changed
        )
        
        audio_layout.addWidget(audio_text)
        audio_layout.addWidget(self.main_app.audio_export_combo)
        layout.addLayout(audio_layout)

        # =====================================================================
        # ADVANCED AUDIO CONTROLS SECTION
        # =====================================================================
        
        # Audio codec selection
        audio_codec_layout = QHBoxLayout()
        audio_codec_text = QLabel("Audio Codec:")
        self.main_app.audio_codec_combo = QComboBox()
        
        from .editing_config import AUDIO_CODECS
        
        audio_codec_names = list(AUDIO_CODECS.keys())
        self.main_app.audio_codec_combo.addItems(audio_codec_names)
        self.main_app.audio_codec_combo.setCurrentText("AAC")
        self.main_app.audio_codec_combo.currentTextChanged.connect(
            self._on_audio_codec_changed
        )
        
        audio_codec_layout.addWidget(audio_codec_text)
        audio_codec_layout.addWidget(self.main_app.audio_codec_combo)
        layout.addLayout(audio_codec_layout)

        # Sample rate selection
        sample_rate_layout = QHBoxLayout()
        sample_rate_text = QLabel("Sample Rate:")
        self.main_app.sample_rate_combo = QComboBox()
        
        from .editing_config import SAMPLE_RATES
        
        sample_rate_keys = list(SAMPLE_RATES.keys())
        self.main_app.sample_rate_combo.addItems(sample_rate_keys)
        self.main_app.sample_rate_combo.setCurrentText("48000")
        self.main_app.sample_rate_combo.currentTextChanged.connect(
            self._on_sample_rate_changed
        )
        
        sample_rate_layout.addWidget(sample_rate_text)
        sample_rate_layout.addWidget(self.main_app.sample_rate_combo)
        layout.addLayout(sample_rate_layout)

        # PCM bit depth selection (only shown for PCM codec)
        pcm_layout = QHBoxLayout()
        pcm_text = QLabel("PCM Bit Depth:")
        self.main_app.pcm_bit_depth_combo = QComboBox()
        
        from .editing_config import PCM_BIT_DEPTHS
        
        pcm_bit_keys = list(PCM_BIT_DEPTHS.keys())
        self.main_app.pcm_bit_depth_combo.addItems(pcm_bit_keys)
        self.main_app.pcm_bit_depth_combo.setCurrentText("24 bit")
        self.main_app.pcm_bit_depth_combo.currentTextChanged.connect(
            self._on_pcm_bit_depth_changed
        )
        
        pcm_layout.addWidget(pcm_text)
        pcm_layout.addWidget(self.main_app.pcm_bit_depth_combo)
        self.main_app.pcm_bit_depth_label = pcm_text
        self.main_app.pcm_layout = pcm_layout
        layout.addLayout(pcm_layout)
        # Hide PCM controls initially (only show when PCM codec selected)
        pcm_text.hide()
        self.main_app.pcm_bit_depth_combo.hide()

        # AAC bitrate selection (only shown for AAC codec)
        aac_layout = QHBoxLayout()
        aac_text = QLabel("AAC Bitrate:")
        self.main_app.aac_bitrate_combo = QComboBox()
        
        from .editing_config import AAC_BITRATES
        
        aac_bitrate_keys = list(AAC_BITRATES.keys())
        self.main_app.aac_bitrate_combo.addItems(aac_bitrate_keys)
        self.main_app.aac_bitrate_combo.setCurrentText("320k")
        self.main_app.aac_bitrate_combo.currentTextChanged.connect(
            self._on_aac_bitrate_changed
        )
        
        aac_layout.addWidget(aac_text)
        aac_layout.addWidget(self.main_app.aac_bitrate_combo)
        self.main_app.aac_bitrate_label = aac_text
        layout.addLayout(aac_layout)
        # Show AAC controls initially (AAC is default)
        aac_text.show()
        self.main_app.aac_bitrate_combo.show()

        # FPS limiting
        fps_layout = QHBoxLayout()
        fps_text = QLabel("FPS Limit:")
        self.main_app.fps_combo = QComboBox()
        
        from .editing_config import FPS_OPTIONS
        
        fps_keys = list(FPS_OPTIONS.keys())
        self.main_app.fps_combo.addItems(fps_keys)
        self.main_app.fps_combo.setCurrentText("Original")
        self.main_app.fps_combo.currentTextChanged.connect(
            self._on_fps_changed
        )
        
        fps_layout.addWidget(fps_text)
        fps_layout.addWidget(self.main_app.fps_combo)
        layout.addLayout(fps_layout)

        # =====================================================================
        # CLIP CUTTER SECTION (OPTIONAL FEATURE)
        # =====================================================================
        
        clip_label = QLabel("Clip Cutter (Optional - leave empty to disable):")
        clip_label.setObjectName("header_label")
        layout.addWidget(clip_label)

        # Start time input
        start_layout = QHBoxLayout()
        start_text = QLabel("Start Time (HH:MM:SS):")
        self.main_app.clip_start_input = QLineEdit()
        self.main_app.clip_start_input.setPlaceholderText("00:01:20")
        self.main_app.clip_start_input.textChanged.connect(self._on_clip_start_changed)
        
        start_layout.addWidget(start_text)
        start_layout.addWidget(self.main_app.clip_start_input)
        layout.addLayout(start_layout)

        # End time input
        end_layout = QHBoxLayout()
        end_text = QLabel("End Time (HH:MM:SS):")
        self.main_app.clip_end_input = QLineEdit()
        self.main_app.clip_end_input.setPlaceholderText("00:02:10")
        self.main_app.clip_end_input.textChanged.connect(self._on_clip_end_changed)
        
        end_layout.addWidget(end_text)
        end_layout.addWidget(self.main_app.clip_end_input)
        layout.addLayout(end_layout)

        # =====================================================================
        # END CLIP CUTTER SECTION
        # =====================================================================

        # =====================================================================
        # END ADVANCED AUDIO CONTROLS SECTION
        # =====================================================================

        # Download button
        download_btn = QPushButton("Download")
        download_btn.setObjectName("download_button")
        download_btn.clicked.connect(self.main_app.download_manager.add_to_queue)
        layout.addWidget(download_btn)

        # Push content to top
        layout.addStretch()

        return page

    def mode_changed(self, text: str) -> None:
        """
        Handle download mode change to show/hide relevant controls.

        Args:
            text: Selected download mode text
        """
        self.main_app.mode_var = text

        # Hide video quality controls for audio-only modes
        if "MP3" in text:
            self.main_app.video_quality_label.hide()
            self.main_app.video_quality_combo.hide()
        else:
            self.main_app.video_quality_label.show()
            self.main_app.video_quality_combo.show()

    def _on_preset_changed(self, preset_name: str) -> None:
        """
        Handle preset change. Apply preset to UI and app state.

        Args:
            preset_name: Name of selected preset
        """
        from .editing_config import apply_preset
        
        self.main_app.editing_preset = preset_name
        config = apply_preset(preset_name)
        
        # Update UI controls to match preset
        if self.main_app.container_combo:
            self.main_app.container_combo.blockSignals(True)
            self.main_app.container_combo.setCurrentText(config["container"])
            self.main_app.container_combo.blockSignals(False)
        
        if self.main_app.video_codec_combo:
            self.main_app.video_codec_combo.blockSignals(True)
            self.main_app.video_codec_combo.setCurrentText(config["video_codec"])
            self.main_app.video_codec_combo.blockSignals(False)
        
        if self.main_app.audio_export_combo:
            self.main_app.audio_export_combo.blockSignals(True)
            self.main_app.audio_export_combo.setCurrentText(config["audio_export"])
            self.main_app.audio_export_combo.blockSignals(False)
        
        # Update advanced audio parameters from preset
        if self.main_app.audio_codec_combo:
            self.main_app.audio_codec_combo.blockSignals(True)
            self.main_app.audio_codec_combo.setCurrentText(config.get("audio_codec", "AAC"))
            self.main_app.audio_codec_combo.blockSignals(False)
        
        if self.main_app.sample_rate_combo:
            self.main_app.sample_rate_combo.blockSignals(True)
            self.main_app.sample_rate_combo.setCurrentText(config.get("sample_rate", "48000"))
            self.main_app.sample_rate_combo.blockSignals(False)
        
        if self.main_app.pcm_bit_depth_combo:
            self.main_app.pcm_bit_depth_combo.blockSignals(True)
            self.main_app.pcm_bit_depth_combo.setCurrentText(config.get("pcm_bit_depth", "24 bit"))
            self.main_app.pcm_bit_depth_combo.blockSignals(False)
        
        if self.main_app.aac_bitrate_combo:
            self.main_app.aac_bitrate_combo.blockSignals(True)
            self.main_app.aac_bitrate_combo.setCurrentText(config.get("aac_bitrate", "320k"))
            self.main_app.aac_bitrate_combo.blockSignals(False)
        
        if self.main_app.fps_combo:
            self.main_app.fps_combo.blockSignals(True)
            self.main_app.fps_combo.setCurrentText(config.get("fps", "Original"))
            self.main_app.fps_combo.blockSignals(False)
        
        # Update app state with all preset values
        self.main_app.container_format = config["container"]
        self.main_app.video_codec = config["video_codec"]
        self.main_app.audio_export_mode = config["audio_export"]
        self.main_app.use_audio_only = config["use_audio_only"]
        
        # Update advanced audio parameters in app state
        self.main_app.audio_codec = config.get("audio_codec", "AAC")
        self.main_app.sample_rate = config.get("sample_rate", "48000")
        self.main_app.pcm_bit_depth = config.get("pcm_bit_depth", "24 bit")
        self.main_app.aac_bitrate = config.get("aac_bitrate", "320k")
        self.main_app.fps = config.get("fps", "Original")
        
        # Update control visibility based on audio codec
        self._on_audio_codec_changed(self.main_app.audio_codec)

    def _on_container_changed(self, container_name: str) -> None:
        """
        Handle container format change.

        Args:
            container_name: Selected container format (MP4, MKV, MOV)
        """
        self.main_app.container_format = container_name
        # Reset preset to "Custom" or keep last selected
        if self.main_app.preset_combo:
            self.main_app.preset_combo.blockSignals(True)
            # Don't change preset, just update the internal state
            self.main_app.preset_combo.blockSignals(False)

    def _on_codec_changed(self, codec_name: str) -> None:
        """
        Handle video codec change.

        Args:
            codec_name: Selected video codec (H264, H265, ProRes, Copy)
        """
        self.main_app.video_codec = codec_name

    def _on_audio_export_changed(self, audio_name: str) -> None:
        """
        Handle audio export mode change.

        Args:
            audio_name: Selected audio export mode (WAV, FLAC, AAC, Copy)
        """
        self.main_app.audio_export_mode = audio_name

    def _on_audio_codec_changed(self, codec_name: str) -> None:
        """
        Handle audio codec change and show/hide dependent controls.

        Args:
            codec_name: Selected audio codec (Copy, PCM, AAC, FLAC)
        """
        self.main_app.audio_codec = codec_name
        
        # Show/hide dependent controls based on codec type
        if codec_name == "PCM":
            # Show PCM bit depth control for PCM codec
            self.main_app.pcm_bit_depth_label.show()
            self.main_app.pcm_bit_depth_combo.show()
            # Hide AAC bitrate control
            self.main_app.aac_bitrate_label.hide()
            self.main_app.aac_bitrate_combo.hide()
        elif codec_name == "AAC":
            # Hide PCM bit depth control for AAC codec
            self.main_app.pcm_bit_depth_label.hide()
            self.main_app.pcm_bit_depth_combo.hide()
            # Show AAC bitrate control
            self.main_app.aac_bitrate_label.show()
            self.main_app.aac_bitrate_combo.show()
        else:  # Copy or FLAC
            # Hide both dependent controls
            self.main_app.pcm_bit_depth_label.hide()
            self.main_app.pcm_bit_depth_combo.hide()
            self.main_app.aac_bitrate_label.hide()
            self.main_app.aac_bitrate_combo.hide()

    def _on_sample_rate_changed(self, sample_rate: str) -> None:
        """
        Handle sample rate change.

        Args:
            sample_rate: Selected sample rate (Original, 44100, 48000)
        """
        self.main_app.sample_rate = sample_rate

    def _on_pcm_bit_depth_changed(self, bit_depth: str) -> None:
        """
        Handle PCM bit depth change.

        Args:
            bit_depth: Selected bit depth (16 bit or 24 bit)
        """
        self.main_app.pcm_bit_depth = bit_depth

    def _on_aac_bitrate_changed(self, bitrate: str) -> None:
        """
        Handle AAC bitrate change.

        Args:
            bitrate: Selected AAC bitrate (128k, 192k, 320k)
        """
        self.main_app.aac_bitrate = bitrate

    def _on_fps_changed(self, fps: str) -> None:
        """
        Handle FPS limit change.

        Args:
            fps: Selected FPS (Original, 30 fps, 60 fps)
        """
        self.main_app.fps = fps

    def _on_clip_start_changed(self, text: str) -> None:
        """
        Handle clip start time change.

        Args:
            text: Start time in HH:MM:SS format
        """
        self.main_app.clip_start = text.strip()

    def _on_clip_end_changed(self, text: str) -> None:
        """
        Handle clip end time change.

        Args:
            text: End time in HH:MM:SS format
        """
        self.main_app.clip_end = text.strip()

    def create_activity_page(self) -> QWidget:
        """
        Create the activity/logging page for monitoring downloads.

        Returns:
            Widget containing activity log and progress information
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Page title
        title_label = QLabel("Download Activity")
        title_label.setObjectName("header_label")
        layout.addWidget(title_label)

        # Progress bar
        self.main_app.progress_bar = QProgressBar()
        self.main_app.progress_bar.setObjectName("progress_bar")
        self.main_app.progress_bar.setTextVisible(True)
        self.main_app.progress_bar.setValue(0)
        layout.addWidget(self.main_app.progress_bar)

        # Log text area
        self.main_app.log_text = QTextEdit(readOnly=True)
        layout.addWidget(self.main_app.log_text)

        # Control buttons
        button_layout = QHBoxLayout()

        # Clear log button
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(lambda: self.main_app.log_text.clear())
        button_layout.addWidget(clear_btn)

        button_layout.addStretch()

        # Queue status label
        self.main_app.queue_status_label = QLabel("Queue: 0 pending")
        self.main_app.queue_status_label.setObjectName("status_label")
        button_layout.addWidget(self.main_app.queue_status_label)

        layout.addLayout(button_layout)

        return page

    def _create_ui(self) -> None:
        """Create and layout the main user interface."""
        # Load stylesheet
        self._load_stylesheet()

        # Create menu bar
        self.create_menubar()

        # Central widget with horizontal layout
        central_widget = QWidget()
        self.main_app.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Sidebar navigation
        self.main_app.sidebar = self.create_sidebar()
        layout.addWidget(self.main_app.sidebar)

        # Main content area with stacked pages
        self.main_app.stack = QStackedWidget()
        self.main_app.download_page = self.create_download_page()
        self.main_app.activity_page = self.create_activity_page()
        self.main_app.stack.addWidget(self.main_app.download_page)
        self.main_app.stack.addWidget(self.main_app.activity_page)
        layout.addWidget(self.main_app.stack, 1)  # Expand to fill available space

        # Status bar
        self.main_app.status_bar = QStatusBar()
        self.main_app.setStatusBar(self.main_app.status_bar)
