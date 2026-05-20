---
name: open-in-editor
description: Use when the user says "open", "show me", "nvr", "open in editor", "open in nvr", "open in neovim", or wants to view a file in their editor rather than in the CLI. Also use proactively after creating or editing a file the user will want to review.
---

# Open in Editor (nvr)

Opens files in the user's neovim instance via `nvr`, using the tmux window name to find the correct socket.

## Usage

```bash
# Open in new tab (default)
~/dots/bin/scripts/llm-open-nvr /path/to/file

# Open at specific line
~/dots/bin/scripts/llm-open-nvr --line 42 /path/to/file

# Open in split / vsplit
~/dots/bin/scripts/llm-open-nvr --split /path/to/file
~/dots/bin/scripts/llm-open-nvr --vsplit /path/to/file

# Diff two files
~/dots/bin/scripts/llm-open-nvr --diff file1 file2

# Send keystrokes (e.g. save current buffer)
~/dots/bin/scripts/llm-open-nvr --send ':w<CR>'

# Evaluate neovim expression
~/dots/bin/scripts/llm-open-nvr --expr 'expand("%:p")'
```

## Error Handling

If the script errors with "No nvr socket", ask the user to start neovim in this tmux window by running the `nvr` shell function.
