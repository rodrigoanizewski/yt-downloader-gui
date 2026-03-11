"""
Command builder for yt-dlp downloads with advanced editing options.

This module provides a central interface for building yt-dlp command lines
with support for custom containers, video codecs, audio extraction, and
professional editing workflows.
"""

import os
from typing import List, Dict, Optional
from .editing_config import (
    CONTAINERS,
    VIDEO_CODECS,
    AUDIO_EXPORT_OPTIONS,
    AUDIO_CODECS,
    PCM_BIT_DEPTHS,
    SAMPLE_RATES,
    AAC_BITRATES,
    FPS_OPTIONS,
    get_preset,
)


class EditingCommandBuilder:
    """
    Builds yt-dlp command lines with video editing parameters.
    
    This class handles the generation of yt-dlp commands with support for:
    - Custom output containers (MP4, MKV, MOV)
    - Video codec selection (Copy, H264, H265, ProRes)
    - Audio extraction modes (WAV, FLAC, AAC, Copy)
    - Professional editing presets
    """

    def __init__(self, yt_dlp_path: str, ffmpeg_path: str):
        """
        Initialize the command builder.
        
        Args:
            yt_dlp_path: Path to yt-dlp executable
            ffmpeg_path: Path to ffmpeg executable
        """
        self.yt_dlp_path = yt_dlp_path
        self.ffmpeg_path = ffmpeg_path

    def validate_codec_container_compatibility(
        self, container: str, video_codec: str, audio_codec: str
    ) -> tuple[bool, str]:
        """
        Validate that codec/container combination is compatible.
        
        Args:
            container: Output container (MP4, MKV, MOV)
            video_codec: Video codec (Copy, H264, H265, ProRes)
            audio_codec: Audio codec (Copy, PCM, AAC, FLAC)
            
        Returns:
            Tuple (is_valid, error_message)
        """
        # MP4 container restrictions
        if container == "MP4":
            if video_codec == "ProRes":
                return False, "ProRes codec is not supported in MP4 container. Use MOV or MKV instead."
            if audio_codec == "PCM":
                return False, "PCM audio is not supported in MP4 container. Use AAC, FLAC, or Copy instead. (MOV/MKV recommended for PCM)"
            if audio_codec == "FLAC":
                return False, "FLAC audio is not supported in MP4 container. Use AAC or Copy instead. (MKV recommended for FLAC)"
        
        # MKV supports everything - no restrictions
        
        # MOV container restrictions
        if container == "MOV":
            # MOV supports most codecs, no restrictions for common use cases
            pass
        
        return True, ""

    def build_download_command(
        self,
        url: str,
        output_path: str,
        container: str = "MP4",
        video_codec: str = "H264",
        audio_export: str = "AAC",
        use_audio_only: bool = False,
        video_quality: str = "Best Available",
        apply_preset: bool = False,
        preset_name: Optional[str] = None,
        # Advanced audio parameters
        audio_codec: str = "AAC",
        sample_rate: str = "48000",
        pcm_bit_depth: str = "24 bit",
        aac_bitrate: str = "320k",
        fps: str = "Original",
        # Clip cutter parameters
        clip_start: str = "",
        clip_end: str = "",
        # Playlist parameters
        is_playlist: bool = False,
    ) -> List[str]:
        """
        Build a complete yt-dlp command with editing parameters.
        
        Command order (logical/correct):
        1. yt-dlp executable
        2. Global options (ffmpeg-location, extractor-args, user-agent)
        3. Playlist/format options (no-playlist, format)
        4. Output/merge options (output, merge-output-format)
        5. Postprocessor options (postprocessor-args, download-sections)
        6. URL (must be last)
        
        Args:
            url: YouTube URL to download
            output_path: Output directory path
            container: Output container format (MP4, MKV, MOV)
            video_codec: Video codec (Copy, H264, H265, ProRes)
            audio_export: Audio export mode (Copy, WAV, FLAC, AAC)
            use_audio_only: If True, extract audio only (ignores video_codec)
            video_quality: Video quality filter (e.g., "1080p", "720p", "Best Available")
            apply_preset: If True, use preset_name to override other parameters
            preset_name: Name of preset to apply (if apply_preset=True)
            audio_codec: Audio codec (Copy, PCM, AAC, FLAC)
            sample_rate: Sample rate (Original, 44100, 48000)
            pcm_bit_depth: PCM bit depth (16 bit, 24 bit)
            aac_bitrate: AAC bitrate (128k, 192k, 320k)
            fps: Frame rate limit (Original, 30, 60)
            clip_start: Start time for clip cutting (HH:MM:SS format, empty to disable)
            clip_end: End time for clip cutting (HH:MM:SS format, empty to disable)
            is_playlist: If True, output template includes playlist index to ensure unique filenames
            
        Returns:
            List of command arguments for subprocess.Popen()
        """
        # Respect user's explicit mode selection (Single Video vs Playlist)
        # When Single Video mode: remove playlist parameter from URL
        # When Playlist mode: keep URL unchanged
        if not is_playlist:
            # Single video mode: strip the playlist parameter if present
            clean_url = url.split("&list=")[0] if "&list=" in url else url
        else:
            # Playlist mode: keep URL unchanged
            clean_url = url
        
        # Apply preset if requested
        if apply_preset and preset_name:
            preset = get_preset(preset_name)
            if preset:
                container = preset.container
                video_codec = preset.video_codec
                audio_export = preset.audio_export
                use_audio_only = preset.use_audio_only
                audio_codec = preset.audio_codec
                sample_rate = preset.sample_rate
                pcm_bit_depth = preset.pcm_bit_depth
                aac_bitrate = preset.aac_bitrate
                fps = preset.fps

        # Build base command with proper ordering
        # 1. Executable and core options
        cmd = [
            self.yt_dlp_path,
            "--ffmpeg-location",
            self.ffmpeg_path,

            "--user-agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        ]
        
        # Only add --no-playlist for single videos (not playlists)
        if not is_playlist:
            cmd.append("--no-playlist")

        # Handle audio-only extraction
        if use_audio_only:
            cmd.extend(["--format", "bestaudio/best"])
            cmd.extend(["--extract-audio"])
            
            # Configure audio format and quality
            if audio_export == "WAV":
                cmd.extend(["--audio-format", "wav"])
                # WAV quality is handled via postprocessor args
            elif audio_export == "FLAC":
                cmd.extend(["--audio-format", "flac"])
            elif audio_export == "AAC":
                cmd.extend(["--audio-format", "aac"])
                cmd.extend(["--audio-quality", "320K"])
            # "Copy" mode: keep original audio format
            else:
                cmd.extend(["--audio-format", "best"])
        else:
            # Video download with optional codec/container customization
            cmd = self._add_video_format_options(cmd, video_quality)
            
            # Add postprocessor arguments for codec and container
            cmd = self._add_postprocessor_args(
                cmd, video_codec, audio_export, container,
                audio_codec, sample_rate, pcm_bit_depth, aac_bitrate, fps
            )

        # Add output path (must come before clip cutter and URL)
        # Use appropriate filename template based on mode
        if is_playlist:
            # Playlist format: zero-padded index - title
            # Example: 001 - Video Title.mp4, 002 - Another Video.mp4
            output_template = "%(playlist_index)03d - %(title)s.%(ext)s"
        else:
            # Single video format: just title
            output_template = "%(title)s.%(ext)s"
        
        cmd.extend(["--output", os.path.join(output_path, output_template)])

        # Add clip cutter if both start and end times are provided
        if clip_start and clip_end:
            cmd.extend(["--download-sections", f"*{clip_start}-{clip_end}"])

        # Add URL at the end (must be last argument)
        # Use cleaned URL for single video mode (with playlist param removed)
        cmd.append(clean_url)

        return cmd

    def _add_video_format_options(
        self, cmd: List[str], video_quality: str
    ) -> List[str]:
        """
        Add video format selection to command with robust fallback.
        
        This uses a flexible format string that doesn't restrict to specific 
        extensions, which prevents HTTP 403 errors when MP4/M4A streams aren't
        available for certain videos.
        
        Args:
            cmd: Current command list
            video_quality: Quality filter (e.g., "1080p", "720p", "Best Available")
            
        Returns:
            Updated command list
        """
        if video_quality == "Best Available":
            # Robust format: best video + best audio with generic fallback
            # This avoids HTTP 403 errors on videos without MP4/M4A streams
            cmd.extend(["--format", "bestvideo+bestaudio/best"])
        else:
            # Apply quality filter (e.g., "720p" -> height<=720)
            try:
                height = video_quality.split("p")[0]
                format_str = f"bestvideo[height<={height}]+bestaudio/best"
                cmd.extend(["--format", format_str])
            except (IndexError, ValueError):
                # If parsing fails, use best available with robust fallback
                cmd.extend(["--format", "bestvideo+bestaudio/best"])

        return cmd

    def _add_postprocessor_args(
        self,
        cmd: List[str],
        video_codec: str,
        audio_export: str,
        container: str,
        audio_codec: str = "AAC",
        sample_rate: str = "48000",
        pcm_bit_depth: str = "24 bit",
        aac_bitrate: str = "320k",
        fps: str = "Original",
    ) -> List[str]:
        """
        Add postprocessor arguments for codec conversion and audio handling.
        
        Args:
            cmd: Current command list
            video_codec: Video codec selection (Copy, H264, H265, ProRes)
            audio_export: Audio export mode (for backward compatibility)
            container: Output container format
            audio_codec: Audio codec (Copy, PCM, AAC, FLAC)
            sample_rate: Sample rate (Original, 44100, 48000)
            pcm_bit_depth: PCM bit depth (16 bit, 24 bit)
            aac_bitrate: AAC bitrate (128k, 192k, 320k)
            fps: Frame rate limit (Original, 30, 60)
            
        Returns:
            Updated command list
        """
        # Get video codec postprocessor args
        codec_config = VIDEO_CODECS.get(video_codec, VIDEO_CODECS["H264"])
        video_codec_args = codec_config["postprocessor_args"]

        # Build audio codec arguments based on codec selection
        audio_codec_args = self._build_audio_codec_args(
            audio_codec, pcm_bit_depth, aac_bitrate
        )
        
        # Build sample rate arguments
        sample_rate_config = SAMPLE_RATES.get(sample_rate, SAMPLE_RATES["Original"])
        sample_rate_args = sample_rate_config["sample_rate_args"]
        
        # Build FPS arguments
        fps_config = FPS_OPTIONS.get(fps, FPS_OPTIONS["Original"])
        fps_args = fps_config["fps_args"]
        
        # Combine all postprocessor args
        # Order: video codec, audio codec, sample rate, fps, progress
        combined_parts = [video_codec_args, audio_codec_args, sample_rate_args, fps_args]
        combined_args = " ".join(part for part in combined_parts if part).strip()
        
        # Add FFmpeg progress reporting for real-time encoding feedback
        # This allows the GUI to display encoding progress to the user
        if combined_args:
            combined_args += " -progress pipe:1"
        else:
            combined_args = "-progress pipe:1"

        # Add postprocessor-args to command
        if combined_args:
            cmd.extend(["--postprocessor-args", combined_args])

        # Add merge output format (container)
        container_format = CONTAINERS.get(container, "mp4")
        cmd.extend(["--merge-output-format", container_format])

        return cmd

    def _build_audio_codec_args(
        self,
        audio_codec: str,
        pcm_bit_depth: str,
        aac_bitrate: str,
    ) -> str:
        """
        Build FFmpeg audio codec arguments.
        
        Args:
            audio_codec: Audio codec (Copy, PCM, AAC, FLAC)
            pcm_bit_depth: PCM bit depth (16 bit, 24 bit) - only used for PCM
            aac_bitrate: AAC bitrate (128k, 192k, 320k) - only used for AAC
            
        Returns:
            FFmpeg audio codec arguments string
        """
        if audio_codec == "Copy":
            return "-c:a copy"
        
        elif audio_codec == "PCM":
            # Use bit depth to determine exact PCM codec
            pcm_config = PCM_BIT_DEPTHS.get(pcm_bit_depth, PCM_BIT_DEPTHS["24 bit"])
            return pcm_config["codec_args"]
        
        elif audio_codec == "AAC":
            # Get bitrate args and combine with AAC codec
            bitrate_config = AAC_BITRATES.get(aac_bitrate, AAC_BITRATES["320k"])
            return f"{AUDIO_CODECS['AAC']['codec_args']} {bitrate_config['bitrate_args']}"
        
        elif audio_codec == "FLAC":
            return AUDIO_CODECS["FLAC"]["codec_args"]
        
        else:
            # Default to AAC with 320k bitrate
            bitrate_config = AAC_BITRATES.get(aac_bitrate, AAC_BITRATES["320k"])
            return f"{AUDIO_CODECS['AAC']['codec_args']} {bitrate_config['bitrate_args']}"

    def build_standard_video_command(
        self,
        url: str,
        output_path: str,
        video_quality: str = "Best Available",
    ) -> List[str]:
        """
        Build standard video download command (backward compatible with existing code).
        
        Args:
            url: YouTube URL
            output_path: Output directory path
            video_quality: Video quality filter
            
        Returns:
            List of command arguments
        """
        return self.build_download_command(
            url=url,
            output_path=output_path,
            container="MP4",
            video_codec="H264",
            audio_export="AAC",
            use_audio_only=False,
            video_quality=video_quality,
        )

    def build_standard_audio_command(
        self,
        url: str,
        output_path: str,
        audio_quality: str = "320",
    ) -> List[str]:
        """
        Build standard audio extraction command (backward compatible with existing code).
        
        Args:
            url: YouTube URL
            output_path: Output directory path
            audio_quality: Audio quality in kbps
            
        Returns:
            List of command arguments
        """
        cmd = [
            self.yt_dlp_path,
            "--ffmpeg-location",
            self.ffmpeg_path,
            "--no-playlist",
            "--output",
            os.path.join(output_path, "%(playlist_index)s - %(title)s.%(ext)s"),
            "--format",
            "bestaudio/best",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--audio-quality",
            audio_quality,
            url,
        ]
        return cmd

    @staticmethod
    def format_command_for_logging(cmd: List[str]) -> str:
        """
        Format a command list into a readable string for logging/debugging.
        
        This method takes a command list and formats it with proper spacing
        for readability while protecting arguments that contain spaces.
        
        Args:
            cmd: List of command arguments
            
        Returns:
            Formatted command string suitable for logging
        """
        # Join arguments with spaces, quoting those that contain spaces or special chars
        formatted_args = []
        for arg in cmd:
            # Quote arguments that contain spaces, special characters, or are complex paths
            if any(char in str(arg) for char in [' ', '\\', ':', '"', "'"]):
                # Use double quotes and escape any existing quotes
                formatted_args.append(f'"{str(arg)}"')
            else:
                formatted_args.append(str(arg))
        
        return " ".join(formatted_args)


def create_editing_command_builder(
    yt_dlp_path: str, ffmpeg_path: str
) -> EditingCommandBuilder:
    """
    Factory function to create an EditingCommandBuilder instance.
    
    Args:
        yt_dlp_path: Path to yt-dlp executable
        ffmpeg_path: Path to ffmpeg executable
        
    Returns:
        EditingCommandBuilder instance
    """
    return EditingCommandBuilder(yt_dlp_path, ffmpeg_path)
