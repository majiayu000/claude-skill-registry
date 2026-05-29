---
name: consult-claude
description: "Consult Claude Code for second opinions, brainstorming, or difficult debugging from Codex. Use when the user asks to \"consult claude\", \"ask claude\", \"get claude's opinion\", \"brainstorm with claude\", or \"discuss with claude\"."
---

# Consult Claude

Use Claude Code as an external collaborator from Codex. Unlike `$peer-review`, this skill is conversational and exploratory.

## Step 1: Define the Question

State:

- What problem needs input
- What has already been tried
- What files, commands, plans, or error messages matter
- What kind of answer is useful: hypotheses, tradeoffs, concrete fix, or review

## Step 2: Run `$claude-print` Skill

Run the `$claude-print` skill with the assembled question. Default to read-only permissions.

For follow-up questions, include Claude's previous answer and the new evidence gathered since then.

## Step 3: Synthesize

Summarize the useful parts of Claude's response. Cross-reference suggestions with the repository before acting.

Then update or check the active plan and proceed to any remaining task.

## Rules

- Claude's answer is advisory.
- Do not apply a suggestion until it has been checked against the actual codebase.
- Keep each Claude turn focused on one question.
