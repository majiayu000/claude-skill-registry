---
name: claude-tail
description: View Claude Code session logs with colors, filtering, and real-time following
---
# Claude Tail Skill

You are a Claude Code session log analysis specialist using the `claude-tail` tool. This skill provides comprehensive guidance for viewing, filtering, and analyzing Claude Code session logs.

## Core Concepts

`claude-tail` reads Claude Code session logs (JSONL format) and displays them with:
- Syntax highlighting and colors
- Real-time following (like `tail -f`)
- Filtering by event type, tool, time range, or errors
- Multiple display modes (compact, verbose, stats, tools-only)

## Basic Usage

### View a Session Log

```bash
# View a specific log file (follows by default)
claude-tail ~/.claude/sessions/2024-01-15-session.jsonl

# View without following (read once and exit)
claude-tail --no-follow ~/.claude/sessions/2024-01-15-session.jsonl

# Read from stdin
cat session.jsonl | claude-tail
```

### Follow Logs in Real-Time

```bash
# Follow mode is enabled by default
claude-tail session.jsonl

# Explicitly enable follow mode
claude-tail -f session.jsonl

# Follow multiple files
claude-tail session1.jsonl session2.jsonl
```

### Watch for New Logs

```bash
# Watch all JSONL files in current directory
claude-tail --pattern "*.jsonl"

# Watch all session logs
claude-tail --pattern "~/.claude/sessions/*.jsonl"
```

## Display Modes

### Compact Mode

```bash
# Minimal output, one-line per event
claude-tail --compact session.jsonl
```

### Verbose Mode

```bash
# Detailed output with full event information
claude-tail --verbose session.jsonl
```

### Statistics Mode

```bash
# Show statistics about the session
claude-tail --stats session.jsonl
```

### Tools-Only Mode

```bash
# Show only tool usage events
claude-tail --tools-only session.jsonl
```

## Filtering

### Filter by Event Type

```bash
# Show only specific event types (comma-separated)
claude-tail --type tool_use,error session.jsonl

# Common event types: tool_use, text, error, system
claude-tail --type text session.jsonl
```

### Filter by Tool Name

```bash
# Show only specific tools (comma-separated)
claude-tail --tool Read,Write session.jsonl

# Show only bash commands
claude-tail --tool Bash session.jsonl

# Show only file operations
claude-tail --tool Read,Write,Edit session.jsonl
```

### Filter by Time Range

```bash
# Show events after a specific time (HH:MM:SS)
claude-tail --after 14:30:00 session.jsonl

# Show events before a specific time
claude-tail --before 15:45:00 session.jsonl

# Show events in a time window
claude-tail --after 14:30:00 --before 15:45:00 session.jsonl
```

### Show Only Errors

```bash
# Display only error events
claude-tail --errors-only session.jsonl
```

## Display Options

### Terminal Width and Wrapping

```bash
# Set custom terminal width
claude-tail --width 120 session.jsonl

# Disable line wrapping
claude-tail --no-wrap session.jsonl

# Combine options
claude-tail --width 80 --no-wrap session.jsonl
```

## Common Workflows

### Debug a Session

```bash
# Show all errors in a session
claude-tail --errors-only --no-follow session.jsonl

# Show tool usage with errors
claude-tail --tools-only --errors-only session.jsonl

# Verbose output for debugging
claude-tail --verbose --errors-only session.jsonl
```

### Monitor Tool Usage

```bash
# Watch what tools are being called
claude-tail --tools-only -f session.jsonl

# Monitor specific tools in real-time
claude-tail --tool Bash,Read,Write -f session.jsonl

# Get tool usage statistics
claude-tail --stats --tools-only session.jsonl
```

### Analyze Session Activity

```bash
# Review activity in a time window
claude-tail --after 10:00:00 --before 11:00:00 --no-follow session.jsonl

# See compact summary of a session
claude-tail --compact --no-follow session.jsonl

# Get detailed statistics
claude-tail --stats session.jsonl
```

### Watch Live Sessions

```bash
# Follow the most recent session
claude-tail -f ~/.claude/sessions/$(ls -t ~/.claude/sessions/*.jsonl | head -1)

# Watch all new session files
claude-tail --pattern "~/.claude/sessions/*.jsonl"

# Monitor errors in real-time
claude-tail --errors-only -f current-session.jsonl
```

## Advanced Usage

### Combining Filters

```bash
# Show Read/Write operations with errors after 2pm
claude-tail --tool Read,Write \
           --errors-only \
           --after 14:00:00 \
           session.jsonl

# Monitor specific tools in compact mode
claude-tail --tool Bash,Grep,Read \
           --compact \
           -f session.jsonl
```

### Session Log Analysis

```bash
# Quick session overview
claude-tail --stats --no-follow session.jsonl

# Detailed tool usage analysis
claude-tail --tools-only --verbose --no-follow session.jsonl

# Find all errors in a session
claude-tail --errors-only --verbose --no-follow session.jsonl
```

### Debugging Workflows

```bash
# Debug a specific time period with full detail
claude-tail --verbose \
           --after 14:30:00 \
           --before 14:35:00 \
           --no-follow \
           session.jsonl

# Monitor for errors during development
claude-tail --errors-only --tools-only -f session.jsonl

# Watch file operations in real-time
claude-tail --tool Read,Write,Edit,Glob,Grep \
           --compact \
           -f session.jsonl
```

## Session Log Location

Claude Code session logs are typically stored in:

```bash
~/.claude/sessions/*.jsonl
```

### Find Recent Sessions

```bash
# List sessions by most recent
ls -lt ~/.claude/sessions/*.jsonl | head -5

# View the most recent session
claude-tail ~/.claude/sessions/$(ls -t ~/.claude/sessions/*.jsonl | head -1)
```

## Common Event Types

- **tool_use** - Claude called a tool (Read, Write, Bash, etc.)
- **text** - Claude sent text output
- **error** - An error occurred
- **system** - System messages and events

## Common Tools to Filter

- **Read** - File reading operations
- **Write** - File writing operations
- **Edit** - File editing operations
- **Bash** - Shell command execution
- **Grep** - Code search operations
- **Glob** - File pattern matching
- **Task** - Agent task launches
- **WebFetch** - Web content fetching
- **WebSearch** - Web search queries

## Best Practices

1. **Use follow mode for active sessions**: Monitor live sessions with `-f`
2. **Filter aggressively**: Use `--tool`, `--type`, and time filters to focus on relevant events
3. **Start with stats mode**: Get an overview with `--stats` before diving into details
4. **Use compact mode for overviews**: Quickly scan many events with `--compact`
5. **Use verbose mode for debugging**: Get full detail when investigating issues
6. **Watch for errors**: Regular `--errors-only` checks help catch issues early
7. **Analyze tool patterns**: Use `--tools-only` to understand workflow patterns

## Tips

- Follow mode is enabled by default (use `--no-follow` to disable)
- Combine multiple filters to narrow down events precisely
- Use time filters to focus on specific parts of a session
- Stats mode is great for session retrospectives
- Errors-only mode helps quickly identify problems
- Tools-only mode shows the "what" without the "why"

## Quick Reference

```bash
# View and follow
claude-tail session.jsonl

# View once
claude-tail --no-follow session.jsonl

# Show stats
claude-tail --stats session.jsonl

# Only errors
claude-tail --errors-only session.jsonl

# Only tools
claude-tail --tools-only session.jsonl

# Filter by tool
claude-tail --tool Read,Write session.jsonl

# Filter by time
claude-tail --after 14:00:00 --before 15:00:00 session.jsonl

# Compact output
claude-tail --compact session.jsonl

# Verbose output
claude-tail --verbose session.jsonl

# Watch pattern
claude-tail --pattern "*.jsonl"
```
