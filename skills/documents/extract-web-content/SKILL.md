---
name: extract-web-content
description: >
  Extract clean web content as markdown using ezycopy CLI. Use when user asks to
  "extract this webpage", "save this article", "copy clean content from URL",
  "get markdown from this link", "convert webpage to markdown",
  provides a URL to extract content from, or wants to save web content to clipboard
  or file without ads and clutter.
model: claude-sonnet-4-5
allowed-tools:
  - Bash
  - AskUserQuestion
  - WebFetch
---

# EzyCopy CLI

Extracts clean markdown from URLs. Default: fast HTTP fetch. Use `--browser` for Chrome when needed.

## Usage

```
ezycopy <URL> [flags]
```

**Flags:**
- `--browser` — Use Chrome (for JS-heavy or authenticated sites)
- `-o <path>` — Save to file/directory (default: clipboard)
- `--no-images` — Strip image links
- `-t <duration>` — Timeout (default: 30s)

## When to use `--browser`

- Twitter/X, SPAs, or JS-rendered sites
- Authenticated/paywalled content
- If default returns empty or suspiciously short content

## Install

If not installed: `go install github.com/gupsammy/EzyCopyCLI/cmd/ezycopy@latest`
