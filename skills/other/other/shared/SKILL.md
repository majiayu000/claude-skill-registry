---
name: shared
description: 'DO NOT use directly: this skill is infrastructure for other imbue skills.
  This skill provides shared patterns consumed by other imbue skills. Use when other
  imbue skills need common patterns, creating new analysis skills, ensuring consistency
  across imbue plugin.'
category: infrastructure
tags:
- shared
- patterns
- templates
- analysis
provides:
  infrastructure:
  - todowrite-patterns
  - evidence-formats
  - analysis-workflows
reusable_by:
- all imbue skills
- pensive skills
- sanctum skills
estimated_tokens: 200
modules:
- modules/todowrite-patterns.md
- modules/evidence-formats.md
- modules/anti-cargo-cult.md
version: 1.4.0
---

# Shared Infrastructure for Imbue

## Purpose

Reusable patterns for analysis workflows, evidence logging, understanding verification, and structured outputs used across imbue skills and by dependent plugins (pensive, sanctum).

## Modules

### Anti-Cargo-Cult Reasoning
The `modules/anti-cargo-cult.md` module prevents superficial technical artifacts:
- Understanding verification protocol (Five Whys)
- Cargo cult red flags (code-level, thought-level, AI-specific)
- Integration with proof-of-work, scope-guard, rigorous-reasoning
- Recovery protocol for detected cargo cult code

### TodoWrite Patterns
The `modules/todowrite-patterns.md` module documents naming conventions:
- Pattern: `skill-name:step-name`
- Common prefixes: evidence-logging, diff-analysis, review-core, catchup
- Examples from all imbue skills

### Evidence Formats
The `modules/evidence-formats.md` module standardizes evidence capture:
- Command logging format `[E1]`, `[E2]`
- Citation format `[C1]`, `[C2]`
- Artifact indexing conventions
- Reference linking in findings

### Analysis Workflows
Common workflow patterns (see individual skills for detailed modules):
- **Diff analysis**: See `diff-analysis` skill modules
- **Catchup**: See `catchup` skill modules
- **Structured output**: See `structured-output` skill

## When to Reference

- **New skill development**: Use patterns for consistency
- **Cross-plugin integration**: Reference evidence formats from pensive, sanctum
- **Template generation**: Use output formats for reports

## Integration Notes

This skill provides infrastructure used by:
- `pensive:*-review` skills via `dependencies: [imbue:evidence-logging]`
- `sanctum:git-workspace-review` for analysis patterns
- Any skill needing reproducible evidence trails
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
