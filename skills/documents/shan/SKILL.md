---
name: shan
description: Dump a Claude Code session transcript as navigable Markdown. Use when user wants to review, analyze, or export a session transcript.
argument-hint: transcript dump [session-id]
allowed-tools: Bash(bun:*)
---

# Shan

Claude Code tooling CLI (named after Claude Shannon).

## Execute

Run the shan CLI with provided arguments:

```bash
bun ~/projects/jasonkuhrt/dotfiles/packages/shan/src/bin/shan.ts $ARGUMENTS
```

## Commands

### `transcript dump [session-id]`

Convert JSONL transcripts to navigable Markdown with columnar headings for editor outline navigation.

**Arguments:**

| Argument | Description |
|----------|-------------|
| `[session-id]` | Optional. Partial UUID prefix (e.g., `dc8ffe42`). Defaults to current session. |

**Output:** `.claude/transcripts/<session-id>.transcript.md` in project directory

**Examples:**
```
/shan transcript dump              # dump current session
/shan transcript dump dc8ffe42     # dump specific session
```

**Output Format:**

Headings use monospace columns with underscore padding for editor outline alignment:

```markdown
# `001` `01/25/2026 22:45` `file-history-snapshot` `snapshot______________________`
# `002` `01/25/2026 22:45` `progress_____________` `SessionStart:clear____________`
# `003` `01/25/2026 22:46` `user_________________` `sync__________________________`
```
