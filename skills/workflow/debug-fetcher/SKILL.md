---
name: debug-fetcher
description: >
  Automated URL fetch failure handling with strategy exhaustion, memory learning,
  and human-in-the-loop recovery. Use when fetches fail and you need intelligent
  retry, pattern learning, and human collaboration.
allowed-tools: Bash, Read, Write, Task
triggers:
  - debug fetch
  - debug fetcher
  - why did fetch fail
  - fetch failure
  - analyze fetch failure
  - retry fetch
  - resilient fetch
metadata:
  short-description: Failure-to-recovery automation for URL fetching
---

# Debug-Fetcher Skill

Automated fetch failure handling that:
1. **Queries /memory first** - applies learned strategies before trying defaults
2. **Exhausts all strategies** - direct, playwright, wayback, brave, jina, proxy, UA rotation
3. **Stores successes** - saves working strategies to /memory for future runs
4. **Collaborates with humans** - uses /interview when all automated strategies fail

## Quick Start

```bash
# Fetch single URL with failure handling
./run.sh fetch https://example.com

# Fetch batch with failure handling
./run.sh fetch-batch urls.txt

# Check what was learned about a domain
./run.sh recall example.com

# Export all learned strategies
./run.sh export-learnings
```

## How It Works

```
URL Request
    │
    ▼
┌──────────────────────────┐
│  1. Query /memory        │
│  "What works for this    │
│   domain?"               │
└──────────────────────────┘
    │
    ▼
┌──────────────────────────┐
│  2. Try learned strategy │
│     (if exists)          │
└──────────────────────────┘
    │
    ▼ (fail or no learned strategy)
┌──────────────────────────┐
│  3. Exhaust strategies:  │
│  - direct fetch          │
│  - playwright            │
│  - wayback machine       │
│  - brave alternates      │
│  - jina reader           │
│  - proxy rotation        │
│  - user-agent rotation   │
└──────────────────────────┘
    │
    ▼ (all fail)
┌──────────────────────────┐
│  4. Launch /interview    │
│  Ask human for help:     │
│  - Credentials?          │
│  - Mirror URL?           │
│  - Manual download?      │
│  - Skip this URL?        │
└──────────────────────────┘
    │
    ▼
┌──────────────────────────┐
│  5. Store to /memory     │
│  - Successful strategy   │
│  - Domain patterns       │
│  - Human-provided info   │
└──────────────────────────┘
```

## Memory Schema

Each learned strategy stores:

| Field | Description |
|-------|-------------|
| `domain` | Target domain (e.g., "nytimes.com") |
| `path_pattern` | URL path pattern (e.g., "/article/*") |
| `successful_strategy` | What worked (e.g., "playwright") |
| `headers` | Custom headers that helped |
| `timing_ms` | How long the fetch took |
| `success_rate` | Historical success rate |
| `failure_count` | How many times this domain failed |
| `last_used` | Timestamp of last use |
| `discovered_at` | When strategy was first learned |

## Commands

| Command | Description |
|---------|-------------|
| `fetch <url>` | Fetch single URL with failure handling |
| `fetch-batch <manifest>` | Fetch list of URLs with failure handling |
| `recall <domain>` | Show learned strategies for domain |
| `export-learnings` | Export all strategies to JSON |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DEBUG_FETCHER_MEMORY_SCOPE` | Memory scope for storing strategies (default: "fetcher_strategies") |
| `DEBUG_FETCHER_MAX_RETRIES` | Max retries per strategy (default: 2) |
| `DEBUG_FETCHER_INTERVIEW_THRESHOLD` | Min failures before triggering interview (default: 3) |

## Integration with Fetcher

Debug-fetcher wraps the standard fetcher skill and adds failure handling capabilities.
All fetcher environment variables (BRAVE_API_KEY, FETCHER_EMIT_MARKDOWN, etc.) are respected.

## Examples

### Learning from Failures

After fetching a batch of URLs, debug-fetcher stores successful strategies:

```bash
# Fetch a batch
./run.sh fetch-batch urls.txt --output results.jsonl

# View what was learned
./run.sh recall attack.mitre.org
# Output:
# Domain: attack.mitre.org
# Strategy: playwright
# Success rate: 95%
# Last used: 2025-01-30

# Next time, playwright will be tried first for attack.mitre.org
./run.sh fetch https://attack.mitre.org/techniques/T1059
```

### Human-in-the-Loop Interview

When all strategies fail, an interview is generated:

```bash
# Fetch batch with failures
./run.sh fetch-batch difficult_urls.txt

# Interview generated at: /tmp/interview_abc123.json
# Run: ./agents/skills/interview/run.sh /tmp/interview_abc123.json

# Example interview questions:
# - "Failed 5 URLs from nytimes.com. Do you have credentials?"
# - "archive.org not working. Try a mirror URL?"
```

### YouTube URL Handling

YouTube URLs are automatically detected and handled via the `/ingest-youtube` skill:

```bash
# YouTube URLs use transcript extraction
./run.sh fetch https://www.youtube.com/watch?v=abc123
# Uses: /ingest-youtube skill for transcript extraction
# Falls back to other strategies if transcript unavailable
```

### Batch Analysis

After a batch run, analyze patterns:

```python
from debug_fetcher.batch_analyzer import analyze_batch, get_failure_summary

# Get summary
summary = get_failure_summary(results)
# {
#   "total": 1000,
#   "success": 850,
#   "failed": 150,
#   "success_rate": "85.0%",
#   "top_failing_domains": [
#     {"domain": "nytimes.com", "count": 45},
#     {"domain": "wsj.com", "count": 30}
#   ],
#   "patterns": [
#     "All 45 URLs from nytimes.com returned HTTP 403",
#     "High failure rate: 50% of failures are paywalled sites"
#   ]
# }
```

## Recovery Actions

When human provides help via interview:

| Action Type | Description | Example |
|-------------|-------------|---------|
| `credentials` | Login credentials provided | username/password for site |
| `mirror` | Alternative URL to try | archive.org mirror |
| `manual_file` | Human downloaded file manually | Path to local PDF |
| `skip` | URL not needed | "Not critical" |
| `retry` | Try again later | Server was down |
| `custom_strategy` | Specific approach suggested | "Use proxy" |

## Files

```
.agents/skills/debug-fetcher/
├── SKILL.md           # This file
├── run.sh             # Entry point
├── pyproject.toml     # Dependencies
└── debug_fetcher/     # Python package
    ├── __init__.py
    ├── cli.py                 # CLI commands
    ├── memory_schema.py       # FetchStrategy dataclass
    ├── memory_bridge.py       # Recall/learn from /memory
    ├── strategy_engine.py     # Strategy exhaustion loop
    ├── batch_analyzer.py      # Analyze batch failures
    ├── interview_generator.py # Generate /interview JSON
    ├── interview_processor.py # Process interview responses
    ├── recovery_executor.py   # Execute recovery actions
    └── pdf_bridge.py          # Cross-skill integration with debug-pdf
```

## Companion Skill: debug-pdf

`debug-fetcher` and `debug-pdf` work together in the pipeline:

```
URL → debug-fetcher → /fetcher → /extractor → debug-pdf
         ↓                           ↓
      fetch fail               extraction fail
         ↓                           ↓
    retry/recover            analyze PDF issues
         ↓                           ↓
      /memory                     /memory
```

**Shared failure patterns:**
| Pattern | debug-fetcher | debug-pdf |
|---------|---------------|-----------|
| `auth_required` | HTTP 401/403 | N/A |
| `access_restricted` | HTTP 403 | N/A |
| `paywall_detected` | Soft paywall | N/A |
| `password_protected` | N/A | Encrypted PDF |
| `scanned_no_ocr` | N/A | No text layer |
| `archive_org_wrap` | Wayback wrapper | Wayback wrapper |

**Cross-skill notifications:**
- When debug-fetcher successfully fetches a PDF but detects issues (password protected, scanned), it notifies debug-pdf via agent-inbox
- When debug-fetcher fails to fetch a PDF URL, it notifies debug-pdf for tracking

## Related Skills

- `/memory` - Stores learned fetch strategies
- `/interview` - Human collaboration for unrecoverable URLs
- `/ingest-youtube` - YouTube transcript extraction
- `/fetcher` - Core URL fetching functionality
- `/extractor` - Content extraction from fetched documents
- `/debug-pdf` - Companion skill for PDF extraction failures
