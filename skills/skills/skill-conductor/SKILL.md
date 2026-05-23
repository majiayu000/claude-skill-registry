---
name: skill-conductor
description: >
  Create, edit, evaluate, and package agent skills. Use when building a new
  skill from scratch, improving an existing skill, running evals to test a
  skill, benchmarking skill performance, optimizing a skill's description
  for better triggering, reviewing third-party skills for quality, or
  packaging skills for distribution. Not for using skills or general coding
  tasks.
---

# Skill Conductor

Full lifecycle management for agent skills: **draft → test → review → improve → repeat**.

One skill to rule them all — from architecture to packaging. The core loop is always the same: write something, test it, see what fails, fix it, test again.

## How to communicate

Read context cues. If the user is a skill author iterating on their own work, be direct and technical. If they're new to skills, explain the *why* behind each step — not just what to do, but why it matters. Default to conversational, not robotic.

- Explain trade-offs when there's a real choice to make
- Use concrete examples over abstract rules
- When something fails, explain the root cause, not just the fix
- Imperative voice in instructions: "Extract the data", not "You should extract"

## Modes

Detect mode from context. If ambiguous, ask.

| Mode | When | What happens |
|------|------|-------------|
| 1. CREATE | "build a skill", "new skill for..." | Full lifecycle: intent → architecture → scaffold → write → test |
| 2. IMPROVE | "fix this skill", "it doesn't trigger" | Diagnose → eval loop → blind comparison → iterate |
| 3. VALIDATE | "test this skill", "run evals" | Structural checks + trigger testing + 5-axis scoring |
| 4. REVIEW | "review this skill", third-party assessment | 11-point quality gate, quick and focused |
| 5. OPTIMIZE | "improve triggering", "description optimization" | Automated description optimization with train/test split |
| 6. PACKAGE | "package for distribution" | Validate + bundle into .skill file |

---

## Mode 1: CREATE

### Step 1: Capture Intent

Before writing anything, extract 2–3 concrete scenarios.

Ask:
- "What specific task should this skill handle?"
- "What would a user say to trigger it?"
- "What should NOT trigger it?"

Don't move on until you have a clear picture of what the skill does, for whom, and when. This prevents the most common failure: a skill that does *something* but triggers for the wrong things.

### Step 2: Baseline (TDD RED)

Before writing the skill, verify the agent fails without it:

1. Take one scenario from Step 1
2. Run it in a clean session without the skill
3. Document what went wrong — what the agent guessed, what it missed

If the agent already handles it perfectly, the skill is unnecessary. This sounds obvious, but it's the most skipped step and the most valuable one.

### Step 3: Architecture

Choose a primary pattern from `references/patterns.md` (can combine):

| Pattern | Use when |
|---------|----------|
| Sequential workflow | clear step-by-step process |
| Iterative refinement | output improves with cycles |
| Context-aware selection | same goal, different tools by context |
| Domain intelligence | specialized knowledge beyond tool access |
| Multi-MCP coordination | workflow spans multiple services |

Choose degrees of freedom — this determines how much control vs. flexibility the skill gives the agent:

| Freedom | When | Example |
|---------|------|---------|
| Low (scripts) | fragile, error-prone, must be exact | PDF rotation, API calls |
| Medium (pseudocode) | preferred pattern exists, some variation ok | data processing |
| High (text) | multiple valid approaches, judgment needed | design decisions |

### Step 4: Scaffold

```bash
uv run scripts/init_skill.py <skill-name> --path <output-dir> [--resources scripts,references,assets]
```

Or create manually:
```
skill-name/
├── SKILL.md          # required — the brain
├── scripts/          # deterministic operations (executed, not loaded)
├── references/       # detailed docs (loaded on demand)
└── assets/           # templates, images for output (never loaded)
```

### Step 5: Write SKILL.md

#### Frontmatter

```yaml
---
name: kebab-case-name
description: >
  [Purpose in one sentence]. Use when [triggers].
  Do NOT use for [negative triggers].
---
```

The description is the single most important line. It determines whether the skill gets triggered at all. Rules:

- `name`: lowercase, digits, hyphens only. No consecutive hyphens. Matches folder name. Max 64 chars
- `description`: max 1024 chars. No angle brackets. No process/workflow steps
- Start with purpose, then "Use when...", then "Do NOT use for..."
- **NEVER put workflow in description** — tested: agent follows description instead of reading body

```yaml
# GOOD: purpose + triggers, no process
description: Analyze Figma design files for developer handoff. Use when user uploads .fig files or asks for "design specs". Do NOT use for Sketch or Adobe XD.

# BAD: process in description (agent skips body)
description: Exports Figma assets, generates specs, creates Linear tasks, posts to Slack.
```

#### Body structure

```markdown
# Skill Name

## Overview
What this enables. 1-2 sentences. Core principle.

## [Main sections]
Step-by-step with numbered sequences.
Concrete templates over prose.
Imperative voice throughout.

## Common Mistakes
What goes wrong + how to fix.

## Troubleshooting (if applicable)
Error: [message] → Cause: [why] → Fix: [how]
```

#### Writing rules

- **One term per concept.** Pick "template" and stick with it — not template/boilerplate/scaffold
- **Progressive disclosure.** SKILL.md = brain (<500 lines). References = details. One level deep
- **Token budget.** Frequently loaded: <200 words. Standard: <500 lines. Heavy: move to references/
- **No junk files.** No README, CHANGELOG inside the skill
- **Scripts:** bundle when same code rewritten repeatedly, or operation is fragile. Must return descriptive stdout/stderr on failure

### Step 6: Test Cases & Eval Loop

Create test cases in `evals/evals.json` (see `references/schemas.md` for format):

1. Write 3–5 eval prompts covering core use cases
2. For each, define expectations (verifiable statements about the output)
3. Start without assertions — run first, observe, then write assertions based on what good output looks like

To run the eval loop:

1. Spawn executor subagent with the skill active, using the eval prompt
2. Spawn a baseline run in parallel (same prompt, no skill) — for comparison
3. While runs execute, draft assertions based on expected behavior
4. When runs complete, save timing data from task notifications
5. Grade outputs using `agents/grader.md`
6. Launch eval viewer: `uv run eval-viewer/generate_review.py <workspace>`
   - **Headless/Cowork:** use `--static <output.html>` instead of live server. ALWAYS show viewer to user BEFORE editing skill yourself
7. Review outputs, write feedback, iterate on the skill

### Step 7: Verify & Refactor

1. Does the skill trigger automatically for the right queries?
2. Does the agent follow body instructions (not just description)?
3. Does the output meet use case requirements?
4. Does it NOT trigger on unrelated queries?

If any fail → iterate. Find how the agent rationalizes around the skill, plug loopholes, re-verify.

---

## Mode 2: IMPROVE

### Step 1: Diagnose

Read the existing SKILL.md completely. Identify the problem class:

| Problem | Signal | Fix |
|---------|--------|-----|
| Undertriggering | skill doesn't load | add keywords, trigger phrases, file types to description |
| Overtriggering | loads for unrelated queries | add negative triggers, be more specific |
| Skips body | follows description only | remove process/workflow from description |
| Inconsistent output | varies across sessions | add explicit templates, reduce freedom, add scripts |
| Too slow | large context | move detail to references/, cut body to <500 lines |

### Improvement mindset

1. **Generalize from feedback.** You're iterating on a few examples, but the skill will be used on thousands of prompts. Don't overfit — avoid fiddly patches or oppressive MUSTs for one test case. Try different metaphors or patterns instead
2. **Keep the prompt lean.** Read transcripts, not just outputs. If the skill makes the model waste time on unproductive steps, remove those instructions and see what happens
3. **Explain the why.** LLMs have good theory of mind. Instead of ALWAYS/NEVER in caps, explain the reasoning — it's more powerful and robust. If you're writing rigid rules, reframe as explanations
4. **Look for repeated work.** If all test runs independently write the same helper script, bundle it in `scripts/`. Saves every future invocation from reinventing the wheel

### Step 2: Eval Iteration Loop

The improvement cycle mirrors CREATE Step 6, but focused on the broken behavior:

1. Run the failing case with current skill → document failure
2. Apply fix using writing rules from CREATE Step 5
3. Run eval again → grade with `agents/grader.md`
4. Launch viewer: `uv run eval-viewer/generate_review.py <workspace>`
   - **Headless/Cowork:** use `--static <output.html>` instead of live server
5. Review, provide feedback, iterate

### Step 3: Blind Comparison (optional, for major changes)

When you have two meaningfully different versions:

1. Run both versions on the same evals
2. Spawn `agents/comparator.md` — receives outputs A and B without knowing which skill produced which
3. Comparator scores on rubric (content + structure, 1–5 each) and picks a winner
4. Spawn `agents/analyzer.md` — unblinds results, analyzes WHY the winner won
5. Apply insights to improve the losing version

This prevents bias. The comparator judges output quality, not skill design.

---

## Mode 3: VALIDATE

Three stages, run in order.

### Stage 1: Structural Validation

```bash
uv run scripts/eval_skill.py <skill-folder>
```

Checks: frontmatter, naming, description quality, process leak detection, body size, structure, scripts. Target: 10/10, no warnings.

### Stage 2: Discovery (trigger testing)

Generate 6 test prompts:
- 3 that SHOULD trigger the skill
- 3 that should NOT (similar-sounding but wrong domain)

Run each in clean session. Target: 6/6 correct.

For automated trigger testing at scale, use:
```bash
uv run scripts/run_eval.py --eval-set <path> --skill-path <path> --runs-per-query 3
```

### Stage 3: 5-Axis Scoring

Rate on 5 axes (1–10 each):

| Axis | What it measures |
|------|-----------------|
| Discovery | triggers correctly, doesn't false-trigger |
| Clarity | instructions unambiguous, no guessing needed |
| Efficiency | token budget respected, progressive disclosure used |
| Robustness | handles edge cases, scripts have error handling |
| Completeness | covers the stated use cases fully |

**Interpretation:** 45–50 production ready · 35–44 solid · 25–34 needs work · <25 rewrite

---

## Mode 4: REVIEW

Quick quality gate for third-party skills.

### Checklist (pass/fail)

```
[ ] SKILL.md exists, exact case
[ ] Valid YAML frontmatter (name + description)
[ ] name: kebab-case, matches folder, ≤64 chars
[ ] description: ≤1024 chars, no angle brackets
[ ] description has triggers ("Use when...")
[ ] description has NO workflow/process steps
[ ] No README.md inside skill folder
[ ] SKILL.md < 500 lines
[ ] References max 1 level deep
[ ] Scripts tested and executable
[ ] No hardcoded paths/tokens/secrets
```

Then run VALIDATE Stage 2 (discovery) on the description. Report score + checklist.

The checklist exists because these are the failure modes that actually happen in practice — especially process-in-description, which causes the agent to skip the body entirely.

---

## Mode 5: OPTIMIZE

Automated description optimization. The description competes with other skills for Claude's attention — optimization finds the wording that triggers most accurately.

### How it works

1. Create an eval set: 20 queries (10 should-trigger, 10 should-not)

#### Writing good eval queries

Queries must be realistic — concrete, detailed, with file paths, context, abbreviations, typos. Not `"Format this data"` but `"my boss sent Q4 sales final FINAL v2.xlsx, add profit margin % column, revenue is col C costs col D"`.

**Should-trigger (10):** Different phrasings of the same intent — formal, casual, implicit. Include cases where user doesn't name the skill but clearly needs it. Add competing-skill edge cases.

**Should-NOT-trigger (10):** Near-misses that share keywords but need something different. Adjacent domains, ambiguous phrasing. "Write fibonacci" as negative for PDF skill = useless — too easy. Make negatives genuinely tricky.

**Triggering mechanics:** Claude only consults skills for tasks it can't handle directly. Simple queries ("read this PDF") won't trigger skills regardless of description — Claude handles them with basic tools. Eval queries must be substantive enough that consulting a skill would help.

2. Review queries in the browser: `assets/eval_review.html`
3. Run the optimization loop:

```bash
uv run scripts/run_loop.py \
  --eval-set evals/eval_set.json \
  --skill-path <skill-dir> \
  --model claude-sonnet-4-20250514 \
  --max-iterations 5 \
  --holdout 0.4 \
  --verbose
```

The loop:
- Splits queries into train (60%) and test (40%) to prevent overfitting
- Each iteration: evaluates current description → Claude proposes improvement → re-evaluates
- Improvement model sees only train results (blinded to test)
- Selects the best description by test score
- Opens live HTML report automatically

### Supporting scripts

| Script | Purpose |
|--------|---------|
| `scripts/run_eval.py` | Run trigger evaluation on a description |
| `scripts/improve_description.py` | Claude proposes improved description |
| `scripts/generate_report.py` | HTML visualization of optimization history |
| `scripts/aggregate_benchmark.py` | Statistical aggregation of benchmark runs |

---

## Mode 6: PACKAGE

1. Run REVIEW checklist (Mode 4)
2. Validate:

```bash
uv run scripts/quick_validate.py <skill-folder>
```

3. Package:

```bash
uv run scripts/package_skill.py <skill-folder> [output-dir]
```

Creates `skill-name.skill` (zip with .skill extension). Verify: unzip in temp dir, check structure intact.

---

## Quick Reference

### Skill categories

1. **Document/Asset Creation** — consistent output (docs, designs, code)
2. **Workflow Automation** — multi-step processes with methodology
3. **MCP Enhancement** — workflow guidance on top of tool access

### File purposes

| Directory | Loaded? | Purpose |
|-----------|---------|---------|
| SKILL.md | on trigger | brain — instructions |
| references/ | on demand | detailed docs, schemas |
| scripts/ | executed, not loaded | deterministic operations |
| assets/ | never loaded | templates, images |

### Progressive disclosure budget

| Level | When loaded | Budget |
|-------|-------------|--------|
| Frontmatter | always (system prompt) | ~100 words |
| SKILL.md body | on trigger | <500 lines |
| Bundled resources | on demand | unlimited |

### Description formula

```
[What it does] + Use when [triggers, file types, symptoms]. + Do NOT use for [negatives].
```

## Reference Files

| Path | What's inside |
|------|--------------|
| `agents/grader.md` | Evidence-based assertion grading |
| `agents/comparator.md` | Blind A/B output comparison |
| `agents/analyzer.md` | Post-hoc analysis + benchmark notes |
| `references/patterns.md` | 5 architectural patterns + anti-patterns |
| `references/schemas.md` | JSON schemas for evals, grading, benchmark |
| `eval-viewer/` | Interactive HTML viewer for eval results |
| `assets/eval_review.html` | Trigger eval set editor |
| `scripts/eval_skill.py` | Structural validation (10-point scoring) |
| `scripts/init_skill.py` | Skill scaffolder |
| `scripts/run_eval.py` | Trigger evaluation runner |
| `scripts/run_loop.py` | Eval + improve optimization loop |
| `scripts/improve_description.py` | Claude-powered description improvement |
| `scripts/aggregate_benchmark.py` | Benchmark statistics aggregator |
| `scripts/generate_report.py` | HTML report generator |
| `scripts/quick_validate.py` | Quick validation for packager |
| `scripts/package_skill.py` | Skill → .skill packager |
| `scripts/utils.py` | Shared utilities (parse_skill_md) |
