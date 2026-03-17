---
name: model-ab-test
description: "Use when validating model downgrades for skills or agents. Runs A/B comparison between current and proposed model, scores outputs against test criteria, produces verdict."
user-invocable: true
context: fork
allowed-tools: Task, Read, Write, Glob, Grep
argument-hint: <test-definition-file> [specific-test-name]
---

# Model A/B Test Harness

Run each test case from a definition file: dispatch two subagents (baseline vs proposed model) in parallel, score outputs binary per criterion, write evidence files, produce verdict.

## Phase 1: Parse Test Definitions

Split `$ARGUMENTS` — first token = file path, second (optional) = test name filter (case-insensitive substring match on `### <name>` headings).

Read the file. For each test case block, extract:

| Field | Source |
|-------|--------|
| `name` | `### <name>` heading (before parenthetical) |
| `proposed_model` | From `(Opus -> X)` — extract target as lowercase: `sonnet` or `haiku` |
| `test_input` | Content under `**Test input:**` until next bold section |
| `green_criteria` | List under `**GREEN criteria**` |
| `red_indicators` | List under `**RED indicators**` |

Skip cases with missing fields (log warning). Skip `~~strikethrough~~` or `EXEMPTED` headings entirely.

## Phase 2: Locate Content + Preloaded Skills

For each test case `name`:

1. Glob `plugins/*/skills/{name}/SKILL.md` — if found, this is `primary_content` (type: skill)
2. Else glob `plugins/*/agents/{name}.md` — if found, this is `primary_content` (type: agent)
3. If agent has `skills:` in frontmatter, parse comma-separated names. For each:
   - If qualified (`plugin:skill`), split on `:` → glob `plugins/{plugin}/skills/{skill}/SKILL.md`
   - If bare name → glob `plugins/*/skills/{name}/SKILL.md`
   - Read content, store in `preloaded_skills` map
4. Not found → log error, skip test case

## Phase 3: Dispatch A/B Subagents

For each test case, assemble the prompt using the template from `references/subagent-prompt.md`. Replace placeholders with resolved content.

Dispatch **TWO Task subagents in a SINGLE message** (parallel):

```
Task A: subagent_type="general-purpose", model="opus"
Task B: subagent_type="general-purpose", model="{proposed_model}"
```

Both receive the **identical** assembled prompt. No modifications for either model.

After both return:
- Write Task A output → `_docs/model-tests/results/{name}-opus.md`
- Write Task B output → `_docs/model-tests/results/{name}-{proposed_model}.md`

## Phase 4: Score Results

Read both output files. Score each criterion **binary** — no "close enough":

**GREEN criteria** — for each, per model: `pass` or `fail`
**RED indicators** — for each, per model: `clean` or `triggered`

Every score MUST cite a specific quote from the output as evidence.

**Verdict logic:**

| Condition | Verdict |
|-----------|---------|
| Proposed passes ALL green AND triggers ZERO red | **PASS** |
| Proposed passes all green AND red triggers <= opus | **PASS** |
| Proposed fails any green that opus passes, OR triggers more red | **FAIL** |
| Both models show identical scores | **INCONCLUSIVE** |
| Otherwise | **INCONCLUSIVE** |

Write comparison entry per test case:

```markdown
## {name} (Opus -> {proposed_model})

### GREEN Criteria
| # | Criterion | Opus | {proposed_model} |
|---|-----------|:----:|:----------------:|
| 1 | {text} | pass/fail | pass/fail |

### RED Indicators
| # | Indicator | Opus | {proposed_model} |
|---|-----------|:----:|:----------------:|
| 1 | {text} | clean/triggered | clean/triggered |

### Verdict: {PASS/FAIL/INCONCLUSIVE}
{1-2 sentences citing specific evidence from outputs.}
```

## Phase 5: Summary Report

After all test cases, derive the report filename from the source test definition file: strip path and extension to get the stem (e.g., `01-haiku-templates` from `_docs/model-tests/01-haiku-templates.md`). Write `_docs/model-tests/results/{stem}-report.md`:

```markdown
# Model A/B Comparison Report
Generated: {date} | Source: {test definition file}

{all comparison entries from Phase 4}

---

## Summary
| Skill/Agent | Downgrade | GREEN | RED | Verdict |
|-------------|-----------|:-----:|:---:|:-------:|
| {name} | Opus->{model} | {n}/{total} | {n} new | PASS/FAIL/INCONCLUSIVE |

## Safe to Downgrade
{PASS verdicts with justification, or "None."}

## Keep on Opus
{FAIL verdicts with failed criteria, or "None."}

## Needs More Testing
{INCONCLUSIVE verdicts with what would resolve, or "None."}
```

## Sequencing

- Test cases within a file: **sequential** (one at a time)
- Subagents A and B for same test case: **parallel** (both Task calls in one message)

## Discipline Rules

These rules exist because without them, agents rationalize shortcuts under pressure. Each rule addresses a documented failure mode.

| # | Rule | Why It Exists |
|---|------|---------------|
| 1 | Both Task calls in a **single message**. Never sequential. | Agents default to "run A first, then B" under time pressure |
| 2 | Every score is **binary** (pass/fail, clean/triggered). No "partial", "close enough", "similar" | Without this, agents score subjectively: "looks about the same" |
| 3 | Every score cites a **specific quote** from the output file | Without this, agents score from memory without reading files |
| 4 | Write output files **before** scoring — files are the evidence record | Agents skip file writes to "save time" |
| 5 | Prompt is **identical** for both models. Zero modifications | Agents "help" the weaker model by simplifying the prompt |
| 6 | Use the assembled prompt template only. No ad-hoc prompts | Agents improvise prompts that leak test criteria to the model |
| 7 | Ambiguous criterion → score as **fail**, note in verdict | "Benefit of the doubt" produces false PASS verdicts |
| 8 | **Never** run multiple test cases in parallel | Context overload makes scoring unreliable |
| 9 | "Time pressure" is not a reason to skip steps | The #1 rationalization for cutting corners |
| 10 | "Manager says eyeball it" is not a reason to skip scoring | Authority pressure is the #2 rationalization |
| 11 | "We already know the answer" is not a reason to skip dispatch | Sunk cost / confirmation bias is the #3 rationalization |
| 12 | Existing output files are **not** a substitute for fresh dispatch | Agents find prior results and skip re-running "since it's done" |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Sequential subagent dispatch | Both Task calls in single message |
| Running all test cases at once | One at a time, sequentially |
| Generous scoring ("close enough") | Binary: met or not met |
| Forgetting to write output files | Write BEFORE scoring |
| Not quoting evidence in scores | Every score needs a quote |
