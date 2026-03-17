---
name: gitingest
description: Use when the user wants to fetch and contextualize a GitHub repository for future reference.
argument-hint: [url | user/repo | repo-name] [filters...]
allowed-tools:
  - Bash(mkdir docs/reference)
  - Bash(gitingest:*)
  - Read
---

# Fetch GitHub Repository Context

## Arguments

```
$ARGUMENTS
```

## Instructions

### 1. Parse Input
- **Full URL**: use directly
- **user/repo**: construct `https://github.com/{user/repo}`
- **Single name**: infer canonical repo (e.g., "rails" → "rails/rails"); if ambiguous, ask

### 2. Parse Filters
Natural language filters map to options:
- "only Python files" → `-i "*.py"`
- "exclude tests" → `-e "test/*" -e "*_test.py"`
- "branch develop" → `-b develop`

### 3. Build Command
```bash
mkdir -p docs/reference/
gitingest [OPTIONS] -o docs/reference/<user>-<repo>.txt <url>
```

**Options:**
| Flag | Purpose |
|------|---------|
| `-o PATH` | Output file (required) |
| `-i PATTERN` | Include pattern (repeatable) |
| `-e PATTERN` | Exclude pattern (repeatable) |
| `-b NAME` | Branch |
| `-s BYTES` | Max file size |
| `--include-gitignored` | Include .gitignore'd files |
| `--include-submodules` | Include submodules |
| `-t TOKEN` | GitHub PAT for private repos |

### 4. Execute & Confirm
1. Run the command
2. Read generated file to understand repo
3. Report: repo name, purpose, file location, filters applied

## Examples

```
/gitingest rails                    → rails/rails to docs/reference/rails-rails.txt
/gitingest jdx/mise only rust       → -i "*.rs" filter
/gitingest user/repo exclude tests  → -e "test/*" -e "*_test.py"
/gitingest https://github.com/x/y branch main
```
