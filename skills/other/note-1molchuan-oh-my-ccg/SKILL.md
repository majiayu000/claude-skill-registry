---
name: note
description: 保存会话笔记到记事本，防止上下文压缩丢失
---

# oh-my-ccg Note

Save important information to the session notepad.

## Usage
`/oh-my-ccg:note <content>` — Add to working memory (auto-pruned after 7 days)
`/oh-my-ccg:note --priority <content>` — Set priority context (always loaded, max 500 chars)
`/oh-my-ccg:note --permanent <content>` — Add to manual section (never auto-pruned)
`/oh-my-ccg:note --read [section]` — Read notepad (all/priority/working/manual)
`/oh-my-ccg:note --prune [days]` — Prune entries older than N days (default 7)

## Sections
- **Priority**: Max 500 chars. Loaded at every session start. Use for critical project context.
- **Working**: Timestamped entries. Auto-pruned after 7 days. Use for session-specific notes.
- **Manual**: Permanent entries. Never auto-pruned. Use for long-term references.

## Storage
File: `.oh-my-ccg/notepad.md`
