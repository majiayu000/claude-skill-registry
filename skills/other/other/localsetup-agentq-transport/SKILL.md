---
name: localsetup-agentq-transport
description: Agent Q bidirectional transport client - file_drop ship/ingest, mail pull/ship (including strict gpg preencrypted), registry validation, queue-pending, archive-prune. Use when shipping or ingesting sealed PRD manifests between agents over shared folders or mail; when editing agent_trust_registry, manifest.schema.json, or agentq CLI.
metadata:
  version: "1.0"
---

# Agent Q transport

## Purpose

Operate the **agentq_transport_client** CLI and related config so Agent A and Agent B exchange PRDs and artifacts via **file_drop** (shared directory + ready marker) or **mail** (policy-gated), with OpenPGP outer blobs and optional strict gpg sign-then-encrypt.

## When to use

- User says "ship PRD to agent", "ingest agentq blob", "file-drop-poll", "mail-pull Agent Q", "strict gpg ship".
- Editing `agent_trust_registry.yaml`, `agent_queue.example.yaml`, or `manifest.schema.json`.
- Setting up same-machine different-repos handoff (see AGENTIC_AGENT_Q_SCENARIOS.md).

## Key paths

| Path | Role |
|------|------|
| `_localsetup/tools/agentq_transport_client/agentq_cli.py` | CLI entrypoint |
| `_localsetup/tools/agentq_transport_client/docs/USER_GUIDE.md` | Commands and examples |
| `_localsetup/tools/agentq_transport_client/docs/ADMIN_GUIDE.md` | Policy, rotation, mail automation |
| `_localsetup/config/agent_trust_registry.example.yaml` | Registry template |
| `_localsetup/config/manifest.schema.json` | Inner manifest schema |

## Skills to load with this

- **localsetup-mail-protocol-control** – mail adapter backend; `preencrypted_openpgp_armored` for ship-mail-strict.
- **localsetup-agentic-prd-batch** – batch reads `in/` only; version mismatch and structured queue.

## Docs

- [AGENTIC_AGENT_TO_AGENT_PROTOCOL.md](../../docs/AGENTIC_AGENT_TO_AGENT_PROTOCOL.md)
- [AGENTIC_AGENT_Q_SCENARIOS.md](../../docs/AGENTIC_AGENT_Q_SCENARIOS.md)
- [AGENTIC_AGENT_Q_BIDIRECTIONAL_BUILD_SPEC.md](../../docs/AGENTIC_AGENT_Q_BIDIRECTIONAL_BUILD_SPEC.md)

## Smoke / verify

From repo root:

```bash
python _localsetup/tools/agentq_transport_client/agentq_cli.py --help
python3 -m pytest _localsetup/tools/agentq_transport_client/tests/ -q
```

Skill directory has no bundled scripts; CLI lives under `tools/agentq_transport_client/`.
