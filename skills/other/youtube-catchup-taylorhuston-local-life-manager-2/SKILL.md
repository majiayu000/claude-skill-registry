---
name: youtube-catchup
description: Fetch and summarize latest videos from priority YouTube channels. Creates notes with transcripts summarized as bullet points. Use to catch up on subscriptions without watching everything. Triggers on "youtube catchup", "video catchup", "check youtube", "summarize videos".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
---

Catch up on YouTube channels by auto-summarizing new videos.

## Architecture

This skill uses a **coordinator + subagent** pattern:
- **Coordinator (Sonnet)**: Fetches video lists, filters new videos, spawns summarization agents, updates state
- **Summarizer (Haiku subagents)**: Each video gets its own agent with fresh context to ensure quality

## Prerequisites

Requires `yt-dlp`:
```bash
pip install yt-dlp
```

## Helper Script

Use `scripts/youtube_helper.py` for fetching data:

```bash
# Get NEW videos uploaded since a date (default operation)
python3 scripts/youtube_helper.py new @handle YYYY-MM-DD [processed_ids]

# Backfill: get all unprocessed videos regardless of date (explicit request only)
python3 scripts/youtube_helper.py backfill @handle [limit] [processed_ids]

# Fast channel list (no date info - rarely needed)
python3 scripts/youtube_helper.py channel @handle [limit]

# Get video metadata
python3 scripts/youtube_helper.py video VIDEO_ID

# Get transcript only
python3 scripts/youtube_helper.py transcript VIDEO_ID

# Get metadata + transcript (for summarization)
python3 scripts/youtube_helper.py full VIDEO_ID
```

**Important:** The `new` command checks upload dates to avoid backfilling old content. Use `backfill` only when explicitly requested.

## Workflow

### Phase 1: Discovery (Coordinator)

1. **Load configuration**
   - Read channel list from `references/channels.json`
   - Read processed videos list from `references/state.json`
   - Note the `last_run` date for filtering

2. **For each enabled channel:**
   - Run: `python3 scripts/youtube_helper.py new @handle {last_run} {processed_ids}`
   - This returns ONLY videos uploaded since `last_run` that aren't in processed list
   - **Skip videos under 5 minutes** (likely promotional/announcement fluff)
   - Collect list of new videos needing summarization

3. **Deduplicate against existing notes:**
   - Before processing, check if a note with that video URL already exists:
     ```bash
     grep -rl "youtube.com/watch?v={video_id}" "my-vault/07 Knowledge Base/Capture/Videos/"
     ```
   - If a note exists: skip that video (already processed, just missing from state)
   - This prevents duplicates even if state.json is out of sync

4. **Report findings to user:**
   - Show count of new videos per channel
   - Ask user how to proceed (all, select channels, limit count)

**Backfill mode:** If user explicitly requests backfilling old videos, use `backfill` command instead of `new`.

### Phase 2: Summarization (Haiku Subagents)

5. **Spawn subagents for summarization:**
   - Use Task tool with `model: haiku` and `subagent_type: general-purpose`
   - Process 4-6 videos in parallel (multiple Task calls in single message)
   - Each subagent handles ONE video with fresh context
   - Wait for batch to complete before starting next batch

6. **Subagent prompt template:**
```
Summarize this YouTube video and create a note.

VIDEO_ID: {video_id}
CHANNEL: {channel_name}
TAGS: {tags}
OUTPUT_PATH: {output_path}

IMPORTANT: Use the OUTPUT_PATH exactly as given with literal spaces (e.g., "my-vault/07 Knowledge Base/...").
Do NOT escape spaces with backslashes - this creates directories with literal backslash characters in the name.

STEPS:
1. Run: cd /home/taylor/my-life/.claude/skills/youtube-catchup && python3 scripts/youtube_helper.py full {video_id}
2. If NO_TRANSCRIPT_AVAILABLE, create note with that notice (see format below)
3. Otherwise, summarize the transcript into detailed bullet points
4. Identify any discoveries (tools, products, frameworks worth exploring)
5. Write the note file to the output path
6. Return: SUCCESS or FAILURE with brief reason

SUMMARY GUIDELINES:
- 5-15 bullet points depending on video length/density
- Each bullet should capture a complete idea with specific details
- Include names, numbers, tools, key arguments mentioned
- For tutorials: use step-by-step format with code snippets

NO TRANSCRIPT FORMAT:
## Summary

NO TRANSCRIPT AVAILABLE - REWATCH VIDEO TO CREATE PROPER SUMMARY

- Main topic: {title}

NOTE TEMPLATE:
---
class: Video
aliases:
tags: {tags}
lastReviewedDate:
reviewFrequency:
review:
created: {date}
modified: {date}
media: https://www.youtube.com/watch?v={video_id}
publishDate: {publish_date}
status: Summarized
duration: {duration}
cssclasses:
archived:
---
Related:

## Summary

- Main topic: [one sentence]
- [Key points with specific details...]

## Discoveries

- [[Product Name]] - brief context
- (or "None")

## Why Watch?

[One sentence on whether worth actually watching]
```

### Phase 3: Completion (Coordinator)

7. **Collect results:**
   - Track which videos succeeded/failed
   - Report any failures to user

8. **Update state:**
   - Add successfully processed video IDs to `references/state.json`
   - Report summary of what was processed

## Tagging

**Use tags from the canonical list in `my-vault/09 System/Tag Index.md`.**

Each channel in `references/channels.json` has a `tags` array specifying default tags. Format: `tags: ["tag1", "tag2"]`

## Output Paths

Video notes: `my-vault/07 Knowledge Base/Capture/Videos/{channel_folder}/{title}.md`
Discovery notes: `my-vault/01 Inbox/{name}.md`

**CRITICAL - Path Handling:**
- **NEVER escape spaces with backslashes** in paths passed to subagents or the Write tool
- Use paths exactly as shown: `my-vault/07 Knowledge Base/...` (with literal spaces)
- The Write tool handles spaces correctly - backslash escaping creates literal `\` characters in directory names
- When using Bash commands, wrap paths in double quotes: `"my-vault/07 Knowledge Base/..."`

## Channel Config

Edit `references/channels.json`:
```json
{
  "channels": [
    {
      "name": "Channel Name",
      "handle": "@YouTubeHandle",
      "folder": "Folder Name",
      "tags": ["tag1", "tag2"],
      "priority": "high",
      "enabled": true
    }
  ]
}
```

## Tutorial Videos - Special Handling

If the video is a tutorial, the subagent should use step-by-step format:

```markdown
## Summary

Tutorial: [What you'll build/learn]

### Prerequisites
- Required software/tools
- Prior knowledge needed

### Steps

#### 1. [First major step]
- Specific action
- Code snippet if applicable
- Expected result

#### 2. [Continue for all steps...]

### Final Result
- What you should have
- How to verify it works

### Troubleshooting
- Common issues and solutions
```

**Tutorial goals:** Someone should be able to follow WITHOUT watching the video.

## Discovery Notes

Subagents should identify products, services, frameworks, tools worth exploring.

**Create notes for:** New tools, interesting frameworks, notable projects
**Skip:** Well-known things (Python, AWS, React), generic concepts

Discovery note format:
```markdown
---
class: Note
tags: ["tag1"]
---
Related: [[Video Title]]

## What is it?
[One sentence description]

## Why look into it?
[Why it seemed interesting]

## Links
- [URL if mentioned]
```

## Error Handling

- If subagent fails, log the video ID and continue with others
- If transcript unavailable, create note with NO TRANSCRIPT notice
- Report all failures at the end for manual review

## Example Coordinator Flow

```
1. Load channels.json, state.json (last_run: 2026-01-16)
2. Fetch NEW videos (uploaded since last_run):
   python3 youtube_helper.py new @t3dotgg 2026-01-16 id1,id2,...
   - Theo: 2 new videos
   - HealthyGamerGG: 1 new video
   - LangChain: 0 new videos
3. User confirms: "Process all"
4. Batch 1 - spawn 3 Haiku agents:
   - Task(video_1, theo, ...)
   - Task(video_2, theo, ...)
   - Task(video_3, healthygamer, ...)
5. Wait for batch completion
6. Update state.json with successful IDs
7. Update last_run to today's date
8. Report: "Processed 3 videos, 0 failures"
```

**For explicit backfill:**
```
User: "backfill Gamers Nexus videos"
1. Use: python3 youtube_helper.py backfill @GamersNexus 50 id1,id2,...
2. This returns ALL unprocessed videos regardless of upload date
3. Proceed with normal summarization workflow
```
