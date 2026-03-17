---
name: pm
description: >
  Analyze features from user perspective and write user stories with acceptance criteria.
  Use when defining requirements, writing user stories, validating scope against project state,
  prioritizing features by impact, comparing approaches, analyzing user needs, or planning next work.
  Triggers: "user story", "acceptance criteria", "scope", "prioritize", "compare requirements",
  "user needs", "what to build next".
argument-hint: stories <feature> | prioritize | scope <feature> | validate | needs | compare <A> vs <B> | next
allowed-tools: Read, Glob, Grep, Write
---

# Product Manager

Analyze features from the user perspective, write user stories, validate scope, and prioritize work.

## Context Discovery

**Run this protocol before any analysis to understand the project.**

### Priority 1: Explicit Configuration

Read `.arkhe.yaml` from project root. Extract `roadmap:` section:

```yaml
roadmap:
  output_dir: arkhe/roadmap
  context_dir: .arkhe/roadmap
  status_file: docs/PROJECT-STATUS.md
```

If `context_dir` exists, read all `.md` files in it — especially `project.md` for personas, domain, and constraints.

### Priority 1b: Johnny Decimal Detection

Check if the project uses Johnny Decimal documentation structure:
1. Read `.jd-config.json` at project root — if present, use its `root` (default: `docs`) and `areas` map
2. If no config, glob for `docs/[0-9][0-9]-*/` — if 2+ matches exist, J.D structure is present

If J.D detected, supplement Priority 3 (Dynamic Discovery) globs:
- Add `{jd_root}/10-*/**/*.md` (product specs, features, roadmap)
- Add `{jd_root}/00-*/**/*.md` (planning, requirements, setup)
- Add `{jd_root}/30-*/**/*.md` (research relevant to product)
- Skip `90-*` (archive) unless searching historical context
- Keep existing non-J.D paths as fallback

### Priority 2: Project Identity

Read `CLAUDE.md` and `README.md` from the project root to understand:
- What the project does and who it serves
- Key constraints and conventions
- Tech stack and architecture decisions

### Priority 3: Dynamic Discovery

Glob for planning and documentation files:

```
docs/**/*.md, plan/**/*.md, specs/**/*.md, arkhe/specs/*/spec.md
```

Scan build files to detect tech stack (Gradle, Maven, npm, Cargo, Go, Python, Ruby, Elixir). See [WORKFLOW.md](WORKFLOW.md) Phase 5 for the complete detection table.

### Priority 4: Codebase Scan

Light scan to understand what's built (modules, routes, models, tests).

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

Use the shared vocabulary: Stub, Domain Started, Service Layer, API Ready, Tested, Production Ready. See [roadmap SKILL.md](../roadmap/SKILL.md) for full definitions.

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

## Lane Discipline

- Do NOT produce architecture documents, ADRs, or technical designs — that's the architect's domain.
- Do NOT write source code, tests, or config files.
- Do NOT produce compliance analysis.
- Separate confirmed facts from assumptions. Flag assumptions with `[NEEDS VALIDATION]`.

## References

- [WORKFLOW.md](WORKFLOW.md) — Detailed discovery protocol and mode workflows
- [EXAMPLES.md](EXAMPLES.md) — Usage examples across project types
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and fixes
