"""
Configuration for video editing features (codecs, containers, presets).

This module defines all codec options, audio extraction options, and preset
configurations for professional video editing workflows.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass

# ============================================================================
# CONTAINER FORMATS
# ============================================================================

CONTAINERS = {
    "MP4": "mp4",
    "MKV": "mkv",
    "MOV": "mov",
}

CONTAINER_DESCRIPTIONS = {
    "MP4": "H.264 compatible, ideal for web and Adobe Premiere",
    "MKV": "Matroska format, supports multiple streams, great for archival",
    "MOV": "Apple's QuickTime format, native in Final Cut Pro",
}

# ============================================================================
# VIDEO CODEC OPTIONS
# ============================================================================

VIDEO_CODECS = {
    "Copy": {
        "display_name": "Copy (no re-encoding)",
        "postprocessor_args": "-c:v copy",
        "description": "Fastest option, no quality loss, direct copy",
    },
    "H264": {
        "display_name": "H.264 (libx264)",
        "postprocessor_args": "-c:v libx264 -preset slow -crf 18",
        "description": "High quality, good compatibility, slower encoding",
    },
    "H265": {
        "display_name": "H.265 (libx265)",
        "postprocessor_args": "-c:v libx265 -crf 20",
        "description": "Better compression, smaller file sizes, 50% encoding time",
    },
    "ProRes": {
        "display_name": "ProRes (prores_ks)",
        "postprocessor_args": "-c:v prores_ks -profile:v 3",
        "description": "Apple ProRes 422 HQ, professional editing standard",
    },
}

# ============================================================================
# AUDIO CODEC OPTIONS (FOR ADVANCED AUDIO CONTROL)
# ============================================================================

AUDIO_CODECS = {
    "Copy": {
        "display_name": "Copy",
        "codec_args": "-c:a copy",
        "description": "Keep original audio codec",
    },
    "PCM": {
        "display_name": "PCM",
        "codec_args": "",  # Will be set based on bit depth
        "description": "Lossless PCM audio (bit depth set separately)",
    },
    "AAC": {
        "display_name": "AAC",
        "codec_args": "-c:a aac",
        "description": "Advanced Audio Codec",
    },
    "FLAC": {
        "display_name": "FLAC",
        "codec_args": "-c:a flac",
        "description": "Free Lossless Audio Codec",
    },
}

# ============================================================================
# PCM BIT DEPTH OPTIONS
# ============================================================================

PCM_BIT_DEPTHS = {
    "16 bit": {
        "display_name": "16 bit",
        "codec_args": "-c:a pcm_s16le",
        "description": "16-bit signed little-endian PCM",
    },
    "24 bit": {
        "display_name": "24 bit",
        "codec_args": "-c:a pcm_s24le",
        "description": "24-bit signed little-endian PCM (broadcast standard)",
    },
}

# ============================================================================
# SAMPLE RATE OPTIONS
# ============================================================================

SAMPLE_RATES = {
    "Original": {
        "display_name": "Original",
        "sample_rate_args": "",
        "description": "Keep original sample rate",
    },
    "44100": {
        "display_name": "44100 Hz",
        "sample_rate_args": "-ar 44100",
        "description": "CD quality (44.1 kHz)",
    },
    "48000": {
        "display_name": "48000 Hz",
        "sample_rate_args": "-ar 48000",
        "description": "Video standard (48 kHz)",
    },
}

# ============================================================================
# AAC BITRATE OPTIONS
# ============================================================================

AAC_BITRATES = {
    "128k": {
        "display_name": "128 kbps",
        "bitrate_args": "-b:a 128k",
        "description": "Standard streaming quality",
    },
    "192k": {
        "display_name": "192 kbps",
        "bitrate_args": "-b:a 192k",
        "description": "Good quality",
    },
    "320k": {
        "display_name": "320 kbps",
        "bitrate_args": "-b:a 320k",
        "description": "High quality",
    },
}

# ============================================================================
# FPS (FRAMES PER SECOND) OPTIONS
# ============================================================================

FPS_OPTIONS = {
    "Original": {
        "display_name": "Original",
        "fps_args": "",
        "description": "Keep original frame rate",
    },
    "30": {
        "display_name": "30 fps",
        "fps_args": "-filter:v fps=30",
        "description": "Standard video frame rate",
    },
    "60": {
        "display_name": "60 fps",
        "fps_args": "-filter:v fps=60",
        "description": "High frame rate",
    },
}

# ============================================================================
# AUDIO EXTRACTION OPTIONS (SFX WORKFLOWS)
# ============================================================================

AUDIO_EXPORT_OPTIONS = {
    "Copy": {
        "display_name": "Copy (no conversion)",
        "postprocessor_args": "-vn -c:a copy",
        "description": "Keep original audio format and quality",
    },
    "WAV": {
        "display_name": "WAV (PCM 24-bit 48kHz)",
        "postprocessor_args": "-vn -c:a pcm_s24le -ar 48000",
        "description": "Lossless PCM audio, broadcast quality",
    },
    "FLAC": {
        "display_name": "FLAC (Lossless)",
        "postprocessor_args": "-vn -c:a flac",
        "description": "Lossless compression, larger than ZIP",
    },
    "AAC": {
        "display_name": "AAC (320 kbps)",
        "postprocessor_args": "-vn -c:a aac -b:a 320k",
        "description": "High quality lossy compression",
    },
}

# ============================================================================
# EDITING PRESETS
# ============================================================================

@dataclass
class EditingPreset:
    """Represents a preset configuration for video editing workflows."""
    name: str
    description: str
    container: str
    video_codec: str
    audio_export: str
    use_audio_only: bool = False
    # Advanced audio parameters
    audio_codec: str = "AAC"  # For advanced audio control
    sample_rate: str = "48000"  # 44100, 48000, or Original
    pcm_bit_depth: str = "24 bit"  # 16 bit or 24 bit
    aac_bitrate: str = "320k"  # 128k, 192k, 320k
    fps: str = "Original"  # Original, 30, 60


EDITING_PRESETS: Dict[str, EditingPreset] = {
    "YouTube Edit": EditingPreset(
        name="YouTube Edit",
        description="Optimized for YouTube: MP4 H.264 with AAC audio",
        container="MP4",
        video_codec="H264",
        audio_export="AAC",
        use_audio_only=False,
    ),
    "Professional Editing": EditingPreset(
        name="Professional Editing",
        description="DaVinci/Premiere ready: MOV with ProRes and PCM audio",
        container="MOV",
        video_codec="ProRes",
        audio_export="WAV",
        use_audio_only=False,
    ),
    "Fast Download": EditingPreset(
        name="Fast Download",
        description="No re-encoding: MKV with copy codecs",
        container="MKV",
        video_codec="Copy",
        audio_export="Copy",
        use_audio_only=False,
    ),
    "DaVinci Resolve": EditingPreset(
        name="DaVinci Resolve",
        description="Optimized for DaVinci Resolve: MOV ProRes with WAV audio",
        container="MOV",
        video_codec="ProRes",
        audio_export="WAV",
        use_audio_only=False,
    ),
    "Adobe Premiere": EditingPreset(
        name="Adobe Premiere",
        description="Optimized for Premiere Pro: MP4 H.264 with AAC",
        container="MP4",
        video_codec="H264",
        audio_export="AAC",
        use_audio_only=False,
    ),
    "After Effects": EditingPreset(
        name="After Effects",
        description="Optimized for After Effects: MOV H.264 with AAC",
        container="MOV",
        video_codec="H264",
        audio_export="AAC",
        use_audio_only=False,
    ),
    "Final Cut Pro": EditingPreset(
        name="Final Cut Pro",
        description="Optimized for Final Cut Pro: MOV ProRes with WAV",
        container="MOV",
        video_codec="ProRes",
        audio_export="WAV",
        use_audio_only=False,
    ),
    "SFX PCM Audio": EditingPreset(
        name="SFX PCM Audio",
        description="Extract audio only: WAV 48kHz 24-bit PCM",
        container="MOV",
        video_codec="Copy",
        audio_export="WAV",
        use_audio_only=True,
    ),
    "SFX FLAC Audio": EditingPreset(
        name="SFX FLAC Audio",
        description="Extract audio only: FLAC lossless",
        container="MKV",
        video_codec="Copy",
        audio_export="FLAC",
        use_audio_only=True,
    ),
}


def get_preset_names() -> List[str]:
    """Get list of all available preset names."""
    return list(EDITING_PRESETS.keys())


def get_preset(preset_name: str) -> EditingPreset:
    """
    Get a preset by name.
    
    Args:
        preset_name: Name of the preset
        
    Returns:
        EditingPreset object, or None if not found
    """
    return EDITING_PRESETS.get(preset_name)


def apply_preset(preset_name: str) -> Dict[str, str]:
    """
    Apply a preset and return configuration dictionary.
    
    Args:
        preset_name: Name of the preset to apply
        
    Returns:
        Dictionary with keys: container, video_codec, audio_export, use_audio_only,
        audio_codec, sample_rate, pcm_bit_depth, aac_bitrate, fps
    """
    preset = get_preset(preset_name)
    if not preset:
        # Return default/safe values
        return {
            "container": "MP4",
            "video_codec": "H264",
            "audio_export": "AAC",
            "use_audio_only": False,
            "audio_codec": "AAC",
            "sample_rate": "48000",
            "pcm_bit_depth": "24 bit",
            "aac_bitrate": "320k",
            "fps": "Original",
        }
    
    return {
        "container": preset.container,
        "video_codec": preset.video_codec,
        "audio_export": preset.audio_export,
        "use_audio_only": preset.use_audio_only,
        "audio_codec": preset.audio_codec,
        "sample_rate": preset.sample_rate,
        "pcm_bit_depth": preset.pcm_bit_depth,
        "aac_bitrate": preset.aac_bitrate,
        "fps": preset.fps,
    }
