---
name: plan
description: 'Epic decomposition into trackable issues. Triggers: "create a plan", "plan implementation", "break down into tasks", "decompose into features", "create beads issues from research", "what issues should we create", "plan out the work".'
---


# Plan Skill

> **Quick Ref:** Decompose goal into trackable issues with waves. Output: `.agents/plans/*.md` + bd issues.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**


## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--auto` | off | Skip human approval gate. Used by `$rpi --auto` for fully autonomous lifecycle. |
| `--fast-path` | off | Force Minimal detail template (see Step 3.2) |

## Execution Steps

Given `$plan <goal> [--auto]`:

### Step 0: Bead-Input Pre-Flight (Stale-Scope Gate)

When the input to `$plan` is a bead ID (`[a-z]{2,6}-[0-9a-z.]+`) and the plan is full-complexity, older than 7 days, or inherited from a prior session, run `ao beads verify <bead-id>` before setup or decomposition.

```bash
if [[ "$INPUT" =~ ^[a-z]{2,6}-[0-9a-z.]+$ ]]; then
    ao beads verify "$INPUT" || true
fi
```

If verification reports STALE citations, stop planning in interactive mode and ask for scope re-validation. In `--auto` mode, log the stale-scope evidence into the plan/execution packet and do not decompose against stale evidence until the scope is refreshed against HEAD.

This implements the shared stale-scope validation rule: inherited scope estimates must be re-validated against HEAD before acting on deferred beads, handoff docs, or prior-session plans.

### Step 1: Setup
```bash
mkdir -p .agents/plans
```

### Step 2: Check for Prior Research

Look for existing research on this topic:
```bash
ls -la .agents/research/ 2>/dev/null | head -10
```

Use Grep to search `.agents/` for related content. If research exists, read it to understand the context before planning.

**Search knowledge flywheel for prior planning patterns:**
```bash
if command -v ao &>/dev/null; then
    ao search "<topic> plan decomposition patterns" 2>/dev/null | head -10
    ao lookup --query "<goal>" --limit 5 2>/dev/null | head -30
fi
```
**Apply retrieved knowledge (mandatory when results returned):**

If ao returns relevant learnings or patterns, do NOT just load them as passive context. For each returned item:
1. Check: does this learning apply to the current planning goal? (answer yes/no)
2. If yes: incorporate as a planning constraint — does it warn about scope? suggest decomposition? flag a known pitfall?
3. Cite applicable learnings by filename when they influence a planning decision

After reviewing, record each citation with the correct type:
```bash
# Only use "applied" when the learning actually influenced your output.
# Use "retrieved" for items that were loaded but not referenced in your work.
ao metrics cite "<learning-path>" --type applied 2>/dev/null || true   # influenced a decision
ao metrics cite "<learning-path>" --type retrieved 2>/dev/null || true # loaded but not used
```

**Section evidence:** When lookup results include `section_heading`, `matched_snippet`, or `match_confidence` fields, prefer the matched section over the whole file — it pinpoints the relevant portion. Higher `match_confidence` (>0.7) means the section is a strong match; lower values (<0.4) are weaker signals. Use the `matched_snippet` as the primary context rather than reading the full file.

Skip silently if ao is unavailable or returns no results.

### Step 2.1: Load Compiled Prevention First (Mandatory)

Before decomposition, load compiled planning rules from `.agents/planning-rules/*.md` when they exist. This is the primary prevention surface for `$plan` in the compiler-enabled flow.

Use the tracked contracts in `docs/contracts/finding-compiler.md` and `docs/contracts/finding-registry.md`:

- prefer compiled planning rules first
- match by finding ID, `applicable_when` overlap, language overlap, and literal goal-text overlap
- when file inventory is known, rank by changed-file overlap before falling back to weaker textual matches
- cap the injected set at top 5 findings / rule files
- if compiled planning rules are missing, incomplete, or fewer than the matched finding set, fall back to `.agents/findings/registry.jsonl`
- fail open:
  - missing compiled directory or registry -> skip silently
  - empty compiled directory or registry -> skip silently
  - malformed line -> warn and ignore that line
  - unreadable file -> warn once and continue without findings

Use the selected planning rules / active findings as hard planning context before issue decomposition. Record the applied finding IDs and how they changed the plan. These become required context for the written plan, not optional side notes.

Every written plan must include an `Applied findings:` line, even when the value is `none`.

**Ranked packet contract:** Treat compiled planning rules, active findings, and matching high-severity `next-work.jsonl` items as one ranked packet, not three unrelated lookups. The packet must prefer the strongest overlap in this order:
1. literal goal-text overlap
2. `applicable_when` / issue-type overlap
3. language overlap
4. changed-file overlap (once the file table exists)
5. backlog severity / repo affinity for next-work items

### Step 2.2: Read and Validate Research Content

If research files exist, read the most recent one and verify it contains substantive findings before proceeding:

```bash
LATEST_RESEARCH=$(ls -t .agents/research/*.md 2>/dev/null | head -1)
if [ -n "$LATEST_RESEARCH" ]; then
    # Verify research has substantive content (not just frontmatter)
    if grep -qE '^## (Summary|Key Files|Findings|Key Findings|Architecture|Executive Summary|Recommendations|Part [0-9])' "$LATEST_RESEARCH"; then
        echo "Research validated: $LATEST_RESEARCH"
    else
        echo "WARNING: Research file exists but lacks standard sections (Summary, Key Files, Findings, Key Findings, Architecture, Executive Summary, or Recommendations)."
        echo "Consider running $research first for a thorough exploration."
    fi
fi
```

**Read the validated research file** before proceeding to Step 3. Do not plan based solely on file existence — understanding the research content is essential for accurate decomposition.

### Step 3: Explore the Codebase (if needed)


Spawn an exploration agent (via `spawn_agent` or `codex exec`):

```
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

- **File size limits:** check `wc -l` on files near size limits (especially SKILL.md files with the 800-line lint limit). If a planned change will push a file past the limit, split or refactor before implementation.
- **Test fixtures affected:** count test fixtures upstream of any filter/gate/hook being added or modified with `grep -rn 'func Test' <test-dir>/ | wc -l`. Changing a gate without updating its test fixtures causes false-green CI.

Ground truth with numbers prevents scope creep and makes completion verifiable. In ol-571, the audit found 5,752 LOC to remove — without it, the plan would have been vague. In ag-dnu, wrong counts (11 vs 14, 0 vs 7) caused a pre-mortem FAIL that a simple grep audit would have prevented.

### Step 3.2: Scale Detail by Complexity

Auto-select plan detail level based on issue count and goal complexity:

| Level | Criteria | Template | Description |
|-------|----------|----------|-------------|
| **Minimal** | 1-2 issues, fast complexity | Bullet points per issue | Title, 2-line description, acceptance criteria, files list |
| **Standard** | 3-6 issues, standard complexity | Current plan format | Full implementation specs, tests, verification |
| **Deep** | 7+ issues, full complexity, or `--deep` | Extended format | Symbol-level specs, data transformation tables, design briefs, cross-wave registry |

Read [references/detail-templates.md](references/detail-templates.md) for the template definitions.

**Override:** `--deep` forces Deep regardless of issue count. `--fast-path` forces Minimal.

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

3. **Inline code blocks** — for non-obvious constructs (struct definitions, CLI flags, config snippets). Verify all inline snippets compile with `go build ./...` before including them in issue descriptions — workers copy them verbatim:
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

#### Test Level Classification

For each test in the plan, classify its pyramid level per the test pyramid standard (`test-pyramid.md` in the standards skill):

| Test | Level | Rationale |
|------|-------|-----------|
| `TestRateLimitMiddleware_UnderLimit` | L1 (Unit) | Single function behavior in isolation |
| `TestRateLimitMiddleware_Integration` | L2 (Integration) | Middleware + config store interaction |
| `TestRateLimitMiddleware_E2E` | L3 (Component) | Full request pipeline with mocked Redis |

Include `test_levels` metadata in each issue's validation block:
```json
{
  "test_levels": {
    "required": ["L0", "L1"],
    "recommended": ["L2"],
    "rationale": "Reason for level selection"
  }
}
```

Agents own L0–L3 autonomously. L4+ requires human-defined scenarios — flag these as "human gate" items in the plan.

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

#### Data Transformation Mapping Tables (Mandatory for Filtering)

When a plan declares any struct-level filtering, exclusion, or allowlist logic:
- Create an explicit mapping table showing **source field → output transformation**
- Format: source name → fields affected → transformation (zeroed, renamed, computed)

Example from context orchestration (na-0v2):

| Section Name | Fields Zeroed |
|---|---|
| `HISTORY` | `Sessions` |
| `INTEL` | `Learnings`, `Patterns` |
| `TASK` | `BeadID`, `Predecessor` |

**Why:** Without explicit mapping tables, workers misinterpret data transformations. In na-0v2, section→field mapping ambiguity was caught only in pre-mortem. An explicit table prevents the concern entirely.

### Anti-Pattern Pre-Flight

Before finalizing issue decomposition, verify the plan avoids these confirmed failure modes:

| Anti-Pattern | Detection Question | Gate |
|---|---|---|
| **Brainstorm masquerading as plan** | Does every issue have mechanically verifiable acceptance criteria? | FAIL if any issue lacks `files_exist`, `content_check`, `tests`, or `command` conformance checks |
| **Dead infrastructure** | Does the plan provision anything without an activation test? | WARN if infrastructure is created without a corresponding smoke test issue |
| **Propagation surface blindness** | Has the full propagation surface been enumerated for renames/refactors? | FAIL if structural changes lack a propagation surface table |
| **40% context budget violation** | Will implementation sessions need to load >40% context window for knowledge? | WARN if injected knowledge exceeds estimated budget |
| **Commit-per-session anti-pattern** | Does the wave structure enforce commit-per-wave? | WARN if no explicit commit cadence in execution order |

### Step 4: Decompose into Issues

Analyze the goal and break it into discrete, implementable issues. For each issue define:
- **Title**: Clear action verb (e.g., "Add authentication middleware")
- **Description**: What needs to be done
- **Dependencies**: Which issues must complete first (if any)
- **Acceptance criteria**: How to verify it's done
- **Test levels**: Which pyramid levels (L0–L3) this issue's tests cover (see the test pyramid standard (`test-pyramid.md` in the standards skill))

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

#### Operationalization Heuristics

Each issue must be immediately executable by a swarm worker without further research:

- **File ownership (`metadata.files`):** List every file the issue touches. Workers use this for conflict detection.
- **Validation commands (`metadata.validation`):** Include runnable checks (e.g., `go test ./...`, `bash -n script.sh`). Workers run these before reporting done.
- **Homogeneous wave grouping:** Group issues by work type (all Go, all docs, all shell) within the same wave. Mixed-type waves cause toolchain context-switching and increase conflict risk.
- **Same-file serialization:** If two issues touch the same file, flag them for serialization (different waves) or merge into one issue. Never assign same-file issues to parallel workers.

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
- When adding entries to config files enumerated by tests, search for hardcoded count assertions: `grep -rn 'len.*!=\|len.*==\|expected.*count' <test-dir>/`

#### Schema Strictness Pre-Flight (WARN)

When any issue's file list includes JSON schema files (`*.schema.json`, files in `schemas/`), check for `additionalProperties: false`:

```bash
for f in <issue-files matching *.schema.json or schemas/*.json>; do
  if grep -q '"additionalProperties":\s*false' "$f" 2>/dev/null; then
    echo "WARN: $f has additionalProperties:false — new fields require schema update BEFORE consumer changes"
  fi
done
```

**If triggered:** Ensure schema-modifying issues are in an earlier wave than issues that reference the new fields. This prevents implementation failures where consumer SKILL.md files reference fields that the schema doesn't yet allow.

This is advisory (WARN, not FAIL). The wave decomposition in Step 5 must respect this ordering.

### Step 5: Compute Waves

Group issues by dependencies for parallel execution:
- **Wave 1**: Issues with no dependencies (can run in parallel)
- **Wave 2**: Issues depending only on Wave 1
- **Wave 3**: Issues depending on Wave 2
- Continue until all issues assigned

**Planning Rules Compliance (Mandatory Gate):** After computing waves, fill in the Planning Rules Compliance checklist. Read [references/planning-rules.md](references/planning-rules.md) for detection questions and evidence. Every rule MUST have an explicit justification or N/A rationale. Empty justification = INCOMPLETE plan.

```markdown
## Planning Rules Compliance

| Rule | Status | Justification |
|------|--------|---------------|
| PR-001: Mechanical Enforcement | PASS / N-A | [every integration point has a mechanical gate, OR why N/A] |
| PR-002: External Validation | PASS / N-A | [all validation gates are external, OR why N/A] |
| PR-003: Feedback Loops | PASS / N-A | [each output has a named consumer, OR why N/A] |
| PR-004: Separation Over Layering | PASS / N-A | [component boundaries are explicit contracts, OR why N/A] |
| PR-005: Process Gates First | PASS / N-A | [process gates verified before tool changes, OR why N/A] |
| PR-006: Cross-Layer Consistency | PASS / N-A | [all layers agree on shared parameters, OR why N/A] |
| PR-007: Phased Rollout | PASS / N-A | [changes phased by risk with validation between waves, OR why N/A] |

Unchecked rules: 0
```

If any rule row has an empty Justification column, mark the plan output as **INCOMPLETE** and do not proceed to Step 6 until all rows are filled.

#### File-Level Dependency Matrix (Mandatory)

Before assigning issues to waves, build a file-conflict matrix. For EACH issue, list which files it modifies. If any file appears in 2+ same-wave issues, either:
- **Serialize** them (move one to a later wave), or
- **Merge** them into a single issue assigned to one worker.

```markdown
## File-Conflict Matrix

| File | Issues |
|------|--------|
| `src/auth.go` | Issue 1, Issue 3 | ← CONFLICT: serialize or merge
| `src/config.go` | Issue 2 |
| `src/auth_test.go` | Issue 1 |
```

**Why:** Issue-level dependency graphs miss shared-file conflicts. In context-orchestration-leverage, two tracks both modified `rpi_phased_handoff.go` and required an unplanned Wave 2a/2b split. A file-conflict matrix would have caught this during planning.

#### Cross-Wave Shared File Registry (Mandatory)

After computing waves, build a **cross-wave file registry** listing every file that appears in issues across different waves. These files are collision risks because later-wave worktrees are created from a base SHA that may not include earlier-wave changes.

```markdown
## Cross-Wave Shared Files

| File | Wave 1 Issues | Wave 2+ Issues | Mitigation |
|------|---------------|----------------|------------|
| `src/auth_test.go` | Issue 1 | Issue 5 | Wave 2 worktree must branch from post-Wave-1 SHA |
| `src/config.go` | Issue 2 | Issue 6 | Serial: Issue 6 blocked by Issue 2 |
```

**If any file appears in multiple waves:**
1. Ensure the later-wave issue explicitly declares a dependency on the earlier-wave issue that touches the same file (so `bd dep add` / `addBlockedBy` is set).
2. Flag the file in the plan's `## Cross-Wave Shared Files` section so `$crank` can enforce worktree base refresh between waves.
3. For test files shared across waves, prefer splitting test additions into the same wave as the code they test — avoid a separate "test coverage" issue that touches files already modified in an earlier wave.

**Why:** In na-vs9, Wave 2 agents started from pre-Wave-1 SHA. A Wave 2 test coverage issue overwrote Wave 1's `.md→.json` fix in `rpi_phased_test.go` because the worktree didn't include Wave 1's commit. The cross-wave registry makes these collisions visible during planning.

#### Generated Artifact Companion Scope

When a planned issue changes skill behavior, phrasing, orchestration, or UX under `skills/<name>/`, the same issue must explicitly plan the Codex runtime companion scope:

- `skills-codex/<name>/` when the checked-in Codex artifact needs a body/script/reference change.
- `skills-codex-overrides/<name>/` or `skills-codex-overrides/catalog.json` when the Codex-specific tailoring or treatment changes.
- `skills-codex/.agentops-manifest.json` and `skills-codex/<name>/.agentops-generated.json` when artifact hashes need refresh.

Record these files in the `## File-Conflict Matrix` with the source skill issue, not in a later generic cleanup wave. The issue's validation block must include:

```bash
bash scripts/refresh-codex-artifacts.sh --scope worktree
bash scripts/validate-codex-generated-artifacts.sh --scope worktree
bash scripts/audit-codex-parity.sh --skill <name>
```

If the skill behavior change definitely has no Codex-facing effect, write that as the matrix mitigation with evidence. Do not leave Codex artifact scope implicit.

#### Validate Dependency Necessity

For EACH declared dependency, verify:
1. Does the blocked issue modify a file that the blocker also modifies? → **Keep**
2. Does the blocked issue read output produced by the blocker? → **Keep**
3. Is the dependency only logical ordering (e.g., "specs before roles")? → **Remove**

False dependencies reduce parallelism. Pre-mortem judges will also flag these. In ol-571, unnecessary serialization between independent spec rewrites was caught by pre-mortem.

### Step 6: Write Plan Document

**Write to:** `.agents/plans/YYYY-MM-DD-<goal-slug>.md`

```markdown
---
id: plan-YYYY-MM-DD-<goal-slug>
type: plan
date: YYYY-MM-DD
source: "[[.agents/research/YYYY-MM-DD-<research-slug>]]"
---

# Plan: <Goal>

## Context
<1-2 paragraphs explaining the problem, current state, and why this change is needed. Include `Applied findings: <id, id, ...>` from `.agents/planning-rules/*.md` first, with `.agents/findings/registry.jsonl` as fallback.>

Applied findings:
- `<finding-id>` — `<how it changed the plan>`

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

## Planning Rules Compliance

| Rule | Status | Justification |
|------|--------|---------------|
| PR-001: Mechanical Enforcement | PASS / N-A | [justification] |
| PR-002: External Validation | PASS / N-A | [justification] |
| PR-003: Feedback Loops | PASS / N-A | [justification] |
| PR-004: Separation Over Layering | PASS / N-A | [justification] |
| PR-005: Process Gates First | PASS / N-A | [justification] |
| PR-006: Cross-Layer Consistency | PASS / N-A | [justification] |
| PR-007: Phased Rollout | PASS / N-A | [justification] |

Unchecked rules: 0

## Post-Merge Cleanup

After bulk-merging wave results, audit for scaffold-era names:
- Rename placeholder function/variable names (e.g., `handleThing`, `processItem`) to domain-specific names
- Search with `grep -rn 'TODO\|FIXME\|HACK\|XXX' <modified-files>` for deferred cleanup markers
- If any `skills/` files were modified, run `scripts/regen-codex-hashes.sh` to sync codex parity and copy reference files.

## Next Steps
- Run `$pre-mortem` to validate plan
- Run `$crank` for autonomous execution
- Or `$implement <issue>` for single issue
```

### Step 7: Create Tasks for In-Session Tracking

Write task specs to `.agents/plan/tasks/` for in-session tracking:

```bash
mkdir -p .agents/plan/tasks

# For each task, write a spec file
cat > ".agents/plan/tasks/<task-slug>.md" << 'EOF'
# Task: <issue title>

**Status:** pending
**Blocked by:** [list dependency task slugs]
**Active form:** <-ing verb form of the task>

## Description
<Full description including:>
- What to do
- Acceptance criteria
- Dependencies
EOF
```

To mark dependencies, add `blocked_by` references in each task file. Update `**Status:**` to `in_progress` or `done` as work proceeds.

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

When creating beads issues, embed the conformance checks from the plan as a fenced validation block in the issue description. This flows to worker validation metadata via $crank:

````
bd create --title "<task>" --body "Description...

\`\`\`validation
{\"files_exist\": [\"src/auth.go\"], \"content_check\": {\"file\": \"src/auth.go\", \"pattern\": \"func Authenticate\"}}
\`\`\`
" --parent <epic-id>
````

**Include cross-cutting constraints in epic description:**

"Always" boundaries from the plan should be added to the epic's description as a `## Cross-Cutting Constraints` section. $crank reads these from the epic (not per-issue) and injects them into every worker task's validation metadata.

**Waves are formed by `blocks` dependencies:**
- Issues with NO blockers → Wave 1 (appear in `bd ready` immediately)
- Issues blocked by Wave 1 → Wave 2 (appear when Wave 1 closes)
- Issues blocked by Wave 2 → Wave 3 (appear when Wave 2 closes)

**`bd ready` returns the current wave** - all unblocked issues that can run in parallel.

Beads-backed issues are the preferred path because they give `$crank` richer dependency data and make ratchet progress easier to inspect. When bd is unavailable or degraded, keep the plan file + execution packet path accurate and continue in file-backed mode for `$crank` and `$validation`.

### Step 7b: Verify Validation Blocks (Post-Creation Check)

After creating all beads issues, verify that every issue body contains a fenced validation block. Missing validation blocks break the plan-to-crank pipeline — `$crank` cannot extract conformance checks from issues that lack them.

```bash
if command -v bd &>/dev/null && [[ -n "$EPIC_ID" ]]; then
    MISSING_VALIDATION=()
    for ISSUE_ID in $ALL_CREATED_ISSUES; do
        if ! bd show "$ISSUE_ID" 2>/dev/null | grep -q '```validation'; then
            MISSING_VALIDATION+=("$ISSUE_ID")
        fi
    done
    if [[ ${#MISSING_VALIDATION[@]} -gt 0 ]]; then
        echo "WARNING: ${#MISSING_VALIDATION[@]} issue(s) missing validation blocks: ${MISSING_VALIDATION[*]}"
        echo "  $crank will fall back to default files_exist checks for these issues."
        echo "  Consider adding ```validation``` blocks with conformance checks."
    else
        echo "All ${#ALL_CREATED_ISSUES[@]} issues have validation blocks."
    fi
fi
```

This is a warning gate, not a blocker — plans can proceed without validation blocks, but crank execution will use weaker fallback checks.

### Step 8: Request Human Approval (Gate 2)

**Skip this step if `--auto` flag is set.** In auto mode, proceed directly to Step 9.

Ask the user directly:

> Plan complete with N tasks in M waves. Approve to proceed?
>
> Options:
> 1. **Approve** — Proceed to `$pre-mortem` or `$crank`
> 2. **Revise** — Modify the plan before proceeding
> 3. **Back to Research** — Need more research before planning

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
4. Tasks created (beads issue IDs or file-backed task refs)
5. Next step: `$pre-mortem` for failure simulation, then `$crank` for execution

## Key Rules

- **Read research first** if it exists
- **Explore codebase** to understand current state
- **Identify dependencies** between issues
- **Compute waves** for parallel execution
- **Always write the plan** to `.agents/plans/`

## Examples

**`$plan "add user authentication"`** — Reads research, decomposes into 5 issues (middleware, session store, token validation, tests, docs), creates epic with 2 waves, writes plan to `.agents/plans/`.

**`$plan --auto "refactor payment module"`** — Skips approval gates, creates 3-wave/8-issue epic autonomously, ready for `$crank`.

**`$plan "remove dead code"`** — Runs quantitative audit (3,003 LOC), creates issues with exact file/LOC targets, includes deletion verification checks.

**`$plan "add stale run detection to RPI status"`** — Symbol-level detail: names exact functions, struct fields, JSON tags, test names. Implementer executes in a single pass.

See [references/examples.md](references/examples.md) for full walkthroughs.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| bd create fails | Run `bd init --prefix <prefix>` first |
| Plan too large (>20 issues) | Narrow goal or split into multiple epics |
| Wave structure incorrect | Review dependencies: does blocked issue modify blocker's files? |
| Conformance checks missing | Add `files_exist`, `content_check`, `tests`, or `command` checks |

See [references/examples.md](references/examples.md) for more troubleshooting scenarios.

## Reference Documents

- [references/planning-rules.md](references/planning-rules.md) — seven compiled planning rules (mechanical enforcement, external validation, feedback loops, separation, process gates, cross-layer consistency, phased rollout).
- [references/plan-mutations.md](references/plan-mutations.md)
- [references/complexity-estimation.md](references/complexity-estimation.md)
- [references/detail-templates.md](references/detail-templates.md)
- [references/examples.md](references/examples.md)
- [references/sdd-patterns.md](references/sdd-patterns.md)
- [references/templates.md](references/templates.md)

## Local Resources

### references/

- [references/planning-rules.md](references/planning-rules.md)
- [references/complexity-estimation.md](references/complexity-estimation.md)
- [references/detail-templates.md](references/detail-templates.md)
- [references/examples.md](references/examples.md)
- [references/sdd-patterns.md](references/sdd-patterns.md)
- [references/templates.md](references/templates.md)

### scripts/

- `scripts/validate.sh`
