---
name: youtube-transcribe
description: This skill should be used when the user asks to "download YouTube transcript", "get YouTube captions", "extract YouTube subtitles", or needs to retrieve transcript from a YouTube video.
license: MIT
compatibility: opencode
metadata:
  category: media
  version: 2.0.0
---

# YouTube Transcribe

## When to Use This Skill

Use this skill when:
- User requests YouTube video transcript or captions
- User wants to extract subtitles from YouTube
- User needs transcript content from a video

## Overview

This skill guides downloading YouTube transcripts using `yt-dlp` and formatting them as structured HTML.

**Core principle:** Create HTML transcript with title, chapter headings (using video chapters if available), and paragraph content. Abort cleanly if transcript unavailable.

## Output Format

**Create one file:** `transcript.html` - Structured HTML with:
- `<h1>` title from video
- `<h2>` chapter headings with start timestamp only (format: `MM:SS - Title`)
- `<p>` paragraph content under each chapter

**Chapter sources (in priority order):**
1. **Video chapters** from description (if available) - use these timestamps and titles
2. **Auto-generated chapters** - create 1-3 minute sections with descriptive titles

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| Check transcript availability | `yt-dlp --list-subs URL` | Run first to verify |
| Get video metadata + chapters | `yt-dlp --print "%(title)s\|%(chapters)s" URL` | Chapters may be null |
| Download transcript | `yt-dlp --write-auto-sub --sub-lang en --sub-format vtt --skip-download URL` | VTT has timestamps |
| Download manual subs (fallback) | `yt-dlp --write-sub --sub-lang en --sub-format vtt --skip-download URL` | If auto unavailable |

## Implementation Steps

### Step 1: Check Transcript Availability

```bash
yt-dlp --list-subs VIDEO_URL
```

**If no subtitles available:**
- ✅ Abort with message: "This video does not have transcripts available."
- ❌ Do NOT attempt speech-to-text, scraping, or workarounds

### Step 2: Get Video Metadata and Chapters

```bash
yt-dlp --print "%(title)s|%(description)s" VIDEO_URL
```

**Check description for chapter markers:**
- Chapter format: `MM:SS Title` or `HH:MM:SS Title` on separate lines
- Example:
  ```
  0:00 Introduction
  2:30 Main Topic
  5:15 Conclusion
  ```

**If chapters exist in description:**
- ✅ Use these timestamps and titles for H2 headings
- ✅ Format: `MM:SS - Title` (start timestamp and title only)

**If no chapters in description:**
- Create chapters automatically (see Step 4)

### Step 3: Download Transcript

```bash
# Try auto-generated first
yt-dlp --write-auto-sub --sub-lang en --sub-format vtt --skip-download VIDEO_URL

# If auto unavailable, try manual
yt-dlp --write-sub --sub-lang en --sub-format vtt --skip-download VIDEO_URL
```

### Step 4: Process Transcript

**Parse VTT file:**
1. Remove VTT headers and metadata
2. Remove inline timing tags: `<00:00:00.000>`, `<c>`, etc.
3. Extract timestamps from cue lines: `00:00:00.000 --> 00:00:00.000`
4. Clean and deduplicate text

**If using video chapters (from description):**
- Group transcript text by chapter timestamp ranges
- Use chapter titles from description
- Format H2: `MM:SS - Chapter Title`

**If creating auto-generated chapters:**
- Create 1-3 minute sections
- Generate descriptive titles from content (3-8 words, max 60 chars)
- Format H2: `MM:SS - Generated Title`

### Step 5: Create HTML File

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Video Title Here</title>
</head>
<body>

    <h1>Video Title Here</h1>

    <h2>0:00 - Introduction</h2>
    <p>First paragraph of this chapter...</p>
    <p>Second paragraph of this chapter...</p>

    <h2>2:30 - Main Topic</h2>
    <p>Content for this section...</p>

</body>
</html>
```

**Requirements:**
- ✅ UTF-8 charset declaration
- ✅ `<h1>` with video title
- ✅ `<h2>` with format `MM:SS - Title`
- ✅ Paragraphs grouped under chapters
- ✅ Clean semantic HTML

### Step 6: Clean Up

Remove temporary VTT file after processing.

## Common Mistakes

### Mistake 1: Ignoring Video Chapters

**Wrong:**
Always creating auto-generated 1-3 minute chapters even when video has chapter markers in description.

**Right:**
1. Check description for chapter timestamps first
2. If found, use those chapters and titles
3. Only generate chapters if none exist in description

### Mistake 2: Missing Structure Elements

**Wrong (no chapters):**
```html
<body>
    <h1>Video Title</h1>
    <p>All transcript text...</p>
</body>
```

**Right:**
```html
<body>
    <h1>Video Title</h1>
    <h2>0:00 - Introduction</h2>
    <p>Transcript text for this chapter...</p>
    <h2>2:30 - Next Topic</h2>
    <p>More content...</p>
</body>
```

### Mistake 3: Wrong Timestamp Format

**Wrong:**
```html
<h2>Introduction</h2>
<h2>0:00 Introduction</h2>
<h2>00:00:00.000 - Introduction</h2>
<h2>0:00 - 2:30 - Introduction</h2>
```

**Right:**
```html
<h2>0:00 - Introduction</h2>
```

### Mistake 4: Using Wrong Tool

**Wrong:**
```bash
webfetch https://www.youtube.com/watch?v=...
```

**Right:**
```bash
yt-dlp --write-auto-sub --sub-format vtt --skip-download URL
```

### Mistake 5: Poor Auto-Generated Chapter Titles

**Wrong (using first sentence verbatim):**
```html
<h2>0:00 - Can you break down the difference between capitalist, socialist, commu</h2>
```

**Right (concise summary):**
```html
<h2>0:00 - Economic Systems Overview</h2>
```

**Guidelines for auto-generated titles:**
- Summarize topic, don't copy first sentence
- 3-8 words, max 60 characters
- Be descriptive and informative

## Red Flags Checklist

If you catch yourself thinking:

- [ ] "Should I skip checking for video chapters?" → NO. Always check description first.
- [ ] "Should I skip the title?" → NO. Always include `<h1>` with video title.
- [ ] "Should I skip chapter headings?" → NO. Always create `<h2>` chapters.
- [ ] "Let me try WebFetch" → STOP. Use yt-dlp.
- [ ] "No transcript, let me try speech-to-text" → STOP. Abort cleanly.
- [ ] "Timestamps optional in chapter headings?" → NO. Always `MM:SS - Title`.
- [ ] "Should I create markdown?" → NO. Always HTML.

## Workflow Summary

```
1. User requests YouTube transcript
   ↓
2. Check transcript availability (yt-dlp --list-subs)
   ↓
3a. If unavailable → Abort with message
3b. If available → Continue
   ↓
4. Get video title and description
   ↓
5. Check description for chapter markers
   ↓
6a. Chapters found → Use those timestamps/titles
6b. No chapters → Generate 1-3 min sections
   ↓
7. Download transcript (VTT format)
   ↓
8. Process VTT: remove tags, extract timestamps, clean text
   ↓
9. Group content by chapters
   ↓
10. Create transcript.html:
    - <h1> with title
    - <h2> chapters with MM:SS - Title
    - <p> paragraphs under each chapter
   ↓
11. Clean up temporary files
```

## Complete Example

**Video with chapters in description:**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Understanding Economic Systems</title>
</head>
<body>

    <h1>Understanding Economic Systems</h1>

    <h2>0:00 - Introduction</h2>
    <p>Welcome to this video on economic systems. Today we'll explore the key differences...</p>

    <h2>2:30 - Capitalism Explained</h2>
    <p>Capitalism is a system where capital goes to those who can generate the best returns...</p>

    <h2>5:45 - Socialist Approaches</h2>
    <p>In socialist systems, the government plays a larger role in economic decisions...</p>

    <h2>8:20 - Conclusion</h2>
    <p>Each system has tradeoffs. Understanding these helps us make informed decisions...</p>

</body>
</html>
```

**Key features:**
1. UTF-8 charset for proper character encoding
2. H1 with video title
3. H2 chapters with `MM:SS - Title` format (from video's chapter markers)
4. Paragraphs grouped logically under chapters
5. Clean, semantic HTML structure

## Additional Resources

- **yt-dlp documentation:** <https://github.com/yt-dlp/yt-dlp>
- **VTT format specification:** <https://www.w3.org/TR/webvtt1/>
