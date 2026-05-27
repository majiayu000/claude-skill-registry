---
name: receive-feedback
description: Process external code review feedback with technical rigor. Use when receiving feedback from another LLM, human reviewer, or CI tool. Verifies claims before implementing, tracks disposition.
disable-model-invocation: false
---

# Receive Feedback

## Overview

Process code review feedback with verification-first discipline.
No performative agreement. Technical correctness over social comfort.

The orchestrator **verifies** and **dispatches**. It never edits files itself.
Every valid item is fixed by a dedicated subagent spawned in parallel.

## Quick Reference

```text
┌─────────────┐     ┌──────────────┐     ┌──────────────────────┐
│   VERIFY    │ ──▶ │   CONFIRM    │ ──▶ │   DISPATCH FIXES     │
│ (tool-based)│     │ ("launch     │     │ (one subagent per    │
│             │     │  fixes for   │     │  valid item, run in  │
│             │     │  1,2,3?")    │     │  parallel)           │
└─────────────┘     └──────────────┘     └──────────────────────┘
```

## Core Principle

**Verify, confirm once, then dispatch subagents. The orchestrator does not fix.**

If a bug is valid, a subagent fixes it. Full stop. No deferral, no excuses.

## When To Use

- Receiving code review from another LLM session
- Processing PR review comments
- Evaluating CI/linter feedback
- Handling suggestions from pair programming

## Workflow

1. **Verify every item** against the current codebase (tools, not memory).
2. **Classify** each item as **VALID** (must fix) or **INVALID** (reject with evidence).
   - Truly unparseable items get one clarification question. That is the only escape.
3. **Print** a short summary: invalid items with evidence, valid items numbered.
4. **Ask exactly one prompt**: `launch fixes for 1,2,3?` (list every valid item's number — the default proposal is always the full valid set).
5. **Resolve the user's reply**:
   - Confirmation (`y`, `yes`, `go`, `ok`, `do it`, `lgtm`, or just ↵) → dispatch the full proposed set.
   - A comma/space-separated list of numbers (e.g. `1,3` or `1 3 4`) → dispatch only those numbers. They must be a subset of the proposed valid set. Items the user omits are NOT marked deferred — they are simply not run this round.
   - `no` / `cancel` / `stop` → halt without dispatching.
   - Anything else → re-print the prompt once; do not invent a new disposition.
6. **Spawn one subagent per chosen item, all in a single message** so they run in parallel. The orchestrator MUST NOT call Edit / Write / NotebookEdit for any fix.
7. **Collect** subagent results and emit the final response table.

## Forbidden Behaviors

These are non-negotiable. The orchestrator may **not**:

- Ask the user *which* items to fix. The only question allowed is `launch fixes for <numbers>?`, where `<numbers>` defaults to the full valid set. (The user may override by replying with their own subset of numbers — that is a user override, not an agent question.)
- Claim an issue is **pre-existing**. If a reviewer found it on this PR, it is in scope.
- Claim an issue is **out of scope** for the PR. If the bug exists on this branch, the PR owns it.
- **Defer** a valid item to "later", a "backlog", a "follow-up PR", or a "future ticket".
- Use any reasoning — risk, complexity, time, churn, "minor", "cosmetic", "edge case" — to avoid fixing a valid item.
- **Edit code directly.** Every fix is performed by a spawned subagent.
- Bundle multiple fixes into one subagent. One valid item = one subagent.

A valid bug raised by a code or security reviewer **must** be fixed by a subagent. There is no other option.

## Hard Gates

Do not advance to the next gate until its **pass condition** is true. Details live in `VERIFICATION.md`, `EVALUATION.md`, and `RESPONSE.md`.

**Gate 1 — Verification evidence (per item)**

1. Locate the referenced code or behavior (`Read`, `Grep`, tests, or another check from `VERIFICATION.md`).
2. Record the outcome: **VALID** (claim holds and is actionable) or **INVALID** (claim fails), with an artifact (file path and line range, command/test result, or short quoted tool output — not paraphrase alone).
3. If unparseable, mark **NEEDS CLARIFICATION** with the specific question. Do not invent a disposition.

**Pass when:** Every item has VALID / INVALID / NEEDS CLARIFICATION plus an artifact. **Fail (stop):** Proceeding without an artifact, or downgrading a VALID item to "skip" / "defer" / "pre-existing" / "out of scope".

**Gate 2 — Single batch confirmation**

1. Print the invalid items (with rejection evidence) and the valid items (numbered).
2. Ask the **single** prompt: `launch fixes for <comma-separated numbers>?` — `<numbers>` MUST be the full valid set. Do not pre-narrow it.
3. Accept the user's reply per the Workflow resolution rules: confirmation → full set; subset of numbers → that subset only; refusal → halt.

**Pass when:** The user confirms or supplies a subset of the proposed numbers, and the chosen set is locked in writing before Gate 3. **Fail (stop):** Proposing a narrowed default, asking "which would you like to fix?", or proposing to defer any valid item.

**Gate 3 — Parallel subagent dispatch**

1. In a single tool-use block, spawn one `Agent` per item in the user-chosen set. Each subagent gets: the original feedback text, the verification artifact, the file/line target, and the Fix-Quality Contract.
2. The orchestrator does not call `Edit`, `Write`, or `NotebookEdit` during this gate.

**Pass when:** Every item in the user-chosen set has a corresponding subagent invocation in the same message. **Fail (stop):** Fixing inline, serializing the subagents, or skipping any item the user actually chose.

**Gate 4 — Response artifact (batch)**

1. After subagents return, fill the structured template in `RESPONSE.md`.
2. The response has exactly two sections: **Implemented** and **Rejected**. There is no Deferred section.
3. Valid items the user explicitly excluded from this round get a single line under the table — `Not run this round: <numbers> (user-excluded)` — and nothing else. Do not label them deferred or out of scope.

**Pass when:** Every item appears in Implemented or Rejected with file:line citations, and any user-excluded valid items are listed verbatim under the table. **Fail (stop):** Shipping a summary that omits an item, lacks evidence on a rejection, or invents a "Deferred" bucket.

## Command Workflow

Use this skill from the `/receive-feedback` command or by invoking it directly with a feedback file path.

1. **Read** the feedback file at `$ARGUMENTS`
2. **Parse** individual feedback items, whether numbered, bulleted, or freeform
3. **Verify** each item per `VERIFICATION.md`
4. **Confirm** via single `launch fixes for <numbers>?` prompt
5. **Dispatch** one subagent per valid item in a single message
6. **Produce** the response summary defined in `RESPONSE.md`

## Expected Feedback File Format

```markdown
1. Remove unused import on line 15
2. Add error handling to the API call
3. Consider using a generator for large datasets
4. Fix typo in variable name: `usr` → `user`
```

Freeform prose is also acceptable; extract actionable items from the text.

## Subagent Dispatch Template

When spawning a fix subagent, the prompt MUST include:

- The original feedback text (verbatim).
- The verification artifact: file path, line range, and what was confirmed.
- The exact change required, or "implement the reviewer's suggestion as written" if the reviewer specified one.
- The fix-quality contract below, copied verbatim into every subagent prompt.

### Fix-Quality Contract (paste into every subagent prompt)

```text
You are fixing one code review finding. Hard requirements:

1. Make the fix. Do not defer. Do not declare anything out of scope.
   Do not call anything pre-existing. If you discover the fix needs to
   touch adjacent code to be correct, touch it.

2. The fix must be clean and architectural — idiomatic for the language
   and the file's surrounding patterns. Read enough of the
   surrounding module to match its conventions before editing.
   No inline hacks, no band-aids, no "minimum to make it green".

3. Do NOT over-engineer. No new abstractions, no speculative
   generality, no helper layers, no config knobs. Solve the actual
   reported problem. If three lines are right, write three lines.

4. Write NO comments unless a future reader would be genuinely
   confused without one (a non-obvious invariant, a workaround for a
   specific upstream bug, a hidden constraint). Never write comments
   that restate what the code does. Never write headers, banners,
   "fix:" markers, or "// added for review feedback" notes.
   Excessive comments are a defect — do not produce them.

5. Run the project's typecheck / lint for the file you touched if a
   command is obvious from the repo. Report what you ran.

6. Report back: the resulting diff, the file:line of the change, and
   one sentence on what you changed and why.
```

Use `subagent_type: "general-purpose"` unless a domain-specific agent is clearly better.

## Example

```bash
/receive-feedback reviews/pr-123-feedback.md
```

Reads the file, verifies each item, prints invalid/valid summary, asks `launch fixes for 1,3,4?`, and on confirmation spawns three subagents in parallel to fix items 1, 3, and 4.

## Files

- `VERIFICATION.md` - Tool-based verification workflow
- `EVALUATION.md` - Classification rules (VALID / INVALID / NEEDS CLARIFICATION)
- `RESPONSE.md` - Structured output format
- `references/skill-integration.md` - Using with code-review skills
