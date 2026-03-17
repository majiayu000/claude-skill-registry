---
name: py-test-swarm
description: Orchestrate hierarchical BioETL test swarms (L1/L2/L3) for full-audit, fix-failures, coverage-boost, optimize, and flakiness-scan with workload-based delegation, telemetry aggregation, flaky analysis, and final reporting in reports/test-swarm/task-id/FINAL-REPORT.md. Use when users request broad test campaigns, failure triage at scale, coverage expansion, or stability diagnostics across layers/providers.
---

# py-test-swarm

## Core Role
Act as L1 orchestrator by default.
Decompose work into L2/L3 agents, enforce constraints, aggregate evidence, and produce final artifacts.

## Startup Sequence
1. Read memory:
- `../../../.ai/memory/agent-memory.md`
- `../../../.ai/memory/memory-py-test-bot.md`
- `../../../.claude/agents/ORCHESTRATION.md` (sections 2-7)
2. Read profile:
- `../../../.claude/agents/py-test-swarm.md`
3. Confirm input contract:
- `task-id` (required)
- `mode` (required): `full-audit | fix-failures | coverage-boost | optimize | flakiness-scan`
- `scope` (optional, default all tests)
- `baseline-report` (optional)
- `flakiness-runs` (optional, default `5`)
4. Create artifact root: `reports/test-swarm/<task-id>/`.

## L1 Workflow
1. Run Discovery baseline commands from [l1-playbook.md](references/l1-playbook.md).
2. Build `00-swarm-plan.md` with workload scores and parallel execution plan.
3. Launch L2 agents with full task brief template from [l2-l3-task-brief.md](references/l2-l3-task-brief.md).
4. Limit concurrent L2 agents to 4; run independent scopes in parallel.
5. Collect all L2/L3 `report.md`, `metrics.json`, and telemetry JSONL.
6. Build aggregated telemetry and flaky DB using [telemetry-and-flaky-db.md](references/telemetry-and-flaky-db.md).
7. Produce `FINAL-REPORT.md` from [report-templates.md](references/report-templates.md).

## Decomposition Model
Use three axes:
- Architecture layers: `domain`, `application`, `infrastructure`, `composition`, `interfaces`
- Test types: `unit`, `integration`, `e2e`, `architecture`, `contract`, `smoke`, `performance`, `security`
- Infrastructure zones: adapters/providers, transformation, storage, DQ, retry/circuit-breaker, checkpoint/locking/heartbeat, observability, CLI

## Delegation Rules
Calculate:
```text
workload-score = files-count * complexity-factor * failing-factor * coverage-gap-factor
```

Decision:
- `< 40`: self-execute
- `40-89`: delegate to 2-3 child agents
- `>= 90`: delegate to 4-6 child agents

Fallback delegation triggers (if formula is not practical):
- test files in scope `> 30`
- failing tests `> 15`
- modules without tests `> 10`
- estimated runtime `> 20 min`
- flaky rate `> 10%` (spawn dedicated flaky triage agent)

Hierarchy limit: `L1 -> L2 -> L3` only.

## L2/L3 Protocol
L2 and L3 must follow 6 phases:
- Phase 0: discovery and workload scoring
- Phase 1: stabilization
- Phase 2: coverage expansion
- Phase 3: optimization
- Phase 4: telemetry/flakiness scan
- Phase 5: reporting

For L3 agents always prepend the mandatory leaf-agent instruction from [l2-l3-task-brief.md](references/l2-l3-task-brief.md).

## Artifact Contract
Minimum required outputs:
- `reports/test-swarm/<task-id>/00-swarm-plan.md`
- `reports/test-swarm/<task-id>/L2-*/report.md`
- `reports/test-swarm/<task-id>/L2-*/metrics.json`
- `reports/test-swarm/<task-id>/telemetry/raw/events-*.jsonl`
- `reports/test-swarm/<task-id>/telemetry/aggregated/failure-stats.csv`
- `reports/test-swarm/<task-id>/telemetry/aggregated/flaky-index.csv`
- `reports/test-swarm/<task-id>/telemetry/failure-frequency-summary.md`
- `reports/test-swarm/<task-id>/flakiness-database.json`
- `reports/test-swarm/<task-id>/FINAL-REPORT.md`

## Constraints
MUST:
- Keep architecture boundaries and no I/O in domain.
- Use `uv run python -m pytest ...` and `uv run python -m mypy --strict ...`.
- Keep swarm changes in tests/reporting artifacts; do not modify production code unless explicitly requested outside swarm.
- Use VCR/respx for HTTP tests; keep secrets out of cassettes.
- Add regression tests for fixed failures when fixes are applied.
- Provide evidence (`file + lines + command`) for architectural claims.

MUST NOT:
- Remove tests without rationale.
- Hide failures via unjustified `skip`.
- Add test-only logic in `src/bioetl/`.
- Exceed L3 depth.
- Leak secrets in logs/reports/cassettes.

## Mode Matrix
- `full-audit`: phases 0-5
- `fix-failures`: phases 0-1
- `coverage-boost`: phases 0 and 2
- `optimize`: phases 0 and 3
- `flakiness-scan`: phases 0 and 4

## Completion Criteria
Treat task as done only when:
- all active agents wrote `report.md` and `metrics.json`;
- L2 orchestrators aggregated L3 reports (if any);
- L1 generated `FINAL-REPORT.md`;
- telemetry aggregates + flaky DB are generated;
- unresolved assumptions are explicitly marked `Requires Manual Review`.

## References
- L1 runbook and command sequence: [l1-playbook.md](references/l1-playbook.md)
- L2/L3 task briefs and prompt templates: [l2-l3-task-brief.md](references/l2-l3-task-brief.md)
- Report and metrics templates: [report-templates.md](references/report-templates.md)
- Telemetry schema and flaky DB contract: [telemetry-and-flaky-db.md](references/telemetry-and-flaky-db.md)
