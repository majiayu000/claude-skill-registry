---
name: give-plan
description: "Use when the user wants a written, reviewable plan or spec produced before coding starts. Triggers on: mapping out changes without implementing, thinking through risks of upgrades or migrations, evaluating approaches before committing to one, writing specs for team review, phasing work into stages, or any request that explicitly defers coding ('don't implement yet', 'before we build'). The distinguishing signal is that the user wants a plan artifact — not implementation, not a conversational answer. MUST activates inside Claude's native plan mode to have a better planning behavior."
argument-hint: what-to-plan
---

ultrathink

## Core contract

Figure out the right approach, write a plan the user can inspect, and **stop**. Planning is not approval to implement — wait for explicit go-ahead before writing any code.

- Clarify only what would materially change the plan.
- Read the codebase before making claims. Distinguish confirmed facts, inferences, and unknowns — never hide uncertainty.
- Optimize for reviewability over momentum.

If already in native plan mode, this skill shapes *how* to plan; plan mode provides the workflow structure and must follow this skill guidelines.

## Process

Check conversation context and skip completed steps.

### 1. Clarify the planning goal
What kind of plan? Scoped implementation, phased feature, migration/rollout, architecture decision, or spec artifact. Ask only the questions that matter.

### 2. Ground in evidence
Read relevant files and search the codebase before proposing changes. Be explicit about what's confirmed from code vs. inferred vs. unknown.

### 3. Choose the right altitude
- **Small change** → concise plan with touchpoints and validation
- **Multi-file feature** → phased plan with dependencies
- **Architecture choice** → options, tradeoffs, recommendation
- **Migration / rollout** → sequencing, rollback, validation checkpoints

Don't force every request into the same template.

### 4. Write the plan (right-size the artifact)
Match artifact to plan size — don't force `plans/*.md` on small scoped changes.

- **Inline prose** — small single-file tweaks, quick scoped edits, brief decisions. Present the plan in the response and stop.
- **`plans/YYYYMMDDHHMMSS-{plan-name}.md`** — multi-file features, migrations, architecture decisions, anything that benefits from review or history.
- **`plans/YYYYMMDDHHMMSS-{plan-name}/plan.md` + phase files** — large multi-phase work where each phase warrants independent reading/editing.

Use `date +%Y%m%d%H%M%S` for timestamps.

A strong plan covers: problem summary, recommended approach, phases/workstreams, affected files/modules/systems, dependencies and sequencing, validation strategy, risks and mitigations, assumptions and open questions, non-goals when useful.

### 5. Present and stop
Summarize the recommendation, call out risks/assumptions/unknowns, clarify what needs user confirmation, then wait. Do not drift into coding.

## Boundaries

- **Prose, not code** — describe *what* changes in prose (name the file, the concept); never include executable syntax (function bodies, JSX, SQL, migration scripts, shell commands). "Illustrative" snippets are still implementation code.
- **Right-sized artifacts** — don't force heavyweight structure onto small work; don't leave plans so abstract they name no touchpoints or validation path.
- **Every plan needs a validation path** — how will you know the implementation succeeded?
- Name concrete files, interfaces, and systems where possible. Surface tradeoffs instead of hiding them.

## Request

<request>$ARGUMENTS</request>
