---
name: exploring-codebases
description: Semantic search for codebases. Locates matches with ripgrep and expands them into full AST nodes (functions/classes) using tree-sitter. Returns complete, syntactically valid code blocks rather than fragmented lines. Use when looking for specific implementations, examples, or references where full context is needed.
metadata:
  version: 0.2.0
---

# Exploring Codebases

Hybrid search tool that combines the speed of `ripgrep` with the structural awareness of `tree-sitter`. It finds matches and returns the *entire* function or class containing the match, de-duplicating results semantically.

## Progressive Disclosure

**By default, returns signatures only** (docstrings + declarations without function bodies), reducing token usage by 10-20×. Use `--expand-full` to get complete implementations when needed.

## Installation

```bash
uv venv /home/claude/.venv
uv pip install tree-sitter-language-pack --python /home/claude/.venv/bin/python
```

## Usage

```bash
# Default: signatures only (efficient)
/home/claude/.venv/bin/python /mnt/skills/user/exploring-codebases/scripts/search.py "query" /path/to/repo

# Full implementations
/home/claude/.venv/bin/python /mnt/skills/user/exploring-codebases/scripts/search.py "query" /path/to/repo --expand-full
```

## Options

- `--glob pattern`: Filter files (e.g., `*.py`, `*.ts`)
- `--expand-full`: Return full implementations instead of signatures
- `--json`: Output JSON for machine processing (default is Markdown)

## Examples

**Find class signatures:**
```bash
/home/claude/.venv/bin/python /mnt/skills/user/exploring-codebases/scripts/search.py "class User" /path/to/repo
```

Output:
```python
class User:
    """User account model."""
    ...
```

**Find full method implementation:**
```bash
/home/claude/.venv/bin/python /mnt/skills/user/exploring-codebases/scripts/search.py "def validate" /path/to/repo --expand-full
```

**Find usage of `process_data` in Python files:**
```bash
/home/claude/.venv/bin/python /mnt/skills/user/exploring-codebases/scripts/search.py "process_data" /path/to/repo --glob "*.py"
```
