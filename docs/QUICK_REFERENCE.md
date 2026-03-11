# Video Editing Features - Quick Reference & Examples

## Quick Start

### For YouTube Videos
1. Launch yt-downloader-gui
2. Leave editing settings at default (YouTube Edit preset)
3. Download as usual
4. ✓ Optimized for YouTube (1080p-capable, AAC audio)

### For Professional Editing (DaVinci Resolve)
1. Select preset: **"DaVinci Resolve"**
2. GUI automatically configures:
   - Container: MOV
   - Codec: ProRes 422 HQ
   - Audio: WAV 48kHz 24-bit
3. Download
4. ✓ Ready to import into DaVinci Resolve

### For Adobe Premiere
1. Select preset: **"Adobe Premiere"**
2. GUI automatically configures:
   - Container: MP4
   - Codec: H.264
   - Audio: AAC 320kbps
3. Download
4. ✓ Ready to import into Adobe Premiere

### For Sound Effects (SFX) Library
1. Select preset: **"SFX PCM Audio"**
2. Download
3. ✓ Gets WAV file at professional broadcast standard (48kHz 24-bit)

### For Fast Downloads (No Re-encoding)
1. Select preset: **"Fast Download"**
2. GUI sets:
   - Container: MKV
   - Codec: Copy (no re-encoding)
   - Audio: Copy (original format)
3. Download
4. ✓ Fastest download, original quality preserved, larger file

## Container Formats Compared

| Format | Best Use Case | File Size | Compatibility |
|--------|---------------|-----------|---------------|
| **MP4** | Web, YouTube, Premiere | Medium | Universal, all players |
| **MKV** | Archival, multiple streams | Large | Good for editing, less universal |
| **MOV** | Final Cut Pro, DaVinci | Large | Apple/Pro tools |

## Video Codec Comparison

| Codec | Quality | Speed | File Size | Use Case |
|-------|---------|-------|-----------|----------|
| **Copy** | Original | ⚡ Fastest | As-is | Fast download, archival |
| **H264** | High | Medium | Medium | YouTube, web, universal |
| **H265** | Excellent | ✓ Medium | 40-50% smaller | Modern devices, storage |
| **ProRes** | Perfect | Slower | Largest | Professional editing |

*Note: Quality and speed are relative. ProRes encoding can take 1-2x longer than realtime.*

## Audio Format Comparison

| Format | Quality | File Size | Use Case |
|--------|---------|-----------|----------|
| **Copy** | Original | Original | No conversion |
| **WAV** | Lossless | Large (1GB/hour) | Professional audio, SFX |
| **FLAC** | Lossless | Medium (500MB/hour) | Archival, no patents |
| **AAC** | Lossy 320k | Small (50MB/hour) | Web, streaming |

*Note: WAV and FLAC are lossless but very large. AAC is lossy but efficient for web use.*

## All Available Presets

### Content Creation
**YouTube Edit**
- Best for: YouTube video uploads
- Container: MP4 | Codec: H264 | Audio: AAC
- File: ~50-150MB per hour (depends on original quality)

**Professional Editing**
- Best for: Professional editing workflows
- Container: MOV | Codec: ProRes | Audio: WAV
- File: ~1-2GB per hour (preserve maximum quality)

**Fast Download**
- Best for: Quick downloads without re-encoding
- Container: MKV | Codec: Copy | Audio: Copy
- File: Variable (same as original)

### Software-Specific

**DaVinci Resolve**
- Container: MOV | Codec: ProRes | Audio: WAV
- Reason: Native ProRes support, WAV for professional audio

**Adobe Premiere**
- Container: MP4 | Codec: H264 | Audio: AAC
- Reason: Good Adobe compatibility, reasonable file size

**After Effects**
- Container: MOV | Codec: H264 | Audio: AAC
- Reason: QuickTime compatibility, H264 support

**Final Cut Pro**
- Container: MOV | Codec: ProRes | Audio: WAV
- Reason: Native FCP format, optimal performance

### Audio Only (SFX Workflows)

**SFX PCM Audio**
- Format: WAV file, 48kHz 24-bit
- Best for: Sound effects libraries, Foley work
- Quality: Professional broadcast standard
- Note: Very large files (20-30MB per minute)

**SFX FLAC Audio**
- Format: FLAC (lossless compress)
- Best for: Archival, editing workflows
- Quality: Lossless, smaller than WAV
- Size: ~50% of WAV

## Codec Details

### H264 (libx264)
```
FFmpeg args: -c:v libx264 -preset slow -crf 18
- preset slow = higher quality (slower encoding)
- crf 18 = high quality (lower = better, 0-51 range)
```
**Good for**: Modern devices, YouTube, web
**Bad for**: Professional editing (not ideal for re-encoding)

### H265 (libx265)
```
FFmpeg args: -c:v libx265 -crf 20
- crf 20 = high quality
- ~50% smaller files than H264
- Older devices may not support
```
**Good for**: Modern devices only, space-constrained
**Bad for**: Older devices, some codecs less mature

### ProRes (prores_ks)
```
FFmpeg args: -c:v prores_ks -profile:v 3
- profile 3 = ProRes 422 HQ
- Maintains maximum quality
- Large files but no further compression needed
```
**Good for**: Professional editing, broadcast
**Bad for**: Web (no browser support)

## File Size Estimates

### YouTube Edit (H264 AAC)
- 1 hour 1080p video: ~80-150MB
- 1 hour 4K video: ~300-500MB
- Audio only: ~50MB

### Professional (ProRes WAV)
- 1 hour 1080p video: ~600-800MB
- 1 hour 4K video: ~2-3GB
- Audio only: ~600MB (lossless WAV)

### Fast Download (Copy audio/video)
- File size depends on original
- Usually matches or smaller than original

## Manual Configuration Example

Instead of presets, you can pick individual options:

**Example: Custom H265 High-Quality**
1. Container: MKV (supports H265 well)
2. Video Codec: H265 (modern compression)
3. Audio Export: FLAC (lossless, not too large)
4. Download: Get next-gen video format with lossless audio

**Example: Data Hoarder Setup**
1. Container: MKV
2. Video Codec: Copy (no re-encoding)
3. Audio Export: Copy (preserve original audio)
4. Download: Original format preserved, fastest

**Example: Portable Editing Setup**
1. Container: MP4
2. Video Codec: H264
3. Audio Export: AAC
4. Download: Universal format, smaller files, works everywhere

## Troubleshooting

### "Failed to encode video"
**Cause**: Video codec not available in FFmpeg
**Solution**: Install ffmpeg with full codec support

### Huge file sizes
**Cause**: Using ProRes or WAV output
**Expected**: ProRes and WAV are designed for professional quality, not compression
**Solution**: Use H264/AAC for web, or accept large files for professional work

### Downloaded file won't open
**Cause**: Container/codec mismatch for your software
**Solution**: Check software documentation for supported formats

### Video plays but no audio
**Cause**: Container doesn't properly support audio codec
**Solution**: Use MP4 or MOV (more stable than MKV for audio)

### Very slow download
**Cause**: Using ProRes (real-time or slower encoding)
**Expected**: Professional codecs are slower
**Solution**: Use "H264" or "Copy" for faster downloads

## Preset Recommendations by Use Case

### Scenario 1: "I'm uploading to YouTube"
→ Use **"YouTube Edit"** preset

### Scenario 2: "I'm editing in DaVinci Resolve"
→ Use **"DaVinci Resolve"** preset

### Scenario 3: "I'm editing in Premiere Pro"
→ Use **"Adobe Premiere"** preset

### Scenario 4: "I need the highest quality for editing"
→ Use **"Professional Editing"** preset

### Scenario 5: "I just want a quick download"
→ Use **"Fast Download"** preset

### Scenario 6: "I need audio for my SFX library"
→ Use **"SFX PCM Audio"** preset

### Scenario 7: "I don't know what to use"
→ Use default **"YouTube Edit"** preset (safest choice)

## Advanced Usage

### Command Line Inspection
To see the exact yt-dlp command being run, check the Activity tab during download. The command will be logged.

### Batch Downloads with Same Settings
1. Set your desired preset/settings
2. Add multiple videos to queue
3. All will use the same settings
4. They download sequentially

### Changing Settings Mid-Download
⚠️ **Warning**: Changes apply only to future downloads in queue, not the current one

### Custom Extensions
Edit `src/app/editing_config.py` to:
- Add new presets
- Modify codec arguments
- Add new containers
- Change descriptions

## FFmpeg Tips

### Checking Your FFmpeg Installation
```bash
ffmpeg -codecs | findstr "prores"      # Check for ProRes support
ffmpeg -codecs | findstr "h264"        # Check for H264 support
ffmpeg -codecs | findstr "hevc"        # Check for H265 support
ffmpeg -encoders                       # List all encoders
```

### Quality Settings
- **CRF (Constant Rate Factor)**: 0-51 (lower = better quality)
- **Preset**: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
- **Profile**: h264 uses different profiles, ProRes uses profiles 0-4

---

**Last Updated**: 2026-03-11  
**Version**: 1.0.0  
**Maintained by**: yt-downloader-gui Team
