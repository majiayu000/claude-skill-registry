---
name: agent-native
description: 'Operate explicit orchestrator, implementer, validator, and scribe roles through a caller-selected agent runtime. Triggers: "agent-native factory", "role-shaped agent panes", "persistent workers".'
practices: [team-topologies, design-by-contract]
hexagonal_role: supporting
consumes: [explicit-role-packets]
produces: [runtime-evidence, worker-handoff]
context_rel:
- kind: customer-of
  with: ntm
- kind: customer-of
  with: agent-mail
skill_api_version: 1
user-invocable: true
metadata:
  tier: meta
  dependencies: []
  capabilities: [role_dispatch, observe_workers, handoff]
  effects: [manage_runtime_sessions]
  canonical_status: canonical
  disposition: keep_optional_adapter
output_contract: runtime evidence for explicit packets
---

# Agent Native

Operate caller-selected agent sessions as explicit roles without turning the
runtime into AgentOps lifecycle authority.

## Roles

- **Orchestrator:** passes explicit packets and reports runtime facts.
- **Implementer:** may modify only its packet's declared subject.
- **Validator:** receives exact candidate content in a fresh, read-only context.
- **Scribe:** records runtime evidence without judging acceptance.

## Contract

1. Require an explicit packet, role, workspace, context identity, and evidence
   destination before starting a worker.
2. Prove runtime readiness and engagement from observable state; a successful
   prompt send is not proof of work.
3. Keep concurrent writers disjoint and isolated. Runtime coordination is not a
   claim, lease, queue, or completion state in AgentOps.
4. Record provider state, transcript references, artifacts, and terminal status.
5. Return runtime evidence to the caller. Do not convert provider retries,
   reconnects, idle states, or failures into Plan, Candidate, or verdict state.
6. A validator session may supply judgment to Validate, but only Validate writes
   `verdict.v2`.

NTM, native processes, Agent Mail, and Gas City are replaceable adapters. Use
them only when the caller selected that execution shape. A single local agent
pays no factory coordination cost.
