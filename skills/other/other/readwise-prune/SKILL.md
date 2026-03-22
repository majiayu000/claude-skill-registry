---
name: readwise-prune
description: Clean up stale Readwise Reader documents. Use when the user wants to declutter their reading library, remove old unread articles, or manage Reader inbox. Triggers on "clean up readwise", "prune reader", "delete old articles", "declutter reading list".
context: fork
agent: librarian
user-invocable: false
---

# Readwise Reader Prune

Two-pass stale document removal with safe defaults.

<EXTREMELY-IMPORTANT>

## IRON LAW: Dry Run First

**NEVER pass `--delete` without showing the user the dry-run output first.**

1. Run without `--delete` (dry run)
2. Show the user the candidate list and category breakdown
3. Get explicit confirmation
4. THEN run with `--delete`

</EXTREMELY-IMPORTANT>

## How It Works

**Pass 1:** Fetch all documents updated in the last N months (the "safe set" -- these have recent activity and are never pruned).

**Pass 2:** Fetch all documents matching filters. Remove from candidates any document that:
- Is in the safe set (recently active)
- Has highlights (num_highlights > 0)
- Has an excluded tag

## Commands

```bash
# Dry run (always do this first)
readwise-custom prune
readwise-custom prune --months 6
readwise-custom prune --category rss --location new
readwise-custom prune --exclude-tag "keep" --exclude-tag "reference"

# Limit candidates shown
readwise-custom prune --months 3 --limit 20

# JSON output (for review)
readwise-custom prune --months 6 --json

# Actually delete (after reviewing dry run)
readwise-custom prune --months 3 --delete
readwise-custom prune --category rss --months 1 --delete
```

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--months <n>` | 3 | Documents inactive for this many months are candidates |
| `--location <loc>` | all | Filter: new, later, shortlist, archive, feed |
| `--category <cat>` | all | Filter: article, email, rss, pdf, epub, tweet, video |
| `--exclude-tag <tag>` | none | Skip documents with this tag (repeatable) |
| `--limit <n>` | all | Cap number of candidates |
| `--delete` | false | Actually delete (default is dry run) |
| `--json` | false | Output as JSON |

## Recommended Workflows

### Weekly RSS cleanup
```bash
readwise-custom prune --category rss --months 1 --location new
# Review, then:
readwise-custom prune --category rss --months 1 --location new --delete
```

### Quarterly deep clean
```bash
readwise-custom prune --months 6 --exclude-tag "reference"
# Review, then:
readwise-custom prune --months 6 --exclude-tag "reference" --delete
```
