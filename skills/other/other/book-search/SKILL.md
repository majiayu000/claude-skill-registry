---
context: fork
model: haiku
---

# /book-search

Search the vault's indexed book and PDF content using BM25 relevance ranking. Returns ranked results from architecture books without reading full files.

## Usage

```
/book-search <topic>
/book-search "event driven"
/book-search microservices
/book-search clean architecture
```

## Instructions

When the user invokes `/book-search <query>` or asks "which books discuss X" or "what do my books say about X":

### Phase 1: Search the Graph Index

Run the graph search filtered to book content:

```bash
node scripts/graph-query.js --search "<query>"
```

### Phase 2: Filter to Books Only

From the results, include ONLY entries where:

- Type is `PDF` (indexed PDF books)
- Type is `Page` with source field containing `.pdf` or tags containing `pdf-import` or `type/book`

**IMPORTANT: Do NOT read the full Page or PDF files.** Only use the search results (title, score, path) to present the ranked list.

### Phase 3: Present Results

Format as a concise table:

```markdown
## Books discussing "<query>"

| Score | Book                                                   | Source     |
| ----- | ------------------------------------------------------ | ---------- |
| 11.89 | Clean Architecture (Robert C. Martin)                  | PDF        |
| 8.50  | Building Microservices 2nd Ed (Sam Newman)             | Page + PDF |
| 5.45  | Fundamentals of Software Architecture (Richards, Ford) | PDF        |

_Ranked by BM25 relevance score. Use `/search <query>` for all vault content._
```

### Phase 4: Offer Follow-up (Do NOT Auto-Execute)

After presenting results, offer but do NOT automatically perform:

```
To dive deeper, I can:
- Read a specific book's Page note for key concepts
- Search for specific passages in the full extracted text
- Find related ADRs or projects that reference these concepts
```

**Wait for the user to explicitly request** before reading any files.

## Key Rules

1. **Never read full book Page notes or PDFs automatically** - only present search results
2. **Never summarise book content** unless the user explicitly asks after seeing results
3. **Always use the graph search** - never grep through PDF directories
4. **Distinguish Page notes from raw PDFs** - Page notes have curated summaries, PDFs have keyword indexes only
5. **Keep responses concise** - this is a lookup tool, not a research tool

## How Book Content is Indexed

The graph search index includes:

- **Page notes** (e.g., `Page - Building Microservices 2nd Edition.md`) — have title, keywords, tags, and excerpt
- **PDF files** (e.g., `+PDFs/buildingmicroservices2e.pdf`) — have extracted keywords and title only

Page notes contain richer metadata and will typically score higher than raw PDFs for the same book.

## Examples

```
/book-search "domain driven design"
/book-search saga
/book-search "API gateway"
/book-search resilience patterns
/book-search "data mesh"
/book-search strangler fig
```

## Related Skills

- `/search` - Full vault search (all note types)
- `/graph-query` - Direct graph queries with type/status filters
- `/related <topic>` - Find all notes mentioning a topic
