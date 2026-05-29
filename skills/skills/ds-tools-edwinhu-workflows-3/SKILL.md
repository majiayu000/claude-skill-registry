---
name: ds-tools
description: "This skill should be used when the user asks 'what data science tools are available', 'list data analysis plugins', 'what skills work with data', 'enable data science code intelligence', or needs to discover data-specific plugins and skills like wrds, lseg-data, gemini-batch, or data context skills. Use this for data science tool discovery; use dev-tools for general development tool discovery."
user-invocable: false
---

# Available Data Science Tools

Plugins and skills for data science workflows. For general development tools (testing, automation), see `/dev-tools`.

## Code Intelligence Plugins

| Plugin | Description | Enable Command |
|--------|-------------|----------------|
| `serena` | Semantic code analysis, symbol navigation | `claude --enable-plugin serena@claude-plugins-official` |
| `pyright-lsp` | Python type checking and diagnostics | `claude --enable-plugin pyright-lsp@claude-plugins-official` |
| `context7` | Up-to-date library docs (pandas, numpy, sklearn, etc.) | `claude --enable-plugin context7@claude-plugins-official` |

## Data Access Skills (Built-in)

These are skills, not plugins - already available:

| Skill | Description |
|-------|-------------|
| `/wrds` | WRDS (Wharton Research Data Services) queries |
| `/lseg-data` | LSEG Data Library (formerly Refinitiv) |
| `/gemini-batch` | Gemini Batch API for large-scale LLM processing |
| `/data-context` | Extract tribal knowledge about datasets, generate data context skills |

## Notebook & Format Skills (Built-in)

| Skill | Description |
|-------|-------------|
| `/jupytext` | Jupyter notebooks as text files |
| `/marimo` | Marimo reactive Python notebooks |
| `/xlsx` | Spreadsheets, formulas, CSV conversion |
| `/pdf` | PDF extraction, creation, form filling |
| `/docx` | Word docs, tracked changes, reports |

## When to Enable Plugins

- **serena**: Understanding complex analysis codebases, refactoring pipelines
- **context7**: Access current docs for pandas, scikit-learn, statsmodels
- **pyright-lsp**: Type check data pipelines

## Usage

```bash
claude --enable-plugin <plugin-name>  # Enable for current session
```
