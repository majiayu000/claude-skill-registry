---
name: readwise-docs
description: Manage Readwise Reader documents. Use when the user wants to list, save, update, or delete documents in their Reader library. Triggers on "add to reader", "save article", "list my documents", "readwise list", "reader documents".
context: fork
agent: librarian
user-invocable: false
---

# Readwise Reader Document Management

CRUD operations on the Reader document library via official CLI (`readwise`) and custom CLI (`readwise-custom`).

## Commands — Official CLI (`readwise`)

### List Documents

```bash
readwise reader-list-documents                                    # All documents (limit 10)
readwise reader-list-documents --limit 20                         # First 20
readwise reader-list-documents --tag "proxy advisors"             # By tag (up to 5 for AND logic)
readwise reader-list-documents --category pdf --location archive  # By category + location
readwise reader-list-documents --updated-after 2026-01-01T00:00:00Z
readwise reader-list-documents --seen false                       # Unseen only
readwise reader-list-documents --response-fields title,author,summary  # Reduce token usage
readwise reader-list-documents --id <id>                          # Specific document
```

**Filter values:**

| Flag | Values |
|------|--------|
| `--location` | `new` (inbox), `later`, `shortlist`, `archive`, `feed` |
| `--category` | `article`, `email`, `rss`, `highlight`, `note`, `pdf`, `epub`, `tweet`, `video`, `podcast`, `audiobook` |
| `--tag` | Any tag name (up to 5 tags for AND logic) |
| `--seen` | `true` (opened), `false` (unopened) |

### Search Documents (Hybrid)

```bash
readwise reader-search-documents --query "proxy advisors"
readwise reader-search-documents --query "regulation" --author-search "Jackson"
readwise reader-search-documents --query "AI" --category-in article --location-in later,archive
readwise reader-search-documents --query "climate" --published-date-gt 2025-01-01
```

### Get Document

```bash
readwise reader-get-document-details --document-id <id>   # Returns markdown content
```

### Save URL

```bash
readwise reader-create-document --url https://example.com/article
readwise reader-create-document --url https://example.com --title "Title" --tags research,ai --notes "Note"
readwise reader-create-document --title "Custom Doc" --markdown "# Content..." --url "https://me.com#doc1"
```

### Move Documents

```bash
readwise reader-move-documents --document-ids <id1>,<id2> --location archive   # Max 50 per call
readwise reader-move-documents --document-ids <id> --location later
```

### Bulk Edit Metadata

```bash
readwise reader-bulk-edit-document-metadata --documents '[{"document_id": "<id>", "seen": true}]'
readwise reader-bulk-edit-document-metadata --documents '[{"document_id": "<id>", "title": "New Title"}]'
```

### Tags

```bash
readwise reader-list-tags                                                    # List all tags
readwise reader-add-tags-to-document --document-id <id> --tag-names important,research
readwise reader-remove-tags-from-document --document-id <id> --tag-names old-tag
```

### Highlights

```bash
readwise reader-get-document-highlights --document-id <id>
readwise reader-create-highlight --document-id <id> --html-content "<p>passage</p>"
readwise reader-create-highlight --document-id <id> --html-content "<p>passage</p>" --note "Note" --tags concept
readwise reader-add-tags-to-highlight --document-id <id> --highlight-document-id <hid> --tag-names concept
readwise reader-set-highlight-notes --document-id <id> --highlight-document-id <hid> --notes "Updated note"
```

### Export

```bash
readwise reader-export-documents                                         # Full library as ZIP of markdown
readwise reader-export-documents --since-updated "2026-01-01T00:00:00Z"  # Delta export
readwise reader-get-export-documents-status --export-id <id>             # Check status
```

## Commands — Custom CLI (`readwise-custom`)

### Delete Document (not available in official CLI)

```bash
readwise-custom delete <id>
```

### Highlights & Books (v2 API)

```bash
readwise-custom highlights                              # All highlights
readwise-custom highlights --search "fiduciary"         # Keyword search
readwise-custom highlights --book-id 12345 --json       # By source

readwise-custom books                                   # All sources
readwise-custom books --category articles --search "law"
```

### Upload File (PDF/EPUB)

```bash
readwise-custom upload <file.pdf>
readwise-custom upload <file.epub>
```

## Piping & Scripting

All commands support `--json` for machine-readable output:

```bash
# Get IDs of all PDFs
readwise reader-list-documents --category pdf --json | jq -r '.results[].id'

# Count highlights per book
readwise-custom books --json | jq '.[] | {title, num_highlights}'

# Export all tags
readwise reader-list-tags --json > tags.json
```
