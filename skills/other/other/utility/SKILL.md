---
name: utility
description: >-
  Utility-guided action selection for agent orchestration.
  Scores candidate actions by balancing gain, step cost,
  uncertainty, and redundancy.
  Use when deciding whether to take another action, launch
  another agent, or stop.
  Do not use for simple single-step operations.
version: 1.7.1
alwaysApply: false
category: infrastructure
tags:
- orchestration
- cost-control
- decision-making
- agent-dispatch
dependencies: []
provides:
  infrastructure:
  - utility-scoring
  - action-selection
  - termination-control
  patterns:
  - gain-estimation
  - cost-computation
  - redundancy-detection
usage_patterns:
- agent-dispatch-gating
- tool-call-decisions
- continuation-decisions
- model-tier-selection
complexity: intermediate
model_hint: standard
estimated_tokens: 600
progressive_loading: true
modules:
- modules/state-builder.md
- modules/gain.md
- modules/step-cost.md
- modules/uncertainty.md
- modules/redundancy.md
- modules/action-selector.md
- modules/integration.md
---
# Utility Skill

## Overview

A decision framework for agent orchestration based on Liu et al.,
"Utility-Guided Agent Orchestration for Efficient LLM Tool Use"
(arXiv:2603.19896).
Each candidate action is scored by subtracting weighted costs from
expected gain, producing a single utility value that guides action
selection.
The framework prevents over-calling tools and premature stopping by
making both errors costly.
Utility range is [-2.3, 1.0].

## When To Use

- Deciding whether to dispatch another agent or tool call
- Gating expensive tool calls (search, code execution, delegation)
- Selecting the right model tier for a sub-task
- Continuation decisions after receiving partial results
- Verification gating before writing or committing output

## When NOT to Use

- Single-step operations with one obvious action
- Trivial tasks where cost of scoring exceeds benefit
- Already-committed actions that cannot be undone

## Action Space

`A = {respond, retrieve, tool_call, verify, delegate, stop}`

| Action | Description |
|-----------|------------------------------------------------------|
| respond | Emit a final answer from current context |
| retrieve | Fetch additional information (search, read, lookup) |
| tool_call | Execute a tool (code runner, API, file write) |
| verify | Check a prior result for correctness or completeness |
| delegate | Spawn a sub-agent or hand off to a specialist |
| stop | Terminate the loop and return current state |

## Utility Function

```
U(a | s_t) = Gain(a | s_t)
           - λ₁ · StepCost(a | s_t)
           - λ₂ · Uncertainty(a | s_t)
           - λ₃ · Redundancy(a | s_t)
```

| Parameter | Default | Rationale |
|-----------|---------|---------------------------------------------------|
| λ₁ | 1.0 | Cost baseline; all other weights relative to this |
| λ₂ | 0.5 | Weak empirical correlation with outcome (r=0.0131) |
| λ₃ | 0.8 | Redundancy pruning yields ~10% token savings |

Utility range: **[-2.3, 1.0]**.
Positive values indicate the action is worth taking.
Values below the floor (-0.5 default) indicate the action should
be skipped.

## Termination Conditions

Stop the loop when **any** of the following is true:

- (a) Selected action is `stop`
- (b) Step budget exhausted (default: 10 steps)
- (c) All non-`stop` actions score below the floor (default: -0.5)

**High-gain override:** If `Gain >= 0.7` for any action, condition
(c) may be overridden.
Document the override and the gain value in your reasoning trace.

## Quick Start

Minimal 4-step advisory pattern:

1. **Construct state** -- gather task context per
   `modules/state-builder.md`
2. **Score candidates** -- evaluate each action in `A` per
   `modules/action-selector.md`
3. **Prefer highest utility** -- select the action with the
   maximum `U(a | s_t)`, subject to termination conditions
4. **Log score and decision** -- record the winning action,
   its utility value, and step count before executing

## Detailed Resources

- **State Builder**: `modules/state-builder.md` -- how to
  populate `s_t` from task context
- **Gain**: `modules/gain.md` -- estimating expected information
  or progress gain
- **Step Cost**: `modules/step-cost.md` -- token, latency, and
  monetary cost tables
- **Uncertainty**: `modules/uncertainty.md` -- confidence
  estimation and calibration
- **Redundancy**: `modules/redundancy.md` -- detecting duplicate
  or low-delta actions
- **Action Selector**: `modules/action-selector.md` -- scoring
  loop and tie-breaking rules
- **Integration**: `modules/integration.md` -- wiring utility
  scoring into existing orchestration loops

## Exit Criteria

- [ ] State constructed with task goal and prior steps
- [ ] All six actions scored before selecting one
- [ ] Termination condition checked after each step
- [ ] Score and decision logged for each step taken
- [ ] High-gain overrides documented with gain value
