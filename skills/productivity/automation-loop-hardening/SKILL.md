---
name: automation-loop-hardening
description: |-
  Use when turning repeated manual operations into safer, observable, reusable automation loops.
  Triggers:
practices:
- pragmatic-programmer
skill_api_version: 1
user-invocable: false
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
hexagonal_role: supporting
metadata:
  tier: execution
  stability: experimental
  dependencies: []
output_contract: skills/automation-loop-hardening/skill.spec.json
---
# Automation Loop Hardening

Use this skill when a manual operation has repeated enough times that it may deserve automation, but the next step is not yet obvious. The goal is not to automate everything. The goal is to promote proven, repetitive work into the smallest safe loop with clear evidence, controls, and feedback.

## Operating Rule

Automation earns promotion by evidence:

1. The operation recurs with similar inputs, decisions, and outputs.
2. The manual version has visible cost, delay, error risk, or coordination load.
3. The operation can be made bounded, idempotent, observable, and reversible.
4. A human can understand the loop state without reading the implementation.

If those conditions are not met, return a "do not automate yet" verdict and specify what evidence would change the decision.

## Workflow

### 1. Capture the manual loop

Record the current operation as a concrete runbook:

- Trigger: what starts the operation.
- Inputs: files, services, tickets, commands, credentials, and human decisions.
- Steps: exact commands or UI actions, including checks between steps.
- Outputs: artifacts, state changes, notifications, and expected end state.
- Failure modes: partial writes, duplicate effects, stale data, rate limits, permission failures, and unclear ownership.
- Frequency: how often it repeats and how similar each run is.

Do not design automation from memory when a recent real run can be inspected. Prefer command history, logs, tickets, PRs, CI runs, and chat handoffs as evidence.

### 2. Pick the minimum durable shape

Choose the smallest promotion rung that removes real toil while keeping the loop inspectable:

| Rung | Use when | Required controls |
|---|---|---|
| Keep manual | The operation is rare, ambiguous, or high judgment | Checklist, owner, evidence to revisit |
| Runbook checklist | Steps repeat but decisions are still human | Preconditions, stop points, expected outputs |
| Script | Commands repeat and inputs are bounded | Dry run, idempotency, exit codes, structured logs |
| Scheduled job | Timing is predictable and failures can be retried | Locking, alerting, backoff, run history |
| Daemon or service | The loop reacts continuously to external state | State model, health checks, metrics, safe shutdown |

Avoid jumping straight to a daemon when a script plus scheduler provides the same value with less operational surface.

### 3. Define the safety envelope

Before implementation, specify:

- Preconditions that must pass before any mutation.
- A dry-run mode that shows intended effects without changing state.
- Idempotency strategy for duplicate runs, retries, and partial completion.
- Locking or concurrency behavior.
- Rollback or repair procedure for each mutable side effect.
- Secrets and permission boundaries.
- Rate limits, timeouts, and retry policy.
- Human approval gates for irreversible or high-impact changes.

Missing safety controls are a blocker for promotion, not an implementation detail to solve later.

### 4. Add observability

Every reusable loop must answer these questions from its own output or logs:

- What run happened, when, and with what inputs?
- What changed and what was intentionally skipped?
- What failed, where did it stop, and is it safe to retry?
- Who owns the loop and where should failures be reported?
- What metric or artifact proves the loop is still useful?

Prefer structured output for machines and a concise summary for humans. Store durable evidence where the surrounding project already stores run reports, CI artifacts, or operational notes.

### 5. Validate before relying on it

Validate the chosen loop at the lowest practical blast radius:

- Unit-test parsing and decision logic.
- Fixture-test representative inputs, empty inputs, duplicates, and malformed data.
- Run dry-run against a realistic target.
- Run one controlled live execution if mutation is required.
- Verify retry behavior and partial-failure recovery.
- Document the rollback command or manual repair path.

The validation result must state what was tested, what was not tested, and what remains manual.

## Output

Return a report matching `skills/automation-loop-hardening/skill.spec.json`:

- Verdict: keep manual, checklist, script, scheduled job, daemon, or do not automate yet.
- Evidence: the repeated operation and why it deserves that rung.
- Safety envelope: idempotency, rollback, locking, permissions, and approval gates.
- Observability plan: logs, metrics, artifacts, alerts, and owner.
- Implementation plan: the concrete files, commands, scheduler, or service boundaries.
- Validation result: commands run, evidence collected, and residual risk.
