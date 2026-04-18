---
name: transformer
description: Use when rewriting an existing skill so Opus 4.7 (or any frontier reasoning model) executes it with better judgment, less scaffolding, and tighter calibration. Do NOT trigger for new skills from scratch (use skill-creator) or for prompt artifacts (use prompt).
argument-hint: <path to SKILL.md or skill name>
---

input = $ARGUMENTS

Rewrite the target skill so Opus 4.7 executes it with better judgment — not just different wording. The drafting craft is governed by `~/.claude/skills/prompt/SKILL.md` (inlined below); this skill adds only what's specific to transforming existing skills.

## Resolve input

Path first. If no file at `$input`, try `~/.claude/skills/$input/SKILL.md`, then `./.claude/skills/$input/SKILL.md`. HALT and ask if neither resolves — don't guess.

## Classify each element

**Strip — content a reasoning model handles natively:**
- Reasoning scaffolding for problems it solves unaided.
- Phantom constraints ("write clean code", "be careful", "be thorough").
- Restated CLAUDE.md doctrine.
- Cadence scaffolding ("every N tool calls, summarize") — Opus 4.7 emits progress updates natively; external scaffolding impedes.

**Keep — domain knowledge the model cannot infer:**
- **Orchestration.** Approval gates, agent coordination, conditional phases. Protocol, not scaffolding.
- **Calibration.** Statements countering pretraining bias — "you'll want to skip this step — don't"; "this tier is 50% of savings". **Highest-value lines in any skill.** Never strip.
- **Templates & contracts.** Output formats, tool-call shapes, approval signals.
- **Domain facts the model can't infer.** Library quirks, protocol behaviors, tool gotchas. Phrase positively ("python-pptx: apply formatting before closing the run"), not as things to avoid — negatives prime the forbidden behavior. LLM-output patterns are not domain facts; reframe them as positive invariants in the relevant section.
- **Domain taxonomies.** Non-obvious expertise compressed into categories.

**Litmus test.** Would removing this cause wrong output, skipped coordination, or silent regression? Keep. Would a reasoning model arrive here unaided? Strip.

## Both-directions guardrail

Under-specification is the twin failure of over-scaffolding. If the target is principle-only — abstract rules with no anchoring — ADD:

- At least one example or anti-example showing the core judgment call.
- 2–3 domain facts the model can't infer, phrased positively.
- Explicit invariants, XML-tagged when load-bearing.

The verdict "nothing to cut, much to add" is valid. A rewrite that removes more than it adds is not automatically better.

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
    9. Present them to the user
    10. Iterate based on feedback

**After** — calibrated:

    Read the target file completely before hypothesizing — hypotheses
    from partial reads miss cross-function invariants. For each suspected
    bug: state the hypothesis, name the exact test that would confirm or
    reject it, run that test before proceeding.

**Diagnosis.** Steps 1–5 are reasoning a 4.7 model does unaided. Step 6's structure is the only load-bearing content, and it gets a calibration line explaining *why* read-fully-first. Steps 7–10 are user-owned workflow, not skill content.

## Calibration

Internalize before drafting:

- You will want to rewrite every line. Don't. Changes in voice without changes in structure are noise.
- Flat rule lists feel clean; they train the model to pattern-match instead of reason.
- Your first instinct will be a checklist. The target is likely *under*-specified in calibration, *over*-specified in steps. Compress steps, add calibration.
- Domain facts and calibration statements are tiny per line but load-bearing. Don't cut them to hit a length target.

## Process

1. Resolve `$input` to a SKILL.md path.
2. Read the target completely.
3. Classify every element — strip / keep / add-missing.
4. Draft the rewrite.
5. **Present via AskUserQuestion. Do not write the file until the user approves.** Skill rewrites are silent by default; regressions are hard to diff after the fact. This gate is non-negotiable.
6. On approval, write.

## Prompt design philosophy

Drafting craft is authoritative in the prompt skill — do not restate below. Inlined so it's in context while you draft:

!`cat ~/.claude/skills/prompt/SKILL.md`

## Opus 4.7 migration guide

Target-model behavior reference — what changed in 4.7 vs. prior Claude versions. Inlined so calibration decisions are grounded in documented shifts, not guesses:

!`cat ~/.claude/skills/transformer/opus-4.7-migration-guide.md`

## Opus 4.7 — what's new

New-capability reference — what 4.7 can now do unaided (often justifying scaffolding removal):

!`cat ~/.claude/skills/transformer/opus-4.7-whats-new.md`
