---
name: domain
description: Canonical vocabulary for human-AI software work.
practices:
- ddd-bounded-context
- wiki-knowledge-surface
- pragmatic-programmer
hexagonal_role: domain
consumes: []
produces:
- stdout
context_rel: []
skill_api_version: 1
context:
  window: isolated
  intent:
    mode: none
  sections:
    exclude:
    - HISTORY
    - INTEL
    - TASK
  intel_scope: none
metadata:
  tier: knowledge
  dependencies: []
  internal: false
  stability: experimental
output_contract: 'stdout: domain-language reference (loaded JIT)'
---
# Domain Skill — Ubiquitous Language for Human-AI Software Building

This is a **library skill**. It doesn't run standalone — it holds the shared
vocabulary that you, the agent, and other skills cite when describing work.

## Why this exists

AgentOps's existing skills (research, plan, crank, validate, ...) are verbs.
This skill holds the nouns and the discipline they operate on. When a session
talks about "this is a tracer bullet" or "we need a vertical slice through the
eval surface," the meaning is fixed here, not improvised.

## Status

**Tracer bullet shape with one canonical operating concept.** This skill currently holds:

- 6 structural primitives (Entry, Index, Citation, Primitive, Slice, Anti-Pattern)
- 1 test entry (Tracer Bullet) written using only citations to the 6 primitives
- 1 canonical operating concept (Context Density Rule)

If the test entry can describe its own concept using only the primitives, the
shape works and we grow the corpus by adding more entries — never new
structural primitives without operator consent.

## How to use this skill

1. Read `references/INDEX.md` first — it lists every entry by kind and status.
2. Load only the entries relevant to the current work. Do not preload the
   whole corpus — that defeats the JIT purpose.
3. When applying an entry, cite it: include the entry slug in your output, plan,
   commit message, or `bd` issue body so future sessions can trace the
   reasoning.
4. When you find a concept missing or misnamed, add a draft entry under
   `references/` and update `INDEX.md`. Promotion from `draft` to `canonical`
   requires operator approval.

## Entries (tracer-bullet set)

Structural primitives (the architecture):

- [references/domain.feature](references/domain.feature) — Executable spec: load-on-demand corpus, draft→canonical ratchet, vocabulary root (soc-qk4b)
- [`references/entry.md`](references/entry.md) — Entry: the atomic concept doc
- [`references/index-primitive.md`](references/index-primitive.md) — Index: the discovery surface (concept)
- [`references/citation.md`](references/citation.md) — Citation: how Entries reference each other and how agents claim use

Vocabulary nouns (the working units):

- [`references/primitive.md`](references/primitive.md) — Primitive: atomic capability (skill, hook, CLI command, eval suite)
- [`references/slice.md`](references/slice.md) — Slice: vertical work unit cutting through multiple Primitives
- [`references/anti-pattern.md`](references/anti-pattern.md) — Anti-Pattern: documented mistake with cost when ignored

Test entry:

- [`references/tracer-bullet.md`](references/tracer-bullet.md) — Tracer Bullet: described using only citations to the six primitives above

Operating discipline:

- [`references/context-density-rule.md`](references/context-density-rule.md) — Context Density Rule: every context token carries intent, boundary, evidence, decision, constraint, or next action
- [`references/behavior-shaping.md`](references/behavior-shaping.md) — Behavior Shaping: the ABC register (antecedent/behavior/consequence/reinforcement/extinction/shaping); building agent capability is operant conditioning, not specification

Catalog:

- [`references/INDEX.md`](references/INDEX.md) — full corpus index

## Domain as a scoped RPI loop (runtime)

The `Slice` primitive above has a runtime counterpart: a **domain slice** can
be run as a scoped Research-Plan-Implement loop. A *domain* is a named vertical
slice with an explicit boundary contract — a manifest at
`docs/domains/<name>/manifest.yaml` listing the Primitives the slice may touch,
its goal, and its decision gate.

```bash
ao rpi phased --domain <name> "<goal>"        # run RPI scoped to a domain slice
ao rpi phased --scaffold-domain <name>         # write a manifest template, then exit
ao rpi phased --scaffold-domain <name> --force # overwrite an existing manifest
```

`--domain` loads `docs/domains/<name>/manifest.yaml` and carries its boundaries
into every phase prompt, so the loop stays inside the slice. `--scaffold-domain`
writes the manifest template and exits without running RPI — use it to bootstrap
a new slice, then fill in the boundary before running. The manifest schema and
resolution rules are in `docs/adr/ADR-0004`; the `/scaffold` skill documents the
bootstrap step.

## What's NOT here

- Procedural how-tos (those live in other skills)
- Repo conventions (those live in `skills/standards/`)
- Findings, learnings, patterns (those live in `.agents/`)
- Product framing (lives in `PRODUCT.md`)

## See also

- `skills/standards/SKILL.md` — repo coding standards (sibling library skill)
- `docs/architecture/primitive-chains.md` — concrete AgentOps primitive layers
  (Mission/Discovery/Risk/Execution/Validation/Learning/Ratchet/Continuity)
  that compose the domain into chains
