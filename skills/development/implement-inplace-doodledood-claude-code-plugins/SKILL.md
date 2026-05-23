---
name: implement-inplace
description: 'Single-agent implementation: executes plans in-place without subagents. Use /implement (default) for complex features; use this for simpler tasks or when subagent overhead is unwanted.'
---

**User request**: $ARGUMENTS

Autonomously execute implementation in-place. Supports plan files, inline tasks, or interactive mode.

**Fully autonomous**: No pauses except as specified in Phase 3's "Pause ONLY when" list and Edge Cases.

## Workflow

### Phase 1: Resolve Input & Setup

**Review flag**: Review workflow runs by default after implementation. If arguments contain `--no-review` (case-insensitive), disable it. Remove flag from arguments before processing below.

**Priority order:**
1. **File path** (ends in `.md` or starts with `/`) → use plan file, optionally with `--spec <path>`
2. **Inline task** (any other text) → create ad-hoc single chunk:
   ```
   ## 1. [Task summary - first 50 chars (if longer, truncate at last space before char 50 if that space is at position 10+; otherwise truncate at char 47 and append "..."; if 50 chars or fewer, use as-is)]
   - Depends on: -
   - Tasks: [user's description]
   - Files: (list as created/modified during execution)
   - Acceptance criteria: task completed AND gates pass
   ```
3. **Empty** → search `/tmp/plan-*.md` (most recent by file modification time; if tied, use alphabetically last filename); if none found, **ask user** what they want to implement

**For plan files**, parse each chunk (`## N. [Name]` headers):
- Dependencies (`Depends on:` field, `-` = none)
- Files to modify/create with descriptions
- Context files (paths, optional line ranges)
- Implementation tasks (bullet list)
- Key functions/types

**Invalid plan**: Empty file, missing `## N. [Name]` chunk headers, or malformed Depends on/Tasks fields (Depends on must be `-` or comma-separated chunk numbers; Tasks must be a bullet list with at least one item) → Error with path + expected structure.

**Build dependency graph**: No-dependency chunks first, then topological order.

**Create flat todo list** (granular progress, resumable):
```
[ ] Read context for [Chunk]
[ ] [Task 1]...[ ] [Task N]
[ ] Run gates for [Chunk]
[ ] Commit chunk: [Chunk]
...
# Unless --no-review, append:
[ ] Run review on implemented changes
[ ] (Expand: fix review issues as findings emerge)
```
All todos created at once via TodoWrite (status `pending`). If TodoWrite unavailable, use `/tmp/implement-progress.md` with markdown checkboxes: `- [ ] pending`, `- [~] in progress`, `- [x] completed`, with timestamp prefix `[HH:MM:SS]`.

**Spec file** (`--spec <path>`): Read before implementation for requirements/acceptance criteria. If path doesn't exist, add to Notes: "Warning: Spec not found: [path]" and continue. Spec is only used when explicitly provided via --spec.

### Phase 2: Execute Chunks

**CRITICAL**: Execute continuously without pauses.

Per chunk:
1. Read context files from plan + files-to-modify, respect line ranges
2. Implement each task, marking `in_progress`→`completed` immediately
3. Run gates (Phase 3)
4. Commit chunk: `git add [files created/modified] && git commit -m "feat(plan): implement chunk N - [Name]"` (do NOT push)
5. Track created/modified files for summary

### Phase 3: Auto-Fix Gates

**Run gates in order**: typecheck, then tests, then lint. Stop at first failure and iterate on that gate until it passes before proceeding to the next gate.

**Gate command detection**:
1. Check CLAUDE.md for explicit commands (look for sections labeled "Development Commands", "Scripts", or "Gates"; identify typecheck/test/lint by command names like `tsc`, `jest`, `eslint`, `mypy`, `pytest`, `ruff`)
2. If CLAUDE.md commands fail with "command not found", "not recognized", or exit code 127 → fall back to config detection
3. Use fallback detection (see Gate Detection section)

**On failure—iterate**:
1. Analyze: parse errors, identify files/lines, understand root cause
2. Fix by addressing root cause (not by suppressing errors, skipping tests, or adding `// @ts-ignore`)
3. Re-run the failing gate
4. Track attempts per issue by error message and file:line; if same error persists after 3 distinct fix strategies, escalate per "Pause ONLY when" rules

**Distinct fix strategy**: A strategy is distinct if it modifies different lines OR uses a categorically different technique: (1) adding/changing type annotations, (2) type assertions/casts, (3) refactoring logic/control flow, (4) adding null/undefined checks, (5) changing function signatures, (6) adding/modifying imports.

**Pause ONLY when**:
- Same error message and file:line persists after 3 distinct fix strategies
- Need info not available in codebase or context (API keys, credentials, external service configs)
- Fix requires modifying files not listed in the chunk's "Files:" field (creating new files is allowed only if they are: helper/utility modules, type definition files, or test files directly testing the chunk's code)
- Plan requirements contradict each other (both can't be satisfied simultaneously)

Report: what tried, why failed, what's needed.

### Phase 4: Completion

```
## Implementation Complete
Chunks: N | Todos: M | Created: [list] | Modified: [list]
### Notes: [warnings/assumptions/follow-ups]
Run `/review` for quality verification.
```

Unless `--no-review` → proceed to Phase 5.

### Phase 5: Review Workflow (default, skip with --no-review)

Skip if `--no-review` was set.

1. Mark "Run review" `in_progress` → invoke `Skill("vibe-workflow:review", "--autonomous")` → mark `completed`
2. If no issues → mark fix placeholder `completed`, done
3. Expand fix placeholder:
   ```
   [x] (Expand: fix review issues as findings emerge)
   [ ] Fix critical/high severity issues
   [ ] Re-run review to verify fixes
   [ ] (Expand: additional fix iterations if needed)
   ```
4. Mark "Fix critical/high" `in_progress` → invoke `Skill("vibe-workflow:fix-review-issues", "--severity critical,high --autonomous")` → mark `completed`
5. Mark "Re-run review" `in_progress` → invoke `Skill("vibe-workflow:review", "--autonomous")` → mark `completed`
6. Repeat fix/review cycle until clean or max 3 cycles

## Edge Cases

| Case | Action |
|------|--------|
| Invalid plan (empty file, missing `## N. [Name]` headers, or malformed fields) | Error with path + expected structure |
| Missing context file | Add to Notes: "Warning: Context file not found: [path]", continue |
| Chunk fails (gates fail after 3 distinct fix strategies OR task requires unavailable info) | Leave todos pending, skip dependents, continue independents, report in summary |
| Partial gate success (e.g., typecheck passes but tests fail after 3 strategies) | Chunk fails; require all gates to pass for chunk completion |
| Inline task provided | Create ad-hoc single chunk, proceed normally |
| No input + no recent plan | Ask user what they want to implement |
| Interrupted | Todos reflect exact progress; on next invocation with same plan, agent resumes from first pending todo. If files were partially modified without git: read current state and complete remaining work rather than overwriting |
| CLAUDE.md gate commands fail | Fall back to config-based detection (see Gate Detection) |
| No CLAUDE.md or no matching sections | Skip to config-based detection |
| Circular dependencies | Error: "Circular dependency detected: [chunk A] ↔ [chunk B]". List cycle, abort. |
| TodoWrite unavailable | Track progress via `/tmp/implement-progress.md` with checkbox format |
| Spec file doesn't exist | Add to Notes: "Warning: Spec not found: [path]", continue without spec |

## Principles

- **Autonomous**: No prompts/pauses/approval needed except blocking issues listed in Phase 3 and Edge Cases
- **Granular todos**: One todo per action, visible progress, resumable
- **Persistent auto-fix**: Iterate until gates pass (up to 3 distinct strategies per issue), escalate only when stuck
- **Dependency order**: Execute in order, skip failed chunk's dependents
- **Gates non-negotiable**: Fix root cause (no `@ts-ignore`, test skips, or suppressions); skip chunk only after 3 failed strategies
- **Simplicity**: Prefer readable code over micro-optimizations; don't add complexity for marginal performance gains
- **Commit per chunk**: Each successful chunk gets its own commit (no push until end); provides rollback points for recovery

## Gate Detection

**Priority**: CLAUDE.md → package.json scripts → Makefile → config detection

Skip any source that doesn't define relevant commands (test/lint/typecheck).

**Fallback** (if CLAUDE.md doesn't specify or commands fail with exit code 127):
- TS/JS: `tsconfig.json`→`tsc --noEmit`, `eslint.config.*`→`eslint .`, `jest/vitest.config.*`→`npm test`
- Python: `pyproject.toml`→`mypy`/`ruff check`, pytest config→`pytest`
- Go: `go.mod`→`go build ./...`, `golangci.yml`→`golangci-lint run`
- Rust: `Cargo.toml`→`cargo check`, `cargo test`
- Other languages: Skip gates with warning "No gate commands detected for [language]; specify in CLAUDE.md"
