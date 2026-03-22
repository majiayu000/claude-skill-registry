---
name: spec
version: 1.2.0
description: >-
  Collaborative spec workflow between two agents. Use when the user says
  "spec", "design with", "collaborative spec", "spec with codex",
  "spec with claude", or any variation of "let's design X with Y".
  This is a structured multi-phase protocol — do NOT shortcut it.
argument-hint: "<description of what to design> [with <partner>]"
metadata:
  short-description: Multi-agent collaborative spec workflow
  compatibility: claude-code, codex-cli
---

# /spec — Collaborative Specification Workflow

This skill defines a structured two-agent specification flow.

Use canonical phases in order:
`Research -> Discuss -> Draft -> Review -> Present -> Execute`

Detailed step-by-step protocol lives in `references/spec-workflow.md`.
This file is the concise operational entrypoint.

## Parse Input

From the user prompt, extract:
- **topic**: short kebab-case spec name (e.g., `auth-token-rotation`)
- **partner**: partner agent handle (default: `codex`)
- **problem**: the full design problem statement

If topic/problem are unclear, ask for clarification.

## Pre-flight

1. Verify AMQ is available: `which amq`
2. Verify co-op is initialized (`.amqrc`), otherwise run: `amq coop init`
3. Use thread name: `spec/<topic>`

## First Action: Send problem to partner IMMEDIATELY

**CRITICAL: Do this FIRST, before ANY research, exploration, or code reading.**
The entire point of the spec workflow is parallel research. Every second you
spend researching before sending is a second your partner sits idle.

```bash
amq send --to <partner> --kind question \
  --labels workflow:spec,phase:request \
  --thread spec/<topic> --subject "Spec: <topic>" --body "<problem>"
```

Send the user's problem description verbatim. Do NOT include your own analysis.
Do NOT pre-research "to give better context". Send it NOW, then research.

## Label Convention (MANDATORY)

Use existing AMQ kinds plus labels to express spec workflow semantics:

| Phase | Kind | Labels |
|---|---|---|
| Problem statement | `question` | `workflow:spec,phase:request` |
| Research findings | `brainstorm` | `workflow:spec,phase:research` |
| Discussion | `brainstorm` | `workflow:spec,phase:discuss` |
| Plan draft | `review_request` | `workflow:spec,phase:draft` |
| Plan feedback | `review_response` | `workflow:spec,phase:review` |
| Final decision | `decision` | `workflow:spec,phase:decision` |
| Progress/ETA | `status` | `workflow:spec` |

## Quick Command Skeleton

```bash
# Initiate spec with problem statement
amq send --to <partner> --kind question \
  --labels workflow:spec,phase:request \
  --thread spec/<topic> --subject "Spec: <topic>" --body "<problem>"

# Submit independent research
amq send --to <partner> --kind brainstorm \
  --labels workflow:spec,phase:research \
  --thread spec/<topic> --subject "Research: <topic>" --body "<findings>"

# Discuss and align
amq send --to <partner> --kind brainstorm \
  --labels workflow:spec,phase:discuss \
  --thread spec/<topic> --subject "Discussion: <topic>" --body "<analysis>"

# Draft plan
amq send --to <partner> --kind review_request \
  --labels workflow:spec,phase:draft \
  --thread spec/<topic> --subject "Plan: <topic>" --body "<plan>"

# Review plan
amq send --to <partner> --kind review_response \
  --labels workflow:spec,phase:review \
  --thread spec/<topic> --subject "Review: <topic>" --body "<feedback>"

# Optional final decision message
amq send --to <partner> --kind decision \
  --labels workflow:spec,phase:decision \
  --thread spec/<topic> --subject "Final: <topic>" --body "<final plan>"
```

## When You RECEIVE a Spec Message

If you receive a message labeled `workflow:spec`, your action depends on the phase:

| Label | Your action |
|---|---|
| `phase:request` | Read the problem statement, do your **own independent research first**, then submit findings as `brainstorm` + `phase:research` |
| `phase:research` | Read thread, start discussion as `brainstorm` + `phase:discuss` |
| `phase:discuss` | Reply with your analysis, continue discussion until aligned |
| `phase:draft` | **REVIEW the plan and send feedback** as `review_response` + `phase:review`. Do NOT implement. |
| `phase:review` | Revise plan if needed, or confirm alignment |
| `phase:decision` | **STOP. Do NOT implement.** Only the user can authorize implementation. Wait for the initiator to confirm user approval. |

**The partner agent NEVER implements.** Only the initiator presents the plan
to the user. Implementation starts only after the initiator explicitly tells
you the user approved and assigns you work.

## Non-Negotiable Rules

- **NEVER** research before sending the problem to your partner. Send FIRST, research SECOND.
- **NEVER** skip phases or collapse directly to a finished spec.
- **NEVER** read partner research before submitting your own research.
- **NEVER** enter plan mode during research if it blocks tool usage.
- **NEVER** implement when you receive a plan. Review it and send feedback — that's your job.
- **NEVER** implement before the user approves the final plan in chat. Only the initiator talks to the user.
- **ALWAYS** use `--thread spec/<topic>` for spec workflow messages.
- **ALWAYS** use the label convention table above.
- **ALWAYS** present the final plan to the user and wait for explicit approval.

## Reference

For full protocol details, templates, and phase gates, see:
- [references/spec-workflow.md](references/spec-workflow.md)
