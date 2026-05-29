---
name: localsetup-agentic-umbrella-queue
description: "Umbrella/queue: only when queue or PRD in scope; named workflows; impact summary + user confirmation before big/destructive runs. Use when editing .agent/queue/**, .agent/**, PRD.md, *.prd.md or when user invokes a named umbrella workflow."
metadata:
  version: "1.1"
---

# Umbrella and queue (scope-based)

This rule applies when **queue or PRD is in scope** (e.g. user is editing `.agent/queue/**` or references a named umbrella workflow) or when the user explicitly asks to run an umbrella/workflow by name.

## Named workflows

- Workflows have **distinct names**. Execute only on **clear user intent** (e.g. "Please execute the umbrella workflow X", "Run make-it-happen").
- Do not start an umbrella or queue run without the user having asked for it by name or by editing queue/PRD with clear intent.

## Guardrails

- **Impact summary + user confirmation:** Before running **big, complex, or destructive** workflows, present a short impact summary (what will change, what could be affected) and require explicit user confirmation. Do not proceed without user acknowledgment.
- **Scope:** This rule does not activate for routine edits outside `.agent/` or PRD; it activates when queue/PRD is in scope or when a named workflow is invoked.

## References

- [_localsetup/docs/WORKFLOW_REGISTRY.md](../../docs/WORKFLOW_REGISTRY.md)  - list of named workflows, when to use, impact review required.
- [_localsetup/docs/AGENTIC_UMBRELLA_WORKFLOWS.md](../../docs/AGENTIC_UMBRELLA_WORKFLOWS.md)  - umbrella definition, no mid-run stop, PHC gates, single final webhook.
- [_localsetup/docs/PRD_SCHEMA_EXTERNAL_AGENT_GUIDE.md](../../docs/PRD_SCHEMA_EXTERNAL_AGENT_GUIDE.md)  - spec format, external confirmation protocol.
