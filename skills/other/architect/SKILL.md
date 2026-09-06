---
name: architect
description: 'Use when non-trivial code needs a design, architecture needs improving, or one module needs targeted interface narrowing, seams, or testability. Not for diagrams, deploy, or irreversible changes.'
---

# Architect

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Design non-trivial code before implementation (greenfield), or improve an existing codebase's architecture (brownfield): survey for shallow modules, locate a seam, deepen a structure, harden with guardrails, or make code testable; or design one named module's interface, seams, and testability (targeted-module). |
| Authority | Reversible local: writes only named local design artifacts and, when the request permits, the selected design in the working tree; rollback is deleting or reverting those writes. No VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | A local design package; in implement mode, the accepted refactor, its tests, inline `CONTEXT.md` entries for established domain terms, and an optional local ADR the user accepts. |
| Done | An explicit design choice with tradeoffs and a coherent implementation plan are recorded. In brownfield implement mode: one chosen deepening candidate is grilled to resolution, its shallow path is replaced rather than layered, tests exercise the resulting interface, obsolete shallow tests and code are removed, and established domain terms and accepted decisions are recorded locally. In targeted-module mode: the chosen module presents a small coherent interface, hides implementation complexity, concentrates change locally, and is testable through explicit seams. |

## Refusal

Not for visual architecture diagrams or HTML artifacts; use architecture-diagram, which renders a self-contained visual from a frozen specification; architect designs code structure (modules, interfaces, seams, depth) and produces a design package, not a rendered diagram. Not for deploy, remote, credential, publish, or irreversible changes; use shipping skills. Not for people-process or organizational architecture.

## Inputs

- `mode`: `greenfield` (design before implementation), `brownfield` (survey, deepen, or seams/testability/guardrails on existing code), or `targeted-module` (one named module's interface, seams, and testability). Infer from the request; confirm when ambiguous.
- Targeted-module: one named target module (a function, class, package, crate, or tier-spanning slice) with readable source and enough of its callers and tests to judge what they must know; optional: intended adapters, candidate seam locations, and the target language, inferred from the source when not stated.

## Vocabulary

Use these terms consistently in every recommendation and design sketch:

- Module: any unit with an interface and implementation, at any scale.
- Interface: every fact a caller must know: types, invariants, ordering, errors, configuration, performance plan.
- Implementation: what the interface hides.
- Depth: behavior hidden per unit of interface learned; a deep module provides high leverage through a small interface. Shallow modules expose a broad surface with little hidden.
- Seam: a point where behavior can be substituted or tested in isolation without editing that behavior in place.
- Adapter: a concrete implementation used at a seam.
- Leverage: capability gained per unit of interface learned.
- Locality: concentrating a change, bug, or required knowledge at one maintenance site.

Fix these terms; do not substitute near-synonyms: no "unit", "component", or "service" for module; no "API" or "signature" for interface, which name only the type-level surface; no "boundary" for seam, which is overloaded with DDD's bounded context. Say "adapter" when the seam is the topic and "implementation" otherwise; a small adapter can hold a large implementation, and a large adapter a small one.

## Procedure

### Greenfield mode: design before implementation

1. **Bound scope.** Confirm the code unit to design and its trust boundary (inputs, callers, failure paths). Done when: the unit is named and its boundary stated. If the request is trivial or already fully specified, stop and report no design needed.
2. **Sketch the usage surface first.** Write the public call plan, signatures, call sites, data shapes, before any implementation detail. Done when: the usage surface is recorded as a local artifact.
3. **Produce at least two competing design sketches** that each satisfy the usage surface and differ in structure or tradeoff. Done when: each sketch is coherent enough to evaluate.
4. **Evaluate every sketch against red flags:** hidden complexity, leaky abstraction, unbounded scope, premature generality, missing error or edge handling. Done when: each sketch has a red-flag record.
5. **Apply the redesign threshold.** If every sketch trips a blocking red flag or no sketch is coherent, redesign from the usage surface. Stop redesigning once at least one sketch is coherent and trips no blocking red flag. Done when: at least one coherent, unblocked sketch exists.
6. **Select the sketch with the best tradeoff record.** State the explicit design choice and the rejected alternatives with their tradeoffs. Done when: the choice and rejections are recorded.
7. **Derive the coherent implementation plan**, modules, types, control flow, failure paths, from the selected sketch. Done when: the implementation plan is recorded.
8. **Implement only if the human request and authority permit;** otherwise stop at the design package. Done when: either implementation is complete or the design package is delivered.

### Brownfield mode: improve existing architecture

#### Survey (read-only)

1. **Validate scope.** If a scope subset is supplied, confirm each path exists. Reject any path that does not. Done when: scope is confirmed or rejected with the missing path named.
2. **Enumerate module surfaces and assess depth.** See `references/survey-ranking.md` for the depth indicators and two-axis scoring. Done when: every public module is scored.
3. **Identify shallow modules and rank deepening candidates** by refactoring effort (call sites affected) and architectural gain (internal depth gained). Higher gain, lower effort ranks higher. Done when: a ranked candidate list exists.
4. **Select the top candidate** with a one-paragraph rationale. If no shallow modules are found, report zero candidates. Done when: one candidate is chosen or zero-candidate is reported.
5. **Return the report.** Do not modify source code. Done when: the ranked list, chosen candidate, internal seam notes, and any load-bearing rejection note are delivered.

#### Deepen (implement)

1. **Dispatch a read-only explorer** over the selected candidate's scope. Read applicable `CONTEXT.md` and local ADRs when present. Done when: the candidate's files, coupling, and dependencies are understood.
2. **Classify friction with the deletion test:** if deleting a module removes complexity, it is pass-through; if complexity spreads into callers, it earns its place. Treat the public interface as the test surface. Introduce a seam only for two real implementations (production + test); do not create a port for a hypothetical second adapter. Done when: each candidate has a deletion-test result.
3. **Present a numbered candidate list.** For each: name the files, the concrete problem and deletion-test result, a plain-language solution without an interface proposal, and expected locality, leverage, and testability changes. Ask the user to select one before writing. Done when: the user selects one candidate.
4. **Grill the selected candidate adversarially.** Resolve one dependent design decision at a time and recommend one answer. Bound the changed-file set before mutation. If a new domain term becomes established, update or lazily create `CONTEXT.md` immediately. If the user rejects a design for a reason future maintainers need, offer a local ADR and write it only after acceptance. Done when: every design decision is resolved.
5. **If the user requests interface alternatives, dispatch the design-twice parallel passes** described in `references/interface-design.md`. Done when: the designs are compared and differences resolved.
6. **Choose the dependency treatment by observed class**: see `references/deepening.md` for the four categories and their testing strategies. Done when: the dependency treatment is named.
7. **Implement only the accepted design.** Validate external and serialized inputs at the new interface. Migrate every scoped caller, delete the replaced shallow path, and delete shallow-module tests after equivalent interface tests exist. Do not layer the new design over the old. Done when: the shallow path is replaced, not layered.
8. **Exercise the changed behavior through the same interface callers use.** Confirm the accepted invariants, error modes, and relevant dependency implementation. Review the final changed-file set against the bound scope. Done when: interface-level checks pass and the changed-file set matches the bound scope.

#### Locate seam, testability, guardrails (read-only or implement)

1. **Locate the seam:** identify points where a caller can substitute an alternate implementation or inject a test double. If no seam exists, propose the smallest interface introduction that creates one without widening the public surface. Done when: each seam is named or the smallest creating-interface is proposed.
2. **Make code testable:** identify the concrete dependencies that block isolated testing, then propose seams (interface extraction or dependency injection) that make those dependencies substitutable. Prefer a seam that does not change production behavior. Done when: each blocking dependency has a proposed seam.
3. **Harden with guardrails:** recommend tooling that enforces the decisions: type-level constraints that make invalid states unrepresentable, lint or analysis rules that fail on violation, boundary checks, or tests that fail when an invariant breaks. Name the invariant each guardrail protects. Done when: each guardrail is tied to its invariant.
4. **Stop at recommendations unless the request and authority permit implementation.** Mark any recommendation not grounded in read code as inference. Done when: recommendations are delivered or implementation is complete.

#### Targeted module (single-module design; read-only or implement)

1. **Bound one module.** Name exactly one target module and confirm its source is readable; a name matching nothing is an unbounded-target stop, not a guess. Read the interface surface, the implementation, and the callers and tests crossing them. If depth cannot be judged inside this scope, stop and name the missing evidence. Done when: one module is named, its source is read, and its callers and tests are surveyed.
2. **Classify depth by leverage, not line ratio.** Depth is a property of the interface, not the implementation: internal parts, including internal seams used only by the module's own tests, are not interface, and a module has exactly one interface. One method that handles a hard problem well is deeper than ten methods that each forward to another layer. Done when: a deep or shallow classification is stated with leverage evidence.
3. **Run the deletion test.** If deleting the module removes the complexity, it was a pass-through hiding nothing. If the complexity reappears across N callers, it earns its keep. A pass-through verdict is a valid finding: report the module as shallow and name the callers that would absorb its complexity. Done when: the deletion test produces a pass-through or earning-its-keep verdict.
4. **Narrow the interface.** Ask in order: can methods be reduced? can parameters be simplified? can more complexity be hidden inside? Prefer the form that gives callers leverage and maintainers locality. Done when: the interface is at its narrowest form that preserves caller-visible behavior.
5. **Place seams by variation.** The external seam carries the interface; internal seams stay private to the implementation and its tests. Introduce a seam only when something varies across it: one adapter is a hypothetical seam, two adapters a real one. Done when: every seam is placed where variation crosses it.
6. **Check the test surface.** Callers and tests cross the same seam; a test that must reach past the interface means the module is the wrong plan. Restructure by accepting dependencies as parameters (not constructing them internally), returning results (not mutating in place), and keeping the surface small. Done when: callers and tests cross the same seam without reaching past the interface.
7. **Reject the framings wherever they appear.** Depth measured as a ratio of implementation lines to interface lines rewards padding the implementation; use depth as leverage. An interface narrowed to the language keyword or a class's public methods is too narrow; the interface is every fact a caller must know. Done when: both rejected framings are checked and neither is present in the analysis.
8. **Anchor terms in the target language.** See `references/language-anchors.md` for the per-language module, interface, seam, and adapter mappings; infer the language from the source when not stated. Done when: the vocabulary is anchored in the target language's constructs.
9. **Deliver, then edit.** Emit the recommendation in the fixed vocabulary; when restructuring is in scope, apply local edits confined to the bounded module while every caller and test keeps crossing the same seam. Done when: the recommendation is delivered and any local edits are applied within the bounded module.

## Failure and recovery

- Trivial or fully specified request (greenfield): stop, report no design needed, mutate nothing.
- No coherent sketch after the redesign threshold (greenfield): report blocked with the red-flag record; do not implement.
- Target code unreadable or absent (brownfield): report what is missing and stop. Do not infer structure from names alone.
- Ambiguous design question (brownfield): ask which sub-branch applies before proceeding. Do not guess and do not run all sub-branches.
- Unbounded target (targeted-module): the module cannot be isolated, its source is unreadable, or judging depth needs callers outside the scope: stop before any edit, report which evidence is missing, and ask for a narrower target. Do not widen scope or invent structure.
- Pass-through verdict (targeted-module): the deletion test shows the module hides nothing: report it as shallow and name the callers that would absorb its complexity. This is a valid finding, not a silent rewrite.
- Breaking or failed edit (targeted-module): an edit does not apply or breaks a caller or test: revert the uncommitted edits to the touched files (version-control checkout or manual revert) so no partial restructuring remains; recommendations already delivered stand.
- Non-converged interface (targeted-module): the interface cannot be narrowed without changing caller-visible behavior beyond the bounded scope: report the blocked state and the specific conflict. Never claim done while the done predicate fails to hold and never swallow the error.
- No defensible candidate (brownfield deepen): return `no-candidate` with the inspected scope and observed friction; make no changes.
- No selection or unresolved decision (brownfield deepen): return `blocked` with the candidate list or exact unresolved decision; preserve completed read-only analysis; make no implementation change.
- ADR conflict without a load-bearing reopening reason: preserve the ADR and return `blocked-by-decision`; do not re-litigate or bypass it.
- Conflicting constraints: surface the conflict and the tradeoff explicitly. Do not silently pick one side.
- Missing required implementation fact or unavailable behavioral check: return `blocked` with the missing fact or check and the files already changed. Do not claim the done predicate.
- Failed implementation or verification: restore every modified named file to its captured pre-change contents, remove only newly created artifacts from this run, and return `failed-rolled-back` with the failing observation. If exact restoration cannot be proved, stop with `recovery-required`, listing each affected file and its pre-change source.
- Partial result: analysis, candidate lists, and resolved decisions may be reported, but partially migrated code is never a successful output and must be rolled back. Ungrounded recommendations are marked as inference.
- Scope drift: stop, report the widening, mutate nothing outside the named artifacts.
- Rollback: delete or revert the named local design artifacts. No VCS, credential, or remote mutation is permitted.

## Output

A design package containing: the usage surface (greenfield) or the surveyed scope and ranked candidates (brownfield); the competing sketches or candidate list; the red-flag evaluation or deletion-test results; the selected design with tradeoffs and rejected alternatives; the coherent implementation plan; and, in implement mode, the interface-level checks and observed results, any `CONTEXT.md` or accepted ADR update, and the replacement and deletion performed. In targeted-module mode the package is a design recommendation in the fixed vocabulary: interface and implementation, external and internal seams, deep/shallow verdict with deletion-test result, interface-narrowing steps, seam placement, testability restructure, and any applied local edits with the rollback point. Terminal classification: `done`, `no-design-needed`, `no-candidate`, `blocked`, `blocked-by-decision`, `failed-rolled-back`, or `recovery-required`.
