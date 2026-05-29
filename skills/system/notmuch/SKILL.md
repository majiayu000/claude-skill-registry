---
name: notmuch
description: notmuch email indexer - search, threading, tagging for local Maildir. Use when searching emails, understanding notmuch queries, or integrating with notmuch.
---

# notmuch

notmuch is a system for indexing, searching, reading, and tagging large collections of email messages in Maildir format. It uses Xapian for fast full-text search.

## CRITICAL

- notmuch is **local only** - indexes your local Maildir, not IMAP directly
- Thread IDs are **internal to notmuch** - not portable across systems
- Tags are **per-message**, not per-thread
- Use with mbsync: `mbsync -a && notmuch new`

## Documentation

**Local reference:** See `references/man-pages.md` for cached man pages.

| Resource | URL |
|----------|-----|
| Official Docs | https://notmuchmail.org/doc/latest/ |
| Man Pages | https://notmuchmail.org/manpages/ |
| Search Terms | https://notmuchmail.org/doc/latest/man7/notmuch-search-terms.html |
| FAQ | https://notmuchmail.org/faq/ |
| News/Releases | https://notmuchmail.org/news/ |
| ArchWiki | https://wiki.archlinux.org/title/Notmuch |

## Core Concepts

### Data Model

```
Maildir (files)
    │
    ▼
notmuch index (Xapian database)
    │
    ├── Messages (indexed content + metadata)
    │       └── Tags (flat strings per message)
    │
    └── Threads (groupings derived from headers)
```

- **Message**: Indexed email file with full-text content
- **Thread**: Logical grouping reconstructed from In-Reply-To and References headers
- **Tag**: String label attached to individual messages (not threads)

### Threading

notmuch reconstructs threads from email headers:
- `In-Reply-To`: Direct parent message
- `References`: Chain of ancestor Message-IDs

Thread IDs are opaque internal identifiers (e.g., `thread:00000000000001dd`).

**Note:** Threading is heuristic. notmuch considers all references, not just the heuristically chosen parent.

## Commands

### Basic Operations

```bash
# Index new mail
notmuch new

# Search (returns threads)
notmuch search <query>

# Search (returns messages)
notmuch search --output=messages <query>

# Show message content
notmuch show <query>
notmuch show --format=json <query>

# Count matches
notmuch count <query>

# Tag messages
notmuch tag +inbox +unread -- <query>
notmuch tag -unread -- <query>

# List all tags
notmuch search --output=tags '*'
```

### Output Formats

```bash
# Thread list (default)
notmuch search tag:unread

# Message IDs only
notmuch search --output=messages tag:unread

# File paths only
notmuch search --output=files tag:unread

# JSON format
notmuch search --format=json tag:unread
notmuch show --format=json tag:unread

# S-expressions
notmuch search --format=sexp tag:unread
```

## Search Syntax

### Prefixes

| Prefix | Type | Description |
|--------|------|-------------|
| `from:` | Probabilistic | Sender address or name |
| `to:` | Probabilistic | Recipient address or name |
| `subject:` | Probabilistic | Subject line |
| `body:` | Probabilistic | Message body |
| `attachment:` | Probabilistic | Attachment filename |
| `mimetype:` | Probabilistic | MIME type |
| `tag:` | Boolean | Message tag |
| `id:` | Boolean | Message-ID |
| `thread:` | Boolean | Thread ID |
| `folder:` | Boolean | Maildir folder |
| `path:` | Boolean | File path |
| `date:` | Special | Date/time range |
| `lastmod:` | Special | Database modification |

### Boolean Operators

```bash
# AND (implicit with space, or explicit)
notmuch search from:alice subject:meeting
notmuch search from:alice and subject:meeting

# OR
notmuch search from:alice or from:bob

# NOT
notmuch search from:alice and not tag:spam

# XOR
notmuch search from:alice xor from:bob

# Grouping
notmuch search '(from:alice or from:bob) and tag:unread'
```

### Date Queries

```bash
# Relative dates
notmuch search date:today
notmuch search date:yesterday
notmuch search date:last_week
notmuch search date:this_month
notmuch search date:7_days_ago..today

# Absolute dates
notmuch search date:2024-01-01..2024-01-31
notmuch search date:2024-01-01..

# Timestamps
notmuch search date:@1234567890..@1234567900
```

### Regex Support (Xapian 1.4+)

```bash
# Regex on from/subject
notmuch search 'from:/.*@amazon\./'
notmuch search 'subject:/order.*shipped/'
```

### Thread Queries

```bash
# By thread ID
notmuch search thread:00000000000001dd

# Indirect: threads containing messages matching query
notmuch search 'thread:{from:alice}' and 'thread:{subject:crypto}'
```

## Tags

### Built-in Tags

| Tag | Description | Maildir Sync |
|-----|-------------|--------------|
| `inbox` | Default for new messages | No |
| `unread` | Not yet read | Syncs to Maildir flag |
| `draft` | Draft message | Syncs to Maildir flag |
| `flagged` | Starred/important | Syncs to Maildir flag |
| `replied` | Replied to | Syncs to Maildir flag |
| `passed` | Forwarded | Syncs to Maildir flag |

### Tag Operations

```bash
# Add tags
notmuch tag +important +work -- from:boss@company.com

# Remove tags
notmuch tag -inbox -unread -- tag:archived

# Multiple operations
notmuch tag +archived -inbox -- date:..2023-01-01

# Tag all messages in a thread
notmuch tag +project-x -- thread:00000000000001dd
```

### Maildir Flag Sync

notmuch can sync certain tags to Maildir flags (visible to other clients):

```ini
# In notmuch config
[maildir]
synchronize_flags=true
```

Mapped tags: draft, flagged, passed, replied, unread (S flag)

## Configuration

```bash
# Show config
notmuch config list

# Set config
notmuch config set user.name "Your Name"
notmuch config set user.primary_email "you@example.com"

# Database path
notmuch config set database.path "/path/to/mail"
```

### Config File Location

- `~/.notmuch-config` (legacy)
- `$XDG_CONFIG_HOME/notmuch/default/config` (modern)
- `$NOTMUCH_CONFIG` environment variable

### New Mail Tags

```ini
[new]
tags=unread;inbox
ignore=.mbsyncstate;.strstrignore
```

## Hooks

notmuch supports hooks for automation:

```
~/.config/notmuch/default/hooks/
├── pre-new      # Before indexing
└── post-new     # After indexing
```

Example post-new hook:
```bash
#!/bin/bash
# Auto-tag based on rules
notmuch tag +newsletter -- from:*@substack.com and tag:new
notmuch tag -new -- tag:new
```

## API & Bindings

### C Library (libnotmuch)

Core functions:
- `notmuch_database_open` / `notmuch_database_create`
- `notmuch_query_create` / `notmuch_query_search_messages`
- `notmuch_message_get_tags` / `notmuch_message_add_tag`

### Python Bindings

```python
# Modern (notmuch2 - CFFI based)
import notmuch2

with notmuch2.Database() as db:
    for msg in db.messages('tag:unread'):
        print(msg.header('Subject'))

# Legacy (deprecated, removed in 0.39)
import notmuch  # Don't use
```

### Other Bindings

- Emacs: Full MUA built-in
- Vim: notmuch-vim plugin
- Go: go-notmuch
- Ruby: notmuch gem

## Integration with Other Tools

### mbsync

```bash
# Sync then index
mbsync -a && notmuch new
```

### himalaya

himalaya can use notmuch as a backend for search.

### aerc

Terminal MUA with native notmuch support.

### Emacs

notmuch ships with a full Emacs interface.

## Strengths (Don't Replicate)

| Capability | Why It's Good |
|------------|---------------|
| **Full-text search** | Xapian is battle-tested, handles 100k+ messages |
| **Threading** | Correct reconstruction from headers |
| **Maildir integration** | Direct file access, no sync issues |
| **Fast tagging** | Immediate, lightweight |
| **Incremental indexing** | `notmuch new` only indexes new messages |
| **Stable** | Mature, reliable, used by power users for years |

## Limitations

| Limitation | Impact |
|------------|--------|
| **No relational queries** | Can't join sender info with thread analysis |
| **Tags are flat strings** | No hierarchy, metadata, or relations |
| **No structured data** | Can't store "tracking_number = X" |
| **No computed properties** | Thread participant count needs manual query |
| **Thread ID is opaque** | Can't query thread properties directly |
| **Local only** | Thread IDs not portable across machines |
| **Per-message tags** | Tagging a "thread" means tagging all messages |

## Common Patterns

### Auto-tagging in post-new hook

```bash
#!/bin/bash
# Tag newsletters
notmuch tag +newsletter -inbox -- \
  '(from:*@substack.com or from:*@buttondown.email) and tag:new'

# Tag receipts
notmuch tag +receipt -- \
  'subject:receipt or subject:invoice and tag:new'

# Clear new tag
notmuch tag -new -- tag:new
```

### Export thread as mbox

```bash
notmuch show --format=mbox thread:xxx > thread.mbox
```

### Find large threads

```bash
# No direct way - must iterate
notmuch search '*' | while read -r line; do
  thread_id=$(echo "$line" | cut -d' ' -f1)
  count=$(notmuch count "thread:$thread_id")
  echo "$count $thread_id"
done | sort -rn | head -10
```

### Backup tags

```bash
notmuch dump > tags-backup.txt
notmuch restore < tags-backup.txt
```

## Version Requirements

- Xapian 1.4.0+ (for regex support)
- GMime 3.0.3+
- Python 3.x for notmuch2 bindings

## Attribution

Research compiled 2026-01-11 from:
- https://notmuchmail.org/doc/latest/
- https://notmuchmail.org/news/
- https://notmuchmail.org/manpages/notmuch-search-terms-7/
- https://wiki.archlinux.org/title/Notmuch
- https://notmuchmail.org/faq/
