---
name: planning-workflow
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  Comprehensive markdown planning methodology for software projects. Use when
  starting a new project, creating implementation plans, or refining architecture
  before coding.
practices:
- pragmatic-programmer
---
<!-- TOC: Philosophy | THE EXACT PROMPT | Process Overview | References -->

# Planning Workflow — The Foundation of Agentic Development

> **Core Philosophy:** "Planning tokens are a lot fewer and cheaper than implementation tokens."
>
> The models are far smarter when reasoning about a detailed plan that fits within their context window. This is the key insight behind spending 80%+ of time on planning.

---

## Outcome — When This Skill Has Delivered

You have a usable plan when **all** of the following hold:

- The plan is **self-contained**: a fresh agent who has never seen the project can read it and start implementing without asking the human for clarification.
- It is **dependency-aware**: every non-trivial task names what blocks it and what it unblocks, so the work decomposes cleanly into a beads graph.
- It is **justified**: every architectural choice and every non-obvious feature has at least one sentence on *why*, not just *what* — future agents need the rationale to make consistent local decisions.
- It has survived **at least 4 review rounds** by a strong reasoning model (GPT Pro Extended Reasoning is the proven choice) and reached steady-state — i.e., the most recent round produces marginal rather than structural revisions.
- It has been **converted to beads** with the dependency graph intact, so implementation agents can pick up ready work via `br ready --json` without re-reading the plan.

You have NOT delivered if any of these is true: the plan is < ~1,500 lines for a non-trivial project (under-specified); the plan is > ~10,000 lines with no decomposition (impossible to act on); the human is still being asked "what should this do?" mid-implementation (planning was abandoned, not completed); beads exist but have no dependency edges (the plan's structure was lost in conversion).

## When NOT to Use This Skill

Reach for something else if:

- **The change is small and local** (one bug fix, one file, < ~200 LOC) → plan in chat or as a one-line TaskCreate; the planning overhead exceeds the implementation cost.
- **You are doing pure research** (investigating an unknown codebase, prototyping an idea) → use `codebase-archaeology` or `idea-wizard` first; planning is for execution, not discovery.
- **The architecture is dictated** (you are porting an existing system, following a spec, or implementing a well-defined RFC) → use `porting-to-rust` or `testing-conformance-harnesses`; the plan is the spec itself.
- **You're under a hard deadline that doesn't permit 80%-on-planning** (live incident, hotfix, security patch) → ship the fix, then retrofit the plan if the area needs further work.

## Grounding — Sources of Truth for Plan Decisions

When a planning model proposes architecture, the proposal is a hypothesis. Ground every load-bearing claim in a verifiable source before letting it survive a review round:

- **Library/framework choices:** read the actual current docs (latest stable version, not the model's training-time snapshot). If the model says "use X for Y," verify X still exists, is maintained, and supports Y in the version you'd install.
- **Existing-codebase claims:** for any plan that touches an existing project, the model's understanding of the project structure is suspect. Grep, `git log`, or use `codebase-archaeology` to confirm structural claims before they shape the plan.
- **Performance / scaling claims:** never accept a number ("handles 10k req/s," "loads in <100ms") without a citation or a planned benchmark. Bare numbers in plans are guesses dressed as facts.
- **Cost claims:** verify against the provider's pricing page at planning time; pricing models change. Pin the plan to the specific tier you priced against.
- **Cross-references to other skills/tools:** if the plan says "use `<tool>` for X," confirm the tool's current contract supports X. Linkrot in plans is a quiet failure mode.

A plan that survived review without grounding is a plan that will surprise you in implementation. Cheap verification at planning time beats expensive rework after the code is half-written.

## Validation Loop (between review rounds)

After each review round, before sending the plan back for another pass, run all four:

1. **Self-containment check** — pick the most obscure task in the plan, paste it alone into a fresh chat, and ask "is this implementable as written?" If no, expand.
2. **Dependency-graph check** — can you draw the DAG of tasks? Are there cycles? Are there orphans (tasks with no consumers)? Either is a planning bug.
3. **Justification check** — sample 5 random architectural decisions. Each must have a paragraph of *why*. If not, ask the planning model to add it.
4. **Steady-state check** — diff this round's plan against the previous round's. If the diff is large structural changes, you need another round. If it's typo-level polish, you're done.

If any of these fails, the plan is not ready for beads conversion — do another review round.

---

## Why Planning Matters

- **Measure twice, cut once** — becomes "Check your plan N times, implement once"
- A very big, complex markdown plan is still shorter than a few substantive code files
- Front-loading human input in planning enables removing yourself from implementation
- The code will be written ridiculously quickly when you start enough agents with a solid plan

---

## THE EXACT PROMPT — Plan Review (GPT Pro Extended Reasoning)

```
Carefully review this entire plan for me and come up with your best revisions in terms of better architecture, new features, changed features, etc. to make it better, more robust/reliable, more performant, more compelling/useful, etc. For each proposed change, give me your detailed analysis and rationale/justification for why it would make the project better along with the git-diff style change versus the original plan shown below:

<PASTE YOUR EXISTING COMPLETE PLAN HERE>
```

---

## THE EXACT PROMPT — Integrate Revisions (Claude Code)

After GPT Pro finishes (may take 20-30 minutes), paste output into Claude Code:

```
OK, now integrate these revisions to the markdown plan in-place; use ultrathink and be meticulous. At the end, you can tell me which changes you wholeheartedly agree with, which you somewhat agree with, and which you disagree with:

```[Pasted text from GPT Pro]```
```

---

## Process Overview

```
1. INITIAL PLAN (GPT Pro / Opus 4.7 in web app)
   └─► Explain goals, intent, workflows, tech stack

2. ITERATIVE REFINEMENT (GPT Pro Extended Reasoning)
   └─► 4-5 rounds of revision until steady-state

3. MULTI-MODEL BLENDING (Optional but recommended)
   └─► Gemini 3.1 Pro Deep Think, Grok4 Heavy, Opus 4.7
   └─► GPT Pro as final arbiter

4. CONVERT TO BEADS (Claude Code + Opus 4.7)
   └─► Self-contained tasks with dependency structure

5. POLISH BEADS (6+ rounds until steady-state)
   └─► Cross-model review, never oversimplify
```

---

## What Makes a Great Plan

| Good Plan | Great Plan |
|-----------|------------|
| Describes what to build | Explains WHY you're building it |
| Lists features | Details user workflows and interactions |
| Mentions tech stack | Justifies tech choices with tradeoffs |
| Has tasks | Has tasks with dependencies and rationale |
| ~500 lines | ~3,500+ lines after refinement |

### Essential Elements

1. **Self-contained** — Never need to refer back to external docs
2. **Granular** — Break complex features into specific subtasks
3. **Dependency-aware** — What blocks what?
4. **Justified** — Include reasoning, not just instructions
5. **User-focused** — How does each piece serve the end user?

---

## Common Mistakes

1. **Starting implementation too early** — 3 hours of planning saves 30 hours of rework
2. **Single-round review** — You continue to get improvements even at round 6+
3. **Not using GPT Pro** — Extended Reasoning is uniquely good for this
4. **Skeleton-first coding** — One big comprehensive plan beats incremental coding
5. **Losing context** — Convert plans to beads so agents don't need the original

---

## References

| Topic | Reference |
|-------|-----------|
| All exact prompts | [PROMPTS.md](references/PROMPTS.md) |
| Real-world examples | [EXAMPLES.md](references/EXAMPLES.md) |
| FAQ | [FAQ.md](references/FAQ.md) |
