---
name: peer-review-spec
description: "Run spec review using the codex CLI as an independent reviewer. Returns structured findings without applying fixes. Use when the user asks to \"peer review my spec\", \"get a second opinion on my spec\", \"codex review my spec\", or \"run codex on my spec\"."
---

# Peer Review Spec

AI-powered spec review via codex. Delegates to `/codex-exec` for an independent review of the specification document.

## Step 1: Identify the Spec

Determine the spec to review:

- If **spec text** was provided by the caller, use it
- If a **spec file path** was provided, read the file
- If **neither** was provided, check for a spec at `.turbo/spec.md`, or look in the current conversation context

## Step 2: Run `/codex-exec` Skill

Run the `/codex-exec` skill in read-only mode with the full spec text and these review instructions:

> Review the following specification document for issues that would cause problems during implementation planning. For each issue found, state: (1) what the problem is, (2) where in the spec it occurs, (3) what impact it has on planning or implementation, (4) a suggested fix, and (5) priority: P0 (fundamentally flawed), P1 (significant gap), P2 (moderate issue), or P3 (minor improvement). Ignore stylistic preferences and minor wording. If no issues are found, state that the spec looks sound.

## Step 3: Return Findings

Return the codex review output. The caller determines what to do with the findings.
