---
name: repo2txt
description: Convert code repositories to formatted text for LLM analysis. Use when the user wants to send code to Gemini, Claude, or other LLMs for debugging, code review, or analysis. Triggers on phrases like "convert code to text", "repo to text", "format code for LLM", "send code to Gemini", or when analyzing code structure and contents for LLM consumption.
---

# Repo2txt

## Overview

This skill converts local code repositories into a formatted text file suitable for sending to LLMs like Gemini, Claude, or ChatGPT. It's similar to https://repo2txt.simplebasedomain.com/ but runs locally, giving you full control over file selection and formatting.

## Quick Start

### Basic Usage

Convert a repository to text and display in terminal:

```bash
python3 scripts/repo2txt.py /path/to/repo
```

Save to a file:

```bash
python3 scripts/repo2txt.py /path/to/repo -o output.txt
```

### Filter by Extensions

Only include specific file types:

```bash
python3 scripts/repo2txt.py /path/to/repo -e .py,.js,.ts
```

Exclude certain extensions:

```bash
python3 scripts/repo2txt.py /path/to/repo -x .test.js,.spec.ts
```

### Common Scenarios

**Debug a specific module:**
```bash
python3 scripts/repo2txt.py ./src/components -e .tsx,.ts -o component_debug.txt
```

**Analyze backend API:**
```bash
python3 scripts/repo2txt.py ./src/api -e .py -o api_analysis.txt
```

**Review configuration files:**
```bash
python3 scripts/repo2txt.py . -e .json,.yaml,.yml,.toml -o config_review.txt
```

## Output Format

The generated text file includes three sections:

1. **Repository Summary**: File counts, total lines, breakdown by file type
2. **Directory Structure**: Tree visualization of the file hierarchy
3. **File Contents**: Each file with its path, type, and full content

Example output structure:
```
================================================================================
REPOSITORY SUMMARY
================================================================================
Total Files: 42
Total Lines: 3,456
Total Size: 128.5 KB

Files by Type:
  TypeScript: 25
  JavaScript: 10
  JSON: 5
  CSS: 2

================================================================================
DIRECTORY STRUCTURE
================================================================================

└── src
    ├── components
    │   ├── Button.tsx
    │   └── Card.tsx
    └── utils
        └── helpers.ts

================================================================================
FILE CONTENTS
================================================================================

--------------------------------------------------------------------------------
File: src/components/Button.tsx
Type: React/TS
--------------------------------------------------------------------------------

[file content here]
```

## Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-o, --output` | Output file path | `-o analysis.txt` |
| `-e, --extensions` | Include only these extensions | `-e .py,.js` |
| `-x, --exclude-extensions` | Exclude these extensions | `-x .test.js` |
| `-i, --ignore` | Additional ignore patterns | `-i temp,*.bak` |
| `--no-tree` | Skip directory tree | `--no-tree` |
| `--no-summary` | Skip summary section | `--no-summary` |
| `--max-file-size` | Max file size in bytes | `--max-file-size 500000` |

## Default Ignore Patterns

The following are automatically ignored:
- Version control: `.git`, `.svn`, `.hg`
- Dependencies: `node_modules`, `vendor`, `__pycache__`, virtual environments
- Build outputs: `dist`, `build`, `target`, `.next`, `.nuxt`
- IDE files: `.idea`, `.vscode`
- Lock files: `package-lock.json`, `yarn.lock`, `poetry.lock`, etc.
- Binary files: images, fonts, videos, archives
- Large data files: CSV, large JSON files

## Resources

### scripts/

- **repo2txt.py**: Main script for converting repositories to formatted text. Supports filtering by extensions, custom ignore patterns, and various output options.

## Usage Tips

1. **For Gemini/Claude**: Most LLMs have context limits. If your repo is large, filter to specific directories or file types.

2. **Focus on relevant code**: Use `-e` to include only the file types relevant to your question.

3. **Skip generated files**: The default ignore patterns handle most build artifacts and dependencies.

4. **Copy to clipboard** (macOS):
   ```bash
   python3 scripts/repo2txt.py . -e .py | pbcopy
   ```

5. **Copy to clipboard** (Linux):
   ```bash
   python3 scripts/repo2txt.py . -e .py | xclip -selection clipboard
   ```
