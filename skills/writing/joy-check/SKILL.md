---
name: joy-check
description: "Validate content framing on joy-grievance spectrum."
user-invocable: false
argument-hint: "[--fix] [--strict] [--mode writing|instruction] <file>"
command: /joy-check
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - joy check
    - check framing
    - tone check
    - negative framing
    - joy validation
    - too negative
    - reframe positively
    - positive framing check
    - instruction framing
  pairs_with:
    - voice-writer
    - anti-ai-editor
    - voice-validator
    - skill-creator
  complexity: Simple
  category: content
---

# Joy Check

Validate content framing using mode-specific rubrics. Two modes:

- **writing** — Joy-grievance spectrum for human-facing content (blog posts, emails, articles). Evaluates whether content frames experiences through curiosity and generosity rather than grievance and accusation.
- **instruction** — Positive framing validation for LLM-facing content (agents, skills, pipelines). Evaluates whether instructions tell the reader what to do rather than what to avoid (ADR-127).

By default the skill evaluates each paragraph/instruction independently, produces a score (0-100), and suggests reframes without modifying content. Optional flags: `--fix` rewrites flagged items in place and re-verifies; `--strict` fails on any item below 60; `--mode writing|instruction` overrides auto-detection.

This skill checks *framing*, not *topic* and not *voice*. Voice fidelity belongs to voice-validator, AI pattern detection belongs to anti-ai-editor.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| scoring instruction files (agents, skills, pipelines): positive-framing rubric | `instruction-rubric.md` | Loads detailed guidance from `instruction-rubric.md`. |
| scoring human-facing prose (blog posts, emails, docs): joy-grievance rubric | `writing-rubric.md` | Loads detailed guidance from `writing-rubric.md`. |

## Instructions

### Phase 0: DETECT MODE

**Goal**: Determine which rubric to apply based on file location or explicit flag.

**Auto-detection rules** (in priority order):
1. Explicit `--mode writing|instruction` flag → use that mode
2. File in `agents/*.md` → **instruction**
3. File in `skills/*/SKILL.md` → **instruction**
4. File in `skills/workflow/references/*.md` → **instruction**
5. File is `CLAUDE.md` or `README.md` → **instruction**
6. Everything else → **writing**

**Load the rubric**: Read `references/{mode}-rubric.md` for the scoring criteria, patterns, and examples relevant to this mode.

**GATE**: Mode determined, rubric loaded. Proceed to Phase 1.

### Phase 1: PRE-FILTER

**Goal**: Use regex scanning as a fast gate to catch obvious patterns before spending LLM tokens on semantic analysis.

**For writing mode**: Run the regex-based scanner for grievance patterns:
```bash
python3 ~/.claude/scripts/scan-negative-framing.py [file]
```

**For instruction mode**: Run a grep scan for prohibition patterns:
```bash
grep -nE 'NEVER|do NOT|must NOT|FORBIDDEN' [file]
grep -nE "^-?\s*Don't|^-?\s*Avoid|^#+.*Anti-[Pp]attern|^#+.*Avoid" [file]
```

**Handle hits**: Report findings with suggested reframes from the loaded rubric. If `--fix` mode is active, apply reframes and re-run to confirm clean.

**GATE**: Regex/grep scan returns zero hits. Resolve obvious patterns before proceeding to Phase 2 — mechanical fixes come first.

### Phase 2: ANALYZE

**Goal**: Read the content and evaluate each item against the loaded rubric using LLM semantic understanding.

**Step 1: Read the content**

Read the full file. Skip frontmatter (YAML between `---` markers) and code blocks.

- **Writing mode**: Identify paragraph boundaries (blank-line separated blocks). Skip blockquotes.
- **Instruction mode**: Identify each instructional statement — bullet points, table cells, imperative sentences, section headings. Skip examples, code blocks, quoted user dialogue, and file path references.

**Step 2: Evaluate against the rubric**

Apply the scoring dimensions from the loaded rubric (`references/{mode}-rubric.md`). Each rubric defines its own PASS/FAIL dimensions, subtle patterns to detect, and contextual exceptions.

For **writing mode**: Evaluate through the joy-grievance lens. Watch for the subtle patterns described in `references/writing-rubric.md` (defensive disclaimers, accumulative grievance, passive-aggressive factuality, reluctant generosity).

For **instruction mode**: Evaluate through the positive-negative lens. Check each instruction against the patterns table in `references/instruction-rubric.md`. Apply contextual exceptions — subordinate negatives attached to positive instructions are PASS, as are negatives in code examples, writing samples, and technical terms.

**Step 3: Score each item**

Apply the scoring scale from the loaded rubric. For any item scoring in the lower tiers (CAUTION/GRIEVANCE for writing, NEGATIVE-LEANING/PROHIBITION-HEAVY for instruction), draft a specific reframe suggestion that preserves the substance while shifting the framing.

When an item seems subtle enough to question flagging — that is precisely when flagging matters most. Subtle patterns are what the regex/grep pre-filter misses, making them the primary purpose of this LLM analysis phase.

**GATE**: All items analyzed and scored. Reframe suggestions drafted for all flagged items. Proceed to Phase 3.

### Phase 3: REPORT

**Goal**: Produce a structured report with scores, findings, and reframe suggestions.

**Step 1: Calculate overall score**

Average all item scores. Pass criteria come from the loaded rubric:
- **Writing mode**: Score >= 60 AND no GRIEVANCE paragraphs
- **Instruction mode**: Score = 100 AND zero primary negative patterns in instructional context

**Step 2: Output the report**

```
JOY CHECK: [file]
Mode: [writing|instruction]
Score: [0-100]
Status: PASS / FAIL

Items:
  [writing mode]
  P1 (L10-12): JOY [85] -- explorer framing, curiosity
  P3 (L18-22): CAUTION [40] -- "confused" leans defensive
    -> Reframe: Focus on what you learned from the confusion

  [instruction mode]
  L33: NEGATIVE [20] -- "NEVER edit code directly"
    -> Rewrite: "Route all code modifications to domain agents"
  L45: PASS [90] -- "Create feature branches for all changes"
  L78: PASS [85] -- "Credentials stay in .env files, never in code" (subordinate negative OK)

Overall: [summary of framing arc]
```

**Step 3: Handle fix mode**

If `--fix` mode is active:
1. Rewrite flagged items using the drafted reframe suggestions
2. Preserve the substance — change only the framing
3. Re-run Phase 2 analysis on rewritten items to verify fixes landed
4. If fixes introduce new flagged items, iterate (maximum 3 attempts)

**GATE**: Report produced. If `--fix`, all rewrites applied and re-verified. Joy check complete.

---

### Integration

This skill integrates with content and toolkit pipelines:

**Writing pipeline** (human-facing content):
```
CONTENT --> voice-validator --> scan-ai-patterns --> joy-check --mode writing --> anti-ai-editor
```

**Instruction pipeline** (agent/skill/pipeline creation and modification):
```
SKILL.md --> joy-check --mode instruction --> fix flagged patterns --> re-verify
```

**Auto-invocation points**:
- `skill-creator` pipeline: Run `joy-check --mode instruction` after generating a new skill
- `agent-upgrade` pipeline: Run `joy-check --mode instruction` after modifying an agent
- `voice-writer`: Run `joy-check --mode writing` during validation
- `doc-pipeline`: Run `joy-check --mode instruction` for toolkit documentation

The joy-check can be invoked standalone via `/joy-check [file]` (auto-detects mode) or with explicit `--mode writing|instruction`.

---

## Error Handling

### Error: "File Not Found"
**Cause**: Path incorrect or file does not exist
**Solution**:
1. Verify path with `ls -la [path]`
2. Use glob pattern to search: `Glob **/*.md`
3. Confirm correct working directory

### Error: "Regex Scanner Fails or Not Found"
**Cause**: `scan-negative-framing.py` script missing or Python error
**Solution**:
1. Verify script exists: `ls scripts/scan-negative-framing.py`
2. Check Python version: `python3 --version` (requires 3.10+)
3. If script unavailable, skip Phase 1 and proceed directly to Phase 2 LLM analysis -- the regex pre-filter is an optimization, not a requirement

### Error: "All Paragraphs Score GRIEVANCE"
**Cause**: Content is fundamentally framed through grievance -- not recoverable with paragraph-level reframes
**Solution**:
1. Report the scores honestly
2. Suggest the content needs a full rewrite with a different framing premise, not paragraph-level fixes
3. Point the user to the Joy Principle section and Examples for guidance on the target framing

### Error: "Fix Mode Fails After 3 Iterations"
**Cause**: Rewritten paragraphs keep introducing new CAUTION/GRIEVANCE patterns, often because the underlying premise is grievance-based
**Solution**:
1. Output the best version achieved with flagged remaining concerns
2. Explain which specific rubric dimensions resist correction
3. Suggest the framing premise itself may need rethinking, not just the language

---

## References

### Rubric Files
- `references/writing-rubric.md` — Joy-grievance spectrum, subtle patterns, scoring, examples (writing mode)
- `references/instruction-rubric.md` — Positive framing rules, patterns to flag, rewrite strategies, examples (instruction mode)

### Scripts
- `scan-negative-framing.py` — Regex pre-filter for grievance patterns (writing mode, Phase 1)

### Complementary Skills
- `voice-validator` — Voice fidelity validation (different concern)
- `anti-ai-editor` — AI pattern detection and removal (different concern)
- `voice-writer` — Content pipeline that invokes joy-check as a validation phase
- `skill-creator` — Skill creation pipeline that invokes joy-check in instruction mode
