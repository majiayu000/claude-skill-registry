---
name: nzbget
description: Check NZBGet download status and queue information. Use when the user asks about NZBGet downloads, wants to know how many things are downloading, check download speed, view the queue, or get a full status report of their Usenet downloads.
---

# NZBGet Status Checker

This skill provides quick access to NZBGet download status and queue information.  Required env vars: NZBGET_USER, NZBGET_PASS, NZBGET_HOST

## Usage

### Quick Count
Get a simple count of active downloads:
```bash
bash scripts/check_nzbget.sh count
```
Returns: `3` (number of items downloading)

### Full Status Report
Get complete status with speed, queue, and remaining size:
```bash
bash scripts/check_nzbget.sh
```

### Specific Queries

| Query | Command | Output |
|-------|---------|--------|
| How many downloading? | `count` | Number only |
| Current speed? | `speed` | Speed in MB/s |
| What's in queue? | `queue` | First 10 items only |
| Full status | (no args) | Complete report (max 10 items shown) |

**Note:** Queue listings are capped at 10 items to avoid flooding with large queues (400+ items). The script shows "Next 10 of X items" when there are more.

## Examples

**User:** "NZBGet count"
```
3
```

**User:** "What's downloading?"
```
📥 NZBGet Status: Downloading

Active Downloads: 3
Speed: 12.5 MB/s
Remaining: 45.2 GB

Current Queue:
  • Movie.2025.2160p.mkv - 67%
  • TV.Show.S01E05.1080p.mkv - 23%
  • Documentary.4K.mkv - 89%
```

**User:** "NZBGet speed"
```
12.5 MB/s
```

## Response Guidelines

- For "count" or "how many": Use the number directly in a conversational response
- For "speed": Report the current download speed
- For full status: Summarize the key info (count, speed, remaining) and list active items
- If NZBGet is unreachable or no items downloading, say so clearly
- Keep responses concise unless user asks for full details
