---
name: subagent-driven-development
description: "Fresh-subagent-per-task execution with two-stage review gates."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
routing:
  triggers:
    - "subagent per task"
    - "fresh context execution"
    - "plan execution"
    - "execute plan with agents"
    - "fresh context per task"
  category: process
  pairs_with:
    - pair-programming
    - testing-agents-with-subagents
---

# Subagent-Driven Development Skill

## Instructions

### Phase 1: SETUP

**Goal**: Extract all tasks and establish project context before any implementation begins.

**Step 1: Read plan and extract tasks**

Read the plan file ONCE. Extract every task with full text:

```markdown
## Tasks Extracted from Plan

**Task 1: [Title]**
Full text: [Complete task description from plan]
Files: [List of files to create/modify]
Verification: [How to verify this task]

**Task 2: [Title]**
...
```

**Why**: Providing complete task text inline prevents subagents from burning tokens reading files and pollutes their context if they need to refer back to the plan. This isolation is critical for clean review cycles.

**Step 2: Create TodoWrite**

Create TodoWrite with ALL tasks:
```
1. [pending] Task 1: [Title]
2. [pending] Task 2: [Title]
3. [pending] Task 3: [Title]
```

**Why**: TodoWrite gives the operator visibility and prevents task slip.

**Step 3: Gather scene-setting context**

Before dispatching any implementer, capture:
- Current branch status (`git status`)
- Capture BASE_SHA: `git rev-parse HEAD` -- required for final integration review
- Relevant existing code patterns (naming conventions, error handling style)
- Project conventions from CLAUDE.md
- Dependencies and setup requirements

This context gets passed to EVERY subagent to prevent repeated discovery and question loops.

**Why**: Early context capture answers 80% of subagent questions before they ask, unblocks implementation immediately, and must be collected once (not rediscovered per task). BASE_SHA must be captured BEFORE the first implementer runs because subsequent edits will move HEAD forward.

**Step 4: Determine parallel vs sequential dispatch (scope-overlap check)**

Each extracted task already carries its `Files:` list. Feed those file scopes into the deterministic overlap checker before defaulting to sequential. Tasks whose scopes do not overlap can run in parallel; only overlapping tasks must serialize.

```bash
python3 scripts/check-scope-overlap.py \
  --tasks '[{"id":"task-1","scope":["path/a.py"]},{"id":"task-2","scope":["path/b.py"]}]' \
  --human   # use --check for exit 0 (no conflicts) / exit 1 (conflicts) in scripted gates
```

Each task object takes `id` (string) and `scope` (list of file/dir paths); add `"readonly": true` for tasks that only read a path. Directory entries match any file beneath them. The output reports conflicting pairs plus parallel groups and a dispatch recommendation. Use those groups to decide Phase 2 dispatch: parallelize within a group, serialize across overlapping tasks.

**Gate**: All tasks extracted with full text. BASE_SHA captured. Scene-setting context gathered. Scope-overlap check run; parallel groups identified. Proceed only when gate passes.

### Phase 2: EXECUTE (Per-Task Loop)

**Goal**: Implement each task with a fresh subagent, then verify through two-stage review.

**Step 1: Mark task in_progress**

Update TodoWrite status for the current task.

**Step 2: Dispatch implementer subagent**

Use the Task tool with the prompt template from `./implementer-prompt.md`. Include:
- Full task text (Replace with "see plan" -- subagents must have complete context)
- Scene-setting context
- Clear deliverables
- Permission to ask questions

**Implementation constraints** (enforced inline):
- Implementer must understand task fully before coding begins. If they ask questions: answer clearly and completely, provide additional context, re-dispatch with answers. Give them time to fully understand the task.
- Dispatch follows the Phase 1 scope-overlap decision: parallelize tasks within a non-overlapping group; serialize tasks whose file scopes overlap, because overlapping file edits cause conflicts that are expensive to resolve. When the overlap check reports any conflict, run those tasks sequentially.
- Implementer MUST follow these steps in order:
  1. Understand the task fully
  2. Ask questions if unclear (BEFORE implementing)
  3. Implement following TDD where appropriate
  4. Run tests
  5. Self-review code
  6. Commit changes

**Why scope-aware dispatch**: When task scopes overlap, parallel edits to the same files break file-locking semantics and require complex merge handling — those tasks serialize so each output feeds the next. When scopes are disjoint (verified by the scope-overlap check), parallel dispatch is safe and faster. The check makes the choice deterministic instead of defaulting to sequential for every plan.

**Step 3: Dispatch ADR compliance reviewer subagent**

Use the prompt template from `./adr-reviewer-prompt.md`. The ADR compliance reviewer checks:
- Does implementation match the ADR EXACTLY?
- Is anything MISSING from requirements?
- Is anything EXTRA that was not requested?

**Two-stage review constraint** (enforced inline): run ADR compliance review first, then code quality review. ADR compliance gates code quality because code that doesn't match requirements is wrong, regardless of how well-written. Reviewing code quality on functionally wrong code wastes the quality reviewer's effort.

If ADR compliance reviewer finds issues: dispatch new implementer subagent with fix instructions. ADR compliance reviewer reviews again. Repeat until ADR compliance passes.

**Max retries: 3** -- After 3 failed ADR compliance reviews, STOP and escalate:
> "ADR compliance failing after 3 attempts. Issues: [list]. Need human decision."

**Why escalation after 3 retries**: 3 retries = ~15-20 min of subagent time. If unresolved by then, the problem is structural (ADR is ambiguous, requirements conflict, or subagent fundamentally misunderstood something). Continuing loops wastes tokens. Human needs to decide: clarify ADR, adjust requirements, or accept the implementation as-is.

**Step 4: Dispatch code quality reviewer subagent**

Use the prompt template from `./code-quality-reviewer-prompt.md`. The code quality reviewer checks:
- Code is well-structured
- Tests are meaningful
- Error handling is appropriate
- No obvious bugs

**Quality review sequencing** (enforced inline): Only dispatch quality reviewer AFTER ADR compliance passes. Code quality review focuses on how well requirements are met, not whether wrong things were built.

If quality reviewer finds issues: implementer fixes Critical and Important issues (Minor issues are optional). Quality reviewer reviews again.

**Max retries: 3** -- After 3 failed quality reviews, STOP and escalate:
> "Quality review failing after 3 attempts. Issues: [list]. Need human decision."

**Why different retry limits for both stages**: Both stages can get stuck. Both deserve a fair number of attempts (3 each = up to 60 min total per task). Both hitting the limit means something is wrong with the process or the task definition itself.

**Step 5: Mark task complete**

Only when BOTH reviews pass:
```
Task [N]: [Title] -- COMPLETE
  ADR compliance: PASS
  Code quality: PASS
```

Return to Step 1 for the next task.

**Gate**: Both ADR compliance and code quality reviews pass. Task marked complete in TodoWrite. Proceed only when gate passes.

### Phase 3: FINALIZE

**Goal**: Verify the full implementation works together and complete the workflow.

**Step 1: Final integration review**

Dispatch a reviewer subagent for the entire changeset (diff from BASE_SHA to HEAD):
- All tests pass together
- No integration issues between tasks
- No conflicting patterns or redundant code

**Why final integration review after all tasks**: Per-task reviews ensure each task is correct in isolation. Final integration review catches cross-task problems: Task 1 and Task 3 both define the same utility, tests pass individually but conflict when run together, or Task 2 introduced a breaking change that Task 4 didn't account for. This catch-all review is why BASE_SHA was captured upfront.

**Step 2: Complete development workflow**

Use the appropriate completion path:
- `/pr-workflow` to create PR
- Manual merge
- Keep branch for further work

**Gate**: Final review passes. All tests pass. Integration verified. Proceed only when gate passes.

---

## Error Handling

### Error: "Subagent Asks Questions Mid-Implementation"
Cause: Insufficient context in the dispatch prompt
Solution:
1. Answer all questions clearly and completely
2. Add the missing context to the scene-setting for future tasks
3. Re-dispatch implementer with answers included

**Prevention**: The answer-questions-first constraint prevents this by design. If a subagent still asks questions after full context, they're asking for clarification on the ADR itself, which is valuable signal that requirements are ambiguous.

### Error: "Review Loop Exceeds 3 Retries"
Cause: ADR ambiguity, fundamental misunderstanding, or unreasonable review criteria
Solution:
1. STOP the loop immediately
2. Summarize all issues and attempted fixes for the user
3. Ask user to clarify ADR or adjust requirements
4. Resume only after user provides direction

**Why hard limit**: Review loops that fail to converge are expensive and signal a deeper problem. Continuing them burns tokens without progress. Human judgment is needed to decide whether to clarify, change, or accept.

### Error: "Subagent File Conflicts"
Cause: Multiple subagents modifying overlapping files — the scope-overlap check missed an overlap because a task's declared `scope` list was incomplete.
Solution:
1. Resolve conflicts manually
2. Re-run the affected review stage
3. Re-run `check-scope-overlap.py` with the corrected (complete) scope lists, then serialize the now-overlapping tasks

**Why this happens**: Parallel dispatch is only safe for disjoint scopes. A conflict means the declared scopes understated the real file footprint. Complete the scope lists and let the overlap check re-group the tasks.

---

## References

### Prompt Templates
- `implementer-prompt.md`: Dispatch template for implementation subagents
- `adr-reviewer-prompt.md`: Dispatch template for ADR compliance review
- `code-quality-reviewer-prompt.md`: Dispatch template for code quality review
