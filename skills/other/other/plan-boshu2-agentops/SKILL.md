---
name: plan
description: 'Epic decomposition into trackable issues. Triggers: "create a plan", "plan implementation", "break down into tasks", "decompose into features", "create beads issues from research", "what issues should we create", "plan out the work".'
metadata:
  tier: execution
  dependencies:
    - research   # optional - checks for prior research
    - beads      # optional - creates issues via bd CLI (fallback: plain markdown plan)
    - pre-mortem # optional - suggested before crank
    - crank      # optional - suggested for execution
    - implement  # optional - suggested for single issue
---

# Plan Skill

> **Quick Ref:** Decompose goal into trackable issues with waves. Output: `.agents/plans/*.md` + bd issues.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

**CLI dependencies:** bd (issue creation). If bd is unavailable, write the plan to `.agents/plans/` as markdown with issue descriptions, and use TaskList for tracking instead. The plan document is always created regardless of bd availability.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--auto` | off | Skip human approval gate. Used by `/rpi --auto` for fully autonomous lifecycle. |

## Execution Steps

Given `/plan <goal> [--auto]`:

### Step 1: Setup
```bash
mkdir -p .agents/plans
```

### Step 2: Check for Prior Research

Look for existing research on this topic:
```bash
ls -la .agents/research/ 2>/dev/null | head -10
```

Use Grep to search `.agents/` for related content. If research exists, read it with the Read tool to understand the context before planning.

**Search knowledge flywheel for prior planning patterns:**
```bash
if command -v ao &>/dev/null; then
    ao search "<topic> plan decomposition patterns" 2>/dev/null | head -10
fi
```
If ao returns relevant learnings or patterns, incorporate them into the plan. Skip silently if ao is unavailable or returns no results.

### Step 3: Explore the Codebase (if needed)

**USE THE TASK TOOL** to dispatch an Explore agent. The explore prompt MUST request symbol-level detail:

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Understand codebase for: <goal>"
  prompt: |
    Explore the codebase to understand what's needed for: <goal>

    1. Find relevant files and modules
    2. Understand current architecture
    3. Identify what needs to change

    For EACH file that needs modification, return:
    - Exact function/method signatures that need changes
    - Struct/type definitions that need new fields
    - Key functions to reuse (with file:line references)
    - Existing test file locations and naming conventions (e.g., TestFoo_Bar)
    - Import paths and package relationships

    Return: file inventory, per-file symbol details, reuse points with line numbers, test patterns
```

#### Pre-Planning Baseline Audit (Mandatory)

**Before decomposing into issues**, run a quantitative baseline audit to ground the plan in verified numbers. This is mandatory for ALL plans — not just cleanup/refactor. Any plan that makes quantitative claims (counts, sizes, coverage) must verify them mechanically.

Run grep/wc/ls commands to count the current state of what you're changing:

- **Files to change:** count with `ls`/`find`/`wc -l`
- **Sections to add/remove:** count with `grep -l`/`grep -L`
- **Code to modify:** count LOC, packages, import references
- **Coverage gaps:** count missing items with `grep -L` or `find`

**Record the verification commands alongside their results.** These become pre-mortem evidence and acceptance criteria.

| Bad | Good |
|-----|------|
| "14 missing refs/" | "14 missing refs/ (verified: `ls -d skills/*/references/ \| wc -l` = 20 of 34)" |
| "clean up dead code" | "Delete 3,003 LOC across 3 packages (verified: `find src/old -name '*.go' \| xargs wc -l`)" |
| "update stale docs" | "Rewrite 4 specs (verified: `ls docs/specs/*.md \| wc -l` = 4)" |
| "add missing sections" | "Add Examples to 27 skills (verified: `grep -L '## Examples' skills/*/SKILL.md \| wc -l` = 27)" |

Ground truth with numbers prevents scope creep and makes completion verifiable. In ol-571, the audit found 5,752 LOC to remove — without it, the plan would have been vague. In ag-dnu, wrong counts (11 vs 14, 0 vs 7) caused a pre-mortem FAIL that a simple grep audit would have prevented.

### Step 3.5: Generate Implementation Detail (Mandatory)

**After exploring the codebase**, generate symbol-level implementation detail for EVERY file in the plan. This is what separates actionable specs from vague descriptions. A worker reading the plan should know exactly what to write without rediscovering function names, parameters, or code locations.

#### File Inventory Table

Start with a `## Files to Modify` table listing EVERY file the plan touches:

```markdown
## Files to Modify

| File | Change |
|------|--------|
| `src/auth/middleware.go` | Add rate limit check to `AuthMiddleware` |
| `src/config/config.go` | Add `RateLimit` section to `Config` struct |
| `src/auth/middleware_test.go` | **NEW** — rate limit middleware tests |
```

Mark new files with `**NEW**`. This table gives the implementer the full blast radius in 30 seconds.

#### Per-Section Implementation Specs

For each logical change group, provide symbol-level detail:

1. **Exact function signatures** — name the function, its parameters, and what changes:
   - "Add `worktreePath string` parameter to `classifyRunStatus`"
   - "Create new `RPIConfig` struct with `WorktreeMode string` field"

2. **Key functions to reuse** — with `file:line` references from the explore step:
   - "Reuse `readRunHeartbeat()` at `rpi_phased.go:1963`"
   - "Call existing `parsePhasedState()` at `rpi_phased.go:1924`"

3. **Inline code blocks** — for non-obvious constructs (struct definitions, CLI flags, config snippets):
   ```go
   type RPIConfig struct {
       WorktreeMode string `yaml:"worktree_mode" json:"worktree_mode"`
   }
   ```

4. **New struct fields with tags** — exact field names and JSON/YAML tags

5. **CLI flag definitions** — exact flag names, types, defaults, and help text

#### Named Test Functions

For each test file, list specific test functions with one-line descriptions:

```markdown
**`src/auth/middleware_test.go`** — add:
- `TestRateLimitMiddleware_UnderLimit`: Request within limit returns 200
- `TestRateLimitMiddleware_OverLimit`: Request exceeding limit returns 429
- `TestRateLimitMiddleware_ResetAfterWindow`: Counter resets after time window
```

#### Verification Procedures

Add a `## Verification` section with runnable bash sequences that reproduce the scenario and confirm the fix:

```markdown
## Verification

1. **Unit tests**: `go test ./src/auth/ -run "TestRateLimit" -v`
2. **Build check**: `go build ./...`
3. **Manual simulation**:
   ```bash
   # Start server
   go run ./cmd/server/ &
   # Hit endpoint 11 times (limit is 10)
   for i in $(seq 1 11); do curl -s -o /dev/null -w "%{http_code}\n" localhost:8080/api; done
   # Last request should return 429
   ```
```

**Why this matters:** The golden plan pattern (file tables + symbol-level specs + verification procedures) enabled single-pass implementation of an 8-file, 5-area change with zero ambiguity. Category-level specs ("modify classifyRunStatus") force implementers to rediscover symbols, causing divergence and rework.

### Step 4: Decompose into Issues

Analyze the goal and break it into discrete, implementable issues. For each issue define:
- **Title**: Clear action verb (e.g., "Add authentication middleware")
- **Description**: What needs to be done
- **Dependencies**: Which issues must complete first (if any)
- **Acceptance criteria**: How to verify it's done

#### Design Briefs for Rewrites

For any issue that says "rewrite", "redesign", or "create from scratch":
Include a **design brief** (3+ sentences) covering:
1. **Purpose** — what does this component do in the new architecture?
2. **Key artifacts** — what files/interfaces define success?
3. **Workflows** — what sequences must work?

Without a design brief, workers invent design decisions. In ol-571, a spec rewrite issue without a design brief produced output that diverged from the intended architecture.

#### Issue Granularity

- **1-2 independent files** → 1 issue
- **3+ independent files with no code deps** → split into sub-issues (one per file)
  - Example: "Rewrite 4 specs" → 4 sub-issues (4.1, 4.2, 4.3, 4.4)
  - Enables N parallel workers instead of 1 serial worker
- **Shared files between issues** → serialize or assign to same worker

#### Conformance Checks

For each issue's acceptance criteria, derive at least one **mechanically verifiable** conformance check using validation-contract.md types. These checks bridge the gap between spec intent and implementation verification.

| Acceptance Criteria | Conformance Check |
|-----|------|
| "File X exists" | `files_exist: ["X"]` |
| "Function Y is implemented" | `content_check: {file: "src/foo.go", pattern: "func Y"}` |
| "Tests pass" | `tests: "go test ./..."` |
| "Endpoint returns 200" | `command: "curl -s -o /dev/null -w '%{http_code}' localhost:8080/api \| grep 200"` |
| "Config has setting Z" | `content_check: {file: "config.yaml", pattern: "setting_z:"}` |

**Rules:**
- Every issue MUST have at least one conformance check
- Checks MUST use validation-contract.md types: `files_exist`, `content_check`, `command`, `tests`, `lint`
- Prefer `content_check` and `files_exist` (fast, deterministic) over `command` (slower, environment-dependent)
- If acceptance criteria cannot be mechanically verified, flag it as underspecified

### Step 5: Compute Waves

Group issues by dependencies for parallel execution:
- **Wave 1**: Issues with no dependencies (can run in parallel)
- **Wave 2**: Issues depending only on Wave 1
- **Wave 3**: Issues depending on Wave 2
- Continue until all issues assigned

#### Validate Dependency Necessity

For EACH declared dependency, verify:
1. Does the blocked issue modify a file that the blocker also modifies? → **Keep**
2. Does the blocked issue read output produced by the blocker? → **Keep**
3. Is the dependency only logical ordering (e.g., "specs before roles")? → **Remove**

False dependencies reduce parallelism. Pre-mortem judges will also flag these. In ol-571, unnecessary serialization between independent spec rewrites was caught by pre-mortem.

### Step 6: Write Plan Document

**Write to:** `.agents/plans/YYYY-MM-DD-<goal-slug>.md`

```markdown
# Plan: <Goal>

**Date:** YYYY-MM-DD
**Source:** <research doc if any>

## Context
<1-2 paragraphs explaining the problem, current state, and why this change is needed>

## Files to Modify

| File | Change |
|------|--------|
| `path/to/file.go` | Description of change |
| `path/to/new_file.go` | **NEW** — description |

## Boundaries

**Always:** <non-negotiable requirements — security, backward compat, testing, etc.>
**Ask First:** <decisions needing human input before proceeding — in auto mode, logged only>
**Never:** <explicit out-of-scope items preventing scope creep>

## Baseline Audit

| Metric | Command | Result |
|--------|---------|--------|
| <what was measured> | `<grep/wc/ls command used>` | <result> |

## Implementation

### 1. <Change Group Name>

In `path/to/file.go`:

- **Modify `functionName`**: Add `paramName Type` parameter. If `paramName != ""` and condition, return `"value"`.

- **Add `NewStruct`**:
  ```go
  type NewStruct struct {
      FieldName string `json:"field_name,omitempty"`
  }
  ```

- **Key functions to reuse:**
  - `existingHelper()` at `path/to/file.go:123`
  - `anotherFunc()` at `path/to/other.go:456`

### 2. <Next Change Group>

<Same pattern — exact symbols, inline code, reuse references>

## Tests

**`path/to/file_test.go`** — add:
- `TestFunctionName_ScenarioA`: Input X produces output Y
- `TestFunctionName_ScenarioB`: Edge case Z handled correctly

**`path/to/new_test.go`** — **NEW**:
- `TestNewFeature_HappyPath`: Normal flow succeeds
- `TestNewFeature_ErrorCase`: Bad input returns error

## Conformance Checks

| Issue | Check Type | Check |
|-------|-----------|-------|
| Issue 1 | content_check | `{file: "src/auth.go", pattern: "func Authenticate"}` |
| Issue 1 | tests | `go test ./src/auth/...` |
| Issue 2 | files_exist | `["docs/api-v2.md"]` |

## Verification

1. **Unit tests**: `go test ./path/to/ -run "TestFoo" -v`
2. **Full suite**: `go test ./... -short -timeout 120s`
3. **Manual simulation**:
   ```bash
   # Create test scenario
   mkdir -p .test/data
   echo '{"key": "value"}' > .test/data/input.json
   # Run the tool
   ./bin/tool --flag value
   # Verify expected output
   cat .test/data/output.json  # Should show "result"
   ```

## Issues

### Issue 1: <Title>
**Dependencies:** None
**Acceptance:** <how to verify>
**Description:** <what to do — reference Implementation section for symbol-level detail>

### Issue 2: <Title>
**Dependencies:** Issue 1
**Acceptance:** <how to verify>
**Description:** <what to do>

## Execution Order

**Wave 1** (parallel): Issue 1, Issue 3
**Wave 2** (after Wave 1): Issue 2, Issue 4
**Wave 3** (after Wave 2): Issue 5

## Next Steps
- Run `/pre-mortem` to validate plan
- Run `/crank` for autonomous execution
- Or `/implement <issue>` for single issue
```

### Step 7: Create Tasks for In-Session Tracking

**Use TaskCreate tool** for each issue:

```
Tool: TaskCreate
Parameters:
  subject: "<issue title>"
  description: |
    <Full description including:>
    - What to do
    - Acceptance criteria
    - Dependencies: [list task IDs that must complete first]
  activeForm: "<-ing verb form of the task>"
```

**After creating all tasks, set up dependencies:**

```
Tool: TaskUpdate
Parameters:
  taskId: "<task-id>"
  addBlockedBy: ["<dependency-task-id>"]
```

**IMPORTANT: Create persistent issues for ratchet tracking:**

If bd CLI available, create beads issues to enable progress tracking across sessions:
```bash
# Create epic first
bd create --title "<goal>" --type epic --label "planned"

# Create child issues (note the IDs returned)
bd create --title "<wave-1-task>" --body "<description>" --parent <epic-id> --label "planned"
# Returns: na-0001

bd create --title "<wave-2-task-depends-on-wave-1>" --body "<description>" --parent <epic-id> --label "planned"
# Returns: na-0002

# Add blocking dependencies to form waves
bd dep add na-0001 na-0002
# Now na-0002 is blocked by na-0001 → Wave 2
```

**Include conformance checks in issue bodies:**

When creating beads issues, embed the conformance checks from the plan as a fenced validation block in the issue description. This flows to worker validation metadata via /crank:

````
bd create --title "<task>" --body "Description...

\`\`\`validation
{\"files_exist\": [\"src/auth.go\"], \"content_check\": {\"file\": \"src/auth.go\", \"pattern\": \"func Authenticate\"}}
\`\`\`
" --parent <epic-id>
````

**Include cross-cutting constraints in epic description:**

"Always" boundaries from the plan should be added to the epic's description as a `## Cross-Cutting Constraints` section. /crank reads these from the epic (not per-issue) and injects them into every worker task's validation metadata.

**Waves are formed by `blocks` dependencies:**
- Issues with NO blockers → Wave 1 (appear in `bd ready` immediately)
- Issues blocked by Wave 1 → Wave 2 (appear when Wave 1 closes)
- Issues blocked by Wave 2 → Wave 3 (appear when Wave 2 closes)

**`bd ready` returns the current wave** - all unblocked issues that can run in parallel.

Without bd issues, the ratchet validator cannot track gate progress. This is required for `/crank` autonomous execution and `/post-mortem` validation.

### Step 8: Request Human Approval (Gate 2)

**Skip this step if `--auto` flag is set.** In auto mode, proceed directly to Step 9.

**USE AskUserQuestion tool:**

```
Tool: AskUserQuestion
Parameters:
  questions:
    - question: "Plan complete with N tasks in M waves. Approve to proceed?"
      header: "Gate 2"
      options:
        - label: "Approve"
          description: "Proceed to /pre-mortem or /crank"
        - label: "Revise"
          description: "Modify the plan before proceeding"
        - label: "Back to Research"
          description: "Need more research before planning"
      multiSelect: false
```

**Wait for approval before reporting completion.**

### Step 9: Record Ratchet Progress

```bash
ao ratchet record plan 2>/dev/null || true
```

### Step 10: Report to User

Tell the user:
1. Plan document location
2. Number of issues identified
3. Wave structure for parallel execution
4. Tasks created (in-session task IDs)
5. Next step: `/pre-mortem` for failure simulation, then `/crank` for execution

## Key Rules

- **Read research first** if it exists
- **Explore codebase** to understand current state
- **Identify dependencies** between issues
- **Compute waves** for parallel execution
- **Always write the plan** to `.agents/plans/`

## Examples

### Plan from Research

**User says:** `/plan "add user authentication"`

**What happens:**
1. Agent reads recent research from `.agents/research/2026-02-13-authentication-system.md`
2. Explores codebase to identify integration points
3. Decomposes into 5 issues: middleware, session store, token validation, tests, docs
4. Creates epic `ag-5k2` with 5 child issues in 2 waves
5. Output written to `.agents/plans/2026-02-13-add-user-authentication.md`

**Result:** Epic with dependency graph, conformance checks, and wave structure for parallel execution.

### Plan with Auto Mode

**User says:** `/plan --auto "refactor payment module"`

**What happens:**
1. Agent skips human approval gates
2. Searches knowledge base for refactoring patterns
3. Creates epic and child issues automatically
4. Records ratchet progress

**Result:** Fully autonomous plan creation with 3 waves, 8 issues, ready for `/crank`.

### Plan Cleanup Epic with Audit

**User says:** `/plan "remove dead code"`

**What happens:**
1. Agent runs quantitative audit: 3,003 LOC across 3 packages
2. Creates issues grounded in audit numbers (not vague "cleanup")
3. Each issue specifies exact files and line count reduction
4. Output includes deletion verification checks

**Result:** Scoped cleanup plan with measurable completion criteria (e.g., "Delete 1,500 LOC from pkg/legacy").

### Plan with Implementation Detail (Symbol-Level)

**User says:** `/plan "add stale run detection to ao rpi status"`

**What happens:**
1. Agent explores codebase, finds `classifyRunStatus` at `rpi_status.go:850`, `phasedState` at `rpi_phased.go:100`
2. Produces file inventory: 4 files to modify, 2 new files
3. Each implementation section names exact functions, parameters, struct fields with JSON tags
4. Tests section lists `TestClassifyRunStatus_StaleWorktree`, `TestDetermineRunLiveness_MissingWorktree` with descriptions
5. Verification section provides manual simulation: create fake stale run, check `ao rpi status` output

**Result:** Implementer can execute the plan in a single pass without rediscovering any symbol names, reducing implementation time by ~50% and eliminating spec-divergence rework.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| bd create fails | Beads not initialized in repo | Run `bd init --prefix <prefix>` first |
| Dependencies not created | Issues created without explicit `bd dep add` calls | Verify plan output includes dependency commands. Re-run to regenerate |
| Plan too large | Research scope was too broad, resulting in >20 issues | Narrow the goal or split into multiple epics |
| Wave structure incorrect | False dependencies declared (logical ordering, not file conflicts) | Review dependency necessity: does blocked issue modify blocker's files? |
| Conformance checks missing | Acceptance criteria not mechanically verifiable | Add `files_exist`, `content_check`, `tests`, or `command` checks per validation-contract.md |
| Epic has no children | Plan created but bd commands failed silently | Check `bd list --type epic` output; re-run plan with bd CLI available |
