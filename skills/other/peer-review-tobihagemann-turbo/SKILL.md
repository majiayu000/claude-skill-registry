---
name: peer-review
description: "Run an independent peer review via Codex. Use when the user asks to \"peer review\", \"peer review my code\", \"peer review my plan\", \"peer review my spec\", \"peer review my shells\", \"get a second opinion\", or \"independent review\"."
---

# Peer Review

Independent peer review via codex. Translates a natural-language review request into a codex-specific prompt so invocations stay implementation-agnostic.

## Step 1: Understand the Request

Identify from the invoking prompt or conversation context:

- **Material** — the code scope, artifact text, feedback items, or other content under review
- **Criteria** — reference file paths codex should read directly, inline criteria text, or the material's own domain conventions
- **Dimensions** — one review concern (single-pass) or multiple independent concerns (fan-out, one per dimension)
- **Skepticism guidance** — any material-specific instruction for pushing past surface findings; optional
- **Output format** — finding layout, priority scale, or verdict labels; optional

If no reviewable material is available, stop and state that material is required.

## Step 2: Build the Codex Prompt

Assemble the prompt using codex's XML tag conventions (see `/codex-exec` Prompt Shaping):

- **`<task>`** — the scope or material, criteria pointers (file paths codex should read, or inline criteria), and any needed context. When multiple independent dimensions are specified, wrap the dimension list with explicit parallel fan-out instructions so codex delegates each dimension to its own sub-agent and waits for all before synthesizing. See `/codex-exec` [references/parallel-execution.md](../codex-exec/references/parallel-execution.md) for the prompt pattern.

- **`<dig_deeper_nudge>`** — the skepticism guidance from the request if provided; otherwise the default: "Do not stop at surface-level findings. Check for second-order failures, transformation-chain bypasses, and cases where the material relies on unstated assumptions."

- **`<structured_output_contract>`** — the output format from the request if provided. Otherwise use the default, which aligns with the finding shape internal reviews emit so findings can be concatenated without transformation:

  ```
  ### [P<N>] <title (imperative, ≤80 chars)>

  **File:** `<file path>` (lines <start>-<end>) or **Section:** <location>
  **Reviewer:** peer (<dimension>)

  <one paragraph explaining the issue and its impact>
  ```

  The `(lines <start>-<end>)` slot is optional; include it when reviewing code, omit for section references. Include the `(<dimension>)` parenthetical whenever the request identifies a dimension label (covers both single- and multi-dimension cases); omit only for undifferentiated reviews where no dimension was named. Default priority scale: P0 (fundamentally flawed or blocking), P1 (significant gap or urgent), P2 (moderate issue), P3 (minor improvement). End with an Overall Verdict block containing a 1–3 sentence assessment. If there are no issues, state that the material looks sound.

Include an explicit instruction that codex perform the review itself rather than delegating to another peer review skill or back to Claude. The prompt has already crossed the tool boundary; further forwarding would loop.

## Step 3: Run `/codex-exec` Skill

Invoke `/codex-exec` via the Skill tool in read-only mode with the assembled prompt.

## Step 4: Shape the Response

Compare codex's output against the dimensions and structure requested in Step 2, then classify it into one of three branches:

- **Codex returned the requested findings** — output them verbatim.
- **Incomplete output** (any reason — partial fan-out with missing dimensions, mid-run truncation, sections cut off, sub-agent failure, single-dimension review that ends mid-finding, etc.) — output what came back verbatim, name what is missing relative to Step 2's request, then append: "**Action required:** Peer review returned partial output. Use the `AskUserQuestion` tool to ask the user whether to retry peer review now (transient codex errors like usage limits often clear within minutes) or proceed with the partial findings. State what is missing so the user can decide."
- **No output / codex failed** — output a single notice stating the cause (usage limit, error, empty response), then append: "**Action required:** Peer review failed. Use the `AskUserQuestion` tool to ask the user whether to retry peer review now (transient codex errors like usage limits often clear within minutes) or proceed without peer review."

Do not synthesize peer findings locally to fill a gap. Peer review's value is independence; locally written findings labeled "peer" mislead the consumer.

Then use the TaskList tool and proceed to any remaining task.

## When You Are a Subagent

If you are a subagent, follow the guardrails in [references/subagent-wrapping.md](references/subagent-wrapping.md). Otherwise codex events can drop after you emit final text, producing a false-empty return that silently bypasses Step 4's `AskUserQuestion` gate.
