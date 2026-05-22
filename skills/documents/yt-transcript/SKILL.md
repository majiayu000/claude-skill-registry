---
name: yt-transcript
description: Fetch transcripts from YouTube videos. Use when user asks to get, download, extract, or retrieve YouTube video transcripts, captions, or subtitles. Also activates for video content analysis, summarizing YouTube videos, or processing video content.
allowed-tools:
  - Read
  - Write
  - Bash
---

# YouTube Transcript Skill

Fetch transcripts from YouTube videos for analysis, summarization, or content processing.

## When This Skill Activates

This skill automatically activates when:
- User asks to get, download, or extract YouTube transcripts
- User wants to summarize or analyze YouTube video content
- User mentions video captions or subtitles
- User needs to process YouTube video text content

## Quick Start

### Prerequisites

The skill requires `youtube-transcript-api` to be installed:

```bash
pip install youtube-transcript-api
```

Or with uv:

```bash
uv pip install youtube-transcript-api
```

### Basic Usage

Fetch a single transcript (outputs to stdout):

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py "https://youtu.be/dQw4w9WgXcQ"
```

Save to file:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py "https://youtu.be/dQw4w9WgXcQ" --output transcript.txt
```

Fetch multiple videos:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py \
  "https://youtu.be/VIDEO_ID_1" \
  "https://youtu.be/VIDEO_ID_2" \
  --output transcripts.txt
```

Get transcript without timestamps:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py "https://youtu.be/dQw4w9WgXcQ" --no-timestamps
```

## Supported URL Formats

The skill handles various YouTube URL formats:

- Short links: `https://youtu.be/dQw4w9WgXcQ`
- Standard URLs: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Embed URLs: `https://www.youtube.com/embed/dQw4w9WgXcQ`
- Video IDs only: `dQw4w9WgXcQ`
- URLs with parameters: `https://youtu.be/dQw4w9WgXcQ?si=abcd1234`

## Output Format

Default output includes timestamps:

```
# Transcript for https://youtu.be/dQw4w9WgXcQ (Video ID: dQw4w9WgXcQ)

0.00  First line of the transcript
2.50  Second line of the transcript
5.00  Third line of the transcript
```

Without `--no-timestamps` flag, plain text output:

```
# Transcript for https://youtu.be/dQw4w9WgXcQ (Video ID: dQw4w9WgXcQ)

First line of the transcript
Second line of the transcript
Third line of the transcript
```

## Common Workflows

### Analyze Video Content

```bash
# Fetch transcript
python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py "https://youtu.be/VIDEO_ID" --output video.txt

# Now Claude can read and analyze the content
```

### Summarize Multiple Videos

```bash
# Fetch all transcripts to one file
python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py \
  "https://youtu.be/VIDEO1" \
  "https://youtu.be/VIDEO2" \
  "https://youtu.be/VIDEO3" \
  --output all_transcripts.txt
```

### Extract Quotes or Key Points

```bash
# Get clean text without timestamps for easier processing
python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py "https://youtu.be/VIDEO_ID" --no-timestamps > clean.txt
```

## Troubleshooting

### No Transcript Available

Some videos don't have transcripts available. The script will report:
```
Error: Could not fetch transcript for: <url>
```

This can happen when:
- The video has no captions/subtitles
- The video is private or restricted
- The transcript is disabled by the uploader

### Transcripts Not Auto-Generated

YouTube auto-generates transcripts for many videos, but not all. If a video has no manual captions and no auto-generated captions, the transcript won't be available.

### Rate Limiting

For bulk operations, you may encounter rate limiting. The script fetches one transcript at a time to minimize issues.

## Requirements

- Python 3.8+
- `youtube-transcript-api` package
- Network access to YouTube's transcript servers

## Script Options

```
usage: get_transcript.py [-h] [-o OUTPUT] [--no-timestamps] urls [urls ...]

positional arguments:
  urls                  YouTube video URL(s)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file (default: stdout)
  --no-timestamps       Exclude timestamps from output
```

## Examples

### Get transcript for analysis

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py "https://www.youtube.com/watch?v=tgbNymZ7vqY" --output talk.txt
```

### Fetch clean text for summarization

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py "https://youtu.be/VIDEO_ID" --no-timestamps > summary_input.txt
```

### Batch process a playlist's videos

```bash
# Build URLs from a list of video IDs
for vid in VIDEO_ID1 VIDEO_ID2 VIDEO_ID3; do
  python ${CLAUDE_PLUGIN_ROOT}/scripts/get_transcript.py "https://youtu.be/${vid}" --output "transcript_${vid}.txt"
done
```
