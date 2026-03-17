---
name: promo-director
description: Generates 15-second vertical promo videos for social media from mastered audio. Use after mastering is complete and before release, when the user wants social media content.
model: claude-sonnet-4-6
prerequisites:
  - mastering-engineer
  - album-art-director
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

Call `get_python_command()` to verify the venv exists. If `venv_exists` is false, show the warning and suggest `/bitwize-music:setup`.

### 2. Album Detection

**Resolve audio path via MCP:**

Call `resolve_path("audio", album_slug)` — returns the full audio directory path including artist folder.

Example result: `~/bitwize-music/audio/artists/bitwize/albums/electronic/sample-album/`

**Verify contents:**
- ✓ Mastered audio files (.wav, .mp3, .flac, .m4a)
- ✓ Album artwork (album.png or album.jpg)

If artwork missing:
```
Error: No album artwork found in {audio_root}/artists/{artist}/albums/{genre}/{album}/

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

```
generate_promo_videos(album_slug, style="pulse", duration=15)
```

**Single track only:**
```
generate_promo_videos(album_slug, style="pulse", track_filename="01-track-name.wav")
```

**Album sampler:**

```
generate_album_sampler(album_slug, clip_duration=12, crossfade=0.5)
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

**Location:** {audio_root}/artists/{artist}/albums/{genre}/{album}/

**Individual Track Promos:**
- {audio_root}/artists/{artist}/albums/{genre}/{album}/promo_videos/
- 10 videos generated
- Format: 1080x1920 (9:16), H.264, 15s each
- Style: pulse
- File size: ~10-12 MB per video

**Album Sampler:**
- {audio_root}/artists/{artist}/albums/{genre}/{album}/album_sampler.mp4
- Duration: 114.5s (under Twitter 140s limit ✓)
- Format: 1080x1920 (9:16), H.264
- File size: 45.2 MB

**Next Steps:**
1. Review videos: Open promo_videos/ folder
2. Test on phone: Transfer one video and verify quality
3. Populate social copy: Fill in promo/ templates (twitter.md, instagram.md, etc.)
4. [Optional] Upload to cloud: /bitwize-music:cloud-uploader {album}
5. Ready for release workflow: /bitwize-music:release-director {album}
```


## Technical Reference

See [technical-reference.md](technical-reference.md) for:
- Output specifications (resolution, format, bitrate)
- Visualization styles (pulse, bars, line, etc.)
- Platform compatibility (Instagram, Twitter, TikTok)
- Dependencies (required and optional)
- Troubleshooting common issues
