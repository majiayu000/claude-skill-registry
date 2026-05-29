---
name: read-webpage-content-as-markdown
description: Read a webpage into cleaned markdown using curl + markitdown + codex exec. Use whenever asked to read a webpage or extract article content from a URL. Static HTML only; JS/client-rendered pages require a Playwright workflow.
---

# Read Webpage Content as Markdown

Use:

```bash
scripts/read-webpage-content-as-markdown.sh [--navlinks] <url> [output_md]
```

Notes:
- Uses curl (static HTML only); JavaScript is not executed.
- Temp artifacts are stored under /tmp.
- Output includes YAML frontmatter: source_url, accessed_at, commands.
- Output path defaults to `/tmp/read-webpage-content-as-markdown.<timestamp>.md`; relative output paths are written under `/tmp/`.
- --navlinks keeps only topic-relevant navigation links (e.g., in-page table of contents); it drops site-wide menus and unrelated links.
- If the script reports JS/client rendering, retry with Playwright.
