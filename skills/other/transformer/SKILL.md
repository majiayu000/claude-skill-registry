---
name: transformer
description: Use when rewriting an existing skill so Opus 4.7 (or any frontier reasoning model) executes it with better judgment, less scaffolding, and tighter calibration. Do NOT trigger for new skills from scratch (use skill-creator) or for prompt artifacts (use prompt).
argument-hint: <path to SKILL.md or skill name>
---

input = $ARGUMENTS

Rewrite the target skill so Opus 4.7 executes it with better judgment. Drafting craft lives in `~/.claude/skills/prompt/SKILL.md` (inlined below).

## Procedure

1. Resolve `$input` to a path. If no file at `$input`, try `~/.claude/skills/$input/SKILL.md`, then `./.claude/skills/$input/SKILL.md`. HALT and ask if neither resolves.
2. Read the target completely.
3. Classify every element — strip / keep / add-missing (rules below).
4. Write the rewrite. The diff is the review surface — the user reads it after.

## Classify

**Strip — reasoning 4.7 does unaided:**
- Step-by-step scaffolding for problems the model solves directly.
- Phantom constraints ("be careful", "be thorough", "write clean code").
- Restated CLAUDE.md doctrine.
- Cadence scaffolding ("every N tool calls, summarize") — 4.7 emits progress updates natively.

**Keep — domain knowledge the model cannot infer:**
- **Orchestration.** Approval gates, agent coordination, conditional phases.
- **Calibration.** Statements countering pretraining bias — "you'll want to skip this step — don't"; "this tier is 50% of savings". Highest-value lines in any skill; never strip.
- **Templates & contracts.** Output formats, tool-call shapes, approval signals.
- **Domain facts the model can't infer.** Library quirks, protocol behaviors, tool gotchas. Phrase positively ("apply formatting before closing the run"), not as avoidance — negatives prime the forbidden behavior.
- **Domain taxonomies.** Non-obvious expertise compressed into categories.

**Litmus.** Would removing this cause wrong output, skipped coordination, or silent regression? Keep. Would a reasoning model arrive here unaided? Strip.

## Both-directions guardrail

Under-specification is the twin failure of over-scaffolding. If the target is principle-only with no anchoring, ADD:

- One example or anti-example showing the core judgment call.
- 2–3 domain facts the model can't infer, phrased positively.
- Explicit invariants, XML-tagged when load-bearing.

"Nothing to cut, much to add" is a valid verdict. A rewrite that removes more than it adds is not automatically better.

## Calibration for the rewriter

- Resist voice-only rewrites and checklists; prefer structural changes. Exception: if the target's frame is wrong, rewrite from scratch against the 4.7 guidelines.
- Domain facts and calibration statements are tiny per line but load-bearing. Don't cut them to hit a length target.

## Worked transformation

**Before** — over-scaffolded:

    ## Investigation
    1. Open the file
    2. Read all of it carefully
    3. Make a list of all the functions
    4. Identify what they do
    5. Think about which ones might have bugs
    6. For each suspected bug:
       - Write a hypothesis
       - Test it
       - Confirm or reject
    7. Document findings
    8. Suggest fixes

**After** — calibrated:

    Read the target file completely before hypothesizing — partial-read
    hypotheses miss cross-function invariants. For each suspected bug:
    state the hypothesis, name the exact test that would confirm or
    reject it, run that test before proceeding.

Steps 1–5 are reasoning 4.7 does unaided. Step 6's structure is the only load-bearing content; it gets a calibration line explaining *why* read-fully-first. Steps 7+ are user-owned workflow, not skill content.

## Prompt design philosophy

Drafting craft is authoritative in the prompt skill — do not restate. Inlined so it's in context while you draft:

!`cat ~/.claude/skills/prompt/SKILL.md`

## Opus 4.7 migration guide

Target-model behavior reference:

!`cat ~/.claude/skills/transformer/opus-4.7-migration-guide.md`

## Opus 4.7 — what's new

New capabilities that often justify scaffolding removal:

!`cat ~/.claude/skills/transformer/opus-4.7-whats-new.md`
