---
title: Pandoc Wizard
description: A modular CLI wizard for constructing and running complex Pandoc commands, specifically focused on HTML chunking and Lua filters.
tool_name: pandoc-wizard
---

# Pandoc Wizard

This tool provides a guided interface for using Pandoc, helping you select files, apply Lua filters, and configure chunking options without remembering all the command-line flags.

## Usage

Run the wizard interactively:

```bash
python "C:\Users\matts\AI Workspace\custom_tools\pandoc_wizard\pandoc_wizard.py"
```

## Modules

### HTML Chunking
- Select an input HTML file.
- Choose a split level (headers 1-6).
- Apply Lua filters from your `AI Workspace\pandoc-lua-filters` directory.
- Generate the command and run it.
