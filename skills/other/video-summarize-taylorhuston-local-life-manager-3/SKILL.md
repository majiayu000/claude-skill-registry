---
name: video-summarize
description: Summarize a single YouTube video and create a note. Use when user shares a video URL or asks to summarize a specific video. Triggers on "summarize this video", "video summary", YouTube URLs.
allowed-tools: Bash, Read, Write, Edit, Glob
---

Summarize a single YouTube video and create a note in my-vault.

## Usage

```
/video-summarize <youtube-url> [folder]
```

- `youtube-url`: Full YouTube URL or video ID
- `folder` (optional): Subfolder under `Videos/` (e.g., "Atlassian", "Ali Abdaal"). If not specified, uses channel name.

## Workflow

1. **Extract video ID** from URL (supports youtube.com/watch?v=, youtu.be/, and bare IDs)

2. **Fetch video metadata** using the youtube-catchup helper script:
   ```bash
   python3 .claude/skills/youtube-catchup/scripts/youtube_helper.py full <video_id>
   ```

3. **Review the transcript** and create a summary with:
   - Bullet point summary of key concepts
   - "Why Watch?" section with recommendation

4. **Determine folder:**
   - Use provided folder if specified
   - Otherwise use channel name from metadata
   - Create folder if it doesn't exist

5. **Create note** at `my-vault/06 Knowledge Base/Capture/Videos/<folder>/<title>.md`

6. **Assign tags:**
   - Check `youtube-catchup/references/channels.json` for channel's default tags
   - If channel not in config, infer tags from the canonical list in `my-vault/09 System/Tag Index.md`

## Tagging

**Use tags from the canonical list in `my-vault/09 System/Tag Index.md`.**

Common channel → tag mappings are in `.claude/skills/youtube-catchup/references/channels.json`. If the channel exists there, use its `tags` array. Otherwise, infer appropriate tags based on content.

Format tags as: `tags: ["tag1", "tag2"]`

## Video Note Format

Use the exact template format:

```markdown
---
class: Video
media: https://www.youtube.com/watch?v=VIDEO_ID
publishDate: YYYY-MM-DD
status: Summarized
duration: Xm or Xh Ym
reviewFrequency:
lastReviewedDate:
review:
aliases:
tags: ["tag1", "tag2"]
cssclasses:
archived:
---
Related:

## Summary

- **Key point** - Details
- **Key point** - Details

## Why Watch?

<Brief recommendation on whether/why to watch, target audience, length note>
```

## Summary Guidelines

- Use bullet points with **bold key concepts**
- Adjust detail level based on video length:
  - < 5 min: 3-5 bullets
  - 5-15 min: 5-8 bullets
  - 15-30 min: 8-12 bullets
  - 30+ min: Use sections/headers, 12+ bullets
- Focus on actionable takeaways, not timestamps
- "Why Watch?" should help user decide if they need to actually watch it

## Duration Formatting

- Under 60 min: `Xm` (e.g., `23m`)
- 60+ min: `Xh Ym` (e.g., `1h 15m`)

## Title Sanitization

Remove or replace these characters for filenames:
- `:` → ` -`
- `/` → `-`
- `|` → `-`
- `?` → (remove)
- `"` → (remove)
- `<` `>` → (remove)

## Examples

```
/video-summarize https://www.youtube.com/watch?v=abc123
/video-summarize abc123 "Tech Talks"
/video-summarize https://youtu.be/xyz789 Atlassian
```

## Path Handling

**CRITICAL - Never escape spaces with backslashes:**
- Use paths exactly as shown: `my-vault/06 Knowledge Base/...` (with literal spaces)
- The Write tool handles spaces correctly - backslash escaping creates literal `\` characters in directory names
- When using Bash commands, wrap paths in double quotes: `"my-vault/06 Knowledge Base/..."`

## Notes

- Reuses `youtube_helper.py` from youtube-catchup skill (no duplicate code)
- If transcript unavailable, note this in the summary and summarize from description/title only
- Check if note already exists before creating (search by video ID in media field)
