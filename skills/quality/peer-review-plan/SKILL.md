---
name: peer-review-plan
description: "Run plan review using the codex CLI as an independent reviewer. Returns structured findings without applying fixes. Use when the user asks to \"peer review my plan\", \"get a second opinion on my plan\", \"codex review my plan\", or \"run codex on my plan\"."
---

# Peer Review Plan

AI-powered plan review via codex. Delegates to `/codex-exec` for an independent review of the implementation plan.

## Step 1: Identify the Plan

Determine the plan to review:

- If **plan text** was provided by the caller, use it
- If a **plan file path** was provided (e.g., `.turbo/prompts.md`), read the file
- If **neither** was provided, look for plan text in the current conversation context

## Step 2: Run `/codex-exec` Skill

Run the `/codex-exec` skill in read-only mode with the full plan text and these review instructions:

> Review the following implementation plan for issues that would cause an implementer to build the wrong thing or get stuck. For each issue found, state: (1) what the problem is, (2) where in the plan it occurs, (3) what impact it has on implementation, (4) a suggested fix, and (5) priority: P0 (fundamentally flawed), P1 (significant gap), P2 (moderate issue), or P3 (minor improvement). Ignore stylistic preferences and minor wording. If no issues are found, state that the plan looks sound.

## Step 3: Return Findings

Return the codex review output. The caller determines what to do with the findings.
