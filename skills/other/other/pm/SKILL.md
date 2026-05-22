---
name: pm
description: >
  Analyze features from user perspective and write user stories with acceptance criteria.
  Use when defining requirements, writing user stories, validating scope against project state,
  prioritizing features by impact, comparing approaches, analyzing user needs, or planning next work.
  Triggers: "user story", "acceptance criteria", "scope", "prioritize", "compare requirements",
  "user needs", "what to build next".
argument-hint: "[--deep] stories <feature> | prioritize | scope <feature> | validate | needs | compare <A> vs <B> | next"
allowed-tools: Read, Glob, Grep, Write
---

# Product Manager

Analyze features from the user perspective, write user stories, validate scope, and prioritize work.

## Context Discovery

Run the shared context discovery protocol in [CONTEXT_DISCOVERY.md](../../references/CONTEXT_DISCOVERY.md). Execute all phases in order. Store results for use in analysis below.

## Arguments

Parse from `$ARGUMENTS`:

| Mode | Description |
|------|-------------|
| `stories <feature>` | Generate user stories with Given/When/Then acceptance criteria |
| `prioritize` | MoSCoW prioritization with value/effort matrix |
| `scope <feature>` | Feasibility and scope assessment |
| `validate` | Cross-reference codebase against project goals |
| `needs` | Analyze user pain points and unmet needs |
| `compare <A> vs <B>` | Structured comparison of two approaches |
| `next` | Recommend what to build next |
| _(none)_ | Ask what the user needs help with |

## Mode Execution

| Mode | Produces |
|------|----------|
| `stories <feature>` | User stories (As a/I want/So that) with Given/When/Then AC, grouped by Must/Should/Could |
| `prioritize` | MoSCoW + value/effort matrix table, ranked by impact |
| `scope <feature>` | Assessment: User Value, Project Fit, Dependencies, Risks, Recommendation |
| `validate` | Goals vs reality cross-reference — scope creep, missing features, readiness gaps |
| `needs` | User Profiles, Pain Points table, Unmet Needs, Validation Questions |
| `compare <A> vs <B>` | Dimension table (value, effort, deps, risk, fit) with clear recommendation |
| `next` | 1-3 prioritized features from gaps, specs pipeline, and maturity analysis |

See [WORKFLOW.md](WORKFLOW.md) for detailed execution steps and output templates per mode.

## Module Maturity Scale

Use the shared vocabulary in [MATURITY_SCALE.md](../../references/MATURITY_SCALE.md).

## Output Rules

- **Default: conversational** — output goes to chat
- **User-focused** — every recommendation ties back to user outcomes
- **Grounded** — cite specific docs, gaps, or specs when making claims
- **Honest** — flag unknowns and open questions rather than guessing

## File Persistence

After producing the analysis, ask the user:

> **Save this analysis to `{output_dir}/requirements/{filename}.md`?**

Where `{output_dir}` comes from `.arkhe.yaml` (default: `arkhe/roadmap`).

| Mode | Filename Pattern |
|------|-----------------|
| `stories <feature>` | `{feature-slug}-stories.md` |
| `prioritize` | `{YYYY-MM-DD}-priorities.md` |
| `scope <feature>` | `scope-{feature-slug}.md` |
| `validate` | `{YYYY-MM-DD}-validation.md` |
| `needs` | `{YYYY-MM-DD}-needs.md` |
| `compare <A> vs <B>` | `{a-slug}-vs-{b-slug}.md` |
| `next` | `{YYYY-MM-DD}-next.md` |

## Deep Mode (`--deep`)

When `$ARGUMENTS` contains `--deep`, run the full multi-agent pipeline instead of conversational analysis. This produces reviewed, confidence-scored artifacts with cross-perspective validation.

See [WORKFLOW.md](WORKFLOW.md) § Deep Pipeline for the 5-phase execution protocol.

**Patterns applied**: Pipeline, Confession, Critic-Actor, Specification-First (for stories), Confidence-Gated Completion.

## Lane Discipline

See the PM section of [LANE_DISCIPLINE.md](../../references/LANE_DISCIPLINE.md). Stay in your lane.

## References

- [WORKFLOW.md](WORKFLOW.md) — Detailed discovery protocol and mode workflows
- [EXAMPLES.md](EXAMPLES.md) — Usage examples across project types
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and fixes
