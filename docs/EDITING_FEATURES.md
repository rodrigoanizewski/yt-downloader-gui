# Video Editing Features Extension Documentation

## Overview

This extension adds professional video editing workflow support to **yt-downloader-gui** without breaking existing functionality. Users can now:

- Select output container formats (MP4, MKV, MOV)
- Choose video codecs (Copy, H264, H265, ProRes)
- Configure audio export modes (WAV, FLAC, AAC, Copy)
- Apply editing presets (YouTube Edit, DaVinci Resolve, Adobe Premiere, Final Cut Pro, etc.)

## New Modules Created

### 1. `src/app/editing_config.py`
**Purpose**: Central configuration for editing feature options

**Key Components**:
- `CONTAINERS`: Dictionary mapping container names to yt-dlp format codes
- `VIDEO_CODECS`: Video codec options with FFmpeg postprocessor arguments
- `AUDIO_EXPORT_OPTIONS`: Audio extraction modes with detailed FFmpeg parameters
- `EDITING_PRESETS`: Pre-configured workflows for professional editing software

**Available Options**:

#### Containers
```
MP4  → mp4   (H.264 compatible, Adobe Premiere, YouTube)
MKV  → mkv   (Matroska, multiple streams, archival)
MOV  → mov   (QuickTime, Final Cut Pro, Apple ecosystem)
```

#### Video Codecs
```
Copy    → "-c copy"                                      (No re-encoding, fastest)
H264    → "-c:v libx264 -preset slow -crf 18"          (High quality, slow)
H265    → "-c:v libx265 -crf 20"                        (Better compression, 50% faster)
ProRes  → "-c:v prores_ks -profile:v 3"                (Apple ProRes 422 HQ)
```

#### Audio Export Modes
```
Copy    → "-vn -c:a copy"                              (Original format)
WAV     → "-vn -c:a pcm_s24le -ar 48000"               (PCM 24bit 48kHz, broadcast)
FLAC    → "-vn -c:a flac"                              (Lossless compression)
AAC     → "-vn -c:a aac -b:a 320k"                     (High quality lossy)
```

#### Available Presets
1. **YouTube Edit**: MP4 H.264 + AAC (YouTube optimized)
2. **Professional Editing**: MOV ProRes + WAV (DaVinci/Premiere ready)
3. **Fast Download**: MKV Copy + Copy (No re-encoding)
4. **DaVinci Resolve**: MOV ProRes + WAV
5. **Adobe Premiere**: MP4 H.264 + AAC
6. **After Effects**: MOV H.264 + AAC
7. **Final Cut Pro**: MOV ProRes + WAV
8. **SFX PCM Audio**: Audio-only WAV extraction
9. **SFX FLAC Audio**: Audio-only FLAC extraction

### 2. `src/app/command_builder.py`
**Purpose**: Dynamic yt-dlp command generation with editing parameters

**Key Class**: `EditingCommandBuilder`

**Main Methods**:

#### `build_download_command()`
Builds complete yt-dlp commands with editing parameters.

```python
cmd = builder.build_download_command(
    url="https://www.youtube.com/watch?v=...",
    output_path="/path/to/downloads",
    container="MP4",           # Container format
    video_codec="H264",        # Video codec
    audio_export="AAC",        # Audio mode
    use_audio_only=False,      # Extract audio only?
    video_quality="1080p",     # Quality filter
    apply_preset=False,        # Use preset?
    preset_name="YouTube Edit" # Which preset?
)
# Returns: List of command arguments for subprocess.Popen()
```

#### `build_standard_video_command()`
Backward-compatible video download (uses YouTube presets).

#### `build_standard_audio_command()`
Backward-compatible audio extraction (keeps original MP3 extraction).

**Command Structure**:
```
yt-dlp --ffmpeg-location <path>
       --no-playlist
       --output "<path>/%(title)s.%(ext)s"
       --format <quality>
       --postprocessor-args "<codec_args> <audio_args>"
       --merge-output-format <container>
       <url>
```

## Modified Files

### 1. `src/app/main_window.py`

**New UI Element Declarations** (lines ~25):
```python
preset_combo: Optional[QComboBox] = None
container_combo: Optional[QComboBox] = None
video_codec_combo: Optional[QComboBox] = None
audio_export_combo: Optional[QComboBox] = None
```

**New State Variables** (in `_initialize_state()`):
```python
self.editing_preset = "YouTube Edit"      # Current preset
self.container_format = "MP4"              # Output container
self.video_codec = "H264"                  # Video codec
self.audio_export_mode = "AAC"             # Audio export mode
self.use_audio_only = False                # Audio-only flag
```

### 2. `src/app/download_manager.py`

**New Import**:
```python
from .command_builder import create_editing_command_builder
```

**Updated `_handle_single_download()`**:
- Added editing parameters to download tasks:
  - `container`, `video_codec`, `audio_export`, `preset`
- Same for `_process_selected_videos()` (playlist/channel downloads)

**Updated `download_video()`**:
- Uses `EditingCommandBuilder` instead of `_build_video_download_command()`
- Respects editing feature parameters from GUI selections
- Maintains backward compatibility with MP3 extraction

### 3. `src/app/ui_manager.py`

**New Methods**:
- `_on_preset_changed(preset_name)`: Applies preset to UI and app state
- `_on_container_changed(container_name)`: Updates container selection
- `_on_codec_changed(codec_name)`: Updates video codec
- `_on_audio_export_changed(audio_name)`: Updates audio export mode

**Updated `create_download_page()`**:
- Added "Video Editing Options (Advanced)" section
- Preset selector combo box
- Container format selector
- Video codec selector
- Audio export mode selector
- All with proper signal connections and state updates

## Integration Points

### How It Works

1. **User Interface Flow**:
   ```
   User selects preset → Updates all UI controls
   User manually changes container/codec/audio → Updates internal state
   User clicks Download → Task includes editing parameters
   ```

2. **Download Flow**:
   ```
   add_to_queue() → Creates task with editing parameters
   ↓
   download_video() → Uses EditingCommandBuilder
   ↓
   Builds yt-dlp command with FFmpeg postprocessor args
   ↓
   subprocess.Popen() executes command
   ```

3. **Backward Compatibility**:
   - Original `_build_video_download_command()` and `_build_audio_download_command()` remain unused but intact
   - MP3 extraction uses `build_standard_audio_command()` (same output format as before)
   - YouTube presets mirror original behavior (MP4 H.264 AAC)
   - Existing GUI modes (Playlist, Channel, etc.) work unchanged

## Usage Examples

### Example 1: YouTube Edit Preset
```
1. Select "YouTube Edit" preset
2. GUI auto-configures: MP4 container, H.264 codec, AAC audio
3. User downloads → Command includes proper FFmpeg args
4. Output: MP4 file suitable for YouTube upload
```

### Example 2: Professional Editing
```
1. Select "Professional Editing" preset
2. GUI auto-configures: MOV container, ProRes codec, PCM WAV audio
3. User downloads → High-quality master file
4. Output: MOV file ready for DaVinci Resolve or Premiere editing
```

### Example 3: Fast Download
```
1. Select "Fast Download" preset
2. GUI auto-configures: MKV container, Copy codec (no re-encoding), Copy audio
3. User downloads → Maximum speed, no quality loss, largest file size
4. Output: MKV with original streams
```

### Example 4: Manual Configuration
```
1. Select individual options:
   - Container: MOV
   - Codec: H265
   - Audio: FLAC
2. Download → Custom configuration with high-quality H.265 video + lossless audio
3. Output: MOV file with H.265 video and FLAC audio
```

### Example 5: Audio-Only SFX Workflow
```
1. Select "SFX PCM Audio" preset
2. Download → Audio-only extraction
3. Output: WAV file at 48kHz 24-bit (professional audio standard)
```

## Generated Command Examples

### Command 1: YouTube Edit Preset
```bash
yt-dlp --ffmpeg-location "C:\...\ffmpeg.exe"
       --no-playlist
       --output "D:\downloads\%(title)s.%(ext)s"
       --format "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"
       --postprocessor-args "-c:v libx264 -preset slow -crf 18 -vn -c:a aac -b:a 320k"
       --merge-output-format mp4
       https://www.youtube.com/watch?v=...
```

### Command 2: Professional Editing (DaVinci)
```bash
yt-dlp --ffmpeg-location "C:\...\ffmpeg.exe"
       --no-playlist
       --output "D:\downloads\%(title)s.%(ext)s"
       --format "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"
       --postprocessor-args "-c:v prores_ks -profile:v 3 -vn -c:a pcm_s24le -ar 48000"
       --merge-output-format mov
       https://www.youtube.com/watch?v=...
```

### Command 3: Fast Download
```bash
yt-dlp --ffmpeg-location "C:\...\ffmpeg.exe"
       --no-playlist
       --output "D:\downloads\%(title)s.%(ext)s"
       --format "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"
       --postprocessor-args "-c copy -vn -c:a copy"
       --merge-output-format mkv
       https://www.youtube.com/watch?v=...
```

### Command 4: Audio-Only SFX
```bash
yt-dlp --ffmpeg-location "C:\...\ffmpeg.exe"
       --no-playlist
       --output "D:\downloads\%(title)s.%(ext)s"
       --format "bestaudio/best"
       --extract-audio
       --audio-format wav
       https://www.youtube.com/watch?v=...
```

## File Structure

```
src/app/
├── __init__.py
├── main_window.py           ← MODIFIED: Added editing UI state + elements
├── download_manager.py      ← MODIFIED: Uses EditingCommandBuilder
├── ui_manager.py            ← MODIFIED: Added editing UI controls
├── command_builder.py       ← NEW: Dynamic command generation
├── editing_config.py        ← NEW: Editing options and presets
├── updater.py
├── login_manager.py
└── assets/
    └── style.qss
```

## Code Quality Notes

1. **Clean Integration**: New modules don't modify core logic
2. **Backward Compatible**: Existing functionality untouched
3. **Type Hints**: All functions have proper type annotations
4. **Documentation**: Comprehensive docstrings and comments
5. **No Hardcoding**: All options configured in `editing_config.py`
6. **Thread-Safe**: Command building happens in main thread, execution in worker thread

## Future Extensions

Possible enhancements:

1. **Custom Codec Args**: Allow users to input FFmpeg args directly
2. **Batch Presets**: Save/load custom preset configurations
3. **Quality Comparison**: Show file size estimates for different codecs
4. **Format Conversion**: Additional container/codec combinations
5. **Subtitle Handling**: Options for subtitle extraction/burning
6. **Thumbnail Extraction**: Download video thumbnails alongside video

## Testing Checklist

- [ ] Preset selection works correctly
- [ ] Container format changes apply to command
- [ ] Video codec selection works
- [ ] Audio export modes generate correct FFmpeg args
- [ ] MP3 extraction still works (backward compatibility)
- [ ] Playlist downloads respect editing settings
- [ ] Channel downloads respect editing settings
- [ ] Progress tracking works with re-encoding
- [ ] All generated commands execute successfully
- [ ] UI state preserves across mode changes

## Support Resources

- **yt-dlp Documentation**: https://github.com/yt-dlp/yt-dlp
- **FFmpeg Documentation**: https://ffmpeg.org/documentation.html
- **Project Repository**: https://github.com/ukr/yt-downloader-gui

---

**Version**: 1.0.0  
**Date**: 2026-03-11  
**Compatibility**: yt-downloader-gui 1.0.0+
