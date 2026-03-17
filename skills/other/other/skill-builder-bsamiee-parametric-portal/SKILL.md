---
name: skill-builder
type: standard
depth: full
description: >-
    Creates and refines Claude Code skills via structured workflows with YAML frontmatter, typed folders, and depth-gated LOC limits. Use when authoring SKILL.md files, organizing references/, or validating skill structure.
---

# [H1][SKILL-BUILDER]
>**Dictum:** *Structured authoring produces discoverable, maintainable skills.*

<br>

Create and refine Claude Code skills via structured workflows.

**Tasks:**
1. Collect parameters — Scope: `create | refine`, Type: `simple | standard | complex`, Depth: `base | extended | full`
2. Read [frontmatter.md](./references/frontmatter.md) — Discovery metadata, trigger patterns
3. Read [structure.md](./references/structure.md) — Folder layout gated by Type
4. Read [depth.md](./references/depth.md) — LOC limits, nesting gated by Depth
5. (complex) Read [scripting.md](./references/scripting.md) — Automation standards
6. Capture requirements — purpose, triggers, outputs
7. Invoke `skill-summarizer` with skill `style-standards` — Extract voice, formatting, taxonomy
8. Invoke `deep-research` — Domain research for skill topic
9. Plan with 3 agents — file inventory, section structure, content framework
10. Execute per Scope:
    - (create) Author new artifacts; select template:
      - [simple](./templates/simple.skill.template.md) - DEFAULT
      - [standard](./templates/standard.skill.template.md)
      - [complex](./templates/complex.skill.template.md)
    - (refine) Compare input to existing frontmatter; see [refine.md](./references/workflows/refine.md):
      - Input = existing → optimize (density, fixes, quality)
      - Input > existing → upgrade (expand structure or depth)
      - Input < existing → downsize (combine, refactor, remove low-relevance)
11. Validate — Quality gate, LOC compliance, structure match

**Dependencies:**
- `deep-research` — Domain research via parallel agents
- `skill-summarizer` — Voice and formatting extraction (with skill `style-standards`)
- `report.md` — Sub-agent output format

[REFERENCE]: [index.md](./index.md) — Complete file listing

---
## [1][FRONTMATTER]
>**Dictum:** *Metadata enables discovery before loading.*

<br>

Frontmatter indexed at session start (~100 tokens). Description is ONLY field parsed for relevance—quality determines invocation accuracy.

**Guidance:**
- `Discovery` — LLM reasoning matches description to user intent. No embeddings, no keyword matching.
- `Trigger Density` — Include file types, operations, "Use when" clauses. Every word aids matching.
- `Voice` — Third person, active, present tense. Prohibit: 'could', 'might', 'probably', 'should'.

**Best-Practices:**
- **Length** — 1-2 sentences. Concise triggers outperform verbose explanations.
- **Classification** — Include `type` and `depth` fields for refine workflow detection.
- **Invocation Control** — `disable-model-invocation: true` for user-only; `user-invocable: false` for Claude-only.

---
## [2][STRUCTURE]
>**Dictum:** *Type determines breadth—folder existence defines capability scope.*

<br>

Type gates folder creation. Structure defines WHAT exists; Depth constrains HOW MUCH content.

| [INDEX] | [TYPE]   | [FOLDERS]                          |
| :-----: | -------- | ---------------------------------- |
|   [1]   | Simple   | SKILL.md only                      |
|   [2]   | Standard | +index.md, references/, templates/ |
|   [3]   | Complex  | +scripts/                          |

**Guidance:**
- `Naming` — Skill folder matches frontmatter `name` exactly. Kebab-case throughout.
- `Index` — Standard/Complex require index.md at root listing all reference files.
- `Upgrade Path` — Start with simplest type satisfying requirements.

**Best-Practices:**
- **Directory Purpose** — references/ for domain knowledge, templates/ for output scaffolds, scripts/ for automation.
- **File Limit** — Max 7 files in references/ (including nested).

---
## [3][DEPTH]
>**Dictum:** *Depth determines comprehensiveness—hard caps prevent bloat.*

<br>

Depth enforces LOC limits and nesting rights. Each level adds +50 SKILL.md, +25 reference files (cumulative).

| [INDEX] | [DEPTH]  | [SKILL.MD] | [REF_FILE] | [NESTING]      |
| :-----: | -------- | :--------: | :--------: | -------------- |
|   [1]   | Base     |    <300    |    <150    | Flat only      |
|   [2]   | Extended |    <350    |    <175    | 1 subfolder    |
|   [3]   | Full     |    <400    |    <200    | 1-3 subfolders |

**Guidance:**
- `Nesting Gate` — Subfolder requires 3+ related files OR distinct domain concern.
- `Content Scaling` — Base: 1-2 items per Guidance/Best-Practices. Extended: 2-4. Full: comprehensive.
- `LOC Optimization` — Density over deletion; see [depth.md§LOC_OPTIMIZATION](./references/depth.md).
- `Content Separation` — SKILL.md = WHY, references = HOW; see [depth.md§CONTENT_SEPARATION](./references/depth.md).

**Best-Practices:**
- **Hard Caps** — Exceeding limits requires refactoring, not justification.
- **No Brute-Force** — Consolidate → restructure → densify → prune (in order).

---
## [4][SCRIPTING]
>**Dictum:** *Deterministic automation extends LLM capabilities.*

<br>

Complex type enables scripts/ folder for external tool orchestration, artifact generation, validation.

**Guidance:**
- `Justification` — Script overhead demands explicit need: tool wrapping, exact reproducibility, schema enforcement.
- `Depth Scaling` — Base/Extended: single script. Full: multiple when distinct concerns justify.

**Best-Practices:**
- **Type Selection** — Standard suffices for most skills. Complex only when automation is core purpose.
- **Augmentation** — Scripts support workflows; core logic remains in SKILL.md and references.

---
## [5][TEMPLATES]
>**Dictum:** *Templates enforce canonical structure.*

<br>

Templates define output scaffolds. Agent combines user input with template skeleton for consistent artifacts.

**Guidance:**
- `Purpose` — Follow template exactly. No improvisation.
- `Composition` — Input data + template skeleton = generated artifact.

**Best-Practices:**
- **Placeholder Syntax** — Use `${variable-name}` for insertion points.
- **Structure Match** — Template complexity matches depth selection.

---
## [6][VALIDATION]
>**Dictum:** *Gates prevent incomplete artifacts.*

<br>

[VERIFY] Completion:
- [ ] Parameters: Scope, Type, Depth collected and applied.
- [ ] Research: `deep-research` completed fully before authoring.
- [ ] Style: `skill-summarizer` constraints applied to output.
- [ ] Workflow: Executed per Scope (create | refine).
- [ ] Quality: LOC within limits, content separation enforced.

[REFERENCE] Operational checklist: [→validation.md](./references/validation.md)
