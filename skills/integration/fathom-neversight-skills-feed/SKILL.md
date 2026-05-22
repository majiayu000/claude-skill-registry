---
name: fathom
description: Fetch meetings, transcripts, summaries, and action items from Fathom API. Use when user asks to get Fathom recordings, sync meeting transcripts, or fetch recent calls.
---

# Fathom Meeting Fetcher

Fetches meeting data directly from Fathom API including transcripts, AI summaries, action items, and participant info.

## Usage

```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `--list` | List recent meetings with IDs |
| `--id <id>` | Fetch specific meeting by recording ID |
| `--today` | Fetch all meetings from today |
| `--since <date>` | Fetch meetings since date (YYYY-MM-DD) |

### Options

| Option | Description |
|--------|-------------|
| `--analyze` | Run transcript-analyzer on fetched meetings |
| `--download-video` | Download video recording (requires ffmpeg) |
| `--output <path>` | Output directory (default: ~/Brains/brain) |
| `--limit <n>` | Max meetings to list (default: 10) |

## Examples

### List recent meetings
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --list
```

### Fetch today's meetings
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --today
```

### Fetch and analyze
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --today --analyze
```

### Fetch since date
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --since 2025-01-01
```

### Fetch specific meeting
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --id abc123def456
```

### Download video with meeting
```bash
python3 ~/.claude/skills/fathom/scripts/fetch.py --id abc123def456 --download-video
```

## Output Format

Each meeting is saved as markdown with:

```markdown
---
fathom_id: <id>
title: "Meeting Title"
date: YYYY-MM-DD
participants: [list]
duration: HH:MM
fathom_url: <url>
share_url: <url>
---

# Meeting Title

## Summary
{AI-generated summary from Fathom}

## Action Items
- [ ] Item 1 (@assignee)
- [ ] Item 2

## Transcript
**Speaker Name**: What they said...
```

## File Naming

Files are saved as: `YYYYMMDD-meeting-title-slug.md`

Example: `20250106-weekly-standup.md`

## Prerequisites

Install dependencies (first time):
```bash
pip install requests python-dotenv
```

For video download (optional):
```bash
# ffmpeg required for video downloads
brew install ffmpeg  # macOS
# or apt install ffmpeg (Linux)
```

## Configuration

API key stored in `~/.claude/skills/fathom/scripts/.env`:
```
FATHOM_API_KEY=your-api-key
```

## Integration

- **transcript-analyzer**: Use `--analyze` flag to automatically process transcripts
- **video-downloader**: Use `--download-video` flag to download meeting recordings
  - Validates downloaded videos using ffprobe
  - Automatically retries up to 3 times if download fails
  - Videos saved as .mp4 next to meeting markdown files
- Replaces Dropbox sync workflow (direct API access)
