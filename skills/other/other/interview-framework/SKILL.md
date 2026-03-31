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

## Recommendation Format

Every question asked via `AskUserQuestion` in Phase 1 leads with the recommended option (except when options are symmetric, in which case `[Recommended]` may be omitted):

```yaml
AskUserQuestion:
  question: "[Context-aware question referencing prior answers]. [One sentence rationale for the recommendation.]"
  options:
    - "[Recommended] [Option text -- the AI's suggested answer]"
    - "[Alternative 1]"
    - "[Alternative 2 if needed]"
    - "Other"
```

Rules:
- `[Recommended]` is a label prefix on the first option only.
- The rationale sits in the question text, not the option label.
- Option count still 2-4 max (Option Limit Rule preserved).
- If there is no meaningful recommendation (truly symmetric choice), omit the `[Recommended]` label rather than placing it arbitrarily.

Example:

```yaml
AskUserQuestion:
  question: "Where should the spec live? You only have one specs directory configured, so the default is fine unless you want to reorganize."
  options:
    - "[Recommended] ./specs/ (default)"
    - "Let me configure a different path"
    - "Other"
```

## Codebase-First Exploration

Before asking any question, determine whether the answer is a **codebase fact** or a **user decision**:

- **Codebase fact**: something discoverable by reading code, config, or existing specs (e.g., which framework is used, whether an interface already exists, what a file currently does). Use the Explore agent to find it. Never ask the user.
- **User decision**: a preference, priority, trade-off, or constraint that only the user can answer (e.g., which approach to take, what the success criteria are, what's in scope). Ask via AskUserQuestion.

Only ask what you cannot discover yourself.

## Completion Signal Detection

After each response, check for early completion signals using token-based matching:

```text
completionSignals = ["done", "proceed", "skip", "enough", "that's all", "continue", "next"]

tokens = tokenize(userResponse.lower())  # split on whitespace/punctuation
for signal in completionSignals:
  if signal in tokens:  # exact token match, not substring
    -> SKIP remaining questions, move to PROPOSE APPROACHES
```

## 3-Phase Overview

### Phase 1: UNDERSTAND (Decision-Tree)

Read all available context (.progress.md, prior artifacts, goal text). Build a question tree from the exploration territory with dependency ordering. Traverse the tree: auto-resolve codebase facts via exploration, ask user only about decisions. Each question leads with `[Recommended]` answer. No fixed question caps. Exit when all nodes resolved or user signals completion.

See `references/algorithm.md` for full pseudocode.

### Phase 2: PROPOSE APPROACHES

Synthesize dialogue into 2-3 distinct approaches. Each includes: name, description, trade-offs. Lead with recommendation. Present via AskUserQuestion. Maximum 3 approaches (more causes decision fatigue). Trade-offs must be honest. No straw-man alternatives.

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

- **`references/algorithm.md`** -- Full 3-phase pseudocode (UNDERSTAND decision-tree, PROPOSE APPROACHES, CONFIRM & STORE)
- **`references/examples.md`** -- Example interview questions, "Other" response handling, context storage format
