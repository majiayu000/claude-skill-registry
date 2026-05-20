---
name: anycrawl-social-extractor
description: Route a public social-media URL to the correct AnyCrawl skill and extractor automatically. Use when a user provides a TikTok, Instagram, or YouTube link and wants one skill that detects the platform, runs the right AnyCrawl-backed extractor, and returns the saved artifact path plus a compact execution summary.
---

# AnyCrawl Social Extractor

Use this skill when the user gives a social URL and does not want to choose between the TikTok, Instagram, or YouTube skills manually.

## Workflow

1. Accept a single public URL.
2. Run the router:

```bash
node .claude/skills/anycrawl-social-extractor/scripts/run.js "<social-url>"
```

3. Read the compact JSON summary from stdout.
4. Open the saved artifact file if the user needs the full extraction.
5. Summarize the meaningful fields for the user instead of dumping raw HTML into the chat.

## Routing Rules

- TikTok URLs route to `anycrawl-tiktok-scraper`
- Instagram URLs route to `anycrawl-instagram-scraper`
- YouTube watch or `youtu.be` URLs route to `anycrawl-youtube-video-extractor`

If the URL is not one of those platforms, fail fast and tell the user it is unsupported.

## Output Handling

The router does not scrape directly. It delegates to the platform-specific canonical extractor and returns:

- `platform`
- `routedSkill`
- `runnerScript`
- `outputPath`
- the delegated script's summary fields

Read [references/router-notes.md](.claude/skills/anycrawl-social-extractor/references/router-notes.md) if you need the exact platform mappings.
