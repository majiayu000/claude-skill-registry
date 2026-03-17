---
name: YouTube Transcription
description: This skill should be used when the user wants to "transcribe a YouTube video", "get a transcript of a video", "download and transcribe audio", or needs to convert video/audio content to searchable markdown text using AssemblyAI. Supports both YouTube URLs and local audio files.
version: 0.1.0
---

# YouTube Transcription Skill

Convert YouTube videos and audio files to searchable, formatted markdown transcripts using AssemblyAI.

## When to Use This Skill

Use this skill when you need to:
- Transcribe YouTube videos into markdown documents
- Convert audio files (MP3, WAV, M4A) to text transcripts
- Create searchable transcripts with metadata and proper formatting
- Add transcripts to knowledge bases or project documentation

## Core Workflow

The skill provides a three-step workflow:

1. **Download Audio** (if needed) - Extract audio from YouTube video using yt-dlp with Firefox cookie authentication
2. **Transcribe** - Send audio to AssemblyAI API for speech-to-text conversion
3. **Format & Save** - Create markdown document with metadata and transcript text

## Prerequisites

- **AssemblyAI API key** - Free account at https://www.assemblyai.com (set as `ASSEMBLYAI_API_KEY` environment variable)
- **Firefox browser** - For YouTube authentication (only needed for video downloads)
- **yt-dlp** - Automatically installed by `uv run`

## Quick Start

### From YouTube URL

```bash
export ASSEMBLYAI_API_KEY="your_key_here"
cd /path/to/vault
uv run --with=assemblyai ./.claude/skills/youtube-transcription/scripts/transcribe_video.py "https://youtu.be/VIDEO_ID"
```

### From Local Audio File

```bash
export ASSEMBLYAI_API_KEY="your_key_here"
uv run --with=assemblyai ./.claude/skills/youtube-transcription/scripts/transcribe_video.py /path/to/audio.mp3
```

**Output:** Full transcript printed to stdout + saved to `/tmp/transcript.txt`

## Common Tasks

### Task 1: Transcribe a YouTube Video and Save to Project

```bash
# 1. Run transcription
export ASSEMBLYAI_API_KEY="your_key_here"
uv run --with=assemblyai ./.claude/skills/youtube-transcription/scripts/transcribe_video.py "https://youtu.be/_gPODg6br5w"

# 2. Copy output to project with metadata
# Edit the transcript file to add:
# - Title
# - Video ID, URL, Date
# - Proper markdown formatting

# 3. Save to your project
cp /tmp/transcript.txt pages/Projects/My-Project/Video-Title-Transcript.md
```

### Task 2: Download YouTube Audio First (if video requires authentication)

```bash
# Download with Firefox cookies
yt-dlp -x --audio-format mp3 --cookies-from-browser firefox -o "video.mp3" "https://youtu.be/VIDEO_ID"

# Then transcribe the saved file
export ASSEMBLYAI_API_KEY="your_key_here"
uv run --with=assemblyai ./.claude/skills/youtube-transcription/scripts/transcribe_video.py ./video.mp3
```

### Task 3: Batch Transcribe Multiple Videos

Create a simple script to loop through videos:

```bash
#!/bin/bash
export ASSEMBLYAI_API_KEY="your_key_here"
SKILL_PATH="./.claude/skills/youtube-transcription/scripts/transcribe_video.py"

for url in \
    "https://youtu.be/VIDEO1" \
    "https://youtu.be/VIDEO2" \
    "https://youtu.be/VIDEO3"
do
    echo "Transcribing: $url"
    uv run --with=assemblyai $SKILL_PATH "$url"
    sleep 5  # Rate limiting
done
```

## Troubleshooting

### Problem: "Sign in to confirm you're not a bot"

YouTube is blocking yt-dlp. This happens with age-restricted or new videos.

**Solution:** Use Firefox cookies with JavaScript runtime:
```bash
yt-dlp -x --audio-format mp3 \
    --cookies-from-browser firefox \
    --js-runtimes bun \
    --remote-components ejs:github \
    -o "video.mp3" \
    "https://youtu.be/VIDEO_ID"
```

### Problem: AssemblyAI module not found

Script needs the AssemblyAI package at runtime.

**Solution:** Always use `--with=assemblyai` flag:
```bash
uv run --with=assemblyai ./scripts/transcribe_video.py <input>
```

### Problem: API key not recognized

AssemblyAI requires valid API key.

**Solution:** Verify environment variable is set:
```bash
echo $ASSEMBLYAI_API_KEY  # Should show your key
```

Set it in your shell profile to persist:
```bash
# Add to ~/.bashrc or ~/.zshrc
export ASSEMBLYAI_API_KEY="your_actual_key_here"
```

## Output Format

The skill outputs raw transcript text. Format it as markdown with metadata:

```markdown
# Video Title

**Source:** YouTube - Creator Name (@handle)
**Video ID:** VIDEO_ID
**URL:** https://youtu.be/VIDEO_ID
**Date:** YYYY-MM-DD
**Duration:** MM:SS

---

## Full Transcript

[Transcript text...]

---

## Key Sections

- [Timestamp] Section title
- [Timestamp] Another section
```

## Integration Tips

### For [[Second Brain]] Project

Save transcripts following this structure:

```
pages/Projects/Second Brain/
├── Nate B Jones - Why 2026 Is the Year to Build a Second Brain - Transcript.md
├── Nate B Jones - Follow-up Video - Transcript.md
└── README.md (links to transcripts)
```

Update the project README to include:
```markdown
- `[[Title - Transcript]]` - Full video transcript
```

### For Knowledge Base

Create a transcripts folder:
```
pages/PKB/Video Transcripts/
├── Topic 1/
│   └── Video Title - Transcript.md
├── Topic 2/
│   └── Another Video - Transcript.md
```

## Cost & Limits

- **AssemblyAI pricing:** ~$0.60-1.00 per hour of audio
- **Free tier:** Limited minutes per month
- **Check usage:** https://www.assemblyai.com/dashboard
- **Language support:** English (best), others supported but less accurate

## Advanced Options

See `references/assemblyai_options.md` for:
- Language detection
- Speaker diarization (multiple speakers)
- Entity detection
- Summarization options
- Custom punctuation rules

## Related Skills

- [[Second Brain]] - Knowledge management project using transcripts
- [[Git Workflow]] - For committing transcripts to version control

## Resources

- AssemblyAI documentation: https://www.assemblyai.com/docs/
- yt-dlp documentation: https://github.com/yt-dlp/yt-dlp/wiki
- Skill implementation: `.claude/skills/youtube-transcription/scripts/transcribe_video.py`
