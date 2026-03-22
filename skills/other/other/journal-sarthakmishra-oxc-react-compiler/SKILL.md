---
name: journal
description: Implementation journal maintenance. Records completed work as phase entries in .journal/ with file tables, upstream references, and technical narrative. Use after completing a compiler pass, feature, or refactor.
---

# Journal — Implementation Log

You maintain the `.journal/` directory — a chronological log of all implementation work.

## Entry Format

Each phase entry follows this structure:

```markdown
---

## Phase {N}: {Short Title}

**Date:** {YYYY-MM-DD}
**Task:** {.todo/file.md -- Section name, or "Ad-hoc" if no .todo item}
**Upstream:** {src/Path/To/UpstreamFile.ts, or "N/A" for OXC-specific work}

{1-2 paragraph technical narrative. Key decisions, patterns, trade-offs. Note any divergences from upstream.}

### New files:

| File                                                     | Description   |
| -------------------------------------------------------- | ------------- |
| `crates/oxc_react_compiler/src/path/to/file.rs`         | Brief purpose |

### Modified files:

| File                                                     | Change       |
| -------------------------------------------------------- | ------------ |
| `crates/oxc_react_compiler/src/path/to/file.rs`         | What changed |
```

## Rules

1. **Phase numbers are sequential** — increment from the latest entry
2. **Date format** — YYYY-MM-DD
3. **Task links to `.todo/`** when applicable
4. **Upstream references** — note the corresponding TypeScript file(s) from babel-plugin-react-compiler
5. **Narrative is technical** — what was built, key decisions, patterns, divergences from upstream. No fluff.
6. **File tables are exhaustive** — every new and modified file
7. **Omit empty sections** — skip "New files" if none exist, same for "Modified files"
8. **Split at ~50 entries** — create new numbered file, update index
9. **Reverse-chronological** — newest entries at top of file
10. **Separate with `---`** — horizontal rule between entries

## Index Format

`.journal/index.md`:

```markdown
# Implementation Journal

> Chronological log of implementation sessions. Each file covers ~50 entries before splitting.

| File             | Entries | Phases | Notes                                            |
| ---------------- | ------- | ------ | ------------------------------------------------ |
| [001.md](001.md) | N       | X–Y    | Brief summary of what this file covers           |
```

## Workflow

### Recording work

1. Run `git diff --stat HEAD~1` and `git log --oneline -5` to see changes
2. Read `.journal/index.md` to find latest file and phase number
3. Read the latest `.journal/*.md` to confirm current phase
4. Write new entry at the top of the latest file (after the header)
5. Update index if entry count changed or new file created

### Splitting files

When a file reaches ~50 entries:

1. Create next numbered file with header `# Implementation Journal — Part N`
2. Add to `.journal/index.md` with phase range
3. Continue in the new file
