---
name: youtube-transcript-analyzer
description:
  Use when analyzing YouTube videos for research, learning, or understanding how
  content relates to a project - downloads transcripts with yt-dlp, chunks long
  content, and provides context-aware analysis
---

# YouTube Transcript Analyzer

## Overview

Download and analyze YouTube video transcripts to extract insights, understand concepts,
and relate content to your work. Uses yt-dlp for reliable transcript extraction with
intelligent chunking for long-form content.

## When to Use

Use when you need to:

- Understand how a YouTube video/tutorial relates to your current project
- Research technical concepts explained in video format
- Extract key insights from talks, presentations, or educational content
- Compare video content with your codebase or approach
- Learn from video demonstrations without watching the entire video

## Prerequisites

Ensure yt-dlp is installed:

```bash
# Install via pip
pip install yt-dlp

# Or via homebrew (macOS)
brew install yt-dlp

# Verify installation
yt-dlp --version
```

## Transcript Extraction Process

### Download Transcript

Use yt-dlp to extract subtitles/transcripts:

```bash
# Download transcript only (no video)
yt-dlp --skip-download --write-auto-sub --sub-format vtt --output "transcript.%(ext)s" URL

# Or get manually created subtitles if available (higher quality)
yt-dlp --skip-download --write-sub --sub-lang en --sub-format vtt --output "transcript.%(ext)s" URL

# Get video metadata for context
yt-dlp --skip-download --print-json URL
```

### Handle Long Transcripts

For transcripts exceeding 8,000 tokens (roughly 6,000 words or 45+ minutes):

1. Split into logical chunks based on timestamp or topic breaks
2. Generate a summary for each chunk focusing on key concepts
3. Create an overall synthesis connecting themes to the user's question
4. Reference specific timestamps for detailed sections

For shorter transcripts, analyze directly without chunking.

## Analysis Approach

### Context-Aware Analysis

When analyzing with respect to a project or question:

1. Extract the video's core concepts and techniques
2. Identify patterns, architectures, or approaches discussed
3. Compare with the current project's implementation
4. Highlight relevant insights, differences, and potential applications
5. Note specific timestamps for key moments

### Structured Output

Provide analysis in this format:

**Video Overview:**

- Title, author, duration
- Main topic and key themes

**Key Insights:**

- Concept 1 with timestamp
- Concept 2 with timestamp
- Technical approaches explained

**Relevance to Your Project:**

- Direct applications
- Differences from current approach
- Potential improvements or learnings

**Specific Recommendations:**

- Actionable items based on video content
- Code patterns or techniques to consider

## Example Workflow

```bash
# 1. Get video metadata
yt-dlp --print-json "https://youtube.com/watch?v=VIDEO_ID" > metadata.json

# 2. Download transcript
yt-dlp --skip-download --write-auto-sub --sub-lang en --sub-format vtt \
  --output "transcript" "https://youtube.com/watch?v=VIDEO_ID"

# 3. Read and analyze transcript content
# 4. If long: chunk by timestamp ranges (every 10-15 minutes)
# 5. Generate summaries and relate to user's question
```

## Handling Common Issues

**No transcript available:**

- Some videos lack auto-generated or manual captions
- Inform user and offer alternative approaches (video description, comments)

**Multiple languages:**

- Prefer English transcripts: `--sub-lang en`
- If unavailable, check available languages: `--list-subs`

**Long processing time:**

- Set expectations for videos over 2 hours
- Offer to focus on specific sections if timestamps provided

## Best Practices

Focus analysis on practical application rather than comprehensive summaries. Users
want to know "how does this help me" not "what did they say for 90 minutes."

Extract concrete examples and code patterns when available. Reference specific
timestamps so users can jump to relevant sections.

When comparing with project code, be specific about similarities and differences.
Vague comparisons like "similar approach" don't add value.

For technical content, identify the underlying patterns and principles rather than
surface-level implementation details. Help users understand transferable concepts.

## Token Efficiency

For very long transcripts (2+ hours):

- Process in 15-20 minute segments
- Summarize each segment to 200-300 words
- Create final synthesis under 500 words
- Provide detailed analysis only for highly relevant sections
