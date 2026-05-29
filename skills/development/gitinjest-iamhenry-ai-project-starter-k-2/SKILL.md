---
name: gitinjest
description: Analyze GitHub repositories by converting to LLM-readable text. TRIGGER when user pastes github.com URL, asks "how does [library] work", or references external codebases. Supports public/private repos and subdirectories.
---

# Gitingest

## TRIGGER CONDITIONS

USE when user message contains:
- `github.com/` URL
- "look at this repo" or "analyze this codebase"
- Questions about third-party library internals

SKIP when:
- URL is user's own project
- User just wants to clone/fork

Convert GitHub repos into text format using the CLI. By default, gitingest writes to `digest.txt`; use `-o -` to stream to stdout.

## STREAMING ONLY (HARD DEFAULT)

ALWAYS stream to stdout with `-o -`. DO NOT:
- Clone repos locally
- Write output files (`-o file.txt`)
- Redirect to disk (`> out.txt`)
- Create temp files

Only write to disk if user EXPLICITLY requests it.

```bash
# CORRECT: streams to stdout (recommended default)
gitingest https://github.com/user/repo -o -
gitingest https://github.com/user/repo -i "*.ts" -o -

# WRONG - writes to disk (avoid unless user asks)
gitingest https://github.com/user/repo -o output.txt
gitingest https://github.com/user/repo > dump.txt
```

# Gitingest CLI Commands for External Codebase Analysis

Key lesson: Always search broadly first (-i "*.ts" for TypeScript, -i "*.py" for Python, etc.) before narrowing down. The commands are powerful, but your search scope determines what you find.

## Installation

```bash
pipx install gitingest
```

### Linux Notes

- If `pip install --user` fails with PEP 668 error, use `pipx install gitingest` instead.
- If `gitingest: command not found` after `pipx install`, ensure `~/.local/bin` is on PATH. Run `pipx ensurepath`, restart your shell, then verify `command -v gitingest`.
- Verify: `gitingest --help` or `pipx list | grep gitingest`

## Default Usage (Streaming to stdout)

```bash
# Stream output directly (no file created)
gitingest https://github.com/username/repo -o -

# Capture in variable for processing
output=$(gitingest https://github.com/username/repo -o -)
```

## Private Repositories

```bash
# Set token as environment variable
export GITHUB_TOKEN=github_pat_...
gitingest https://github.com/username/private-repo -o -

# Or pass directly
gitingest https://github.com/username/private-repo --token github_pat_... -o -
```

## Subdirectories

```bash
# Analyze only specific part of repo
gitingest https://github.com/user/repo/tree/main/src -o -
```

## Basic Usage

- `gitingest https://github.com/user/repo -o -` - Get full repo overview (stdout)
- `gitingest https://github.com/user/repo --include-submodules -o -` - Include submodules

## File/Content Search

- `gitingest https://github.com/user/repo -i "pattern" -o -` - Search files containing pattern
- `gitingest https://github.com/user/repo -i "*filename*" -o -` - Find files by name/glob
- `gitingest https://github.com/user/repo -i "path/to/file" -o -` - Get specific file content

## Filtering

- `gitingest https://github.com/user/repo -e "pattern" -o -` - Exclude files matching pattern
- `gitingest https://github.com/user/repo -i "*.ts" -e "node_modules/*" -o -` - Include TS files, exclude node_modules


## Key Options

- `-o -` or `--output -`: Stream to stdout (no temp file)
- `--token` or `-t`: GitHub token for private repos
- `--include-submodules`: Include git submodules
- `--include-gitignored`: Include files normally ignored by .gitignore

## Output Structure

The CLI returns formatted text with:
- Summary: File count, size, token count
- Tree: Directory visualization
- Content: All code combined and formatted
