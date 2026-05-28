---
name: localsetup-mail-protocol-control
description: Provide full SMTP and IMAP account control for delegated mailboxes with attachment-first MIME handling and full-envelope encryption. Use when an agent must read, send, organize, decrypt, and manage mailbox state with strict admin controls.
metadata:
  version: "1.2"
---

# Mail protocol control

## Purpose

Give an AI agent full operational control of delegated SMTP and IMAP accounts while keeping safety and governance in one place. This skill is built for deterministic tool calls, low token usage, and strict policy enforcement.

## When to use

- User asks for agent-driven mailbox automation over SMTP or IMAP.
- User needs policy-controlled read, write, and destructive mailbox actions.
- User needs token-efficient MCP tools for mail triage and response workflows.
- User needs auditable account actions with confirmation gates for high-impact operations.

## Scope

- In scope: SMTP and IMAP.
- Out of scope for v1: POP3.

## Architecture

- Python domain layer:
  - SMTP via `smtplib`.
  - IMAP via `imaplib`.
- Attachment-first MIME envelope support for send and fetch paths.
- Full-envelope encryption and decryption engine:
  - PSK AES-GCM.
  - Password-derived AES-GCM.
  - Pure-Python OpenPGP.
- Policy gate for all mutating operations.
- MCP bridge with compact atomic and composite tools.
- Confirmation token lifecycle for threshold-gated destructive operations.

## Tooling layout

```
_localsetup/skills/localsetup-mail-protocol-control/
├── SKILL.md
├── scripts/
│   ├── mail_protocol_control.py
│   ├── mail_types.py
│   ├── mail_utils.py
│   ├── policy_engine.py
│   ├── crypto_types.py
│   ├── crypto_engine.py
│   ├── mcp_server.py
│   └── tests/
│       └── test_mail_protocol_control.py
└── references/
    ├── SMTP_IMAP_OPERATION_MATRIX.md
    ├── MCP_TOOL_SCHEMA.md
    ├── POLICY_SCHEMA.md
    ├── CREDENTIAL_PROVIDER_CONTRACT.md
    ├── USER_GUIDE.md
    ├── ADMIN_GUIDE.md
    ├── API_EXAMPLES.md
    ├── TROUBLESHOOTING.md
    ├── ENCRYPTION_MODEL.md
    └── KEY_MANAGEMENT.md
```

## Admin controls

- Policy profiles: `full`, `restricted`, `read_only`.
- Action-level allow and deny lists.
- Threshold controls for high-impact operations.
- Confirmation token challenge for gated destructive actions.

## MCP tools

- Atomic tools:
  - `mail_accounts_list`
  - `mail_capabilities_get`
  - `mail_query`
  - `mail_get`
  - `mail_get_attachment`
  - `mail_mutate`
  - `mail_send`
  - `mail_encrypt`
  - `mail_decrypt`
  - `mail_send_encrypted`
  - `mail_get_decrypted`
  - `mail_sync`
  - `mail_policy_preview`
- Composite tools:
  - `mail_triage_batch`
  - `mail_reply_flow`

## Token efficiency rules

- Use compact fields (`lim`, `cursor`, `code`, `op_id`, `next`).
- Default `lim=25`, hard max `lim=100`.
- Keep responses concise unless `detail=true`.
- Keep attachment content metadata-first unless explicit retrieval is requested.
- Return machine-readable codes and deterministic shapes.

## Use with Agent Q

Agent-to-agent PRD handoff can use this skill as the **mail adapter** backend (SMTP send / IMAP fetch+decrypt). The **Agent Q transport client** orchestrates pull and push; batch PRD processing stays filesystem-only. See [_localsetup/docs/AGENTIC_AGENT_TO_AGENT_PROTOCOL.md](../../docs/AGENTIC_AGENT_TO_AGENT_PROTOCOL.md) and [_localsetup/docs/AGENTIC_AGENT_Q_BIDIRECTIONAL_BUILD_SPEC.md](../../docs/AGENTIC_AGENT_Q_BIDIRECTIONAL_BUILD_SPEC.md). Client CLI: `_localsetup/tools/agentq_transport_client/agentq_cli.py`. Post-ingest mail should move processed messages to `LocalsetupAgentQ/Processed` (or config override) so UNSEEN cannot replay without ledger.

## Security baseline

- Treat every external input as hostile.
- Enforce schema and bounds checks before execution.
- No shell interpolation of untrusted values.
- Enforce TLS or STARTTLS unless policy explicitly allows otherwise.
- Redact secrets and message payload data in logs.

## Documentation requirement

All user-facing documentation and guidance for this skill must be written in GitHub Flavored Markdown, render correctly in preview, and follow the humanization workflow in `localsetup-humanizer`.

