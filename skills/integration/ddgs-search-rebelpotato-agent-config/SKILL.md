---
name: ddgs-search
description: Web search via the DDGS metasearch library. Use for searching for unknown documentation, facts, or any web content. Lightweight, no browser required.
---

# DDGS search

Web search and content extraction using the DDGS library. No browser required.

## Usage

Run from any directory:

```bash
uv run {baseDir}/search.py "python programming"                     # Basic search (5 results)
uv run {baseDir}/search.py "python programming" --proxy http://proxy.example.com:8080  # Use proxy
uv run {baseDir}/search.py "russia filetype:pdf"                    # Search with advanced query
uv run {baseDir}/search.py "python programming" -n 20               # More results
uv run {baseDir}/search.py "python programming" -r uk-en            # UK English results
uv run {baseDir}/search.py "python programming" -s off              # Disable safesearch
uv run {baseDir}/search.py "python programming" -t w2               # Results from the last two weeks
uv run {baseDir}/search.py "python programming" -p 2                # Page 2 of results
uv run {baseDir}/search.py "python programming" -b "bing,google"    # Use specific backends
uv run {baseDir}/search.py "python programming" --brief             # Show only snippets (no full text extraction)
```

### Options

- `-n, --max-results <num>` - Maximum number of results (default: 5)
- `-r, --region <code>` - Region/language code: us-en, uk-en, ru-ru, etc. (default: us-en)
- `-s, --safesearch <level>` - Safesearch level: on, moderate, off (default: off)
- `-t, --timelimit <period>` - Time limit: d, w, m, y. (default: None)
- `-p, --page <num>` - Page number of results (default: 1)
- `-b, --backend <backends>` - Single or comma-delimited backends (default: auto)
  - available backends: bing, brave, duckduckgo, google, grokipedia, mojeek, yandex, yahoo, wikipedia
- `--proxy <url>` - Proxy URL (default: None)
- `--brief` - Suppress full text extraction from webpages (show only snippets)

### Output Format

By default, the tool fetches and displays full text from each webpage:

```plaintext
--- Result 1 ---
Title: Python (programming language)
Href: https://grokipedia.com/page/Python_(programming_language)
Body: Python is an interpreted, high-level, general-purpose programming language designed for code readability and simplicity, featuring a dynamic type system and support for...

Full Text:
----------------------------------------
# Python (programming language)

Python is an interpreted, high-level, general-purpose programming language...

[... truncated ...]
----------------------------------------

--- Result 2 ---
...
```

Use `--brief` to show only the search result snippets without full text extraction.

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- Any task requiring web search without interactive browsing

## Next Steps

### Useful commands

- Use `curl` to fetch webpage or download files
- Use `uvx html2text` to convert webpages into readable text
- Use `pdftotext` or `uvx pdfplumber` to extract text from PDF documents
