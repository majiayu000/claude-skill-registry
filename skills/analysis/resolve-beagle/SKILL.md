---
name: resolve-beagle
description: "Use as the follow-up to brainstorm-beagle when a spec has an Open Questions section (or quietly carries latent gaps) that need closing before planning or implementation can begin. Triggers on: \"resolve the open questions\", \"close the gaps in this spec\", \"research the open items\", \"finalize my spec\", \"make this spec implementation-ready\", \"answer the TBDs\". Also triggers whenever the user points at a brainstorm-beagle spec and asks for research, proposals, or answers to unresolved items. Orchestrates parallel research subagents when available (falls back to inline sequential research otherwise), proposes answers one at a time for user approval, then rewrites the spec in place so it arrives at planning with no known gaps. Does NOT write code, design implementation, or create plans — it only produces a complete spec."
---

# Resolve: Close Spec Gaps

Take a spec produced by `brainstorm-beagle` and close its remaining gaps — both the explicit Open Questions and the latent ones the self-review missed — by researching, proposing answers, and rewriting the spec in place.

The terminal state is a spec with no known open questions and no placeholder requirements. Planning can start immediately after.

<hard_gate>
This skill does not write code, scaffold projects, design architecture, or create implementation plans. It only edits the spec document. "Answering an open question" means proposing a WHAT/WHY answer with rationale — never a HOW. If a question turns out to require implementation design, defer it with a note and move on.
</hard_gate>

## Gates (pass before next step)

Objective pass conditions so steps are not skippable by assertion alone:

1. **Spec located** — The target file path is known and `Read` succeeds (or the user supplied a valid path after you listed 3–5 recent `docs/specs/` candidates).
2. **Gap list published** — One message lists every explicit Open Question bullet **and** each latent gap you will treat as in-scope. **Do not dispatch research** until the user adjusts the list (add/remove/defer) **or** explicitly tells you to proceed with that list.
3. **Research artifact per gap** — Before you present a proposal for gap *G*, you have a structured note for *G*: recommended answer, 1–2 rejected alternatives with reasons, and evidence (file:line, URL, or in-spec citation). No proposal without that artifact.
4. **One proposal queue** — Do not open the next gap’s proposal until the current gap has a clear outcome (accepted, revised wording applied, rejected with what happens next, or deferred with reason).
5. **Rewrite reconciled** — After editing, you read the full spec once and resolve cross-section contradictions; then run the self-review checklist from `../brainstorm-beagle/references/spec-reviewer.md` with failures fixed in-session unless the user opts for a follow-up pass.
6. **Commit** — No `git commit` unless the user answered yes to the commit prompt in § Committing.

## Workflow

1. **Locate the spec** — explicit path from the user, or the most recent file in `docs/specs/`
2. **Extract gaps** — parse Open Questions *and* audit for latent issues (placeholders, vague requirements, missing rationale, contradictions)
3. **Show the gap list** — present everything you plan to close in one summary so the user can add or remove items before research starts
4. **Dispatch research** — one task per gap, in parallel via subagents when available; otherwise sequentially inline
5. **Propose answers** — one proposal at a time, with recommendation + alternatives + evidence
6. **Rewrite the spec in place** — migrate resolved items to the right sections; nothing silently dropped
7. **Self-review** — same checklist `brainstorm-beagle` uses (see `../brainstorm-beagle/references/spec-reviewer.md`)
8. **Ask about committing** — prompt the user whether to commit the edit; don't commit unprompted

```
Locate spec → Extract gaps → Show list ──→ User adds/removes
                                          → Dispatch research (parallel if possible)
                                          → Propose answers (one at a time)
                                                → User decision → next
                                          → Rewrite spec in place
                                          → Self-review (fix inline)
                                          → Ask about committing
```

## Locating the spec

If the user gave a path, use it.

Otherwise, list the 3–5 most recently modified files in `docs/specs/` and ask: "Work on `<most recent>`, or another one?" Don't scan the whole directory tree — specs are top-level per `brainstorm-beagle`'s convention.

If no spec directory exists, ask the user for the path.

## Extracting gaps

Two categories count as gaps:

**Explicit gaps** — every bullet under the spec's `Open Questions` heading is one research task.

**Latent gaps** — issues that slipped past the brainstorm's self-review. Scan the spec for:

| Problem | What it looks like |
|---------|-------------------|
| Placeholder | TBD, TODO, "to be determined", ellipsis used as content |
| Vague requirement | "fast", "simple", "good", "user-friendly", "intuitive" — nothing to verify against |
| Missing rationale | Constraint or Out-of-Scope item with no "why" |
| Contradiction | Requirement conflicts with another requirement, with a constraint, or with Out of Scope |
| Untestable success | No observable way to verify the requirement was met |
| Implementation leakage | A requirement prescribes HOW instead of describing WHAT |

The reason to treat latent gaps as first-class: a spec that says "fast" or "good UX" hasn't been answered just because nothing was explicitly flagged. Planning will trip over those same words. Close them here.

Before dispatching research, show the combined list to the user in one message — "here's what I'm planning to close" — and let them add, remove, or defer items. Don't ask permission one-by-one; that's the proposal step.

## Dispatching research

Each gap gets exactly one research task. Classify each task first — the type determines which tools the research needs:

| Task type | Looks like | Tools |
|-----------|-----------|-------|
| Codebase pattern | "How does the existing `--start-at` pattern work?" "Where is `SKILL_MAP` defined?" | Grep, Glob, Read |
| External / API | "What does the Claude SDK expose for sub-agent spawning?" "Does Codex have hooks?" | WebSearch, WebFetch, Context7 (if available) |
| Design tradeoff | "What should the merged report format be?" "How should deduplication work?" | Reasoning + analogous reference points already in the spec |
| Scope / policy | "Should config/docs files route to a stack or fallback?" | Reasoning tied to the spec's own Core Value and Constraints |

### With subagents (preferred)

When the Task tool (or equivalent subagent tool) is available, dispatch each research task as an independent subagent — **all in the same turn**, so they run in parallel. Each subagent gets its own context window, which matters: gaps often come with large supporting context (the spec, the codebase) that you don't want crammed into a single conversation.

See `references/subagent-prompts.md` for the prompt templates (one per task type).

The research return must be structured: recommended answer, 1–2 alternatives with why rejected, and concrete evidence (file:line citations, URLs, or references to existing spec sections). Cap each return at ~300 words — you want decisions, not transcripts.

### Without subagents

If no subagent tool is available, do the research yourself, one question at a time. Work in cheapest-first order: codebase questions, then external, then tradeoffs, then scope/policy. Produce the same structured proposal for each. This is slower but never leaves gaps unresolved.

## Proposing answers

Present proposals **one at a time**. For each:

- **The gap** — restated in one line
- **Recommended answer** — your best call, with WHY
- **Alternatives** — 1–2 credible options and why they were rejected
- **Evidence** — file:line citations, URLs, or references to decisions already in the spec

The user can accept, revise, or reject. Follow the thread if they want to discuss; move on once decided.

**Order matters.** Resolve in this rough sequence:

1. Codebase-reality gaps first (they may inform design tradeoffs)
2. Policy/scope gaps second (they shape everything downstream)
3. Format/presentation gaps last (they depend on the above)

When a gap can't be resolved without input only the user has (budgets, stakeholder preferences, unstated constraints), don't guess — ask directly. It's cheaper than proposing the wrong answer and unwinding it.

## Rewriting the spec

As decisions land, migrate them to where they belong:

| Gap type | Destination after resolution |
|----------|-----------------------------|
| Architectural or policy decision | New entry under **Key Decisions** (with alternatives considered) |
| Concrete behavior | New entry under **Requirements** (assigned must/should/out-of-scope) |
| Hard limit | New entry under **Constraints** (with rationale) |
| External reference discovered during research | New entry under **Reference Points** |
| Vague requirement replaced | Rewrite the existing requirement inline; do not duplicate |
| Intentionally deferred | Stays in **Open Questions** with a `deferred: <reason>` suffix |

Two rules that matter:

- **Never silently drop an Open Question.** Either resolve it, migrate it with rationale, or explicitly defer it with a reason. Dropping a question without a trail is how specs regress between sessions.
- **Rewrite the whole spec, not just the touched sections.** Changes ripple: a new Key Decision may contradict an old Requirement, a resolved Open Question may invalidate a Constraint. Read the spec end-to-end after edits and reconcile.

## Self-review

Run the checks from `../brainstorm-beagle/references/spec-reviewer.md`:

- No placeholders
- No contradictions
- No implementation leakage
- All requirements testable
- Constraints and Out-of-Scope items have rationale

Fix anything that surfaces inline before handing back to the user. If new gaps appear during the rewrite (they sometimes do), add them to a "new gaps surfaced" list and ask the user whether to resolve them now or leave for a later pass.

## Committing

After the rewrite, summarize and ask:

> "Spec updated. Resolved N explicit questions and M latent gaps. Want me to commit this as `docs: resolve open questions in <topic> spec`?"

If yes, commit. If no, leave the working tree for the user. Do not commit unprompted — the user may want to review the diff first or bundle it with other changes.

## Key Principles

- **Close the loop.** The goal is a spec with nothing unanswered that blocks planning. Half-resolved is worse than clearly deferred.
- **One research task per gap.** Don't blur tasks together — it makes the proposal step harder to review and weakens the evidence trail.
- **Evidence over opinion.** Every proposal cites something — a file, a URL, or an existing spec decision. "I think" is not enough.
- **Still WHAT, not HOW.** Answers land as decisions in the spec, not as implementation designs. If an answer requires implementation thinking, defer it.
- **Defer honestly.** A question too expensive to answer now stays an Open Question with a one-line reason. Better to admit a known gap than paper over it.
- **Parallelize when you can.** Subagents run in isolation — fan out aggressively. Sequential research is the fallback, not the default.
- **Don't interrupt unnecessarily.** Show the gap list once, then only stop the user for decisions that need human judgment.
