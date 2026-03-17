---
name: my-skill
description: >
  What this skill does and when to use it. Claude uses this to decide
  when to load the skill automatically.
# disable-model-invocation: true   # uncomment to make this /slash-command only
# user-invocable: false            # uncomment to hide from / menu (background knowledge only)
# allowed-tools: Read, Grep, Glob  # uncomment to restrict tool access
# context: fork                    # uncomment to run in an isolated subagent
# agent: Explore                   # subagent type (when context: fork)
argument-hint: <file|folder>...     # shown during autocomplete; update to match your skill
---

> Key philosophy or concern for this skill (optional).

**Stop after each stage and have changes reviewed with the user.**

## Stage 0 — Understand (agent proposes, developer confirms)

- Read the input and summarize what you understand
- Confirm intent with the developer before proceeding

## Stage 1 — [Action] (agent leads)

- Step-by-step instructions for this stage
- Use questions to guide analysis: "Is X correct?", "Does Y serve the goal?"

## Stage 2 — [Action] (agent leads)

- ...

## Stage N — Tidy up

- Final cleanup pass
- Update glossary if applicable
