---
name: loop
description: Use when beads have tight sequential dependencies or count is small (under 8), or when simplicity is preferred over parallelism. Simplest execution model — one bead at a time.
invocation: agent
---

# Loop

Sequential execution cycle that claims, implements, verifies, and completes beads one at a time in dependency order. Loop is the simplest execution model — use it when the dependency graph is mostly linear or when parallel execution adds unnecessary complexity.

## Invocation Contract

Inputs:
- Ready bead set with dependency states
- Verification commands per bead

Outputs:
- Ordered bead state transitions
- Completion report with final exit-criteria status

## Execution Cycle

### Pre-Loop Recovery

Before entering the main loop, run the Standard Recovery Procedure from `beads-schema` > Recovery Semantics:
1. Process crash markers from `<repo-root>/.arc/crashes/`.
2. Detect and reset stale `in_progress` beads (threshold: `ARC_STALE_THRESHOLD`, default 600s).
3. Report recovered beads. Skip silently if none.

See `beads-schema` for crash marker protocol, staleness configuration, and cleanup contract.

### Main Loop

Repeat until no work remains:

1. **Claim next unblocked bead** — Select the highest-priority bead whose dependencies are all in `closed` state. Transition it to `in_progress`.

2. **Implement the change** — Execute the work described in the bead's objective. Touch only the files listed in the bead's touch points. Follow TDD ordering when applicable: write or update tests first, then implement.

3. **Run verification** — Execute every verification command listed in the bead. All must pass. If any fail, diagnose and fix before proceeding.

4. **Mark complete** — Transition the bead to `closed`. Record verification output for traceability.

5. **Evaluate exit criteria** — After the last bead closes, run the plan-level exit criteria commands (from `plan-schema` Section 6). The loop is complete only when all exit criteria pass.

## Error Handling

- **Verification failure**: Diagnose the root cause. Fix the implementation and re-run verification. Do not skip failing checks. If the fix requires changes outside the bead's declared touch points, flag this as scope creep and note it in the bead record.

- **Blocked bead**: If a bead cannot proceed due to an unresolved dependency or external issue, transition it to `blocked` with a reason. Continue to the next unblocked bead if one exists. If all remaining beads are blocked, report the deadlock and stop.

- **Unexpected failure**: If a system-level failure occurs (build broken, environment issue), pause the loop and report. Do not attempt to continue past infrastructure failures.

## Progress Reporting

After each bead completes, report:
- Bead ID and objective (one line)
- Verification result (pass/fail)
- Remaining bead count and next bead ID

## When to Use Loop vs. Other Execution Modes

- **Loop** — Sequential, simple. Best when beads have tight dependencies or the total count is small (under 8).
- **Swarm** — Parallel workers without a lead agent. Best when many beads are independent.
- **Team** — Coordinated multi-agent with a lead. Best for large plans with mixed dependencies and shared-file conflicts.

## Related Skills

- `beads-schema` defines the bead structure consumed by loop.
- `plan-schema` defines the exit criteria that terminate the loop.
- `swarm` and `team` are alternative execution models.
