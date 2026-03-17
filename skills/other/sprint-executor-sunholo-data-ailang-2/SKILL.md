---
name: AILANG Sprint Executor
description: Execute approved sprint plans with test-driven development, continuous linting, progress tracking, and pause points. Use when user says "execute sprint", "start sprint", or wants to implement an approved sprint plan.
---

# AILANG Sprint Executor

Execute an approved sprint plan with continuous progress tracking, testing, and documentation updates.

## Quick Start

**Most common usage:**
```bash
# User says: "Execute the sprint plan in design_docs/20251019/M-S1.md"
# This skill will:
# 1. Validate prerequisites (tests pass, linting clean)
# 2. Create TodoWrite tasks for all milestones
# 3. Execute each milestone with test-driven development
# 4. Run checkpoint after each milestone (tests + lint)
# 5. Update CHANGELOG and sprint plan progressively
# 6. Pause after each milestone for user review
```

## When to Use This Skill

Invoke this skill when:
- User says "execute sprint", "start sprint", "begin implementation"
- User has an approved sprint plan ready to implement
- User wants guided execution with built-in quality checks
- User needs progress tracking and pause points

## Core Principles

1. **Test-Driven**: All code must pass tests before moving to next milestone
2. **Lint-Clean**: All code must pass linting before moving to next milestone
3. **Document as You Go**: Update CHANGELOG.md and sprint plan progressively
4. **Pause for Breath**: Stop at natural breakpoints for review and approval
5. **Track Everything**: Use TodoWrite to maintain visible progress
6. **DX-First**: Improve AILANG development experience as we go - make it easier next time

## Multi-Session Continuity (NEW)

**Sprint execution can now span multiple Claude Code sessions!**

Based on [Anthropic's long-running agent patterns](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), sprint-executor implements the "Coding Agent" pattern:

- **Session Startup Routine**: Every session starts with `session_start.sh`
  - Checks working directory
  - Reads JSON progress file (`.ailang/state/sprints/sprint_<id>.json`)
  - Reviews recent git commits
  - Validates tests pass
  - Prints "Here's where we left off" summary

- **Structured Progress Tracking**: JSON file tracks state
  - Features with `passes: true/false/null` (follows "constrained modification" pattern)
  - Velocity metrics updated automatically
  - Clear checkpoint messages
  - Session timestamps

- **Pause and Resume**: Work can be interrupted at any time
  - Status saved to JSON: `not_started`, `in_progress`, `paused`, `completed`
  - Next session picks up exactly where you left off
  - No loss of context or progress

**For JSON schema details**, see [`resources/json_progress_schema.md`](resources/json_progress_schema.md)

## Available Scripts

### `scripts/session_start.sh <sprint_id>` **NEW**
Resume sprint execution across multiple sessions.

**When to use:** ALWAYS at the start of EVERY session continuing a sprint.

**What it does:**
1. **Syncs GitHub issues** via `ailang messages import-github`
2. Loads sprint JSON progress file
3. Shows linked GitHub issues with titles from local messages
4. Displays feature progress summary
5. Shows velocity metrics
6. Runs tests to verify clean state
7. Prints "Here's where we left off" summary

### `scripts/validate_prerequisites.sh`
Validate prerequisites before starting sprint execution.

**What it checks:**
1. **Syncs GitHub issues** via `ailang messages import-github`
2. Working directory status (clean/uncommitted changes)
3. Current branch (dev or main)
4. Test suite passes
5. Linting passes
6. Shows unread messages (potential issues/feedback)

### `scripts/validate_sprint_json.sh <sprint_id>` **NEW**
**REQUIRED before starting any sprint.** Validates that sprint JSON has real milestones (not placeholders).

**What it checks:**
- No placeholder milestone IDs (`MILESTONE_ID`)
- No placeholder acceptance criteria (`Criterion 1/2`)
- At least 2 milestones defined
- All milestones have custom values (not defaults)
- Dependencies reference valid milestone IDs

**Exit codes:**
- `0` - Valid JSON, ready for execution
- `1` - Invalid JSON or placeholders detected (sprint-planner must fix)

### `scripts/milestone_checkpoint.sh <milestone_name>`
Run checkpoint after completing a milestone (tests, linting, git diff).
**Now includes JSON update reminder!** Shows current milestone statuses and prompts you to update the sprint JSON.

### `scripts/acceptance_test.sh <milestone_id> <test_type>` **NEW**
Run end-to-end acceptance tests (parser, builtin, examples, REPL, e2e).

### `scripts/finalize_sprint.sh <sprint_id> [version]` **NEW**
Finalize a completed sprint by moving design docs and updating status.

**What it does:**
- Moves design doc from `planned/` to `implemented/<version>/`
- Moves sprint plan markdown to `implemented/<version>/`
- Updates design doc status to "IMPLEMENTED"
- Updates sprint JSON status to "completed"
- Updates file paths in sprint JSON

**When to use:** After all milestones pass and sprint is complete.

**Example:**
```bash
.claude/skills/sprint-executor/scripts/finalize_sprint.sh M-BUG-RECORD-UPDATE-INFERENCE v0_4_9
```

## Execution Flow

### Phase 0: Session Resumption (for continuing sprints)

**If this is NOT the first session for this sprint:**

```bash
# ALWAYS run session_start.sh first!
.claude/skills/sprint-executor/scripts/session_start.sh <sprint-id>
```

This prints "Here's where we left off" summary. **Then skip to Phase 2** to continue with the next milestone.

### Phase 1: Initialize Sprint (first session only)

1. **Validate Sprint JSON** - Run `validate_sprint_json.sh <sprint-id>` **REQUIRED FIRST**
   - If validation fails, STOP and notify user that sprint-planner must fix the JSON
   - Do NOT proceed with placeholder milestones
2. **Read Sprint Plan** - Parse markdown + load JSON progress file (`.ailang/state/sprints/sprint_<id>.json`)
3. **Validate Prerequisites** - Run `validate_prerequisites.sh` (tests, linting, git status)
4. **Create Todo List** - Use TodoWrite to track all milestones
5. **Initial Status Update** - Mark sprint as "🔄 In Progress"
6. **Initial DX Review** - Consider tools/helpers that would make sprint easier (see [resources/dx_improvement_patterns.md](resources/dx_improvement_patterns.md))

### Phase 2: Execute Milestones

**For each milestone:**

1. **Pre-Implementation** - Mark milestone as `in_progress` in TodoWrite
2. **Implement** - Write code with DX awareness (helper functions, debug flags, better errors)
3. **Write Tests** - TDD recommended for complex logic, comprehensive coverage required
4. **Verify Quality** - Run `milestone_checkpoint.sh <milestone-name>` (tests + lint must pass)
5. **Update Documentation**:
   - CHANGELOG.md (what, LOC, key decisions)
   - Example files (REQUIRED for new features)
   - Sprint plan markdown (mark milestone as ✅)
6. **Update Sprint JSON** ⚠️ **CRITICAL** - The checkpoint script reminds you!
   - Update `passes: true/false` in `.ailang/state/sprints/sprint_<id>.json`
   - Set `completed: "<ISO timestamp>"`
   - Add `notes: "<summary of what was done>"`
7. **DX Reflection** - Identify and implement quick wins (<15 min), defer larger improvements
8. **Pause for Breath** - Show progress, ask user if ready to continue

**Quick tips:**
- Use parser test helpers from `internal/parser/test_helpers.go`
- Use `DEBUG_PARSER=1` for token flow tracing
- Use `make doc PKG=<package>` for API discovery
- See [resources/parser_patterns.md](resources/parser_patterns.md) for parser/pattern matching
- See [resources/codegen_patterns.md](resources/codegen_patterns.md) for Go code generation (builtins, expressions)
- See [resources/api_patterns.md](resources/api_patterns.md) for common API patterns
- See [resources/dx_improvement_patterns.md](resources/dx_improvement_patterns.md) for DX opportunities

### Phase 3: Finalize Sprint

1. **Final Testing** - Run `make test`, `make lint`, `make test-coverage-badge`
2. **Documentation Review** - Verify CHANGELOG.md, example files, sprint plan complete
3. **Final Commit** - Git commit with sprint summary (milestones, LOC, velocity)
4. **Move Design Docs** - Run `finalize_sprint.sh <sprint-id> [version]` to:
   - Move design docs from `planned/` to `implemented/<version>/`
   - Update design doc status to IMPLEMENTED
   - Update sprint JSON status to "completed"
   - Update file paths in sprint JSON
5. **Summary Report** - Compare planned vs actual (LOC, time, velocity)
6. **DX Impact Summary** - Document improvements made during sprint

## Key Features

### Continuous Testing
- Run `make test` after every file change
- Never proceed if tests fail
- Track test count increase

### Continuous Linting
- Run `make lint` after implementation
- Fix linting issues immediately
- Use `make fmt` for formatting

### Progress Tracking
- TodoWrite shows real-time progress
- Sprint plan updated at each milestone
- CHANGELOG.md grows incrementally
- **JSON file tracks structured state** (NEW)
- Git commits create audit trail

### GitHub Issue Integration (NEW)
**Uses `ailang messages` for GitHub sync and issue tracking!**

**Automatic sync:**
- `session_start.sh` and `validate_prerequisites.sh` run `ailang messages import-github` first
- Linked issues shown with titles from local message database

If `github_issues` is set in sprint JSON:
- `validate_sprint_json.sh` shows linked issues
- `session_start.sh` displays issue titles from messages
- `milestone_checkpoint.sh` reminds you to include `Refs #...` in commits
- `finalize_sprint.sh` suggests commit message with issue references

**Commit message format:**
```bash
# During development - use "refs" to LINK without closing
git commit -m "Complete M1: Parser foundation, refs #17"

# Final sprint commit - use "Fixes" to AUTO-CLOSE issues on merge
git commit -m "Finalize sprint M-BUG-FIX

Fixes #17
Fixes #42"
```

**Important: "refs" vs "Fixes"**
- `refs #17` - Links commit to issue (NO auto-close)
- `Fixes #17`, `Closes #17`, `Resolves #17` - AUTO-CLOSES issue when merged

**Workflow:**
1. Sprint JSON has `github_issues: [17, 42]` (set by sprint-planner, deduplicated)
2. During development: Use `refs #17` to link commits without closing
3. Final commit: Use `Fixes #17` to auto-close issues on merge
4. No duplicates: `ailang messages import-github` checks existing issues before importing

### Pause Points
- After each milestone completion
- When tests or linting fail (fix before continuing)
- When user requests "pause"
- When encountering unexpected issues

### Error Handling
- **If tests fail**: Show output, ask how to fix, don't proceed
- **If linting fails**: Show output, ask how to fix, don't proceed
- **If implementation unclear**: Ask for clarification, don't guess
- **If milestone takes much longer than estimated**: Pause and reassess

## Resources

### Multi-Session State
- **JSON Schema**: [`resources/json_progress_schema.md`](resources/json_progress_schema.md) - Sprint progress format
- **Session Startup**: Use `session_start.sh` ALWAYS for continuing sprints

### Development Tools
- **Parser & Patterns**: [`resources/parser_patterns.md`](resources/parser_patterns.md) - Parser development + pattern matching pipeline
- **Codegen Patterns**: [`resources/codegen_patterns.md`](resources/codegen_patterns.md) - Go code generation for new features/builtins
- **API Patterns**: [`resources/api_patterns.md`](resources/api_patterns.md) - Common constructor signatures and API gotchas
- **Developer Tools**: [`resources/developer_tools.md`](resources/developer_tools.md) - Make targets, ailang commands, workflows
- **DX Improvements**: [`resources/dx_improvement_patterns.md`](resources/dx_improvement_patterns.md) - Identifying and implementing DX wins
- **DX Quick Reference**: [`resources/dx_quick_reference.md`](resources/dx_quick_reference.md) - ROI calculator, decision matrix
- **Milestone Checklist**: [`resources/milestone_checklist.md`](resources/milestone_checklist.md) - Step-by-step per milestone

### External Documentation
- **Parser Guide**: [docs/guides/parser_development.md](../../docs/guides/parser_development.md)
- **Website**: https://ailang.sunholo.com/

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (YAML frontmatter + execution workflow) - ~250 lines
2. **Execute as needed**: Scripts in `scripts/` directory (validation, checkpoints, testing)
3. **Load on demand**: Resources in `resources/` directory (detailed guides, patterns, references)

## Prerequisites

- Working directory clean (or only sprint-related changes)
- Current branch `dev` (or specified in sprint plan)
- All existing tests pass
- All existing linting passes
- Sprint plan approved and documented
- **JSON progress file created AND POPULATED by sprint-planner** (not just template!)
- **JSON must pass validation**: `scripts/validate_sprint_json.sh <sprint-id>`

## Failure Recovery

### If Tests Fail During Sprint
1. Show test failure output
2. Ask user: "Tests failing. Options: (a) fix now, (b) revert change, (c) pause sprint"
3. Don't proceed until tests pass

### If Linting Fails During Sprint
1. Show linting output
2. Try auto-fix: `make fmt`
3. If still failing, ask user for guidance
4. Don't proceed until linting passes

### If Implementation Blocked
1. Show what's blocking progress
2. Ask user for guidance or clarification
3. Consider simplifying the approach
4. Document the blocker in sprint plan

### If Velocity Much Lower Than Expected
1. Pause and reassess after 2-3 milestones
2. Calculate actual velocity
3. Propose: (a) continue as-is, (b) reduce scope, (c) extend timeline
4. Update sprint plan with revised estimates

## Notes

- This skill is long-running - expect it to take hours or days
- Pause points are built in - you're not locked into finishing
- Sprint plan is the source of truth - but reality may require adjustments
- Git commits create a reversible audit trail
- TodoWrite provides real-time visibility into progress
- Test-driven development is non-negotiable - tests must pass
- **Multi-session continuity** - Sprint can span multiple Claude Code sessions (NEW)
- **JSON state tracking** - Structured progress in `.ailang/state/sprints/sprint_<id>.json` (NEW)
