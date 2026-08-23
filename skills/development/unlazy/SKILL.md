---
name: unlazy
description: 'Gate-file discipline over a task decomposition: prove done instead of claiming it. Use on explicit invocation ("unlazy", "depth tree", "gates", "do not stop until it is done"), on laziness symptoms (work delivered half done, a premature done claim, suspected stubs or silently narrowed scope), or proactively when a build decomposes three or more layers deep.'
---

# Unlazy

The failure this skill kills is output that is technically responsive but quietly incomplete: the done report at 80 percent, the silently narrowed scope, the confident wrong number in a final summary. Prose instructions cannot catch these failures; the ones that survive instructions are exactly wrong self-reported numbers and stalls that feel like completion. So enforcement lives in files and runnable checks, not in goodwill. You do not promise you are done. You prove it against a ledger.

This skill governs gate discipline on a decomposition; it composes with `work`, `incremental`, and `subagent-driven` rather than replacing them.

## Rule zero: gates before work

Before real work starts, write the acceptance gates to a file: `.outline/GATES.md` in the working directory, using [templates/gates.md](templates/gates.md). One checkbox per outcome the task requires. Wherever an outcome is command-checkable, give it a `CHECK:` line (the runnable command) and an `EXPECT:` line (the output that decides it), so the check is a subprocess rather than an opinion.

Why a file: intentions do not survive a long context, files do. A checklist written at minute 2 is exactly as sharp at minute 90, when the pull toward wrapping up is strongest.

The gate contract, in Hoare's register: `CHECK` is the test, `EXPECT` is the postcondition, `EVIDENCE:` is the recorded proof. A checked box is a claim; evidence is the proof. A checked box whose evidence still reads `pending` counts as worse than unchecked, because checked-without-evidence is the exact failure this system exists to catch.

If a gate becomes genuinely impossible, do not quietly drop it. Add `ABANDON: <gate id> <reason>` to the gates file and say so in your report. Visible surrender is honest; silent scope-narrowing is not. The tooling treats an ABANDON line as a resolved exit, not a failure.

## Enforcement

Run the bundled checker to execute CHECK commands, flip boxes, and record evidence:

```
python3 <this-skill-dir>/scripts/gate_check.py .outline/GATES.md
```

It flips a box only when the command's output matches EXPECT (substring, or `/regex/`). `--status` reports without changing anything; exit 0 means every gate is met or honestly abandoned. Manual gates (no CHECK possible) are checked by hand, but only with the `EVIDENCE:` line replaced by actual proof: a measurement, a quote of output, a `file:line`. Upstream unlazy also ships a Claude Code Stop hook that blocks ending the turn on unmet gates; this port does not carry it.

## The depth tree

Decompose at natural joints, N layers deep. Layer 1 is the task; leaves are the only places real work happens. A leaf is a real unit of work: ten or more minutes of focused effort, one coherent deliverable, one gates file. Smaller leaves mean you went one layer too deep; back off. Contracts (interfaces, file ownership, naming) are fixed in the plan before any fan-out, and every internal node gets its own integration gates, because thirty-two finished leaves can still be a broken product.

Depth guidance: tree 2-3 for a feature, bug hunt, or document (solo); tree 4-5 for a subsystem or serious refactor; tree 6-7 for an entire project built to a high bar, orchestrated with leaves on disjoint work units.

Effort per leaf comes from its gates, never from N. A leaf is finished when its gates are fully met with evidence AND a full improvement pass finds nothing, whichever is later. Construction and orchestration details: [references/method.md](references/method.md); gate format and writing guide: [references/gates.md](references/gates.md).

## Work each leaf in passes

1. Implement completely. No placeholders, no TODO, no "rest as exercise".
2. Re-read as a domain expert; name the cheap version of each part and replace it with the good one.
3. Hunt defects: edge cases, correctness, performance, the tells that something is fake. Fix what you find.
4. Polish that costs nothing; tuned constants beat new features.

## Report audit

The most reproducible laziness failure is a report whose numbers are wrong while its substance is right: "34 stat rows" where 17 exist, stated from memory. At report time, re-measure every number you are about to state, or label it unverified. Paste the gates ledger with its count, N of N checked, every ABANDON line surfaced. A report is a set of claims backed by a ledger, never a vibe of completion.

## Behavioral rules

- No report until the ledger is full. Composing a status summary while boxes are unchecked is the laziness reflex firing; open the gates file and pick the next unchecked box instead.
- When you feel finished, check instead of concluding: run gate-check, then re-read one passed gate adversarially and try to refute its evidence.
- Finish one line of attack. Before switching approach, state what the current one still has to give and why switching wins; if you cannot, keep going.
- Do not simulate work you can do. If an action is cheap and reversible, take it and observe.
- Ignore resource anxiety. Never compress, stub, or summarize because the end feels near; if a real limit approaches, write the remaining work into the gates file and hand over with ABANDON lines and reasons.
- Full files, full lists, full sweeps. If the task says all 80 files, the count opened is 80 and you state that count; sampling is only acceptable when declared.

## What this skill is not

Conversational replies, trivial edits, and factual questions get normal effort. No gates file for a one-line fix. The discipline is for work the user wants done well, and it exists to make "done well" the only kind of done you produce.
