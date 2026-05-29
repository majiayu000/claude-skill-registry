---
name: youtube-transcript-analyzer
description: "Use when analyzing YouTube videos for research or learning"
version: 0.4.0
---

<objective>
Download and analyze YouTube video transcripts to extract insights, understand concepts, and relate content to your work. Uses yt-dlp for reliable transcript extraction with intelligent chunking for long-form content.
</objective>

<when-to-use>
Use when you need to understand how a YouTube video/tutorial relates to your current project, research technical concepts explained in video format, extract key insights from talks or presentations, compare video content with your codebase or approach, or learn from video demonstrations without watching the entire video.
</when-to-use>

<prerequisites>
Ensure yt-dlp is installed:

```bash
# Install via pip
pip install yt-dlp

# Or via homebrew (macOS)
brew install yt-dlp

# Verify installation
yt-dlp --version
```

</prerequisites>

<transcript-extraction>
Setup temporary directory - IMPORTANT: Always create and use a temporary directory for downloaded files to avoid cluttering the repository:

```bash
# Create temporary directory for this analysis
ANALYSIS_DIR=$(mktemp -d)
echo "Using temporary directory: $ANALYSIS_DIR"
```

Download transcript using yt-dlp to extract subtitles/transcripts to the temporary
directory:

```bash
# Download transcript only (no video)
yt-dlp --skip-download --write-auto-sub --sub-format vtt --output "$ANALYSIS_DIR/transcript.%(ext)s" URL

# Or get manually created subtitles if available (higher quality)
yt-dlp --skip-download --write-sub --sub-lang en --sub-format vtt --output "$ANALYSIS_DIR/transcript.%(ext)s" URL

# Get video metadata for context
yt-dlp --skip-download --print-json URL > "$ANALYSIS_DIR/metadata.json"
```

Handle long transcripts - For transcripts exceeding 8,000 tokens (roughly 6,000 words or
45+ minutes):

1. Split into logical chunks based on timestamp or topic breaks
2. Generate a summary for each chunk focusing on key concepts
3. Create an overall synthesis connecting themes to the user's question
4. Reference specific timestamps for detailed sections

For shorter transcripts, analyze directly without chunking. </transcript-extraction>

<analysis-approach>
When analyzing with respect to a project or question:
1. Extract the video's core concepts and techniques
2. Identify patterns, architectures, or approaches discussed
3. Compare with the current project's implementation
4. Highlight relevant insights, differences, and potential applications
5. Note specific timestamps for key moments

Provide analysis in this format:

Video Overview:

- Title, author, duration
- Main topic and key themes

Key Insights:

- Concept 1 with timestamp
- Concept 2 with timestamp
- Technical approaches explained

Relevance to Your Project:

- Direct applications
- Differences from current approach
- Potential improvements or learnings

Specific Recommendations:

- Actionable items based on video content
- Code patterns or techniques to consider </analysis-approach>

<handling-common-issues>
No transcript available: Some videos lack auto-generated or manual captions. Inform user and offer alternative approaches (video description, comments).

Multiple languages: Prefer English transcripts using --sub-lang en. If unavailable,
check available languages with --list-subs.

Long processing time: Set expectations for videos over 2 hours. Offer to focus on
specific sections if timestamps provided. </handling-common-issues>

<best-practices>
Focus analysis on practical application rather than comprehensive summaries. Users want to know "how does this help me" not "what did they say for 90 minutes."

Extract concrete examples and code patterns when available. Reference specific
timestamps so users can jump to relevant sections.

When comparing with project code, be specific about similarities and differences. Vague
comparisons like "similar approach" don't add value.

For technical content, identify the underlying patterns and principles rather than
surface-level implementation details. Help users understand transferable concepts.
</best-practices>

<token-efficiency>
For very long transcripts (2+ hours):
- Process in 15-20 minute segments
- Summarize each segment to 200-300 words
- Create final synthesis under 500 words
- Provide detailed analysis only for highly relevant sections
</token-efficiency>
