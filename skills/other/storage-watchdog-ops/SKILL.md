---
name: storage-watchdog-ops
description: "Operate the ACFS storage watchdog: inspect disk pressure, read logs, verify Rust target cleanup, and escalate safely."
---

# storage-watchdog-ops (Codex)

This is the Codex-runtime entry point for the **storage-watchdog-ops** skill. The full runbook — what the daemon actually does, the status/interpret/remediate/escalate procedure, the decision log semantics, and the related ops surfaces — lives in the sibling base skill:

- **Canonical skill:** [`../../skills/storage-watchdog-ops/SKILL.md`](../../skills/storage-watchdog-ops/SKILL.md)

Read that file first. Then follow the Codex Execution Profile in [`prompt.md`](./prompt.md) for the runtime-specific tool mapping and guardrails.
