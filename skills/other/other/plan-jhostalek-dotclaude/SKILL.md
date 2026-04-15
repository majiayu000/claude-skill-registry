---
name: plan
description: Use when a task is multi-step, ambiguous, or high-impact and you need an executable implementation plan before editing code.
argument-hint: [task description]
---

task = $ARGUMENTS

Create an executable implementation plan for this task.

## Core Constraint

The executing agent starts with an empty context window. They get this plan and the codebase — nothing else. No conversation history, no shared understanding. Every ambiguity you leave becomes a wrong guess they make confidently.

Match plan depth to task complexity — a 3-file bug fix needs a paragraph, not a document. The plan should be the minimum artifact that prevents the executor from going wrong.

## Exploration

Explore until you can articulate *why* one approach beats alternatives — then stop exploring and write. If you can't articulate the tradeoffs, you haven't explored enough. If you're still reading files after the picture is clear, you've explored too much.

Two dimensions, run in parallel:

- **Codebase** — existing implementations, patterns, conventions, similar features. Reference these so the executor follows established patterns.
- **External** — web search - how others solved this. Search for libraries, vendor docs, open source implementations. Learn from their experience before designing from scratch.

Spawn read-only exploration teammates for parallel search.

## Decomposition

Choose based on task shape, not habit:

| Strategy | When | Risk it mitigates |
|----------|------|---------------------|
| **Vertical slice** | Multiple independent behaviors | Integration surprises — each slice proves end-to-end |
| **Walking skeleton** | Uncertain integration path | Late-stage "it doesn't connect" — proves the wiring first |
| **Layer-by-layer** | Clear layers, different complexity zones | Allows parallel work; natural when data model drives everything |

Default to vertical slice. Switch when the task shape clearly fits another.

## Specificity

Name concrete files and functions in every step. Describe *what* changes and *why*. Specify the pattern to follow by linking to precedent. Leave *how* to the executor — they need goals and constraints, not pseudocode.

The litmus tests: "Could the executor start working in the wrong file or with the wrong approach?" — be more specific. "Could the executor implement this without reading my plan?" — the step is too detailed.

## Plan Format

Every plan needs:

- **Goal** — One sentence. What exists after that didn't before.
- **Files** — Exact paths. `[NEW]`/`[MOD]`/`[DEL]` prefix. Map the change surface before decomposing into steps.
- **Steps** — Ordered, checkboxed (`- [ ]`), with verification per step. Each step names the file(s) it touches.
- **Verification** — Per-step: command to run + expected result. Final: acceptance criteria the executor checks before declaring done.

Include when the task warrants it:

- **Background** — The *why*, when it's not obvious from the goal.
- **Key Concepts** — Domain terms, sentinel values, non-obvious patterns. Table format.
- **Approach & Rejected Alternatives** — What you chose and rejected, with rationale. Prevents re-litigating decisions.
- **Edge Cases** — The 3-5 most likely failure modes and how the plan handles each. If you can't name them, you haven't understood the problem deeply enough.
- **Risks** — Only non-obvious ones with mitigations.
- **Work Decomposition** — For `/orch`: which steps can run in parallel, which are sequential, and why.

## Save & Handoff

Save to `docs/plans/<type>-<short-name>.md` (adapt to project conventions if a different location is established). Types: `feat-`, `fix-`, `refactor-`, `chore-`.

To update an existing plan, re-read it, diff against new requirements, and revise in place.

Hand off to `/code` for single-agent execution or `/orch` for parallel work.
