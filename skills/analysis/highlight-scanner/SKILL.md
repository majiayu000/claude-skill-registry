---
name: highlight-scanner
description: Combined analysis skill to find viral-worthy highlights from videos. Scans transcripts, detects laughter, analyzes sentiment/emotion, and uses scene changes to identify the most engaging moments for TikTok/Shorts/Reels. Produces ranked list of highlight segments with virality scores.
allowed-tools: Bash(ffmpeg:*) Bash(python:*)
compatibility: Requires other trimer-clip skills and dependencies
metadata:
  version: "1.0"
  methods: "Combined Analysis (Transcript + Laughter + Sentiment + Scenes)"
---

# Highlight Scanner

This skill combines all detection methods to find viral-worthy highlights from videos. It's the core analysis component for the autocut-shorts workflow.

## When to Use

- User wants to find the best moments from a video
- Identifying viral-worthy segments for short-form content
- Creating highlight reels from long videos
- Analyzing podcast, vlog, gaming, or tutorial content
- Preparing content for autocut workflow

## Detection Signals

### 1. Transcript Analysis
- Identifies hooks and attention-grabbing phrases
- Detects story beats and important points
- Finds question/answer patterns
- Keyword matching for viral phrases

### 2. Laughter Detection
- Finds humorous moments
- Detects audience reactions
- Identifies funny segments

### 3. Sentiment/Emotion Analysis
- Positive emotions (excitement, joy)
- Surprise moments
- Negative emotions (controversy, drama)
- Emotional peaks and intensity

### 4. Scene Detection
- Scene changes as natural cut points
- Topic transitions
- Visual changes

## Scoring System

Each highlight is scored based on:

```python
virality_score = (
    transcript_score * 0.35 +
    laughter_score * 0.25 +
    sentiment_score * 0.25 +
    scene_score * 0.15
)
```

**Score Range:** 0.0 - 1.0

- **0.8 - 1.0**: Premium viral potential (must use)
- **0.6 - 0.8**: High potential (excellent clips)
- **0.4 - 0.6**: Good potential (consider using)
- **0.2 - 0.4**: Moderate potential (optional)
- **0.0 - 0.2**: Low potential (skip)

## Available Scripts

### `scripts/find_highlights.py`

Find viral-worthy highlight segments.

**Usage:**
```bash
python skills/highlight-scanner/scripts/find_highlights.py <video_path> [options]
```

**Options:**
- `--transcript-path`: Path to transcript SRT/VTT file
- `--scenes-path`: Path to scenes JSON file (from scene-detector)
- `--laughter-path`: Path to laughter JSON file (from laughter-detector)
- `--sentiment-path`: Path to sentiment JSON file (from sentiment-analyzer)
- `--num-clips`: Number of clips to generate - default: 5
- `--min-duration`: Minimum clip duration (seconds) - default: 15
- `--max-duration`: Maximum clip duration (seconds) - default: 60
- `--output, -o`: Output JSON path (default: `<video_path>_highlights.json`)

**Examples:**

Find highlights with transcript only:
```bash
python skills/highlight-scanner/scripts/find_highlights.py video.mp4 --transcript-path video.srt
```

Full analysis with all signals:
```bash
python skills/highlight-scanner/scripts/find_highlights.py video.mp4 \
  --transcript-path video.srt \
  --scenes-path video_scenes.json \
  --laughter-path video_laughter.json \
  --sentiment-path video_sentiment.json
```

Find 10 clips with custom duration:
```bash
python skills/highlight-scanner/scripts/find_highlights.py video.mp4 \
  --transcript-path video.srt \
  --num-clips 10 \
  --min-duration 20 \
  --max-duration 45
```

### `scripts/analyze_viral_potential.py`

Analyze the viral potential of video segments.

**Usage:**
```bash
python skills/highlight-scanner/scripts/analyze_viral_potential.py <video_path> [options]
```

**Options:**
- `--transcript-path`: Path to transcript file
- `--output, -o`: Output JSON path

**Example:**
```bash
python skills/highlight-scanner/scripts/analyze_viral_potential.py video.mp4 --transcript-path video.srt
```

## Output Format

```json
{
  "video_path": "video.mp4",
  "total_segments_analyzed": 15,
  "highlights": [
    {
      "rank": 1,
      "start_time": 45.2,
      "end_time": 72.5,
      "duration": 27.3,
      "virality_score": 0.92,
      "scores": {
        "transcript": 0.95,
        "laughter": 0.80,
        "sentiment": 0.85,
        "scenes": 0.70
      },
      "text": "This is the key moment text...",
      "reasoning": "Contains hook + laughter + positive emotion",
      "suggested_clip_start": 42.0,
      "suggested_clip_end": 75.0,
      "confidence": "high"
    }
  ],
  "analysis_summary": {
    "total_duration": 120.5,
    "avg_virality_score": 0.68,
    "best_segment_start": 45.2,
    "recommended_num_clips": 5
  }
}
```

## Scoring Weights

Default weights (customizable):

```python
DEFAULT_WEIGHTS = {
    'transcript': 0.35,   # Content analysis
    'laughter': 0.25,     # Humor detection
    'sentiment': 0.25,    # Emotion analysis
    'scenes': 0.15        # Visual transitions
}
```

Adjust weights based on content type:

- **Comedy content**: Increase `laughter` weight
- **Emotional content**: Increase `sentiment` weight
- **Educational content**: Increase `transcript` weight
- **Action content**: Increase `scenes` weight

## Viral Phrases/Keywords

### High-Viral Potential Phrases

**Hooks/Attention Grabbers:**
- "You won't believe..."
- "This changes everything..."
- "The secret to..."
- "What nobody tells you about..."
- "I made a huge mistake..."
- "This is illegal..."

**Story Beats:**
- "The plot twist..."
- "And then it happened..."
- "But here's the catch..."
- "The most important part..."

**Engagement:**
- "Comment if you agree..."
- "Like if you've experienced this..."
- "Wait for it..."
- "Watch till the end..."

### Moderate-Viral Potential

- Interesting facts
- Tips and tricks
- How-to content
- Before/after reveals

## Integration with Other Skills

This skill combines inputs from:

- `video-transcriber`: Transcript for content analysis
- `scene-detector`: Scene changes for cut points
- `laughter-detector`: Humorous moments
- `sentiment-analyzer`: Emotional peaks

Output is used by:

- `video-trimmer`: Create clips from highlights
- `autocut-shorts`: Full workflow execution

## Common Workflow

1. User provides video file
2. Transcribe with `video-transcriber`
3. Detect scenes with `scene-detector` (optional)
4. Detect laughter with `laughter-detector` (optional)
5. Analyze sentiment with `sentiment-analyzer` (optional)
6. Find highlights using this skill (combines all signals)
7. Create clips from highlights with `video-trimmer` or `autocut-shorts`

## Tips

- More input signals = better highlight detection
- Always provide transcript (minimum requirement)
- Scene detection helps with clean cuts
- Laughter detection improves viral potential
- Sentiment analysis identifies emotional peaks
- Adjust weights based on your content type
- Filter by score threshold for quality control
- Consider clip duration when selecting highlights

## Performance

- **Transcript only**: ~2 seconds for 1-minute video
- **Full analysis**: ~10-30 seconds for 10-minute video
- **Scales linearly** with video duration
- Can process in real-time for live content

## References

- Viral content analysis research
- Engagement metrics studies
- TikTok/YouTube algorithm insights
