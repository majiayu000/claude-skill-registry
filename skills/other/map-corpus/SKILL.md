---
name: map-corpus
description: 'Use when the user points at a folder of their own study material and wants it made teachable: inventory the sources, name the concepts they cover, and order those concepts by what has to come first. For learning a topic with no material of your own, use teach.'
argument-hint: "Which folder holds the material?"
---

This skill reads a folder and writes one file. Nothing under the corpus root changes.

## What you do

1. **Resolve the folder.** Take it from the argument; ask once when missing. Expand `~`, resolve the absolute path, and confirm it exists and is a directory. Read every file under it, recursing into subfolders. Done when every file is either inventoried or listed as unreadable.
2. **Inventory.** One table row per readable file: path relative to the corpus root, kind, and the headings worth citing. Done when the row count equals the readable-file count.
3. **Name the concepts.** For each concept the corpus teaches: the term, one sentence of what it is, and the citation anchor where it is taught. Prefer the term the source uses. Done when every inventoried file contributes a concept or is marked `reference only` in its row.
4. **Order them.** Each concept names what it needs first in its `Needs:` field. Emit a flat numbered list where nothing appears before its prerequisites. Two concepts needing each other: keep the one the corpus introduces first and note the cycle on the other's line. Done when no concept lists a prerequisite appearing later.

## CORPUS.md

Write this file at the workspace root, beside `PROGRESS.md` when it exists. It is the only output. One fenced block shapes it:

```md
# Corpus: {name}

corpus_root: {absolute path}
mapped: {YYYY-MM-DD}

## Sources

| File | Kind | Cite from |
|---|---|---|
| ch03-locks.md | textbook | #mutual-exclusion, #deadlock |
| notes/standup.md | work document | reference only |

## Concepts

1. **Mutual exclusion** — only one thread holds the resource at a time. Needs: none. Source: `ch03-locks.md#mutual-exclusion`
2. **Deadlock** — a cycle of threads each holding what the next one waits for. Needs: mutual exclusion. Source: `ch03-locks.md#deadlock`

## Unreadable

- `scan.pdf` — no text layer. Convert it and re-run this skill.
```

## Rules

- Read the corpus and write one file, `CORPUS.md`, at the workspace root. Files under the corpus root stay exactly as they are.
- **Citation anchor form**, used here and by every skill citing the corpus: `<path-relative-to-corpus-root>#<heading-slug>`, falling back to `<path>:<start>-<end>` when the source carries no headings.
- Name unreadable files, say what each is, and finish the map for the rest. Converting them is the user's call; this skill recommends no converter and runs none.
- The concept list is a spine, not an index. Past roughly forty concepts, merge the ones always taught together.
- Re-running rewrites `CORPUS.md` whole. It holds no state worth preserving; `PROGRESS.md` does. See [CORPUS-FORMAT.md](references/CORPUS-FORMAT.md) for the row and anchor contracts.
- Keep paths in `CORPUS.md` relative to the corpus root, not to the workspace. An absolute path in the Sources table ties the map to one machine.

