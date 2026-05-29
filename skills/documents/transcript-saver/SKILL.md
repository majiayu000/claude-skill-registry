---
name: transcript-saver
description: Save and export the current Claude Code session as a shareable HTML transcript. Use this skill when the user asks to save, export, archive, or publish their current Claude Code conversation or session. Triggers on phrases like "save this transcript", "export this session", "create a transcript", "archive this conversation", "publish to gist", or "share this session". Wraps Simon Willison's claude-code-transcripts tool for in-session use.
---

# Claude Code Transcript Saver

Save the current Claude Code session as clean, browsable HTML pages with optional GitHub Gist publishing.

## Quick Start

To save the current session transcript:

```bash
# Save to a local directory (opens in browser by default)
python /path/to/skill/scripts/save_transcript.py

# Save to a specific output directory
python /path/to/skill/scripts/save_transcript.py --output ./my-transcript

# Publish to GitHub Gist (requires gh CLI authenticated)
python /path/to/skill/scripts/save_transcript.py --gist

# Both: save locally AND publish to gist
python /path/to/skill/scripts/save_transcript.py --output ./my-transcript --gist
```

## How It Works

This skill wraps Simon Willison's `claude-code-transcripts` tool, which:

1. Reads Claude Code session files from `~/.claude/projects/` (JSONL format)
2. Converts them to paginated, mobile-friendly HTML pages
3. Generates an index page with a timeline of prompts and commits
4. Optionally publishes to GitHub Gist for easy sharing

### Output Files

The tool generates:
- `index.html` - Summary page with timeline of prompts and commits
- `page-001.html`, `page-002.html`, etc. - Paginated transcript pages with full conversation details

### Important Notes

1. **Session Timing**: The transcript captures the session state at the moment of export. Any conversation that happens *after* running the script won't be included in that transcript.

2. **Current Session Detection**: The script automatically detects the most recent session in the current project directory. If run from within Claude Code, it will typically find the active session.

3. **GitHub Gist Publishing**: The `--gist` option requires the GitHub CLI (`gh`) to be installed and authenticated. Run `gh auth login` first if needed.

## Installation Requirements

The script uses `uvx` to run `claude-code-transcripts` without permanent installation. Requirements:

- **uv**: The fast Python package manager. Install via `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **gh** (optional): GitHub CLI for gist publishing. Install via `brew install gh` or see https://cli.github.com/

If `uv` is not available, the script falls back to `pip install claude-code-transcripts`.

## Usage Examples

### Save transcript to current directory
```bash
python scripts/save_transcript.py --output .
```

### Save with auto-generated directory name based on session ID
```bash
python scripts/save_transcript.py --output ./transcripts --auto-name
```

### Publish to gist and get shareable URL
```bash
python scripts/save_transcript.py --gist
# Outputs something like:
# Preview: https://gistpreview.github.io/?abc123def456/index.html
```

### Include the original JSON session file in output
```bash
python scripts/save_transcript.py --output ./archive --include-json
```

## Command Reference

```
save_transcript.py [OPTIONS]

Options:
  --output, -o DIR      Output directory for HTML files
  --gist                Upload to GitHub Gist and output preview URL
  --auto-name, -a       Auto-name output subdirectory based on session ID
  --include-json        Include original session JSON/JSONL in output
  --open                Open generated HTML in browser (default if no --output)
  --session-id ID       Specific session ID to export (default: most recent)
  --help                Show help message
```

## Troubleshooting

### "No sessions found"
- Ensure you're running from within a Claude Code session
- Check that `~/.claude/projects/` exists and contains session files

### "gh: command not found" (when using --gist)
- Install GitHub CLI: `brew install gh` or see https://cli.github.com/
- Authenticate: `gh auth login`

### "uv: command not found"
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Or the script will attempt to use pip as fallback
