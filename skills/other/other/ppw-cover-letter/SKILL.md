---
name: ppw:cover-letter
description: >-
  Generate submission-ready cover letters from paper content and target journal requirements.
  Includes contribution statement, data availability, conflict of interest, and contact block.
  生成投稿信，包含贡献声明、数据可用性、利益冲突声明和联系方式。
triggers:
  primary_intent: generate submission cover letter for academic paper
  examples:
    - "Write a cover letter for my CEUS submission"
    - "帮我写投稿信"
    - "Generate a cover letter for my paper"
    - "写一封投稿到CEUS的cover letter"
    - "Help me draft a submission cover letter"
    - "帮我生成这篇论文的投稿信"
tools:
  - Read
  - Write
  - Structured Interaction
references:
  required:
    - references/journals/ceus.md
  leaf_hints: []
input_modes:
  - file
  - pasted_text
output_contract:
  - cover_letter_md
---

## Purpose

This Skill generates complete, submission-ready academic cover letters by loading the target journal's template to align the contribution statement with journal scope and aims, collecting correspondence author details via Ask Strategy, and reading the paper (file or pasted text) to extract the paper title, key contribution, and data availability information. Output is a full letter with all four required content blocks: (1) contribution statement — explicitly aligned with the journal's stated scope from the loaded template; (2) data/code availability statement; (3) conflict of interest declaration; (4) correspondence author contact block. If the journal template is not found, the Skill refuses immediately — it never falls back to generic academic prose, consistent with the journal-aware pattern used throughout this project.

## Trigger

**Activates when the user asks to:**
- Write, generate, or draft a cover letter or submission letter for a paper
- 写投稿信、生成cover letter、帮我写投稿信

**Example invocations:**
- "Write a cover letter for my CEUS submission"
- "帮我写投稿信"
- "Generate a cover letter for my paper"
- "写一封投稿到CEUS的cover letter"
- "Help me draft a submission cover letter"
- "帮我生成这篇论文的投稿信"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `direct` | Yes | Single-pass letter generation; all context collected upfront via Ask Strategy |
| `batch` | | NOT supported — each letter requires specific paper context and author details |

**Default mode:** `direct`. User provides a paper and journal; Skill collects any missing details and generates the complete letter in one pass.

## References

### Required (always loaded)

None.

### Leaf Hints (loaded conditionally)

| File | When to Load |
|------|--------------|
| `references/journals/ceus.md` | When user targets CEUS; provides Aims & Scope, scope keywords for contribution alignment |

### Loading Rules

- When journal is specified, load `references/journals/[journal].md`.
- If template not found: **refuse immediately** with: "Journal template for [X] not found. Available: CEUS."
- Do NOT proceed with generic framing if template is missing.
- Extract the Aims & Scope section from the loaded template — the contribution statement must reference it directly.

## Ask Strategy

The Skill needs four inputs. If already provided in trigger or paper content, skip the corresponding question.

1. **Target journal** — required; determines which template to load. Ask if not specified.
2. **Paper file or text** — required; for extracting paper title and key contribution. Ask for file path or paste if not provided.
3. **Correspondence author details** (name, email, institution) — required; ask as a single grouped question if not provided.
4. **Data/code availability** — optional; are datasets or code publicly available? If yes, ask for repository URLs. Default to "Data are not publicly available" if user declines or does not know.

**Rules:**
- Ask at most 3 questions before proceeding.
- Use Structured Interaction when available; fall back to plain-text questions otherwise.
- If correspondence details not provided and user declines: use `[Corresponding Author Name]`, `[Email]`, `[Institution]` placeholders.

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Step 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:cover-letter` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:cover-letter？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Step 1: Collect Context

- Run Ask Strategy for any missing inputs (journal, paper, author details, data availability).
- Load `references/journals/[journal].md`. If not found: **refuse** with "Journal template for [X] not found. Available: CEUS." Do NOT proceed.
- If paper provided as file: use Read tool to load it; extract title and key contribution.
- If paper provided as pasted text: extract title and key contribution from the pasted content.
- Extract Aims & Scope section from the loaded journal template (contribution statement references this directly).
- **Record workflow:** Append `{"skill": "ppw:cover-letter", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

### Step 2: Draft Letter

Use the following locked letter format:

```
[Date]

The Editor-in-Chief
[Editor Name]
[Journal Name]

Dear [Editor Name],

We submit our manuscript entitled "[Paper Title]" for consideration in [Journal Name].

**Contribution Statement**
[1–2 sentences explicitly referencing journal's stated scope from loaded template]

**Data and Code Availability**
[Repository URLs, or "Data are not publicly available due to [reason]."]

**Conflict of Interest**
The authors declare no conflict of interest.

**Corresponding Author**
[Name]
[Email]
[Institution]

Sincerely,
[Authors]
```

**Contribution statement rule:** Write 1–2 sentences that explicitly reference the journal's stated scope and aims from the loaded template. Use journal-specific framing: "This paper addresses [X], which aligns directly with [Journal]'s focus on [scope phrase from template]." Do NOT use generic framing ("this paper advances the field of...").

**Data/code block:** List repository URLs if provided; otherwise state "Data are not publicly available due to [reason if given, otherwise omit reason clause]."

**Conflict of interest:** Always use the standard declaration "The authors declare no conflict of interest."

**Contact block:** Use provided author details or bracketed placeholders if not provided.

### Step 3: Output

- **File input:** Write to `{input_filename_without_ext}_cover_letter.md` using the Write tool.
- **Pasted text input:** Display the complete letter in conversation.
- Confirm output location to user.

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `cover_letter_md` | Markdown file at `{input_filename_without_ext}_cover_letter.md` | File input |
| `cover_letter_text` | Complete letter in conversation | Pasted text input or Write tool failure |

**Required content blocks (all four mandatory in every letter):**

```
**Contribution Statement**    ← references journal scope explicitly
**Data and Code Availability** ← links or "not publicly available"
**Conflict of Interest**       ← standard declaration
**Corresponding Author**       ← name, email, institution
```

Note: Contribution statement must reference journal scope explicitly — not generic academic praise.

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Journal template not found | Refuse: "Journal template for [X] not found. Available: CEUS." Do not generate with generic framing. |
| Paper file not found or unreadable | Ask user to paste paper text or abstract instead |
| Correspondence details not provided; user declines | Use `[Corresponding Author Name]`, `[Email]`, `[Institution]` placeholders; note user must fill before submission |
| Data availability unknown | Use "Data availability will be confirmed at revision stage." |
| Multiple authors listed for correspondence | Ask which one is the corresponding author; include only one in the contact block |
| Aims & Scope section thin in template | Use all available scope language from template; note contribution alignment may be approximate |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask journal name and author details as sequential plain-text questions |
| Read tool fails on paper file | Ask user to paste abstract or key contribution sentences |
| Write tool fails | Display complete letter in conversation; advise user to copy to a `.md` file |
| `references/journals/ceus.md` missing | Refuse with journal-missing message; do not generate without template |

## Examples

**Invocation:** "Write a cover letter for my CEUS submission" (with file `my_paper.tex`)

1. Skill loads `references/journals/ceus.md` — extracts Aims & Scope.
2. Skill reads `my_paper.tex` — extracts title and key contribution.
3. Skill asks: "Please provide your name, email, and institution for the correspondence block."
4. Skill asks: "Are your data or code publicly available? If yes, please share the repository URL(s)."
5. Skill generates letter and writes to `my_paper_cover_letter.md`.

**First 8 lines of output:**

```
March 2026

The Editor-in-Chief
[Editor Name]
Computers, Environment and Urban Systems

Dear [Editor Name],

We submit our manuscript entitled "Spatiotemporal Analysis of Urban Heat Islands Using Remote
Sensing" for consideration in Computers, Environment and Urban Systems.

**Contribution Statement**
This paper addresses urban heat island detection and mitigation across metropolitan areas, which
aligns directly with CEUS's focus on computational approaches to understanding urban systems and
the built environment.
```

---

*Skill: cover-letter-skill*
*Conventions: references/skill-conventions.md*
