---
name: csctf
description: "Chat Shared Conversation To File - convert ChatGPT, Gemini, Grok, and Claude share links to clean Markdown + HTML transcripts with preserved code fences."
---

# csctf Skill

Convert public AI chat share links into clean, portable Markdown and HTML files. Preserves code blocks with language detection, generates deterministic filenames, and optionally publishes to GitHub Pages.

## Supported Providers

| Provider | URL Pattern | Method |
|----------|-------------|--------|
| **ChatGPT** | `chatgpt.com/share/*` | Headless Chromium |
| **Gemini** | `gemini.google.com/share/*` | Headless Chromium |
| **Grok** | `grok.com/share/*` | Headless Chromium |
| **Claude** | `claude.ai/share/*` | Your Chrome (uses session cookies) |

## Basic Usage

```bash
# Convert any share link to Markdown + HTML
csctf https://chatgpt.com/share/69343092-91ac-800b-996c-7552461b9b70

# Gemini conversation
csctf https://gemini.google.com/share/66d944b0e6b9

# Grok conversation
csctf https://grok.com/share/bGVnYWN5_d5329c61-f497-40b7-9472-c555fa71af9c

# Claude conversation (requires Chrome login)
csctf https://claude.ai/share/549c846d-f6c8-411c-9039-a9a14db376cf
```

Output:
- `<conversation_title>.md` - Clean Markdown with preserved code fences
- `<conversation_title>.html` - Styled static HTML (no JavaScript)

## Output Options

```bash
# Markdown only (skip HTML)
csctf <url> --md-only

# HTML only (skip Markdown)
csctf <url> --html-only

# Custom output path
csctf <url> --outfile ~/exports/my_chat.md

# Quiet mode (minimal logging)
csctf <url> --quiet
```

## Timeout Control

```bash
# Default is 60 seconds
csctf <url> --timeout-ms 60000

# For slow/large conversations
csctf <url> --timeout-ms 90000

# Very long conversations
csctf <url> --timeout-ms 120000
```

## GitHub Pages Publishing

Publish conversations to a GitHub Pages site with auto-generated index:

```bash
# Publish with defaults (creates my_shared_conversations repo)
csctf <url> --publish-to-gh-pages --yes

# Custom repo
csctf <url> --publish-to-gh-pages --gh-pages-repo myuser/my-chats --yes

# Custom branch and directory
csctf <url> --publish-to-gh-pages --gh-pages-branch main --gh-pages-dir exports --yes

# Remember settings for future runs
csctf <url> --publish-to-gh-pages --remember --yes

# Then just use --yes for subsequent runs
csctf <url> --yes

# Clear remembered settings
csctf --forget-gh-pages

# Dry run (build index without pushing)
csctf <url> --publish-to-gh-pages --dry-run
```

Requirements for publishing:
- GitHub CLI (`gh`) installed and authenticated
- Run `gh auth status` to verify

## All Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--timeout-ms` | `60000` | Navigation + selector timeout |
| `--outfile` | auto | Override output path |
| `--no-html` / `--md-only` | off | Skip HTML output |
| `--html-only` | off | Skip Markdown output |
| `--quiet` | off | Minimal logging |
| `--check-updates` | off | Check for new version |
| `--version` | — | Print version |
| `--publish-to-gh-pages` | off | Publish to GitHub Pages |
| `--gh-pages-repo` | auto | Target repo (owner/name) |
| `--gh-pages-branch` | `gh-pages` | Target branch |
| `--gh-pages-dir` | `csctf` | Subdirectory in repo |
| `--remember` | off | Save GH settings |
| `--forget-gh-pages` | off | Clear saved settings |
| `--dry-run` | off | Simulate publish |
| `--yes` | off | Skip confirmation prompt |
| `--gh-install` | off | Auto-install `gh` CLI |

## Output Format

### Markdown Structure

```markdown
# Conversation: <Title>

**Source:** https://chatgpt.com/share/...
**Retrieved:** 2026-01-04T15:30:00Z

## User

How do I sort an array in Python?

## Assistant

Here's how to sort an array in Python:

```python
# Sort in place
my_list.sort()

# Return new sorted list
sorted_list = sorted(my_list)
```
```

### HTML Features

- Standalone (no external dependencies)
- Zero JavaScript
- Inline CSS with light/dark mode support
- Syntax highlighting via highlight.js (inline)
- Table of contents
- Print-friendly styles
- Language badges on code blocks

## Filename Generation

Filenames are automatically generated from conversation titles:
- Lowercased
- Non-alphanumerics → `_`
- Trimmed, max 120 chars
- Collision handling: `_2`, `_3`, etc.

Examples:
```
"How to Build a REST API" → how_to_build_a_rest_api.md
"Python Tips & Tricks!"   → python_tips_tricks.md
```

## Clawdbot Workflows

### "Save this ChatGPT conversation"

```
User: Can you save this conversation? https://chatgpt.com/share/abc123...

Clawdbot: *Uses csctf to download and convert*
csctf "https://chatgpt.com/share/abc123..." --outfile ~/Documents/chats/
```

### "Archive all my shared chats"

```bash
# Save multiple conversations
csctf https://chatgpt.com/share/abc... --outfile ~/archive/
csctf https://gemini.google.com/share/xyz... --outfile ~/archive/
csctf https://claude.ai/share/def... --outfile ~/archive/
```

### "Publish to my blog"

```bash
csctf https://chatgpt.com/share/abc... \
  --publish-to-gh-pages \
  --gh-pages-repo myuser/ai-conversations \
  --yes
```

### "Quick export for reference"

```bash
# Just get the markdown, skip HTML
csctf https://chatgpt.com/share/abc... --md-only --quiet
```

## Performance Notes

- **First run**: Downloads Playwright Chromium (~200MB, cached)
- **Subsequent runs**: 5-15 seconds depending on conversation length
- **Claude.ai**: Uses your installed Chrome (bypasses Cloudflare)

## Claude.ai Special Handling

Claude.ai uses Cloudflare protection. csctf handles this by:
1. Copying your Chrome session cookies to a temp profile
2. Launching Chrome with remote debugging
3. Extracting conversation via Chrome DevTools Protocol

Requirements:
- Chrome installed
- Logged into claude.ai in your regular Chrome session
- If Chrome is running, tool will offer to save tabs, restart, and restore

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No messages found" | Link may be private or expired; verify it opens in browser |
| Timeout errors | Use `--timeout-ms 90000` for slow/large conversations |
| Claude.ai won't load | Ensure you're logged into claude.ai in Chrome |
| Cloudflare challenge | Complete challenge in Chrome window, press Enter |
| Publish auth fails | Run `gh auth status` to verify GitHub CLI login |
| Filename collisions | Normal - tool appends `_2`, `_3`, etc. |

## File Locations

- **Config**: `~/.config/csctf/config.json` (GitHub Pages settings)
- **Playwright cache**: `~/.cache/ms-playwright/`
- **Output**: Current directory (or `--outfile` path)

## Requirements

- Bun 1.3+ or prebuilt binary
- macOS, Linux, or Windows
- Chrome (for Claude.ai shares only)
- GitHub CLI (`gh`) for publishing (optional)
