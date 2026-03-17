---
name: documentation-cascade-audit
description: Run a hierarchical documentation audit for BioETL using cascade decomposition across doc domains (architecture, providers, contracts, operations, onboarding), aggregate findings into one prioritized report, and generate an actionable remediation plan. Use when users request large-scale doc audits, stale-doc cleanup, or coordinated doc reconciliation after major refactors/releases.
---

# Documentation Cascade Audit

## Overview

Coordinate a multi-scope documentation audit where each scope is analyzed separately and then merged into a single decision-ready report.
Use this skill when a single-pass manual review is too large or error-prone.

## Startup Context

Read, in this order:
1. `../../../.ai/memory/agent-memory.md`
2. `../../../.claude/agents/ORCHESTRATION.md`
3. `../documentation-audit/SKILL.md`
4. `../documentation-audit/references/audit-checklist.md`
5. `../documentation-audit/references/report-template.md`

## Cascade Workflow

1. Build audit shards.
- Create shard scopes by domain:
  - `docs/01-overview*`, `README.md`, `mkdocs.yml`
  - architecture/ADR docs
  - provider docs
  - contracts/schemas docs
  - operations/monitoring/runbook docs
- Keep shards non-overlapping when possible.

2. Execute shard audits in parallel (conceptually or via subagents if available).
- For each shard, apply the checklist from `documentation-audit`.
- Capture findings with severity and evidence (`file + lines + command`).

3. Normalize findings.
- Deduplicate repeated findings across shards.
- Merge equivalent root causes under one canonical finding.
- Keep conflicting findings in a dedicated `Needs Clarification` section.

4. Produce consolidated outputs.
- Consolidated audit report.
- Prioritized remediation backlog (`P1/P2/P3`).
- Sequenced update plan with effort estimate.

## Deliverables

Required artifacts:
1. `reports/plans/<task-id>/cascade-audit-report.md`
2. `reports/plans/<task-id>/cascade-remediation-plan.md`
3. `reports/plans/<task-id>/cascade-open-questions.md`

## Quality Gates

- Every high-severity claim has evidence.
- Every proposed doc change maps to a concrete file path.
- RULES/REQUIREMENTS/ADRs consistency is explicitly checked.
- The final plan distinguishes factual drift vs style improvements.

## Constraints

MUST:
- Prefer documenting current system behavior over intended behavior.
- Mark unresolved uncertainties as `Requires Manual Review`.
- Keep architecture statements verifiable against code.

MUST NOT:
- Modify production code in this workflow.
- Delete documentation without explicit user approval.
- Hide contradictions between docs and code.

SHOULD:
- Group edits into small, reviewable change sets.
- Provide before/after snippets for high-impact doc changes.

## Handoff Format

Return:
1. Status: `Completed | Partially Completed | Blocked`
2. Top findings by severity
3. File list for proposed changes
4. Open questions requiring user decisions
5. Link to `cascade-audit-report.md`
