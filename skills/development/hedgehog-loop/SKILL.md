---
name: hedgehog-loop
description: Use for every unit of work once a Hedgehog project is bootstrapped — building one layer (schema, contract, repository, service, controller, hook, screen) per module, gated by `hedgehog verify` and committed one layer at a time. Triggers on "next step", "build this module", "what's next", or the start of any work session on a bootstrapped project. Also covers the Correction Protocol for fixing a wrong upstream step.
---

# Hedgehog Loop

The operating loop for a bootstrapped Hedgehog project: `hedgehog next`
emits the packet for one ready layer, build it, `hedgehog verify` gates
and commits it. The build graph (`.hedgehog/hedgehog.db`) is the live
list — query it via `hedgehog status`/`hedgehog next`, never re-derive
state from prose. The step tables below mirror
`src/golden-cores/full-stack-app/core.yaml`, already the source of truth
for layer order, scope, and verify command per layer — read the tables
for the human-readable shape, trust the YAML (and the packet `hedgehog
next` emits from it) as the authoritative one if they ever seem to
disagree.

## Determine phase

Before touching code, know which phase applies to the module in scope:

- **Phase A** — building/extending the backend. Every module in scope
  needs schema → contract → repository → service → controller before
  Phase B starts for any of them.
- **Phase B** — Phase A is closed for the module. Build hooks and screens.

Check `hedgehog status` (or `hedgehog why <path>` for a specific file),
or the commit log for `feat(<module>): api` commits. No such commit (and
no `controller` task `complete` for that module) means the module is in
Phase A.

## The Domain Module Pattern

A **domain module = one table.** `users`, `orders`, `order_items` are each
their own module, carrying the full step sequence below. The schema is the
source of truth for module boundaries.

**Cross-module references are FK-by-ID only.** If `orders.user_id`
references `users`, the `orders` schema holds a plain FK column. The
`orders` repository and service depend only on their own ports — a service
knows related entities only as an ID.

- Need the related row? Resolve it at the contract/controller layer
  (parallel calls to each module's own endpoint), or join against the
  other module's *schema* directly inside the repository (Drizzle query).
- This keeps every service importing only its own ports, so the Nx rule
  `type:service → onlyDependOnLibsWithTags: ['type:port', 'type:util']`
  holds uniformly (wired at bootstrap).

A junction table (e.g. `order_items`) is one table, one module, with two
FK-by-ID columns instead of one, each resolved the same way.

Every module goes through the same shape, in order:

```
schema      (Drizzle)              — types before data
contract    (Zod / ts-rest)        — the boundary
repository  (port + Drizzle adapter)
service     (domain logic)         — imports only ports
controller  (thin HTTP)
hook        (TanStack Query)       — Phase B only
```

Plus, when an operation needs async **and the Queue add-on is on for this
project** (check `.hedgehog/addons.yaml`'s `queue.on`): **queue = port +
BullMQ adapter**, same port/adapter shape as the repository. The service
imports only ports. Queue is one-time project infra, not a compiled
layer — `full-stack-app/core.yaml` has no `queue` layer, so this step has
no `hedgehog verify` gate of its own; build it as part of the
`controller` layer's packet, verified by that layer's own check. If the
Queue add-on is off, there's no `apps/worker` and no queue step, full
stop — an operation that seems to want async processing on a Queue-off
project is a signal to revisit that add-on decision with `planner`, not
to build a one-off queue outside the add-on's scaffolding.

Standard Nx generators (`@nx/nest`, `@nx/next`, `@nx/expo`, `@nx/js`)
scaffold the app/lib shell. Each step's actual content (schema, contract,
repository, service, controller, hook) is hand-built, following this
sequence.

## Domain Module — Backend Steps (Phase A, every module in scope)

A horizontal pass across the whole backend — every module goes through
these before any module gets a hook or screen. Each row is one compiled
layer in `full-stack-app/core.yaml`; delegate each module's Phase A
layers to the `backend-eng` agent, one `hedgehog next` packet at a time —
it builds the layer, `hedgehog verify` gates and commits it.

| # | Layer | Lives in | Commit |
|---|---|---|---|
| 1 | `schema` | `packages/db` (Drizzle) | `feat(<module>): schema` |
| 2 | `contract` | `packages/contracts` (Zod via `drizzle-zod` + ts-rest) | `feat(<module>): contract` |
| 3 | `repository` | `libs/<module>/repository` (port + Drizzle adapter) | `feat(<module>): repository` |
| 4 | `service` | `libs/<module>/service` (domain logic — imports only ports) | `feat(<module>): service` |
| 5 | `controller` | `apps/api` (thin HTTP, wires contract → service; bundles Queue infra, see above, if that add-on is on and this module needs it) | `feat(<module>): api` |

Repeat 1–5 per module in scope, via `hedgehog next`/`hedgehog verify`.
The API is complete, typed, and callable (Postman/curl/contract tests)
before frontend work starts.

## Domain Module — Frontend Steps (Phase B, after Phase A closes for the module)

| # | Layer | Lives in | Commit |
|---|---|---|---|
| 6 | `hook` | `packages/hooks` (TanStack Query) | `feat(<module>): hooks` |
| 6a | UX rationale | `docs/design/<module>.md`, `ux-planner` agent | bundled into layer 7's commit |
| 7 | `screen` | `apps/web` and/or `apps/mobile` | `feat(<module>): screen-web` / `feat(<module>): screen-mobile` |

Phase B starts once Phase A is done for the scope. The frontend is a pure
consumer of an already-finished API. Delegate each module's Phase B
layers to the `front-end-eng` agent, same reasoning as `backend-eng` for
Phase A — one `hedgehog next` packet at a time, in its own context. Step
6a is where "how it should feel" gets decided — once per module, after
the `hook` layer's task is `complete` and before `front-end-eng` starts
the `screen` layer — via `ux-planner`, starting from whatever `planner`
filed in `docs/design/<module>-notes.md` at planning intake, or the raw
UX spec directly if that file is absent. Its first run for a module also
signals to the user that Phase B has started, and is the point a mockup,
screenshot, or export (Google Stitch, Figma) can be handed over. It
writes `docs/design/<module>.md`, not its own compiled layer — the
`screen` layer's `hedgehog verify` is what gates and commits it.

## The Loop (every unit of work)

1. **Run `hedgehog next`.** It emits the task packet for one ready layer
   (STATUS/WHY NOW/BLOCKED DOWNSTREAM/ALLOWED SCOPE/VERIFICATION) —
   trust it: `hedgehog next` never emits a layer whose dependencies
   aren't `complete`, so there's no separate gate check to run by hand.
2. **Delegate the full packet** (not a step name) to `backend-eng`
   (Phase A) or `front-end-eng` (Phase B) — one schema, one contract, one
   repository, matching the packet's ALLOWED SCOPE.
3. The agent **runs typecheck/lint/test on its own work** (mirrors
   lefthook, wired at bootstrap) as a sanity check before reporting
   back — necessary, not sufficient. The agent reports the work as done;
   it does not move the task and does not commit.
4. **Run `hedgehog verify <task-id>`.** It checks the touched files
   against the packet's ALLOWED SCOPE, runs the layer's VERIFICATION
   command, and on a pass writes the commit (the exact Conventional
   Commit message from the tables above, plus the updated build graph)
   and unlocks the next layer. On a scope violation or a failing check,
   the task stays `implemented`/`failed` and nothing downstream unlocks —
   fix it and re-run `hedgehog verify <task-id>`, don't hand-commit
   around it.

   A stalled task is not pickable by `hedgehog next`, so both `hedgehog
   next` and `hedgehog status` list it under NEEDS ATTENTION with the
   task id to re-verify. If `hedgehog next` reports the graph blocked,
   fix that task — don't treat it as "nothing left to do."
5. **Repeat** — `hedgehog next` again for the following layer.

Each `hedgehog verify` call commits exactly one layer, built right for
what's known now; a wrong layer is fixed forward later via the
Correction Protocol.

## Intra-step conventions

The Nx boundaries, phase gate, and lint own the *structural* rules
(what imports what, what gets built when). These are the conventions
*inside* a step that those gates can't see — apply them uniformly so a
fresh-context session builds module N the same way it built module 1. The
`reviewer` agent checks these at a phase boundary.

- **Errors are thrown, typed, and domain-named.** A service throws a
  domain error (`OrderNotFoundError`, not a bare `Error` or an HTTP
  exception) — services don't know they're behind HTTP. The controller is
  the only layer that maps domain errors to status codes. Never return
  `null`/`undefined` to signal a failure a caller must branch on.
- **Repository not-found returns `undefined`; the service decides.** A
  `findById` that misses returns `undefined` (a plain absence, not an
  error); the service turns that into a thrown domain error when the
  operation requires the row. Adapters don't throw domain errors — they
  report absence, the service interprets it.
- **Validation lives at the contract boundary, once.** Input is
  Zod-validated at the controller via the ts-rest contract. Past that
  boundary, types are trusted — services and repositories don't re-parse.
  A service-level invariant that isn't expressible in the Zod schema
  (e.g. "can't cancel after payment") is enforced in the service as a
  thrown domain error, not a second validation pass.
- **Multi-write operations are transactional.** A service method that
  writes more than once wraps the writes in one Drizzle transaction,
  passed through the port — partial writes never escape a failed
  operation.
- **Services are pure domain logic.** No logging, no HTTP, no queue
  mechanics inside a service method — those live at the controller /
  adapter edge. A service reads as the business rule and nothing else.

## Friction log

Real friction during a build — an agent's instructions were unclear, a
redline had to be issued twice for the same underlying gap, the user
had to correct the same kind of mistake more than once, or user
feedback implied something was wrong even without a direct correction
(a preference stated once that, read plainly, means an earlier step
missed something) — is signal worth keeping past this session, separate
from the Correction Protocol that fixes it in the moment. Log one entry
via `hedgehog friction add "<note>" [--task <task-id>]` when that
happens: what was tried, what went wrong or was implied, why if visible,
and the commit/message it traces to, all in the note text; pass `--task`
with the layer's task id when the friction traces to one. This is a log,
not a todo list — don't let it block or slow the Loop; log and keep
moving. `tweaker` reads it (via `hedgehog friction list`) once the build
reaches its Stop Condition.

## Correction Protocol

When a downstream step reveals an upstream step was wrong:

1. Stop.
2. Patch the upstream step directly, in place.
3. Fast-forward every dependent step that breaks, each its own small
   commit. If the patched step lives in a workspace package (e.g.
   `packages/hooks`, `packages/contracts`) that a running `web`/`mobile`
   dev server consumes, run that package's `nx run <pkg>:build` before
   re-verifying — the dev server resolves the package's built `dist/`,
   not its `src/`, so an unbuilt patch looks unchanged to anything
   downstream even though the source is fixed.
4. The commit messages are the explanation.
5. Resume the loop.

Use `conventional-commits` when a correction touches several steps in one
working-tree pass and needs splitting back into per-step commits.

## Phase Transition Checks

Before starting Phase B for a module, confirm:

- `hedgehog status` shows that module's `controller` task `complete`
  (equivalently, a `feat(<module>): api` commit exists).
- The contract is callable and typed (contract tests pass).

Use the `reviewer` agent for this — it checks what the mechanical gate
can't (port discipline, FK-by-ID discipline, contract shape).

Before starting Phase A for a module, confirm it's inside the stated scope
boundary from planning intake (`planner`). If not, stop and ask.

## Rules

- **Phase A closes before Phase B opens.** Every module in scope has a
  working, tested API before any hook or screen starts.
- **Sequential within a phase.** A step starts once the one before it
  compiles and passes tests.
- **Queue infra is conditional twice over** — only if the Queue add-on is
  on for this project at all (per `.hedgehog/addons.yaml`'s `queue.on`),
  and even then only when a given operation genuinely needs async
  (long-running, retries, fan-out); the normal case has no queue.
- **A wrong step gets fixed at its source** — the Correction Protocol, not
  a downstream workaround.
- **Tests gate every commit** in the sequence.
- A module's frontend code (hook, screen) is built after its API is
  committed.
- The screen step doesn't start blank — `ux-planner` runs once per module,
  after the hook is committed, before `front-end-eng` starts the screen.
- `packages/config` is the single source for shared config; a per-app
  override request signals to fix the base config at the source.

## Stop Condition

A build session ends when `hedgehog status` shows every task for every
module in scope `complete` (Phase A and Phase B both closed), or when
scope is ambiguous enough that continuing means guessing — ask one
question and wait.

On the former (a real build completion, not an ambiguity stop), offer a
fresh-context handoff before doing anything else: tell the user the
build is complete, that clearing context now costs nothing (the build
graph and the commit log hold everything), and that a `tweaker` session
is the right next step for any adjustments — it starts clean, reviews
the friction log (`hedgehog friction list`) once for a possible
discipline-improvement suggestion, and takes tweak requests one at a
time from there. Don't start making tweaks in the current, already-large
context; that's what the fresh session is for.
