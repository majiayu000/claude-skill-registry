---
name: source-research
description: Search and cite primary sources from Source Library. Use when asked what historical authors wrote, to find quotes from old texts, investigate alchemical or philosophical works, or cite translated Latin/German sources.
---

# Source Research

Search the Source Library collection of translated historical texts and retrieve quotes with citations.

## When to Use

- "What did Drebbel write about..."
- "Find quotes about quintessence"
- "What do historical sources say about..."
- "Cite primary sources for..."

## API Endpoints

### Search

```bash
curl -s "https://sourcelibrary.org/api/search?q=QUERY"
```

Options: `language=Latin`, `has_doi=true`, `limit=10`

### Get Quote

```bash
curl -s "https://sourcelibrary.org/api/books/BOOK_ID/quote?page=N"
```

Returns translation, original text, and citation.

### Get Book

```bash
curl -s "https://sourcelibrary.org/api/books/BOOK_ID"
```

## Workflow

1. Search for the topic
2. Note book IDs and page numbers from results
3. Get full quotes from relevant pages
4. Present findings with inline citations

## Example

```bash
# Search
curl -s "https://sourcelibrary.org/api/search?q=quintessence&limit=5"

# Get quote
curl -s "https://sourcelibrary.org/api/books/6836f8ee811c8ab472a49e36/quote?page=57"
```

## Citing

Use the `citation.inline` from the response:

> "The Fifth Essence, red like a ruby, is immutable." (Drebbel 1628, p. 57)
