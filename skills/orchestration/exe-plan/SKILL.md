---
name: exe-plan
description: "ONLY when user explicitly types /exe-plan. Never auto-trigger on execute, run, or implement."
argument-hint: "[--sequential]"
---

# /exe-plan - Execute Plan via Orchestrated Subagents

Execute plan.md by delegating phases to subagents. Main thread orchestrates; subagents execute.

## Flags

- `--sequential`: Force sequential execution (ignore parallel groups)
- Default: Parallel when dependency groups allow

## Orchestrator Role (CRITICAL)

Main thread is **orchestrator only**:
- Reads plan.md ONCE at start
- Tracks phase completion status
- Dispatches subagents with isolated context
- Reports progress to user
- Archives on completion

Orchestrator **NEVER**:
- Executes phase tasks directly
- Reads files beyond plan.md and done-phase-*.md
- Accumulates phase details in its context

Preserves main context window for orchestration across many phases.

## Orchestrator Flow

```
1. LOAD
   - Read plan.md
   - Verify marker: <!-- @plan: /create-plan ... --> (timestamp optional)
   - Parse phases, dependencies, parallel groups
   - Create plan-results/ folder
   - Store only: phase numbers, deps, groups, titles (NOT full task lists)

2. SCAN EXISTING
   - Check plan-results/done-phase-*.md
   - Mark completed phases (enables resume after failure)
   - Do NOT read done file contents (just check existence)

3. EXECUTE LOOP
   While phases remain:
   a. Identify ready phases (deps satisfied, not done)
   b. Group by parallel safety:
      - If --sequential: take first ready only
      - Else: take all ready in same parallel group
      - NEVER run phases from different groups in parallel
   c. Spawn subagent(s):
      - One Task tool call per phase
      - Multiple ready in same group: ONE message with MULTIPLE Task calls
      - Subagent type: general-purpose
   d. Await results:
      - On ANY failure: STOP immediately (fail-fast)
   e. Record: "✓ Phase N: [summary]"
      - Do NOT store subagent details in orchestrator context
   f. Continue loop

4. FINALIZE (on success)
   - Timestamp: powershell "Get-Date -Format 'yyMMdd-HHmm'"
   - Create archive at REPO ROOT: was-plan-YYMMDD-HHMM/
   - Move plan-results/* into archive
   - Move plan.md into archive
   - Verify archive contains: plan.md + all done-phase-*.md
   - **CRITICAL:** Archive folder MUST be at repository root, never in subdirectories

5. REPORT
   - Summary of completed phases
   - Failure details if stopped
   - Archive location if complete
```

## Archival Checklist

On success, archive folder MUST be at **repository root**:
```
<repo-root>/was-plan-YYMMDD-HHMM/
├── plan.md              ← MOVED from repo root
├── done-phase-01.md
├── done-phase-02.md
└── ...
```

**IMPORTANT:**
- plan.md moves INTO the archive, not just plan-results/
- Archive folder MUST be at repo root (NEVER in subdirectories like nhand/)

## Subagent Dispatch

### Context Isolation

Each subagent receives ONLY:
- Goal summary (1-2 sentences)
- Its phase details (copy from plan.md)
- Completed phase NUMBERS (not contents)
- Output path for done file

Subagents do NOT receive:
- Other phases' task lists
- Contents of other done-phase files
- Full plan.md (only relevant excerpt)

### Dispatch Template

Spawn with Task tool (subagent_type: general-purpose):

```markdown
# Context
Goal: [1-2 sentence goal from plan.md header]
Working directory: [absolute path]
Completed phases: [comma-separated numbers, e.g., "1, 2, 3"]

# Your Assignment: Phase N

[COPY exact phase section from plan.md, preserving ALL fields:]
## Phase N: [title] [COMPLEXITY]
**Depends:** [deps]
**Modifies:** [file/directory scope]
**Tasks:**
- [ ] Task 1
- [ ] Task 2
...

[If phase has Reference: section, include it]

# Instructions
1. Execute all tasks in order
2. Read necessary files (subagent explores independently)
3. Stay within **Modifies:** scope
4. On success: Write to plan-results/done-phase-NN.md
5. On failure: Stop immediately, return error details
6. Return 1-2 sentence summary

# done-phase-NN.md Format
[standard format below]
```

### Context Budget

- Goal: 1-2 sentences
- Phase section: Exact copy (typically 5-20 lines)
- Completed phases: Numbers only
- **Target:** 50-150 lines; if larger, phase may need decomposition

### Done File Format

```markdown
# Phase N: [title]
**Completed:** YYYY-MM-DD HH:MM
**Status:** success

## Tasks
- [x] Task 1 - [brief note]
- [x] Task 2 - [brief note]

## Results
[What was accomplished]

## Notes
[Observations, warnings, follow-up items]
```

### Parallel Dispatch

Multiple phases ready in SAME parallel group:
1. Compose ONE message with MULTIPLE Task tool calls
2. All Task calls in single message = parallel execution
3. Wait for ALL to complete before proceeding

```
# CORRECT - parallel (one message, multiple tools)
<assistant message>
  <Task call for Phase 4>
  <Task call for Phase 5>
</assistant message>

# WRONG - sequential (separate messages)
<assistant message><Task call for Phase 4></assistant message>
<assistant message><Task call for Phase 5></assistant message>
```

### Subagent Response Contract

```json
{
  "phase": 4,
  "status": "success|failed",
  "summary": "Renamed legacy_api.py → api_client.py",
  "error": null | "File not found: ..."
}
```

## Live Output Format

```
/exe-plan

Loading plan.md... 9 phases, 4 parallel groups
Resuming: phases 1-3 already complete

Executing Group C (parallel):
  ├─ Phase 4: Renaming files in app-client...
  ├─ Phase 5: Updating code in app-client...
  ├─ Phase 6: Renaming files in app-server...
  └─ Phase 7: Updating code in app-server...

  ✓ Phase 4: Renamed legacy_api.py → api_client.py
  ✓ Phase 6: Renamed server.log → app_server.log
  ✓ Phase 7: Updated 5 files in app-server
  ✓ Phase 5: Updated 8 strings in app-client

Executing Group D (sequential):
  ├─ Phase 8: Setting up .gitignore files...
  ✓ Phase 8: Configured 3 .gitignore files

  ├─ Phase 9: Initializing git repos...
  ✓ Phase 9: Initialized 3 repos with initial commits

──────────────────────────────────
Plan complete. 9/9 phases succeeded.
Archive: was-plan-260122-0845/
```

## Failure Output Format

```
/exe-plan

Loading plan.md... 9 phases, 4 parallel groups

Executing Group B (parallel):
  ├─ Phase 2: Copying template → app-client...
  ├─ Phase 3: Copying scaffold → app-server...

  ✓ Phase 2: Copied template → app-client
  ✗ Phase 3: FAILED - scaffold/ directory not found

──────────────────────────────────
Plan stopped. 2/9 phases completed.

Failed: Phase 3
  Error: Directory /project/scaffold does not exist

Blocked: Phases 6,7,8,9 (depend on phase 3)

Fix the issue and run /exe-plan to resume.
Progress saved in plan-results/
```

## Resume Behavior

On re-run after failure:
1. Scan plan-results/done-phase-*.md
2. Skip phases with done files
3. Resume from first incomplete phase

## Constraints

### Orchestrator Rules
- NEVER modify plan.md during execution
- NEVER execute phase tasks directly (always delegate via Task tool)
- NEVER read file contents beyond plan.md and done-phase existence checks
- Keep orchestrator context minimal for multi-phase scalability

### Subagent Rules
- Write ONLY its own done-phase-NN.md
- Do NOT modify plan.md or other done files
- Explore codebase independently (read files as needed)
- Return brief summary only (detailed results in done file)

### Parallel Safety Rules
- Phases in same parallel group MUST NOT touch same files
- If collision risk: run sequentially (safety > speed)
- NEVER run phases from DIFFERENT groups in parallel
- Dependency chain: A → B means B waits for A's done file to exist

### Fail-Fast Rules
- STOP on first subagent failure
- Do NOT start new phases after any failure
- Keep plan-results/ intact for resume
- Report: which phase failed, what was blocked, how to resume

## Integration with /create-plan

Expects plan.md created by /create-plan with:

### Required Fields (per phase)
| Field | Purpose | Used By |
|-------|---------|---------|
| `## Phase N: [title] [COMPLEXITY]` | Identity + sizing hint | Dispatch, reporting |
| `**Depends:** [deps]` | Execution order | Dependency resolution |
| `**Tasks:**` | Work items | Subagent execution |

### Optional Fields (per phase)
| Field | Purpose | Used By |
|-------|---------|---------|
| `**Parallel:** Group X` | Parallel grouping | Batch dispatch |
| `**Modifies:** [scope]` | File scope | Collision detection, subagent focus |
| `**Reference:** [files]` | Context pointers | Subagent exploration |

### Phases Overview Table
```
| Phase | Name | Depends | Parallel Group | Complexity |
```
Used for: progress reporting, dependency graph, parallel batching.

### Marker Format
```
<!-- @plan: /create-plan YYMMDD_HHMM -->
```
Timestamp optional but helps identify plan version.
