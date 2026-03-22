---
name: agentforge-channel-adapters
description: Work on AgentForge channel adapters across runtime and core, including Telegram, Discord, Slack, and WhatsApp.
version: 1.0.0
metadata:
  author: agentforge
---

# AgentForge Channel Adapters

Use this skill for channel integrations and adapter consistency.

## Focus areas

- runtime channel transport classes,
- core channel adapters and message normalization,
- CLI setup commands for channels,
- credentials and connection UX.

## Rules

- Preserve unified message semantics across channels.
- Prefer shared adapter logic over per-channel divergence.
- Keep streaming and progressive response behavior consistent where supported.
