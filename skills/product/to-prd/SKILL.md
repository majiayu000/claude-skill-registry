---
name: to-prd
description: Synthesize current conversation context and codebase understanding into a PRD artifact (markdown file by default, GitHub issue via flag). Trigger when the user asks for a PRD, requirements doc, feature spec, or wants to crystallize an in-flight discussion into a durable artifact before planning. PRD precedes implementation planning.
---

Synthesize a PRD from what you already know. Do NOT interview — extract from context, codebase exploration, and prior decisions. Iterate the artifact in place; commit when the user signs off.

## Emission Modes [LOCKED]

**Default (file mode):** Write to `<project-root>/docs/prd/<feature>.md`. Idempotent — overwrite on rerun. Use file mode when no flag is passed, when working offline, when the repo has no GitHub remote, or when the user explicitly wants a tracked file.

**Flag mode (`--emit-issue`):** Submit via `gh issue create --title "PRD: <feature>" --body-file <tmp>`. Use only when the user explicitly opts in or the project's convention is issue-tracked PRDs (check `<project-root>/CONTRIBUTING.md` and `.github/ISSUE_TEMPLATE/`).

When ambiguous, default to file mode and ask the user one targeted question rather than guessing.

## Process

### 1. Reuse priming if available; explore only when context is thin

If conversation context already covers domain language, naming conventions, and module shape, skip discovery and proceed to step 2. Otherwise dispatch an Explore agent over the codebase. Goal: current architectural state, naming conventions, ADRs, domain language. Read `CONTEXT.md`, `AGENTS.md`, `docs/adr/`, and any `UBIQUITOUS_LANGUAGE.md`. Use `fd -e md . docs/` then `bat -P -p -n -r` for targeted reads.

### 2. Identify deep modules

Sketch modules to build or modify. Prefer **deep modules** — large functionality behind a narrow, stable interface — over shallow modules. Surface 3-7 candidates and their interfaces. Recommend which modules deserve isolated tests; defer to user on edge cases.

### 3. Verify intent only when blocked

If the module breakdown is unambiguous from prior context, skip this step and proceed to writing. Ask the user only when an axis (scope, depth, or test coverage) is genuinely unresolved or when a decision is reversible-but-costly. Surface one unresolved axis at a time with a recommendation; never ask three default-bound axes at once.

### 4. Write the PRD

Render the template below. In file mode, write to `docs/prd/<feature>.md` and `git add` it. In flag mode, write to `/tmp/prd-<feature>.md` then `gh issue create --body-file /tmp/prd-<feature>.md`.

## Template

```
# PRD: <feature>

## Problem Statement
The user-visible problem, framed from the user's perspective. No internal jargon.

## Solution
The user-visible resolution. Behavior, not implementation.

## User Stories
Numbered, exhaustive. Format: `As an <actor>, I want <feature>, so that <benefit>`.

## Implementation Decisions
- Modules to build/modify and their interface contracts
- Architectural decisions (no file paths, no code snippets — they go stale)
- Schema changes, API contracts, key interactions

## Testing Decisions
- What makes a test durable: assert on observable behavior through public interfaces, not internal state
- Which modules earn tests
- Prior art: link to similar tests already in the codebase by name (not path)

## Out of Scope
Explicit non-goals.

## Further Notes
Open questions, follow-ups, deferred decisions.
```

User-story examples across stacks:
1. As a Rust crate consumer, I want zero-copy deserialization, so that hot paths avoid heap traffic.
2. As a TypeScript SPA user, I want optimistic updates with rollback, so that latency feels invisible.
3. As an API caller (any language), I want idempotent retries, so that partial failures are recoverable.

## Iteration Loop

PRD is a living artifact. On every rerun: diff current artifact against latest context (`difft` if file mode); extend or revise sections; never silently drop existing content; bump `Last-revised: <ISO date>` footer.

## Handoff

The PRD file produced here is the **input contract** for downstream implementation planning. Implementation planners read `docs/prd/<feature>.md` (or fetch the issue body in flag mode) and produce the implementation plan. Hand off the path or issue URL explicitly.
