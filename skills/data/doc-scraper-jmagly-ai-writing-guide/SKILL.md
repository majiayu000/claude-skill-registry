---
name: doc-scraper
description: Scrape documentation websites into organized reference files. Use when converting docs sites to searchable references or building Claude skills.
tools: Read, Write, Bash, WebFetch
---

# Documentation Scraper Skill

## Purpose

Single responsibility: Convert documentation websites into organized, categorized reference files suitable for Claude skills or offline archives. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Target URL is accessible (test with `curl -I`)
- [ ] Documentation structure is identifiable (inspect page for content selectors)
- [ ] Output directory is writable
- [ ] Rate limiting requirements are known (check robots.txt)

**DO NOT proceed without verification. Inspect before scraping.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Content selector is ambiguous (multiple `<article>` or `<main>` elements)
- URL patterns unclear (can't determine include/exclude rules)
- Category mapping uncertain (content doesn't fit predefined categories)
- Rate limiting unknown (no robots.txt, unclear ToS)

**NEVER substitute missing configuration with assumptions.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Target URL, selectors, output path | Unrelated documentation |
| PERIPHERAL | Similar site examples for selector hints | Historical scrape data |
| DISTRACTOR | Other projects, unrelated URLs | Previous failed attempts |

## Workflow Steps

### Step 1: Verify Target (Grounding)

```bash
# Test URL accessibility
curl -I <target-url>

# Check robots.txt
curl <base-url>/robots.txt

# Inspect page structure (use browser dev tools or fetch sample)
```

### Step 2: Create Configuration

Generate scraper config based on inspection:

```json
{
  "name": "skill-name",
  "description": "When to use this skill",
  "base_url": "https://docs.example.com/",
  "selectors": {
    "main_content": "article",
    "title": "h1",
    "code_blocks": "pre code"
  },
  "url_patterns": {
    "include": ["/docs", "/guide", "/api"],
    "exclude": ["/blog", "/changelog", "/releases"]
  },
  "categories": {
    "getting_started": ["intro", "quickstart", "installation"],
    "api_reference": ["api", "reference", "methods"],
    "guides": ["guide", "tutorial", "how-to"]
  },
  "rate_limit": 0.5,
  "max_pages": 500
}
```

### Step 3: Execute Scraping

**Option A: With skill-seekers (if installed)**

```bash
# Verify skill-seekers is available
pip show skill-seekers

# Run scraper
skill-seekers scrape --config config.json

# For large docs, use async mode
skill-seekers scrape --config config.json --async --workers 8
```

**Option B: Manual scraping guidance**

1. Use sitemap.xml or crawl starting URL
2. Extract content using configured selectors
3. Categorize pages based on URL patterns and keywords
4. Save to organized directory structure

### Step 4: Validate Output

```bash
# Check output structure
ls -la output/<skill-name>/

# Verify content quality
head -50 output/<skill-name>/references/index.md

# Count extracted pages
find output/<skill-name>_data/pages -name "*.json" | wc -l
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Stop scraping, preserve already-fetched pages
2. **DIAGNOSE** - Check error type:
   - `Connection error` → Verify URL, check network
   - `Selector not found` → Re-inspect page structure
   - `Rate limited` → Increase delay, reduce workers
   - `Memory/disk` → Reduce batch size, clear temp files
3. **ADAPT** - Adjust configuration based on diagnosis
4. **RETRY** - Resume from checkpoint (max 3 attempts)
5. **ESCALATE** - Ask user for guidance

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/doc-scraper/`

Resume interrupted scrape:
```bash
skill-seekers scrape --config config.json --resume
```

Clear checkpoint and start fresh:
```bash
skill-seekers scrape --config config.json --fresh
```

## Output Structure

```
output/<skill-name>/
├── SKILL.md              # Main skill description
├── references/           # Categorized documentation
│   ├── index.md          # Category index
│   ├── getting_started.md
│   ├── api_reference.md
│   └── guides.md
├── scripts/              # (empty, for user additions)
└── assets/               # (empty, for user additions)

output/<skill-name>_data/
├── pages/                # Raw scraped JSON (one per page)
└── summary.json          # Scrape statistics
```

## Configuration Templates

### Minimal Config

```json
{
  "name": "myframework",
  "base_url": "https://docs.example.com/",
  "max_pages": 100
}
```

### Full Config

```json
{
  "name": "myframework",
  "description": "MyFramework documentation for building web apps",
  "base_url": "https://docs.example.com/",
  "selectors": {
    "main_content": "article, main, div[role='main']",
    "title": "h1, .title",
    "code_blocks": "pre code, .highlight code",
    "navigation": "nav, .sidebar"
  },
  "url_patterns": {
    "include": ["/docs/", "/api/", "/guide/"],
    "exclude": ["/blog/", "/changelog/", "/v1/", "/v2/"]
  },
  "categories": {
    "getting_started": ["intro", "quickstart", "install", "setup"],
    "concepts": ["concept", "overview", "architecture"],
    "api": ["api", "reference", "method", "function"],
    "guides": ["guide", "tutorial", "how-to", "example"],
    "advanced": ["advanced", "internals", "customize"]
  },
  "rate_limit": 0.5,
  "max_pages": 1000,
  "checkpoint": {
    "enabled": true,
    "interval": 100
  }
}
```

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| No content extracted | Selector mismatch | Inspect page, update `main_content` selector |
| Wrong pages scraped | URL pattern issue | Check `include`/`exclude` patterns |
| Rate limited | Too aggressive | Increase `rate_limit` to 1.0+ seconds |
| Memory issues | Too many pages | Add `max_pages` limit, enable checkpoints |
| Categories wrong | Keyword mismatch | Update category keywords in config |

## References

- Skill Seekers: https://github.com/jmagly/Skill_Seekers
- REF-001: Production-Grade Agentic Workflows (BP-1, BP-4, BP-9)
- REF-002: LLM Failure Modes (Archetype 1-4 mitigations)
