---
description: Load skill knowledge via skill-summarizer agent
argument-hint: [skill-name] [section?]
allowed-tools: Task
---

# [H1][LEARN-SKILL]
>**Dictum:** *Delegated synthesis preserves tokens while conveying complete knowledge.*

<br>

Delegate to `skill-summarizer` agent. Receive structured skill knowledge.

**Parameters:**
- `$1` — Skill name (required). Fuzzy match to `.claude/skills/{name}/`.
- `$2` — Section (optional). Target specific folder or H2 section.

---
## [1][DELEGATE]
>**Dictum:** *Agent reads exhaustively or targeted per request.*

<br>

Spawn `skill-summarizer` agent via Task tool.

**No section specified:** Read ALL files in `.claude/skills/$1/`, produce complete synthesis.

**Section specified:** Read only the targeted part:
- `references` — Read `references/*.md` files only
- `scripts` — Read `scripts/*.py`(or .ts) files only
- `templates` — Read `templates/**/*.md` files only
- `{H2-label}` — Extract specific section from SKILL.md (e.g., `validation`, `frontmatter`)

[CRITICAL]:
- [NEVER] Read skill files directly — delegate to agent.

---
## [2][RECEIVE]
>**Dictum:** *Dynamic output reflects skill structure.*

<br>

Agent returns sections based on request:
- **Full read:** `[SKILL]`, `[REFERENCES]`, `[{FOLDER}]`, `[SOURCES]`
- **Targeted read:** `[{TARGET}]`, `[SOURCES]`

---
## [3][PROCEED]
>**Dictum:** *Loaded context enables task execution.*

<br>

Confirm skill knowledge received. Continue with user task.