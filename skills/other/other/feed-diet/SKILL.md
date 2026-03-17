---
name: feed-diet
version: 0.1.2
description: Audit your information diet across HN and RSS feeds — beautiful reports with category breakdowns, ASCII charts, and personalized recommendations.
author: Anvil AI
tags: [productivity, reading, analysis, hacker-news, rss, information-diet, discord, discord-v2]
---

# 🍽️ Feed Diet

Audit your information diet and get a gorgeous report showing what you actually consume.

## Trigger

Activate when the user mentions any of:
- "feed diet"
- "information diet"
- "audit my feeds"
- "what am I reading"
- "analyze my HN"
- "reading habits"
- "content diet"
- "feed report"

## Instructions

### Audit Mode (default)

1. **Determine the data source.** Ask the user for one of:
   - A **Hacker News username** (e.g., "tosh")
   - An **OPML file** path containing RSS feed subscriptions

2. **Fetch the content.** Run the appropriate fetch script:
   ```bash
   # For HN:
   bash "$SKILL_DIR/scripts/hn-fetch.sh" USERNAME 100
   
   # For OPML:
   bash "$SKILL_DIR/scripts/opml-parse.sh" /path/to/feeds.opml
   ```

3. **Classify items.** Pipe the fetched items through the classifier:
   ```bash
   cat items.jsonl | bash "$SKILL_DIR/scripts/classify.sh" > classified.jsonl
   ```
   The classifier uses LLM (if ANTHROPIC_API_KEY or OPENAI_API_KEY is set) or falls back to keyword matching.

4. **Generate the report.** Run the main entry point:
   ```bash
   bash "$SKILL_DIR/scripts/feed-diet.sh" audit --hn USERNAME --limit 100
   ```

5. **Present the report** to the user. The output is Markdown — render it directly.

### Digest Mode (weekly curated reading)

When the user wants a filtered reading list based on their goals:

```bash
bash "$SKILL_DIR/scripts/feed-diet.sh" digest --hn USERNAME --goal "systems programming, distributed systems" --days 7
```

### Quick Reference

| Command | Description |
|---------|-------------|
| `feed-diet audit --hn USER` | Full diet audit for an HN user |
| `feed-diet audit --opml FILE` | Full diet audit from RSS feeds |
| `feed-diet digest --hn USER --goal "X"` | Weekly digest filtered by goals |

### Notes for the Agent

- **Be conversational.** After presenting the report, offer observations like "Looks like you're heavy on news — want me to suggest some deeper technical feeds?"
- **Suggest the digest mode** if the user seems interested in filtering their reading.
- **The report is the star.** Don't summarize it — present it in full. It's designed to be screenshot-worthy.
- If classification seems off, mention that setting an LLM API key improves accuracy.

### Discord v2 Delivery Mode (OpenClaw v2026.2.14+)

When the conversation is happening in a Discord channel:

- Send a compact first summary (top category, diversity score, top 2 recommendations), then ask if the user wants the full report.
- Keep the first response under ~1200 characters and avoid wide category tables in the first message.
- If Discord components are available, include quick actions:
  - `Show Full Diet Report`
  - `Generate Weekly Digest`
  - `Show Recommendations`
- If components are not available, provide the same follow-ups as a numbered list.
- Prefer short follow-up chunks (<=15 lines per message) when sharing long reports.

## References

- `scripts/feed-diet.sh` — Main entry point
- `scripts/hn-fetch.sh` — Hacker News story fetcher
- `scripts/opml-parse.sh` — OPML/RSS feed parser
- `scripts/classify.sh` — Batch content classifier (LLM + fallback)
- `scripts/common.sh` — Shared utilities and formatting

## Examples

### Example 1: HN Audit

**User:** "Audit my HN reading diet — my username is tosh"

**Agent runs:**
```bash
bash "$SKILL_DIR/scripts/feed-diet.sh" audit --hn tosh --limit 50
```

**Output:** A full Markdown report with category breakdown table, top categories with sample items, surprising finds, and recommendations.

### Example 2: Weekly Digest

**User:** "Give me a digest of what's relevant to my work on compilers and programming languages"

**Agent runs:**
```bash
bash "$SKILL_DIR/scripts/feed-diet.sh" digest --hn tosh --goal "compilers, programming languages, parsers" --days 7
```

**Output:** A curated reading list of 10-20 items ranked by relevance to the user's goals.

### Example 3: RSS Feed Audit

**User:** "Here's my OPML file, tell me what my feed diet looks like"

**Agent runs:**
```bash
bash "$SKILL_DIR/scripts/feed-diet.sh" audit --opml /path/to/feeds.opml
```
