---
name: escalation-governance
description: |

Triggers: governance, escalation, orchestration, model-selection, agents
  Guide to deciding whether to escalate from a lower model (haiku/sonnet) to
  a higher model (sonnet/opus).

  Triggers: model escalation, haiku to sonnet, sonnet to opus, reasoning depth,
  task complexity, model selection, capability trade-off

  Use when: evaluating whether to escalate models, facing genuine complexity
  requiring deeper reasoning, novel patterns with no existing solutions,
  high-stakes decisions requiring capability investment

  DO NOT use when: thrashing without investigation - investigate root cause first.
  DO NOT use when: time pressure alone - urgency doesn't change task complexity.
  DO NOT use when: "just to be safe" - assess actual complexity instead.

  NEVER escalate without investigation first. This is the Iron Law.
version: 1.0.0
category: agent-workflow
tags: [escalation, model-selection, governance, agents, orchestration]
dependencies: []
estimated_tokens: 800
---
## Table of Contents

- [Overview](#overview)
- [The Iron Law](#the-iron-law)
- [When to Escalate](#when-to-escalate)
- [When NOT to Escalate](#when-not-to-escalate)
- [Decision Framework](#decision-framework)
- [1. Have I understood the problem?](#1-have-i-understood-the-problem)
- [2. Have I investigated systematically?](#2-have-i-investigated-systematically)
- [3. Is escalation the right solution?](#3-is-escalation-the-right-solution)
- [4. Can I justify the trade-off?](#4-can-i-justify-the-trade-off)
- [Escalation Protocol](#escalation-protocol)
- [Common Rationalizations](#common-rationalizations)
- [Agent Schema](#agent-schema)
- [Orchestrator Authority](#orchestrator-authority)
- [Red Flags - STOP and Investigate](#red-flags-stop-and-investigate)
- [Integration with Agent Workflow](#integration-with-agent-workflow)
- [Quick Reference](#quick-reference)


# Escalation Governance

## Overview

Model escalation (haiku→sonnet→opus) trades speed/cost for reasoning capability. This trade-off must be justified.

**Core principle:** Escalation is for tasks that genuinely require deeper reasoning, not for "maybe a smarter model will figure it out."

## The Iron Law

```
NO ESCALATION WITHOUT INVESTIGATION FIRST
```
**Verification:** Run the command with `--help` flag to verify availability.

Escalation is never a shortcut. If you haven't understood why the current model is insufficient, escalation is premature.

## When to Escalate

**Legitimate escalation triggers:**

| Trigger | Description | Example |
|---------|-------------|---------|
| Genuine complexity | Task inherently requires nuanced judgment | Security policy trade-offs |
| Reasoning depth | Multiple inference steps with uncertainty | Architecture decisions |
| Novel patterns | No existing patterns apply | First-of-kind implementation |
| High stakes | Error cost justifies capability investment | Production deployment |
| Ambiguity resolution | Multiple valid interpretations need weighing | Spec clarification |

## When NOT to Escalate

**Illegitimate escalation triggers:**

| Anti-Pattern | Why It's Wrong | What to Do Instead |
|--------------|----------------|---------------------|
| "Maybe smarter model will figure it out" | This is thrashing | Investigate root cause |
| Multiple failed attempts | Suggests wrong approach, not insufficient capability | Question your assumptions |
| Time pressure | Urgency doesn't change task complexity | Systematic investigation is faster |
| Uncertainty without investigation | You haven't tried to understand yet | Gather evidence first |
| "Just to be safe" | False safety - wastes resources | Assess actual complexity |

## Decision Framework

Before escalating, answer these questions:

### 1. Have I understood the problem?

- [ ] Can I articulate why the current model is insufficient?
- [ ] Have I identified what specific reasoning capability is missing?
- [ ] Is this a capability gap or a knowledge gap?

**If knowledge gap:** Gather more information, don't escalate.

### 2. Have I investigated systematically?

- [ ] Did I read error messages/outputs carefully?
- [ ] Did I check for similar solved problems?
- [ ] Did I form and test a hypothesis?

**If not investigated:** Complete investigation first.

### 3. Is escalation the right solution?

- [ ] Would a different approach work at current model level?
- [ ] Is the task inherently complex, or am I making it complex?
- [ ] Would breaking the task into smaller pieces help?

**If decomposable:** Break down, don't escalate.

### 4. Can I justify the trade-off?

- [ ] What's the cost (latency, tokens, money) of escalation?
- [ ] What's the benefit (accuracy, safety, completeness)?
- [ ] Is the benefit proportional to the cost?

**If not proportional:** Don't escalate.

## Escalation Protocol

When escalation IS justified:

1. **Document the reason** - State why current model is insufficient
2. **Specify the scope** - What specific subtask needs higher capability?
3. **Define success** - How will you know the escalated task succeeded?
4. **Return promptly** - Drop back to efficient model after reasoning task

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "This is complex" | Complex for whom? Have you tried? |
| "Better safe than sorry" | Safety theater wastes resources |
| "I tried and failed" | How many times? Did you investigate why? |
| "The user expects quality" | Quality comes from process, not model size |
| "Just this once" | Exceptions become habits |
| "Time is money" | Systematic approach is faster than thrashing |

## Agent Schema

Agents can declare escalation hints in frontmatter:

```yaml
model: haiku
escalation:
  to: sonnet                 # Suggested escalation target
  hints:                     # Advisory triggers (orchestrator may override)
    - security_sensitive     # Touches auth, secrets, permissions
    - ambiguous_input        # Multiple valid interpretations
    - novel_pattern          # No existing patterns apply
    - high_stakes            # Error would be costly
```
**Verification:** Run the command with `--help` flag to verify availability.

**Key points:**
- Hints are advisory, not mandatory
- Orchestrator has final authority
- Orchestrator can escalate without hints (broader context)
- Orchestrator can ignore hints (task is actually simple)

## Orchestrator Authority

The orchestrator (typically Opus) makes final escalation decisions:

**Can follow hints:** When hint matches observed conditions
**Can override to escalate:** When context demands it (even without hints)
**Can override to stay:** When task is simpler than hints suggest
**Can escalate beyond hint:** Go to opus even if hint says sonnet

The orchestrator's judgment, informed by conversation context, supersedes static hints.

## Red Flags - STOP and Investigate

If you catch yourself thinking:
- "Let me try with a better model"
- "This should be simple but isn't working"
- "I've tried everything" (but haven't investigated why)
- "The smarter model will know what to do"
- "I don't understand why this isn't working"

**ALL of these mean: STOP. Investigate first.**

## Integration with Agent Workflow

```
**Verification:** Run the command with `--help` flag to verify availability.
Agent starts task at assigned model
├── Task succeeds → Complete
└── Task struggles →
    ├── Investigate systematically
    │   ├── Root cause found → Fix at current model
    │   └── Genuine capability gap → Escalate with justification
    └── Don't investigate → WRONG PATH
        └── "Maybe escalate?" → NO. Investigate first.
```
**Verification:** Run the command with `--help` flag to verify availability.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Task inherently requires nuanced reasoning | Escalate |
| Agent uncertain but hasn't investigated | Investigate first |
| Multiple attempts failed | Question approach, not model |
| Security/high-stakes decision | Escalate |
| "Maybe smarter model knows" | Never escalate on this basis |
| Hint fires, task is actually simple | Override, stay at current model |
| No hint fires, task is actually complex | Override, escalate |

## Model Capability Notes

**MCP Tool Search (Claude Code 2.1.7+)**: Haiku models do not support MCP tool search. If a workflow uses many MCP tools (descriptions exceeding 10% of context), those tools load upfront on haiku instead of being deferred. This can consume significant context. Consider escalating to sonnet for MCP-heavy workflows or ensure haiku agents use only native tools (Read, Write, Bash, etc.).

## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
