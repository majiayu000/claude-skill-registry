---
name: csctf
description: "Chat Shared Conversation To File - Convert ChatGPT, Gemini, Grok, and Claude share links to clean Markdown + HTML transcripts. Preserves code fences with language detection, deterministic filenames, GitHub Pages publishing. Bun-native CLI."
---

# CSCTF — Chat Shared Conversation To File

A Bun-native CLI that turns public ChatGPT, Gemini, Grok, and Claude share links into clean Markdown + HTML transcripts with preserved code fences, stable filenames, and optional GitHub Pages publishing.

## Why This Exists

Copy/pasting AI share links often:
- **Breaks fenced code blocks** — loses formatting and structure
- **Loses language hints** — no syntax highlighting
- **Produces messy filenames** — random or unreadable names
- **Requires manual cleanup** — inconsistent formatting

CSCTF fixes this with:
- **Stable slugs** — deterministic, collision-proof filenames
- **Language-preserving fences** — code blocks retain syntax hints
- **Normalized whitespace** — clean, consistent output
- **Static HTML twin** — no JS, ready for hosting/archiving
- **One-command GitHub Pages** — instant shareable microsite

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/chat_shared_conversation_to_file/main/install.sh | bash

# Convert any share link
csctf https://chatgpt.com/share/69343092-91ac-800b-996c-7552461b9b70
csctf https://gemini.google.com/share/66d944b0e6b9
csctf https://grok.com/share/bGVnYWN5_d5329c61-f497-40b7-9472-c555fa71af9c
csctf https://claude.ai/share/549c846d-f6c8-411c-9039-a9a14db376cf
```

Output:
- `<conversation_title>.md` — Clean Markdown with preserved code fences
- `<conversation_title>.html` — Styled static HTML (zero JavaScript)

## Supported Providers

| Provider | URL Pattern | Method | Notes |
|----------|-------------|--------|-------|
| **ChatGPT** | `chatgpt.com/share/*` | Headless Chromium | Public shares only |
| **Gemini** | `gemini.google.com/share/*` | Headless Chromium | Public shares only |
| **Grok** | `grok.com/share/*` | Headless Chromium | Public shares only |
| **Claude** | `claude.ai/share/*` | Your Chrome session | Requires login |

### Claude.ai Special Handling

Claude.ai uses Cloudflare protection that blocks standard browser automation. CSCTF handles this automatically:

1. Copies your Chrome session cookies to a temporary profile
2. Launches Chrome with remote debugging enabled
3. Connects via Chrome DevTools Protocol to extract conversation
4. If Chrome is running, offers to save tabs, restart, and restore afterward

**Requirements:** Chrome installed + logged into claude.ai in your regular Chrome session.

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Determinism** | Explicit slugging and collision handling |
| **Minimal network** | Only share URL fetched (update checks/publish opt-in) |
| **Safety** | Static HTML (inline CSS/HLJS), no scripts emitted |
| **Clarity** | Colorized step-based logging, confirmation gates |
| **Atomicity** | Temp+rename writes prevent partial files |

## How It Works

### ChatGPT, Gemini, Grok (End-to-End)

```
1. Launch headless Playwright Chromium with stealth config
   (spoofed navigator properties, realistic headers)
2. Navigate twice (domcontentloaded → networkidle) for late-loading assets
3. Detect provider from URL hostname
4. Wait for provider-specific selectors with retry/fallback
5. Extract each role's inner HTML (assistant/user), traverse Shadow DOM
6. Clean pills/metadata, run Turndown with fenced-code rule
7. Normalize whitespace and newlines
8. Write Markdown to temp file, rename atomically
9. Render HTML twin with inline CSS/TOC/HLJS
```

### Claude.ai

```
1. Copy Chrome session cookies to temporary profile
2. Launch Chrome with remote debugging
3. Connect via Chrome DevTools Protocol
4. Extract conversation HTML
5. Process through same Turndown/normalization pipeline
6. Clean up temporary profile
```

## Processing Algorithms

### Selector Strategy
Provider-specific selectors with fallback chains:
- **ChatGPT:** `article [data-message-author-role]`
- **Gemini:** Custom web components (`share-turn-viewer`, `response-container`)
- **Grok:** Flexible `data-testid` patterns
- **Claude:** `[data-testid="user-message"]` and streaming indicators

Each has multiple fallbacks tried with short timeouts.

### Turndown Customization
- Injects fenced code blocks
- Detects language via `class="language-*"`
- Strips citation pills and `data-start`/`data-end` attributes

### Normalization
- Converts newlines to `\n`
- Removes Unicode LS/PS characters
- Collapses excessive blank lines

### Slugging Algorithm
```
Title → lowercase → non-alphanumerics → "_" → trim → max 120 chars
       → Windows reserved-name suffix → collision suffix (_2, _3, ...)
```

### HTML Rendering
- Markdown-it + highlight.js
- Heading slug de-dupe for TOC
- Inline CSS for light/dark/print
- Zero JavaScript

## Command Reference

```bash
csctf <share-url> [options]
```

### Output Options

| Flag | Default | Description |
|------|---------|-------------|
| `--outfile <path>` | auto | Override output path |
| `--no-html` / `--md-only` | off | Skip HTML output |
| `--html-only` | off | Skip Markdown output |
| `--quiet` | off | Minimal logging |
| `--timeout-ms <ms>` | `60000` | Navigation + selector timeout |

### GitHub Pages Publishing

| Flag | Default | Description |
|------|---------|-------------|
| `--publish-to-gh-pages` | off | Publish to GitHub Pages |
| `--gh-pages-repo <owner/name>` | `my_shared_conversations` | Target repo |
| `--gh-pages-branch <branch>` | `gh-pages` | Target branch |
| `--gh-pages-dir <dir>` | `csctf` | Subdirectory in repo |
| `--remember` | off | Save GH settings |
| `--forget-gh-pages` | off | Clear saved settings |
| `--dry-run` | off | Simulate publish (build index, no push) |
| `--yes` / `--no-confirm` | off | Skip `PROCEED` confirmation prompt |
| `--gh-install` | off | Auto-install `gh` CLI |

### Other

| Flag | Description |
|------|-------------|
| `--check-updates` | Print latest release tag |
| `--version` | Print version and exit |

## Output Format

### Markdown Structure

```markdown
# Conversation: <Title>

**Source:** https://chatgpt.com/share/...
**Retrieved:** 2026-01-08T15:30:00Z

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

- **Standalone** — No external dependencies
- **Zero JavaScript** — Safe for any hosting
- **Inline CSS** — Light/dark mode via `prefers-color-scheme`
- **Syntax highlighting** — highlight.js themes inline
- **Table of contents** — Auto-generated from headings
- **Language badges** — Code block language indicators
- **Print-friendly** — Optimized print styles

## Filename Generation

```
"How to Build a REST API"  → how_to_build_a_rest_api.md
"Python Tips & Tricks!"    → python_tips_tricks.md
"File exists already"      → file_exists_already_2.md
```

Rules:
- Lowercase
- Non-alphanumerics → `_`
- Trimmed leading/trailing `_`
- Max 120 characters
- Windows reserved names suffixed
- Collisions: `_2`, `_3`, ...

## GitHub Pages Publishing

### Quick Recipe

```bash
# Publish with defaults
csctf <url> --publish-to-gh-pages --yes

# Creates: <gh-username>/my_shared_conversations repo
# Branch: gh-pages
# Directory: csctf/
```

### Remembered Settings

```bash
# First time: save settings
csctf <url> --publish-to-gh-pages --remember --yes

# Subsequent: just use --yes
csctf <url> --yes

# Clear remembered settings
csctf --forget-gh-pages
```

### Custom Configuration

```bash
csctf <url> --publish-to-gh-pages \
  --gh-pages-repo myuser/my-chats \
  --gh-pages-branch main \
  --gh-pages-dir exports \
  --yes
```

### Requirements

- GitHub CLI (`gh`) installed and authenticated
- Verify with: `gh auth status`

### Publish Flow

1. Resolve repo/branch/dir (use remembered or defaults)
2. Clone (or create via `gh`)
3. Copy MD + HTML files
4. Regenerate `manifest.json` and `index.html`
5. Commit + push
6. Print viewer URL

## Recipes

### Quiet CI Scrape (MD only)
```bash
csctf <url> --md-only --quiet --outfile /tmp/chat.md
```

### HTML-only for Embedding
```bash
csctf <url> --html-only --outfile site/chat.html
```

### Slow/Large Conversations
```bash
csctf <url> --timeout-ms 90000
```

### Custom Browser Cache
```bash
PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright csctf <url>
```

### Batch Archive
```bash
for url in $URLS; do
  csctf "$url" --outfile ~/archive/ --quiet
done
```

## Security & Privacy

### Network Behavior
- **Only fetches:** The share URL itself
- **Opt-in:** Update checks, GitHub publish flows
- **Auth:** GitHub CLI (`gh`) for publishing—no tokens stored

### HTML Safety
- Zero JavaScript in output
- Inline styles only
- Citation pills and data attributes stripped
- highlight.js used statically

### Filesystem
- Temp+rename write pattern (atomic)
- Collision-proof naming
- Config: `~/.config/csctf/config.json`

### Claude.ai Cookies
- Copied to temporary directory only
- Used for single scraping session
- Original Chrome profile never modified

## Performance

| Phase | Time |
|-------|------|
| First run (Chromium download) | 30-60s |
| Subsequent runs | 5-15s |
| Claude.ai (uses local Chrome) | 5-10s |

### Characteristics
- Playwright browsers cached after first run
- 60s default timeout, 3-attempt backoff
- Single page/context, linear processing
- Atomic writes prevent partial outputs

## Failure Modes & Remedies

| Symptom | Fix |
|---------|-----|
| "No messages found" | Link is private or layout changed; verify public share, retry with `--timeout-ms 90000` |
| Bot detection / challenge page | Stealth techniques used; retry or verify link in browser |
| Timeout or blank page | Raise `--timeout-ms`, verify connectivity |
| Publish fails (auth) | Ensure `gh auth status` passes |
| Publish fails (branch/dir) | Pass `--gh-pages-branch` / `--gh-pages-dir`; use `--remember` |
| Filename collisions | Expected; tool appends `_2`, `_3`, ... |
| Claude.ai Cloudflare challenge | Complete verification in Chrome window, press Enter |
| Claude.ai won't load | Ensure logged into claude.ai in Chrome; close Chrome if prompted |

## Environment Variables

### Runtime

| Variable | Description |
|----------|-------------|
| `PLAYWRIGHT_BROWSERS_PATH` | Reuse cached Chromium bundle |

### Installer

| Variable | Description | Default |
|----------|-------------|---------|
| `VERSION` | Pin release tag | latest |
| `DEST` | Install directory | `~/.local/bin` |
| `CHECKSUM_URL` | Override checksum location | — |

## File Locations

| Path | Purpose |
|------|---------|
| `~/.local/bin/csctf` | Binary |
| `~/.config/csctf/config.json` | GitHub Pages settings |
| `~/.cache/ms-playwright/` | Playwright Chromium cache |

## Installation

```bash
# One-liner (recommended)
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/chat_shared_conversation_to_file/main/install.sh | bash

# Pin version
VERSION=v1.0.0 curl -fsSL .../install.sh | bash

# Custom directory
DEST=/opt/bin curl -fsSL .../install.sh | bash

# Verify checksum
curl -fsSL .../install.sh | bash -s -- --verify
```

### From Source

```bash
bun install
bun run build
# Binary at dist/csctf
```

## Comparison

| Feature | Copy/Paste | csctf |
|---------|------------|-------|
| Code blocks preserved | Often broken | Always preserved |
| Language hints | Lost | Detected and kept |
| Filenames | Random/messy | Deterministic slugs |
| HTML output | None | Styled, no-JS twin |
| GitHub Pages | Manual | One command |
| Collision handling | Overwrite | Auto-suffix |

## Limitations

- Requires **public** share links (except Claude.ai which uses your session)
- Provider layouts may change (selectors maintained with fallbacks)
- Markdown/HTML exports require share to be available at scrape time
- Claude.ai requires Chrome installed with active login session
- First run downloads Playwright Chromium (~200MB)

## Integration with Flywheel

| Tool | Integration |
|------|-------------|
| **CASS** | Archive conversations for session search |
| **CM** | Extract procedural memory from exported chats |
| **Agent Mail** | Attach conversation exports to agent messages |
| **NTM** | Export multi-agent session transcripts |
