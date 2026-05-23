---
name: autocut-shorts
description: Main orchestration skill for automatic creation of short-form content (TikTok, YouTube Shorts, Instagram Reels) from long videos. Fully automated workflow: download video, transcribe, detect highlights (transcript + laughter + sentiment + scenes), trim segments, resize to 9:16 portrait, and add subtitles. Finds viral-worthy moments like OpusClip and Vizard.ai.
allowed-tools: Bash(ffmpeg:*) Bash(yt-dlp:*) Bash(python:*)
compatibility: Requires all trimer-clip dependencies and FFmpeg
metadata:
  version: "1.0"
  platforms: "TikTok, YouTube Shorts, Instagram Reels, Facebook Reels"
---

# Autocut Shorts

This is the main orchestration skill that combines all other skills to automatically create short-form content from long videos.

## What It Does

This skill automates the entire workflow:

1. **Download** video from YouTube URL (if provided)
2. **Transcribe** audio using Whisper or Gemini API
3. **Perform speaker diarization** (pyannote or Gemini) - identifies who speaks when
4. **Detect highlights** using combined analysis:
   - Transcript analysis (hooks, viral phrases)
   - Speaker dynamics (debates, interactions, overlapping speech)
   - Laughter detection (humorous moments)
   - Sentiment analysis (emotional peaks)
   - Scene detection (cut points)
5. **Select** best segments (15-60 seconds each)
6. **Trim** video to highlight segments
7. **Resize** to 9:16 portrait format (1080x1920)
8. **Add** burned-in subtitles with speaker labels
9. **Export** multiple clips ready for upload

## When to Use

- User wants to create TikTok clips from a YouTube video
- Converting podcasts to short-form content
- Finding viral moments in vlogs or tutorials
- Repurposing gaming content for Shorts/Reels
- Batch processing multiple videos

## Available Scripts

### `scripts/autocut.py`

Main autocut workflow script.

**Usage:**
```bash
python skills/autocut-shorts/scripts/autocut.py <video_or_url> [options]
```

**Options:**
- `--source`: Source type (file, youtube) - auto-detected
- `--num-clips`: Number of clips to generate (default: 5)
- `--min-duration`: Minimum clip duration in seconds (default: 15)
- `--max-duration`: Maximum clip duration in seconds (default: 60)
- `--platform`: Target platform (tiktok, shorts, reels, facebook) - default: tiktok
- `--output-dir`: Output directory (default: `./shorts/`)
- `--transcription-model`: Transcription model (auto, whisper, gemini) - default: auto
- `--diarization-model`: Speaker diarization (auto, pyannote, gemini, none) - default: auto
- `--huggingface-token`: HuggingFace token for pyannote (or use env var)
- `--focus-speaker`: Extract clips only for specific speaker (SPEAKER_00, etc.)
- `--gemini-api-key`: Gemini API key (or use env var)
- `--skip-transcribe`: Skip transcription if already have transcript
- `--skip-diarization`: Skip speaker diarization
- `--skip-scenes`: Skip scene detection
- `--skip-laughter`: Skip laughter detection
- `--skip-sentiment`: Skip sentiment analysis
- `--transcript-path`: Use existing transcript file
- `--style`: Subtitle style (tiktok, shorts, reels) - default: tiktok

**Examples:**

Basic autocut from file:
```bash
python skills/autocut-shorts/scripts/autocut.py video.mp4
```

Autocut from YouTube URL:
```bash
python skills/autocut-shorts/scripts/autocut.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Generate 10 clips for Instagram Reels:
```bash
python skills/autocut-shorts/scripts/autocut.py video.mp4 --num-clips 10 --platform reels --style reels
```

Use Gemini for transcription:
```bash
python skills/autocut-shorts/scripts/autocut.py video.mp4 --transcription-model gemini
```

Custom duration range:
```bash
python skills/autocut-shorts/scripts/autocut.py video.mp4 --min-duration 20 --max-duration 45
```

Use existing transcript:
```bash
python skills/autocut-shorts/scripts/autocut.py video.mp4 --transcript-path video.srt --skip-transcribe
```

### `scripts/quick_cut.py`

Quick cut without full analysis (faster).

**Usage:**
```bash
python skills/autocut-shorts/scripts/quick_cut.py <video_path> [options]
```

**Options:**
- `--timestamps`: JSON file with timestamps to cut
- `--output-dir`: Output directory
- `--platform`: Target platform

**Example:**
```bash
python skills/autocut-shorts/scripts/quick_cut.py video.mp4 --timestamps cuts.json
```

## Workflow Steps

### Step 1: Download (Optional)

If URL provided:
- Downloads from YouTube using yt-dlp
- Best quality MP4
- Saves to temp directory

### Step 2: Transcribe

Extracts audio and transcribes:
- **Auto mode**: Chooses based on requirements
- **Whisper**: Local processing, good for privacy
- **Gemini**: Cloud processing, better quality + features

### Step 3: Detect Highlights

Runs detection modules:
- **Transcript analysis**: Viral phrases, hooks, questions
- **Laughter detection**: Funny moments (if enabled)
- **Sentiment analysis**: Emotional peaks (if enabled)
- **Scene detection**: Visual cut points (if enabled)

### Step 4: Score and Rank

Combines all signals:
```
Virality Score = 
  35% Transcript (hooks, viral content) +
  25% Laughter (humor) +
  25% Sentiment (emotion) +
  15% Scenes (visual transitions)
```

Ranks all segments and selects top N.

### Step 5: Trim

For each highlight:
- Extends 2-3 seconds before/after for context
- Trims using FFmpeg (stream copy for speed)
- Validates duration constraints

### Step 6: Resize to Portrait

Converts to 9:16:
- Smart crop (focus on subjects)
- 1080x1920 resolution
- Maintains quality

### Step 7: Add Subtitles

Burns in captions:
- Platform-specific styling
- White text with black outline
- Bottom position
- Readable size (24-28px)

### Step 8: Export

Saves final clips:
- Named: `{original}_short_{index}.mp4`
- Organized in output directory
- JSON report with metadata

## Output Format

### Directory Structure
```
shorts/
  video_short_001.mp4
  video_short_002.mp4
  video_short_003.mp4
  report.json
```

### JSON Report

```json
{
  "success": true,
  "source": {
    "type": "youtube",
    "url": "https://youtube.com/watch?v=...",
    "title": "Video Title",
    "duration": 1200.5
  },
  "processing": {
    "transcription_model": "gemini-flash-lite-latest",
    "detection_methods": ["transcript", "laughter", "sentiment", "scenes"],
    "platform": "tiktok"
  },
  "results": {
    "total_clips": 5,
    "clips": [
      {
        "rank": 1,
        "filename": "video_short_001.mp4",
        "start_time": 45.2,
        "end_time": 72.5,
        "duration": 27.3,
        "virality_score": 0.92,
        "text": "This is the key moment...",
        "output_path": "shorts/video_short_001.mp4"
      }
    ],
    "total_duration": 135.5,
    "avg_virality_score": 0.78
  },
  "performance": {
    "total_time": 180.5,
    "transcription_time": 45.2,
    "analysis_time": 67.3,
    "processing_time": 68.0
  }
}
```

## Platform Presets

### TikTok
- Resolution: 1080x1920
- Duration: 15-60 seconds
- Subtitle style: TikTok
- Output naming: `_tiktok_{index}.mp4`

### YouTube Shorts
- Resolution: 1080x1920
- Duration: 15-60 seconds
- Subtitle style: Shorts
- Output naming: `_shorts_{index}.mp4`

### Instagram Reels
- Resolution: 1080x1920
- Duration: 15-90 seconds
- Subtitle style: Reels
- Output naming: `_reels_{index}.mp4`

### Facebook Reels
- Resolution: 1080x1920
- Duration: 15-90 seconds
- Subtitle style: Default
- Output naming: `_facebook_{index}.mp4`

## Viral Detection Algorithm

### High-Value Signals

**Transcript (35% weight):**
- Viral phrases ("you won't believe", "this changes everything")
- Hooks ("let me tell you", "here's the secret")
- Questions and answers
- Story beats

**Laughter (25% weight):**
- Explicit laughter markers
- High-confidence laughter detection
- Audience reactions

**Sentiment (25% weight):**
- Positive emotions (excitement, joy)
- Surprise moments
- Negative emotions (controversy, drama)
- Emotional intensity > 0.7

**Scenes (15% weight):**
- Scene transitions
- Visual changes
- Topic shifts

### Scoring

```python
virality_score = (
    transcript_score * 0.35 +
    laughter_score * 0.25 +
    sentiment_score * 0.25 +
    scene_score * 0.15
)
```

**Premium Clips (0.8-1.0):** Must include
**Excellent Clips (0.6-0.8):** High priority
**Good Clips (0.4-0.6):** Consider including

## AI Agent Decision Guide

### When to Use pyannote vs Gemini Diarization

**Default Behavior (--diarization-model auto):**
The AI agent automatically selects based on context:

```python
# Use pyannote when:
if "podcast" in user_request or "interview" in user_request:
    return "pyannote"  # Multi-speaker, needs accuracy
if "accurate" in user_request or "precise" in user_request:
    return "pyannote"  # User explicitly wants accuracy
if "panel" in user_request or "debate" in user_request:
    return "pyannote"  # Complex multi-speaker scenarios
if "overlapping" in user_request or "talk over" in user_request:
    return "pyannote"  # Overlapping speech detection
if "privacy" in user_request or "offline" in user_request:
    return "pyannote"  # Local processing needed

# Use Gemini when:
if "quick" in user_request or "fast" in user_request:
    return "gemini"  # Speed priority
if "single speaker" in user_request or "monologue" in user_request:
    return "gemini"  # Simple scenario
if "no diarization" in user_request or "skip speakers" in user_request:
    return "none"  # User doesn't want speaker detection

# Default for ambiguous cases:
return "pyannote" if likely_multi_speaker(video) else "gemini"
```

**Decision Matrix:**

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Podcast with 2-3 hosts | **pyannote** | High accuracy for multi-speaker |
| Interview (host + guest) | **pyannote** | Precise speaker separation |
| Panel discussion | **pyannote** | Handles 4+ speakers well |
| Single speaker vlog | **gemini** | Faster, good enough |
| Gaming commentary | **gemini** | Usually 1-2 speakers |
| Tutorial video | **gemini** | Single speaker, speed matters |
| Debate/competitive | **pyannote** | Overlapping speech detection |
| Privacy-sensitive | **pyannote** | Local processing |

**Examples by Use Case:**

```bash
# Podcast - use pyannote automatically
python skills/autocut-shorts/scripts/autocut.py podcast.mp4

# Interview - use pyannote for accuracy
python skills/autocut-shorts/scripts/autocut.py interview.mp4

# Vlog - use gemini (single speaker, faster)
python skills/autocut-shorts/scripts/autocut.py vlog.mp4

# Force pyannote explicitly
python skills/autocut-shorts/scripts/autocut.py video.mp4 --diarization-model pyannote

# Skip diarization for simple content
python skills/autocut-shorts/scripts/autocut.py tutorial.mp4 --diarization-model none

# Extract only host's segments
python skills/autocut-shorts/scripts/autocut.py podcast.mp4 --focus-speaker SPEAKER_00
```

### Smart Defaults

**The agent automatically detects:**
1. Content type (podcast, vlog, tutorial, gaming, etc.)
2. Likely speaker count based on audio patterns
3. User priority (speed vs accuracy vs privacy)
4. Available resources (GPU, internet, API keys)

**Override any time:**
Users can always override with `--diarization-model` flag.

## Integration

This skill uses all other skills:
- `youtube-downloader`: Download from URL
- `video-transcriber`: Transcribe audio
- `scene-detector`: Find visual cut points
- `laughter-detector`: Find funny moments
- `sentiment-analyzer`: Find emotional peaks
- `highlight-scanner`: Combine all signals
- `video-trimmer`: Cut segments
- `portrait-resizer`: Convert to 9:16
- `subtitle-overlay`: Add captions

## Common Use Cases

### Podcast to Shorts
```bash
python skills/autocut-shorts/scripts/autocut.py podcast.mp4 --num-clips 10 --platform shorts
```

### Vlog Highlights
```bash
python skills/autocut-shorts/scripts/autocut.py vlog.mp4 --num-clips 5 --platform tiktok
```

### YouTube to TikTok
```bash
python skills/autocut-shorts/scripts/autocut.py "https://youtube.com/watch?v=..." --platform tiktok
```

### Tutorial Clips
```bash
python skills/autocut-shorts/scripts/autocut.py tutorial.mp4 --min-duration 30 --max-duration 60
```

## Performance

**Processing Time (approximate):**

- 1-minute video: ~30-60 seconds
- 10-minute video: ~3-5 minutes
- 30-minute video: ~8-12 minutes
- 1-hour video: ~15-25 minutes

**Breakdown:**
- Download: 5-30 seconds (depends on video)
- Transcription: 20-60 seconds
- Detection: 10-30 seconds per method
- Trimming: 1-5 seconds per clip
- Resizing: 5-10 seconds per clip
- Subtitles: 5-10 seconds per clip

## Error Handling

- **Download failure**: Retries up to 3 times
- **Transcription failure**: Falls back to alternative model
- **No highlights found**: Returns error with suggestions
- **Processing failure**: Reports which step failed
- **Partial success**: Reports successful clips vs failed

## Tips

- Use Gemini transcription for best highlight detection
- Provide more clips requested than needed (filter by score)
- 15-30 second clips perform best on TikTok
- 30-60 second clips work well for Shorts/Reels
- Keep 2-3 second buffer around highlights
- Test different platforms for best engagement
- Use transcript-only mode for faster processing
- Batch process multiple videos for efficiency

## References

- OpusClip: https://www.opus.pro/
- Vizard.ai: https://vizard.ai/
- TikTok specs: https://www.tiktok.com/business/en-US/solutions/tiktok-specs
- YouTube Shorts specs: https://support.google.com/youtube/answer/10059066
- Instagram Reels specs: https://help.instagram.com/609412256345459
