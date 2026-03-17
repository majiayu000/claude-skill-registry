---
name: conversation-search
description: Search Claude conversation history JSONL files for keywords, with date filtering and context windows
disable-model-invocation: true
---

# Conversation Search

Search through past Claude conversation history stored in `~/.claude/projects/` JSONL files.

## When to Run

- "What did we decide about X?" — recovering prior decisions
- "Find the session where we debugged Y" — locating specific work
- "When did we last touch Z?" — timeline reconstruction
- Before re-implementing something to check if it was already attempted

## Arguments

- First argument: search keyword or phrase (required)
- `--all-projects`: search all projects, not just BrickTrack
- `--from YYYY-MM-DD`: only records on or after this date
- `--to YYYY-MM-DD`: only records on or before this date
- `--context N`: show N messages before and after each match (default: 0)

## Process

### Stage 1: Fast Pre-filter (grep)

Find JSONL files containing the keyword (filename list only, fast):

```bash
KEYWORD="<user-provided-keyword>"
PROJECT_DIR="$HOME/.claude/projects/-Users-matthewgleeson-Documents-property-tracker"

# If --all-projects flag: search all subdirs under ~/.claude/projects/
# PROJECT_DIR="$HOME/.claude/projects"

grep -rl "$KEYWORD" "$PROJECT_DIR" --include="*.jsonl" 2>/dev/null | head -20
```

If no matches, report "No matches found" and stop.

### Stage 2: Python Structured Extraction

For each matching file from Stage 1, run this Python extraction. Adapt the variables at the top based on the user's flags:

```python
import json, sys, os
from datetime import datetime

keyword = "KEYWORD".lower()       # Replace with actual keyword
from_date = None                  # Set from --from flag, e.g. "2026-01-01"
to_date = None                    # Set from --to flag
context_n = 0                     # Set from --context flag
files = [                         # Paste matching files from Stage 1
    # "/path/to/file1.jsonl",
]

# Types to skip (noisy, not conversational content)
SKIP_TYPES = {'file-history-snapshot', 'progress', 'system', 'queue-operation', 'pr-link'}

results = []

for filepath in files:
    records = []
    try:
        with open(filepath) as f:
            for line in f:
                try:
                    r = json.loads(line.strip())
                    if r.get('type') in SKIP_TYPES:
                        continue
                    records.append(r)
                except json.JSONDecodeError:
                    continue
    except (IOError, OSError):
        continue

    for i, r in enumerate(records):
        ts = r.get('timestamp', '')
        rtype = r.get('type', '')
        text = ''

        # Extract text from user messages (can be string or dict)
        if rtype == 'user':
            msg = r.get('message', '')
            if isinstance(msg, str):
                text = msg
            elif isinstance(msg, dict):
                content = msg.get('content', '')
                if isinstance(content, str):
                    text = content
                elif isinstance(content, list):
                    text = ' '.join(
                        item.get('text', '') for item in content
                        if isinstance(item, dict) and item.get('type') == 'text'
                    )

        # Extract text from assistant messages
        elif rtype == 'assistant':
            msg = r.get('message', {})
            if isinstance(msg, dict):
                content = msg.get('content', [])
                if isinstance(content, list):
                    text = ' '.join(
                        item.get('text', '') for item in content
                        if isinstance(item, dict) and item.get('type') == 'text'
                    )

        if keyword not in text.lower():
            continue

        # Date filter
        if ts and (from_date or to_date):
            try:
                dt = datetime.fromisoformat(ts[:10])
                if from_date and dt < datetime.fromisoformat(from_date):
                    continue
                if to_date and dt > datetime.fromisoformat(to_date):
                    continue
            except ValueError:
                pass

        snippet = text[:300] + ('...' if len(text) > 300 else '')
        results.append({
            'file': os.path.basename(filepath),
            'timestamp': ts[:19] if ts else 'unknown',
            'type': rtype,
            'branch': r.get('gitBranch', ''),
            'snippet': snippet,
        })

# Print results
if not results:
    print(f"No matching messages for: {keyword}")
else:
    print(f"\nFound {len(results)} match(es) for '{keyword}':\n")
    for r in results:
        print(f"[{r['timestamp']}] [{r['type']}] [{r['branch']}] {r['file']}")
        print(f"  {r['snippet']}")
        print()
```

### Tips

- Stage 1 grep is essential — some JSONL files are 100MB+. Never parse all files.
- Limit Stage 1 to `head -20` files to avoid blowing context.
- For `--context N`, expand the extraction to include N records before/after each match from `records[]`.
- The `files` list in Stage 2 should be populated from Stage 1 output.

## Examples

```
/conversation-search "weekly rent"
/conversation-search "basiq" --from 2026-01-01
/conversation-search "circuit breaker" --context 2
/conversation-search "anti-pattern" --all-projects
```
