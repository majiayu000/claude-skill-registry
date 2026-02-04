---
name: llm-code-docs
description: Centralized AI-readable documentation repository with 245+ frameworks and tools. Use to find documentation, add new sources, or update existing docs. Located at ~/github/llm-code-docs.
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep]
---

# LLM Code Docs

## Overview
Centralized repository of AI-optimized documentation for 245+ frameworks, libraries, and developer tools. Three-tier structure prioritizing llms.txt standard sites.

**Location**: `~/github/llm-code-docs`

<examples>
<example>
Task: Find documentation for FastAPI to understand authentication patterns

```bash
grep -i "fastapi" ~/github/llm-code-docs/index.yaml
ls ~/github/llm-code-docs/docs/github-scraped/fastapi/
cat ~/github/llm-code-docs/docs/github-scraped/fastapi/docs/advanced/security.md
```

Output:
FastAPI documentation available in github-scraped folder with complete API security patterns and examples.
</example>

<example>
Task: Search across all documentation for "middleware" implementations

```bash
grep -r "middleware" ~/github/llm-code-docs/docs/llms-txt/*/llms-full.txt | head -10
grep -r "middleware" ~/github/llm-code-docs/docs/github-scraped/ --include="*.md" | head -10
```

Output:
Multiple implementations found across FastAPI, Express, Django, and other frameworks in the repository.
</example>

<example>
Task: Add documentation for a new framework that has an llms.txt file

```bash
# Check if llms.txt exists
./scripts/find-llms-txt.sh example.com

# Add to config
echo "  - name: example-framework
    base_url: https://docs.example.com/
    description: Example framework documentation" >> scripts/llms-sites.yaml

# Download documentation
python3 scripts/llms-txt-scraper.py --site example-framework

# Update index
python3 scripts/update-index.py
```

Output:
New framework documentation indexed and available at docs/llms-txt/example-framework/
</example>

<example>
Task: Update all documentation sources to get latest versions

```bash
cd ~/github/llm-code-docs
./scripts/update.sh
```

Output:
All 228+ llms.txt sites, 14 Git repositories, and web-scraped sources refreshed with latest content.
</example>

<example>
Task: Find documentation for a specific library and verify it exists

```bash
ls ~/github/llm-code-docs/docs/llms-txt/ | grep -i playwright
head -20 ~/github/llm-code-docs/docs/llms-txt/playwright/llms-full.txt
```

Output:
Playwright documentation found and verified to contain expected content.
</example>
</examples>

## First-Time Setup

### Initial Configuration
```bash
# Navigate to the repository
cd ~/github/llm-code-docs

# Install Python dependencies
pip install -r requirements.txt

# Verify documentation is up-to-date
./scripts/update.sh
```

### Verify Installation
```bash
# Check available documentation
ls docs/llms-txt/ | wc -l        # Should show ~228
ls docs/github-scraped/           # Should show ~14 repos
ls docs/web-scraped/              # Should show custom scrapers

# Verify index
cat index.yaml | head -20
```

## Repository Structure

```
llm-code-docs/
├── docs/
│   ├── llms-txt/           # 228 sites (HIGHEST PRIORITY)
│   ├── github-scraped/     # 14 Git repo extractions
│   └── web-scraped/        # Custom scrapers (ntfy, claude-code-sdk, etc.)
├── scripts/                # All extraction and update tools
├── index.yaml              # Index of all documentation sources
└── AGENTS.md               # Guide for AI agents
```

## Quick Start

### Find Documentation
```bash
# Search by topic
ls ~/github/llm-code-docs/docs/llms-txt/ | grep -i react

# Check if a library exists
grep -i "fastapi" ~/github/llm-code-docs/index.yaml

# Read documentation
cat ~/github/llm-code-docs/docs/llms-txt/anthropic/llms-full.txt
```

### Update All Documentation
```bash
cd ~/github/llm-code-docs
./scripts/update.sh
```

### Update Specific Sources
```bash
# Update single llms.txt site
python3 scripts/llms-txt-scraper.py --site anthropic

# Force re-download (ignore cache)
python3 scripts/llms-txt-scraper.py --site vercel-ai-sdk --force

# Update Git repository extractions
python3 scripts/extract_docs.py

# Update specific web-scraped docs
python3 scripts/ntfy-docs.py
python3 scripts/claude-code-sdk-docs.py
```

## Adding New Documentation

### Priority Order
1. **llms.txt** - Check if site has llms.txt first (highest quality)
2. **Git repos** - For comprehensive docs from source
3. **Web scraping** - Last resort for critical docs

### Add llms.txt Site
```bash
# 1. Check if llms.txt exists (probes common subdomain/path combinations)
./scripts/find-llms-txt.sh example.com
# Or manually check:
curl -sL https://docs.example.com/llms.txt | head -20

# 2. Add to config (alphabetical order)
# Edit scripts/llms-sites.yaml:
#   - name: example-site
#     base_url: https://docs.example.com/
#     description: Example documentation

# 3. Download
python3 scripts/llms-txt-scraper.py --site example-site

# 4. Verify
ls -la docs/llms-txt/example-site/

# 5. Update index
python3 scripts/update-index.py
```

### Add Web Scraper (No llms.txt)
```bash
# 1. Create scraper script based on existing pattern
cp scripts/ntfy-docs.py scripts/newsite-docs.py

# 2. Edit script:
#    - Update BASE_URL
#    - Update DOC_PAGES list (from sitemap or manual)
#    - Update output path to docs/web-scraped/newsite/

# 3. Run scraper
python3 scripts/newsite-docs.py

# 4. Update index
python3 scripts/update-index.py
```

### Add Git Repository
```bash
# Edit scripts/repo_config.yaml:
repositories:
  - name: example
    repo_url: https://github.com/owner/repo
    source_folder: docs/
    target_folder: docs/github-scraped/example
    branch: main

# Run extraction
python3 scripts/extract_docs.py
```

## Key Scripts

| Script | Purpose |
|--------|---------|
| `find-llms-txt.sh` | Probe domain for llms.txt (checks subdomains/paths) |
| `llms-txt-scraper.py` | Download from 228+ llms.txt sites |
| `extract_docs.py` | Clone and extract Git repositories |
| `claude-code-sdk-docs.py` | Claude Code SDK documentation |
| `ntfy-docs.py` | ntfy push notification docs |
| `update-index.py` | Update index.yaml with current state |
| `update.sh` | Master script runs all updates |

## Configuration Files

### llms-sites.yaml
```yaml
sites:
- name: anthropic
  base_url: https://docs.anthropic.com/
  description: Claude AI documentation
- name: vercel-ai-sdk
  base_url: https://ai-sdk.dev/
  description: AI SDK for building AI-powered apps
```

### repo_config.yaml
```yaml
repositories:
  - name: fastapi
    repo_url: https://github.com/fastapi/fastapi
    source_folder: docs/en/docs/
    target_folder: docs/github-scraped/fastapi
    branch: master
```

## Caching System

- **Cache duration**: 23 hours
- Files downloaded within cache window are skipped
- Use `--force` to override cache
- Parallel downloads with 15 concurrent workers

## Common Tasks

### Check What's Available
```bash
# List all llms.txt sites
ls docs/llms-txt/ | wc -l

# List web-scraped docs
ls docs/web-scraped/

# Search for specific topic
grep -r "authentication" docs/llms-txt/*/llms-full.txt | head -20
```

### Verify Documentation Quality
```bash
# Check file sizes (small = possibly incomplete)
ls -lh docs/llms-txt/*/llms-full.txt | sort -k5 -h | tail -10

# Check for code examples
grep -l '```' docs/llms-txt/anthropic/*.md | wc -l

# Verify source headers present
head -5 docs/web-scraped/ntfy/publish.md
```

### Troubleshooting

#### Site returns 404
```bash
# Probe all common locations automatically
./scripts/find-llms-txt.sh example.com

# Or check manually
curl -sI https://docs.example.com/llms.txt
curl -sI https://example.com/llms.txt
curl -sI https://docs.example.com/llms-full.txt
```

#### Push blocked by secrets
```bash
# Find and redact test credentials
grep -n "sk_test\|AC[0-9a-f]\{32\}" docs/web-scraped/*/

# Replace with placeholders
sed -i '' 's/AC12345.../AC_EXAMPLE_SID/g' file.md
```

## Statistics

- **228** llms.txt sites fetched
- **14** Git repositories extracted
- **3** web-scraped documentation sets
- **12,000+** markdown files
- **300MB+** total documentation

## See Also

- [reference.md](reference.md) - Complete script reference
- [examples.md](examples.md) - Real-world usage patterns
