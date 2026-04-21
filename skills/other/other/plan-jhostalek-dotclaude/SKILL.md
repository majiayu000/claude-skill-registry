---
name: plan
description: Use when a task is multi-step, ambiguous, or high-impact and you need an executable implementation plan before editing code.
argument-hint: [task description]
---

task = $ARGUMENTS

Produce the minimum artifact that prevents the executor from going wrong. The executor starts with an empty context window: they get this plan and the codebase, nothing else. Every ambiguity becomes a wrong guess they make confidently.

Match depth to complexity. A 3-file bug fix needs a paragraph, not a document.

## Exploration

Explore until you can articulate *why* one approach beats alternatives — then stop and write. If you can't articulate the tradeoffs, you haven't explored enough. If you're still reading files after the picture is clear, you've explored too much.

Two axes, pursued concurrently via read-only exploration teammates:

- **Codebase** — existing implementations, patterns, conventions. Reference them so the executor follows established precedent.
- **External** — web search for how others solved this. Libraries, vendor docs, open-source implementations. Borrow before inventing.

## Decomposition

Choose based on task shape, not habit. Default to vertical slice; switch when the task clearly fits another:

| Strategy | When | Risk it mitigates |
|----------|------|---------------------|
| **Vertical slice** | Multiple independent behaviors | Integration surprises — each slice proves end-to-end |
| **Walking skeleton** | Uncertain integration path | Late-stage "it doesn't connect" — proves wiring first |
| **Layer-by-layer** | Clear layers, different complexity zones | Allows parallel work; natural when data model drives everything |

## Specificity

The hard part of planning is identifying the *surface of change* — which files, which functions, which call sites. Once the surface is named, the edits are obvious. Name concrete files and functions; describe *what* changes and *why*; reference precedent for the pattern to follow. Leave *how* to the executor — they need goals and constraints, not pseudocode.

- **Under-specified:** `Add a rate limiter to the API.`
- **Over-specified:** Pseudocode of the rate-limit check, variable names, HTTP status codes.
- **Calibrated:** `Add per-user rate limiting to authenticated endpoints. New middleware in src/api/middleware/ratelimit.py following the pattern of src/api/middleware/auth.py (middleware class + decorator registration in src/api/app.py:42). Use the existing Redis client from src/infra/redis.py.`

Litmus tests:
- "Could the executor start in the wrong file?" → be more specific.
- "Could the executor implement this without reading my plan?" → the step is too detailed.

## Plan Format

Required:

- **Goal** — One sentence. What exists after that didn't before.
- **Files** — Exact paths with `[NEW]`/`[MOD]`/`[DEL]` prefix. Map the change surface before decomposing into steps.
- **Steps** — Ordered, checkboxed (`- [ ]`), each naming the file(s) it touches.
- **Verification** — Per-step: command + expected result. Final: acceptance criteria the executor checks before declaring done.

Add when the task warrants:

- **Background** — The *why*, when not obvious from the goal.
- **Key Concepts** — Domain terms, sentinel values, non-obvious patterns. Table format.
- **Approach & Rejected Alternatives** — What you chose and rejected, with rationale. Prevents re-litigating decisions.
- **Edge Cases** — The 3–5 most likely failure modes and how the plan handles each. If you can't name them, you haven't understood the problem deeply enough.
- **Risks** — Only non-obvious ones with mitigations.
- **Work Decomposition** — For `/orch`: which steps run in parallel vs. sequential, and why.

## Save & Handoff

Save to `docs/plans/<type>-<short-name>.md` (adapt to project conventions if established). Types: `feat-`, `fix-`, `refactor-`, `chore-`.

To update an existing plan, re-read it, diff against new requirements, and revise in place.

Hand off to `/code` for single-agent execution or `/orch` for parallel work.
