---
name: mooco
description: "Custom orchestrator design notes and skill interface expectations"
license: MIT
tier: 0
allowed-tools: []
protocol: MOOCO
tags: [moollm, orchestration, design, context, safety]
related: [speed-of-light, play-learn-lift, sister-script, cursor-mirror, yaml-jazz, postel]
---

# MOOCO

> *"Deterministic orchestration around creative computation."*

This skill documents the interface surface MOOCO should provide so MOOLLM skills can run safely and predictably. It focuses on ideas, features, and interoperability, not code details.

## Core Expectations

- **Context control**: explicit working-set paging and hot/cold management
- **Safe tool boundaries**: sister scripts run in constrained envelopes
- **Event emission**: structured events for deterministic steps
- **Skill containment**: clear input/output channels and limits
- **Streaming-first**: async, SSE-native sessions with clean reconnection
- **Shared-core mindset**: open components align with private extensions

## Tooling Model (Sister Scripts as Components)

MOOCO should treat skills + sister scripts as dynamic tool components:

- Each skill can declare **multiple sister-script APIs**
- Each API exposes typed parameters and safe defaults
- Invocation is mediated by a component model (COM/OLE/IDispatch analogy)
- MCP is a supported transport layer, but not the only surface
- Skills are finer‑grained and more composable; they remain the primary focus
- The orchestrator can choose between synchronous calls and async lanes
- Skill calls can be encapsulated in one bubble/LLM iteration, or composed across many skill calls and character turns in a single epoch, or anywhere in between

## Execution Modes

- **Fire‑and‑forget**: emit a task and continue
- **Wait‑for‑response**: block on a specific result or a set (fork/join)
- **Parallel lanes**: multiple skill calls in flight
- **Dependency graphs**: schedule based on explicit edges

## Skill Safety and Mutability

- Skills may propose edits to other skills, but mutation is gated
- Skills can be locked read‑only by policy
- Deterministic steps should run before creative steps
- Untrusted skills (including imported Anthropic skills) require review and hardening
- Monitoring and audit trails are mandatory for elevated privileges
- Upgrades should be reversible and traceable

## Untrusted Skill Intake

- **Review**: inspect source, inputs, outputs, and failure modes
- **Analyze**: run skill‑snitch scans and adversarial checks
- **Bullet‑proof**: tighten permissions, constrain inputs, add guardrails
- **Monitor**: log usage, trace context, and watch for drift

## Per‑Skill Storage

Each skill gets isolated scratch and persistent storage:

- `.moollm/skills/<skill-name>/scratch/` — ephemeral, local
- `.moollm/skills/<skill-name>/store/` — durable, user‑owned

This keeps experiments safe while preserving user‑authored state.

## Integration and Uplift

- Promote stable skills into CARD/README/K‑lines for discoverability
- Cross‑link related skills in both directions
- Keep portability: skills should remain usable outside MOOCO

## Skill Compatibility

Skills should be able to declare:

- deterministic steps (handled by orchestration)
- creative steps (handled by LLM)
- context needed to run safely
- required event outputs for traceability

## Design Direction

- Prefer single-epoch simulation when possible
- Use deterministic evaluation before LLM synthesis
- Keep all state in files and event logs
- Emit traceable provenance for every step
- Favor portability across models and orchestrators

## Inheritance Notes

- MOOCO should treat working-set files as directives
- Cursor treats them as advisory; the skill surface should adapt

## Synergies

- **Speed of Light**: single-epoch simulation, multi-agent multi-turn deliberation
- **Sister Scripts**: safe, deterministic execution envelopes
- **Cursor-mirror**: introspection and traceability
- **YAML Jazz**: semantic schemas and human-readable state
- **Edgebox**: probe → analyze → call as a practical PLL precedent

## Architecture Snapshot

MOOCO favors a shared core: conversation schemas, streaming engine, provider abstraction, and tool execution that can be reused across orchestrators. This keeps skills portable and reduces lock-in to any one model or runtime.

## Kilroy Dataflow Networks

MOOCO should support Kilroy‑style dataflow:

- Events are messages, tools are nodes, skills are pipelines
- Deterministic transforms compose before LLM synthesis
- Small local models act as focused nodes in the graph
- Visual programming is a first‑class view of the same network

## GitHub as Microworld

GitHub can be treated as a composable microworld:

- repositories are rooms
- issues and pull requests are objects in play
- labels and milestones are tags and states
- cross‑repo links are portals
- commit messages, PR descriptions, and issue discussions are high‑value narrative objects that preserve intent, prompts, context, and audit trails (thoughtful‑commitment catnip)

This makes multi‑repo composition a first‑class navigation problem.

## Storage Layering

MOOCO favors layered storage:

- PostgreSQL for canonical state
- TimescaleDB for time‑series events
- pgvector for semantic recall
- SQLite for lightweight local mirrors
- Raw text corpora for evidence: Cursor chat history, historic docs, PDFs, citations, Wikipedia pages, web pages, discussion threads, and referenced papers

Layering keeps state durable, analyzable, and portable.

## Future Work

- Define a standard event payload for skill execution
- Specify a context budget contract for skills
- Document containment tiers for sister scripts

## See Also

- [MOOCO-ARCHITECTURE.md](../../../mooco/designs/MOOCO-ARCHITECTURE.md) — Full architecture with event mapping appendix
- [MOOCO-SCHEMA.md](../../../mooco/designs/MOOCO-SCHEMA.md) — Database schema and MessagePart extensions
