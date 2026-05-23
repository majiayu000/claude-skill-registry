---
name: hackernews
description: Browse and search Hacker News. Fetch top, new, best, Ask HN, Show HN stories and job postings. View item details, comments, and user profiles. Search stories and comments via Algolia. Find "Who is hiring?" threads. Use for any HN-related queries like "what's trending on HN?", "search HN for AI", "show comments on story X", "who is hiring?", "latest Ask HN posts".
---

# Hacker News

CLI tool for the Hacker News API. No authentication required.

## CLI Usage

Run `scripts/hn.sh <command>`. All commands support `--json` for raw JSON output.

### Browse Stories

```bash
# Top/trending stories (default 10)
scripts/hn.sh top
scripts/hn.sh top --limit 20

# Other lists
scripts/hn.sh new --limit 5     # newest
scripts/hn.sh best --limit 10   # highest rated
scripts/hn.sh ask                # Ask HN
scripts/hn.sh show               # Show HN
scripts/hn.sh jobs               # job postings
```

### View Item Details & Comments

```bash
# Full item details (story, comment, job, poll)
scripts/hn.sh item 12345678

# Top comments on a story
scripts/hn.sh comments 12345678
scripts/hn.sh comments 12345678 --limit 10 --depth 2
```

### User Profiles

```bash
scripts/hn.sh user dang
```

### Search

```bash
# Basic search
scripts/hn.sh search "rust programming"

# With filters
scripts/hn.sh search "LLM" --type story --sort date --period week --limit 5
scripts/hn.sh search "hiring remote" --type comment --period month
```

### Who is Hiring

```bash
# Latest "Who is hiring?" job postings
scripts/hn.sh whoishiring
scripts/hn.sh whoishiring --limit 20
```

## Common Workflows

| User asks | Command |
|---|---|
| "What's trending on HN?" | `scripts/hn.sh top` |
| "Latest Ask HN posts" | `scripts/hn.sh ask` |
| "Search HN for X" | `scripts/hn.sh search "X"` |
| "Show me comments on story Y" | `scripts/hn.sh comments Y` |
| "Who is hiring?" | `scripts/hn.sh whoishiring` |
| "Tell me about HN user Z" | `scripts/hn.sh user Z` |

## Notes

- Story lists use parallel fetching for speed
- HTML in comments/bios is auto-converted to plain text
- Timestamps shown as relative time ("2h ago", "3d ago")
- For API details, see [references/api.md](references/api.md)
