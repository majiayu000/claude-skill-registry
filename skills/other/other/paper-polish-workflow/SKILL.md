---
name: paper-polish-workflow
description: Systematic top-down workflow for polishing academic papers. Structure to logic to expression with user confirmation at each step.
---

## Purpose

This Skill provides a systematic, top-down workflow for polishing academic papers. It works from structure to logic to expression, with user confirmation at each decision point. Expression options are drawn from reference-driven academic patterns rather than ad hoc rewrites, ensuring professional and consistent output suitable for journal submission.

## Trigger

**Activates when the user asks to:**
- Polish, revise, or improve an academic paper section by section
- 润色、精修、逐步改进学术论文

**Example invocations:**
- "Polish my paper section by section" / "润色论文"
- "Help me revise my introduction step by step" / "精修论文"
- "Guide me through polishing this draft" / "帮我逐步润色这篇论文"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `interactive` | Yes | Full 4-step flow with user confirmation at each decision point |
| `guided` | | Multi-pass with confirmation at key checkpoints only |
| `direct` | | Single-pass polish using defaults; skip AskUserQuestion |
| `batch` | | Same operation applied across multiple sections sequentially |

**Default mode:** `interactive`

**Mode inference:** "quickly" or "just fix" switches to `direct`. "step by step" or "逐步" confirms `interactive` (already default).

## References

### Required (always loaded)

| File | Purpose |
|------|---------|
| `references/expression-patterns.md` | Academic expression patterns overview and module index |

### Leaf Hints (loaded when needed)

| File | When to Load |
|------|--------------|
| `references/expression-patterns/introduction-and-gap.md` | Polishing introduction or background content |
| `references/expression-patterns/methods-and-data.md` | Polishing methods, data, or study area content |
| `references/expression-patterns/results-and-discussion.md` | Polishing results or discussion content |
| `references/expression-patterns/conclusions-and-claims.md` | Polishing conclusion content |
| `references/expression-patterns/geography-domain.md` | Content involves spatial, urban, or planning topics |
| `references/anti-ai-patterns.md` | Polishing expression (Step 3) -- screen for AI-sounding phrases |
| `references/journals/ceus.md` | Target journal is CEUS |

### Loading Rules

- Load expression patterns overview at start; select the appropriate leaf based on section type.
- Load anti-AI patterns when polishing expression (Step 3).
- Load journal template when target journal is specified.
- Load `geography-domain.md` when spatial, urban, or planning content is detected.
- If a reference file is missing, warn the user and proceed with reduced capability.

## Ask Strategy

**Before starting, ask about:**
1. Target journal (if not already known)
2. Which section to work on
3. Preferred mode (if ambiguous from trigger)

**Rules:**
- Never ask more than 3 questions before producing initial output.
- In `direct` mode, skip pre-questions if the user provided enough context.
- In `batch` mode, skip per-item questions; apply settings from the first item.
- Use Structured Interaction when available; fall back to plain-text questions otherwise.
- See `skill-conventions.md > AskUserQuestion Enforcement` for full rules.

## Workflow

### Step 1: Collect Context

- Determine input type (file path or pasted text).
- Load required references (expression-patterns overview).
- Identify target journal; load journal template if specified.
- Read input content using the Read tool; extract key numbers, claims, and data points.
- Locate example/reference papers if the user provides them (use Read tool for PDFs).
- In `interactive` or `guided` mode: confirm scope with the user before proceeding.

### Step 2: Structure & Logic Confirmation

- Analyze section macro structure (e.g., Abstract = Background + Gap + Method + Results + Contribution).
- Present a structure table for user confirmation.
- Break content into sentences; assign a logic function to each.
- Present the logic chain for user confirmation.
- Checkpoint: user confirms structure and logic before expression work begins.
- In `direct` mode: run structure and logic analysis internally, proceed to Step 3 automatically.

### Step 3: Expression Polish & Consistency

- Load the section-appropriate expression pattern leaf and anti-AI patterns.
- For each sentence with expression issues, present 2-3 options via AskUserQuestion (`interactive` mode) or apply the best option automatically (`direct` mode).

```
AskUserQuestion({
  question: "Which expression do you prefer for [sentence function]?",
  options: [
    { label: "[Expression A]", description: "[full sentence with expression A]" },
    { label: "[Expression B]", description: "[full sentence with expression B]" },
    { label: "[Expression C]", description: "[full sentence with expression C]" }
  ]
})
```

- **Reference paper consultation:** when the user questions professionalism, use the Read tool to load example papers and extract expression patterns.
- **Journal style check:** apply journal-specific requirements from the loaded template.
- **Repetition and coherence pass:** check for repeated expressions and missing transitions; suggest fixes.
- **Cross-section consistency:** verify numbers, terminology, and claims across sections.

### Step 4: Output

- Generate highlights if the journal requires them (for CEUS, see `references/journals/ceus.md`).
- Suggest a read-aloud final check to catch awkward phrasing.
- Compile all confirmed content into the final version.
- Present the final version with word count for user confirmation.
- Write to `*_polished.md` after confirmation (or automatically in `batch` mode).
- Report word count and any journal constraint notes.

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `polished_text` | Markdown file (`*_polished.md`) or conversation output | Always produced |
| `change_summary` | Markdown in session | Always produced |
| Word count | Integer | Always reported |
| Journal compliance notes | Bullet list | When a target journal is specified |

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Unprofessional word flagged | Present 2-3 alternatives via AskUserQuestion; accept if user insists |
| Section too long for single pass | Split into paragraph-level sub-passes; maintain cross-paragraph coherence |
| No journal specified | Default to general academic style; note in output |
| Mixed language input | Detect dominant language; ask user to confirm target language |
| Reference paper provided as PDF | Use Read tool to load PDF; extract style patterns for expression matching |
| Abrupt sentence transition | Provide transition options via AskUserQuestion |
| Repetition detected between sections | Identify repeated content; suggest which occurrence to rephrase |
| Logic structure needs modification | Return to Step 2 to re-confirm structure before continuing |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask 1-3 plain-text questions covering highest-impact gaps; do not block workflow |
| Reference file missing | Log the missing file, proceed with reduced capability, warn the user |
| Target journal not specified | Ask once; if declined, use general academic style |
| PDF reference paper unreadable | Ask user to paste relevant excerpts instead |

---

*Skill: paper-polish-workflow*
*Conventions: references/skill-conventions.md*
