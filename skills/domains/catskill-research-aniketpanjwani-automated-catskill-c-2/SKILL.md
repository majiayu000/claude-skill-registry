---
name: catskill-research
description: Research events and conditions data for Catskill Crew newsletter. Use when gathering Instagram events, fetching sun/moon/weather data, or preparing data for newsletter writing.
---

<essential_principles>
## How This Skill Works

This skill gathers raw data for the Catskill Crew newsletter. It does NOT write newsletter content - use `catskill-writer` for that.

### Data Types

1. **Events** - From Instagram venues/promoters via ScrapeCreators API
2. **Conditions** - Sun, moon, air quality, fire danger via Firecrawl scraping

### Output

Research produces structured data saved to `tmp/` for the writer skill to consume:
- `tmp/extraction/event_candidates.json` - Parsed events
- `tmp/extraction/images/<handle>/` - Downloaded flyer images
- `tmp/conditions/` - Conditions data (optional)

### Key Principle

**Images are critical.** Many venues post event details only in flyer images, not captions. Always analyze downloaded images with Claude's vision.
</essential_principles>

<intake>
What would you like to research?

1. **Events** - Scrape Instagram venues for upcoming events
2. **Conditions** - Fetch sun/moon/air/fire data
3. **Both** - Full research for a newsletter edition

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "events", "instagram" | `workflows/research-events.md` |
| 2, "conditions", "weather", "sun", "moon" | `workflows/research-conditions.md` |
| 3, "both", "full", "newsletter" | Run both workflows sequentially |
</routing>

<reference_index>
All domain knowledge in `references/`:

**Instagram:** instagram-api.md, instagram-sources.md
**Conditions:** conditions-sources.md
**Data Models:** event-schema.md
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| research-events.md | Scrape Instagram, download images, extract events |
| research-conditions.md | Fetch sun/moon/air/fire from free sources |
</workflows_index>

<success_criteria>
Research is complete when:
- Event candidates saved to `tmp/extraction/event_candidates.json`
- All flyer images downloaded and analyzed
- Conditions data fetched and parsed
- Data is ready for `catskill-writer` skill
</success_criteria>
