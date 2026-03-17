---
name: youtube-transcript
description: Download YouTube video transcripts with automatic frame extraction for visual references. Use when analyzing YouTube videos, tutorials, or conference talks.
type: command
---

# YouTube Transcript Skill

Download and analyze YouTube video transcripts with automatic frame extraction at visual reference points.

## Usage

```
/youtube-transcript <youtube-url>
```

## What This Skill Does

1. **Downloads transcript** with timestamps (YouTube auto-captions or manual subtitles)
2. **Detects visual references** in the text ("look at this diagram", "as you can see here")
3. **Extracts frames** at those timestamps for context
4. **Presents** transcript with embedded images for analysis

## Requirements

### macOS

```bash
brew install yt-dlp ffmpeg
```

### Linux (Ubuntu/Debian)

```bash
sudo apt install ffmpeg
pip install yt-dlp
```

### Linux (Arch)

```bash
sudo pacman -S yt-dlp ffmpeg
```

## Instructions for Claude

When the user invokes `/youtube-transcript <url>`:

### Step 1: Check Dependencies

```bash
command -v yt-dlp >/dev/null 2>&1 || echo "MISSING: yt-dlp"
command -v ffmpeg >/dev/null 2>&1 || echo "MISSING: ffmpeg"
```

If missing, show installation instructions for the user's platform.

### Step 2: Create Output Directory

Use the scratchpad directory for output:

```bash
# Extract video ID from YouTube URL (POSIX-compatible, works on macOS and Linux)
# Handles: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID
URL="<url>"
VIDEO_ID=$(echo "$URL" | sed -E 's/.*[?&]v=([^&]+).*/\1/;s|.*/embed/([^?/]+).*|\1|;s|.*youtu\.be/([^?/]+).*|\1|')
OUTPUT_DIR="<scratchpad>/youtube-${VIDEO_ID}"
mkdir -p "${OUTPUT_DIR}/frames"
```

### Step 3: Download Transcript

```bash
cd "${OUTPUT_DIR}"

# Try auto-generated subtitles first, fall back to manual
yt-dlp --write-auto-sub --sub-lang en,de --skip-download --convert-subs srt -o "transcript" "<url>" 2>/dev/null || \
yt-dlp --write-sub --sub-lang en,de --skip-download --convert-subs srt -o "transcript" "<url>"
```

### Step 4: Analyze for Visual References

Read the transcript and identify timestamps where visual content is referenced. Look for patterns:

**German:**
- "schau(t)? (mal )?(hier|das)"
- "(dieses|das|dieser) (Diagramm|Bild|Schema|Chart|Graph|Screen|Slide)"
- "wie (du|ihr|Sie) (hier )?(siehst|sehen)"
- "auf (dem|diesem) (Bildschirm|Screen|Slide)"
- "hier sehen wir"

**English:**
- "look at this"
- "as you can see"
- "this (diagram|chart|slide|screen|image)"
- "let me show you"
- "here we have"
- "on the screen"

### Step 5: Download Video and Extract Frames

Only if visual references were found:

```bash
# First, list available formats to find a working one
yt-dlp -F "<url>"

# Then download using a specific format ID (prefer combined formats like 18 for 360p)
# Format 18 is usually 360p mp4 with video+audio combined - most reliable
yt-dlp -f 18 -o "${OUTPUT_DIR}/video.mp4" "<url>"

# If format 18 not available, try other combined formats (22=720p, 18=360p)
# Or use: yt-dlp -f "best[height<=480]" -o "${OUTPUT_DIR}/video.mp4" "<url>"

# Extract frame at timestamp (example: 01:23)
ffmpeg -ss 00:01:23 -i "${OUTPUT_DIR}/video.mp4" -frames:v 1 -q:v 2 "${OUTPUT_DIR}/frames/01_23.jpg"
```

**Important:** Avoid `-f worst` or complex format selectors - they often hang due to yt-dlp JS runtime issues. Use explicit format IDs instead.

Extract frames for each detected visual reference timestamp.

### Step 6: Present Results

Create a summary with:

1. **Video metadata** (title, duration, channel)
2. **Full transcript** with timestamps
3. **Visual references** - show the extracted frames inline where referenced
4. **Ready for questions** - offer to analyze specific parts

Example output format:

```markdown
## Video: [Title]
**Channel:** [Channel Name]
**Duration:** [Duration]

---

## Transcript

[00:00] Introduction to the topic...

[01:23] As you can see in this diagram...
![Frame at 01:23](frames/01_23.jpg)

[02:45] Let's move on to the next point...

---

## Extracted Frames

| Timestamp | Context | Frame |
|-----------|---------|-------|
| 01:23 | "this diagram shows..." | frames/01_23.jpg |

---

Ready to answer questions about this video.
```

## Cleanup

The output directory in scratchpad will be automatically cleaned up. If the user wants to keep the files, they should copy them to their project.

## Limitations

- Requires yt-dlp and ffmpeg installed locally
- Some videos may not have transcripts available
- Age-restricted or private videos may not be accessible
- Very long videos (>2h) may take time to process

## Troubleshooting

**No transcript found:**
- Video may not have captions enabled
- Try a different language: `--sub-lang en,de,es,fr`

**Video download stuck at 0%:**
- This is often caused by yt-dlp's format selection with JS runtime issues
- Solution: List formats first (`yt-dlp -F <url>`), then use explicit format ID (`yt-dlp -f 18 <url>`)
- Format 18 (360p mp4 combined) is usually the most reliable

**JS Runtime Warning:**
- yt-dlp may show "No supported JavaScript runtime" warning
- This is usually fine for downloads, but can cause format selection issues
- Install deno if needed: `brew install deno` or `curl -fsSL https://deno.land/install.sh | sh`

**Connection timeouts:**
- YouTube servers may be slow; retry with explicit format ID
- Kill stuck process: `pkill -f "yt-dlp.*VIDEO_ID"`

**yt-dlp errors:**
- Update yt-dlp: `pip install -U yt-dlp` or `brew upgrade yt-dlp`

**ffmpeg errors:**
- Ensure ffmpeg is installed with video codecs
