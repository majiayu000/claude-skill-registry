---
name: markdown-converter
description: "Convert PDF, Office, HTML, data, media, ZIP to Markdown."
user_invocable: false  # default -- router-dispatched, not user-typed
agent: python-general-engineer
allowed-tools:
  - Bash
  - Read
routing:
  triggers:
    - "convert to markdown"
    - "markitdown"
    - "extract text from PDF"
    - "PDF to markdown"
    - "docx to markdown"
    - "ingest document"
  category: research
  pairs_with:
    - research-pipeline
    - enterprise-search
---

# Markdown Converter

Convert a file to Markdown with markitdown, zero install:

```bash
uvx 'markitdown[all]' input.pdf -o output.md   # to file
uvx 'markitdown[all]' input.docx               # to stdout
cat blob | uvx 'markitdown[all]' -x .pdf       # stdin, with extension hint
```

When `uvx` is missing, run `pipx run 'markitdown[all]' …` with the same arguments. First run downloads dependencies; later runs hit the cache. Output preserves headings, tables, lists, and links.

For video transcripts, use the `video-transcript` skill.

## Formats

| Input | Notes |
|---|---|
| PDF, .docx, .pptx, .xlsx, .xls | Document structure preserved |
| HTML, CSV, JSON, XML | Structured Markdown |
| Images | EXIF metadata + OCR text |
| Audio | EXIF metadata + speech transcription |
| ZIP, EPub | Iterates contents, converts each |

## Options

| Flag | Effect |
|---|---|
| `-o FILE` | Write output to FILE |
| `-x .EXT` | Extension hint for stdin input |
| `-m MIME` | MIME-type hint |
| `-c CHARSET` | Charset hint, e.g. UTF-8 |

## Error handling

### Garbled or empty text from a scanned PDF
Cause: page is an image; the base extractor reads text layers only.
Solution: render pages to images (`pdftoppm`), then convert the images so OCR runs.
