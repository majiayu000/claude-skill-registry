---
name: anycrawl-tiktok-scraper
description: Extract public TikTok data from a single URL through the AnyCrawl Scrape API. Use when a user provides a TikTok video, profile, or hashtag URL and wants as much structured data as possible from that one link, including normalized JSON plus the raw AnyCrawl markdown, HTML, links, and screenshot artifacts.
---

# AnyCrawl TikTok Scraper

Use this skill when the user gives a public TikTok URL and wants a deep pull through AnyCrawl.

## Workflow

1. Accept a single public TikTok URL.
2. Validate that it is one of the supported shapes:
   - `https://www.tiktok.com/@USER/video/VIDEO_ID`
   - `https://www.tiktok.com/@USER`
   - `https://www.tiktok.com/tag/TAG_NAME`
3. Run the bundled extractor:

```bash
node .claude/skills/anycrawl-tiktok-scraper/scripts/run.js "<tiktok-url>"
```

4. Read the JSON file path printed by the script.
5. Summarize the important fields for the user:
   - page type
   - author/profile info
   - caption/title text
   - engagement stats
   - hashtags
   - screenshot URL
   - anything missing or clearly blocked by the source page

## Output Handling

The script writes a full JSON artifact to `/tmp` by default and prints a compact summary to stdout.

The artifact includes:

- `normalized`: structured TikTok-focused extraction
- `anycrawl`: raw AnyCrawl response, including `markdown`, `html`, `links`, and `screenshot@fullPage` when available
- `request`: the exact payload used for the successful attempt

## Retry Guidance

The script already retries with a slower Playwright configuration when the first pass is thin or fails.

Only retry manually when:

- the URL is public but the result is clearly sparse
- TikTok served a login wall or unusual consent page
- the user asks for another URL shape after the first run

If you need the official field coverage or template notes, read [references/template-notes.md](.claude/skills/anycrawl-tiktok-scraper/references/template-notes.md).
