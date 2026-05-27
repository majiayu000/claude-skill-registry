````markdown
---
name: consume-book
description: >
  Search and annotate ingested books. Supports markdown/text files and EPUBs,
  tracks reading position, and stores Horus notes in memory.
triggers:
  - consume book
  - search book
  - book notes
  - bookmark book
  - resume reading
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Consume ingested books - search text, bookmark, take notes
---

# Consume Book Skill

Search and annotate ingested books. Works with content already processed by `/ingest-book`
(or any local book library directory).

## Quick Start

```bash
cd .pi/skills/consume-book

# Import books from library
./run.sh sync --books-dir ~/clawd/library/books

# Search text
./run.sh search "Emperor" --book <book_id>

# Save a bookmark
./run.sh bookmark --book <book_id> --char-position 125000

# Resume reading
./run.sh resume --book <book_id>

# Add a note at a character position
./run.sh note --book <book_id> --char-position 125000 --note "Key doctrine"

# List books
./run.sh list
```

## Commands

### Sync Books

```bash
./run.sh sync [--books-dir <path>]
```

Scans a directory for `.md`, `.txt`, and `.epub` files and imports them into the registry.

### Search Text

```bash
./run.sh search <query> [--book <book_id>] [--context <chars>]
```

Searches book text and returns matches with character positions and context.

### Bookmark

```bash
./run.sh bookmark --book <book_id> --char-position <n> [--time-spent <sec>]
```

Saves the current reading position and optional time spent.

### Resume

```bash
./run.sh resume --book <book_id>
```

Returns the last saved reading position and stats.

### Add Note

```bash
./run.sh note --book <book_id> --char-position <n> --note <text> [--agent <id>]
```

Adds a Horus note at a character position.

### List Books

```bash
./run.sh list [--json]
```

Lists all books in the registry.

## Data Storage

- **Registry**: `~/.pi/consume-book/registry.json`
- **Bookmarks**: `~/.pi/consume-book/bookmarks.json`
- **Notes**: `~/.pi/consume-book/notes/<agent_id>/notes.jsonl`
- **EPUB Cache**: `~/.pi/consume-book/cache/`

## Integration with /memory

Notes are stored in `/memory` using the consume-common memory bridge:

```bash
./memory/run.sh learn \
  --problem "Consumed book: <title>" \
  --solution "<note>" \
  --category emotional_learning \
  --tags book,horus_lupercal
```

````
