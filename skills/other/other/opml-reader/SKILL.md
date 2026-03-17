---
name: opml-reader
description: Store OPML files and fetch latest posts across RSS/Atom feeds. Use when a user provides an OPML URL or file path, wants it saved under ~/Code/Files, or wants the newest entries aggregated across feeds (with optional JSON/TSV output, dedupe, and concurrency controls).
---

# OPML Reader

## Overview
Use `scripts/opml_reader.py` to (1) store OPML from a URL and (2) list the latest posts across all feeds in the OPML. Output timestamps are ISO-8601 in UTC.

## Quick Start
1. Create a venv and install dependency:

```bash
python3 -m venv ~/Code/sandbox/.venv-opml-reader
~/Code/sandbox/.venv-opml-reader/bin/pip install feedparser
```

2. Store an OPML file:

```bash
~/Code/sandbox/.venv-opml-reader/bin/python scripts/opml_reader.py store \
  "https://example.com/feeds.opml" \
  "~/Code/Files/feeds.opml"
```

3. Fetch latest posts:

```bash
~/Code/sandbox/.venv-opml-reader/bin/python scripts/opml_reader.py latest \
  "~/Code/Files/feeds.opml" \
  --limit 5
```

## Workflow
- If the user supplies an OPML URL, store it under `~/Code/Files` using `store`.
- If the OPML file already exists, reuse it unless the user explicitly asks to overwrite.
- Run `latest` to aggregate posts and return the newest entries across feeds.
- Report partial results if some feeds fail (network timeouts are expected on large lists).

## Output Options
- Default output: `text` lines formatted as `index. title | feed | date | link`.
- Use `--format json` or `--format tsv` if the user needs machine-readable output.
- Dedupe is on by default. Use `--no-dedupe` if the user wants raw results.
- Adjust `--workers` and `--timeout` for large or slow feed lists.

## Resources
### scripts/
- `scripts/opml_reader.py`: Store OPML files and list latest posts across RSS/Atom feeds.
