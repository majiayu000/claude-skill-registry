---
name: target
description: Define how unsupervised work will be judged before it runs. Use when execution is an autonomous loop or a long unbabysat agent run that optimizes toward a metric. Triggers on "autonomous loop", "let it run", "optimize until", "overnight run", "unsupervised", "set a goal".
---

Define the observer before unsupervised work runs, so the cheapest way to pass is the real work.

## Contract

- **INPUT**: a spec for work that will run unsupervised.
- **GATE**: "Is the observer mechanical AND un-gameable?" Agent audits, user locks.
- **OUTPUT**: a success contract (spec below). Emit it in conversation.

## The success contract

Concrete and executable. Exact commands, values, and targets, not abstractions.

- **Observable**: the single state or number that means done. One thing, not a dashboard.
- **Verify command**: the literal command the run executes and surfaces in its output, exiting non-zero on crash. Require the real output, exit code and score line, in view. An unsupervised run can claim a check it never ran.
- **Direction and target**: higher or lower is better, and the value that ends the work.
- **Bound**: a turn or wall-clock cap that ends the loop even unmet (`… or stop after N turns`).
- **Baseline**: the observable's value now, from one dry run. Proves the command fires.
- **Guards**: what must keep passing while optimizing. Check before reading the observable. A violation voids the score and the kept change. It never just lowers the score.
- **Cheats closed**: each cheap path to a false pass, paired with its structural closure. Format: `cheat: … / closed by: …`. Done when no listed cheat is cheaper than real work.

## Work loop

1. **Extract target**: from the spec, name the single observable that means done.
2. **Mechanize**: make it extractable, deterministic, fast. If success needs human judgment, it cannot be mechanized. Stop and say so.
3. **Red-team**: start from the known-cheat catalog (`cheat-museum.md`), then hunt the cheats specific to this target. Close each with a fence: a holdout the run can't see, an artifact cap, a cut to feedback resolution, a perturbation probe that gauges memorization. Loop until nothing is cheaper than real work.
4. **Baseline**: dry-run the verify command once, record the value, confirm it exits clean. A command that will not run is a gate FAIL.
5. **Gate**: run the gate audit below.

### Decision prompts

<!-- doc-gen FILE src=../prompts.md -->
- Auto-gather when the answer is retrievable with certainty: cheap local reads, docs, web research, parallel subagents. Return with decisions, not raw findings. Never ask the user something research already made obvious — that is a named stop condition.
- Only non-obvious judgment calls reach the user. Every such AskUserQuestion: exactly 2 candidate answers + 2 uniform escape hatches — "Gather facts" (research/explore) and "Hear tradeoffs" (consult experts). Hatches are first-class options, never hidden behind Other.
- Re-entry after a detour: if the detour made the answer obvious, state the decision and proceed; otherwise re-ask the same question with the new evidence inside the prompt.
- Presentation rule: EVERYTHING the user needs to answer lives inside the question UI — question text, descriptions, previews. Never in prose before the tool call (the dialog hides it).
<!-- end-doc-gen -->

## The gate

"Is the observer mechanical and un-gameable?" Agent audits, user locks.

- Before presenting, run a deletion pass over the draft contract. Cut every cheat already closed by another, every guard that restates the observable, every line a command cannot check.
- Present verdict first via AskUserQuestion: PASSES or FAILS, then the surviving cheats and how each is closed. Proof the adversary ran.
- On FAIL, name what is unmechanical or un-closeable. If success cannot be defined, stop. The work is not ready to run unsupervised. If a cheat cannot be closed, bounce to the user. Never pad the contract to look safe.
- The user locks. The lock is theirs, not yours.

## Pre-flight

Two acts only the human can do before the loop runs unsupervised:

- Issue a disposable API key with a provider-side spend cap. The contract bounds correctness. Only the key bounds cost.
- Babysit cycle one. Watch what the run touches, confirm it uses the instruments the contract names, then leave.

## Boundaries

The human owns and locks the contract. The optimizer never defines its own success. When execution games the contract, fix the contract: widen the observable, add a guard, cap an artifact. Never fix the worker. A cheat is a bug in the target. Resume from the last honest checkpoint and revert what the cheat produced.
