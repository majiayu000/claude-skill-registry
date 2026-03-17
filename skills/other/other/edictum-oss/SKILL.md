---
name: edictum-oss
description: Implement features in the Edictum OSS core (src/edictum/). Use when the task touches pipeline, adapters, YAML engine, CLI, audit, envelope, or session. Core NEVER imports from ee/.
---

# Edictum OSS Core Implementation

Read CLAUDE.md first. Understand the tier boundary before writing code.

## Scope

Everything under `src/edictum/` is OSS core (MIT). This includes:

- Pipeline (`pipeline.py`) — GovernancePipeline, PreDecision, PostDecision
- Envelope (`envelope.py`) — ToolEnvelope, Principal, create_envelope()
- Contracts (`contracts.py`) — @precondition, @postcondition, @session_contract, Verdict
- YAML engine (`yaml_engine/`) — loader, evaluator, compiler, templates
- Adapters (`adapters/`) — all 6 framework adapters
- Audit (`audit.py`) — AuditEvent, StdoutAuditSink, FileAuditSink, RedactionPolicy
- Session (`session.py`) — Session, MemoryBackend
- CLI (`cli/`) — validate, check, diff, replay, test
- Telemetry (`telemetry.py`) — OTel spans, GovernanceTelemetry
- Protocols (`pii.py`) — PIIDetector protocol, PIIMatch dataclass (interface only)

## The ONE RULE

**Core code NEVER imports from ee/.** If you need functionality from ee/, define a protocol/interface in core and let ee/ implement it.

## Workflow

1. **Read CLAUDE.md** — understand boundaries and dropped features
2. **Read the Linear ticket** or user description
3. **Read relevant source files** before proposing changes
4. **Scope with user** — confirm approach before writing code
5. **Implement** — small, focused changes
6. **Behavior test** — every new/changed API parameter gets a test in `tests/test_behavior/test_{module}_behavior.py`
7. **Docs-code sync** — `pytest tests/test_docs_sync.py -v`
8. **Adapter parity** — if touching adapters: `pytest tests/test_adapter_parity.py -v`
9. **Test** — `pytest tests/ -v` then `ruff check src/ tests/`
10. **Commit** — conventional commits, no Co-Authored-By

## Conventions

- Frozen dataclasses for immutable data
- All pipeline/session/audit methods are async
- `from __future__ import annotations` in every file
- Type hints everywhere
- Test file per module: `tests/test_{module}.py`

## Do NOT

- Import from `ee/` — core is self-contained
- Implement Redis/DB StorageBackend — dropped feature
- Implement PII detection backends in core — those go in ee/
- Add Webhook/Splunk/Datadog sinks to core — those go in ee/
- Accept a parameter without testing its observable effect — if it's accepted, it must DO something testable
- Document a feature that doesn't exist in code — `pytest tests/test_docs_sync.py -v` catches this
- Ship an adapter change without running parity checks — `pytest tests/test_adapter_parity.py -v`
