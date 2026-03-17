---
name: check-links
description: Check all internal links on the local Hugo site for broken links. Use before pushing to verify site integrity.
---

# Link Checker

Validates all internal links on the local Hugo development server.

## Usage

Run the link checker script:

```bash
python .claude/skills/check-links/scripts/check_links.py
```

## What it checks

- Crawls all pages starting from http://localhost:1313/
- Follows internal links only (same host)
- Reports broken links (404s, connection errors)
- Shows which page contains each broken link

## Prerequisites

The Hugo development server must be running:

```bash
cd hugo && hugo server
```

## Output

- Lists any broken links found with their source pages
- Exits with code 0 if all links valid, 1 if broken links found
