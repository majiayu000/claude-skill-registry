---
name: newsletter-events-research
description: Research events from Instagram, web aggregators, and Facebook event URLs. Use when scraping event sources, downloading flyer images, or extracting event details.
---

<essential_principles>
## How This Skill Works

This skill gathers raw event data from configured sources. It does NOT write newsletter content - use `newsletter-events-write` for that.

### Data Sources

1. **Instagram** - Via ScrapeCreators API (requires API key)
2. **Web Aggregators** - Via Firecrawl (requires API key)
3. **Facebook Events** - Pass event URLs directly (e.g., `https://facebook.com/events/123456`)

### Output

Research produces structured data saved to `~/.config/local-media-tools/data/`:
- `data/raw/instagram_<handle>.json` - Raw API responses
- `data/images/instagram/<handle>/` - Downloaded flyer images
- `data/events.db` - SQLite database with profiles, posts, events, venues

### Key Principle

**Images are critical.** Many venues post event details only in flyer images, not captions. Always analyze downloaded images with Claude's vision.

**Image Download Requirement:** Instagram CDN URLs return 403 when accessed via WebFetch. Images MUST be downloaded using Python's `requests` library with proper User-Agent headers, then analyzed locally using the Read tool.
</essential_principles>

<critical>
## Use CLI Tools - Never curl

**NEVER use curl or raw API calls.** Always use the CLI tools provided:

**Instagram:**
```bash
# Scrape all configured accounts
uv run python scripts/cli_instagram.py scrape --all

# Scrape specific account
uv run python scripts/cli_instagram.py scrape --handle wayside_cider

# List posts from database
uv run python scripts/cli_instagram.py list-posts --handle wayside_cider

# Show database statistics
uv run python scripts/cli_instagram.py show-stats

# Classify posts (single or batch)
uv run python scripts/cli_instagram.py classify --post-id 123 --classification event --reason "Has future date"
uv run python scripts/cli_instagram.py classify --batch-json '[{"post_id": "123", "classification": "event", "reason": "..."}]'
```

The CLI tools ensure:
- Correct API parameters (`handle`, not `username`)
- Rate limiting (2 calls/second)
- Automatic retry on 429/5xx errors
- Proper database storage with FK relationships
- Raw responses saved to `~/.config/local-media-tools/data/raw/`

**Do NOT:**
- Use `curl` to call ScrapeCreators API directly
- Write raw SQL to insert data
- Guess API parameter names
</critical>

<intake>
What would you like to research?

1. **Instagram** - Scrape Instagram accounts for events
2. **Web Aggregators** - Scrape web event aggregator sites
3. **All configured sources** - Full research from all sources in config
4. **Facebook event URLs** - Pass specific event URLs to scrape

You can also paste Facebook event URLs directly:
- `https://facebook.com/events/123456`
- `https://facebook.com/events/789012`

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "instagram", "ig" | `workflows/research-instagram.md` |
| 2, "web", "aggregator", "websites" | `workflows/research-web-aggregator.md` |
| 3, "all", "both", "full" | `workflows/research-all.md` |
| 4, "facebook", contains `facebook.com/events/` | `workflows/research-facebook.md` |
</routing>

<reference_index>
All domain knowledge in `references/`:

**APIs:** scrapecreators-api.md, facebook-scraper-api.md, firecrawl-api.md
**Detection:** event-detection.md
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| research-instagram.md | Scrape Instagram, download images, extract events |
| research-facebook.md | Scrape individual Facebook event URLs |
| research-web-aggregator.md | Dispatcher for web scraping (calls scrape + extract) |
| research-web-scrape.md | Phase 1: Scrape pages, return JSON |
| research-web-extract.md | Phase 2: Extract events from JSON, save via CLI |
| research-all.md | Run all research workflows |
</workflows_index>

<success_criteria>
Research is complete when:
- [ ] CLI tool used to scrape accounts (not curl)
- [ ] Raw data saved to `~/.config/local-media-tools/data/raw/`
- [ ] Posts saved to database with profiles
- [ ] Posts classified as event/not_event/ambiguous
- [ ] Events extracted from classified posts
- [ ] Data ready for `newsletter-events-write` skill
</success_criteria>
