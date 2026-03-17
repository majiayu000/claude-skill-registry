---
name: file-suggestion
description: Set up fast file suggestions for Claude Code using ripgrep, jq, and fzf. Use this skill when users want to improve file autocomplete performance or add custom file suggestion behavior.
---

# File Suggestion Setup

This skill helps you configure Claude Code's file suggestion feature with a custom script that uses ripgrep, jq, and fzf for fast fuzzy file matching.

## Prerequisites

Install these tools before setup:

```bash
# Ubuntu/Debian
sudo apt install ripgrep jq fzf

# macOS
brew install ripgrep jq fzf

# Arch Linux
sudo pacman -S ripgrep jq fzf
```

## Setup Steps

### 1. Create the Script

Create the file suggestion script at `~/.claude/file-suggestion.sh`:

```bash
#!/bin/bash
# Custom file suggestion script for Claude Code
# Uses rg + fzf for fuzzy matching and symlink support

# Parse JSON input to get query
QUERY=$(jq -r '.query // ""')

# Use project dir from env, fallback to pwd
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

# cd into project dir so rg outputs relative paths
cd "$PROJECT_DIR" || exit 1

{
  # Main search - respects .gitignore, includes hidden files, follows symlinks
  rg --files --follow --hidden . 2>/dev/null

  # Additional paths - include even if gitignored (uncomment and customize)
  # [ -e .notes ] && rg --files --follow --hidden --no-ignore-vcs .notes 2>/dev/null
} | sort -u | fzf --filter "$QUERY" | head -15
```

### 2. Make It Executable

```bash
chmod +x ~/.claude/file-suggestion.sh
```

### 3. Configure Claude Code

Add this to your `~/.claude/settings.json`:

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

## How It Works

The script:

1. **Receives JSON input** with a `query` field from Claude Code
2. **Uses ripgrep** (`rg --files`) to list files fast, respecting `.gitignore`
3. **Follows symlinks** with `--follow` flag
4. **Includes hidden files** with `--hidden` flag
5. **Fuzzy filters** results using `fzf --filter`
6. **Returns top 15 matches** sorted by relevance

## Customization

### Include Gitignored Paths

Uncomment and customize the additional paths section:

```bash
# Include .notes directory even if gitignored
[ -e .notes ] && rg --files --follow --hidden --no-ignore-vcs .notes 2>/dev/null

# Include vendor directory
[ -e vendor ] && rg --files --follow --hidden --no-ignore-vcs vendor 2>/dev/null
```

### Exclude Patterns

Add ripgrep glob patterns to exclude files:

```bash
rg --files --follow --hidden \
   --glob '!*.min.js' \
   --glob '!*.map' \
   --glob '!node_modules' \
   . 2>/dev/null
```

### Change Result Limit

Modify the `head -15` to return more or fewer results:

```bash
# Return top 25 matches
... | head -25
```

## Troubleshooting

### Script Not Found

Ensure the path in settings.json matches your script location and uses `~` or absolute path.

### No Results

Check that:
- ripgrep is installed: `which rg`
- fzf is installed: `which fzf`
- jq is installed: `which jq`
- Script is executable: `ls -la ~/.claude/file-suggestion.sh`

### Slow Performance

If you have a large repo:
- Ensure `.gitignore` excludes `node_modules`, `dist`, etc.
- Add explicit `--glob '!pattern'` exclusions for large directories

## Template Script

A ready-to-use template is available at:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/file-suggestion/scripts/file-suggestion.sh
```

Copy it to your `~/.claude/` directory and customize as needed.
