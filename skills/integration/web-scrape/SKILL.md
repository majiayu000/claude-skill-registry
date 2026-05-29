---
name: web-scrape
description: Intelligent web scraper with content extraction, multiple output formats, and error handling
version: 3.0.0
---

# Web Scraping Skill v3.0

## Usage

```
/web-scrape <url> [options]
```

**Options:**
- `--format=markdown|json|text` - Output format (default: markdown)
- `--full` - Include full page content (skip smart extraction)
- `--screenshot` - Also save a screenshot
- `--scroll` - Scroll to load dynamic content (infinite scroll pages)

**Examples:**
```
/web-scrape https://example.com/article
/web-scrape https://news.site.com/story --format=json
/web-scrape https://spa-app.com/page --scroll --screenshot
```

---

## Execution Flow

### Phase 1: Navigate and Load

```
1. mcp__playwright__browser_navigate
   url: "<target URL>"

2. mcp__playwright__browser_wait_for
   time: 2  (allow initial render)
```

**If `--scroll` option:** Execute scroll sequence to trigger lazy loading:
```
3. mcp__playwright__browser_evaluate
   function: "async () => {
     for (let i = 0; i < 3; i++) {
       window.scrollTo(0, document.body.scrollHeight);
       await new Promise(r => setTimeout(r, 1000));
     }
     window.scrollTo(0, 0);
   }"
```

### Phase 2: Capture Content

```
4. mcp__playwright__browser_snapshot
   → Returns full accessibility tree with all text content
```

**If `--screenshot` option:**
```
5. mcp__playwright__browser_take_screenshot
   filename: "scraped_<domain>_<timestamp>.png"
   fullPage: true
```

### Phase 3: Close Browser

```
6. mcp__playwright__browser_close
```

---

## Smart Content Extraction

After getting the snapshot, apply intelligent extraction:

### Step 1: Identify Content Type

| Page Type | Indicators | Extraction Strategy |
|-----------|------------|---------------------|
| **Article/Blog** | `<article>`, long paragraphs, date/author | Extract main article body |
| **Product Page** | Price, "Add to Cart", specs | Extract title, price, description, specs |
| **Documentation** | Code blocks, headings hierarchy | Preserve structure and code |
| **List/Search** | Repeated item patterns | Extract as structured list |
| **Landing Page** | Hero section, CTAs | Extract key messaging |

### Step 2: Filter Noise

**ALWAYS REMOVE these elements from output:**
- Navigation menus and breadcrumbs
- Footer content (copyright, links)
- Sidebars (ads, related articles, social links)
- Cookie banners and popups
- Comments section (unless specifically requested)
- Share buttons and social widgets
- Login/signup prompts

### Step 3: Structure the Content

**For Articles:**
```markdown
# [Title]

**Source:** [URL]
**Date:** [if available]
**Author:** [if available]

---

[Main content in clean markdown]
```

**For Product Pages:**
```markdown
# [Product Name]

**Price:** [price]
**Availability:** [in stock/out of stock]

## Description
[product description]

## Specifications
| Spec | Value |
|------|-------|
| ... | ... |
```

---

## Output Formats

### Markdown (default)
Clean, readable markdown with proper headings, lists, and formatting.

### JSON
```json
{
  "url": "https://...",
  "title": "Page Title",
  "type": "article|product|docs|list",
  "content": {
    "main": "...",
    "metadata": {}
  },
  "extracted_at": "ISO timestamp"
}
```

### Text
Plain text with minimal formatting, suitable for further processing.

---

## Error Handling

### Navigation Errors

| Error | Detection | Action |
|-------|-----------|--------|
| **Timeout** | Page doesn't load in 30s | Report error, suggest retry |
| **404 Not Found** | "404" in title/content | Report "Page not found" |
| **403 Forbidden** | "403", "Access Denied" | Report access restriction |
| **CAPTCHA** | "captcha", "verify you're human" | Report CAPTCHA detected, cannot proceed |
| **Paywall** | "subscribe", "premium content" | Extract visible content, note paywall |

### Recovery Actions

```
If page load fails:
1. Report the specific error to user
2. Suggest: "Try again?" or "Different URL?"
3. Close browser cleanly

If content is blocked:
1. Report what was detected (CAPTCHA/paywall/geo-block)
2. Extract any available preview content
3. Suggest alternatives if applicable
```

---

## Advanced Scenarios

### Single Page Applications (SPA)
```
1. Navigate to URL
2. Wait longer (3-5 seconds) for JS hydration
3. Use browser_wait_for with specific text if known
4. Then snapshot
```

### Infinite Scroll Pages
```
1. Navigate
2. Execute scroll loop (see Phase 1)
3. Snapshot after scrolling completes
```

### Pages with Click-to-Reveal Content
```
1. Snapshot first to identify clickable elements
2. Use browser_click on "Read more" / "Show all" buttons
3. Wait briefly
4. Snapshot again for full content
```

### Multi-page Articles
```
1. Scrape first page
2. Identify "Next" or pagination links
3. Ask user: "Article has X pages. Scrape all?"
4. If yes, iterate through pages and combine
```

---

## Performance Guidelines

| Metric | Target | How |
|--------|--------|-----|
| **Speed** | < 15 seconds | Minimal waits, parallel where possible |
| **Token Usage** | < 5000 tokens | Smart extraction, not full DOM |
| **Reliability** | > 95% success | Proper error handling |

---

## Security Notes

- Never execute arbitrary JavaScript from the page
- Don't follow redirects to suspicious domains
- Don't submit forms or click login buttons
- Don't scrape pages that require authentication (unless user provides credentials flow)
- Respect robots.txt when mentioned by user

---

## Quick Reference

**Minimum viable scrape (4 tool calls):**
```
1. browser_navigate → 2. browser_wait_for → 3. browser_snapshot → 4. browser_close
```

**Full-featured scrape (with scroll + screenshot):**
```
1. browser_navigate
2. browser_wait_for
3. browser_evaluate (scroll)
4. browser_snapshot
5. browser_take_screenshot
6. browser_close
```

Remember: The goal is to deliver **clean, useful content** to the user, not raw HTML/DOM dumps.
