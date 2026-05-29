---
name: forge-help
description: Show all available Product Forge agents, skills, and commands
short: List all tools in Product Forge
argument-hint: "[search-term]"
keywords: help, list, find, search, index, tools, available
---

# forge-help

Display the Product Forge index - a quick reference for all available tools.

## Usage

```
/forge-help              # Show full index
/forge-help security     # Filter by keyword
/forge-help django       # Find Django-related tools
```

## Execution

Read and display `forge-index.md` from this plugin directory.

If a search term is provided, filter to show only matching entries.

## Regenerating the Index

Run the script to update the index after adding new agents/skills/commands:

```bash
python scripts/generate-forge-index.py --plugins-dir plugins --output plugins/product-design/forge-index.md
```
