---
name: obsidian-organize
description: >-
  Organize Obsidian notes according to clawd's preferences. Use when user asks to
  "organize notes", "move notes to right folder", "clean up vault", "tidy vault",
  "file this note", or when creating new notes in the Obsidian vault. Also use when
  moving, renaming, or categorizing notes, or when the vault root has stray files.
user-invocable: false
---

# Obsidian Note Organization

Clawd's Obsidian vault follows the PARA method. Every note belongs in a specific folder — nothing lives in the vault root.

## Folder Structure

```
Vault/
├── 0. Inbox/              # Unsorted captures, quick notes
├── 1. Projects/           # Active projects with deadlines
├── 2. Areas/              # Ongoing responsibilities
├── 3. Resources/          # Reference material
│   ├── People/            # Notes about individuals
│   ├── References/        # Technical references (APIs, tools, comparisons)
│   ├── Concepts/          # Ideas, frameworks, mental models
│   └── ...                # Other resource categories as needed
├── 4. Archive/            # Completed/inactive items
└── Templates/             # Note templates
```

## Placement Rules

| Note Type | Folder | Example |
|-----------|--------|---------|
| Person (colleague, contact, public figure) | `3. Resources/People/` | `Jeffrey Peck - PSLRA Lobbyist.md` |
| API docs, tool guides, tech comparisons | `3. Resources/References/` | `Claude API - Streaming Responses.md` |
| Concepts, frameworks, mental models | `3. Resources/Concepts/` | `Efficient Market Hypothesis.md` |
| Active project with a deadline | `1. Projects/` | Current research, course prep |
| Ongoing responsibility (no end date) | `2. Areas/` | Teaching, health, finances |
| Quick capture, unsorted | `0. Inbox/` | To be filed later |
| Done, no longer active | `4. Archive/` | Past projects, old references |

## Naming Conventions

Titles should be descriptive and include context so they're findable without opening the note:

- **People**: `Full Name - Role or Context.md` (e.g., `Jeffrey Peck - PSLRA Lobbyist.md`)
- **References**: `Tool/Topic - Specific Aspect.md` (e.g., `jq - Container Compatibility Notes.md`)
- **Projects**: Use the project's natural name

Avoid generic titles like `Meeting Notes.md` or `Ideas.md` — add the date, person, or topic.

## Vault Hygiene

- The vault root directory should contain **only folders**, never loose notes
- If a note doesn't clearly fit a subcategory, place it in the parent PARA folder (e.g., `3. Resources/`) rather than the root
- When in doubt, `0. Inbox/` is the right temporary home — but follow up by filing it properly
- Periodically move completed projects from `1. Projects/` to `4. Archive/`
