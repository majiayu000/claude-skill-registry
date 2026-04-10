---
name: seo-audit
description: Audit websites for SEO, technical, content, security, JS rendering, and AI readiness using SEOmator CLI. Returns LLM-optimized reports with health scores across 251 rules and 20 categories. Use when analyzing websites, debugging SEO issues, or checking site health.
license: MIT
compatibility: Requires Node.js 18+ and npm. Chrome/Chromium optional for Core Web Vitals and JS rendering.
metadata:
  author: seomator
  version: "3.0"
allowed-tools: Bash(seomator:*)
---

# SEO Audit Skill

Audit websites for SEO, technical, content, performance, security, JavaScript rendering, and AI readiness using the SEOmator CLI.

SEOmator provides comprehensive website auditing by analyzing website structure and content against **251 rules** across **20 categories**.

It provides a list of issues with severity levels, affected URLs, and actionable fix suggestions.

## Links

* SEOmator npm package: [npmjs.com/package/@seomator/seo-audit](https://www.npmjs.com/package/@seomator/seo-audit)
* GitHub repository: [github.com/seo-skills/seo-audit-skill](https://github.com/seo-skills/seo-audit-skill)
* Web UI: [seomator.com/free-seo-audit-tool](https://seomator.com/free-seo-audit-tool)

## What This Skill Does

This skill enables AI agents to audit websites for **251 rules** in **20 categories**, including:

- **Core SEO** (19 rules): Canonical URLs, indexing directives, title uniqueness, canonical conflicts/loops
- **Performance** (22 rules): LCP, CLS, FCP, TTFB, INP, compression, caching, minification, HTTP/2
- **Links** (19 rules): Broken links, redirect chains, anchor text, orphan pages, localhost/fragment links
- **Images** (14 rules): Alt text, dimensions, lazy loading, modern formats, alt length, background images
- **Security** (16 rules): HTTPS, HSTS, CSP, external link safety, leaked secrets, SSL expiry/protocol
- **Technical SEO** (13 rules): robots.txt, sitemap.xml, URL structure, 404 pages, soft 404s, error codes
- **Crawlability** (18 rules): Sitemap conflicts, indexability signals, canonical chains, pagination issues
- **Structured Data** (13 rules): Schema.org markup, Article, Organization, FAQ, Product, Breadcrumb
- **JavaScript Rendering** (13 rules): Rendered DOM checks, raw vs rendered mismatches, SSR detection
- **Accessibility** (12 rules): ARIA labels, color contrast, form labels, landmarks, touch targets
- **Content** (17 rules): Word count, readability, keyword density, duplicate detection, pixel widths
- **Social** (9 rules): Open Graph tags, Twitter cards, share buttons, profile links
- **E-E-A-T** (14 rules): Author bylines, citations, trust signals, about/contact pages, YMYL detection
- **URL Structure** (14 rules): Keyword slugs, stop words, uppercase, underscores, session IDs, tracking params
- **Redirects** (8 rules): Redirect loops, types (301/302), meta refresh, JavaScript redirects, broken redirects
- **Mobile** (5 rules): Font sizes, horizontal scroll, intrusive interstitials, viewport issues
- **Internationalization** (10 rules): lang attribute, hreflang validation (return links, conflicts, mismatches)
- **HTML Validation** (9 rules): Doctype, charset, head structure, lorem ipsum, multiple titles/descriptions
- **AI/GEO Readiness** (5 rules): Semantic HTML, AI bot access, llms.txt, schema drift
- **Legal Compliance** (1 rule): Cookie consent

The audit crawls the website, analyzes each page against audit rules, and returns a comprehensive report with:
- Overall health score (0-100) with letter grade (A-F)
- Category breakdowns with pass/warn/fail counts
- Specific issues with affected URLs grouped by rule
- Actionable fix recommendations

## When to Use

Use this skill when you need to:
- Analyze a website's SEO health
- Debug technical SEO issues
- Check for broken links and redirect chains
- Validate meta tags, canonical URLs, and structured data
- Audit security headers, SSL, and HTTPS
- Check accessibility compliance
- Analyze JavaScript rendering and SSR compatibility
- Evaluate AI/GEO readiness (semantic HTML, llms.txt, bot access)
- Detect duplicate content across pages
- Validate hreflang and internationalization setup
- Check HTML document structure and validation
- Generate site audit reports in multiple formats
- Compare site health before/after changes

## Prerequisites

This skill requires the SEOmator CLI to be installed.

### Installation

```bash
npm install -g @seomator/seo-audit
```

### Verify Installation

Check that seomator is installed and the system is ready:

```bash
seomator self doctor
```

This checks:
- Node.js version (18+ recommended)
- npm availability
- Chrome/Chromium for Core Web Vitals and JS rendering
- Write permissions for ~/.seomator
- Local config file presence

## Setup

Running `seomator init` creates a `seomator.toml` config file in the current directory.

```bash
seomator init                    # Interactive setup
seomator init -y                 # Use defaults
seomator init --preset blog      # Blog-optimized config
seomator init --preset ecommerce # E-commerce config
seomator init --preset ci        # Minimal CI config
```

If there is no `seomator.toml` in the directory, CREATE ONE with `seomator init` before running audits.

## Usage

### AI Agent Best Practices

**YOU SHOULD always prefer `--format llm`** - it provides token-optimized XML output specifically designed for AI agents (50-70% smaller than JSON).

When auditing:
1. **Prefer live websites** over local dev servers for accurate performance and rendering data
2. **Use `--no-cwv` for faster audits** when Core Web Vitals and JS rendering checks aren't needed
3. **Scope fixes as concurrent tasks** when implementing multiple fixes
4. **Run typechecking/formatting** after implementing fixes (tsc, eslint, prettier, etc.)

### Website Discovery

If the user doesn't provide a website to audit:
1. Check for local dev server configurations (package.json scripts, .env files)
2. Look for Vercel/Netlify project links
3. Check environment variables for deployment URLs
4. Ask the user which URL to audit

If you have both local and live websites available, **suggest auditing the live site** for accurate results.

### Basic Workflow

```bash
# Quick single-page audit with LLM output
seomator audit https://example.com --format llm --no-cwv

# Multi-page crawl (up to 50 pages)
seomator audit https://example.com --crawl -m 50 --format llm --no-cwv

# Full audit with Core Web Vitals + JS rendering analysis
seomator audit https://example.com --crawl -m 20 --format llm
```

### Advanced Options

Force fresh crawl (ignore cache):
```bash
seomator audit https://example.com --refresh --format llm
```

Resume interrupted crawl:
```bash
seomator audit https://example.com --resume --format llm
```

Audit specific categories only:
```bash
seomator audit https://example.com -c core,security,js --format llm --no-cwv
```

Save HTML report for sharing:
```bash
seomator audit https://example.com --format html -o report.html
```

Verbose output for debugging:
```bash
seomator audit https://example.com --format llm -v
```

## Command Reference

### Audit Command Options

| Option | Alias | Description | Default |
|--------|-------|-------------|---------|
| `--format <fmt>` | `-f` | Output format: console, json, html, markdown, llm | console |
| `--max-pages <n>` | `-m` | Maximum pages to crawl | 10 |
| `--crawl` | | Enable multi-page crawl | false |
| `--categories <list>` | `-c` | Comma-separated categories to audit | All |
| `--refresh` | `-r` | Ignore cache, fetch fresh | false |
| `--resume` | | Resume interrupted crawl | false |
| `--no-cwv` | | Skip Core Web Vitals + JS rendering | false |
| `--verbose` | `-v` | Show progress | false |
| `--output <path>` | `-o` | Output file path | |
| `--config <path>` | | Config file path | |
| `--save` | | Save to ~/.seomator | false |

### Other Commands

```bash
seomator init              # Create config file
seomator self doctor       # Check system setup
seomator config --list     # Show all config values
seomator report --list     # List past reports
seomator db stats          # Show database statistics
```

## Output Formats

| Format | Flag | Best For |
|--------|------|----------|
| console | `--format console` | Human terminal output (default) |
| json | `--format json` | CI/CD, programmatic processing |
| html | `--format html` | Standalone reports, sharing |
| markdown | `--format markdown` | Documentation, GitHub |
| llm | `--format llm` | **AI agents** (recommended) |

The `--format llm` output is a compact XML format optimized for token efficiency:
- **50-70% smaller** than JSON output
- Issues sorted by severity (critical first)
- Fix suggestions included for each issue
- Clean stdout for piping to AI tools

## Examples

### Example 1: Quick Audit with LLM Output

```bash
# User asks: "Check example.com for SEO issues"
seomator audit https://example.com --format llm --no-cwv
```

### Example 2: Deep Crawl for Large Site

```bash
# User asks: "Do a thorough audit with up to 100 pages"
seomator audit https://example.com --crawl -m 100 --format llm --no-cwv
```

### Example 3: Fresh Audit After Changes

```bash
# User asks: "Re-audit the site, ignore cached results"
seomator audit https://example.com --refresh --format llm --no-cwv
```

### Example 4: Generate Shareable Report

```bash
# User asks: "Create an HTML report I can share"
seomator audit https://example.com --crawl -m 20 --format html -o seo-report.html
```

### Example 5: Focus on Specific Areas

```bash
# User asks: "Just check my JavaScript rendering and redirects"
seomator audit https://example.com -c js,redirect --format llm
```

## Evaluating Results

### Score Ranges

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent - Minor optimizations only |
| 80-89 | B | Good - Address warnings |
| 70-79 | C | Needs Work - Priority fixes required |
| 50-69 | D | Poor - Multiple critical issues |
| 0-49 | F | Critical - Major problems to resolve |

### Priority Order (by category weight)

Fix issues in this order for maximum impact:

1. **Core** (12%) - Meta tags, canonical, H1, indexing
2. **Performance** (12%) - Core Web Vitals + optimization
3. **Links** (8%) - Internal linking structure
4. **Images** (8%) - Performance + accessibility
5. **Security** (8%) - Trust signals, SSL
6. **Technical SEO** (7%) - Crawling foundation
7. **Crawlability** (5%) - Indexability, pagination
8. **Structured Data** (5%) - Rich snippets
9. **JavaScript Rendering** (5%) - Rendered DOM, SSR
10. **Content** (5%) - Text quality + duplicates
11. **Accessibility** (4%) - WCAG compliance
12. **Social** (3%) - Social sharing
13. **E-E-A-T** (3%) - Trust, expertise
14. **URL Structure** (3%) - URL hygiene
15. **Redirects** (3%) - Redirect chains
16. **Mobile** (2%) - Viewport, fonts
17. **Internationalization** (2%) - Hreflang
18. **HTML Validation** (2%) - Document structure
19. **AI/GEO Readiness** (2%) - Semantic HTML, AI bots
20. **Legal Compliance** (1%) - Cookie consent

### Fix by Severity

1. **Failures (status: "fail")** - Must fix immediately
2. **Warnings (status: "warn")** - Should fix soon
3. **Passes (status: "pass")** - No action needed

## Output Summary

After implementing fixes, give the user a summary of all changes made.

When planning scope, organize tasks so they can run concurrently as sub-agents to speed up implementation.

## Troubleshooting

### seomator command not found

If you see this error, seomator is not installed or not in your PATH.

**Solution:**
```bash
npm install -g @seomator/seo-audit
```

### Core Web Vitals not measured

If CWV metrics are missing, Chrome/Chromium may not be available.

**Solution:**
1. Install Chrome, Chromium, or Edge
2. Run `seomator self doctor` to verify browser detection
3. Use `--no-cwv` to skip CWV if not needed

### Crawl timeout or slow performance

For large sites, audits may take several minutes.

**Solution:**
- Use `--verbose` to see progress
- Limit pages with `-m 20` for faster results
- Use `--no-cwv` to skip browser-based measurements

### Invalid URL

Ensure the URL includes the protocol:

```bash
# Wrong
seomator audit example.com

# Correct
seomator audit https://example.com
```

## How It Works

1. **Fetch**: Downloads the page HTML and measures response time
2. **Parse**: Extracts DOM, meta tags, links, images, structured data
3. **Enrich**: Fetches robots.txt and sitemap once per audit
4. **Render** (if CWV enabled): Captures rendered DOM via Playwright for JS rendering analysis
5. **Crawl** (if enabled): Discovers and fetches linked pages
6. **Analyze**: Runs 251 audit rules against each page
7. **Score**: Calculates category and overall weighted scores
8. **Report**: Generates output in requested format

Results are stored in `~/.seomator/` for later retrieval with `seomator report`.

## Resources

- **Full rules reference**: See `docs/SEO-AUDIT-RULES.md` for all 251 rules
- **Storage architecture**: See `docs/STORAGE-ARCHITECTURE.md` for database details
- **CLI help**: `seomator --help` and `seomator <command> --help`
