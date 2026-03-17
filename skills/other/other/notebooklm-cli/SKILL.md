---
name: notebooklm-cli
description: Comprehensive CLI for Google NotebookLM including notebooks, sources, and generated artifacts (audio, reports, quizzes, flashcards, mind maps, slides, infographics, videos, data tables). Use when working with NotebookLM programmatically: managing notebooks/sources, generating artifacts, querying sources via chat, or importing research.
---

# NotebookLM CLI

## Overview

This skill provides complete access to Google NotebookLM through the `nlm` CLI.

Key capabilities:
- Manage notebooks and sources
- Query sources via chat (`nlm ask`)
- Generate artifacts (audio, report, quiz, flashcards, slide deck, infographic, etc.)
- Import sources via web/Drive research

## Quick Start

### Authentication

```bash
nlm login
```

### List Notebooks

```bash
nlm list --json
```

### Create Notebook + Add Sources

```bash
nlm create "My Research"
nlm source add --notebook <id> --url "https://example.com/article"
nlm source add --notebook <id> --text "Your content here" --title "My Notes"
```

### Ask a Question

```bash
nlm ask -n <id> --new "Summarize the key takeaways"
```

### Generate Content

```bash
nlm generate report -n <id> "briefing doc for stakeholders"
nlm generate audio -n <id> "deep dive overview"
```

## Authentication

| Command | Description |
|---------|-------------|
| `nlm login` | Authenticate with NotebookLM (opens Chrome) |
| `nlm auth check` | Validate local auth (optionally `--test`) |

Sessions are stored in `~/.notebooklm/storage_state.json` by default.

## Notebook Management

| Command | Description |
|---------|-------------|
| `nlm list` | List all notebooks (`--json` supported) |
| `nlm create "Title"` | Create a new notebook |
| `nlm rename -n <id> "New Title"` | Rename a notebook |
| `nlm delete -n <id>` | Delete a notebook |
| `nlm summary -n <id>` | AI-generated notebook summary |
| `nlm use <id>` | Set active notebook context |
| `nlm status` | Show active notebook + conversation |
| `nlm clear` | Clear active notebook context |

## Source Management

| Command | Description |
|---------|-------------|
| `nlm source list -n <id>` | List sources in a notebook |
| `nlm source add -n <id> --url "..."` | Add URL/YouTube source |
| `nlm source add -n <id> --text "..." --title "..."` | Add pasted text |
| `nlm source add-drive -n <id> --doc <doc-id>` | Add Google Drive doc |
| `nlm source add-research -n <id> "query"` | Web/Drive research + import |
| `nlm source guide <source-id>` | AI source summary + keywords |
| `nlm source fulltext <source-id>` | Full indexed text |
| `nlm source refresh <source-id>` | Refresh URL/Drive source |
| `nlm source wait <source-id>` | Wait for source processing |

## Content Generation (Artifacts)

Use `nlm generate <type>` to create artifacts from notebook sources.

```bash
nlm generate audio -n <id> "brief overview"
nlm generate report -n <id> "study guide"
nlm generate quiz -n <id> "focus on key definitions"
nlm generate flashcards -n <id> "core concepts"
nlm generate slide-deck -n <id> "stakeholder deck"
nlm generate infographic -n <id> "quick visual summary"
nlm generate data-table -n <id> "extract key metrics"
nlm generate mind-map -n <id> "concept map"
nlm generate video -n <id> "short explainer"
```

Add `--wait` to block until completion.

## Artifact Management

| Command | Description |
|---------|-------------|
| `nlm artifact list -n <id>` | List generated artifacts |
| `nlm artifact get <artifact-id>` | Get artifact details |
| `nlm artifact export <artifact-id>` | Export artifact to file |
| `nlm artifact delete <artifact-id>` | Delete artifact |
| `nlm artifact wait <artifact-id>` | Wait for completion |

## Chat

| Command | Description |
|---------|-------------|
| `nlm ask -n <id> --new "question"` | One-shot question |
| `nlm configure -n <id>` | Configure chat persona/response style |
| `nlm history -n <id>` | View/clear conversation history |

Use `--json` on `nlm ask` for structured responses with references.

## Research

Use research to discover and import sources automatically:

```bash
nlm source add-research -n <id> "topic" --mode deep
nlm research status
nlm research wait
```

## Claude Code Skill Integration

```bash
nlm skill install
nlm skill status
nlm skill show
nlm skill uninstall
```

## Output Formats

```bash
nlm list --json
nlm ask -n <id> --new "question" --json
```

## References

- [Command Reference](references/commands.md)
- [Troubleshooting](references/troubleshooting.md)
- [Workflows](references/workflows.md)
