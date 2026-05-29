---
name: specstory-link-trail
description: Track all URLs fetched during SpecStory AI coding sessions. Run when user says "show my link trail", "what URLs did I visit", "list fetched links", or "show web fetches".
license: Apache-2.0
metadata:
  author: SpecStory, Inc.
  version: "1.0.0"
  argument-hint: "[history-file-or-pattern]"
allowed-tools: Bash, Read
---

# SpecStory Link Trail

Reviews your `.specstory/history` sessions and creates a summary of all URLs that were fetched via WebFetch tool calls. Useful for auditing external resources accessed during development.

## How It Works

1. **Parses** SpecStory history files for WebFetch tool calls
2. **Extracts** URLs, status codes, and context
3. **Groups** by session with timestamps
4. **Separates** successful fetches from failures
5. **Deduplicates** repeated URLs with fetch counts

## Why Track Links?

During AI-assisted coding, your assistant fetches documentation, APIs, and resources on your behalf. Link Trail helps you:
- Audit what external resources were accessed
- Find that documentation page you saw earlier
- Review failed fetches that might need retry
- Understand your research patterns

## Usage

### Slash Command

| User says | Script behavior |
|-----------|-----------------|
| `/specstory-link-trail` | All sessions in history |
| `/specstory-link-trail today` | Today's sessions only |
| `/specstory-link-trail last session` | Most recent session |
| `/specstory-link-trail 2026-01-22` | Sessions from specific date |
| `/specstory-link-trail *.md` | Custom glob pattern |

### Direct Script Usage

```bash
# All sessions
python skills/specstory-link-trail/parse_webfetch.py .specstory/history/*.md | \
  python skills/specstory-link-trail/generate_report.py -

# Specific session
python skills/specstory-link-trail/parse_webfetch.py .specstory/history/2026-01-22*.md | \
  python skills/specstory-link-trail/generate_report.py -

# Sessions from a date range
python skills/specstory-link-trail/parse_webfetch.py .specstory/history/2026-01-2*.md | \
  python skills/specstory-link-trail/generate_report.py -
```

## Output

```
Link Trail Report
=================

Sessions analyzed: 5
Total URLs fetched: 23 (18 successful, 5 failed)

Session: fix-authentication-bug (2026-01-22)
--------------------------------------------
Successful fetches:
  - https://docs.github.com/en/rest/authentication (×2)
  - https://jwt.io/introduction
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401

Failed fetches:
  - https://internal.company.com/api/docs (403 Forbidden)

Session: add-caching-layer (2026-01-21)
---------------------------------------
Successful fetches:
  - https://redis.io/docs/latest/commands
  - https://docs.python.org/3/library/functools.html#functools.lru_cache
  - https://stackoverflow.com/questions/... (×3)

Summary by Domain
-----------------
  github.com: 5 fetches
  stackoverflow.com: 4 fetches
  docs.python.org: 3 fetches
  redis.io: 2 fetches
  (9 other domains): 9 fetches
```

## Present Results to User

The script output IS the report. Present it directly without additional commentary, but you may:

1. **Highlight key findings** - Most frequently accessed domains, any failed fetches
2. **Offer follow-ups** - "Want me to retry the failed fetches?" or "Need details on any of these?"

### Example Response

```
Here's your link trail from recent sessions:

[script output here]

I noticed 5 failed fetches - mostly internal URLs that require authentication.
The most accessed domain was github.com (5 fetches), mostly for their REST API docs.

Would you like me to:
- Retry any of the failed fetches?
- Open any of these links?
- Filter to a specific session?
```

## Notes

- Uses streaming parsing for large history files
- URLs are extracted from WebFetch tool calls in the history
- Fetch counts show when the same URL was accessed multiple times
- Failed fetches include the HTTP status code when available
