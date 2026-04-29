---
name: strict-validation-setup
description: One-shot bootstrap of strict-mode tooling per ecosystem plus per-task GOALS.md scaffolding so an agentic loop can self-verify. Writes typechecker / linter / schema-validator config for TS (strict + noUncheckedIndexedAccess + exactOptionalPropertyTypes), Python (Pyright strict, Ruff strict), Rust (Clippy deny-correctness), Go (golangci-lint with staticcheck), OCaml (dune --release) at project edges; establishes a `.agent-tasks/<id>/GOALS.md` per-task convention distinct from project-stable AGENTS.md. C++/Java/Kotlin and framework specifics (Spring Boot, Nest, React-strict) are out of scope in this commit — surface as a follow-up when invoked on those ecosystems. Trigger on new project bootstrap, agentic-task setup, "make this self-verifying", "set the loop's goal", "scaffold goals for this issue". Pairs with `llm-self-loop` runtime — bootstrap once, run many.
disable-model-invocation: true
---

The skill ships two distinct concerns split by *temporal phase*:

- **Project-stable** — strict-mode tooling config + AGENTS.md authoring (defer the AGENTS.md content to `init`; this skill only ensures it exists and references the per-task pattern).
- **Task-ephemeral** — `.agent-tasks/<task-id>/GOALS.md` per task plus failing-test scaffolding co-located with it.

These never mix. Task goals never go into AGENTS.md (would leak as project policy). Project invariants never go into per-task GOALS.md (would duplicate per task and drift).

## Modality differentiation

| Skill                       | Owns                                                                             |
| --------------------------- | -------------------------------------------------------------------------------- |
| **`strict-validation-setup`** | Strict-mode tooling configs + per-task `GOALS.md` convention (this file)        |
| `init`                      | AGENTS.md authoring (project-stable) — defer to it for content                  |
| `test-driven`               | TDD discipline (RED → GREEN → REFACTOR) — defer for test-writing methodology   |
| `type-driven`               | Refined-type / typestate specs — defer for type-system invariants               |
| `design-by-contract`        | Pre/post conditions, runtime contracts — defer for assertion patterns           |
| `validation-first`          | State-machine specs (typestate / FSM / actor) — defer for FSM modeling         |
| `tests-adversarial`         | Assumption-violation tests — defer for the adversarial test pattern             |
| `setup-pre-commit`          | Commit-hook installation — defer for hook tooling                               |
| `setup-gitignore`           | Gitignore patterns — defer for ignore-file composition                          |

Duplication with the existing skills was audited and accepted; bodies cite each rather than re-doing the work. When the surface narrows to a single concern above, defer.

## Three parts

### 1. Strict-mode tooling bootstrap (project-stable)

Detect the ecosystem from manifests, then write strict-mode config per the relevant `references/<ecosystem>.md`. Idempotency: merge with existing config; raise if a destructive overwrite would be required and `--overwrite` is not explicit. Never silently replace.

Languages with bundled references (Q5-approved set; framework specifics deferred to a follow-up):

- `references/typescript.md`
- `references/python.md`
- `references/rust.md`
- `references/go.md`
- `references/ocaml.md`

Languages noted but not yet bundled — write deferred per Q8 rollback path: C++, Java, Kotlin, plus framework specifics (Spring Boot, Nest, React-strict). When the user invokes the skill on one of these, surface the gap explicitly and propose authoring the reference now or escalating to a follow-up commit.

### 2. AGENTS.md and per-task GOALS.md split (load-bearing)

- **AGENTS.md** — project-wide, stable across sessions and tasks. Contains: build/test commands, banned tooling, conventions, contract patterns, and the *location pattern* of per-task goal files (`.agent-tasks/<task-id>/GOALS.md` or whatever path the project chooses). **Defer authoring the AGENTS.md content to `init`** — this skill only ensures the file exists and contains the goal-location pointer.
- **`.agent-tasks/<task-id>/GOALS.md`** — task-ephemeral. Contains: the user's goal in prose, the success criteria the loop checks against, links to the failing tests in `.agent-tasks/<task-id>/tests/`. Cleaned up after the task merges.

The architectural rule: task A's goals never appear in AGENTS.md. AGENTS.md never contains task-specific success criteria. If the line blurs, surface and refuse.

### 3. Verifiable-goals scaffolding (task-ephemeral)

For the current task, translate the user's stated goal into failing tests / contract assertions. The tests live in `.agent-tasks/<task-id>/tests/` alongside the GOALS.md. The loop runs until the tests pass. Goals therefore exist both as prose (GOALS.md) and as code (tests).

Three sub-shapes, decide while drafting per task:

- **Interactive** — ask the user what success means, stub failing tests, hand back for review before agent loop begins.
- **Template-driven** — language-specific test stubs in `references/` (per-ecosystem). Pick the matching language template; let the user fill specifics.
- **Hybrid** — start template-driven; promote to interactive when the user's goal does not fit the template.

The term *verifiable goals* (Devin Agents101, Jun 2025) is preferred over *TDD-for-agents* (non-idiomatic in 2026 production stacks).

## Cross-references

Pairs with `llm-self-loop` runtime: this skill runs once at bootstrap, then `llm-self-loop` runs many times against the gates and goal files this skill installed. The pair is: *bootstrap → run-many*.

## Posture

Bootstrap is a one-shot mode. After running, do not stay resident. The loop that follows is `llm-self-loop`'s territory.
