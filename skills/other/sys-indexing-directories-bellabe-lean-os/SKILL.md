---
name: sys-indexing-directories
description: Generates index.md files listing .md documentation. Pure navigation — what exists and where. No code files. Triggers on "index", "catalog", "build index".
license: Complete terms in LICENSE.txt
allowed-tools: Read Grep Glob
---

# Directory Indexer

Generate or update index.md files — yellow pages for directories.

## Principles

1. **List what exists** — Names and links only
2. **No judgment** — No status, flags, or inference
3. **Hierarchical nav** — ↑ parent · → related
4. **Docs only** — No code files (separate code-mapper skill)
5. **Skip terminal directories** — No index.md in directories with no subdirectories

## Excludes

Directories: `node_modules`, `.git`, `.venv`, `__pycache__`, `src`, `lib`, `dist`, `build`, `vendor`

Files: `*.py`, `*.js`, `*.ts`, `*.jsx`, `*.tsx`, `*.go`, `*.rs`, `*.java`, `*.rb`, `*.php`, `*.c`, `*.cpp`, `*.h`, `*.css`, `*.scss`, `*.json`, `*.yaml`, `*.yml`, `*.toml`, `*.lock`, `*.sum`

## Directory Types

| Pattern | Subdirs |
|---------|---------|
| `artifacts/` | sales, marketing, engineering, operations, etc |
| `docs/` | references, workflows, etc |
| `meeting-notes/` | as found |
| `research/` | customer, market, etc |
| `strategy/` | canvas, goals, financial, etc |
| `threads/` | {domain}/{type}/{thread}/ — see Threads Structure |
| any other | as found |

## Threads Structure

```
threads/
├── index.md
├── marketing/
│   ├── index.md
│   └── {thread_name}/
│       ├── 1-input.md        ← source for index entry (frontmatter)
│       ├── 2-hypothesis.md
│       ├── 3-implication.md
│       ├── 4-decision.md
│       ├── 5-actions.md
│       └── 6-learning.md    ← NO index.md here
├── sales/
├── engineering/
└── operations/
```

**Rules:**
1. **Stop at 1-input.md** — If directory contains `1-input.md`, it's a thread leaf. Do NOT create index inside.
2. **Read 1-input.md** — Extract `thread_id` from frontmatter and first heading for parent index entry.
3. **Index at domain level** — `marketing/index.md` lists all threads under it.

**1-input.md frontmatter (source for index):**
```yaml
---
thread_id: marketing_content-authority_2026q1
goal_id: distribution-q1/1.content-authority
created: 2026-02-01
owner: mkt-content-manager
status: active
---
# Content Authority Execution
```

**Generated index (e.g., `marketing/index.md`):**
```markdown
# Marketing

- [content-authority_2026q1](./content-authority_2026q1/) — Content Authority Execution

↑ [Threads](../)
```

## Process

### 1. Scan
```bash
find {root} -type f -name "*.md" \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/src/*" \
  ! -path "*/lib/*" \
  ! -path "*/dist/*" \
  ! -path "*/build/*" \
  ! -path "*/vendor/*"
```

### 2. Check for Terminal Directory
```
# Terminal = has NO subdirectories (only files)
# Do NOT create index.md in terminal directories
# Instead, parent index lists their contents under ## heading

if directory has subdirectories:
  → CREATE index.md (lists files + subdirs)
else:
  → SKIP index.md — parent will bubble up contents
```

### 3. Check for Thread Leaf
```bash
# If 1-input.md exists, this is a thread — do NOT index inside
if [ -f "{dir}/1-input.md" ]; then
  # Skip — parent will index this via 1-input.md frontmatter
  exit
fi
```

### 4. List
For .md files: `- [{name}](./{name}.md) — {snapshot}`
For non-terminal dirs: `- [{name}](./{name}/) — {snapshot}`
For terminal dirs: bubble up contents under `## {dir_name}` heading:
```markdown
## {dir_name}
- [{file}](./{dir_name}/{file}.md) — {snapshot}
```
For threads (has 1-input.md): read `thread_id` and first heading from 1-input.md

Description: first heading or first line — max 40 chars, truncate with `…`

### 5. Link Navigation
- `↑ [Parent](../)`
- `→ [Related](../related/)`

### 6. Recurse
For subdirs with content → generate index → link ↑↓
**Skip when:**
- Directory contains `1-input.md` (thread leaf)
- Directory has no subdirectories (terminal — contents bubbled up to parent)

## Output Format

```markdown
# {Directory Name}

- [{item}](./{item}/) — {snapshot}
- [{item}](./{item}.md) — {snapshot}

↑ [Parent](../)
```

## Examples

**Artifacts:**
```markdown
# Artifacts

## sales
- [q4-deck](./sales/q4-deck/) — Q4 investor pitch materials
- [prospects](./sales/prospects/) — Enterprise lead tracking

## engineering
- [auth-service](./engineering/auth-service/) — OAuth2 implementation

→ [Strategy](../strategy/) · [Threads](../threads/)
```

**Threads (domain level):**
```markdown
# Marketing

- [campaigns](./campaigns/) — Product launch campaigns
- [content](./content/) — Blog and social content

↑ [Threads](../)
```

**Threads (domain level — reads from 1-input.md):**
```markdown
# Marketing

- [content-authority_2026q1](./content-authority_2026q1/) — Content Authority Execution
- [github-organic_2026q1](./github-organic_2026q1/) — GitHub Organic Growth Execution

↑ [Threads](../)
```

**Strategy (canvas is terminal — files bubble up):**
```markdown
# Strategy

- [Goals](./goals/) — OKRs and milestones

## Canvas
- [00.mode](./canvas/00.mode.md) — Business Model Mode
- [01.context](./canvas/01.context.md) — Strategic Context (KBOS)

→ [Artifacts](../artifacts/)
```

## Boundaries

**Does:** List .md files, read 1-input.md for threads, generate links, build navigation

**Does NOT:**
- Index code files
- Create index inside thread dirs (with 1-input.md)
- Create index in terminal directories (no subdirs)
- Infer status or add judgment

## Error Handling

| Situation | Action |
|-----------|--------|
| Directory empty | Skip, no index needed |
| No .md files found | Create index listing subdirs only |
| 1-input.md malformed | Use directory name as fallback, warn |
| Circular symlinks | Skip symlinked directories |
| Permission denied | Skip directory, log warning |
| Existing index.md | Overwrite with fresh generation |

## References

- `references/patterns.md` — Detection patterns for directory types and navigation
- `references/templates.md` — Index.md templates per directory type