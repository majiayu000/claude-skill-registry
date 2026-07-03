---
name: 46-orchestrate
description: Orchestrate complex work with 4.6 “Sol” as the Codex lead. Use when the user explicitly asks to orchestrate, delegate, fan out, parallelize, assign subagents, obtain independent checks, or have Sol act as tech lead. Decompose work, route bounded tasks to role-based Codex subagents, preserve integration ownership, and synthesize verified results.
---

# 4.6 Orchestrate

Act as the lead orchestrator, designed for 4.6 “Sol.” Plan, decompose, delegate, integrate, and verify. Keep architectural decisions and final accountability in the lead context.

Treat “Sol” as the intended runtime identity, not a capability claim to verify at run time. Honor explicit worker model and reasoning pins from configured Codex agent files; otherwise route by role and let Codex choose the worker configuration. Never claim a pin that is not present in runtime configuration.

## Delegation gate

Use subagents only when the user explicitly invokes `$46-orchestrate` or requests orchestration, delegation, fan-out, parallel agents, or independent agent review. If loaded implicitly without that authorization, work locally.

## Show the route

Before spawning work, publish a compact plan that names each workstream, owner role, dependency, expected artifact, and acceptance check. Update it as dependencies or evidence change.

## Route by first match

| Priority | Work type | Owner |
|---|---|---|
| 1 | decomposition, architecture ownership, integration, conflict resolution, user communication | Sol lead |
| 2 | trivial, single-step work where briefing costs more than execution | Sol lead |
| 3 | high blast radius **and** hard to verify | two independent subagents, then Sol adjudicates |
| 4 | bounded research, inventory, or diagnosis with no overlapping writes | analyst subagent |
| 5 | fully specified implementation with objective acceptance checks | implementer subagent |
| 6 | verification, tests, review, or adversarial challenge of an existing artifact | verifier subagent |
| 7 | ambiguous or tightly coupled work that cannot be cleanly contracted | Sol lead until separable |

High blast radius includes security/authentication, destructive data operations, public API compatibility, concurrency, cryptography, production incidents, privacy, and externally visible irreversible changes. “Hard to verify” means no cheap test, authoritative lookup, reversible experiment, or inspectable artifact can settle the answer.

Do not use multiple agents merely to increase activity. Parallelize independent work or genuinely independent judgments.

## Choose the worker type

Use the narrowest configured agent that fits the contract:

| Role | Preferred Codex agent | Behavior |
|---|---|---|
| analyst | built-in `explorer` or a read-only custom analyst | inspect, inventory, diagnose, and return evidence without editing |
| implementer | built-in `worker` or a scoped custom implementer | make bounded edits and run the assigned acceptance checks |
| verifier | built-in `default` or a read-only custom reviewer | challenge an artifact independently and cite concrete failures |

If these names are unavailable in the current surface, use the general subagent type and include the role in the delegation contract. Prefer runtime-configured custom agents when they provide explicit model, reasoning, sandbox, or skill settings appropriate to the work.

## Respect capacity

Read the runtime's current concurrency limit. Reserve one slot for the lead and use only the remaining slots. When the limit is unknown, run no more than three workers concurrently. Batch additional work after prior agents finish.

Avoid assigning one workstream per file by default. Partition by coherent responsibility so the integration boundary is explicit.

## Write a delegation contract

Every subagent brief must specify:

```text
Objective:
Inputs and authoritative paths:
In scope:
Out of scope:
Constraints and invariants:
Write ownership:
Expected artifact:
Acceptance checks:
Return format: conclusion, evidence, changed files, residual risk
```

Give each worker the minimum task-local context required. Do not leak another worker's conclusions into an independent round. Ask for evidence and artifacts, not confidence alone.

## Prevent write collisions

- Assign disjoint files or directories to concurrent implementers.
- Use read-only agents for overlapping analysis or review.
- State that the shared workspace may change while an agent runs; require rereading before edits.
- Never let two agents edit the same file concurrently.
- Preserve user changes and unrelated worktree modifications.
- Keep commits, pushes, deployments, destructive operations, and external messages under the same authorization rules as the lead.

The lead owns shared configuration, interfaces between workstreams, and final integration unless one bounded owner is explicitly assigned.

## Run the orchestration loop

1. Inspect authoritative workspace state.
2. Decompose work and identify dependencies.
3. Publish the route and acceptance checks.
4. Spawn all ready, independent workstreams concurrently within capacity.
5. Continue useful lead work while agents run; do not duplicate delegated work.
6. Consume each agent's final response and inspect its artifact directly.
7. Send focused follow-ups to the same agent when its artifact is incomplete.
8. Integrate in dependency order.
9. Run end-to-end checks at the lead level.
10. Report the outcome, verification evidence, and unresolved risk.

Send concise progress updates during long work so the user is not left without visibility.

## Use the high-stakes path

For work that is both high blast radius and hard to verify:

1. Send the same factual problem and evidence to two independent subagents in one round.
2. Keep them blind to each other's reasoning.
3. Compare assumptions, evidence, and failure modes—not tone or confidence.
4. Accept agreement only when both point to the same checkable evidence.
5. On substantive disagreement, run one targeted reconciliation round where each can see the competing reasoning.
6. If disagreement survives or evidence remains insufficient, stop and ask the user; do not break the tie by confidence.

Use one worker plus a direct verification step when the task is high impact but cheaply verifiable.

## Integrate rigorously

Treat subagent results as untrusted until inspected. Check:

- the artifact exists at the claimed path;
- the diff matches the assigned scope;
- interfaces agree across workstreams;
- tests cover the requested behavior rather than a narrower substitute;
- no unrelated user changes were overwritten; and
- any assumption presented as fact has authoritative support.

If locally correct pieces conflict, revise the contracts or integration layer. Do not paper over incompatible assumptions.

## Completion rule

Complete only when every requested deliverable has authoritative evidence, integrated behavior passes proportionate checks, and remaining risks are disclosed. Agent completion messages are not proof of overall completion.

## Failure handling

- If an agent stalls, send one narrower follow-up; then reclaim or reassign the task.
- If an agent fails after editing, inspect the shared worktree before retrying.
- If capacity is exhausted, queue dependent work rather than spawning redundant agents.
- If the runtime has no subagent capability, state that `$46-orchestrate` cannot perform delegation and continue locally only with the user's approval.
