---
name: ralph-specum-research
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-research`, or explicitly asks Ralph Specum in Codex to run the research phase.
metadata:
  surface: helper
  action: research
---

# Ralph Specum Research

Use this for the research phase.

## Contract

- Resolve the active spec by explicit path, exact name, or `.current-spec`
- Respect `.claude/ralph-specum.local.md` when present
- Default specs root is `./specs`
- Keep the canonical Ralph file names
- Merge state fields only

## Action

1. Resolve the active spec. If none exists, stop and tell the user to start a spec first.
2. Read the goal, `.progress.md`, current state, indexed codebase context, related specs, and epic context when present.
3. Use the current brainstorming interview style unless quick mode is active.
4. Write or rewrite `research.md` in the spec directory.
5. Merge state with `phase: "research"` and `awaitingApproval: true`.
6. Update `.progress.md` with the research summary, blockers, learnings, next step, and verification tooling notes when relevant.
7. If spec commits are enabled, commit only the spec artifacts.
8. In quick mode, continue directly into requirements.

## Output Shape

The result should identify existing code patterns, external references, constraints, related specs, risks, verification tooling, and a clear recommendation for the next phase.

## Response Handoff

- After writing `research.md`, name `research.md` and summarize the research briefly.
- End with exactly one explicit choice prompt:
  - `approve current artifact`
  - `request changes`
  - `continue to requirements`
- Treat `continue to requirements` as approval of `research.md`.
