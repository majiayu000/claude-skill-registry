---
name: deepline-engine
description: 'Build, publish, and verify a Deepline Play as a durable state machine over Customer DB tables, including a small paid pilot. Invoke this skill explicitly when the user asks to build an engine.'
disable-model-invocation: true
---

# Deepline Engine

## Quick Start

```bash
npm install -g deepline
# Fallback for secure sandboxes: mkdir -p "$HOME/.local" && npm config set prefix "$HOME/.local" && export PATH="$HOME/.local/bin:$PATH" && npm install -g deepline --registry https://code.deepline.com/api/v2/npm/
deepline auth register --wait auto
deepline auth wait --timeout 120 # completes Cowork/browser approval; no-op if already connected
deepline auth status
deepline -h
```

Build an engine from the state machine the user defines.

An engine is an orchestrator Deepline Play that accepts an input, determines its state, calls the transition Play for that state, and produces a new state. The durable data plane lives in Customer DB: every state has an input table and an output table. The output of one transition can become the input to the next state.

The user owns the states, transition rules, transformations, and terminal behavior. This skill owns the reusable structure for turning those decisions into a replay-safe Play. Infer routine names, schemas, advancement behavior, and implementation details from the request and repository conventions. Ask only when missing information would force the engine to invent substantive business policy or create an unsafe side effect. Do not import an outbound workflow, GTM recipes, provider choices, or domain-specific policy unless the user asks for them.

## Core model

For each state, define:

| Part            | Meaning                                                                             |
| --------------- | ----------------------------------------------------------------------------------- |
| Input table     | Rows waiting to be handled in this state                                            |
| State decision  | The user-defined rule that establishes the row's current state                      |
| Transition Play | The child Play that performs the transformation for this state                      |
| Output table    | The input, result, transition status, and next state                                |
| Next input      | The row admitted to the next state's input table, unless the transition is terminal |

Keep the state decision explicit. Inferring state from incidental fields creates transitions the user did not define and makes replay behavior hard to explain.

## Workflow

1. **Capture the state machine.** Extract the states, initial state, terminal states, allowed transitions, state-decision rules, and transformation for each state from the request and available project context. Resolve routine omissions with explicit, reported assumptions. Ask only when competing interpretations would materially change business behavior.
2. **Define row identity.** Choose the stable business key and a transition idempotency key. A retry must address the same row and transition instead of creating a second result.
3. **Define the tables.** Give every state an input table and an output table in Customer DB. Infer clear names and domain columns from the state machine and repository conventions. Record the structural fields needed to connect an input, its result, and the next state.
4. **Choose a durable source directory.** Generate the engine under a maintained project directory inferred from repository conventions. Keep the orchestrator, new child Plays, shared types, README, and Mermaid diagram together as project source. Do not use an ignored `tmp/` scaffold; temporary paths hide work from version control and make the engine disposable.
5. **Resolve every transition Play before authoring one.** Search callable Plays visible to the user's workspace with `deepline plays search "<transition outcome>" --all --json`. Inspect owned and prebuilt candidates with `deepline plays describe <name> --json`. Reuse an exact contract match; names are only hints, so verify input, output, and inline-composition compatibility. If no candidate fits, author one new Play for that transition instead of embedding its transformation in the orchestrator.
6. **Author the orchestrator Play.** Use `definePlay(name, handler, options)`. Determine the state, select the matching transition Play, and call it through `ctx.runPlay(...)` with a stable key. The orchestrator owns state routing and Customer DB persistence; transition Plays own transformations.
7. **Persist the transition.** Materialize the accepted input, the child Play result, `from_state`, `to_state`, status, error or miss information, timestamps, workflow version, transition Play identity/version, and idempotency key. If the transition continues, write the next state's input idempotently.
8. **Choose the advancement model.** Infer one transition per invocation or multiple transitions per invocation from the workflow. Default to multiple transitions through terminal completion when no external event must occur between states. Record the choice and its retry and observability implications instead of pausing for confirmation.
9. **Validate every edge.** Check every new transition Play and the orchestrator. Before the paid-pilot gate, use static checks and provider-free fixtures to test each allowed transition, each terminal state, an invalid or unknown state, a child Play failure, an invalid state returned by a child, and replay of a completed transition. Defer every provider-executing edge test to the bounded pilot after caps and workspace authorization are verified.
10. **Publish and verify.** After checks pass, publish new child Plays in dependency order, check the orchestrator against their live contracts, publish it, and verify every live version. Stop on failure instead of advancing with an unresolved dependency.
11. **Run a small paid pilot.** Before any provider-executing validation or the first publication of paid code, check live balance and pricing, choose one to three synthetic records, and set `billing.maxCreditsPerRun` on the orchestrator and every newly authored provider-backed child. Disclose the aggregate pilot exposure as the maximum top-level run count multiplied by the orchestrator cap; each run resets a per-run cap. Publish only capped paid Plays. In an explicit internal/test workspace, run the pilot automatically. A customer workspace additionally requires explicit paid-pilot approval and a verified way to restore every test credit afterward; if restoration is unavailable, move the pilot to an internal/test workspace. Re-run one completed record with the same idempotency key to prove replay safety without buying the transition twice, counting that attempt in the aggregate bound even though a correct replay costs zero. Stop after the pilot if outputs are wrong, coverage is poor, or cost per usable result is too high. If the engine has no paid transition, run the same live pilot and report zero spend instead of adding a provider merely to create a charge. Do not use real customer rows or install triggers.

Read [references/state-machine-contract.md](references/state-machine-contract.md) when designing the transition table, Customer DB table roles, Play shape, and tests.

## Invariants

- Keep the engine as an orchestrator Play and every transformation as a transition Play. A switch statement full of embedded business transformations hides reusable work and is not the engine architecture.
- Keep generated engine artifacts in a durable, maintained project directory. The orchestrator, child Plays, types, README, and Mermaid diagram are source, not an ignored `tmp/` scaffold.
- Search the user's callable Plays and Deepline prebuilts before creating a transition Play. Reimplementing an existing contract creates duplicate behavior that will drift.
- Accept a reused Play only when its described input/output contract and composition shape fit the transition. A child that owns `ctx.dataset()`, `ctx.csv()`, event waits, or another lifecycle boundary cannot be composed with `ctx.runPlay`; create or adapt a scalar transition Play instead.
- Let the user's state machine drive the implementation. Do not ship a canned business workflow under generic names.
- Give each state distinct input and output table roles. Combine them only when existing project conventions clearly require it and the transition history remains unambiguous; report that assumption.
- Persist engine state with idempotent, schema-qualified Customer DB mutations. `ctx.dataset(...)` creates a run-scoped Runtime Sheet and cannot replace the durable state input and output tables.
- Persist the original input alongside or by stable reference from the output. A result without its input cannot be audited or replayed safely.
- Persist a typed failed or invalid output before rethrowing a child failure, unknown state, or forbidden child result. Failure outcomes use the same transition idempotency key and never create a next-state handoff.
- Make state transitions idempotent. A retry may repair an incomplete handoff, but it must not duplicate a completed output or next-state input.
- Treat unknown states and forbidden transitions as loud failures. Falling through to a default process silently corrupts the machine.
- Keep customer workflow rows and state-transition data in Customer DB. Product control-plane state used by Deepline UI/API/CLI, credentials, billing, and platform run state remain in their Deepline-owned stores, including Convex where applicable.
- Use stable Play names, dataset names, row keys, step ids, and tool ids. Renaming durable identities can make completed work look new.
- Treat an explicit request to build an engine as authorization to publish the checked engine. Run the bounded paid pilot automatically only in an explicit internal/test workspace or when the user explicitly approved that paid pilot and scope. This does not authorize real customer data, trigger installation, a larger run, or unrelated Customer DB mutations.

## Automatic publication and verification

After implementation checks pass, complete one dependency-ordered workflow:

1. Read live Deepline balance and pricing, select at most three pilot records, calculate a per-run cap, and disclose the aggregate bound as `(pilot runs + one replay attempt) × billing.maxCreditsPerRun`. If credits are unavailable, stop without attempting a top-up.
2. Set a static `billing.maxCreditsPerRun` on every newly authored provider-backed child before its first check or publication. A child cap must be no greater than the orchestrator cap so launching the published child directly cannot bypass the pilot bound.
3. Check and publish the capped children required for `ctx.runPlay` name and contract resolution. Never publish an uncapped revision of a newly authored paid child.
4. Set the orchestrator's static `billing.maxCreditsPerRun` before its first check or publication.
5. Check the capped orchestrator against the published child contracts.
6. Publish the capped orchestrator.
7. Verify every publication with `deepline plays get <name> --json`: inspect `play.liveRevision.version` and the static `billing.maxCreditsPerRun` in `play.liveRevision.sourceCode`, not a working revision. Reconcile that live version with the publication result and `deepline plays versions --name <name> --json`. `plays describe` and revision summaries do not expose the billing limit and cannot prove the cap by themselves.
8. Confirm the pilot is in an explicit internal/test workspace. For a customer workspace, also require explicit approval for the disclosed aggregate bound and verify a supported credit-restoration path before spending; otherwise provision or use an internal/test workspace.
9. Run the selected synthetic records through the real paid transitions to terminal completion.
10. Replay one completed transition with the same idempotency key and verify that it produces no duplicate charge, output, or handoff.
11. Compare persisted state, final output, observed spend, and replay behavior with the state-machine contract. If a customer workspace was used, restore every Deepline credit consumed by the test and verify the restored balance before handoff.

Do not request approval during dependency publication. Keep the customer paid-pilot gate to one question and skip it when the current request already explicitly approves the bounded pilot. If any check, publication, version verification, or pilot run fails, stop the workflow, preserve the successful results, and report the exact failure rather than advancing with an unresolved dependency.

The automatic paid pilot is bounded to synthetic inputs, at most three records plus one replay attempt, and the disclosed aggregate maximum derived from the published `billing.maxCreditsPerRun`. Obtain separate approval before using real customer data, installing triggers, scaling beyond the pilot, or causing other external side effects. Scaling requires a newly checked and published revision with the approved Deepline-credit cap; never silently remove or raise the pilot cap.

## Deliverable

Return:

- the resolved state and transition table, including inferred assumptions
- a Mermaid `stateDiagram-v2` diagram showing the complete state machine, including initial, terminal, and unresolved transitions
- the input/output table contract for every state
- the transition-Play reuse inventory, including owned and prebuilt candidates considered
- the maintained project source directory and source tree
- the implemented orchestrator `.play.ts` file and any newly required transition `.play.ts` files
- shared type source, a project README, and the Mermaid diagram as a maintained project file
- the state-decision and `ctx.runPlay` dispatch logic
- the idempotency and replay strategy
- the checks run and their actual results
- the paid pilot inputs and final outputs, observed Deepline spend, orchestrator and provider-backed child caps, aggregate bound, replay result, and any required customer-credit restoration receipt
- unresolved decisions or actions still requiring approval

Retain the exact per-step trace for each paid pilot record, including state determination, child Play calls, provider calls, persistence, handoffs, terminal completion, charges, and the replay attempt. Keep the default deliverable concise: show each pilot input and final output, not the full traces. Tell the user the traces are available and show them only when requested.
