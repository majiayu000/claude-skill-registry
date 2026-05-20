---
name: harvest-monitor
description: Web change monitoring - track changes on pages, detect updates, changelog diffs
allowed-tools: [Bash, Read, Write, WebFetch, Grep]
keywords: [monitor, watch, changes, diff, changelog, update, track, compare]
---

# Harvest Monitor

Track changes on web pages over time. Compare current content against cached versions to detect updates, new releases, breaking changes, and documentation modifications.

## Usage

```bash
# Monitor a page for changes
/harvest-monitor https://docs.example.com/changelog

# Compare against last cached version
/harvest-monitor https://docs.example.com/api --diff

# Track multiple pages
/harvest-monitor --watchlist ~/.claude/cache/agents/harvest/watchlist.json
```

## How It Works

1. Fetch current page content
2. Check cache for previous version
3. Compute diff (content-level, not HTML-level)
4. Categorize changes (added, removed, modified)
5. Report significant changes
6. Update cache with current version

## Output

```markdown
# Change Report: [URL]
> Checked: [timestamp]
> Previous: [cached timestamp]
> Status: CHANGED / NO CHANGE

## Changes Detected
### Added
- [New content]

### Modified
- [Changed content - before → after]

### Removed
- [Removed content]

## Impact Assessment
[What these changes mean for our project]
```

## Watchlist Format

```json
{
  "pages": [
    {
      "url": "https://docs.example.com/changelog",
      "frequency": "daily",
      "notify": ["migrator", "shipper"]
    }
  ]
}
```

## Integration

- **migrator**: Track dependency changelogs for breaking changes
- **shipper**: Monitor deployment status pages
- **tech-radar**: Track technology evolution

## Rules

- Cache previous versions locally
- Content-level diff, not HTML diff
- Ignore style/layout changes
- Only report meaningful content changes
- Max 1 check per hour per URL
