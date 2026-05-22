---
name: readwise
description: Manage Readwise highlights, books, daily review, and Reader documents (save-for-later / read-it-later). Use when the user wants to save articles or URLs to Reader, browse their reading list, search saved documents, review highlights, create or manage highlights and notes, check their daily review, list books/sources, or interact with Readwise/Reader in any way.
---

# Readwise & Reader

Interact with Readwise (highlights, books, daily review) and Reader (save-for-later documents) via the bundled CLI script.

## Setup

Requires `READWISE_TOKEN` env var. Get a token at https://readwise.io/access_token — works for both Readwise and Reader APIs.

## CLI Usage

```bash
scripts/readwise.sh [--pretty] <command> [args...]
```

### Reader Commands (Documents)

```bash
# Save a URL to Reader
readwise.sh save "https://example.com/article" --location later --tags "ai,research"

# List reading list (inbox)
readwise.sh list --location later --limit 10

# Search documents by title/author
readwise.sh search "transformer"

# Update a document
readwise.sh update DOC_ID --location archive --tags "done,good"

# Delete a document
readwise.sh delete DOC_ID

# List all tags
readwise.sh tags
```

### Readwise Commands (Highlights & Books)

```bash
# Get today's daily review
readwise.sh review

# Export highlights (optionally for a specific book)
readwise.sh highlights --book-id 12345 --limit 20

# Get a single highlight
readwise.sh highlight 456789

# Create a highlight
readwise.sh highlight-create --text "Important quote" --title "Book Name" --note "My thought"

# Update highlight color/note
readwise.sh highlight-update 456789 --color blue --note "Updated note"

# Delete a highlight
readwise.sh highlight-delete 456789

# List books/sources
readwise.sh books --category articles --limit 10

# Get book details
readwise.sh book 12345
```

### Output

All commands output JSON. Add `--pretty` for formatted output.

## Common Workflows

**Save article and tag it:**
```bash
readwise.sh save "https://arxiv.org/abs/2401.12345" --title "Cool Paper" --tags "ml,papers" --location later
```

**Check reading list:**
```bash
readwise.sh list --location later --limit 5
```

**Today's review highlights:**
```bash
readwise.sh review
```

**Find highlights about a topic:** Export all highlights then filter, or search Reader docs:
```bash
readwise.sh search "attention mechanism"
readwise.sh highlights --updated-after "2024-01-01"
```

**Archive finished articles:**
```bash
readwise.sh update DOC_ID --location archive
```

## API Reference

For detailed endpoint documentation, parameters, and response shapes, read [references/api.md](references/api.md).

Key details:
- **Rate limits**: Readwise v2: 240 req/min (20/min for list endpoints). Reader v3: 20 req/min (50/min for create/update).
- **Categories**: Books: `books, articles, tweets, podcasts`. Reader: `article, email, rss, highlight, note, pdf, epub, tweet, video`.
- **Locations** (Reader): `new, later, shortlist, archive, feed`
- **Highlight colors**: `yellow, blue, pink, orange, green, purple`
