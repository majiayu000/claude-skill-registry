---
name: multi-agent-orchestration
description: Design and operate bounded multi-agent workflows with task decomposition, dependency graphs, ownership, handoff contracts, shared-state controls, approvals, recovery, and synthesis. Use when a task contains genuinely independent workstreams, specialized roles, parallel research or implementation, reviewer-worker loops, or coordination problems that one agent should not execute sequentially.
---

# Multi-Agent Orchestration

Use multiple agents only when specialization or safe parallelism outweighs coordination cost.

## Use when

- Split a large objective into independent, verifiable workstreams.
- Coordinate specialists that need distinct tools, permissions, or context.
- Run worker-reviewer, planner-executor, map-reduce, or bounded debate patterns.
- Diagnose duplicate work, conflicting edits, weak handoffs, or stalled dependencies.

Do not delegate a tightly coupled, small, or inherently sequential task merely to increase agent count.

## Inputs

Collect the objective, completion criteria, task graph, available agents and tools, concurrency limits, shared files or systems, authority boundaries, deadlines, budget, and final decision owner. State assumptions and unresolved dependencies.

## Output contract

Produce:

1. A decomposition rationale and explicit non-goals.
2. A directed acyclic task graph with owner, dependencies, inputs, output contract, write scope, and verification for every task.
3. A handoff protocol and shared-state policy.
4. Approval points, timeout and retry limits, escalation routes, and stop conditions.
5. A synthesis plan that resolves disagreements and verifies the integrated result.
6. A completion report with evidence, remaining uncertainty, and unused or failed branches.

## Workflow

1. Define one measurable objective and the authority boundary before assigning work.
2. Decompose by separable outputs, not vague roles. Keep shared mutable state to a minimum and retain tightly coupled steps under one owner.
3. Draw dependencies and identify the critical path. Parallelize only tasks with independent inputs and non-overlapping side effects. Read [orchestration-patterns.md](references/orchestration-patterns.md) when choosing a topology.
4. Assign one accountable owner per task. Specify inputs, deliverable format, write scope, validation, deadline or timeout, and what warrants escalation.
5. Give each agent the minimum context and permissions needed. Include source artifacts, not hidden conclusions, when independent judgment matters.
6. Require structured handoffs: status, result, evidence, changed state, assumptions, risks, and next dependency. Acknowledge receipt before downstream mutation.
7. Monitor dependency state and useful progress. Bound retries and debates; do not recursively delegate without a clear capacity and ownership model.
8. Synthesize centrally or through a named integrator. Resolve conflicting claims from primary evidence, run integration checks, and confirm the original completion criteria.
9. Close or cancel unused work, record unresolved risks, and return control to the final decision owner.

Use `python3 scripts/validate_plan.py plan.json --strict` before execution. The command structurally checks dependencies, cycles, ownership, approval references, and numeric execution bounds. Strict mode also fails on warnings, including exact parallel write conflicts, missing timeout/retry bounds, and incomplete retry contracts. It validates declarations only; it cannot verify runtime isolation, authorization, approval authenticity, or actual task behavior.

## Safety and permissions

- Delegation never expands authority. Do not let a child agent perform an action the requester did not authorize.
- Reserve external messages, purchases, deployments, destructive actions, credential access, and production changes for explicit approval points.
- Isolate credentials and sensitive context by role; do not broadcast secrets through shared state or handoffs.
- Use single-writer ownership, branches, transactions, or locks for mutable resources.
- Preserve user-owned changes and make cancellation recoverable.

## Verification

- Validate the plan is acyclic and every dependency and approval reference resolves. Tag consequential work with `consequential`, `deploy`, or `external-mutation` and require its task-local `approval_ref` to name an approval point for that task.
- Confirm concurrently runnable tasks do not write the same file, record, branch, or environment.
- Check every handoff against its output contract before unblocking dependents.
- Re-run end-to-end tests or evidence checks after synthesis; individual task success is insufficient.
- Confirm the final report accounts for all tasks as completed, failed, canceled, or superseded.

## Failure handling

- If an agent stalls, inspect its last evidence, retry once only when the failure is transient, then reassign or collapse the task.
- If agents disagree, ask each for source-backed claims and let the named integrator adjudicate; do not average incompatible answers.
- If shared state conflicts, pause writers, preserve both versions, and reconcile through the single owner.
- If a dependency fails, block or redesign downstream work instead of silently fabricating its input.
- If coordination overhead exceeds remaining work, stop delegation and complete the critical path under one owner.

## Example

For “prepare and implement a cross-platform authentication change,” keep architecture and integration under one owner, delegate independent threat modeling and test-fixture design, assign non-overlapping implementation files only after the interface is frozen, require each handoff to include changed paths and test evidence, gate production configuration behind approval, and have the integrator run the complete suite and reconcile security findings before declaring completion.
