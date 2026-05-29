---
name: yt-transcribe
description: Use when user asks about YouTube video content, wants to know what a video says, needs information from a YouTube URL, or when video transcription would answer their question
---

# YouTube Video Transcription

## Overview

Use `yt-transcribe` to get the actual spoken content from YouTube videos. Web search and fetch tools cannot access video content - they only see metadata.

## When to Use

**Use this skill when:**
- User shares a YouTube URL and asks what it says/contains
- User wants information that likely exists in a video
- User asks "what does this video talk about?"
- You need to extract spoken content from YouTube

**Do NOT use:**
- For video metadata only (title, description) - web search is faster
- When user explicitly wants just the link, not content

## Quick Reference

| Flag | Purpose |
|------|---------|
| `-q` | **Required for LLMs** - clean stdout, no progress noise |
| `-m tiny` | Faster transcription (less accurate) |
| `-m medium` | More accurate (slower, larger model) |
| `-o file` | Save to file instead of stdout |
| `-f srt/vtt` | Include timestamps |

## Core Pattern

```bash
# Standard usage for LLM consumption
yt-transcribe "https://youtube.com/watch?v=VIDEO_ID" -q

# Faster but less accurate
yt-transcribe "https://youtube.com/watch?v=VIDEO_ID" -q -m tiny

# With timestamps
yt-transcribe "https://youtube.com/watch?v=VIDEO_ID" -q -f srt
```

**Always use `-q` flag** - suppresses progress output, gives clean transcript to stdout.

## Workflow

1. User provides YouTube URL or asks about video content
2. Run: `yt-transcribe "URL" -q`
3. Read and summarize the transcript for the user
4. Answer their specific question using the transcript content

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trying WebFetch on YouTube URLs | YouTube blocks bots, use yt-transcribe |
| Forgetting `-q` flag | Progress output pollutes response, always use `-q` |
| Web searching for "what does video say" | Search finds metadata, not content - transcribe instead |
| Using without setup | Run `yt-transcribe --setup` first if binaries missing (exit code 5) |

## Exit Codes

- `0` - Success
- `5` - Binary not found (run `--setup`)
- `3` - Network error
- `4` - Transcription error
