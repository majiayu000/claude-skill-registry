---
name: reading-books
description: Read and search digital books (PDF, EPUB, MOBI, TXT). Use when answering questions about a book, finding quotes or passages, navigating to specific pages or chapters, or extracting information from documents.
---

# Book Reader

Read and query digital book formats from the command line using BM25 search.

## Quick Start

```bash
# Get book metadata
uv run ~/.claude/skills/reading-books/book.py info ~/Books/mybook.pdf

# Show table of contents
uv run ~/.claude/skills/reading-books/book.py toc ~/Books/mybook.epub

# Read a specific chapter
uv run ~/.claude/skills/reading-books/book.py read ~/Books/mybook.pdf --chapter 3

# Read a specific page
uv run ~/.claude/skills/reading-books/book.py read ~/Books/mybook.pdf --page 42

# Search for content (BM25 ranked)
uv run ~/.claude/skills/reading-books/book.py search ~/Books/mybook.pdf "query"

# Extract full text
uv run ~/.claude/skills/reading-books/book.py extract ~/Books/mybook.txt
```

## Supported Formats

| Format | Extensions               | Features                              |
| ------ | ------------------------ | ------------------------------------- |
| PDF    | `.pdf`                   | Page numbers, TOC detection, metadata |
| EPUB   | `.epub`                  | Chapters from spine, full metadata    |
| MOBI   | `.mobi`, `.azw`, `.azw3` | Basic extraction                      |
| Text   | `.txt`, `.text`, `.md`   | Chapter pattern detection             |

## When to Use

- User provides a book file and asks questions about its content
- Need to find specific quotes, passages, or information
- Navigating to specific pages or chapters in a document
- Researching topics across digital books
- Extracting text for further processing

## How It Works

1. **First access**: Extracts and caches the book content
2. **Subsequent access**: Uses cached version (invalidates on file change)
3. **Search**: BM25 algorithm ranks results by relevance
4. **Results**: Include chapter/page location for reference

## See Also

See REFERENCE.md for complete command documentation.
