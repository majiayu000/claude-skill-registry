---
name: mdpreview
description: "Catppuccin-themed live-reloading Markdown viewer with multi-tab support, margin annotations, sidebar TOC, and Chrome --app mode. This skill should be used when previewing .md files in a polished editorial reader, adding AI or human annotations to documents, or launching a collaborative document review session."
argument-hint: <file.md> [file2.md ...] [--port PORT] [--author NAME]
allowed-tools: Bash(python3*), Read, Glob, Write
---

# mdpreview — Markdown Preview & Annotate

Catppuccin Mocha/Latte live-reloading Markdown viewer with multi-tab support and Google Docs-style margin annotations.

> **Canonical repo**: [github.com/tdimino/dabarat](https://github.com/tdimino/dabarat). Clone it or ensure `md_preview_and_annotate` is on your PYTHONPATH.

## Quick Start

```bash
# Preview one or more files
python3 -m md_preview_and_annotate file.md [file2.md ...] --port 3031

# If not installed globally, run from the cloned repo:
python3 ~/Desktop/Programming/md-preview-and-annotate/md_preview_and_annotate/__main__.py file.md
```

### Add a file to a running server

```bash
python3 -m md_preview_and_annotate --add another.md --port 3031
```

### Add an annotation from CLI (no server needed)

```bash
python3 -m md_preview_and_annotate --annotate file.md \
  --text "RPL §235-b" --author "Claude" --comment "Cite the specific subsection"
```

This writes directly to the sidecar JSON (`file.md.annotations.json`). The live viewer picks it up on the next 500ms poll cycle.

## Features

| Feature | Details |
|---------|---------|
| **Live reload** | 500ms polling, auto-refreshes on file save |
| **Multi-tab** | Open multiple .md files, switch tabs, add/close at runtime |
| **Tab reuse** | Launching a new file while the server is running adds it as a tab |
| **Annotations** | Right-margin comment bubbles with author badges (human/AI) |
| **Threaded replies** | Reply to any annotation inline |
| **Bookmarks** | Global persistence to `~/.claude/bookmarks/` with INDEX.md |
| **Sidecar JSON** | Annotations persisted in `file.md.annotations.json` alongside source |
| **File tagging** | 7 predefined + custom tags via command palette `#` prefix |
| **Command palette** | `Cmd+K` / `Ctrl+K` for quick access to commands, tabs, and recent files |
| **Catppuccin** | Full Mocha (dark) / Latte (light) theme with 26 CSS variables |
| **Typography** | Cormorant Garamond headings, DM Sans body, Victor Mono code |
| **Sidebar TOC** | Resizable table of contents with scroll-spy |
| **Code highlighting** | highlight.js with Catppuccin syntax theme |
| **Chrome --app** | Opens in frameless Chrome window for native feel |
| **Cross-file links** | Local `.md` links open in new tabs instead of navigating away |

## Annotation System

To create annotations interactively, select text in the viewer — a floating button appears, then fill in the comment form in the right gutter.

To create annotations programmatically (e.g., from Claude Code), use the `--annotate` CLI flag. This requires no running server — it writes directly to the sidecar JSON.

- **Human authors** — blue name badge
- **AI authors** — mauve name badge with robot icon
- **Actions** — resolve (toggle strikethrough) or delete (trash icon), revealed on hover
- **Persistence** — sidecar JSON file, auto-loaded on viewer refresh or file poll

### Sidecar JSON Schema

```json
{
  "version": 1,
  "tags": ["draft", "research"],
  "annotations": [
    {
      "id": "a1b2c3",
      "anchor": { "text": "selected phrase", "heading": "", "offset": 0 },
      "author": { "name": "Claude", "type": "ai" },
      "created": "2026-02-12T15:30:00+00:00",
      "body": "Comment text here",
      "resolved": false,
      "replies": []
    }
  ]
}
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/content?tab=<id>` | GET | Markdown content for a tab |
| `/api/tabs` | GET | List open tabs |
| `/api/annotations?tab=<id>` | GET | Annotations for a tab |
| `/api/tags?tab=<id>` | GET | Tags for a tab |
| `/api/add` | POST | Open a new file tab |
| `/api/close` | POST | Close a tab |
| `/api/annotate` | POST | Create an annotation |
| `/api/resolve` | POST | Toggle annotation resolved state |
| `/api/reply` | POST | Add a threaded reply |
| `/api/delete-annotation` | POST | Delete an annotation |
| `/api/tags` | POST | Add/remove a tag |
