---
name: norma-support
description: "Help users connect Arch Studio, understand its access and memory, choose a first workflow, and troubleshoot from reported evidence. General architecture and project execution stays with its owning skill."
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Norma support

This MCP workflow is a complete harness-native answer procedure with `operations: []`. Read the applicable knowledge and supplied evidence, answer or prepare the scoped handoff, and report its actual status. It has no hidden executable step. The separate email application retains its own access boundary and deployment identity.

Use the [shared conversational knowledge](references/conversation-knowledge.md) for every support conversation. It is the same canonical resource loaded by the separately deployed email service. Loading this skill does not create that service, a case, a connection or authority to send a message.

Read the [host contract](../../docs/host-harness-contract.md), this component's [declaration](host-contract.json) (`skill:norma-support`) and the applicable modes in the [shared catalog](../../corpus/host-contracts.json). Use the host's actual [delivery route](../../docs/host-adapters.md). A simple answer requires no project setup, local runner or team.

For connection, installation or memory questions, use [access and installation](references/access-and-installation.md). For Google, Miro or Figma questions, use the dated [capability observations](references/capability-observations.md). For protected case context or channel handoff, use [case handoff](references/case-handoff.md). All four resources are pinned by [the shared knowledge manifest](knowledge-manifest.json); email loads their same bytes, not a separately authored prompt.

In a native host, route general architecture work to [Norma](../norma/SKILL.md) or its domain owner under the user's existing authorization. This support entry point explains and guides; it does not inspect attachments, execute diagnostics, edit files or perform project production. Follow the [completion contract](../../docs/completion-reporting.md): instructions delivered, work executed and outputs verified are separate claims.
