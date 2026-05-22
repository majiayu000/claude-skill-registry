---
name: agent-ops-retrospective
description: "Scan the current chat session for durable learnings (clarifications, corrections, decisions, pitfalls) and update .agent/memory.md. Use after critical review and before concluding work."
category: core
invokes: [agent-ops-state, agent-ops-tasks]
invoked_by: []
state_files:
  read: [constitution.md, memory.md, focus.md, issues/*.md]
  write: [memory.md, focus.md, issues/*.md]
---

# Retrospective / Learning workflow (mandatory)

## Goal
Ensure durable, reusable insights from this chat session are captured in `.agent/memory.md` so future sessions can resume without re-discovering them.

## Inputs
- The current chat session transcript (user + assistant messages in this session)
- `.agent/constitution.md`, `.agent/memory.md`, `.agent/focus.md`, `.agent/issues/`

## Extraction rules (strict)
Only capture *durable* items:
- confirmed workflow rules
- stable project conventions (not one-off)
- confirmed commands (but commands/boundaries belong in constitution, not memory)
- user preferences that affect future work on this repo
- corrections to previous misunderstandings
- pitfalls/gotchas discovered during implementation

Do NOT capture:
- transient task state (belongs in focus)
- speculative ideas not adopted
- secrets/tokens
- personal/sensitive data

## Placement rules (strict)
- Project-specific commands/boundaries/constraints → `.agent/constitution.md`
- Durable workflow learnings and recurring conventions → `.agent/memory.md`
- Current session status → `.agent/focus.md`
- Follow-ups and approvals needed → `.agent/issues/`

## Procedure
1) Read: constitution/memory/focus/tasks.
2) Scan the chat session for:
   - explicit corrections ("No, do X instead of Y")
   - newly confirmed commands or tools
   - newly confirmed constraints ("never refactor", "only write docs in …")
   - repeated misunderstandings (add a "pitfall to avoid")
   - preferences expressed by the user
3) Update `.agent/memory.md`:
   - append a dated subsection: `## Retrospective YYYY-MM-DD`
   - add short, atomic bullets phrased as "Do/Don't/Prefer"
   - avoid duplication with constitution (link to constitution section if needed)
4) Update focus if the retrospective reveals unresolved items.
5) Invoke `agent-ops-tasks` discovery if actionable items found.
6) Do not declare completion unless retrospective has been run.

## Issue Discovery During Retrospective

**After scanning session, invoke `agent-ops-tasks` discovery for actionable items:**

1) **Collect actionable learnings:**
   - "We should add tests for X" → `TEST` issue
   - "This pattern is confusing, needs docs" → `DOCS` issue
   - "Found a bug but didn't fix it" → `BUG` issue
   - "This could be optimized later" → `PERF` issue
   - "Technical debt noticed" → `CHORE` or `REFAC` issue
   - "Security concern noted" → `SEC` issue

2) **Present to user:**
   ```
   📋 Retrospective identified {N} actionable items:
   
   Medium:
   - [DOCS] Document the retry mechanism in PaymentService
   - [TEST] Add integration tests for new OAuth flow
   
   Low:
   - [CHORE] Clean up commented-out code in UserController
   - [PERF] Consider caching user preferences (noted during implementation)
   
   Create issues for these? [A]ll / [S]elect / [N]one
   ```

3) **After creating issues:**
   - Mark in memory.md: "Created {ISSUE-IDs} for follow-up"
   - These become part of the project backlog
