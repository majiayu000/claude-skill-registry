---
name: peer-review
description: "Run an independent peer review via codex. Use when the user asks to \"peer review\", \"peer review my code\", \"peer review my plan\", \"peer review my spec\", \"peer review my shells\", \"get a second opinion\", or \"independent review\"."
---

# Peer Review

Independent peer review via codex. Runs `/codex-exec` in read-only mode with a review prompt built from the input material.

## Step 1: Determine What to Review

Determine what to review from the input material (passed in via the task prompt when invoked as a sub-Agent) or from conversation context. If neither provides reviewable material, use `AskUserQuestion` to ask what to review.

## Step 2: Run `/codex-exec` Skill

Invoke `/codex-exec` via the Skill tool in read-only mode with a review prompt tailored to the material. Include the output format in a `<structured_output_contract>` tag:

```
<structured_output_contract>
For each issue, return:

### [P<N>] <title (imperative, ≤80 chars)>

**File:** `<file path>` or **Section:** <location>

<one paragraph explaining the issue and its impact>

Use priorities: P0 (fundamentally flawed), P1 (significant gap), P2 (moderate issue), P3 (minor improvement).
After all findings, add an Overall Verdict section with a 1-3 sentence assessment.
If no issues, state that it looks sound.
</structured_output_contract>
```

When the prompt covers **multiple review dimensions** (e.g., correctness, security, quality, API usage), wrap the task list with parallel fan-out instructions so codex delegates each dimension to a separate sub-agent. See `/codex-exec` [references/parallel-execution.md](../codex-exec/references/parallel-execution.md) for details on codex parallel execution.

## Step 3: Output Findings

Output the codex findings.
