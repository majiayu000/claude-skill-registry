---
name: browser
description: Control a Chromium browser via CDP. Use when automating web browsing, scraping pages, testing web apps, monitoring network traffic, or interacting with page elements.
compatibility: Requires Chromium/Chrome installed and the browser CLI in PATH.
metadata:
  author: browser-cli
  version: "1.0"
---

# Browser CLI Skill

Control a Chromium browser via CDP. Install: https://github.com/camhahu/browser

```bash
curl -fsSL https://raw.githubusercontent.com/camhahu/browser/main/packages/cli/install.sh | bash
```

## Core Loop

```bash
browser open https://example.com  # Starts headless browser, shows outline

browser click l3                  # 1. Click by label from outline
browser text ".product-list"      # 3. Read content

browser stop                      # Always stop when finished
```

**Prefer `text` over screenshots.** Text is faster and more reliable. Use screenshots only when visual layout matters.

## Commands

```bash
# Navigation
browser open <url>                # Open URL (auto-starts headless browser if needed)
browser navigate <url>            # Navigate current tab
browser back / forward / refresh  # History navigation
browser stop                      # Close browser

# Interaction
browser click <selector>          # Click by label, text, or CSS
browser type <text> [selector]    # Type into input (special keys: Enter, Escape, Tab)
browser hover <selector>          # Move mouse to element
browser drag <source> <target>    # Drag element to another element
browser select <selector> <value> # Select dropdown option
browser scroll <target>           # Scroll to top, bottom, or selector

# Content
browser outline                   # Show outline again (or use -a for full structure)
browser text [selector]           # Extract text content
browser screenshot [name]         # Capture screenshot (use when layout matters)

# Tabs
browser tabs                      # List all open tabs
browser use <tab-id>              # Switch to tab
browser close [tab-id]            # Close tab

# Debugging
browser console                   # Show console output
browser network                   # List network requests
browser eval <js>                 # Run JavaScript (shares scope between calls)
```

Navigation commands (`open`, `click`, `navigate`, `back`, `forward`, `refresh`) show an outline after completing.

For debugging or user intervention, start a headed browser with `browser start --headed`.

Run `browser --help` for full command list.

## Outline

Outline shows interactive elements with labels:

```
[l1] link "Products" [href=/products]
[l2] link "About" [href=/about]
[b3] button "Sign up"
[i4] input [type=email] [placeholder="Email"]
```

## Selectors

```bash
browser click l3                 # Label from outline (fastest)
browser click "Sign up"          # Text match (exact first, then partial)
browser click ".btn-primary"     # CSS selector
```

CSS selectors: `#id`, `.class`, `tag`, `[attr=value]`, `parent > child`

## Persistent Profile

Logins, cookies, and browsing data are preserved across sessions in `~/.browser/profile/`.

```bash
browser config clear-profile              # Logout, reset cookies
browser config set persistentProfile false # Disable persistence
```
