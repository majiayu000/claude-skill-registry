---
name: "repository-drift-control"
description: "Enforce coordinated updates across specs, templates, prompts, samples, and docs to prevent repository guidance drift."
metadata:
  source_docs: "AGENTS.md, README.md, specs/context_aware_ai_session_spec.md"
  workflow_type: "governance"
---

# Repository Drift Control

## Purpose
Prevent divergence between authoritative specification, operational prompts/templates, and repository-facing documentation.

## When To Use
- Use this skill when specification or governance files change.
- Use this skill during repo-wide refactors affecting canonical paths or precedence rules.
- Do not use this skill for isolated content edits without cross-artifact impact.

## Required Inputs
- Changed authoritative artifact(s), especially `specs/context_aware_ai_session_spec.md`.
- Current canonical path map.
- List of dependent files expected to be audited.

## Workflow
1. Identify source-of-truth changes and affected dependency set.
2. Audit templates, prompts, samples, README, and AGENTS for alignment.
3. Apply consistent terminology and path references.
4. Verify policy and precedence remain coherent after updates.
5. Record drift-control outcomes in commit/PR summary.

## Output Expectations
- Aligned artifacts with no stale references.
- Stable canonical paths and precedence documentation.
- Clear audit trail of what was updated and why.

## Resources
- Governance contract: `../../AGENTS.md`
- Repository guide: `../../README.md`
- Authoritative model: `../../specs/context_aware_ai_session_spec.md`

## Constraints And Safety
- Treat specification as authoritative when conflicts exist.
- Keep guidance provider-neutral.
- Preserve canonical path stability unless explicitly migrating.
- Avoid partial updates that leave dependent artifacts inconsistent.
