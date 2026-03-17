---
name: process-inbox
description: Process notes in inbox folder. Use when user wants to organize inbox, triage notes, or clean up captured items. Triggers on "process inbox", "organize notes", "inbox zero", "triage".
allowed-tools: Read, Write, Edit, Glob, Bash(mv:*)
model: claude-haiku-4-5-20251001
---

# Inbox Processing

Help process notes in `my-vault/01 Inbox/`.

## For Each Note

1. Read and understand the content
2. Ask one of:
   - Where should this go? (suggest folder based on content)
   - Should this be linked to existing topics?
   - Is this actionable, reference, or can be deleted?
3. Help move/organize based on response

## Folder Destinations

| Folder | Content Type |
|--------|--------------|
| `my-vault/03 Topics/` | Topic-based Maps of Content |
| `my-vault/04 Personal/` | Personal notes, decisions, career |
| `my-vault/05 Projects/` | Active project notes |
| `my-vault/06 Knowledge Base/` | Courses, tech notes, references |

## Processing Tips

- Add appropriate frontmatter if missing
- Suggest topic links based on content
- Flag potential duplicates
- Process one note at a time, don't overwhelm

## Start

List what's in the inbox first.
