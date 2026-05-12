---
name: peer-review
description: "Run an independent peer review via Claude. Use when the user asks to \"peer review\", \"peer review my code\", \"peer review my plan\", \"peer review my spec\", \"peer review my shells\", \"get a second opinion\", or \"independent review\"."
---

# Peer Review

Independent peer review via Claude. Translates a natural-language review request into a Claude-specific prompt so invocations stay implementation-agnostic.

## Step 1: Determine Review Request

Extract from the current context:

- **Material** — code diff, files, plan, spec, shells, feedback, or other artifact to review
- **Review dimensions** — correctness, security, API usage, consistency, simplicity, coverage, plan readiness, spec quality, feedback interpretation, or explicit user criteria
- **Criteria** — reference file paths Claude should read directly, inline criteria text, or the material's own domain conventions
- **Output format** — findings schema, verdict labels, priority scale, and any required metadata fields

If no reviewable material is available, stop and state that material is required.

## Step 2: Build the Claude Prompt

Assemble a prompt for Claude:

- State that Claude is acting as an independent peer reviewer for Codex.
- Identify the exact material and scope. Prefer file paths and diff commands over pasted content when practical.
- Instruct Claude to read referenced criteria files directly.
- Preserve independent dimensions. If multiple dimensions are requested and Codex sub-agent fan-out is unavailable, ask Claude to review each dimension in a separately labeled section.
- Require the exact output format expected by the calling skill.
- Require evidence for every actionable finding.
- Tell Claude not to modify files.
- Tell Claude to perform the review itself rather than delegating to another peer review skill or back to Codex. The prompt has already crossed the tool boundary; further forwarding would loop.

## Step 3: Run `$claude-print` Skill

Run `$claude-print` in read-only mode with the assembled prompt.

## Step 4: Validate Output

Compare Claude's output against the dimensions and structure requested in Step 2, then classify it into one of three branches:

- **Claude returned the requested findings** — output them verbatim.
- **Incomplete output** (any reason — partial fan-out with missing dimensions, mid-run truncation, sections cut off, sub-agent failure, single-dimension review that ends mid-finding, etc.) — output what came back verbatim, name what is missing relative to Step 2's request, then append: "**Action required:** Peer review returned partial output. Use `request_user_input` to ask the user whether to retry peer review now (transient Claude errors like usage limits often clear within minutes) or proceed with the partial findings. State what is missing so the user can decide."
- **No output / Claude failed** — output a single notice stating the cause (usage limit, error, empty response), then append: "**Action required:** Peer review failed. Use `request_user_input` to ask the user whether to retry peer review now (transient Claude errors like usage limits often clear within minutes) or proceed without peer review."

Do not synthesize peer findings locally to fill a gap. Peer review's value is independence; locally written findings labeled "peer" mislead the consumer.

Then update or check the active plan and proceed to any remaining task.

## Rules

- `$peer-review` is the stable abstraction. Pipeline skills should not call `$claude-print` directly unless they need raw Claude print-mode behavior.
- Do not apply Claude findings directly. Evaluation and application belong to downstream skills.
