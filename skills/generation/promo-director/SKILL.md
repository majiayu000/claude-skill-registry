---
name: promo-director
description: Generate promo videos for social media from mastered audio
model: claude-sonnet-4-5-20250929
allowed-tools:
  - Read
  - Bash
  - Glob
requirements:
  external:
    - name: ffmpeg
      purpose: Video generation and audio visualization
      install: "brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
      notes: "Requires showwaves, showfreqs, drawtext, gblur filters"
  python:
    - pillow
    - librosa
    - pyyaml
---

# Promo Director Skill

Generate professional promo videos for social media from mastered audio. Creates 15-second vertical videos (9:16, 1080x1920) optimized for Instagram Reels, Twitter, and TikTok.

## Purpose

After mastering audio, generate promotional videos that combine:
- Album artwork
- Audio waveform visualization (9 styles available)
- Track title + artist name
- Automatic color scheme extracted from artwork
- Intelligent segment selection (finds the most energetic 15 seconds)

## When to Use

- After mastering complete, before release
- User says "generate promo videos" or "create promo videos for [album]"
- When album has mastered audio + artwork ready

## Position in Workflow

```
Generate → Master → **[Promo Videos]** → Release
```

Optional step between mastering-engineer and release-director.

## Workflow

### 1. Setup Verification

**Check ffmpeg:**
```bash
ffmpeg -filters | grep showwaves
```

Required filters: `showwaves`, `showfreqs`, `drawtext`, `gblur`

If missing:
```
Error: ffmpeg not found or missing required filters

Install ffmpeg:
  macOS: brew install ffmpeg
  Linux: apt install ffmpeg

After installing, run this command again.
```

**Check Python dependencies:**
```bash
python3 -c "import PIL, yaml"
```

Optional (for smart segment detection):
```bash
python3 -c "import librosa, numpy"
```

If missing:
```
Python dependencies missing. Create venv?

  mkdir -p ~/.bitwize-music/promotion-env
  python3 -m venv ~/.bitwize-music/promotion-env
  source ~/.bitwize-music/promotion-env/bin/activate
  pip install pillow pyyaml librosa numpy

Which option:
  1. I'll install manually (show commands above)
  2. Create venv automatically
```

### 2. Album Detection

**Read config:**
```python
import yaml
from pathlib import Path

config_path = Path.home() / ".bitwize-music" / "config.yaml"
config = yaml.safe_load(open(config_path))

audio_root = Path(config['paths']['audio_root']).expanduser()
artist = config['artist']['name']
```

**Locate album:**
```
Album path: {audio_root}/{artist}/{album_name}/
```

**Verify contents:**
- ✓ Mastered audio files (.wav, .mp3, .flac, .m4a)
- ✓ Album artwork (album.png or album.jpg)

If artwork missing:
```
Error: No album artwork found in {audio_root}/{artist}/{album}/

Expected: album.png or album.jpg

Options:
  1. Use /bitwize-music:import-art to place artwork
  2. Specify path manually: --artwork /path/to/art.png

Which option?
```

### 3. User Preferences

**Check config defaults first:**

Read `promotion` section from `~/.bitwize-music/config.yaml` for defaults:
- `promotion.default_style` - Default visualization style
- `promotion.duration` - Default clip duration
- `promotion.include_sampler` - Whether to generate album sampler by default
- `promotion.sampler_clip_duration` - Seconds per track in sampler

If config section doesn't exist, use built-in defaults (pulse, 15s, sampler enabled, 12s clips).

**Ask: What to generate?**

Options (default from config or "both"):
1. Individual track promos (15s each) + Album sampler (all tracks)
2. Individual track promos only
3. Album sampler only

**Ask: Visualization style?**

Default from `promotion.default_style` or `pulse` if not set.

| Style | Best For | Description |
|-------|----------|-------------|
| `pulse` | Electronic, hip-hop | Oscilloscope/EKG style with heavy glow (default) |
| `bars` | Pop, rock | Fast reactive spectrum bars |
| `line` | Acoustic, folk | Classic clean waveform |
| `mirror` | Ambient, chill | Mirrored waveform with symmetry |
| `mountains` | EDM, bass-heavy | Dual-channel spectrum (looks like mountains) |
| `colorwave` | Indie, alternative | Clean waveform with subtle glow |
| `neon` | Synthwave, 80s | Sharp waveform with punchy neon glow |
| `dual` | Experimental | Two separate waveforms (dominant + complementary colors) |
| `circular` | Abstract, experimental | Vectorscope (wild circular patterns) |

**Default recommendation:**
- Electronic/Hip-Hop → `pulse`
- Rock/Pop → `bars`
- Folk/Acoustic → `line`
- Ambient/Chill → `mirror`

**Ask: Custom duration?**

Default: 15 seconds (optimal for Instagram/Twitter)

Options:
- 15s (recommended, Instagram Reels sweet spot)
- 30s (longer preview)
- 60s (full clip, less common)

**For sampler:**

Default: 12 seconds per track

Calculate total:
```
Total duration = (tracks * clip_duration) - ((tracks - 1) * crossfade)
Twitter limit: 140 seconds
```

If over 140s:
```
WARNING: Expected duration {duration}s exceeds Twitter limit (140s)

Recommendation: Reduce --clip-duration to {140 / tracks}s
```

### 4. Generation

**Individual track promos:**

Run from plugin directory:
```bash
cd {plugin_root}
python3 tools/promotion/generate_promo_video.py \
  --batch {audio_root}/{artist}/{album}/ \
  --style pulse \
  -o {audio_root}/{artist}/{album}/promo_videos/
```

Progress:
```
Found 10 tracks
  Analyzing audio for most energetic segment...
  Found energetic segment at 45.2s
  Extracting colors from artwork...
  Dominant: (42, 187, 255) -> Complementary: (255, 170, 42) (hex: 0xffaa2a)
Generating: 01-track_promo.mp4
  ✓ 01-track_promo.mp4
Generating: 02-track_promo.mp4
  ✓ 02-track_promo.mp4
...
```

**Album sampler:**

Run from plugin directory:
```bash
cd {plugin_root}
python3 tools/promotion/generate_album_sampler.py \
  {audio_root}/{artist}/{album}/ \
  --artwork {audio_root}/{artist}/{album}/album.png \
  --clip-duration 12 \
  -o {audio_root}/{artist}/{album}/album_sampler.mp4
```

Progress:
```
Album Sampler Generator
=======================
Tracks: 10
Clip duration: 12s
Crossfade: 0.5s
Expected duration: 114.5s
Twitter limit: 140s

Found 10 tracks
Extracting colors from artwork...
  Using color: 0xffaa2a
[1/10] Track Name...
  OK
[2/10] Another Track...
  OK
...
Concatenating 10 clips with 0.5s crossfades...

Created: {audio_root}/{artist}/{album}/album_sampler.mp4
  Duration: 114.5s
  Size: 45.2 MB
```

**Handle errors:**

Common issues:
- **ffmpeg filter error** → Check ffmpeg install includes filters
- **Font not found** → Install dejavu fonts or specify custom font
- **Artwork extraction fails** → Use default cyan color scheme
- **librosa unavailable** → Fall back to 20% into track for segment selection
- **Audio file corrupt** → Skip track, report, continue with others

### 5. Results Summary

**Report generated files:**

```
## Promo Videos Generated

**Location:** {audio_root}/{artist}/{album}/

**Individual Track Promos:**
- {audio_root}/{artist}/{album}/promo_videos/
- 10 videos generated
- Format: 1080x1920 (9:16), H.264, 15s each
- Style: pulse
- File size: ~10-12 MB per video

**Album Sampler:**
- {audio_root}/{artist}/{album}/album_sampler.mp4
- Duration: 114.5s (under Twitter 140s limit ✓)
- Format: 1080x1920 (9:16), H.264
- File size: 45.2 MB

**Next Steps:**
1. Review videos: Open promo_videos/ folder
2. Test on phone: Transfer one video and verify quality
3. [Optional] Upload to cloud: /bitwize-music:cloud-uploader {album}
4. Ready for release workflow: /bitwize-music:release-director {album}
```

## Technical Details

### Output Specifications

**Format:**
- Resolution: 1080x1920 (9:16 vertical)
- Codec: H.264 (libx264)
- Audio: AAC, 192 kbps
- Pixel format: yuv420p (universal compatibility)
- Frame rate: 30 fps

**File sizes:**
- Individual promo (15s): ~10-12 MB
- Album sampler (10 tracks, 115s): ~45-50 MB

### Visualization Styles

**Implementation:**

All styles use ffmpeg filter chains:
- `showwaves` - Time-domain waveform
- `showfreqs` - Frequency spectrum
- `avectorscope` - Phase correlation (circular)
- `gblur` - Gaussian blur for glow effects
- `blend` - Layer blending for multi-layer glows

**Color extraction:**

Uses PIL to extract dominant color from album artwork:
1. Resize to 100x100 for speed
2. Filter out very dark/light pixels
3. Quantize color space (32 levels per channel)
4. Pick most saturated of top 5 colors
5. Generate complementary color (rotate 180° on hue wheel)
6. Use for waveform visualization

**Segment selection:**

With librosa (recommended):
1. Load audio (mono, 22050 Hz)
2. Compute RMS energy over time
3. Find 15s window with highest average energy
4. Usually captures chorus or drop

Without librosa (fallback):
- Start at 20% into track (skips intro, gets to meat)

### Platform Compatibility

**Instagram Reels:**
- ✓ 1080x1920 (9:16)
- ✓ Max 90s (our 15s clips fit easily)
- ✓ H.264 codec

**Twitter:**
- ✓ 1080x1920 (9:16)
- ✓ Max 2:20 (140s)
- ✓ File size < 512 MB (our files ~10-50 MB)

**TikTok:**
- ✓ 1080x1920 (9:16)
- ✓ 15-60s (our 15s clips optimal)
- ✓ H.264 codec

**Facebook:**
- ✓ 1080x1920 (9:16)
- ✓ Various durations accepted
- ✓ H.264 codec

## Dependencies

### Required

**ffmpeg:**
- Version: 4.0+
- Filters: showwaves, showfreqs, drawtext, gblur
- Install: `brew install ffmpeg` (macOS), `apt install ffmpeg` (Linux)

**Python 3.8+**

**Python packages:**
- `pillow` - Image processing (color extraction)
- `pyyaml` - Config file reading

### Optional

**Python packages:**
- `librosa` - Audio analysis (intelligent segment selection)
- `numpy` - Required by librosa

**Graceful degradation:**
- If PIL unavailable → Use default cyan color scheme
- If librosa unavailable → Use 20% into track as start point
- If custom font unavailable → Use system default

## Invocation Examples

**Basic (everything):**
```
/bitwize-music:promo-director my-album
```

**Tracks only:**
```
/bitwize-music:promo-director my-album --tracks-only
```

**Sampler only:**
```
/bitwize-music:promo-director my-album --sampler-only
```

**Custom style:**
```
/bitwize-music:promo-director my-album --style neon
```

**Custom duration:**
```
/bitwize-music:promo-director my-album --duration 30
```

## Integration with Other Skills

### Handoff FROM

**mastering-engineer:**

After mastering complete:
```
## Mastering Complete

**Next Steps:**
1. [Optional] Generate promo videos: /bitwize-music:promo-director my-album
2. Begin release workflow: /bitwize-music:release-director my-album
```

### Handoff TO

**release-director:**

After promo generation:
```
Promo videos generated successfully.

**Optional:** Upload to cloud storage: /bitwize-music:cloud-uploader my-album

Ready for release workflow: /bitwize-music:release-director my-album
```

## Future Enhancements

**Not in initial port (defer to future versions):**

- Twitter campaign automation (tweet generation, scheduling)
- n8n workflow integration
- Automatic platform uploads (Instagram, Twitter APIs)
- Analytics tracking (view counts, engagement)
- Custom branding overlays (logos, watermarks)
- Platform-specific optimizations (1:1 for Twitter, 16:9 for YouTube)
- Batch processing multiple albums
- Template system for recurring visual styles

## Troubleshooting

**"ffmpeg not found"**
- Install: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)
- Verify: `ffmpeg -version`

**"showwaves filter not found"**
- ffmpeg compiled without filter support
- Reinstall with full filters: `brew reinstall ffmpeg --with-all`

**"Font not found"**
- Install dejavu fonts: `apt install fonts-dejavu` (Linux)
- macOS: System fonts should work automatically
- Override with: `--font-path /path/to/font.ttf`

**"Color extraction failed"**
- Activate venv: `source ~/.bitwize-music/promotion-env/bin/activate`
- Install PIL in venv: `pip install pillow`
- Or accept default cyan color scheme (still works)

**"librosa not found" (warning, not error)**
- Activate venv: `source ~/.bitwize-music/promotion-env/bin/activate`
- Install in venv: `pip install librosa numpy`
- Or continue with fallback (20% into track)
- Quality still good, just less intelligent segment selection

**Videos generated but won't play**
- Check codec: Should be H.264, not HEVC
- Check pixel format: Should be yuv420p
- Re-encode if needed: `ffmpeg -i bad.mp4 -c:v libx264 -pix_fmt yuv420p fixed.mp4`

**File sizes too large**
- Normal: 10-12 MB per 15s video
- If much larger: Check artwork resolution (should be ≤3000px)
- Reduce artwork size: `convert album.png -resize 3000x3000\> album.png`

**"Expected duration exceeds Twitter limit"**
- For samplers with many tracks
- Solution: Reduce --clip-duration to fit 140s limit
- Example: 15 tracks → 140/15 = ~9s per track

## Model Recommendation

**Sonnet 4.5** - This skill coordinates workflow and runs scripts. Creative output is in the videos themselves (generated by ffmpeg), not by the LLM.

## Version History

- v0.12.0 - Initial implementation (ported from ../music/tools/promotion/)
  - Individual track promos
  - Album sampler generation
  - 9 visualization styles
  - Config integration
  - Automatic color extraction
  - Intelligent segment selection
