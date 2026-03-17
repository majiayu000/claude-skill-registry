---
name: edictum-ee
description: Implement features in the Edictum Enterprise layer (ee/). Use when the task touches PII detection backends, enterprise audit sinks, server, auth, sequences, or NL authoring. ee/ imports from core freely.
---

# Edictum Enterprise Implementation

Read CLAUDE.md first. Understand the tier boundary before writing code.

## Scope

Everything under `ee/` is enterprise (proprietary license). This includes:

- PII detection (`ee/pii/`) — RegexPIIDetector, PresidioPIIDetector, CompositePIIDetector
- Audit sinks (`ee/sinks/`) — Webhook, Splunk HEC, Datadog
- Server (`ee/server/`) — Central policy server, hot-reload, dashboard
- Auth (`ee/auth/`) — JWT/OIDC verification, SSO
- Sequences (`ee/sequences/`) — Sequence-aware contracts
- NL authoring (`ee/nl_authoring/`) — Natural language -> YAML generation

## The ONE RULE

**ee/ imports from core freely. Core NEVER imports from ee/.**

All ee/ features implement protocols defined in core:
- PII detectors implement `PIIDetector` from `src/edictum/pii.py`
- Audit sinks implement `AuditSink` from `src/edictum/audit.py`

## Workflow

1. **Read CLAUDE.md** — understand boundaries, what's in core vs ee/
2. **Check if the protocol exists in core** — if not, create it in core first (that's an edictum-oss task)
3. **Read the Linear ticket** or user description
4. **Scope with user** — confirm approach before writing code
5. **Implement in ee/** — follow core conventions
6. **Test** — ee/ tests live alongside the ee/ code or in `tests/test_ee/`
7. **Commit** — conventional commits, no Co-Authored-By

## What's in core vs ee/

| Core (MIT) | Enterprise (ee/) |
|---|---|
| PIIDetector protocol | RegexPIIDetector, PresidioPIIDetector |
| AuditSink protocol + Stdout + File (.jsonl) | Webhook, Splunk HEC, Datadog sinks |
| StorageBackend protocol + MemoryBackend | (no Redis/DB — dropped) |
| YAML contract engine | pii_detection YAML shorthand |
| Session model (single-process) | Cross-agent session tracking |

## ee/ Directory Structure

```
ee/
├── LICENSE           (proprietary, separate from root MIT)
├── pii/
│   ├── regex.py      RegexPIIDetector
│   ├── presidio.py   PresidioPIIDetector
│   └── composite.py  CompositePIIDetector
├── sinks/
│   ├── webhook.py    WebhookAuditSink
│   ├── splunk.py     SplunkHECSink
│   └── datadog.py    DatadogSink
├── server/           (Phase 4)
├── auth/             (Phase 4)
├── sequences/
└── nl_authoring/
```

## Do NOT

- Modify core code to import from ee/
- Put ee/ implementations in src/edictum/
- Implement dropped features (Redis/DB StorageBackend, reset_session)
