---
name: seo-audit
description: Audit websites for SEO, technical, content, and security issues using SEOmator CLI. Returns LLM-optimized reports with health scores, broken links, meta tag analysis, and actionable recommendations. Use when analyzing websites, debugging SEO issues, or checking site health.
license: MIT
compatibility: Requires Node.js 18+ and npm. Chrome/Chromium optional for Core Web Vitals.
metadata:
  author: seomator
  version: "2.1"
allowed-tools: Bash(seomator:*)
---

# SEO Audit Skill

Audit websites for SEO, technical, content, performance, and security issues using the SEOmator CLI.

SEOmator provides comprehensive website auditing by analyzing website structure and content against **134 rules** across **18 categories**.

It provides a list of issues with severity levels, affected URLs, and actionable fix suggestions.

## Links

* SEOmator npm package: [npmjs.com/package/@seomator/seo-audit](https://www.npmjs.com/package/@seomator/seo-audit)
* GitHub repository: [github.com/seo-skills/seo-audit-skill](https://github.com/seo-skills/seo-audit-skill)
* Web UI: [seomator.com/free-seo-audit-tool](https://seomator.com/free-seo-audit-tool)

## What This Skill Does

This skill enables AI agents to audit websites for **134 rules** in **18 categories**, including:

- **Core SEO**: Canonical URLs, indexing directives, title uniqueness
- **Meta Tags**: Title, description, viewport, favicon, canonical
- **Headings**: H1 presence, heading hierarchy, keyword usage
- **Technical SEO**: robots.txt, sitemap.xml, URL structure, 404 pages
- **Core Web Vitals**: LCP, CLS, FCP, TTFB, INP measurements
- **Links**: Broken links, redirect chains, anchor text, orphan pages
- **Images**: Alt text, dimensions, lazy loading, modern formats
- **Security**: HTTPS, HSTS, CSP, external link safety, leaked secrets
- **Structured Data**: Schema.org markup, Article, Organization, FAQ, Product
- **Social**: Open Graph tags, Twitter cards, share buttons, profile links
- **Content**: Word count, readability, keyword density, author info
- **Accessibility**: ARIA labels, color contrast, form labels, landmarks
- **Performance**: DOM size, CSS optimization, font loading, preconnect
- **Crawlability**: Sitemap conflicts, indexability signals, canonical chains
- **URL Structure**: Keyword slugs, stop words
- **Mobile**: Font sizes, horizontal scroll, intrusive interstitials
- **Internationalization**: lang attribute, hreflang tags
- **Legal Compliance**: Cookie consent, privacy policy, terms of service

The audit crawls the website, analyzes each page against audit rules, and returns a comprehensive report with:
- Overall health score (0-100) with letter grade (A-F)
- Category breakdowns with pass/warn/fail counts
- Specific issues with affected URLs grouped by rule
- Actionable fix recommendations

## When to Use

Use this skill when you need to:
- Analyze a website's SEO health
- Debug technical SEO issues
- Check for broken links
- Validate meta tags and structured data
- Audit security headers and HTTPS
- Check accessibility compliance
- Generate site audit reports
- Compare site health before/after changes
- Improve website performance, accessibility, SEO, security and more

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
- Chrome/Chromium for Core Web Vitals
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
2. **Use `--no-cwv` for faster audits** when Core Web Vitals aren't needed
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

# Full audit with Core Web Vitals
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
| `--refresh` | `-r` | Ignore cache, fetch fresh | false |
| `--resume` | | Resume interrupted crawl | false |
| `--no-cwv` | | Skip Core Web Vitals | false |
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

1. **Core Web Vitals** (11%) - User experience + ranking
2. **Links** (9%) - Internal linking structure
3. **Images** (9%) - Performance + accessibility
4. **Security** (9%) - Trust signals
5. **Meta Tags** (8%) - Search visibility
6. **Technical SEO** (8%) - Crawling foundation
7. **Structured Data** (5%) - Rich snippets
8. **Accessibility** (5%) - WCAG compliance
9. **Performance** (5%) - Static optimization
10. **Content** (5%) - Text quality

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
3. **Crawl** (if enabled): Discovers and fetches linked pages
4. **Analyze**: Runs 134 audit rules against each page
5. **Score**: Calculates category and overall scores
6. **Report**: Generates output in requested format

Results are stored in `~/.seomator/` for later retrieval with `seomator report`.

## Resources

- **Full rules reference**: See `docs/SEO-AUDIT-RULES.md` for all 134 rules
- **Storage architecture**: See `docs/STORAGE-ARCHITECTURE.md` for database details
- **CLI help**: `seomator --help` and `seomator <command> --help`
