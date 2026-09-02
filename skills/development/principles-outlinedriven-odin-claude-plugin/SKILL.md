---
name: principles
description: 'Use when a request names a working principle (subtract before you add, idempotent operations, never block on the human) or asks which principle governs a decision. Returns the law and its bite point; routes to the owning skill for execution. Not for running a repair — use fix.'
---

# Principles

Indexed anchor register: 21 named principles, each a law plus the moment it bites. Read the index, jump to the anchor, apply the law. Principles governs judgment only and never executes or mutates. When an anchor requires mutation or execution, route the user to the owning skill (`fix`, `debug`, `architect`, `deslop`, `commit`, `ci-cd`) instead of instructing execution. Come here to decide, not to run a repair.

Five anchors carry procedure-dense references (linked inline); the rest are complete at anchor length.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A request names a working principle by name or example, or asks which principle governs a decision. |
| Authority | Read-only. Names the owning skill for execution; never mutates files, VCS, credentials, or remote state. |
| Side effect | Guidance in chat output only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Done | The governing principle is named with its law and bite point, and the owning skill is named when the anchor requires execution. |

## Index

| Anchor | Governs |
|---|---|
| Subtract before you add | land deletions first, as their own commit |
| Sequence verifiable units | per-unit checks, halt at first failure |
| Outcome-oriented execution | plan → rollback-anchor migration |
| Migrate callers, then delete | one-wave API replacement |
| Redesign from first principles | requirement integration without bolt-ons |
| Build the lever | hand-do one, codify, rerun |
| Idempotent operations | retries converge to one state |
| Encode lessons in structure | repeated instruction → enforcement artifact |
| Fix root causes | why-chain over symptom patching |
| Prove it works | captured evidence from the real artifact |
| Model the domain | typed state machines, illegal states fail compile |
| Type system discipline | compiler as the proof of constraints |
| Foundational thinking | types before logic |
| Boundary discipline | validate once, at the seam |
| Separate before serializing | per-actor state before locks |
| Laziness protocol | deletion-first smallest change |
| Minimize reader load | one-pass state trace |
| Experience first | fewer polished over many partial |
| Exhaust the design space | 3+ distinct alternatives, criteria first |
| Never block on the human | reversible proceeds, irreversible parks |
| Guard the context window | decisions in context, payload out |

## Sequencing and structure

### Subtract before you add

Land obsolete-code deletions as their own green commit before the addition or rewrite starts, so the new work rests on a simpler base.

**Bites when** an addition or rewrite lands on code the new design obsoletes.

The deletion commit is the recovery anchor: if the gate fails after deletion, revert it and abort the addition; if it fails after the addition, fix forward, never revert the subtraction to mask an addition bug. Announce the deletion set and get confirmation before staging; a narrowed-to-empty set skips straight to the addition. When this anchor requires landing commits, route to `commit`.

### Sequence verifiable units

Decompose multi-step work into units, each with a named check; halt the sequence at the first failing check and report that unit only.

**Bites when** work decomposes into two or more units, each verifiable in isolation.

Map the dependency graph first; units at the same depth may run in parallel. A failed unit means no partial commit and no success summary.

### Outcome-oriented execution

Execute a planned migration stepwise against a rollback anchor, verifying each step's predicted intermediate state; roll back to the anchor on any mismatch.

**Bites when** a plan names a target architecture and the intermediate breakage is reversible.

Establish the anchor before the first mutation; release it only after the end state verifies. Procedure and failure codes: `references/outcome-oriented-execution.md`. When this anchor requires executing the migration, route to `fix`.

### Migrate callers, then delete

Replace an internal API by migrating every caller in one wave, proving zero references remain, then deleting the legacy path under VCS.

**Bites when** an API replacement is scoped and every caller is enumerable.

A missed caller after deletion → restore from VCS, migrate it, redo the verify-and-delete. An ambiguous caller halts the wave before any mutation. When this anchor requires executing the migration, route to `architect`.

### Redesign from first principles

Integrate a new requirement by resolving it against named invariants and propagating structural edits everywhere the answer changes, never bolting it on at one site.

**Bites when** a requirement lands that the current structure only half-fits.

Name the invariants first; a conflict is resolved by revising the principle or reshaping the requirement, never suppressed. Partial propagation is a stop, not a done. When this anchor requires propagating structural edits, route to `architect`.

## Levers and enforcement

### Build the lever

For non-trivial repetitive work: do the first unit by hand, codify the recipe into a deterministic rerunnable script, prove it reproduces the hand-done unit, then run it for the rest.

**Bites when** work repeats and is more than a couple of obvious edits.

Pick the artifact by intent: edits → codemod; repeated files → generator; analysis → structured query; verification → rerunnable check with an explicit pass/fail contract. Commit the lever when the work outlives the session; a reviewer must be able to rerun it without session context. When this anchor requires building and committing the lever, route to `commit`.

### Idempotent operations

Design every retryable operation so running it N times converges to the same state as running it once.

**Bites when** commands, loops, or migrations can be interrupted and re-entered.

Classify each side effect (naturally / conditionally / not idempotent) and replace or guard it; guards read state at execution time, never from cache; the rollback must itself be idempotent. Procedure and replacement table: `references/idempotent-operations.md`.

### Encode lessons in structure

Turn a repeated instruction into an enforcement artifact (lint rule, check, CI gate, schema constraint) that fires on the violation, instead of re-telling it.

**Bites when** the same correction has been given more than once and a mechanism can catch it.

One violation per artifact; prove it fails before the fix and passes after; name the rollback. No preemptive rules without a named violation. When this anchor requires creating CI gates or lint rules, route to `ci-cd`.

## Truth and proof

### Fix root causes

Reproduce first, trace the why-chain to a decision in this project's source, fix the pattern at every instance, and reject any change that only silences the failure.

**Bites when** a defect is reported with wrong behavior (not a feature request).

Instrument rather than guess; a guard is legal only where the why-chain proves the state invalid. Procedure, symptom-fix rejection list, and failure classes: `references/fix-root-causes.md`. For the guarded repair loop with retry budgets, use `fix`; this anchor governs the diagnosis.

### Prove it works

Completion claims require captured output from a real artifact, not a mock: state the claim, run the minimal verification command, record what it printed.

**Bites when** about to claim done.

Verification contradicting the claim stops the run: no re-running hoping for a different result, no substituting a test double, no claiming done while the reproduction fails.

## Types and boundaries

### Model the domain

Encode stateful, branch-heavy logic as a typed state machine so illegal states and transitions fail to compile.

**Bites when** flags and booleans track domain progress.

Enumerate states and transitions before writing types; one constructor per live state; validate reachability and migrate every caller, unmigrated call sites mean not done. When this anchor requires encoding the state machine in code, route to `architect`.

### Type system discipline

Choose types so the compiler, not review, detects invalid and unhandled states: sum types for exclusivity, branded types for look-alike domains, literal unions for closed sets, exhaustive matches without wildcards.

**Bites when** designing types or signatures for a domain.

Compiler rejects valid code → widen; accepts invalid → narrow; re-run until both hold. The five moves and the tighten/loosen loop: `references/type-system-discipline.md`.

### Foundational thinking

Settle the core types and data structures before writing any logic; data shapes that compose make downstream code obvious.

**Bites when** starting a feature or module.

Strongest available type (enums over strings, branded over bare, records over loose maps); validate at trust boundaries; if an operation needs a cast or escape hatch, extend the type set instead.

### Boundary discipline

Validate once, at the trust boundary; the interior trusts validated types and carries only business logic.

**Bites when** placing validation and error handling.

Classify each guard boundary / interior / absent and move it outward to the seam; a thin shell means no nil-guards on data that entered validated. A guard that cannot move cleanly is a stop, not a partial move.

### Separate before serializing

Fix shared-write races by splitting per-actor state out of shared scope before choosing a lock, then define the explicit read-boundary merge.

**Bites when** two or more actors write one mutable location.

Shared residue gets the narrowest primitive that covers the write path; a merge that cannot be expressed without a papering-over lock is a stop, not a lock. Procedure and failure classes: `references/separate-before-serializing.md`. When this anchor requires executing the split, route to `fix`.

## Economy

### Laziness protocol

Deletion first: anything the requirement sentence does not demand is a candidate for removal; every retained element carries a stated reason.

**Bites when** minimizing an implementation or refactor.

Reuse before new code; of two sufficient approaches pick fewer moving parts; note adjacent improvements in one line without doing them.

### Minimize reader load

Collapse pass-through layers and narrow scopes until a fresh reader traces each state's origin and mutation in one pass, with behavior unchanged.

**Bites when** reading cost, not behavior, is the problem.

A forwarder survives only if it adds behavior, guards a boundary, or carries a needed name. An edit that changes behavior is restored immediately. When this anchor requires executing the collapse, route to `deslop`.

### Experience first

Scope products to fewer fully polished experiences over many partial ones; every retained feature carries a one-sentence quality guarantee.

**Bites when** scope exceeds resources.

Cut stubs outright; cut partials that do not harm the core experience; never lower the quality bar to fit more features.

## Decisions and attention

### Exhaust the design space

For a novel interaction or architecture: three or more structurally distinct alternatives, criteria fixed before comparison, winner chosen on recorded evidence.

**Bites when** the choice is genuinely novel, not a parameter tweak.

Prototypes need only reveal the shape; a tie is documented, not broken arbitrarily.

### Never block on the human

Proceed asynchronously on reversible work; park each irreversible item behind exactly one concrete question (target, consequence, recommended option).

**Bites when** deciding what needs a question before the human answers.

Reversible = undoable locally with no credential, publication, data-at-rest change, or destructive delete; uncertain means irreversible. Silence and timeouts are non-consent.

### Guard the context window

Keep raw payload (full files, bulk search results) out of main context; delegate bulk reading or read selectively, carrying forward decisions and facts only.

**Bites when** context fills and reasoning room shrinks.

If the payload cannot be distilled into a decision, say so; do not pretend the context is clean.
