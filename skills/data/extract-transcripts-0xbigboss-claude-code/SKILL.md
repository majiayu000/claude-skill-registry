---
name: extract-transcripts
description: Extract readable transcripts from Claude Code and Codex CLI session JSONL files
---

# Extract Transcripts

Extracts readable markdown transcripts from Claude Code and Codex CLI session JSONL files.

## Scripts

### Claude Code Sessions

```bash
# Extract a single session
uv run ~/.claude/skills/extract-transcripts/extract_transcript.py <session.jsonl>

# With tool calls and thinking blocks
uv run ~/.claude/skills/extract-transcripts/extract_transcript.py <session.jsonl> --include-tools --include-thinking

# Extract all sessions from a directory
uv run ~/.claude/skills/extract-transcripts/extract_transcript.py <directory> --all

# Output to file
uv run ~/.claude/skills/extract-transcripts/extract_transcript.py <session.jsonl> -o output.md

# Summary only (quick overview)
uv run ~/.claude/skills/extract-transcripts/extract_transcript.py <session.jsonl> --summary

# Skip empty/warmup-only sessions
uv run ~/.claude/skills/extract-transcripts/extract_transcript.py <directory> --all --skip-empty
```

**Options:**
- `--include-tools`: Include tool calls and results
- `--include-thinking`: Include Claude's thinking blocks
- `--all`: Process all .jsonl files in directory
- `-o, --output`: Output file path (default: stdout)
- `--summary`: Only output brief summary
- `--skip-empty`: Skip empty and warmup-only sessions
- `--min-messages N`: Minimum messages for --skip-empty (default: 2)

### Codex CLI Sessions

```bash
# Extract a Codex session
uv run ~/.claude/skills/extract-transcripts/extract_codex_transcript.py <session.jsonl>

# Extract from Codex history file
uv run ~/.claude/skills/extract-transcripts/extract_codex_transcript.py ~/.codex/history.jsonl --history
```

## Session File Locations

### Claude Code
- Sessions: `~/.claude/projects/<project-path>/<session-id>.jsonl`

### Codex CLI
- Sessions: `~/.codex/sessions/<session_id>/rollout.jsonl`
- History: `~/.codex/history.jsonl`

## DuckDB-Based Transcript Index

For querying across many sessions, use the DuckDB-based indexer:

```bash
# Index all sessions (incremental - only new/changed files)
uv run ~/.claude/skills/extract-transcripts/transcript_index.py index

# Force full reindex
uv run ~/.claude/skills/extract-transcripts/transcript_index.py index --full

# Limit number of files to process
uv run ~/.claude/skills/extract-transcripts/transcript_index.py index --limit 10

# List recent sessions
uv run ~/.claude/skills/extract-transcripts/transcript_index.py recent
uv run ~/.claude/skills/extract-transcripts/transcript_index.py recent --limit 20
uv run ~/.claude/skills/extract-transcripts/transcript_index.py recent --project myapp
uv run ~/.claude/skills/extract-transcripts/transcript_index.py recent --since 7d

# Search across sessions
uv run ~/.claude/skills/extract-transcripts/transcript_index.py search "error handling"
uv run ~/.claude/skills/extract-transcripts/transcript_index.py search "query" --cwd ~/myproject

# Show a session transcript
uv run ~/.claude/skills/extract-transcripts/transcript_index.py show <file_path>
uv run ~/.claude/skills/extract-transcripts/transcript_index.py show <file_path> --summary
```

**Requirements:** uv (dependencies auto-installed via inline script metadata)

**Database location:** `~/.claude/transcript-index/sessions.duckdb`

## Output Format

Transcripts are formatted as markdown with:
- Session metadata (date, duration, model, working directory, git branch)
- User messages prefixed with `## User`
- Assistant responses prefixed with `## Assistant`
- Tool calls in code blocks (if --include-tools)
- Thinking in blockquotes (if --include-thinking)
- Tool usage summary for Codex sessions
