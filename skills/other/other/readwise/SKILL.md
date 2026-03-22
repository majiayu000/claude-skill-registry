---
name: readwise
description: This skill should be used when the user asks to "search Readwise", "find highlights", "get quotes from my reading", "add highlights to notebook", "search my annotations", "get full document text", "fetch article content", "add tagged documents to notebook", or needs to query their Readwise library.
version: 1.0.0
context: fork
agent: librarian
user-invocable: false
---

# Readwise

<EXTREMELY-IMPORTANT>
## IRON LAW: Main Chat NEVER Calls Readwise CLI

**EVERY READWISE OPERATION MUST GO THROUGH LIBRARIAN. This is not negotiable.**

Main chat MUST NOT:
- Run `readwise` CLI commands directly
- Run `readwise-custom` CLI commands directly
- "Just quickly check" highlights

**If you're about to do anything Readwise in main chat, STOP. Spawn a librarian sub-agent instead.**
</EXTREMELY-IMPORTANT>

### Permission Model

| Context | Readwise CLI | readwise-custom CLI |
|---------|-------------|-------------------|
| Main chat | **FORBIDDEN** | **FORBIDDEN** |
| Librarian sub-agent | ALLOWED | ALLOWED |

### Red Flag Detection

```
STOP if you catch yourself thinking:
- "Let me quickly search Readwise..."
- "I'll just run readwise reader-search-documents..."
- "I'll just run readwise-custom search..."

These thoughts in MAIN CHAT = VIOLATION. Delegate instead.
```

### Correct Pattern

```
User: "Search my Readwise for proxy advisor articles"

MAIN CHAT RESPONSE:
Task(subagent_type="workflows:librarian", prompt="Search Readwise for proxy advisor articles and summarize findings")

NEVER IN MAIN CHAT:
readwise readwise-search-highlights --vector-search-term "proxy advisors"
readwise-custom search "proxy advisors"
```

---

## Two CLIs

| CLI | Binary | Use for |
|-----|--------|---------|
| **Official** (`@readwise/cli`) | `readwise` | Search, list, get, save, move, tags, highlights CRUD, export, daily review |
| **Custom** (`~/projects/readwise-cli/`) | `readwise-custom` | Chat/RAG, ghostreader, file upload (PDF/EPUB), prune, keyword highlight search |

---

## Tag-Based Workflow

<EXTREMELY-IMPORTANT>
**When user mentions items were added by tag, NEVER use semantic search.**

### Trigger Phrases
- "we added items tagged X"
- "I thought we added X to NLM"
- "items tagged [tag]"
- "documents with tag [tag]"

### Required Workflow

```
User mentions tagged items or NLM content
              │
              ▼
    ┌──────────────────────────────────┐
    │ 1. CHECK NLM FIRST              │ ← MANDATORY
    │    nlm list                     │
    │    nlm chat <id>                │
    └──────────────────────────────────┘
              │
       Not in NLM?
              ▼
    ┌──────────────────────────────────┐
    │ 2. USE readwise for tagged items │
    │    readwise reader-list-documents│
    │    --tag "X"                     │
    │    NOT search!                   │
    └──────────────────────────────────┘
```
</EXTREMELY-IMPORTANT>

---

## Quick Reference

### Official CLI (`readwise`)

| Need | Command |
|------|---------|
| Semantic search highlights | `readwise readwise-search-highlights --vector-search-term "query"` |
| Search documents (hybrid) | `readwise reader-search-documents --query "query"` |
| Documents by tag | `readwise reader-list-documents --tag "X"` |
| Full document (markdown) | `readwise reader-get-document-details --document-id <id>` |
| List all tags | `readwise reader-list-tags` |
| Save URL | `readwise reader-create-document --url <url>` |
| Move documents | `readwise reader-move-documents --document-ids <id> --location archive` |
| Bulk edit metadata | `readwise reader-bulk-edit-document-metadata --documents '[...]'` |
| Export library | `readwise reader-export-documents` |
| Daily review | `readwise readwise-get-daily-review` |

Add `--json` to any command for machine-readable output.

### Custom CLI (`readwise-custom`)

| Need | Command |
|------|---------|
| RAG chat over highlights | `readwise-custom chat "question"` |
| Keyword search highlights | `readwise-custom highlights --search "term"` |
| Prune stale docs | `readwise-custom prune` |
| Upload PDF/EPUB | `readwise-custom upload <file>` |
| Ghostreader | `readwise-custom ghostread summarize <id>` |
| Full document (HTML) | `readwise-custom get <id> --html` |

**Sub-skills with detailed reference:**

| Skill | Purpose |
|-------|---------|
| `readwise-search` | Vector + fulltext highlight search |
| `readwise-docs` | Document CRUD (list, get, save, move, bulk edit, export) |
| `readwise-chat` | GPT-5.1 RAG chat over highlights (fallback — prefer search + Claude synthesis) |
| `readwise-prune` | Two-pass stale document cleanup |

---

## Batch Add to NLM (by tag)

```bash
python3 /Users/vwh7mb/projects/workflows/skills/readwise/scripts/readwise_to_nlm.py \
  --tag "proxy advisors" --tag "disclosure" \
  --notebook <notebook-id>
```

Add `--dry-run` to preview. Add `--verbose` for detailed output.

## Anti-Pattern: Never Fetch from Source URL

**WRONG:** Search Readwise, find document, fetch from original URL (fails for paywalled content).

**RIGHT:** Search Readwise, get full text FROM READWISE using `readwise reader-get-document-details --document-id <id>`.

If a document is in Readwise, the full text is already there. Never go back to the source URL.
