---
name: peer-review
description: "Run an independent peer review via codex. Use when the user asks to \"peer review\", \"peer review my code\", \"peer review my plan\", \"peer review my spec\", \"peer review my prompt plan\", \"get a second opinion\", or \"independent review\"."
---

# Peer Review

Independent peer review via codex. Runs `/codex-exec` in read-only mode with a caller-provided review prompt.

## Step 1: Identify the Review Prompt

Determine the review prompt:

- If the **caller provided a review prompt** (in the Agent task context), use it as-is
- If **no prompt was provided** (standalone invocation), determine what to review from conversation context and build a prompt using `/codex-exec` XML tags (`<task>`, `<structured_output_contract>`, and optionally `<dig_deeper_nudge>`)

When building a standalone prompt, use P0-P3 priorities: P0 (fundamentally flawed), P1 (significant gap), P2 (moderate issue), P3 (minor improvement). Example:

```
<task>
Review the following for issues that would cause incorrect behavior or get an implementer stuck.
</task>

<structured_output_contract>
For each issue: (1) problem, (2) location, (3) impact, (4) suggested fix, (5) priority P0-P3.
If no issues, state that it looks sound.
</structured_output_contract>
```

## Step 2: Run `/codex-exec` Skill

Run the `/codex-exec` skill in read-only mode with the review prompt.

When the prompt covers **multiple review dimensions** (e.g., correctness, security, quality, API usage), wrap the task list with parallel fan-out instructions so codex delegates each dimension to a separate sub-agent. Add to the prompt:

```
Delegate each review dimension to a separate sub-agent using spawn_agent so they run in parallel. Wait for all agents to complete, then synthesize their findings into a unified report.
```

See `/codex-exec` [references/parallel-execution.md](../codex-exec/references/parallel-execution.md) for details on codex parallel execution.

## Step 3: Return Findings

Return the codex output. The caller determines what to do with the findings.
