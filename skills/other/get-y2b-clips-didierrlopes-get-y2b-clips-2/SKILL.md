---
name: get-y2b-clips
description: Extract the most meaningful, engaging clips from YouTube videos. Use when user provides a YouTube URL and wants to find highlights, best moments, controversial takes, or valuable segments. Supports specifying number of clips or topic focus.
allowed-tools: Bash,Read,Write,Glob
---

# YouTube Nuggets Extractor

Extract the most valuable clips ("nuggets") from YouTube videos automatically. Analyzes transcripts to find high-value segments based on controversy, insightful analysis, or user-specified topics.

## When to Use This Skill

Activate when the user:
- Wants to extract "best clips", "highlights", or "nuggets" from a YouTube video
- Asks to find "interesting moments" or "valuable segments"
- Wants controversial takes, insights, or specific topics from a video
- Provides a YouTube URL and mentions clips, segments, or highlights

## Dependencies Check

**ALWAYS check dependencies first:**

```bash
# Check for yt-dlp
command -v yt-dlp || echo "MISSING: yt-dlp"

# Check for ffmpeg
command -v ffmpeg || echo "MISSING: ffmpeg"
```

### Install Missing Dependencies

**yt-dlp:**
```bash
# macOS
brew install yt-dlp

# Linux
sudo apt update && sudo apt install -y yt-dlp

# pip (universal)
pip3 install yt-dlp
```

**ffmpeg:**
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt update && sudo apt install -y ffmpeg
```

## Input Requirements

- **Required**: YouTube URL
- **Optional** (ask user if not specified for long videos >30 min):
  - Number of clips (default: 3-5 based on video length)
  - Topic focus keywords
  - Min/max clip duration (default: 30s-180s)

## Available Python Scripts

The skill includes helper scripts in the `.claude/skills/get-y2b-clips/` directory:

| Script | Purpose |
|--------|---------|
| `parse_vtt.py` | Parse VTT subtitles into segments.json (cleans HTML entities) |
| `extract_transcript.py` | Extract transcript with auto sentence boundary detection |
| `download_clip.py` | Download video clip with retry logic and progress reporting |
| `burn_subtitles.py` | Generate subtitled video with hardcoded captions |
| `utils.py` | Shared utilities for timestamp parsing |

## Transcript Curation (CRITICAL)

**Auto-generated YouTube captions lack punctuation.** The transcript must be manually curated to ensure:

1. **Complete starting sentence**: Must begin with a coherent thought, not mid-sentence
2. **Complete ending sentence**: Must end with a complete thought, not cut off
3. **Proper formatting**: Sentences on separate lines with blank lines between
4. **Punctuation added**: Add periods, commas, question marks as needed

### Workflow: Transcript → Video (Not the reverse!)

```
1. Identify target timestamps (where the insight is)
2. Run extract_transcript.py to get raw extraction + suggested video timestamps
3. MANUALLY CURATE the transcript:
   - Ensure first sentence is complete (may need to trim start)
   - Ensure last sentence is complete (may need to extend/trim end)
   - Add punctuation and formatting
   - Split into readable paragraphs
4. Use the VIDEO_START and VIDEO_END from script output
   - Video should start ~2s BEFORE first word of transcript
   - Video should end ~2s AFTER last word of transcript
5. Download video using those curated timestamps
```

### Example Curation:

**Raw extraction** (bad):
```
Successful why do you think we're learned and it turns out that many or most of the people in The Venture business...
```

**Curated** (good):
```
It turns out that many or most of the people in the venture business historically would answer that question by telling you they finance the best and brightest, the greatest managers.

We do not.

We have always focused on the market - the size of the market, the dynamics of the market, the nature of the competition.

Because our objective always was to build big companies.

If you don't attack a big market, it's highly unlikely you're ever going to build a big company.
```

### Using extract_transcript.py

```bash
# Run the script to get raw extraction and video timestamps
python3 extract_transcript.py \
    --start 00:04:00 \        # Target start (where insight begins)
    --end 00:05:08 \          # Target end (where insight ends)
    --title "Clip Title" \
    --source "Video Title" \
    --output "clip_folder/Transcript.txt" \
    --json                     # Also outputs JSON with timestamps

# Output will show:
#   VIDEO_START=00:03:58      <- Use this for video download
#   VIDEO_END=00:05:10        <- Use this for video download
```

Then manually edit the Transcript.txt file to curate the text before downloading the video.

## Console Progress Reporting

**IMPORTANT**: Provide clear progress updates to the user at each stage:

```
[SETUP] Fetching video info...
  ✓ Video: "Title Here" (32 min)
  ✓ Output: ./clips/2024-01-01_12-00-00_video-slug/

[TRANSCRIPT] Downloading subtitles...
  ✓ Auto-generated English subtitles found
  ✓ Parsed 912 segments

[ANALYSIS] Identifying best clips...
  ✓ Found 5 high-value segments
  ✓ Selected top 2 clips

[CLIP 1/2] "Factory is the Weapon" (08:56 - 10:31)
  ✓ metadata.json created
  ✓ Transcript.txt extracted (321 words)
  ✓ Video.mp4 downloaded (14.1 MB)
  ✓ Subtitled.mp4 created (13.8 MB)

[CLIP 2/2] "Peter Thiel Always Right" (29:59 - 31:17)
  ✓ metadata.json created
  ✓ Transcript.txt extracted (307 words)
  ⚠ Download failed (403), retrying...
  ✓ Video.mp4 downloaded (10.4 MB)
  ✓ Subtitled.mp4 created (10.1 MB)

[DONE] Extracted 2 clips (2m53s total)
```

## Retry Logic for Downloads

YouTube occasionally returns 403 errors. Always implement retry logic:

```python
# Use the download_clip.py script with built-in retries
python3 .claude/skills/get-y2b-clips/download_clip.py \
    --url "$VIDEO_URL" \
    --start "00:08:56" \
    --end "00:10:31" \
    --output "$CLIP_DIR/Video.mp4" \
    --retries 3
```

Or implement inline:
```python
import time
import subprocess

def download_with_retry(cmd, max_retries=3, delay=2):
    for attempt in range(max_retries):
        result = subprocess.run(cmd)
        if result.returncode == 0:
            return True
        print(f"  ⚠ Retry {attempt + 1}/{max_retries}...")
        time.sleep(delay)
    return False
```

## Complete Workflow

**CRITICAL: The order of operations is WHY → TRANSCRIPT → VIDEO**

The "Why" justifies the selection, the transcript defines the EXACT timestamps, and the video is downloaded to match those exact timestamps.

### Phase 1: Setup

```bash
# Get video info
VIDEO_URL="USER_PROVIDED_URL"
VIDEO_TITLE=$(yt-dlp --print "%(title)s" "$VIDEO_URL" | tr '/:?*"<>|\\' '-')
VIDEO_DURATION=$(yt-dlp --print "%(duration)s" "$VIDEO_URL")
VIDEO_ID=$(yt-dlp --print "%(id)s" "$VIDEO_URL")

echo "Video: $VIDEO_TITLE"
echo "Duration: $((VIDEO_DURATION / 60)) minutes"

# Create output folder
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
SLUG=$(echo "$VIDEO_TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-50)
OUTPUT_DIR="./clips/${TIMESTAMP}_${SLUG}"
mkdir -p "$OUTPUT_DIR"

echo "Output folder: $OUTPUT_DIR"
```

### Phase 2: Get Transcript with Exact Timestamps

**Priority order: Manual subtitles → Auto-generated → Whisper**

```bash
cd "$OUTPUT_DIR"

# Check available subtitles
yt-dlp --list-subs "$VIDEO_URL"

# Try manual subtitles first
if yt-dlp --write-sub --sub-langs "en" --skip-download -o "transcript" "$VIDEO_URL" 2>/dev/null; then
    echo "Manual subtitles downloaded"
elif yt-dlp --write-auto-sub --sub-langs "en" --skip-download -o "transcript" "$VIDEO_URL" 2>/dev/null; then
    echo "Auto-generated subtitles downloaded"
else
    echo "No subtitles available - Whisper transcription required"
    # Ask user before proceeding with Whisper (downloads audio)
fi
```

**Parse VTT using the skill's Python script:**

```bash
# Parse VTT file into segments.json and full_transcript.txt
python3 .claude/skills/get-y2b-clips/parse_vtt.py transcript.en.vtt

# This creates:
#   - segments.json (for precise timestamp lookup)
#   - full_transcript.txt (for reading/analysis)
```

**Alternative inline Python (if script not available):**

```python
import re
import json

def parse_vtt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    segments = []
    current_start = None
    current_end = None
    seen_text = set()

    for line in lines:
        line = line.strip()

        # Check if this is a timestamp line
        time_match = re.match(r'^(\d{2}:\d{2}:\d{2})\.(\d{3}) --> (\d{2}:\d{2}:\d{2})\.(\d{3})', line)
        if time_match:
            current_start = f"{time_match.group(1)}.{time_match.group(2)}"
            current_end = f"{time_match.group(3)}.{time_match.group(4)}"
            continue

        # Skip metadata and empty lines
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue

        # Skip lines with tags (word-by-word breakdowns)
        if '<' in line:
            continue

        # This is a clean text line
        text = line.strip()
        if text and text not in seen_text and current_start:
            seen_text.add(text)
            segments.append({
                'start': current_start,
                'end': current_end,
                'text': text
            })

    return segments

segments = parse_vtt("transcript.en.vtt")

# Write full transcript with timestamps
with open('full_transcript.txt', 'w') as f:
    for seg in segments:
        f.write(f"[{seg['start']}] {seg['text']}\n")

# Write segments JSON for precise timestamp lookup
with open('segments.json', 'w') as f:
    json.dump(segments, f, indent=2)

print(f"Parsed {len(segments)} segments with exact timestamps")
```

### Phase 3: Analyze Content & Generate "Why" FIRST

**This is the critical phase - identify segments and justify selection BEFORE extracting.**

Read `full_transcript.txt` and analyze using these scoring criteria:

1. **Controversy Signals** (weight: 0.30)
   - "I disagree", "controversial", "unpopular opinion"
   - Strong language: "absolutely", "never", "always"
   - Debate markers: "push back", "challenge that"

2. **Insight Signals** (weight: 0.35)
   - Statistics, data points, percentages
   - Predictions: "will happen", "in X years"
   - Frameworks: "the way I see it", "my model"
   - Expert knowledge, technical depth

3. **Engagement Signals** (weight: 0.20)
   - Rhetorical questions
   - Stories: "let me tell you", "for example"
   - Emotional peaks, emphasis
   - Direct address: "think about it"

4. **Topic Match** (weight: 0.15, or 0.40 if user specified topics)
   - Keyword presence
   - Semantic relevance

**Analysis output - use EXACT timestamps from transcript:**

For each identified clip, record:
1. **Title**: Short descriptive name
2. **Start timestamp**: EXACT timestamp from first line of segment (from segments.json)
3. **End timestamp**: EXACT timestamp from last line of segment (from segments.json)
4. **Why**: Full justification with scores

**IMPORTANT**: The start and end times MUST come from the transcript timestamps. Do not approximate or round. The video will be cut to match these exact times.

### Phase 4: For Each Clip - Create Files in Order

**Order: metadata.json → Transcript.txt → Video.mp4 → Subtitled.mp4**

#### Step 1: Create metadata.json (combines "why" + transcript info)

```python
import json

clip_metadata = {
    "title": "Clip Title",
    "source_video": "Video Title",
    "video_start": "00:12:06.000",
    "video_end": "00:14:05.000",
    "duration_seconds": 119,
    "word_count": 321,
    "transcript": "Full transcript text with proper formatting...",
    "selection_rationale": {
        "controversy": {
            "score": 8,
            "reason": "Explanation of controversy signals found"
        },
        "insight": {
            "score": 9,
            "reason": "Key insights delivered"
        },
        "engagement": {
            "score": 7,
            "reason": "Engagement signals found"
        },
        "relevance": {
            "score": 8,
            "reason": "How it relates to the main topic"
        }
    },
    "actionable_takeaway": "What viewers/investors should do with this information"
}

with open('Clip Title metadata.json', 'w') as f:
    json.dump(clip_metadata, f, indent=2)
```

#### Step 2: Create Transcript.txt (human-readable version)

Extract transcript text with a 5-second buffer before and after the video timestamps. This ensures all spoken words in the video clip are captured in the transcript (accounting for keyframe cuts).

**Key rules:**
- **Clean text only** - no timestamps in the output
- **5-second buffer** - transcript covers slightly more than the video
- **Proper formatting** - capitalize first letter of sentences, new line for each sentence
- **Readable flow** - sentences separated by blank lines for easy reading

**Formatting the transcript:**
1. Join all segment text together
2. Split on sentence boundaries (. ! ?)
3. Capitalize first letter of each sentence
4. Write each sentence on its own line with blank line between

```python
import json
import re

# Load segments
with open('segments.json', 'r') as f:
    segments = json.load(f)

# Define VIDEO boundaries (what will be downloaded)
video_start = "00:12:06.000"
video_end = "00:14:05.000"

# Define TRANSCRIPT boundaries (5-second buffer)
transcript_start = "00:12:01.000"  # 5s before video
transcript_end = "00:14:10.000"    # 5s after video

# Extract matching segments
clip_text = []
for seg in segments:
    if seg['start'] >= transcript_start and seg['start'] <= transcript_end:
        clip_text.append(seg['text'])

# Join and format nicely
raw_text = ' '.join(clip_text)

# Split into sentences and format
sentences = re.split(r'(?<=[.!?])\s+', raw_text)
formatted_sentences = []
for s in sentences:
    s = s.strip()
    if s:
        # Capitalize first letter
        s = s[0].upper() + s[1:] if len(s) > 1 else s.upper()
        formatted_sentences.append(s)

# Write clean, formatted transcript
with open('Clip_Title Transcript.txt', 'w') as f:
    f.write(f"Clip Title - Transcript\n")
    f.write(f"Source: Video Title\n")
    f.write(f"Video: {video_start[:8]} - {video_end[:8]}\n\n---\n\n")
    f.write('\n\n'.join(formatted_sentences))  # Each sentence on new line
```

#### Step 3: Download Video using EXACT timestamps

**CRITICAL**: Use the same timestamps from the transcript extraction.

```bash
START_TIME="00:12:06"  # Must match transcript start
END_TIME="00:14:05"    # Must match transcript end
CLIP_TITLE="Clip Title"
SAFE_TITLE=$(echo "$CLIP_TITLE" | tr '/:?*"<>|\\' '-')

# Create clip folder
CLIP_DIR="$OUTPUT_DIR/01_$(echo "$SAFE_TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | cut -c1-40)"
mkdir -p "$CLIP_DIR"

# Download video clip with EXACT timestamps
yt-dlp -f 'bestvideo[height<=1080]+bestaudio/best[height<=1080]' \
  --download-sections "*${START_TIME}-${END_TIME}" \
  --force-keyframes-at-cuts \
  --merge-output-format mp4 \
  -o "$CLIP_DIR/${SAFE_TITLE} Video.%(ext)s" \
  "$VIDEO_URL"
```

#### Step 4: Create Subtitled Video

**ALWAYS create a subtitled version** for social media sharing. Uses ffmpeg to burn subtitles directly into the video with styled captions.

```bash
# Use the burn_subtitles.py script
python3 .claude/skills/get-y2b-clips/burn_subtitles.py \
    --video "$CLIP_DIR/${SAFE_TITLE} Video.mp4" \
    --segments segments.json \
    --start "$START_TIME" \
    --end "$END_TIME" \
    --output "$CLIP_DIR/${SAFE_TITLE} Subtitled.mp4"
```

**What it does:**
1. Reads `segments.json` for accurate word-level timing
2. Generates SRT subtitles for the clip's time range
3. Burns subtitles into video using ffmpeg with styling:
   - Large readable font (24pt)
   - Semi-transparent black background
   - White text with black outline
   - Bottom-center positioning

**Subtitle options:**
```bash
# Custom font size (default: 24)
--font-size 28

# Keep the SRT file (for external use)
--keep-srt

# When video has buffer before speech starts (sync fix)
--transcript-start "00:31:38.350"

# When video has buffer after speech ends
--transcript-end "00:32:50.000"
```

**Important**: If the video starts a few seconds before the actual speech, use `--transcript-start` to specify when the transcript content begins. This prevents showing subtitles for content before the clip's main topic.

### Phase 5: Generate Metadata

```json
{
  "source": {
    "url": "VIDEO_URL",
    "title": "VIDEO_TITLE",
    "video_id": "VIDEO_ID",
    "duration_seconds": DURATION
  },
  "extraction": {
    "date": "ISO_TIMESTAMP",
    "output_dir": "OUTPUT_DIR",
    "clip_count": N,
    "topic_filter": null
  },
  "clips": [
    {
      "index": 1,
      "folder": "01_clip_slug",
      "title": "Clip Title",
      "start_time": "00:12:06.000",
      "end_time": "00:14:05.000",
      "duration_seconds": 119,
      "scores": {
        "controversy": 0.9,
        "insight": 0.9,
        "engagement": 0.8,
        "overall": 0.87
      },
      "summary": "Brief description"
    }
  ]
}
```

### Phase 6: Summary

Display to user:
- Number of clips extracted
- Total clip duration
- List of clips with titles and EXACT timestamps
- Output folder location

## Timestamp Alignment Rules

**These rules ensure video matches transcript exactly:**

1. **Source of truth**: The VTT transcript timestamps are the source of truth
2. **No rounding**: Use timestamps exactly as they appear in segments.json
3. **Verify alignment**: The first and last words in `Transcript.txt` should match the first and last words spoken in `Video.mp4`
4. **Buffer if needed**: If a sentence is cut mid-word, extend to the next segment boundary

## Clip Duration Guidelines

| Video Length | Recommended Clips | Default Clip Length |
|--------------|-------------------|---------------------|
| < 15 min     | 1-2               | 30-60 seconds       |
| 15-30 min    | 2-3               | 45-90 seconds       |
| 30-60 min    | 3-4               | 60-120 seconds      |
| 1-2 hours    | 4-5               | 90-180 seconds      |
| > 2 hours    | 5-7               | 90-180 seconds      |

## Interactive Flow (Long Videos)

For videos > 30 minutes without user guidance, ask:

```
I found a [X] minute video. How would you like to proceed?

A) Extract top 5 clips automatically (recommended)
B) Focus on specific topics - please specify keywords
C) Extract more clips - specify how many
D) Let me scan the transcript first and suggest topics
```

## Error Handling

| Issue | Solution |
|-------|----------|
| No subtitles | Offer Whisper with audio size warning |
| ffmpeg missing | Provide install command |
| Clip download fails | Retry with simpler format `-f best` |
| Private video | Inform user, cannot proceed |
| Very short video | Suggest 1 clip or full download |
| Timestamp mismatch | Re-verify against segments.json |

## Output File Naming

- Folder: `YYYY-MM-DD_HH-MM-SS_<video-slug>/`
- Clips: `NN_<clip-slug>/`
- Files per clip:
  - `<Title> metadata.json` - Complete clip info (transcript, timestamps, why selected)
  - `<Title> Transcript.txt` - Human-readable transcript with formatting
  - `<Title> Video.mp4` - Raw video clip
  - `<Title> Subtitled.mp4` - Video with burned-in captions (for social media)

### Per-Clip metadata.json Structure

Each clip folder contains a `metadata.json` with all information combined:

```json
{
  "title": "This Is NOT a Bubble",
  "source_video": "Bitcoin Fear Hits All-Time High",
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID&t=1896s",
  "video_start": "00:31:36.000",
  "video_end": "00:32:54.000",
  "transcript_start": "00:31:38.350",
  "duration_seconds": 78,
  "word_count": 218,
  "selection_rationale": {
    "controversy": {
      "score": 10,
      "reason": "Directly calls out Michael Burr and Jeff Gundlach as wrong about AI bubble"
    },
    "insight": {
      "score": 9,
      "reason": "Data-driven comparison: NDX 800% vs 100%, Nvidia $60B quarterly revenue"
    },
    "engagement": {
      "score": 9,
      "reason": "Strong emotional conviction, direct callout of famous contrarians"
    },
    "relevance": {
      "score": 9,
      "reason": "Directly addresses fear sentiment from video title"
    }
  },
  "actionable_takeaway": "Don't conflate extreme fear with bubble conditions. Look at earnings growth and historical comparisons.",
  "transcript": "Full transcript text here (always last key for readability)..."
}
```

**Notes**:
- `video_url`: Direct link to the clip's start time in the original video (uses `&t=XXXs` parameter)
- `transcript_start`: Used when video has a buffer before speech starts (ensures subtitle sync)

## Example Session

**User**: Extract the best clips from https://www.youtube.com/watch?v=abc123

**Claude**:
1. Checks dependencies (yt-dlp, ffmpeg)
2. Gets video info: "AI Future Podcast - 1:45:00"
3. Downloads transcript with exact timestamps
4. Analyzes transcript, identifies top segments
5. **For each clip:**
   - Creates metadata.json (transcript + selection rationale + scores)
   - Creates Transcript.txt (human-readable version)
   - Downloads video using exact timestamps
   - Creates subtitled version with burned-in captions
6. Returns summary with folder location

**User**: Get 3 clips about "startup funding" from https://youtube.com/watch?v=xyz789

**Claude**:
1. Same setup
2. Filters transcript for "startup", "funding", "invest", "raise" keywords
3. Scores segments with topic_match weighted higher
4. For each of 3 clips: metadata.json → Transcript.txt → Video → Subtitled Video
5. Returns summary
