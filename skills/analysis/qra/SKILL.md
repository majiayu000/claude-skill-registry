---
name: qra
description: >
  Extract Question-Reasoning-Answer pairs from text.
  Use --context for domain-focused extraction.
  Validates answers are grounded in source text.
allowed-tools: Bash, Read
triggers:
  - extract QRA
  - extract Q&A
  - extract knowledge
  - create Q&A pairs
  - knowledge extraction
  - generate questions from
metadata:
  short-description: Extract grounded Q&A pairs from text
---

# QRA Skill

Extract Question-Reasoning-Answer pairs from text and store in memory.

## Happy Path

```bash
# Extract from text file
./run.sh --file document.md --scope research

# With domain focus (recommended)
./run.sh --file notes.txt --scope project --context "security expert"

# Preview before storing
./run.sh --file transcript.txt --dry-run

# From stdin
cat meeting_notes.txt | ./run.sh --scope meetings
```

## Parameters

| Flag | Description |
|------|-------------|
| `--file` | Text or markdown file |
| `--text` | Raw text content |
| `--scope` | Memory scope (default: research) |
| `--context` | Domain focus, e.g. "ML researcher" |
| `--dry-run` | Preview without storing |
| `--json` | JSON output |

## What It Does

1. **Split** text into logical sections
2. **Extract** Q&A pairs via LLM (parallel batch)
3. **Validate** answers are grounded in source
4. **Store** to memory via `memory-agent learn`

## When to Use

- Text content (not PDFs - use `distill` for PDFs)
- Meeting transcripts
- Code documentation
- Notes and summaries
- Any plain text you want to remember

## Examples

```bash
# Meeting transcript
./run.sh --file meeting.txt --scope team --context "project manager"

# Code documentation
./run.sh --file README.md --scope code --context "Python developer"

# From clipboard/pipe
pbpaste | ./run.sh --scope notes --dry-run
```

## Environment Variables (Optional Tuning)

| Variable | Default | Description |
|----------|---------|-------------|
| `QRA_CONCURRENCY` | 6 | Parallel LLM requests |
| `QRA_GROUNDING_THRESH` | 0.6 | Grounding similarity threshold |
| `QRA_NO_GROUNDING` | - | Set to 1 to skip validation |
