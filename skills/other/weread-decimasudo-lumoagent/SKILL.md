---
name: weread
description: |
  WeChat Reading (微信读书) CLI tool for fetching notes and highlights.
  Use when: (1) user asks about weread/微信读书 notes or highlights,
  (2) fetching today's or recent reading notes, (3) exporting book highlights,
  (4) managing reading bookshelf, (5) any task involving reading notes from WeChat Reading.
---

# weread-cli

CLI tool for fetching notes and highlights from WeChat Reading (微信读书).

## Quick Start

```bash
# Login via WeChat QR code
weread login

# List books with notes
weread list

# Get highlights from a book
weread get <bookId>
```

## Commands

### Authentication

```bash
weread login     # Open browser for QR code login
weread logout    # Clear saved cookies
weread whoami    # Check login status
```

### Fetching Data

```bash
# List all books with notes
weread list [--json]

# Get book highlights and reviews
weread get <bookId> [options]
  --json, -j       JSON output
  --highlights, -H Only show highlights
  --reviews, -R    Only show reviews
  --since, -s      Filter by date (today, yesterday, YYYY-MM-DD)

# List books from shelf (sorted by recent read time)
weread shelf [-n <limit>] [--json]
```

## Practical Examples

### 1. Get Today's/Yesterday's Notes

Fetch notes created after a specific date:

```bash
# Today's highlights from a book
weread get CB_3x2HoH --since today

# Yesterday's notes
weread get CB_3x2HoH --since yesterday

# Notes after a specific date
weread get CB_3x2HoH --since 2024-01-15
```

### 2. Export to Markdown

Export book highlights as Markdown file:

```bash
# Export highlights only
weread get CB_3x2HoH -H > notes.md

# Full export with reviews
weread get CB_3x2HoH > notes.md
```

The text output is already formatted with chapter headers (`## Chapter`) and quote markers (`>`).

### 3. JSON + jq Processing

Use JSON output for batch processing:

```bash
# Get all highlight texts
weread get CB_3x2HoH --json | jq -r '.highlights[].markText'

# Count highlights per chapter
weread get CB_3x2HoH --json | jq '.chapters | length'

# Extract book info
weread get CB_3x2HoH --json | jq '.book | {title, author}'

# List all book IDs with notes
weread list --json | jq -r '.[].bookId'

# Get total highlight count across all books
weread list --json | jq '[.[].bookmarkCount] | add'
```

### 4. Shelf Management

List and manage your bookshelf:

```bash
# Recent 10 books
weread shelf -n 10

# All books as JSON
weread shelf --json

# Get book IDs from shelf
weread shelf --json | jq -r '.[].bookId'
```

### 5. Get Recent Notes from All Books

Workflow: Get shelf -> Fetch today's notes from each book:

```bash
# Step 1: Get recent books from shelf
weread shelf -n 5 --json | jq -r '.[].bookId'

# Step 2: For each book, fetch today's notes
for id in $(weread shelf -n 5 --json | jq -r '.[].bookId'); do
  echo "=== Book: $id ==="
  weread get "$id" --since today -H
done

# One-liner: Recent notes from top 3 books
for id in $(weread shelf -n 3 --json | jq -r '.[].bookId'); do weread get "$id" --since today; done
```

With book titles:

```bash
# Get recent notes with book titles
weread shelf -n 5 --json | jq -c '.[] | {id: .bookId, title: .title}' | while read book; do
  id=$(echo "$book" | jq -r '.id')
  title=$(echo "$book" | jq -r '.title')
  echo "=== $title ==="
  weread get "$id" --since today -H
done
```

## Authentication Options

Priority: ENV variable > Local cache > CookieCloud

1. **QR Login** (recommended):
   ```bash
   weread login
   ```

2. **Environment variable**:
   ```bash
   export WEREAD_COOKIE="wr_vid=xxx;wr_skey=xxx"
   weread list
   ```

3. **CookieCloud** (for synced cookies):
   ```bash
   export COOKIECLOUD_SERVER="https://your-server.com"
   export COOKIECLOUD_UUID="your-uuid"
   export COOKIECLOUD_PASSWORD="your-password"
   weread list
   ```

## FAQ

**Q: How do I find a book's ID?**
```bash
weread list --json | jq '.[] | {title: .book.title, id: .bookId}'
```

**Q: Cookie expired?**
```bash
weread logout && weread login
```

**Q: Where are cookies stored?**
`~/.config/weread/cookies.json`
