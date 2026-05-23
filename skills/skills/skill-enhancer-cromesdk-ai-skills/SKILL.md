---
name: skill-enhancer
description: Upgrade existing agent skills end-to-end with deterministic edits, stronger trigger wording, cross-assistant portability hardening, and test coverage improvements. Use when users ask to update, fix, review, refactor, standardize, optimize, or harden any `SKILL.md` workflow and its companion files (`agents/openai.yaml`, `tests/scenarios.md`) for Codex, Claude, Gemini, and Cursor.
---

# Skill Enhancer

Strengthen existing skills through proactive technical review and targeted remediation, then deliver enterprise-grade, assistant-agnostic improvements by default.

Compatibility note:
- Treat `$skill-enhancer` as the primary trigger.
- Legacy prompts may still use `$codex-skill-enhancer`; handle them as migration-compatible aliases in documentation and tests.

## Mandatory reference policy

- Always find and use official sources from vendor documentation, standards bodies, or primary project documentation sites.
- Do not rely on forum-only or opinion-only sources when an official source exists.
- Load and follow `references.md` in this skill folder to select and report valid reference sources.
- Every final skill-enhancement output must include a `References` section with source title and URL.

## Workflow

### Step 0: Resolve scope and target (required)

Determine target scope before editing:
- If the user names a specific skill path, use it.
- If the user says "update this skill" while this skill is explicitly invoked, default target to this skill directory.
- If target is ambiguous, ask one precise clarification question.

Locate the target skill path. If missing, ask for it or search likely skill directories.

### Step 1: Confirm baseline (required)

Read at minimum:
- `SKILL.md`
- `tests/scenarios.md` (if present)
- `agents/openai.yaml` (required; create if missing)

Summarize the current state:
- Trigger quality (description precision and searchability)
- Workflow clarity (ordered, imperative, actionable steps)
- Portability (generic instructions not tied to one assistant)
- Test coverage (scenario breadth and edge cases)

### Step 2: Run proactive enterprise-grade assessment (required)

Do not ask "what to improve" as a default step. Instead, infer and address the highest-impact issues immediately.

Assess and prioritize:
1. Trigger precision and coverage in `description`.
2. Instruction actionability and deterministic workflow order.
3. Portability across Codex, Claude, Gemini, and Cursor.
4. Completeness of `agents/openai.yaml` alignment with current skill purpose.
5. Test scenario rigor, including hard and edge-case behavior.
6. Enterprise quality bar: clarity, consistency, verification gates, and low ambiguity.

Ask clarifying questions only when blocked by missing critical context (for example, missing target path or conflicting requirements).

### Step 3: Run assistant-agnostic technical analysis (required)

Evaluate against this checklist:
1. Name quality: lower-case slug, clear and stable intent.
2. Description quality: what + when to use, includes trigger terms.
3. Actionability: imperative steps, correct order, clear success checks.
4. Progressive disclosure: keep core workflow in `SKILL.md`, move detailed variants to references only when needed.
5. Scope discipline: single responsibility; avoid tool or platform overfitting.
6. Portability: avoid assistant-specific jargon unless paired with a generic equivalent.
7. Evaluation readiness: `tests/scenarios.md` exists and includes easy, hard, and edge-case scenarios.
8. Reference integrity: proposed changes are justified with official documentation links from `references.md` policy.

### Step 4: Gather official references (required)

Before editing files:
1. Identify which parts of the enhancement need external grounding (for example: authoring standards, YAML schema conventions, test design quality bars).
2. Find official documentation sources for those topics (product docs, standards docs, or primary project docs).
3. Record only relevant links that directly support the applied changes.
4. Avoid non-official sources unless no official source exists; if fallback is used, explicitly state why.

### Step 5: Present a prioritized enhancement plan

Use this format:

```markdown
## Enhancement Plan

### User-requested
1. [Observed issue] -> [Specific fix]

### Technical
1. [Standards issue] -> [Specific fix]

### Portability
1. [Cross-assistant risk] -> [Generic wording or workflow fix]
```

Prioritize user-requested items first, then technical, then portability refinements.

Create and maintain a TODO checklist from this plan before editing files. Track each item as:
- `[ ]` pending
- `[-]` in progress (only one at a time)
- `[x]` complete

Keep the TODO list updated as work progresses. Do not mark verification items complete until checks pass.

### Step 6: Implement enhancements

Apply changes in this order:
1. Fix `description` trigger clarity.
2. Rewrite weak workflow sections into imperative steps.
3. Remove assistant-locked phrasing and replace with generic instruction patterns.
4. Expand or repair `tests/scenarios.md` for realistic evaluation.
5. Write or update `agents/openai.yaml` so interface metadata matches the current skill behavior and trigger intent.

Preserve valid existing behavior. Avoid unnecessary restructuring.
Update TODO status after each completed change.

### Step 7: Verify quality gates

Confirm:
- Highest-impact enterprise-quality issues are explicitly addressed.
- Workflow is executable without hidden assumptions.
- Language is generic enough for Codex, Claude, Gemini, and Cursor.
- Scenario tests reflect real failure modes and expected behavior.
- `agents/openai.yaml` exists and is aligned with `SKILL.md` (display name, short description, and default prompt reflect current purpose).
- Final report includes official references backing the applied changes.

If available, run a validator for structural checks and fix any reported issues.
Complete the TODO list only when implementation and verification tasks are fully done.

## Output requirements

When reporting results, include:
1. What changed (files and high-impact edits)
2. Why each change matters
3. Remaining risks or follow-up improvements
4. Final TODO checklist snapshot
5. References (official sources only, title + URL)

## Tips

- Rewrite the `description` first. Trigger quality has the highest impact on whether a skill is discovered and used.
- Default to proactive remediation; ask questions only when essential context is missing.
- Replace vendor terms with role-based terms like "agent", "assistant", and "tooling" unless platform-specific wording is required.
- Favor one precise follow-up question over multiple broad questions to reduce turn overhead.
- Add at least one edge-case scenario whenever behavior changes, especially for missing paths or ambiguous scope.
- Treat `agents/openai.yaml` as a maintained contract, not optional metadata.
- Keep TODO items atomic; split large edits into smaller checkable actions.
- If a fix adds complexity, include a short verification check so future agents can confirm behavior quickly.
- Avoid expanding scope in one pass; finish the requested enhancement before proposing secondary refactors.

## Deterministic execution rules

- Prefer direct file edits over speculative recommendations when the user asks to "update" a skill.
- Keep edits minimal and traceable to observed issues from Step 1 and Step 2.
- Do not rename skill folders or files unless the user explicitly requests a rename.
- If companion files are missing, create them with minimal valid content aligned to the current skill purpose.
- If blocked, stop before partial rewrites and report the exact blocker plus one next action.
