---
name: ppw:abstract
description: >-
  Generate or optimize academic paper abstracts using the 5-sentence Farquhar formula.
  Supports generate-from-scratch and restructure-existing paths. Produces labeled output
  for formula verification plus a clean version for clipboard use.
  摘要生成与优化，支持从原始材料生成或改写现有摘要。
triggers:
  primary_intent: generate or optimize academic paper abstract
  examples:
    - "Write an abstract for my paper"
    - "帮我写摘要"
    - "Optimize my existing abstract"
    - "改写我的摘要，符合五句话公式"
    - "Generate a submission-ready abstract for CEUS"
    - "帮我生成一个投稿摘要"
    - "Restructure my abstract using the Farquhar formula"
    - "优化摘要让它更符合学术规范"
tools:
  - Read
  - Write
  - Structured Interaction
references:
  required:
    - references/expression-patterns.md
    - references/bilingual-output.md
  leaf_hints:
    - references/expression-patterns/introduction-and-gap.md
    - references/expression-patterns/results-and-discussion.md
    - references/expression-patterns/conclusions-and-claims.md
    - references/expression-patterns/methods-and-data.md
input_modes:
  - file
  - pasted_text
output_contract:
  - labeled_abstract
  - clean_abstract
  - bilingual_abstract
---

## Purpose

This Skill generates or optimizes academic paper abstracts using the locked 5-sentence Farquhar formula: [1: Contribution], [2: Difficulty], [3: Method], [4: Evidence], [5: Key Result]. It operates on two mutually exclusive paths — generate a new abstract from raw materials (paper sections, bullet points, or a brief description), or restructure an existing abstract to comply with the formula. Both paths produce labeled output first so users can verify formula compliance sentence by sentence, followed by a clean plain-paragraph version ready for clipboard use. When a target journal is specified, journal-specific style conventions are applied.

## Trigger

**Activates when the user asks to:**
- Write, generate, or create an abstract from paper content
- Optimize, restructure, or rewrite an existing abstract
- 写摘要、生成摘要、改写摘要、优化摘要

**Example invocations:**
- "Write an abstract for my paper" / "帮我写摘要"
- "Optimize my existing abstract" / "改写我的摘要"
- "Restructure this abstract using the 5-sentence formula"
- "Generate a CEUS-ready abstract from my introduction and results"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `direct` | Yes | Single-pass abstract output using the 5-sentence formula |
| `batch` | | Not supported — abstract requires full paper context |

**Default mode:** `direct`. User provides content and receives labeled + clean abstract in one pass.

**Path selection (within direct mode):**
- Input reads like a formed abstract → restructure path
- Input is raw content (sections, bullets, "my paper is about...") → generate path
- Ambiguous → ask before proceeding

## References

### Required (always loaded)

| File | Purpose |
|------|---------|
| `references/expression-patterns.md` | Academic expression patterns overview |

### Leaf Hints (loaded when needed)

| File | When to Load |
|------|--------------|
| `references/expression-patterns/introduction-and-gap.md` | Contribution and gap framing (sentences 1-2) |
| `references/expression-patterns/conclusions-and-claims.md` | Calibrated claim language (sentences 1 and 5) |
| `references/expression-patterns/methods-and-data.md` | Method description (sentence 3, when weak) |
| `references/expression-patterns/results-and-discussion.md` | Evidence and result framing (sentences 4-5) |

### Journal Template (conditional)

- When user specifies a target journal, load `references/journals/[journal].md`.
- If template missing, **refuse**: "Journal template for [X] not found. Available: CEUS."
- If no journal specified, ask once; if declined, apply general academic style.

## Ask Strategy

**Before starting, ask about:**
1. Path: does the user have an existing abstract to restructure, or raw content to generate from? (skip if clear from input)
2. Target journal if not specified (ask once; if declined, use general academic style)
3. Word limit if known (typically 150-300 words; ask once)

**Path inference:**
- User pastes text that reads like an abstract → restructure path
- User provides sections, bullets, or "my paper is about..." → generate path
- Ambiguous → ask: "Do you have an existing abstract to restructure, or shall I generate one from your materials?"

**Rules:**
- Never ask more than 2 questions before starting.
- Skip path question if inference is clear from input.
- In `direct` mode with sufficient context, proceed without pre-questions.

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Step 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:abstract` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:abstract？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Step 1: Collect Context

- Load `references/expression-patterns.md` overview.
- If journal specified, load `references/journals/[journal].md`. If missing, refuse with: "Journal template for [X] not found. Available: CEUS."
- Read user input: file via Read tool, or pasted text from conversation.
- Determine path: restructure if input reads like a formed abstract; generate if raw materials. Ask if ambiguous.
- **Opt-out check:** Scan the user's trigger prompt for any of these phrases (case-insensitive, exact phrase match): `english only`, `no bilingual`, `only english`, `不要中文`. Store result as `bilingual_mode` (true/false). This flag governs Step 3 output below.
- **Record workflow:** Append `{"skill": "ppw:abstract", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

### Step 2a: Generate Path (raw content provided)

- Load `references/expression-patterns/introduction-and-gap.md` for contribution and gap framing.
- Load `references/expression-patterns/conclusions-and-claims.md` for calibrated claim language.
- Load `references/expression-patterns/methods-and-data.md` if the user's method description is weak.
- Synthesize sentence 1 (contribution): start with "We introduce / propose / demonstrate / show..."
- Synthesize sentence 2 (difficulty): why this problem is hard or why it matters.
- Synthesize sentence 3 (method): how the problem is solved, with key technical terminology.
- Load `references/expression-patterns/results-and-discussion.md` for sentences 4-5.
- Synthesize sentence 4 (evidence): what was measured, on what benchmark or dataset.
- Synthesize sentence 5 (key result): the most important number or qualitative outcome.

### Step 2b: Restructure Path (existing abstract provided)

- Load the same leaf hints as the generate path.
- Map each existing sentence to one of the 5 formula positions.
- Rewrite each sentence to tighten formula compliance while preserving the user's content.
- **Internal audit:** After restructuring, verify all 5 positions are filled.
- Flag any missing position with `[MISSING: position-name]` — never silently drop content.

### Step 3: Output

- Present the labeled version first (formula positions explicit, see Output Contract).
- Present the clean version (plain paragraph, no labels) separated by `---`.
- If the user wants to save: offer to write to a file using the Write tool.
- If word limit was specified, report word count; warn if over limit.
- **Bilingual display:** If `bilingual_mode` is true: after presenting the labeled version and after presenting the clean version, append a `> **[Chinese]** ...` blockquote for each sentence of the abstract. Use a header: "**双语对照 / Bilingual Comparison:**" before the blockquotes. Format:

  > **[Chinese]** [1: 贡献] ...
  > **[Chinese]** [2: 难度] ...
  > **[Chinese]** [3: 方法] ...
  > **[Chinese]** [4: 证据] ...
  > **[Chinese]** [5: 关键结果] ...

  Each blockquote corresponds to one Farquhar formula sentence. Label prefixes in Chinese are for readability only -- the clean version Chinese follows the plain paragraph structure without labels.
- If `bilingual_mode` is false (opt-out detected): skip bilingual display entirely.
- Optionally recommend the Polish Skill for further expression refinement.

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `labeled_abstract` | Labeled 5-sentence block with `[N: Position]` markers | Always |
| `clean_abstract` | Plain paragraph with no labels, separated by `---` | Always |
| Word count | Integer | When user specified a word limit |
| `bilingual_abstract` | `> **[Chinese]** ...` blockquotes in session (one per sentence) | When bilingual_mode is true (default). Skipped when opt-out detected. |

**Exact labeled format:**

```
[1: Contribution] We propose...
[2: Difficulty] Despite growing interest in X, existing approaches fail to...
[3: Method] We address this by...
[4: Evidence] Evaluated on N datasets...
[5: Key Result] Our approach achieves...

---
Clean version:
We propose... Despite growing interest in X, existing approaches fail to... We address this by... Evaluated on N datasets... Our approach achieves...
```

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Input is ambiguous (not clearly raw content or existing abstract) | Ask before proceeding: "Do you have an existing abstract to restructure, or shall I generate one?" |
| Existing abstract has fewer than 5 sentences | Run restructure path; flag missing positions with `[MISSING: ...]` |
| User specifies word limit | Count words in output; warn if over limit with exact count |
| Journal specified but template missing | Refuse: "Journal template for [X] not found. Available: CEUS." |
| Formula position cannot be filled from available content | Flag with `[MISSING: difficulty statement]`; do not invent content |
| User provides only a title or one-sentence summary | Ask for more content before proceeding |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask 1-2 plain-text questions (path + journal) |
| Expression pattern leaf missing | Proceed with general academic register; warn user |
| Journal template missing (no journal specified) | Ask once; if declined, use general academic style |
| Write tool fails | Present output in conversation instead |

## Examples

**Invocation:** "Help me restructure my abstract to follow the 5-sentence formula."

User pastes: "In this paper we study urban mobility patterns using GPS data. We find that mobility is highly predictable. We propose a model called MobNet. It outperforms existing approaches by 12% on the next-location prediction task."

**Output:**

```
[1: Contribution] We propose MobNet, a model for predicting urban mobility using GPS data.
[2: Difficulty] Despite the prevalence of GPS data, existing mobility models fail to capture [MISSING: difficulty statement — why prediction is hard or why existing approaches fall short].
[3: Method] MobNet addresses this by [MISSING: method description — how MobNet works].
[4: Evidence] Evaluated on a next-location prediction task using GPS traces from urban environments.
[5: Key Result] MobNet outperforms existing approaches by 12% on next-location prediction.

---
Clean version:
We propose MobNet, a model for predicting urban mobility using GPS data. [MISSING: difficulty statement]. MobNet addresses this by [MISSING: method description]. Evaluated on a next-location prediction task using GPS traces from urban environments. MobNet outperforms existing approaches by 12% on next-location prediction.
```

Two formula positions are flagged as missing. Please provide: (1) why mobility prediction is hard or what existing approaches fail to do, and (2) a brief description of how MobNet works.

---

*Skill: abstract-skill*
*Conventions: references/skill-conventions.md*
