---
name: necessary-work
description: 'Gate every candidate action against one test: would deleting it leave the requested outcome unmet or unproven? Use when work is about to grow past the ask with an extra check, artifact, abstraction, retry, threshold, or follow-up, when deciding whether the task is already done, or when the user says minimum, only what is needed, or stop when it works. Applies to coding, research, planning, debugging, review, and writing alike.'
---

# Necessary Work

Do only the work that satisfies and proves the requested outcome.

## Kernel

For every candidate action `c`:

```
delete(c) => outcome unmet or unproven ? do_minimum(c) + prove(c) : reject(c)
```

- Define the requested outcome and the minimum proof before acting.
- Nothing is necessary merely because it is useful, conventional, safer, cleaner, or more thorough.
- Add no constraint, process, artifact, abstraction, check, or follow-up without a source of necessity.
- Prefer the smallest sufficient implementation.
- Once the outcome is proven, stop.
- If ambiguity cannot be resolved, bind the smallest interpretation consistent with stated intent and report it.

## Do this

1. Define the contract: the requested outcome plus the minimum evidence that proves it.
2. Treat every possible piece of work as a candidate, never as automatically necessary.
3. Admit a candidate only when removing it would leave the contract unmet or unproven.
4. Execute the smallest reliable action that closes that gap.
5. Stop the moment the contract is proven.

A source of necessity is one of four: the request, the environment, authoritative policy, or measured evidence. Limits, thresholds, retries, budgets, abstractions, artifacts, and process come from one of those four or they do not come at all.

## Report

- **Outcome** - what was requested, and that it now holds.
- **Evidence** - what proves it.
- **Rejected** - candidates the kernel dropped, and any ambiguity left unresolved.

Speculative follow-up work is not part of the report.

## Verify

- [ ] The contract was written down before work started: outcome plus minimum proof.
- [ ] Every admitted action fails the delete test, so removing it would leave the contract unmet or unproven.
- [ ] Work stopped at the proof, with no useful-but-unrequested additions.
