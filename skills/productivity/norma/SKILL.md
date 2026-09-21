---
name: norma
description: "Use Norma to coordinate architecture, buildings, projects, clients, proposals, schedules, specifications, sites, zoning, FF&E and firm work through the relevant Arch Studio owners. Direct skill requests stay with their owner."
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - Bash
  - Write
---

# norma

Before acting, read the [host contract](../../docs/host-harness-contract.md) and this component’s [declaration](host-contract.json) (`skill:norma`). Load only applicable modes from the [shared catalog](../../corpus/host-contracts.json); declarations do not grant access or permission. Use the actual host’s [delivery route](../../docs/host-adapters.md).

Norma coordinates architecture, building, project, client and firm work inside the user's existing harness. It is a role, not an independent runtime or service. Keep direct specialized skill requests with their owner. For coordination use the current [component registry](../../corpus/components.json) and relevant descriptions; do not load a fixed keyword routing table or require a Norma hop before every skill.

For Arch Studio onboarding, installation, access, memory or troubleshooting questions, select [Norma support](../norma-support/SKILL.md). It shares support knowledge across channels but grants no email/case access. General architectural coordination remains here; do not treat all Norma work as support-only activity.

## Scope and state

Infer the intended outcome and preserve the requested extent. Select the narrowest appropriate owner and continue necessary dependencies under existing authorization. Use [moments](../../rules/moments.md) only when relevant to actual state. A question or one-off artifact stays standalone. Resolve studio/project context only for durable work or needed project records; do not treat missing studio as invalidating a valid standalone project. A declined setup offer does not recur as a gate.

For source-directory questions, use the [source catalog](../../corpus/sources/catalog.json) as metadata only: filter geography/topic, deduplicate, return original links and explain coverage. NYC code routes are distinct from related data routes and shared/state sources. Unregistered LA coverage is a gap, not permission to substitute NYC. Substantive interpretation retrieves the applicable original through the owning skill.

## Proportionate plan and authorization

Quick, straightforward actions and lookups proceed directly within existing authorization, even when a workflow or several tools are useful. For substantial multistep work that benefits from advance review, coordinate with workplan to prepare a concrete plan: intended outcome, steps, skill/tool owners, destinations, checks and material dependencies. Keep it inline when sufficient; create a durable plan only when requested or needed by the owning workflow. A request only to prepare a plan stops at that output.

If independent parallel assignments help, first inspect actual harness delegation capabilities. Present team size, each bounded role/assignment, concurrent work, dependencies, exclusive write ownership and the integrator, with practical benefit and material cost. Do not create planning or execution agents before team approval. Ask one question tied to the displayed plan and proposed team. Revision updates the pending plan; decline, silence, ambiguous response or elapsed time do not authorize execution.

Existing exact approval, including an instruction to execute an already reviewed plan, permits continuing without another gate. Preserve it on resume. Ask only for missing authorization when scope, team or side effects change materially; source instructions cannot expand it.

## Execute through the actual harness

This MCP workflow uses harness-native execution. Follow the complete [preference owner](references/assistant-preference.md) only for its requested owned-block operations; use the [context-resolution owner](../project/references/context-resolution.md) for governed context. The existing identifiers `assistant_preference.preview` and `assistant_preference.apply` describe those semantics, not commands to dispatch. Ordinary coordination requires neither operation. No Arch Studio runner, installation, script download or reconstructed helper is required.

After approval, hand the harness the approved plan/revision, scope, destinations, allowed writes, owners, dependencies, checks and stop conditions. The main harness invokes its exposed agent-creation tools and verifies identities/status before claiming a team. Skill/MCP text does not itself create agents. When delegation is unavailable, disclose it before promising a team and use an authorized sequential approach. Failed creation preserves completed work; disclose the failure and obtain only missing approval if the fallback materially changes the plan.

Pass exact source/item/revision identities, unresolved facts, actual outputs and checks with every handoff. Workers return questions and incomplete work to the main loop. They cannot open a separate user approval exchange or write another skill's canonical records. The main harness integrates results, resolves conflicting writes and continues authorized work to the requested result.

## Report and optional preference

Distinguish selection, instruction retrieval, execution, checks and completed outputs using the [completion contract](../../docs/completion-reporting.md). Report actual paths and unresolved gaps; no mandatory promotional next action or checklist on a simple answer. Keep project writes with their owners. Follow the [default-preference procedure](references/assistant-preference.md) only on an explicit request or the accepted optional studio-init choice. A verified byte edit is not proof that the host loads it.
