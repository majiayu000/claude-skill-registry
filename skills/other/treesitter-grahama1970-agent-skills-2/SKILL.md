---
name: treesitter
description: >
  Parse and extract code symbols using tree-sitter. Use when you need to extract
  functions, classes, or understand code structure from files or code blocks.
allowed-tools: Bash, Read
triggers:
  - parse this code
  - extract functions from
  - list symbols in
  - what functions are in
  - code structure
  - parse with treesitter
metadata:
  short-description: Parse code with tree-sitter for symbol extraction
---

# Treesitter Skill

Parse code files or snippets using tree-sitter to extract symbols (functions, classes, methods).

## Quick Start

```bash
# Extract symbols from a file
.agents/skills/treesitter/run.sh symbols /path/to/file.py --json

# Extract with full source code
.agents/skills/treesitter/run.sh symbols /path/to/file.py --content --json

# Scan a directory
.agents/skills/treesitter/run.sh scan /path/to/dir --json

# Parse a code snippet (writes to temp file)
.agents/skills/treesitter/run.sh parse --language python --code "def foo(): pass" --json
```

## Commands

| Command | Description |
|---------|-------------|
| `symbols <path>` | Extract functions/classes from a file |
| `scan <dir>` | Walk directory, summarize symbols per file |
| `parse --code "..." --language <lang>` | Parse a code snippet |

## Options

| Option | Description |
|--------|-------------|
| `--content`, `-c` | Include full source code of symbols |
| `--language` | Override auto-detected language |
| `--json` | Output JSON format |
| `--max-chunk-size` | Max chars for content chunks |

## Auto-Install

This skill uses `uvx` to automatically install treesitter-tools from git.
No pre-installation required.

## Integration with Distill

The distill skill can use treesitter to properly extract and parameterize
code blocks from documents, storing them with their language and structure.

## Supported Languages

Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, and more.
Language is auto-detected from file extension or can be specified with `--language`.
