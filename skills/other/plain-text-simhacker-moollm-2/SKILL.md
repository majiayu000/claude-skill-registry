---
name: plain-text
description: "Text files are forever. No lock-in. No corruption. No transformation."
license: MIT
tier: 0
protocol: PLAIN-TEXT
allowed-tools:
  - read_file
  - write_file
origin: "Unix Philosophy — 'Text is the universal interface'"
lineage:
  - "Unix Philosophy — Text streams, pipes"
  - "Donald Knuth — Literate Programming"
  - "John Gruber — Markdown (2004)"
  - "Anil Dash — 'How Markdown Took Over the World' (2025)"
related: [yaml-jazz, markdown, sniffable-python, format-design, constructionism, session-log]
tags: [moollm, philosophy, format, durability, git, llm]
---

# Plain Text

> *"I don't want to worry about whatever cursed format OneNote uses still being something I can extract in 2035."*
> — @Havoc, Hacker News (2025)

---

## What Is It?

**Plain text** is MOOLLM's substrate. Everything important is stored in human-readable text files:

- **SESSION.md** — Session logs in Markdown
- **ROOM.yml** — Room state in YAML
- **CHARACTER.yml** — Character data in YAML
- **SKILL.md** — Skill documentation in Markdown

No proprietary formats. No binary blobs. No databases. **Just text.**

---

## Why Plain Text Wins

### 1. Durability

| Format | Status in 2004 | Status in 2025 | Status in 2045? |
|--------|----------------|----------------|-----------------|
| Microsoft Word .doc | Ubiquitous | Legacy | Unknown |
| OneNote | New | Current | Unknown |
| Markdown .md | New | Ubiquitous | **Still readable** |
| Plain .txt | Ancient | Universal | **Still readable** |

Text files from 1970 are still readable. They will be readable in 2070.

### 2. No Lock-In

```
# This file requires:
# - Any text editor
# - That's it
```

No vendor. No license. No subscription. No "cloud service discontinued."

### 3. Git-Friendly

```diff
- player_location: start
+ player_location: maze
```

Plain text diffs are:
- **Readable** — Humans understand the change
- **Mergeable** — Git can combine concurrent edits
- **Auditable** — History is meaningful

### 4. LLM-Native

From Anil Dash (2025):

> *"All of it — all of it — is controlled through Markdown files. When you see the brilliant work shown off from somebody who's bragging about what they made ChatGPT generate for them... all of the most advanced work has been prompted in Markdown."*

LLMs:
- Are **trained on** plain text (GitHub, web, books)
- **Output** plain text naturally
- **Understand** structure in text (headers, indentation, bullets)
- **Process** text more efficiently than structured formats

### 5. Inspectable

```bash
cat SESSION.md     # Read it
grep "player" *.yml # Search it
diff old.yml new.yml # Compare it
git log SESSION.md  # Track it
```

No special tools. No viewers. No converters.

---

## The Unix Philosophy

Ken Thompson and Dennis Ritchie knew this in 1969:

> *"Text is the universal interface."*

Pipes, streams, filters — all work on text:

```bash
cat rooms/*.yml | grep "exits" | sort | uniq
```

MOOLLM inherits this: **the filesystem IS the database**.

---

## Plain Text Formats in MOOLLM

| Format | Extension | Purpose |
|--------|-----------|---------|
| **Markdown** | `.md` | Prose, documentation, session logs |
| **YAML** | `.yml` | Structured data with comments |
| **Templates** | `.tmpl` | Empathic templates (YAML + placeholders) |

All are plain text. All are human-readable. All work with standard tools.

---

## The "Worse is Better" Principle

Richard Gabriel (1989):

> *"Simplicity is the most important consideration in a design."*

Markdown is "worse" than DocBook:
- Fewer features
- Less precise
- Less formally specified

But Markdown **won** because:
- **Easier to learn** — 5 minutes
- **Easier to read** — Raw or rendered
- **Easier to write** — No closing tags
- **Easier to implement** — Hundreds of parsers

**Simple formats that actually get used beat complex formats that don't.**

---

## Plain Text and AI

The entire trillion-dollar AI industry runs on plain text:

| AI Component | Format |
|--------------|--------|
| Training data | Text files (books, web, code) |
| Prompts | Markdown / plain text |
| Outputs | Text / Markdown |
| Context windows | Measured in text tokens |
| RAG documents | Often Markdown |
| Agent instructions | Markdown files |

From Anil Dash:

> *"The trillion-dollar AI industry's system for controlling their most advanced platforms is a plain text format one guy made up for his blog."*

---

## MOOLLM's Commitment

### 1. Files as State

No databases. State is in files:

```
adventure-4/
├── ADVENTURE.yml      # Game state
├── start/
│   ├── ROOM.yml       # Room state
│   └── lamp.yml       # Object state
└── characters/
    └── don-hopkins/
        └── CHARACTER.yml  # Character state
```

### 2. Human-Readable Always

If a human can't read the file in vim, rethink the format.

### 3. Comments ARE Data

```yaml
# CRITICAL: Do not delete this
# It contains the player's memories
memories:
  - "Met Bumblewick in the maze"
```

Comments are preserved, not stripped.

### 4. No Transformation Gap

The YAML you write is the YAML that runs. No compilation step hides meaning.

---

## Anti-Patterns

❌ **Binary formats** — Opaque, require special tools  
❌ **Proprietary formats** — Lock-in, potential for obsolescence  
❌ **Database-only state** — Not inspectable, not git-friendly  
❌ **Generated-only files** — If no human source exists, fragile  
❌ **Minified output** — Readable formats should stay readable

---

## Exceptions

Some things aren't text:

- **Images** — Binary, but referenced from text
- **Audio/Video** — Binary, but metadata in YAML
- **Large datasets** — May need binary for performance

For these: keep the **metadata and references** in plain text, even if the content is binary.

---

## Dovetails With

- [markdown/](../markdown/) — The primary prose format
- [yaml-jazz/](../yaml-jazz/) — The primary data format
- [session-log/](../session-log/) — Plain text session history
- [postel/](../postel/) — Be liberal in parsing text
- [files-as-state/](../room/) — The filesystem is the database

---

## Protocol Symbol

```
PLAIN-TEXT
```

Invoke when: Choosing formats, designing storage, considering durability.

---

## The Bottom Line

> *"Markdown files from 2004 are still readable today. They'll be readable in 2045. Plain text is forever."*

Write for the future. Write in plain text.
