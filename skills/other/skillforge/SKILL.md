---
name: skillforge
description: "Use when creating, improving, finding, or auditing agent skills - the user says 'create a skill', 'do I have a skill for X', 'improve the X skill', 'which skill should I use', asks whether a skill exists for a task, or wants to validate, test, evaluate, package, or health-check skills. Also use for skill ecosystem maintenance (duplicate detection, stale skills, trigger collisions) and advisor checkpoints."
license: MIT
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
  - Task
metadata:
  version: 6.0.0
  domains: [meta-skill, skill-creation, skill-testing, orchestration, routing]
  type: orchestrator
---

# SkillForge 6 - Skill Router, Creator & Ecosystem Maintainer

Routes any skill-related request to the right action (use, improve, create, compose), creates new skills through an evidence-driven pipeline, and maintains the health of the whole skill ecosystem. Core principle: **skill quality is a property of behavior, not documents - a skill is done when a fresh agent demonstrably does better with it than without it.**

## Routing (Phase 0)

Always triage before creating anything:

```bash
python3 scripts/discover_skills.py            # refresh index (auto-refreshes if >24h old)
python3 scripts/triage_skill_request.py "<the user's request>" --json
```

| Triage result | Action |
|---|---|
| Strong match (existing skill) | Recommend it; do not create a duplicate |
| Moderate match | Offer IMPROVE_EXISTING on the matched skill |
| Weak/no match + create intent | Proceed to creation pipeline |
| Multi-domain | Suggest composing existing skills |
| Ambiguous | Ask one clarifying question |

Match bands are keyword-evidence heuristics, not calibrated probabilities - report them as "strong/moderate/weak match", never as percent confidence.

## Creation pipeline

Run phases in order. Each phase's detailed procedure lives in its reference - read the reference when you reach the phase, not before.

**0. Baseline gate (RED).** Before designing anything, dispatch a fresh subagent (Task tool) on 1-2 representative target tasks WITHOUT the skill. Capture verbatim what it does wrong. **If the baseline does not fail, stop - the skill is unnecessary.** The failures become the skill's test cases and its description keywords. See [references/testing-and-evals.md](references/testing-and-evals.md).

**1. Analysis.** Identify explicit, implicit, and discovered requirements. Apply the three load-bearing lenses - Inversion (what guarantees failure → anti-patterns), Pareto (which 20% of scope delivers 80% → cut the rest), Root Cause (is this the real problem?) - plus any others from [references/multi-lens-framework.md](references/multi-lens-framework.md) that earn their tokens. Classify the failure type you are guarding against and match the guidance form to it (see the failure-form table in [references/testing-and-evals.md](references/testing-and-evals.md)). Choose instruction specificity with [references/degrees-of-freedom.md](references/degrees-of-freedom.md). Decide scripts with [references/script-integration-framework.md](references/script-integration-framework.md).

**2. Specification.** Write the spec using [references/specification-template.md](references/specification-template.md). Minimal tier (problem, requirements, decisions with WHY, success criteria, test scenarios) for most skills; full tier (temporal projection, obsolescence triggers, extension points) only for infrastructure skills. Never fill a section you cannot ground - omit it.

**3. Generation in fresh context.** Dispatch a subagent (Task tool) that receives ONLY the spec and the baseline failures - not the analysis transcript - to write SKILL.md and supporting files. Scaffold first: `python3 scripts/init_skill.py <name> --path <skills-dir>`. Description doctrine: trigger conditions only, third person, symptom keywords, never a workflow summary. Budget: SKILL.md under 1,500 words; move depth to references/; `<details>` tags save zero tokens for agents - do not use them.

**4. Execution testing (GREEN).** Re-run the baseline tasks WITH the skill via fresh subagents. Gate on behavioral delta: the with-skill runs must not exhibit the baseline failures. Then run the description-triggering check (positive and near-miss queries). Iterate description and body against observed failures, not hunches. For improvements to existing skills, use blind A/B judging. Full protocols: [references/testing-and-evals.md](references/testing-and-evals.md).

**5. Review = lint + one adversarial reviewer.** Mechanical gates first:

```bash
python3 scripts/validate_skill.py <skill-dir>     # structure, frontmatter, lint (pinned models, word budget, description shape)
python3 scripts/check_docs_safety.py <skill-dir>
```

Then one fresh-context subagent prompted to REFUTE the skill (find the case where it misleads, over-triggers, or fails its own scenarios), carrying the reviewer checklists in [references/synthesis-protocol.md](references/synthesis-protocol.md). Fix what it proves; ship what survives. Do not convene approval panels - same-model unanimity measures nothing.

**6. Ship with evals.** Every generated skill keeps its tests: an `evals/` directory (trigger queries + behavioral scenarios + assertions) so future edits can be regression-tested with `python3 scripts/run_skill_evals.py <skill-dir>`. Iterate post-ship with [references/iteration-guide.md](references/iteration-guide.md).

## Frontmatter and platform facts

Write frontmatter against the current Claude Code field set (17 fields) documented in [references/claude-code-frontmatter.md](references/claude-code-frontmatter.md), which also covers hooks (hooks receive JSON on stdin, not env vars), `context: fork`/`agent`, `$ARGUMENTS`, and the agentskills.io portability limits (64-char name, 1024-char description) that `validate_skill.py` enforces. Never pin dated model IDs (`claude-*-YYYYMMDD`) - the validator rejects them.

## Ecosystem maintenance

```bash
python3 scripts/skillforge_doctor.py              # trigger collisions, duplicates, stale refs, token budgets, description lint
python3 scripts/compile_skill.py <dir> --target claude|codex|agentskills
python3 scripts/package_skill.py <dir> ./dist     # .skill zip, honors .skillignore
python3 scripts/mine_skill_friction.py --consent  # opt-in: mine local transcripts for skill friction
```

Use doctor output to drive IMPROVE_EXISTING work; use friction reports as advisor evidence.

## Context Skill Advisor

Proactive suggestions are delivered through Claude Code hooks (SessionStart surfaces the queue; UserPromptSubmit scores checkpoints inline) - no daemon. Configure with `python3 scripts/install_skillforge.py` (interactive; hooks and Personal Context scanning are **opt-in**, never default). Manage the queue: `python3 scripts/context_advisor.py list|use|snooze|dismiss`. Suggestions are evidence-backed and never auto-invoke a skill.

## Script inventory

| Script | Purpose |
|---|---|
| `discover_skills.py` | Build/refresh the cross-runtime skill index |
| `triage_skill_request.py` | Route input to use/improve/create/compose/clarify |
| `validate_skill.py` | Full structural + lint validation (`quick_validate.py` = fast subset) |
| `run_skill_evals.py` | Run a skill's evals/ regression suite |
| `skillforge_doctor.py` | Ecosystem health report |
| `init_skill.py` | Scaffold a new skill (with evals/) |
| `compile_skill.py` | Compile a skill for a target runtime |
| `package_skill.py` | Package as .skill archive |
| `mine_skill_friction.py` | Opt-in transcript friction mining |
| `context_advisor.py` / `install_skillforge.py` | Advisor queue and setup |
| `check_docs_safety.py` | Unsafe interpolation check |

Script exit codes: 0 success, 1 failure, 2 usage/consent error, 10 validation failure, 11 verification/dependency failure.

Extension points: new lint checks in `validate_skill.py`; new doctor checks in `skillforge_doctor.py`; new compile targets in `compile_skill.py`; new lenses in `references/multi-lens-framework.md`.

## Anti-patterns

| Avoid | Instead |
|---|---|
| Creating without a failing baseline | Run the RED gate; no failure = no skill |
| Description that summarizes workflow | Trigger conditions only - agents act on summaries and skip the body |
| Body "Triggers" sections as a mechanism | Only the frontmatter description drives invocation |
| Approval panels and self-scored gates | Lint what is falsifiable; adversarially refute the rest |
| `<details>` blocks for "progressive disclosure" | Separate reference files loaded on demand |
| Pinned dated model IDs | Family aliases or omit `model:` |
| Duplicating an existing skill | Phase 0 triage first, always |

## Verification checklist

- [ ] Baseline failure captured before writing (RED)
- [ ] With-skill runs clear the baseline failures (GREEN)
- [ ] Trigger check passes on positive and near-miss queries
- [ ] `validate_skill.py` and `check_docs_safety.py` pass
- [ ] Adversarial reviewer's proven issues fixed
- [ ] `evals/` shipped with the skill; `run_skill_evals.py` passes
- [ ] SKILL.md under 1,500 words (`wc -w`)
