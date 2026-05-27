---
name: dream
description: Retired pointer — out-of-session compounding moved to Gas City.
practices:
- lean-startup
- wiki-knowledge-surface
- sre
hexagonal_role: supporting
consumes: []
produces:
- .agents/research/*.md
context_rel: []
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - TASK
  intel_scope: topic
metadata:
  tier: session
  stability: experimental
output_contract: Retired. The in-tree out-of-session compounding CLI engine was removed in soc-2rtm0; between-session knowledge compounding now runs via GC. This skill is a retirement pointer only.
---
# Dream - Retired (out-of-session compounding moved to GC)

> **Status: RETIRED (soc-2rtm0).** The in-tree out-of-session compounding
> engine and its whole CLI surface (the former always-on lane — now Gas City)
> were removed, along with the always-on background process that carried it.
> AgentOps no longer ships the out-of-session orchestration substrate —
> scheduled, between-session knowledge compounding now runs via **GC** (Gas
> City). This skill remains only as a pointer; it no longer drives an in-repo
> command.

> **Cross-vendor analog:** Anthropic Managed Agents Dreaming (research preview,
> May 2026) — scheduled session review, pattern extraction, memory curation
> between runs. AgentOps now delegates that lane to GC rather than owning it.

## What moved

The "dream cycle" (bounded `INGEST -> REDUCE -> MEASURE` knowledge compounding
between sessions) is no longer an `ao` command. Drive it through GC's
out-of-session scheduling surfaces instead. Do not invent a replacement `ao`
workflow.

## What stays in AgentOps

The KEEP primitives the dream cycle was built on are unchanged and remain
on-demand:

- `/harvest` — promote `.agents/` knowledge across rigs
- `/forge` — mine transcripts into learnings
- `/compile` — Mine → Grow → Defrag → Lint the wiki corpus
- `/inject` — JIT decay-ranked context assembly
- `/evolve` — daytime, operator-driven code compounding via `/rpi`

The nightly-CI dream-cycle proof job in `.github/workflows/nightly.yml`
(`harvest -> forge -> close-loop -> defrag -> metrics health`) still runs against
the checked-in corpus; it is built on those KEEP primitives, not on the retired
CLI engine.

## Delineation vs /evolve

`/evolve` owns the daytime code-compounding layer (operator-driven, via `/rpi`).
The knowledge-compounding layer that `/dream` used to own now lives outside
AgentOps (GC). Both still share the fitness-measurement substrate via
`corpus.Compute` / `ao goals measure`.

## Reference Documents

- [references/dream.feature](references/dream.feature) — Historical executable spec for the retired bounded bedtime loop (harvest→forge→close-loop→defrag), kept for provenance (soc-qk4b)
- [How It Works](../../docs/how-it-works.md)
- [CLI Reference](../../cli/docs/COMMANDS.md)

## See Also

- `/harvest`, `/forge`, `/compile`, `/inject` - the KEEP knowledge primitives
- `/evolve` - daytime code-compounding loop
- `/handoff` - capture explicit session closeout
