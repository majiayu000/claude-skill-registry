---
name: quick-plan
description: "Use when you need a bite-sized, TDD-driven implementation plan but do NOT have a brainstorm-beagle spec to plan against. quick-plan reconstructs intent from the current conversation, fans out domain-expert exploration subagents across the codebase, and synthesizes the same plan format write-plan produces — without requiring `.beagle/concepts/<slug>/spec.md`. Triggers on: \"quick plan\", \"plan this out\", \"plan what we just discussed\", \"turn this into an implementation plan\", \"plan this without a spec\", \"I don't have a spec, just plan it\", \"write-plan but no spec\". Make sure to use this skill whenever the user wants an implementation or TDD plan and there is no spec to plan against — even if they just say \"plan it\" after discussing a feature. Writes to `.beagle/plans/<slug>/plan.md`. If a finalized spec already exists at `.beagle/concepts/<slug>/spec.md`, prefer write-plan. Does NOT brainstorm specs, write code, or execute the plan — produces the plan document (and an optional handoff prompt) only."
---

# Quick Plan: Conversation Into Implementation Plan

Turn the work already discussed in this session into the same comprehensive, TDD-driven implementation plan [write-plan](../write-plan/SKILL.md) produces — but without a spec. An engineer (or downstream agent) can execute it task-by-task without re-deriving intent.

The output is a single markdown plan at `.beagle/plans/<slug>/plan.md`. The plan captures HOW — file structure, task decomposition, exact tests, exact commands. Because there is no spec, quick-plan also captures the WHAT and WHY *inside* the plan, in an **Intent** header it synthesizes from the conversation and verifies before locking.

## What Replaces the Spec

write-plan leans on a reviewed spec for three things. quick-plan reconstructs each, because skipping them is how plans bake in unexamined assumptions:

| The spec gives write-plan… | quick-plan reconstructs it from… |
|---|---|
| **WHAT / WHY** (requirements, core value, out-of-scope) | The **conversation** — what the user has been asking for, correcting, and ruling out this session — distilled into an **Intent Brief**. |
| **Key Decisions** (vetted architectural choices) | **Fanout domain-expert subagents** that recommend an approach grounded in this codebase's real patterns and the stack's idioms. |
| **Reference Points** (analogous existing code) | The same fanout subagents, returning `file:line` analogs the plan mirrors. |
| **A human-reviewed gate** | A **gap check**: proceed silently when the conversation is unambiguous; ask the user targeted questions only where intent has real holes. |

The spec is a contract written *before* planning. quick-plan writes that contract *during* planning, from cheaper signals, and confirms only the load-bearing parts with the user. Everything downstream of the Intent Brief — task decomposition, TDD discipline, the recoverability test, the self-review gates — is **identical to write-plan**. Same output, different front-half.

## Workflow

Complete these steps in order:

1. **Reconstruct intent** — distill the conversation into an *Intent Brief* (goal, must-haves, constraints, out-of-scope, any approach signals). See *Reconstructing Intent*.
2. **Gap check** — decide whether the Brief is solid enough to plan. Proceed silently if unambiguous; ask targeted questions only for real holes. See *Gap Check*.
3. **Fan out exploration + experts** — dispatch parallel subagents, one per codebase region the plan will touch. Each is briefed as a domain expert and returns a file map, conventions, exact test commands, `file:line` reference points, and idiom/pitfall guidance. See *Fanout Exploration*.
4. **Read project conventions** — scan `AGENTS.md`/`CLAUDE.md` (root and nested) for testing tiers, comment policy, commit format, forbidden patterns the plan must respect.
5. **Design file structure** — map files to create/modify before writing any task.
6. **Decompose into tasks** — bite-sized (2-5 min) TDD steps with exact paths, tests, and commands — using write-plan's format exactly. See *Plan Format*.
7. **Self-review** — run the checklist (intent coverage, placeholders, discriminating assertions, spike/parallel gates). See *Self-Review*.
8. **Present draft to user** — show the full draft in chat; iterate on request.
9. **Write to disk** — save to `.beagle/plans/<slug>/plan.md` only after explicit approval, then offer the execution handoff.

```text
Reconstruct Intent Brief from conversation
        ↓
Gap check ── real holes? ── Yes → ask targeted questions → fill Brief
          └──────────────── No  → proceed silently
        ↓
Fan out exploration + expert subagents (parallel)  ─┐
Read project conventions (AGENTS.md / CLAUDE.md)   ─┘→ merge findings into Brief
        ↓
Design file structure → Decompose into TDD tasks
        ↓
Self-review → fix inline
        ↓
Present draft → User review
               ├─ Changes? → Revise
               └─ Approved? → Write to .beagle/plans/<slug>/plan.md
```

**The terminal state is a written plan.** quick-plan does not execute the plan, run tests, or modify production code. After writing it asks whether to generate an execution handoff prompt via the **subagent-prompt** skill ([../../../beagle-core/skills/subagent-prompt/SKILL.md](../../../beagle-core/skills/subagent-prompt/SKILL.md)).

## Reconstructing Intent

The conversation is the raw material the spec would otherwise be. Mine it before doing anything else, and write the result down — the Intent Brief is the contract the plan plans against, so it must be explicit, not held in your head.

Pull from the **whole session**, not just the last message: the feature asked for, behaviors described, corrections the user made ("no, it should…"), examples or error logs pasted, things explicitly ruled out, and any tech/library named. A correction the user made three messages ago is a requirement; treat it like one.

Draft the Intent Brief with these fields. This becomes the plan's **Intent** header verbatim:

- **Goal** — one sentence: what this builds and the value it delivers.
- **Must-haves** — the observable behaviors that define "done." Each must be specific enough to write a test against.
- **Out of scope** — what the user ruled out or what you're deliberately deferring. Without a spec, scope creep is the main failure mode; name the boundary.
- **Constraints** — tech stack, libraries, performance/compatibility limits the conversation pinned.
- **Approach signals** — any HOW the user already expressed a preference about (and, after fanout, the expert-recommended approach with its rationale — this is the spec's *Key Decisions* equivalent).
- **Open questions** — anything the conversation left genuinely ambiguous (feeds the gap check).

If the conversation is too thin to fill **Goal**, **Must-haves**, and **Out of scope** at all, quick-plan is premature — the work hasn't been thought through enough to plan. Say so and offer [brainstorm-beagle](../brainstorm-beagle/SKILL.md) to shape it first, rather than inventing requirements to fill the gaps.

## Gap Check

You have no reviewed spec, so you are the only check on whether the reconstructed intent is real or invented. After drafting the Brief, look at it with fresh eyes and ask: *would two reasonable engineers build materially different things from this?*

**Proceed silently** when the conversation already pins the answer — don't re-ask what the user just told you. Re-litigating settled intent is the fastest way to make a "quick" plan feel slow.

**Ask targeted questions** only for holes that would change the plan's shape:
- A must-have whose acceptance criteria are genuinely ambiguous ("notify the user" — how? in-app, email, both?).
- A scope boundary the user never drew, where guessing wrong wastes whole tasks.
- A fork in approach the conversation didn't settle and the fanout can't resolve from existing patterns.
- A load-bearing assumption about data shape, an external contract, or tool behavior that, if wrong, invalidates tasks.

Ask these as a short batch, not a drip. Anything you can answer yourself by reading the code, resolve in fanout — don't spend a user question on it. Record what you assumed (not asked) in the plan's Assumptions block so a future reader sees the decision.

## Fanout Exploration + Domain Experts

This is what lets quick-plan match write-plan's rigor without a spec: instead of one sequential read of "relevant code," dispatch **parallel subagents that are both explorers and domain experts** for the area they own. They reconstruct the spec's *Reference Points* and *Key Decisions* from the actual codebase.

**Scope the fanout to the regions the plan will plausibly touch** — one subagent per cohesive area (a subsystem, a layer, a directory, an integration point). Two or three is typical; don't shard so finely that agents trip over each other or so coarsely that one agent owns the whole repo. If the task is a one-file change, skip the fanout and explore inline — the dispatch overhead isn't worth it.

Each subagent is briefed as a senior expert in that area's stack and returns a compact structured report: file map, conventions, exact test command(s), `file:line` reference points to mirror, idioms, pitfalls, and a recommended approach with risks. The full dispatch template is in [references/fanout-brief.md](references/fanout-brief.md) — read it before dispatching.

**If the agent environment supports subagents**, dispatch them in parallel (one message, multiple tool calls) and pass paths, not file contents. **If it does not**, run the same briefs inline and sequentially — identical questions, identical structured output, just slower. Either way, fold every report into the Brief: reference points become the analogs your behavior contracts point at, recommended approaches become **Approach signals**, and surfaced pitfalls become spike candidates or named bug-class tests.

**Reconcile, don't rubber-stamp.** Experts disagree and codebases contradict their own conventions. When two reports conflict, or an expert's recommendation fights an existing pattern, surface it — as a gap-check question if it changes the plan's shape, or as a recorded Assumption if you can resolve it. An expert recommendation that contradicts a load-bearing comment in the code is an assumption-audit item, not a given.

## Plan Format

The plan document — header, file structure, task blocks, TDD steps, self-review outcome — uses **write-plan's template exactly**: [../write-plan/references/plan-template.md](../write-plan/references/plan-template.md). Read it; it is the single source of truth for the output shape, so the two skills never drift apart.

**One override:** quick-plan has no spec to link, so replace the template's `> **Source spec:** …` header line with the synthesized **Intent** block:

```markdown
# [Feature Name] Implementation Plan

> **Source:** Reconstructed from conversation via quick-plan (no spec). Intent captured below.
> **For downstream agents:** Execute task-by-task. Each task uses `- [ ]` checkboxes. Do not skip the test-first steps — they catch wiring bugs that pure-logic tests miss.

**Goal:** [Intent Brief → Goal]

**Architecture:** [2-3 sentences — the approach, informed by the fanout experts' recommendation]

**Tech Stack:** [from Intent Brief → Constraints]

## Intent
- **Must-haves:** [bulleted, each testable]
- **Out of scope:** [bulleted boundaries]
- **Approach decisions:** [the chosen HOW + one-line rationale, citing the expert reasoning — this is the Key-Decisions equivalent]

---
```

The **Intent** block is load-bearing, not decoration: it is the contract this plan was built against. A future reader (or executor agent) has no spec to fall back on — the plan must stand completely alone.

Everything else — the `## Assumptions`, `## Patterns`, `## File Structure`, `## Task N` blocks, and `## Self-Review Outcome` — follows the template unchanged.

### TDD and Contract Discipline (inherited from write-plan)

quick-plan produces the *same* plans, so the same discipline applies. These are the load-bearing rules; write-plan's [SKILL.md](../write-plan/SKILL.md) carries the full rationale for each:

- **Bite-sized always** — 2-5 minute steps (write failing test → run it, see it fail → implement → run suite green → sweep → commit). Never bundle.
- **TDD by default** — a failing-test step precedes every implementation step.
- **Tests are the contract; impls are not.** Show real, exact test assertions + the call site (~15 lines, no seed-loop ceremony). For implementations, show a **behavior contract** — files touched + 3-5 bullets of new/changed behavior + a `file:line` **Reference** to the closest analog the fanout found. Do NOT pre-write implementation code; the executor writes it against the test under real signatures.
- **Assertions pin observable consequence** — a value, a row, a written file, the output the next call sees — never dispatch ("the handler was called").
- **Recoverability test** — delete anything the executor can recover by reading the referenced file. Verbosity is not specificity. References point (`file.ext:line-line`), they never paste.
- **Reuse scaffolding** — grep for an existing helper/fixture/mock before inventing one; if none fits, name the one considered and why.
- **Failure-propagation policy is non-optional** — every new fallible op (serialize/parse/convert/open/connect) states how its error propagates. `.unwrap_or(<plausible fallback>)` without explicit rationale is a bug class.
- **Sweep on the way out** — every modify-file task ends by removing orphaned comments, unused imports, and dead helpers in the files it touched (targets named in plain language, not line numbers).
- **DRY repetition with Patterns** — a transformation across 3+ sites is named once in a `Patterns` section; each task still owns its files, test, and commit. Patterns applied across N sites get a final `Audit` task.
- **No placeholders** — no TBD/TODO, no "add validation" without naming which rules, no "similar to Task N." A behavior contract is the deliberate exception: specific contract, not vague verbs.

### Spike and Parallel-Implementation Gates (stricter here)

These two gates from write-plan matter **more** without a spec, because no reviewed Key Decision stands behind the plan's assumptions:

- **Spike before plan-lock.** Any claim of the form "tool X does Y" or "input arrives in shape Z" that neither this repo nor the conversation has verified gets a `Task 0: Spike <claim>` — run the canonical command against this repo, capture real output, confirm or revise before other tasks run. Reconstructed intent has *more* unverified claims than a vetted spec, so scan hard for them.
- **Parallel-implementation gate.** If the plan adds a second backend/platform/adapter behind an existing interface, the final task runs the canonical contract suite against **both** and asserts byte-identical observable behavior. Non-optional.

## Self-Review

After drafting the plan, look at the Intent Brief with fresh eyes and check the plan against it. Same checklist as write-plan, with **intent coverage** standing in for spec coverage:

| Dimension | What to check |
|-----------|---------------|
| **Intent coverage** | Every must-have in the Intent Brief maps to a task. Every task traces back to a must-have or a fanout finding — nothing invented. List any gap. |
| **Scope discipline** | No task drifts into something the Brief marks out of scope. Without a spec, this is the easiest line to cross — cut creep. |
| **Placeholder scan** | No TBD/TODO/"handle errors"/vague verbs. Fix inline. |
| **Type consistency** | Names, signatures, and types match across tasks (`clearLayers()` vs `clearFullLayers()` is a bug). |
| **Test discipline** | Every behavior-changing task has a failing-test step before its implementation step. |
| **Discriminating assertion** | For each test, name a plausible broken/no-op impl that still passes it. If one exists, the assertion is on the wrong target — move it to the region the bug corrupts. |
| **Consumer check** | Every new public surface (trait method, exported fn, endpoint, CLI flag) has a named **production** consumer in this plan — a test is not a consumer. Cut dead surface. |
| **Spike candidates** | Every unverified "tool X does Y" / input-shape claim has a `Task 0` spike, or the Brief is revised. |
| **Parallel-implementation gate** | Second backend/adapter behind an interface → final contract-equivalence task present. |
| **Failure-propagation** | Every new fallible op's contract names its error policy. |
| **Project conventions** | Plan respects AGENTS.md/CLAUDE.md — test tiers, comment policy, commit format. |
| **Open questions closed** | Every Intent Brief open question is resolved — answered by the user, by fanout, or recorded as an Assumption. None left dangling. |

Fix issues inline. Advance only when every item is honestly *yes*.

## Draft Review

Before writing to disk, present the draft in chat:
- The full plan markdown, end-to-end, including the Intent block.
- The assumptions you made (especially anything you chose rather than asked).
- The list of files the plan will create or modify.
- A one-line note on what the fanout experts recommended and why.

If the user requests changes, revise inline and present again. Do not write to disk during this loop.

## Writing the Plan

**Pass before creating or overwriting `plan.md`:** Do not write until both are true.

1. **User gate** — the user explicitly approved the draft or directed you to save it. Vague enthusiasm is not approval.
2. **Path gate** — target path finalized: default `.beagle/plans/<slug>/plan.md`.

- **Default path:** `.beagle/plans/<slug>/plan.md` (note: `plans/`, a sibling to `concepts/` — quick-plan output is not spec-derived).
- **Slug source (in order):** user-supplied slug/path → a short kebab-case slug inferred from the dominant topic of the conversation → ask the user to name it if ambiguous.
- If the user explicitly asks to commit: `docs: add <slug> implementation plan`.
- After writing, tell the user:
  > "Plan written to `.beagle/plans/<slug>/plan.md`. Review it on disk and let me know if you want changes."
- Then ask exactly: **"Do you want a prompt to execute this plan in a new session?"**
  - **If yes:** load the **subagent-prompt** skill ([../../../beagle-core/skills/subagent-prompt/SKILL.md](../../../beagle-core/skills/subagent-prompt/SKILL.md)), naming the just-written `plan.md` as the source material so its task-decomposition gates resolve from the plan without re-interrogating the user.
  - **If no:** tell the user the plan is ready and they can hand it off later via the **subagent-prompt** skill in a fresh session.
  - **If subagent-prompt is unavailable** (e.g. `beagle-core` not installed): instruct the user to invoke it themselves.
- Wait for the next instruction before considering work complete.

**Do not start executing.** quick-plan produces the plan (and optionally the handoff prompt); execution is a separate decision and a separate skill.

## Key Principles

- **Conversation is the contract source** — reconstruct intent from the whole session and write it into the plan's Intent block; the plan must stand alone with no spec behind it.
- **Confirm only the gaps** — proceed silently when intent is clear; spend user questions only on holes that change the plan's shape.
- **Fanout experts reconstruct Reference Points and Key Decisions** — parallel explore-and-advise subagents ground the plan in real code and stack idioms; reconcile their conflicts, don't rubber-stamp.
- **Same output as write-plan** — identical template, TDD discipline, recoverability test, and self-review gates; quick-plan only changes how the contract is sourced.
- **Spike harder** — reconstructed intent carries more unverified claims than a vetted spec; every "tool X does Y" or input-shape assumption gets a Task 0 spike.
- **Guard scope** — without a spec boundary, creep is the main failure mode; the Intent Brief's out-of-scope list is load-bearing.

## When This Skill Is Wrong For the Job

- **A finalized spec already exists** at `.beagle/concepts/<slug>/spec.md` → use [write-plan](../write-plan/SKILL.md); it plans against the vetted contract directly.
- **The conversation is too thin** to fill Goal + Must-haves + Out-of-scope → the idea isn't shaped enough to plan; route to [brainstorm-beagle](../brainstorm-beagle/SKILL.md) first.
- **A one-line fix, a single-file refactor, or a spike** → a full plan is overkill; tell the user to just do the work directly.
