---
name: session-search
description: "[DEPRECATED] Use /conversation-search instead — has date filtering, context windows, and structured extraction"
user-invocable: true
disable-model-invocation: true
---

# /session-search — Past Session Search (DEPRECATED)

> **Use `/conversation-search` instead.** It provides date filtering, context windows, and structured extraction.
> This skill is a simplified version kept for backward compatibility.

Search `~/.claude/projects/` for past session transcripts containing a keyword.

## Usage

User provides: `/session-search <keyword>` (e.g., `/session-search weekly rent`)

## Steps

1. **Search session files:**
   ```bash
   grep -rl "<keyword>" ~/.claude/projects/ --include="*.jsonl" | head -20
   ```

2. **For each matching file, extract context:**
   ```bash
   grep -n "<keyword>" <file> | head -5
   ```

3. **Present results** as a table:
   | Session File | Matches | Date (from filename/mtime) |
   |---|---|---|

4. **Offer to read** specific sessions for more detail.

## Notes
- Session files are JSONL format (one JSON object per line)
- Each line contains a message with role, content, and metadata
- Search is case-insensitive by default
- Limit to 20 files to avoid overwhelming output
- Files may be large — use grep line numbers to find specific context
