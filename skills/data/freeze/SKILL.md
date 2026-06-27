---
name: freeze
description: Use when a pipeline stage or the human meets facts that live outside the repo — a service, database, queue, third party, or live logs — and the work depends on their current state. Triggers on "what's the state of", "check prod", "is the service returning", "snapshot the data", external-system dependencies. Repo-local work skips it.
---

Freeze the moving cross-boundary state a system depends on into one immutable snapshot. The consumer is the agent stages (intent / shape / delegate / builder), not the human's memory — grounding, not narration.

## Contract

- **INPUT** — a system to ground AND the work order (intent) that scopes which external facts matter. Doubly scoped: only the slice of the world this work order touches, never a general map.
- **GATE** — "Is the snapshot factual and complete — every required fact observed, or an explicit gap?" Agent audits, user locks.
- **OUTPUT** — a snapshot VALUE, emitted in conversation. Stateless: nothing persisted. Re-run to refresh.

## Observed-or-gap, never inference

A fact's VALUE is OBSERVED or it is a GAP. There is no third path.

- **Inference builds the source map only** — reasoning enumerates WHICH facts this system + intent depends on. It never produces a fact's value.
- **A value is observed** — a read-only acquisition agent sees it live, or the human retrieves it by hand.
- WRONG: infer a value from a config file, a stale doc, or "it's probably still X" and write it as a fact.
- RIGHT: unreachable fact → an OPEN gap with retrieval instructions, never a fabricated value.

The outcome is a uniformly factual snapshot: every line is something observed, or something named as missing.

## The snapshot

Two parts. Facts append; the belief derives.

- **OBSERVED facts** — each `{ source, claim, where-it-lives, as-of, observed-by }`.
- **OPEN gaps** — each `{ required-fact, why-needed, where-to-look, how-to-retrieve }`.
- **Derived view** — any map / belief over the facts is a VIEW, marked as derived, never mixed into the observed set. A consuming stage sees a complete factual picture or exactly which facts are still missing.

## The work loop

1. **Scope** — from the system + intent, infer the source map: the set of external facts this work order depends on. This is the only place inference runs.
2. **Acquire** — fan out read-only acquisition agents in parallel, one observation per fact, live. The skill spawns and folds; it never does the reads itself.
3. **Fold** — assemble each return into an OBSERVED fact. Anything unobserved becomes an OPEN gap with its retrieval instructions.
4. **Gap-fill** — surface gaps for the human to hand-retrieve; re-fold each return. Re-check. The loop terminates when no gaps remain OR the human stops.
5. **Gate** — run the gate audit (below).

## Acquisition is delegation-shaped

The skill is a router: it spawns acquisition agents and folds their returns. It does not read external systems directly — same law as delegate's "router does no work".

- **READ-ONLY is a hard guard** — acquisition agents observe, never mutate. No write, no POST that changes state, no migration, no toggle. An agent that would mutate an external system is the wrong tool; stop and make it a gap for the human.
- **Parallel by default** — independent facts go out as parallel agent calls in one message.
- **Self-contained prompts** — each agent gets the one fact to observe, where it lives, and the read-only constraint.

## Decision prompts

<!-- doc-gen FILE src=../prompts.md -->
- Auto-gather when the answer is retrievable with certainty: cheap local reads, docs, web research, parallel subagents. Return with decisions, not raw findings. Never ask the user something research already made obvious — that is a named stop condition.
- Only non-obvious judgment calls reach the user. Every such AskUserQuestion: exactly 3 candidate answers + 1 uniform escape hatch — "Gather facts" (research/explore). The hatch is a first-class option, never hidden behind Other.
- Re-entry after a detour: if the detour made the answer obvious, state the decision and proceed; otherwise re-ask the same question with the new evidence inside the prompt.
- Presentation rule: EVERYTHING the user needs to answer lives inside the question UI — question text, descriptions, previews. Never in prose before the tool call (the dialog hides it).
<!-- end-doc-gen -->

## The gate

"Is the snapshot factual and complete?" Agent audits, user locks.

- **Factual pass** — every OBSERVED fact traces to an observation (an agent return or a human hand-retrieval). Any value reached by inference is a defect: demote it to an OPEN gap or re-acquire it.
- **Completeness pass** — every fact in the source map is either OBSERVED or an OPEN gap. A required fact that is silently absent is the failure mode; name it as a gap.
- Present verdict-FIRST via AskUserQuestion: PASSES or FAILS, then the observed count and the open gaps — proof both passes ran.
- On FAIL: name exactly which facts are inferred or missing. Never fabricate a value to close a gap.
- The user locks. The lock is theirs, not yours.

## Convergence

The gap-fill cycle (observe → surface gaps → human hand-retrieves → re-fold → recheck) is human-gated, not autonomous. It has no metric and no unsupervised run, so it does NOT pass through target. It ends when gaps are closed or the human stops — a snapshot with named open gaps is a valid lock.

## Boundaries

- **On-demand, not mandatory** — any stage invokes freeze when it meets outside-the-repo facts. It is not a pre-intent stage; repo-local work skips it entirely.
- **freeze vs over** — freeze is world→pipeline grounding: acquire external facts, feed the agent stages. over is output→human handoff. Complements, never folded together.
