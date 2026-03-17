---
name: codex-sdk
description: >-
  Architect-level guidance, workflows, and scripts for building agentic coding systems with OpenAI Codex. Use for Codex SDK (@openai/codex-sdk) threads + streaming JSONL events; Codex CLI automation (codex exec, output schema, JSONL, resume); MCP server usage (codex mcp-server) and dynamic tool integration; multi-agent orchestration with OpenAI Agents SDK (handoffs, gating, tracing); durable state, caching, and memory using SQLite; safe-by-default sandbox/approval patterns and execpolicy rules.
---

# Codex SDK + Codex CLI (master skill)

Build reliable, auditable, multi-step coding workflows that scale from a single run to multi-agent orchestration.

## ExecPlans (durable planning)

For multi-hour work, keep intent durable across compaction/restarts using an **ExecPlan**:

- Contract: `references/execplans.md`
- Template + rules: `.agent/PLANS.md` (use `scripts/init_agent_workspace.py` to bootstrap a repo)
- ExecPlan skeleton: `assets/templates/execplan.md` (or generate a file with `scripts/new_execplan.py`)

## Workflow decision tree

1. **Need a scriptable one-shot in CI or cron?** → use `codex exec` (`references/codex-cli-exec.md`)
2. **Need a server-side app controlling Codex programmatically?** → use `@openai/codex-sdk` (`references/codex-sdk-typescript.md`)
3. **Need multi-agent orchestration or dynamic tools?** → run `codex mcp-server` and orchestrate via OpenAI Agents SDK (`references/mcp-and-agents-sdk.md`)
4. **Need durability across runs (memory, caching, resumable state)?** → persist run metadata and event logs in SQLite (`references/state-memory-sqlite.md`)

## Default workflow (safe + production-friendly)

1. Inventory inputs (repo root, diffs, failing commands, constraints).
2. Choose sandbox + approvals (least privilege; default to read-only).
3. Plan in explicit steps (short, verifiable; include stop conditions).
4. Use structured outputs (JSON Schema) and validate before acting.
5. Record an audit trail (JSONL events → SQLite).
6. Verify (re-run tests/lint/format; stop).

## Durable state and “memory” (SQLite)

SQLite is the simplest reliable substrate for:

- recording every `codex exec --json` event as an immutable audit log
- indexing runs by repo, branch, and purpose
- storing `threadId` so runs can resume deterministically
- caching expensive analysis artifacts (diff summaries, inventories, dependency graphs)

### Use the bundled scripts

- Initialize a DB:
  - `python3 scripts/codex_jsonl_to_sqlite.py --db codex-runs.sqlite --init`
- Ingest a JSONL run:
  - `codex exec --json "<prompt>" | python3 scripts/codex_jsonl_to_sqlite.py --db codex-runs.sqlite --run-label "ci-autofix"`
- Summarize runs:
  - `python3 scripts/codex_sqlite_report.py --db codex-runs.sqlite --latest`

## Multi-agent orchestration (recommended shape)

Use:

- a single **orchestrator** responsible for gating and artifact checks
- multiple **scoped worker agents** with strict deliverables
- structured outputs at boundaries (handoff payloads, review findings, test results)
- traces/telemetry to debug and tune

Details: `references/mcp-and-agents-sdk.md`

## Safety and policy

Prefer:

- analysis-only: `sandbox: read-only`, `approval-policy: never`
- controlled edits: `sandbox: workspace-write`, `approval-policy: on-request` / `on-failure`
- block risky commands with `execpolicy` rules (`references/safety-and-execpolicy.md`)

## Resources

### references/
- `references/codex-sdk-typescript.md` – SDK patterns (threads, streaming, schemas)
- `references/codex-cli-exec.md` – CLI patterns (JSONL, schema files, resume)
- `references/mcp-and-agents-sdk.md` – Codex as MCP server + multi-agent orchestration
- `references/agents-sdk-consistent-workflows.md` – gated handoffs + traces with Codex MCP + Agents SDK
- `references/execplans.md` – ExecPlans for long-running work across compaction
- `references/state-memory-sqlite.md` – SQLite schema + memory/caching patterns
- `references/safety-and-execpolicy.md` – sandboxing, approvals, prompt-injection defenses
- `references/codex-config-knobs.md` – config keys and feature flags that matter
- `references/orchestration-patterns.md` – planner/executor/verifier and orchestrator/worker patterns
- `references/rag-and-memory.md` – SQLite-first shared memory and RAG guidance
- `references/context-personalization.md` – state + memory notes personalization patterns (Agents SDK)

### scripts/
- `scripts/codex_jsonl_to_sqlite.py` – ingest Codex JSONL into SQLite
- `scripts/codex_sqlite_report.py` – summarize runs from SQLite
- `scripts/init_agent_workspace.py` – create `.agent/AGENTS.md` + `.agent/PLANS.md` from templates
- `scripts/new_execplan.py` – generate `execplans/execplan-*.md` from the ExecPlan template

### assets/
- `assets/templates/` – copy/paste templates (ExecPlan, prompts, schemas)
- `assets/templates/agents-sdk/` – Agents SDK starter snippets (MCP stdio, sessions, personalization)
