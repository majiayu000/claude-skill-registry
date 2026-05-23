---
name: ambit
description: "Check source code coverage using ambit - analyze how much of your codebase Claude has seen during a session"
allowed-tools: Bash(ambits *)
---

# /ambit - Source Code Coverage Analysis

Ambit analyzes Claude Code session logs to determine which parts of your codebase were viewed during a coding session. It provides visibility metrics showing how much of your code Claude has "seen" versus examined in full detail.

## When to Use

- Understand how much of a codebase Claude has examined
- Verify coverage before making architectural decisions
- Identify blind spots in code review sessions
- Track historical session coverage

## Quick Start

### Current Project Coverage (Most Recent Session)
```bash
ambits -p . --coverage
```

### Specific Session Coverage
```bash
ambits -p . --coverage --session <session-id>
```

### Interactive TUI Mode
```bash
ambits -p .
```

### With Serena LSP Symbols (more languages, finer detail)
```bash
ambits -p . --serena
```

## Understanding the Output

```
Coverage Report (Session: abc123...)
──────────────────────────────────────────────────────────
File                              Seen%    Full%
──────────────────────────────────────────────────────────
src/main.rs                       100.0%   75.0%
src/parser/rust.rs                 80.0%   40.0%
src/coverage.rs                   100.0%  100.0%
──────────────────────────────────────────────────────────
```

- **Seen%**: Percentage of symbols Claude viewed at any depth (overview, signature, or full body)
- **Full%**: Percentage of symbols where Claude read the complete implementation

## Coverage Patterns

| Seen% | Full% | Interpretation |
|-------|-------|----------------|
| High  | High  | Thoroughly examined - Claude understands implementation details |
| High  | Low   | Scanned/overviewed but not deeply read - knows structure but not internals |
| Low   | Low   | Barely touched - potential blind spot |
| Low   | High  | Specific functions read without broader context |

**Critical files** (core business logic, security) should have high Full%.
Low coverage on bug-related files suggests Claude may be missing context.

## Examples

```bash
# Check coverage for current project (latest session)
ambits -p . --coverage

# Check a specific session
ambits -p . --coverage --session 34e212cf-a176-4059-ba12-eca94b56e43b

# Launch interactive TUI with symbol-level depth
ambits -p .

# Dump symbol tree to stdout
ambits -p . --dump

# Use Serena's LSP symbol cache
ambits -p . --serena --coverage
```

## Flags Reference

| Flag | Description |
|---|---|
| `--project`, `-p` | Path to the project root (required) |
| `--session`, `-s` | Session ID to track (auto-detects latest) |
| `--dump` | Print symbol tree to stdout and exit |
| `--coverage` | Print coverage report to stdout and exit |
| `--serena` | Use Serena's LSP symbol cache instead of tree-sitter |
| `--log-dir` | Path to Claude Code log directory (auto-derived) |

## Troubleshooting

**"No session found"**: Ensure Claude Code sessions exist in `~/.claude/projects/`. The project slug is derived from your absolute project path with `/` replaced by `-`.

**Low coverage numbers**: Coverage only tracks what Claude explicitly read via tools. Files mentioned in conversation but not read via Read/Edit tools won't be tracked.

**Session not loading**: Verify the session ID matches a `.jsonl` file in the projects directory. Check file permissions.

## Reference Documentation

For detailed guidance, see:
- [coverage-guide.md](coverage-guide.md) - Deep analysis of coverage patterns and strategic interpretation
- [session-management.md](session-management.md) - Finding and managing session files
- [examples.md](examples.md) - Extended usage examples and workflow patterns
