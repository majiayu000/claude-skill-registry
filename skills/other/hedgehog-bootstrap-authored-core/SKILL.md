---
name: hedgehog-bootstrap-authored-core
description: Use once, at the start of a new Hedgehog project on an authored core (`hedgehog-core-design` wrote `.hedgehog/core.yaml`), to generate a verified workspace for the stack `hedgehog-core-design` chose. Runs as the `bootstrap` agent's only move on this core, and closes Bootstrap.
---

# Hedgehog Bootstrap — authored core

Lands the workspace for a project whose core `hedgehog-core-design`
designed. `hedgehog init` never scaffolds anything core-specific until a
core is actually chosen, so nothing needs clearing here — this skill is
the first thing that writes a workspace for this project. The stack
varies per project (`hedgehog-core-design`'s Step 2 stack table), so it's
generated live from the ecosystem's own tooling and verified before it's
committed.

## Steps

### 1. Confirm this hasn't already run

Check for a `feat(<project>): workspace` commit matching
`.hedgehog/core.yaml`'s `id` (`git log --oneline --grep="^feat("`), or
the presence of a root config file the stack in `core-design.md` would
produce (e.g. `wxt.config.ts` for a WXT browser extension,
`pyproject.toml` for a Python CLI). Either means this already ran — stop
there. A workspace that looks wrong is a Correction Protocol case against
the specific file.

### 2. Fill in `CLAUDE.md`'s core section

Root `CLAUDE.md` was landed by `init` as a shell with its
`{{CORE_SECTION}}` placeholder still unfilled (no core was known yet).
Read `src/templates/CLAUDE.core.authored.md` from the installed Hedgehog
package and write its contents in place of the placeholder — every other
line in root `CLAUDE.md`, including the `{{PROJECT_NAME}}`/
`{{PROJECT_SUMMARY}}` values `planner` already filled at planning intake,
stays untouched.

If the placeholder is already filled (a project that ran `init` with an
explicit core flag and only reached an authored core through a later
redesign), this step is a no-op — move on.

### 3. Read the stack choice

Read `.hedgehog/core-design.md`'s Step 2 record (language, package
manager, named framework(s), test runner) and `.hedgehog/core.yaml`'s
`id` and `layers`. These two files are the only inputs — don't re-derive
the stack from the project description; that decision was already made
and locked at `hedgehog-core-design`'s Confirm & Lock.

### 4. Generate the workspace

Scaffold the stack named in `core-design.md` at the repo root using that
ecosystem's own official generator — the one its documentation puts on
the getting-started page. A generator already encodes the conventions,
lockfile, and config layout that ecosystem expects, which is why this
step runs one rather than hand-writing a skeleton.

Generator CLIs, their flags, and their names change between releases, so
confirm the current invocation from the tool's own documentation before
running it. Working from memory here is how a bootstrap fails on a
renamed flag. Where a framework ships a generator (WXT, Electron, a web
framework), that generator is the entry point; where the language's
toolchain is the generator (`cargo`, `go mod`, `uv`, `pnpm`), that is.

By the end of this step the workspace has, whatever the stack:

- A dependency manifest and lockfile, with the framework(s) and test
  runner from `core-design.md` installed.
- A test runner wired to a command, so a layer's `verify` can call it.
- A build or typecheck command, where the language has one.
- Source directories that the layer `scope` globs in `.hedgehog/core.yaml`
  actually match.

Strip anything the generator scaffolds that collides with Hedgehog's own
root conventions — its own `AGENTS.md`, `CLAUDE.md`, `README.md`, or
workspace manifest. A generator written for standalone repos doesn't know
it's landing inside a Hedgehog project's root, and those files shadow the
real ones.

A gap between the generated workspace and `.hedgehog/core.yaml` — a
`verify` command naming a test runner the generator didn't wire, a
`scope` glob pointing at a directory the stack doesn't produce — is a
mismatch between the design and this step. `core.yaml` is locked and this
step conforms to it: close the gap by wiring what the design expects.
Where the design asks for something the stack genuinely can't provide,
stop and report it.

### 5. Install and verify

Install dependencies via the ecosystem's package manager, then run every
layer's `verify` command from `.hedgehog/core.yaml` once, in order,
against the freshly generated workspace. Each should pass clean: with no
domain content yet, this checks that the toolchain wiring those commands
depend on actually works.

A `verify` command that fails here fails for a reason worth naming
before any layer is built on top of it — a missing test runner, a script
the generator didn't add, a path that doesn't exist. Fix the generation
(step 4), then re-run this step.

### 6. Commit

```
feat(<id>): workspace
```

using `.hedgehog/core.yaml`'s `id`. One commit for the whole of this
core's bootstrap, which closes Bootstrap. State plainly that
`hedgehog-authored-loop` owns everything from here, one layer at a time.

## Constraints

- Run once per project, as the `bootstrap` agent's only move on an
  authored core — never invoked standalone.
- The stack choice, layer sequence, and every `core.yaml` field are
  locked at `hedgehog-core-design`'s Confirm & Lock. This skill executes
  that design. A stack or layer that turns out wrong once generation is
  underway is a Correction Protocol case through `planner`.
- Write no domain content in the generated workspace — no business
  logic, no first layer's files. That's the first build task, started
  once this Bootstrap commit lands.
- Never overwrite `{{PROJECT_NAME}}`/`{{PROJECT_SUMMARY}}` in root
  `CLAUDE.md` while filling `{{CORE_SECTION}}` — those are `planner`'s
  content, not this skill's.
