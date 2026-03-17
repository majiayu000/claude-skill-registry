---
name: ralph-prompt-generator
description: Use when a user has a rough coding objective and needs an execution-ready `$ralph-wiggum-codex` prompt with optimized structure, model/reasoning settings, and loop flags.
---

# Ralph Prompt Generator

Companion skill for `$ralph-wiggum-codex`.

This skill converts a rough request into a paste-ready handoff block that:
- preserves intent and constraints
- clarifies success criteria and validations
- selects model + reasoning defaults
- proposes Ralph runner guardrails (iterations, scopes, timeouts, failures)

## The Core Problem This Skill Solves

Prompt improvement is underspecified by default.

When the user provides a vague prompt, the only reliable way to improve it is:
- extract what is already specified
- identify what is missing
- ask targeted questions only where missing details change execution
- draft a structured prompt
- critique and revise it before finalizing

This skill encodes that workflow so the agent is not guessing.

## When To Use

Use this skill when:
- The user objective is under-specified, verbose, or ambiguous.
- Model choice, reasoning effort, and loop guardrails are unclear.
- Validation or scope constraints are missing.
- The user wants a reusable handoff prompt for a long-running Ralph loop.

Do not use this skill when:
- The user already provided a complete run-ready Ralph handoff block.
- The user wants `$ralph-wiggum-codex` executed immediately without rewriting.

## Prompt-Improver Workflow (Draft -> Critique -> Finalize)

Follow this internal workflow (inspired by `prompt-improver.md` + `prompt-improver-finalize.md`).

### Step 1: Extract What Exists

From the source prompt, extract:
- explicit objective(s)
- explicit constraints (must/must-not)
- environment facts (language, frameworks, repo, OS)
- any validation signals (tests, lint, build)
- any examples (input/output pairs)

Do not reinterpret constraints. Copy them into the brief.

### Step 2: Identify Variables And Unknowns

Build a minimal variable table in your head:
- What is required to run Ralph correctly?
- What will change the plan/flags materially?

Required for a final handoff block:
- `cwd`
- `validation_cmds`

Required for many real-world tasks:
- `progress_scopes` (especially when narrow/high risk)
- success criteria

If anything required is missing, prepare questions.

### Step 3: Draft The Handoff Block (Internal)

Draft the final handoff block using the template below.

Rules:
- include non-goals when the prompt is broad
- keep context minimal (only execution-relevant)
- keep the block scannable

Do not output the draft yet if any required clarifications are missing.

### Step 4: Critique The Draft

Run these checks before final output:

Constraint preservation:
- All explicit must/must-not rules carried forward.
- No constraint weakened.

Anti-scope-creep:
- No new deliverables.
- No prescriptive step-by-step implementation plan.
- Non-goals prevent drift.

Execution readiness:
- `cwd` present.
- `validation_cmds` present and ordered.
- `progress_scopes` are narrow enough.
- Runner flags match the actual runner (no invented flags).

Prompting quality:
- clear delimiters
- observable success criteria
- no chain-of-thought prompting language ("think step by step")

### Step 5: Revise

Tighten the objective, add missing non-goals, and fix any guardrail gaps.

If revisions reveal missing info, ask questions instead of finalizing.

### Step 6: Finalize

If all required clarifications are resolved:
- output exactly one fenced markdown code block
- no additional prose outside the code block

If not resolved:
- ask the smallest set of questions that unblock finalization

## Non-Negotiable Rules

1. Clarify, do not prescribe.
- Improve the briefing and boundaries.
- Do not do the downstream agent’s work.

2. Preserve constraints.
- Keep all must/must-not constraints.
- If you introduce an assumption, label it as an assumption.

3. Avoid scope creep.
- Do not add deliverables the user didn’t ask for.
- Prefer explicit non-goals over speculative roadmaps.

4. Optimize for execution.
- Make success criteria observable.
- Make validations explicit and ordered.

## Intake Fields (What To Extract)

Normalize the user prompt into these fields. Prefer to infer from context before asking.

- `cwd`: where to run (repo path)
- `goal`: one sentence; testable
- `constraints`: hard requirements and must-nots
- `non_goals`: explicit out-of-scope items
- `success_criteria`: observable outcomes (ideally tied to validations)
- `validation_cmds`: repeatable commands proving success
- `progress_scopes`: git pathspec(s) that should change for progress to count
- `risk_profile`: `low|medium|high` based on blast radius
- `surface`: Codex session vs API-oriented usage
- `source_of_truth`: paths/URLs defining requirements (optional)
- `preflight_cmds`: one-time commands before the loop (optional)

If the user supplies examples, preserve them as examples, not additional requirements.

## Optional Auto-Discovery (When Repo Access Exists)

If `validation_cmds` are missing, attempt a quick scan and propose candidates, then ask the user to confirm:
- `package.json` scripts: `lint`, `test`, `typecheck`, `build`
- `Makefile`, `justfile`, `Taskfile.yml`
- `pyproject.toml`, `tox.ini`, `pytest.ini`
- `go.mod` (common default: `go test ./...`)
- `tests/`, `scripts/`, repo `README.md`

If `progress_scopes` are missing, propose the narrowest plausible scope:
- prefer a module path implied by the goal
- otherwise prefer `src/` (and add `tests/` only if tests are expected)

Never finalize the handoff block with guessed validations.

## Mandatory Clarification Behavior

Ask this question every run before finalizing output:

`Do you want a suggested output section included in the generated prompt?`

If unanswered after one follow-up attempt, default to: omit suggested output.

Ask additional clarifying questions only when required for correctness or safety:
- Missing `cwd`.
- Missing or unknown `validation_cmds`.
- Missing `progress_scopes` for narrow/high-risk tasks.
- Conflicting constraints.
- Unclear success criteria.

Clarification channel:
- In Plan Mode: use `request_user_input`.
- Outside Plan Mode: ask plain-text questions.

If 3+ clarifications are required and you are not in Plan Mode, recommend switching to Plan Mode (`/plan`) so questions can be answered efficiently.

## Synthesis Rules (Model + Guardrails)

Use the references to keep selections consistent:
- `references/prompt-improver-principles.md`
- `references/openai-codex-prompting-2026.md`
- `references/ralph-flag-selection-matrix.md`

If you are uncertain about a model name, config key, or capability, consult the `openaiDeveloperDocs` MCP dependency declared in `agents/openai.yaml`.

### Surface-Aware Model Selection

- Codex sessions: default `gpt-5.3-codex`.
- API-oriented runs: default `gpt-5.2-codex`.

If the user explicitly requests a different model, preserve it.

### Reasoning Effort Selection

Select one and justify briefly inside the handoff block:
- `medium`: low ambiguity, narrow change, low blast radius
- `high`: multi-step engineering work
- `xhigh`: ambiguous requirements, high risk, cross-system changes, migrations

Avoid chain-of-thought prompting language.

### Autonomy / Sandbox Guidance

If the task is high risk, include a conservative recommendation:
- prefer `--autonomy-level l0` or `l1` for read-heavy or safety-critical work
- prefer `--autonomy-level l2` for typical engineering tasks
- use `l3` only when explicitly requested

Only include an explicit `--sandbox` override when you have a strong reason.

### Loop Flag Synthesis

Map complexity/risk to runner flags using `references/ralph-flag-selection-matrix.md`.

Always include (unless user overrides):
- `--events-format both`
- `--progress-artifact`

## Strict Output Contract

When clarifications are complete, return exactly one fenced markdown code block and no additional prose.

If required clarifications are still missing, ask questions instead of producing the final block.

### Final Handoff Block Template

```text
/skills
$ralph-wiggum-codex
Run this in: <cwd>
Objective: <one-sentence goal>
Context (optional): <only facts that materially affect implementation>
Constraints:
- <must / must-not>
Non-goals:
- <explicitly out of scope>
Success criteria:
- <observable criteria tied to validations/behavior>
Validation:
- <repeatable commands, fastest first>
Progress scope:
- <pathspecs that should change>
Source of truth (optional):
- <paths/urls>
Recommended model: <gpt-5.3-codex|gpt-5.2-codex|...>
Reasoning effort: <medium|high|xhigh>
Risk profile: <low|medium|high> (why)
Suggested runner flags:
--autonomy-level <l0|l1|l2|l3>
--sandbox <read-only|workspace-write> (only if overriding default)
--model <model> (only if overriding)
--profile <profile> (optional)
--max-iterations <n>
--max-consecutive-failures <n>
--max-stagnant-iterations <n>
--progress-scope "<pathspec>" (repeatable)
--idle-timeout-seconds <n>
--hard-timeout-seconds <n>
--timeout-retries <n>
--events-format both
--progress-artifact
--validate-cmd "<command>" (repeatable)
```

### Suggested Output Section (Optional)

If the user answered `yes` to the suggested-output question, append a final section:

- Keep it non-restrictive.
- Do not conflict with Ralph’s schema-based completion contract.
- Prefer guidance like what to include in `evidence` (tests run, files changed, key decisions) over rigid report formats.

## References

Load these as needed:
- `references/prompt-improver-principles.md`
- `references/openai-codex-prompting-2026.md`
- `references/ralph-flag-selection-matrix.md`
