---
name: read-software-docs
description: Read and navigate software package documentation websites. Use when the user provides a documentation URL and wants to understand an API, SDK, framework, or library. Triggers on requests like "read the docs at [url]", "look up [topic] in the [package] documentation", "what does [API] do according to the docs", or any task requiring fetching and comprehending online software documentation. Supports any HTML-based documentation site including Sphinx, Doxygen, ReadTheDocs, MkDocs, and custom doc sites. Common targets include NVIDIA Isaac Sim, Omniverse Kit, OpenUSD, ROS 2, PyTorch, and similar software packages.
---

# Read Software Docs

Fetch, parse, and navigate software documentation websites to answer user questions or build understanding of APIs, SDKs, and frameworks.

## Script

`scripts/fetch_docs.py` — run with the project venv:

```
.venv/bin/python3 <skill-dir>/scripts/fetch_docs.py <mode> <url> [options]
```

**Modes:**

| Mode | Purpose | Key Options |
|------|---------|-------------|
| `page` | Fetch a single page as clean markdown | `--output FILE` |
| `links` | List all internal doc links on a page | `--filter REGEX` |
| `sitemap` | Crawl from a root URL, build page tree | `--depth N` (default 1), `--filter REGEX`, `--output FILE` |

Dependencies (`beautifulsoup4`, `html2text`, `requests`) must be installed in the `.venv`.

## Workflow

### 1. Orient: discover the doc structure

Start with `links` mode on the user's URL (or the doc site index) to see available pages:

```bash
.venv/bin/python3 scripts/fetch_docs.py links <url>
```

Use `--filter` to narrow results when the link list is large:
```bash
.venv/bin/python3 scripts/fetch_docs.py links <url> --filter "api|reference|python"
```

For broader discovery, use `sitemap` with shallow depth:
```bash
.venv/bin/python3 scripts/fetch_docs.py sitemap <url> --depth 1
```

### 2. Read: fetch specific pages

Fetch pages identified in step 1:

```bash
.venv/bin/python3 scripts/fetch_docs.py page <page-url>
```

For large pages, save to a file and read selectively:
```bash
.venv/bin/python3 scripts/fetch_docs.py page <page-url> --output .cache/knowledge/doc_page.md
```

### 3. Drill down: follow links as needed

If the initial page references sub-pages or related APIs, fetch those too. Repeat steps 1-2 to navigate deeper into the documentation tree.

### 4. Synthesize

After reading the relevant pages, produce the deliverable the user requested — this could be:
- A summary of an API or module
- A how-to guide assembled from multiple doc pages
- Answers to specific questions about the software
- Code examples based on the documented API

Save research output to `.knowledge/` for easy user access (same pattern as `read-arxiv-paper`).

## Tips

- **WebFetch fallback**: If `fetch_docs.py` struggles with a page (e.g., JavaScript-rendered content), fall back to the `WebFetch` tool which may handle it differently.
- **API docs**: For Python/C++ API reference pages, use `--filter` with module names to quickly find the right page (e.g., `--filter "omni.isaac.core|isaacsim"`).
- **Version pinning**: Many doc sites include version numbers in URLs. Confirm the user wants the version in the URL before deeply reading docs for a different version.
- **Caching**: Save fetched pages to `.cache/knowledge/` to avoid re-fetching during a session. Use descriptive filenames like `.cache/knowledge/isaacsim_core_api.md`.
