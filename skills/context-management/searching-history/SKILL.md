---
name: searching-history
description: >-
  Search past Claude Code conversation history and tool logs to recall previous
  solutions, commands, and approaches. ALWAYS load this skill when the user
  mentions anything about past sessions, previous conversations, or prior work
  done in Claude Code. Trigger phrases include: "have I done this before", "how
  did I fix", "what command did I run", "remind me how", "last time we", "find
  that session", "pick up where we left off", "check my history", "I did this
  before", "previous conversation", "a few months ago", "we figured it out",
  "can you find what I did", or any reference to recalling, remembering, or
  looking up something from a past Claude Code session. Also trigger when the
  user asks about past implementations, error resolutions, configuration changes,
  or commands from earlier conversations — even if they don't explicitly say
  "search history". Do NOT use for searching the current codebase, the web, npm,
  GitHub repos, git log, or documentation — only for recalling past Claude Code
  session history.
allowed-tools: Bash
argument-hint: "<search-query>"
---

# glhf — Conversation History Search

Search your Claude Code conversation history using hybrid search (text + semantic).

When invoked as `/glhf <query>`, run: `glhf search "$ARGUMENTS" --mode semantic --compact`

## Quick Examples

```bash
# Find past solutions (semantic search)
glhf search "authentication" --mode semantic --compact

# Find commands you've run
glhf search "docker" -t Bash --compact

# Regex search for exact error messages
glhf search -e "ECONNREFUSED|ETIMEDOUT" --compact

# Search with context (like grep -C)
glhf search "panic" -C 2 --compact

# Check recent sessions
glhf recent -l 10

# Get session overview then dive deeper
glhf session abc123 --summary
glhf session abc123 --limit 50
```

## Commands

| Command    | Purpose                              |
| ---------- | ------------------------------------ |
| `search`   | Find content across all sessions     |
| `session`  | View a specific session's content    |
| `related`  | Find sessions similar to a given one |
| `recent`   | List recent sessions                 |
| `projects` | List all indexed projects            |
| `status`   | Show index stats                     |
| `index`    | Update index (incremental by default)|

## Key Search Flags

| Flag                     | Purpose                                       |
| ------------------------ | --------------------------------------------- |
| `--compact`              | One-line output, fewer tokens                 |
| `--mode semantic`        | Conceptual search (how to X, patterns)        |
| `--mode text`            | Exact keyword matching                        |
| `-e`/`--regex`           | Regex pattern matching (like grep -e)         |
| `-i`/`--ignore-case`     | Case-insensitive (for regex mode)             |
| `-A N`/`-B N`/`-C N`     | Context lines after/before/around matches     |
| `-t Bash`                | Filter by tool (Bash, Read, Edit, Grep, etc.) |
| `-p .`                   | Filter to current project                     |
| `-X name`                | Exclude a project by name (repeatable)        |
| `--since 1d`             | Time filter (1h, 2d, 1w, or date)             |
| `--errors`               | Only show error results                       |
| `--messages-only`        | Exclude tool calls                            |
| `--tools-only`           | Exclude messages                              |
| `--show-session-id`      | Include session IDs for follow-up             |
| `--json`                 | Machine-readable JSON output                  |
| `--scores`               | Show relevance scores                         |
| `--oldest`               | Reverse sort (oldest first)                   |
| `--include-this-project` | Override auto-exclusion of current project    |
| `--include-this-session` | Override auto-exclusion of current session    |
| `--this-session`         | Filter to current session only                |

## Recommended Patterns

**Find past solutions:**

```bash
glhf search "problem description" --mode semantic --compact
glhf search "specific keyword" --show-session-id --compact
glhf session <id> --summary
```

**Recall commands:**

```bash
glhf search "git rebase" -t Bash --compact
glhf search "cargo" -t Bash --since 1w --compact
```

**Regex search for exact errors:**

```bash
glhf search -e "thread.*panicked" --compact
glhf search -e "error\[E\d+\]" -i --compact
```

**Find similar work:**

```bash
glhf recent -l 10
glhf related <session-id> --limit 5
```

**Debug past errors:**

```bash
glhf search "error" --errors --since 1d --compact
```

**Cross-project search (override auto-exclusion):**

```bash
glhf search "auth" --include-this-project --compact
glhf search "deploy" -X stable -X dotfiles --compact
```

## Tips

1. **Always use `--compact`** — significantly reduces output tokens
2. **Use `--mode semantic`** for "how to" questions and conceptual searches
3. **Use `-e` (regex)** for exact error messages and patterns
4. **Chain commands**: search → get session ID → view summary → get full context
5. **Current project/session auto-excluded** when running inside Claude Code — use `--include-this-project` or `--include-this-session` to override
6. **Use `-p .`** to filter to current project when you want to include it
7. **Use `--json`** when piping to other tools or processing programmatically
8. **Index is incremental** — `glhf index` only re-processes changed files (~0.1s). Use `--full` to rebuild from scratch
9. **Search shows staleness hints** — if the index is behind, it prints how many files changed and when last indexed. Run `glhf index` to update
