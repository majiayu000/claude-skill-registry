---
name: session-reflect
description: Capture session learnings and propose targeted improvements to docs, skills, or core agent instructions. Evidence-based only - no theoretical improvements. Closes the feedback loop directly by updating existing files.
---

# Session Reflect

Capture evidence-based learnings from the current session (or a clearly identified recent session) and propose targeted, atomic improvements to existing documentation, skills, or core instructions. There is no separate learnings store: improvements are applied directly to the best existing target(s).

This skill is a post-step that closes the loop after `/fact-find`, `/plan-feature`, `/re-plan`, and `/build-feature`.

## Operating Mode

**REFLECTION ONLY**

**Allowed:** read relevant files, analyze the session timeline, extract evidence, draft proposals, and (only if approved) update the target files.

**Not allowed:**

- Creating new "learnings" files or a parallel knowledge base
- Making any changes without explicit user approval
- Bundling unrelated improvements into a single proposal
- Speculative "best practice" additions without session evidence

## Inputs

At trigger time, establish the minimum context (without derailing the user):

**What session/workstream are we reflecting on?** (e.g., "the feature build we just completed", "the re-plan for TASK-07", "the briefing request")

**Where is the authoritative artifact?**

- Plan: `docs/plans/<feature-slug>-plan.md`
- Fact-find: `docs/plans/<feature-slug>-fact-find.md`
- Relevant skill: `.claude/skills/<skill>/SKILL.md`
- Core instructions: `CLAUDE.md`, `AGENTS.md`, etc.

If the session is ambiguous, ask one clarifying question to anchor it; otherwise proceed.

## When to Trigger (Semi-Automatic)

Prompt the user to run reflection when any of these occurred:

### Planning pipeline signals

- A task was forced into `/re-plan` due to <80% confidence.
- A build stop occurred due to confidence regression or unexpected blast radius.
- Plan task boundaries proved inaccurate (needed new files or new dependencies).
- Acceptance criteria or test plan was missing/insufficient and had to be invented mid-build.

### Execution signals

- A validation failure was non-obvious and required investigation.
- The agent made an incorrect assumption that the user corrected.
- A recurring pattern was rediscovered (re-learning).
- A "gotcha" or edge case caused rework or delay.

### Documentation/skill adequacy signals

- Skill instructions were followed but still led to wasted steps.
- The user asked for the same clarification more than once across sessions.
- Repo conventions were unclear and had to be inferred from history.

### Do not trigger

- Routine work that proceeded smoothly with no notable friction
- Pure preference changes without evidence of cost or error
- "Nice-to-have" ideas not tied to session outcomes

## Progressive Disclosure Layers

Use the smallest-layer change that solves the problem.

| Layer | Target | Appropriate learning types | Evidence standard |
|-------|--------|---------------------------|-------------------|
| **L0: Core** | `CLAUDE.md`, `AGENTS.md` | Cross-repo behavioral rules and invariants | Quantified impact + recurrence signal |
| **L1: Skills** | `.claude/skills/*/SKILL.md` | Procedure gaps, missing gates, unclear outputs | Specific skill gap + observed failure mode |
| **L2: Domain Docs** | `docs/**/*.md` (including `docs/plans/**`) | System behavior, gotchas, conventions, operational notes | Session evidence (files, errors, decisions) |

### Layer selection rules

- If the learning is only relevant to one command's workflow → L1
- If it's specific to a subsystem/module → L2
- Use L0 only when it reduces repeated failure across many tasks/features.

## Evidence Standards (Hard Requirements)

### Acceptable evidence (must include at least one per proposal)

Pick from:

**Quantitative cost:** minutes lost, number of retries, number of CI failures, number of re-plans, number of times user corrected behavior

**Concrete session artifacts:** failing command output, specific error message, impacted file paths, plan task IDs, decision points recorded, discovered dependency chain

### Format requirements

- L0/L1 proposals must include quantified impact (measured or explicitly estimated).
- L2 proposals must include session evidence (paths, errors, decision points).

### Not acceptable

- "Might be useful"
- "Best practice suggests"
- Theoretical edge cases not observed in the session

If you do not have enough evidence, do not propose. Instead:
- ask the user for the missing measurement ("Was this a 5-minute hiccup or a 45-minute derail?"), or
- defer entirely.

## Workflow

### 1) Identify

Describe succinctly:
- What happened (symptom)
- What was missing (root cause)
- What would have prevented it (proposed documentation/skill change)

### 2) Classify

Assign:
- Layer (L0/L1/L2)
- Target file path
- Change type: Add / Clarify / Strengthen Gate / Remove / Reorder

### 3) Draft (atomic proposals only)

Produce 1–3 proposals max per reflection run, each independently approvable.

If there are more than 3, prioritize by quantified impact and recurrence likelihood.

### 4) Present for approval (mandatory)

For each proposal, present a "proposal card" including:
- Layer and target
- Evidence (quantified and/or artifact-based)
- Current state (brief excerpt or summary; avoid long quotes)
- Proposed change in the exact target-file format
- Expected impact
- Risk of change (e.g., over-constraining, false positives)
- Approval question (Yes/No)

### 5) Apply or discard

**If approved:** update the target file(s) and show what changed (diff-style or clear before/after).

**If rejected:** do nothing persistent. Do not argue; optionally ask what would make it acceptable (one question max).

## Proposal Card Template

Use this exact structure when presenting changes:

```markdown
### REF-01: <short title>
- **Layer:** L1 (Skills)
- **Target:** `.claude/skills/<skill>/SKILL.md`
- **Change type:** Strengthen Gate
- **Evidence:**
  - Quantified: <e.g., "~25 minutes lost chasing failing tests caused by missing 'baseline check' step">
  - Artifacts: <e.g., "CI failure: <error>; discovered in TASK-04 build notes; files: ...">
- **Current state (summary):** <1–2 sentences>
- **Proposed change (draft):**
  <insert text block or diff-style snippet>
- **Expected impact:** <how it prevents recurrence>
- **Risk / tradeoff:** <what could get worse>
- **Approve to apply?** (Yes/No)
```

## Integration With the Planning Pipeline

When reflecting on work that involved your planning skills, prefer these targets:

- If the issue was unclear intent / insufficient initial user context → update `/fact-find` intake gates (L1).
- If the issue was task confidence inflation or missing evidence → update `/plan-feature` confidence rubric / evidence requirements (L1).
- If the issue was mid-build surprises → update `/build-feature` stopping conditions and preflight/baseline checks (L1).
- If the issue was tasks under-specified (missing acceptance/test/rollout) → update `/re-plan` plan-repair requirements (L1).
- If the issue was subsystem-specific (e.g., auth edge case) → update a domain doc (L2), and optionally reference it from the plan template.

## Anti-Patterns (Explicitly Forbidden)

- Proposing changes without session evidence
- Creating separate learnings files (e.g., `learnings.md`, `notes.md`, `postmortem.md`) that are not already part of the repo's established docs structure
- Bundling unrelated learnings into a single proposal
- Proposing L0 changes for subsystem/domain-specific issues
- Skipping user approval
- Turning reflection into new planning or implementation work

## Completion Messages

Use one of the following:

**If proposals were approved and applied:**
> "Reflection complete. Applied <N> approved improvement(s) to <targets>. No separate learnings files created."

**If proposals were presented but not approved:**
> "Reflection complete. Proposed <N> improvement(s); none applied due to lack of approval."

**If insufficient evidence:**
> "Reflection skipped. I do not have sufficient session evidence to justify a durable documentation/skill change."
