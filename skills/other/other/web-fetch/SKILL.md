---
name: web-fetch
description: Fetches web content with intelligent content extraction, converting HTML to clean markdown. Use for documentation, articles, and reference pages http/https URLs.
---

# Web Content Fetching

Fetch web content using `curl | html2markdown` with CSS selectors for clean, complete markdown output.

## Quick Usage (Known Sites)

Use site-specific selectors for best results:

```bash
# Anthropic docs
curl -s "<url>" | html2markdown --include-selector "#content-container"

# MDN Web Docs
curl -s "<url>" | html2markdown --include-selector "article"

# GitHub docs
curl -s "<url>" | html2markdown --include-selector "article" --exclude-selector "nav,.sidebar"

# Generic article pages
curl -s "<url>" | html2markdown --include-selector "article,main,[role=main]" --exclude-selector "nav,header,footer"
```

## Site Patterns

| Site | Include Selector | Exclude Selector |
|------|------------------|------------------|
| platform.claude.com | `#content-container` | - |
| docs.anthropic.com | `#content-container` | - |
| developer.mozilla.org | `article` | - |
| github.com (docs) | `article` | `nav,.sidebar` |
| Generic | `article,main` | `nav,header,footer,script,style` |

## Universal Fallback (Unknown Sites)

For sites without known patterns, use the Bun script which auto-detects content:

```bash
bun ~/.claude/skills/web-fetch/fetch.ts "<url>"
```

### Setup (one-time)

```bash
cd ~/.claude/skills/web-fetch && bun install
```

## Finding the Right Selector

When a site isn't in the patterns list:

```bash
# Check what content containers exist
curl -s "<url>" | grep -o '<article[^>]*>\|<main[^>]*>\|id="[^"]*content[^"]*"' | head -10

# Test a selector
curl -s "<url>" | html2markdown --include-selector "<selector>" | head -30

# Check line count
curl -s "<url>" | html2markdown --include-selector "<selector>" | wc -l
```

## Options Reference

```bash
--include-selector "CSS"  # Only include matching elements
--exclude-selector "CSS"  # Remove matching elements
--domain "https://..."    # Convert relative links to absolute
```

## Comparison

| Method | Anthropic Docs | Code Blocks | Complexity |
|--------|----------------|-------------|------------|
| Full page | 602 lines | Yes | Noisy |
| `--include-selector "#content-container"` | 385 lines | Yes | Clean |
| Bun script (universal) | 383 lines | Yes | Clean |

## Troubleshooting

**Wrong content selected**: The site may have multiple articles. Inspect the HTML:
```bash
curl -s "<url>" | grep -o '<article[^>]*>'
```

**Empty output**: The selector doesn't match. Try broader selectors like `main` or `body`.

**Missing code blocks**: Check if the site uses non-standard code formatting.

**Client-rendered content**: If HTML only has "Loading..." placeholders, the content is JS-rendered. Neither curl nor the Bun script can extract it; use browser-based tools.
