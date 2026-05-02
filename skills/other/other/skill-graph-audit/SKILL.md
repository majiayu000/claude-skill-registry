---
name: skill-graph-audit
role: library
description: 'Map Skill() refs across plugins; detect hubs, isolates, and dangling targets. Use when auditing skill composition or hunting broken refs.'
version: 1.9.3
alwaysApply: false
tools: []
modules:
- modules/usage.md
- modules/interpretation.md
---

# Skill Graph Audit

## Overview

Build a directed graph of `Skill(plugin:name)` invocations across the
marketplace and surface composition patterns: which skills are heavily
referenced (hubs), which orchestrate many others (orchestrators), which
have no incoming or outgoing references (isolates), and which point at
non-existent skills (dangling references).

Replaces the manual curation step previously needed for
`docs/quality-gates.md#skill-level-quality-gate-composition` -- the
federation graph is now derivable from source.

## When To Use

- Before a documentation pass on skill composition
- After a renaming or retirement to catch broken `Skill()` references
- During quarterly audits to spot orphaned skills
- When evaluating consolidation candidates (hubs are higher-risk to merge)
- When a new skill's outbound references should be sanity-checked

## When NOT To Use

- For per-skill quality scoring -- use `Skill(abstract:skills-eval)` instead
- For frontmatter/structure validation -- use `Skill(abstract:plugin-review)`
- For hook-specific audits -- use `Skill(abstract:hooks-eval)`

## Quick Start

```bash
python3 plugins/abstract/scripts/skill_graph.py \
  --plugins-root plugins --top-n 10
```

For machine-readable output:

```bash
python3 plugins/abstract/scripts/skill_graph.py \
  --plugins-root plugins --format json --output reports/skill-graph.json
```

See `modules/usage.md` for full CLI reference and example workflows.

## Core Outputs

| Output | Meaning | Action when high |
|--------|---------|------------------|
| Hubs | Most-referenced skills | Treat as core API; retire with extreme care |
| Orchestrators | Skills that call many others | Verify each ref still resolves |
| Isolates | Zero in / zero out | Check role: library? entrypoint? typo? |
| Dangling -- bugs | Missing internal target | Fix immediately (typo or retired skill) |
| Dangling -- external | Reference to external plugin | Document plugin dependency |
| Dangling -- placeholders | Template text like `-NAME` | Verify intentional |

See `modules/interpretation.md` for false-positive guidance and
isolation taxonomy.

## Dogfood Evidence

This skill itself was scaffolded TDD-first; on first run against
`plugins/`, it caught two genuine dangling refs that the manual
audit (2026-04-25) had missed:

- `attune:makefile-generation -> abstract:makefile-dogfooder`
  (script name confused with skill name)
- `imbue:karpathy-principles -> spec-kit:speckit-clarify`
  (command referenced as skill)

Both were converted to correct command-style references in the
same session.

## Verification

Two ways to validate the audit output is trustworthy:

1. **Test-suite correctness check**: Run `pytest -o addopts=
   plugins/abstract/tests/scripts/test_skill_graph.py` to confirm
   extraction, graph construction, ranking, isolate detection, and
   dangling-ref classification all pass on the current code. The
   `-o addopts=` flag bypasses the package-wide coverage gate, which
   would otherwise fail on a single-file run.
2. **Round-trip smoke check**: Note the dangling-ref count from a
   baseline run, fix one or more flagged references, then rerun and
   verify the count drops by at least the number fixed. If the count
   does not move, the report is stale or the regex missed a syntax
   variant.

## Related Skills

- `Skill(abstract:skills-eval)` -- per-skill quality scoring
- `Skill(abstract:plugin-review)` -- plugin manifest + structure
- `Skill(abstract:hooks-eval)` -- hook-specific validation
- `Skill(abstract:rules-eval)` -- rules directory validation

## References

- Implementation: `plugins/abstract/scripts/skill_graph.py`
- Tests: `plugins/abstract/tests/scripts/test_skill_graph.py`
- Composition documentation:
  `docs/quality-gates.md#skill-level-quality-gate-composition`
- Skill role taxonomy: `docs/skill-integration-guide.md#skill-role-taxonomy`
