---
name: interview-framework
description: This skill should be used when running an interactive interview before a spec phase, gathering requirements through dialogue, asking the user clarifying questions before delegating to a subagent, or when any Ralph phase command (research, requirements, design, tasks) needs adaptive brainstorming dialogue. Covers the 3-phase algorithm (Understand, Propose Approaches, Confirm and Store).
version: 0.2.0
user-invocable: false
---

# Interview Framework

Adaptive brainstorming dialogue algorithm for all spec phases. Each phase command provides its own exploration territory (phase-specific areas to probe).

## Option Limit Rule

Each question must have 2-4 options (max 4). Keep the most relevant options, combine similar ones.

## Intent-Based Depth Scaling

Read `.progress.md` for intent classification. Scale dialogue depth accordingly:

| Intent | Questions |
|--------|-----------|
| TRIVIAL | 1-2 |
| REFACTOR | 3-5 |
| MID_SIZED | 3-7 |
| GREENFIELD | 5-10 |

## Completion Signal Detection

After each response, check for early completion signals: "done", "proceed", "skip", "enough", "that's all", "continue", "next".

If `askedCount >= minRequired` and signal detected, skip remaining questions and move to Propose Approaches.

## 3-Phase Overview

### Phase 1: UNDERSTAND (Adaptive Dialogue)

Read all available context (.progress.md, prior artifacts, goal text). Identify what is unknown vs already decided. Generate questions from context and exploration territory -- not from a fixed pool. Each question builds on prior answers. Never ask something .progress.md already answers.

See `references/algorithm.md` for full pseudocode.

### Phase 2: PROPOSE APPROACHES

Synthesize dialogue into 2-3 distinct approaches. Each includes: name, description, trade-offs. Lead with recommendation. Present via AskUserQuestion. Maximum 3 approaches (more causes decision fatigue). Trade-offs must be honest -- no straw-man alternatives.

See `references/algorithm.md` for full pseudocode.

### Phase 3: CONFIRM & STORE

Brief recap to user of key decisions and chosen approach. If user corrects something, update before storing. Store in .progress.md under Context Accumulator pattern.

See `references/algorithm.md` for full pseudocode.

## Adaptive Depth (Other Responses)

When user selects "Other": ask a context-specific follow-up (never generic "elaborate"). Reference what the user typed. Continue until clarity or 5 rounds. Do not increment askedCount for follow-ups.

See `references/examples.md` for example follow-up patterns.

## Context Accumulator Pattern

After each interview, update `.progress.md`: read existing content, append new section under "## Interview Responses" with descriptive keys reflecting what was discussed. Include the chosen approach.

See `references/examples.md` for storage format.

## References

- **`references/algorithm.md`** -- Full 3-phase pseudocode (UNDERSTAND, PROPOSE APPROACHES, CONFIRM & STORE)
- **`references/examples.md`** -- Example interview questions, "Other" response handling, context storage format
