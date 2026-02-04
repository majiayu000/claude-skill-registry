---
name: write-markdown-output
description: Write content to a timestamped markdown file. Use when agents need to save plans, reviews, or other outputs.
user-invocable: true
argument-hint: <-s "scope" -c "content" -o "output-dir">
---

# Write Markdown Output

Write content to a markdown file with a UTC timestamp in the filename.

## Quick Reference

| Input | Description |
|-------|-------------|
| `-s`, `--scope` | Scope/title for the filename (e.g., "sql-validation-plan") |
| `-c`, `--content` | Markdown content to write |
| `-o`, `--output-dir` | Output directory path |

## Output Format

Files are written to: `<output-dir>/<timestamp>-<scope>.md`

| Format | Example |
|--------|---------|
| Timestamp | `2026-02-02T025204Z` |
| Full path | `.claude/agent-outputs/plans/2026-02-02T025204Z-sql-validation-plan.md` |

## Usage

```bash
# Write a plan
uv run python .claude/skills/write-markdown-output/scripts/write_markdown_output.py \
    -s "sql-validation-plan" \
    -c "# Plan\n\nPlan content here..." \
    -o ".claude/agent-outputs/plans"

# Write a review
uv run python .claude/skills/write-markdown-output/scripts/write_markdown_output.py \
    -s "parser-review" \
    -c "# Review\n\nReview content here..." \
    -o ".claude/agent-outputs/reviews"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | File written successfully |
| 1 | Error writing file |
| 2 | Usage error (missing arguments) |

## Output

On success, prints the full path to the created file:

```
[WRITTEN] .claude/agent-outputs/plans/2026-02-02T025204Z-sql-validation-plan.md
```

## Python Function

```python
from datetime import datetime, timezone
from pathlib import Path

def write_markdown_output(scope: str, content: str, output_dir: Path | str) -> Path:
    """Write content to a timestamped markdown file.

    Args:
        scope: Scope/title for the filename (e.g., "sql-validation-plan").
        content: Markdown content to write.
        output_dir: Output directory path.

    Returns:
        Path: Full path to the created file.
    """
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"{timestamp}-{scope}.md"
    file_path = output_path / filename
    file_path.write_text(content, encoding="utf-8")

    return file_path
```

## Agent Workflow

1. Generate content (plan, review, PR description, etc.)
2. Determine appropriate output directory
3. Call this skill to write the file
4. Report the file path to the user

## Output Directories

| Content Type | Directory |
|--------------|-----------|
| Plans | `.claude/agent-outputs/plans/` |
| Reviews | `.claude/agent-outputs/reviews/` |
| PR Descriptions | `.claude/agent-outputs/pr-descriptions/` |
