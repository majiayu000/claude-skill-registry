---
name: session-search
description: Search through historical Claude sessions for code, conversations, and commands. Use when user asks about previous sessions, past conversations, "did I ever", "find in history", or wants to retrieve code/info from earlier chats.
---

# Session Search

Search through your Claude session history stored in `~/.claude/projects/`.

## Usage

Run the search script with a regex or keyword pattern:

```bash
python ~/.claude/skills/session-search/search.py "pattern" [max_results]
```

## Examples

```bash
# Find sessions mentioning a specific function
python ~/.claude/skills/session-search/search.py "def parse_config"

# Find discussions about a topic
python ~/.claude/skills/session-search/search.py "kubernetes|docker"

# Find code with specific imports
python ~/.claude/skills/session-search/search.py "from fastapi import"

# Limit results
python ~/.claude/skills/session-search/search.py "error" 10
```

## Output

Returns matches with:
- Session slug/ID and project path
- Timestamp
- Role (user/assistant)
- Matching content with surrounding context
- 1 message before/after for context

Results are sorted by recency (newest first), limited to 20 by default.
