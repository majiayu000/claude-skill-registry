---
name: blunder-backfill
description: Re-annotate recent games with outdated or missing blunder analysis. Use when users ask to backfill or refresh blunder annotations.
---

# Blunder Backfill

Re-annotate games that have outdated or missing blunder analysis.

Run the backfill script on the most recent N outdated games (default 10):

```bash
uv run --project puppeteer python scripts/analysis/toolbox/backfill_annotations.py [N]
```

The script:

- Finds games with `blunderScriptVersion` older than current (or missing annotations)
- Processes them most-recent-first
- Runs full per-decision Sonnet 4.5 analysis on each
- Prints a cost breakdown per game

Requires `OPENROUTER_API_KEY` environment variable.

If the user specifies a number, pass it as the argument. Otherwise use the default (10).
