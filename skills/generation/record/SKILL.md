---
name: record
description: |
  Terminal recording with asciinema for documentation. Creates .cast files
  that can be embedded in documentation or converted to GIF/video. Use when
  users need to create terminal recordings for tutorials, demos, or docs.
---

# record - Terminal Recording

## Overview

The `record` command creates asciinema terminal recordings for documentation purposes. It records a command execution with automatic title and metadata injection, producing `.cast` files compatible with asciinema players.

**Key Concept:** Records are non-interactive - you specify the command to run and it captures the output. The recording fails if the command fails (exit code != 0).

## Quick Reference

| Parameter | Long Flag | Short | Required | Description |
|-----------|-----------|-------|----------|-------------|
| File | `--file` | `-f` | Yes | Output .cast file path |
| Command | `--command` | `-c` | Yes | Command to record |
| Title | `--title` | `-t` | No | Recording title (defaults to filename) |

## Usage

```bash
# Basic recording
ujust record -f OUTPUT.cast -c "COMMAND"

# With title
ujust record -f OUTPUT.cast -t "TITLE" -c "COMMAND"

# Long form
ujust record --file=OUTPUT.cast --title="TITLE" --command="COMMAND"
```

## Examples

### Record a Simple Command

```bash
ujust record -f docs/recordings/hello.cast -c "echo Hello World"
```

### Record a ujust Command

```bash
ujust record -f docs/recordings/ollama-start.cast -t "Starting Ollama" -c "ujust ollama start"
```

### Record Multiple Commands

```bash
# Use quoted string with && or ;
ujust record -f docs/recordings/setup.cast -c "ujust ollama config && ujust ollama start"
```

### Record to Specific Directory

```bash
# Creates directory if needed
ujust record -f /tmp/demos/test.cast -c "ls -la"
```

## Output Format

The command produces asciinema v3 format `.cast` files:

- **Header:** JSON with title, timestamp, and injected command metadata
- **Events:** Timestamped terminal output events
- **Compatible with:** asciinema player, asciinema-agg (GIF), svg-term

### Example Header

```json
{"version":3,"width":80,"height":24,"title":"Starting Ollama","command":"ujust ollama start"}
```

## Requirements

The following tools must be available:

| Tool | Purpose |
|------|---------|
| `asciinema` | Terminal recording |
| `jq` | Metadata injection |

Both are pre-installed in Bazzite AI.

## Behavior

1. Validates required parameters (`--file` and `--command`)
2. Creates output directory if needed
3. Creates temp script with the command
4. Records execution with asciinema
5. Injects command metadata into .cast header
6. **Fails and removes output** if command exits non-zero

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Recording successful |
| 1 | Missing parameters, asciinema error, or jq error |
| N | Command exit code (recording removed on failure) |

## Common Workflows

### Documentation Recording

```bash
# Record feature demonstration
ujust record -f docs/recordings/feature-demo.cast -t "Feature Demo" -c "ujust feature-name"

# Verify recording
asciinema play docs/recordings/feature-demo.cast
```

### Convert to GIF

```bash
# Using asciinema-agg (separate tool)
agg docs/recordings/demo.cast docs/images/demo.gif

# Or using svg-term
svg-term --in docs/recordings/demo.cast --out docs/images/demo.svg
```

## Troubleshooting

### "asciinema not installed"

Asciinema should be pre-installed. If missing:

```bash
flatpak install flathub org.asciinema.asciinema
```

### "Recording failed - command exited with code N"

The recorded command failed. Fix the command first, then re-record:

```bash
# Test command manually
ujust ollama start

# Then record
ujust record -f output.cast -c "ujust ollama start"
```

### Recording is Empty or Truncated

Ensure the command produces output. Silent commands may appear empty:

```bash
# Add echo for visibility
ujust record -f output.cast -c "echo 'Starting...' && silent-command"
```

## Cross-References

- **Related:** Documentation workflows, demo creation
- **asciinema docs:** [https://asciinema.org/docs](https://asciinema.org/docs)

## When to Use This Skill

Use when the user asks about:

- "record terminal", "terminal recording", "asciinema"
- "create demo", "record command", "capture terminal"
- "documentation recording", "tutorial recording"
- ".cast file", "terminal GIF"
