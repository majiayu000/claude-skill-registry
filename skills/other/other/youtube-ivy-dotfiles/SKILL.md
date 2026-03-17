---
name: youtube
description: Fetch and structure the transcript from this YouTube video.
argument-hint: [url | video-id]
context: fork
{{- template "bedrock-model" (dict "tier" "sonnet" "root" .) }}
allowed-tools:
  - Bash(yt-dlp:*)
  - Bash(mkdir -p tmp:*)
  - Bash(rm tmp/transcript*:*)
  - Read
  - Task
---

# YouTube Transcript to Structured Notes

## Arguments

```
$ARGUMENTS
```

## Instructions

This workflow fetches a YouTube video transcript and transforms it into a structured, skimmable reference document. Uses a forked context since the transcript processing doesn't need to inform follow-up conversation.

### 1. Parse Video Input

- **Full URL**: Use directly (supports youtube.com, youtu.be)
- **Video ID**: Construct `https://youtube.com/watch?v={id}`
- **If missing**: Ask for the video URL

### 2. Fetch Video Metadata

```bash
yt-dlp --print "%(title)s" --print "%(channel)s" --print "%(uploader)s" --print "%(upload_date)s" --print "%(duration)s" --skip-download "VIDEO_URL"
```

Capture:
- **Title** — for filename and frontmatter
- **Channel/Uploader** — for attribution (use uploader if personal, channel if organizational)
- **Upload Date** — format as YYYY-MM-DD
- **Duration** — for context

### 3. Download Transcript

```bash
mkdir -p tmp
yt-dlp --skip-download --write-auto-subs --sub-langs "en" --sub-format "srt" --convert-subs srt -o "tmp/transcript" "VIDEO_URL"
```

Saves to `tmp/transcript.en.srt`. If no English subs, try `en-orig` or check `--list-subs`.

### 4. Determine Output Filename

Use **APA-style title capitalization** with creator:

**Format:** `Reference/Full Title Here (Creator Name).md`

**APA rules:**
- Capitalize first word and all major words
- Capitalize words of 4+ letters
- Lowercase: a, an, the, and, but, or, for, nor, on, at, to, by (unless first)

**Examples:**
- `No Vibes Allowed - Solving Hard Problems in Complex Codebases (Dex Horthy).md`
- `The Art of Doing Science and Engineering (Richard Hamming).md`

### 5. Spawn Processing Agent

**CRITICAL:** Do NOT read the transcript yourself. Use Task tool with `subagent_type: general-purpose`:

```
## Task: Convert Video Transcript to Structured Written Document

**Input file:** `tmp/transcript.en.srt`

**Video Metadata:**
- Title: [VIDEO TITLE]
- Speaker/Creator: [CREATOR NAME]
- Channel: [CHANNEL NAME]
- Upload Date: [YYYY-MM-DD]
- URL: [VIDEO URL]
- Duration: [DURATION]

## Your Mission

Transform this SRT transcript into a **structured written document** optimized for speed-reading and reference.

## Key Principles

1. **Structure, don't summarize.** Convert spoken word to written form — don't condense. The human brain can skim structured text far faster than watching video.

2. **Preserve density.** Don't pad with filler, but don't cut substantive points. If the speaker made a point, include it.

3. **Use document structure liberally:**
   - Clear hierarchical headings (H2, H3, H4)
   - Blockquotes for key quotes or memorable phrasings
   - Bullet lists for enumerations
   - Code blocks for technical examples
   - Bold for key terms/concepts
   - Horizontal rules between major sections

4. **Write for skimmability.** Someone should get the gist from headings alone, then dive deeper as needed.

## Output Format

Write to: `Reference/[FILENAME].md`

Start with YAML frontmatter:
```yaml
---
title: "[Full Video Title]"
speaker: [Speaker/Creator Name]
organization: [Organization if applicable, omit if none]
event: [Event name if applicable, omit if none]
date: YYYY-MM-DD
source: [VIDEO URL]
type: talk-notes
tags:
  - [relevant-tag-1]
  - [relevant-tag-2]
  - [add 2-4 more based on content]
---
```

After frontmatter, include attribution:
*Video by [Creator]. [Watch the original](URL).*

## Quality Checklist

Before finishing, verify:
- [ ] All substantive points from the talk are represented
- [ ] Headings create a scannable outline
- [ ] Key quotes preserved as blockquotes
- [ ] Technical terms properly formatted
- [ ] Reads as coherent written piece (not transcript-like)
- [ ] Someone could understand the content without watching
```

### 6. Clean Up

After agent completes:

```bash
rm tmp/transcript.en.srt
```

### 7. Confirm to User

Report:
1. Where the file was saved (full path)
2. Brief summary of what was captured (major sections, tags used)

## Troubleshooting

**No subtitles:** Try `--write-auto-subs` with different language codes, or `--list-subs`

**Garbled transcript:** Note quality issues in output if auto-generated captions are poor

**Very long video (1+ hours):** Task agent handles it; may benefit from more aggressive sectioning

## Examples

```
/youtube https://www.youtube.com/watch?v=abc123
/youtube youtu.be/abc123
/youtube abc123
```
