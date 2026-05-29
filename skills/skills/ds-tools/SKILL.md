---
name: ds-tools
description: This skill should be used when the user asks "what plugins are available", "list data science tools", "what MCP servers can I use", "enable code intelligence", or needs to discover available plugins like serena, context7, or data access skills like wrds and lseg-data.
---

# Available Data Science Plugins

These plugins extend Claude Code capabilities for data science workflows. Enable when needed.

## Code Intelligence

| Plugin | Description | Enable Command |
|--------|-------------|----------------|
| `serena` | Semantic code analysis, refactoring, symbol navigation | `claude --enable-plugin serena@claude-plugins-official` |
| `pyright-lsp` | Python type checking and diagnostics | `claude --enable-plugin pyright-lsp@claude-plugins-official` |

## Documentation

| Plugin | Description | Enable Command |
|--------|-------------|----------------|
| `context7` | Up-to-date library docs (pandas, numpy, sklearn, etc.) | `claude --enable-plugin context7@claude-plugins-official` |

## Web & Automation

| Plugin | Description | Enable Command |
|--------|-------------|----------------|
| `playwright` | Web scraping, browser automation, screenshots | `claude --enable-plugin playwright@claude-plugins-official` |

## Workflow

| Plugin | Description | Enable Command |
|--------|-------------|----------------|
| `ralph-loop` | Self-referential iteration loops | Already enabled |
| `hookify` | Create custom hooks from conversation patterns | Already enabled |

## Data Access Skills (Built-in)

These are skills, not plugins - already available via `/ds`:

| Skill | Description |
|-------|-------------|
| `/wrds` | WRDS (Wharton Research Data Services) queries |
| `/lseg-data` | LSEG Data Library (formerly Refinitiv) |
| `/gemini-batch` | Gemini Batch API for large-scale LLM processing |
| `/jupytext` | Jupyter notebooks as text files |
| `/marimo` | Marimo reactive Python notebooks |

## File Format Skills (Bundled)

Office document and PDF skills from Anthropic's official skills repo (bundled via submodule):

| Skill | Use For |
|-------|---------|
| `/xlsx` | Spreadsheets, formulas, CSV→Excel conversion |
| `/pdf` | PDF extraction, creation, form filling |
| `/pptx` | Presentation creation and editing |
| `/docx` | Word docs, tracked changes, reports |

These skills are available via the `shared` plugin - no separate installation needed.

## When to Enable

- **serena**: Understanding complex analysis codebases, refactoring pipelines
- **context7**: Access current docs for pandas, scikit-learn, statsmodels, and other libraries
- **playwright**: Scrape web data sources, automate data collection
- **pyright-lsp**: Type check data pipelines

## Usage

Enable a plugin for the current session:
```bash
claude --enable-plugin <plugin-name>  # Enable a plugin by name and source
```

Enable a plugin for a project by adding to `.claude/settings.json`:
```json
{
  "enabledPlugins": {
    "serena@claude-plugins-official": true
  }
}
```
