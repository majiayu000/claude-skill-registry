---
name: exhaustive
description: 'Prove a decision space, state space, requirement set, or behavior surface is fully covered by enumerating every cell and classifying each as covered, gap, or deferred with an executed check. Use when the user says "exhaustive", "prove coverage", "did I miss any case", "enumerate the state space", or when a refactor or feature needs a completeness audit before it is called done.'
---

# Exhaustive

Prove nothing was missed. `exhaustive` enumerates a target space and classifies every cell, so completion is a checked fact rather than a feeling. It enumerates algorithmically; it is not a round-based question walker (that is `batch-ask-me`) and not a hypothesis-sampling Q&A (that is `askme` exhaustive mode).

## Target space

Pick the enumeration that fits the target (name the choice in the output so the reader knows which space was covered):
- **State space** — for code with lifecycle, state machines, or error paths: the State × Event × Outcome Cartesian matrix.
- **Decision space** — for a design with open forks: the dependency-respecting set of decision axes.
- **Requirement space** — for a spec or feature: the requirement-to-symbol map, with each acceptance criterion traced to a code or test symbol.
- **Behavior surface** — for a refactor or deletion: every exported symbol and reachable path in scope.

If the target space is unbounded or unidentifiable after one read, stop and ask one question to bound it; do not enumerate an infinite space.

## Method

1. **Enumerate.** Generate the full cell list for the chosen space with tool-backed discovery (`ast_grep` for code constructors and match arms, `grep`/`lsp references` for symbols and callsites, `read` for spec criteria). Every cell carries an `id` and a one-line description. The list is the universe; nothing outside it is in scope, nothing inside it may be silently dropped.

2. **Execute the check per cell.** For each cell, run a programmatic check that proves coverage or exposes the gap — `grep`/`ast_grep`/`lsp` for code, a subagent read for prose, or a test run where a test is the proof. A cell with no executable check is classified by an explicit reasoned argument, never by silence.

3. **Classify every cell.** Assign each cell exactly one of `covered`, `gap`, or `deferred`, each with a one-line reason. `deferred` requires a named owner or follow-up; it is not a silent drop.

4. **Emit the coverage manifest.** Output the classified cell list plus a one-line tally (`covered: N, gap: M, deferred: K, total: T`). For a code state space, also assert zero wildcard catch-alls over the enumerated constructors, verifiable with `ast_grep`.

5. **Prepare the unresolved cells.** Sort `gap` cells in dependency order so a caller can hand them to another workflow without rebuilding the space. `exhaustive` emits the ordered gaps; it does not run a downstream question or ideation workflow itself.

## Completion

`exhaustive` is done when the manifest has **zero unclassified cells** — every enumerated cell is `covered`, `gap`, or `deferred` with a reason — and, for code state spaces, the wildcard-catch-all assertion holds. Re-enumerate once after any fix the user applies to a `gap`; stop when a re-enumeration adds no new unclassified cell.

## Machine-readable output

On explicit request for structured output, emit the manifest as a fenced `exhaustive-manifest/v1` block containing a YAML list of `{id, description, classification, reason, check}` plus the tally line. In a plain interactive run, emit only the human-readable classified list plus tally.
