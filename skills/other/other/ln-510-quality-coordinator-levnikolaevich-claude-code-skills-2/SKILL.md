---
name: ln-510-quality-coordinator
description: "Coordinates code quality checks: metrics, cleanup, agent review, regression, log analysis. Use when Story needs quality_verdict with aggregated results."
allowed-tools: Read, Grep, Glob, Bash, Skill, mcp__hex-graph__index_project, mcp__hex-graph__analyze_changes
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

**Type:** L2 Coordinator
**Category:** 5XX Quality

# Quality Coordinator

Runtime-backed quality coordinator. The runtime owns phase transitions, worker summary tracking, and deterministic resume while ln-510 still performs the same quality orchestration.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | Yes | args, git branch, kanban, user | Story to process |

**Resolution:** Story Resolution Chain.
**Status filter:** To Review

## Purpose & Scope
- Invoke ln-511-code-quality-checker (metrics, MCP Ref, static analysis)
- Invoke ln-512-tech-debt-cleaner (auto-fix safe findings from ln-511)
- Run inline agent review (Codex + Gemini in parallel on cleaned code)
- Run Criteria Validation (Story dependencies, AC-Task Coverage, DB Creation Principle)
- Run linters from tech_stack.md
- Invoke ln-513-regression-checker (test suite after all changes)
- Invoke ln-514-test-log-analyzer (classify errors, assess log quality)
- Return quality_verdict + aggregated results
- Calculate quality_verdict per normalization matrix + `references/gate_levels.md`

## Runtime Contract

**MANDATORY READ:** Load `shared/references/coordinator_runtime_contract.md`, `shared/references/quality_runtime_contract.md`, `shared/references/quality_summary_contract.md`, `shared/references/quality_worker_runtime_contract.md`, `shared/references/review_runtime_contract.md`

Runtime family: `quality-runtime`

Identifier:
- Story ID

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_CODE_QUALITY`
4. `PHASE_3_CLEANUP`
5. `PHASE_4_AGENT_REVIEW`
6. `PHASE_5_CRITERIA`
7. `PHASE_6_LINTERS`
8. `PHASE_7_REGRESSION`
9. `PHASE_8_LOG_ANALYSIS`
10. `PHASE_9_FINALIZE`
11. `PHASE_10_SELF_CHECK`

Worker summary contract:
- `ln-511`, `ln-512`, `ln-513`, `ln-514` receive deterministic child `runId` plus exact `summaryArtifactPath`
- checkpoint child runtime metadata before waiting for the artifact
- each worker writes a `quality-worker` summary envelope before terminal outcome
- ln-510 consumes worker summaries, not free-text worker prose

## When to Use
- All implementation tasks in Story status = Done

## Workflow

### Phase 0: Resolve Inputs

**MANDATORY READ:** Load `shared/references/input_resolution_pattern.md`

1. **Resolve storyId:** Run Story Resolution Chain per guide (status filter: [To Review]).

### Phase 1: Discovery

1) Auto-discover team/config from `docs/tasks/kanban_board.md`
2) Load Story + task metadata from Linear (no full descriptions)
3) **Collect git scope** (sets `changed_files[]` for ln-511 via coordinator context):
   **MANDATORY READ:** Load `shared/references/git_scope_detection.md`
   Run algorithm from guide → build `changed_files[]`
4) **Index codebase graph (if available):** IF `hex-graph` MCP server is available:
   - `index_project(path=codebase_root)` — builds/refreshes code graph for workers
   - Add `graph_indexed: true` to coordinator context for ln-511
   - Workers use graph tools (`audit_workspace`, `analyze_architecture`, `find_references`, `trace_paths`) when graph_indexed=true
   - If indexing fails or graph path is unavailable, record `graph_indexed: false` and continue without graph-backed evidence

**Fast-track mode:** When invoked with `--fast-track` flag (readiness 10/10), run Phase 2 with `--skip-mcp-ref` (metrics + static only, no MCP Ref), skip Phase 3 (ln-512), run Phase 4 with **1 agent minimum** (reduced from 2). Run Phase 5 (criteria), Phase 6 (linters), Phase 7 (ln-513), Phase 8 (ln-514).

### Phase 2: Code Quality (delegate to ln-511 — ALWAYS runs)

> **MANDATORY STEP:** ln-511 invocation required in ALL modes.
> **Full gate:** ln-511 runs everything (metrics + MCP Ref + static analysis).
> **Fast-track:** ln-511 runs with `--skip-mcp-ref` (metrics + static analysis only — catches complexity, DRY, dead code without expensive MCP Ref calls).

1) **Invoke ln-511-code-quality-checker** via Skill tool
   - Compute `childRunId = {parent_run_id}--ln-511--{storyId}`
   - Compute artifact path `.hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-511--{storyId}.json`
   - Materialize manifest `.hex-skills/quality/ln-511--{storyId}_manifest.json`
   - Start `quality-worker-runtime` and checkpoint `child_run` metadata before delegation
   - Full: ln-511 runs code metrics, MCP Ref validation (OPT/BP/PERF), static analysis
   - Fast-track: ln-511 runs code metrics + static analysis only (skips OPT-, BP-, PERF- MCP Ref checks)
   - Read only the resulting `quality-worker` artifact
2) **If ln-511 returns ISSUES_FOUND** -> aggregate issues, continue (ln-500 decides action)

**Invocation:**
```
# Full gate:
node shared/scripts/quality-worker-runtime/cli.mjs start --skill ln-511 --story {storyId} --manifest-file .hex-skills/quality/ln-511--{storyId}_manifest.json --run-id {parent_run_id}--ln-511--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-511--{storyId}.json
node shared/scripts/quality-runtime/cli.mjs checkpoint --story {storyId} --phase PHASE_2_CODE_QUALITY --payload '{"child_run":{"worker":"ln-511","run_id":"{parent_run_id}--ln-511--{storyId}","summary_artifact_path":".hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-511--{storyId}.json"}}'
Skill(skill: "ln-511-code-quality-checker", args: "{storyId} --run-id {parent_run_id}--ln-511--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-511--{storyId}.json")
# Fast-track:
node shared/scripts/quality-worker-runtime/cli.mjs start --skill ln-511 --story {storyId} --manifest-file .hex-skills/quality/ln-511--{storyId}_manifest.json --run-id {parent_run_id}--ln-511--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-511--{storyId}.json
node shared/scripts/quality-runtime/cli.mjs checkpoint --story {storyId} --phase PHASE_2_CODE_QUALITY --payload '{"child_run":{"worker":"ln-511","run_id":"{parent_run_id}--ln-511--{storyId}","summary_artifact_path":".hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-511--{storyId}.json"}}'
Skill(skill: "ln-511-code-quality-checker", args: "{storyId} --skip-mcp-ref --run-id {parent_run_id}--ln-511--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-511--{storyId}.json")
```

### Phase 3: Tech Debt Cleanup (delegate to ln-512 — SKIP if --fast-track)

> **MANDATORY STEP (full gate):** ln-512 invocation required. Safe auto-fixes only (confidence >=90%).
> **Fast-track:** SKIP this phase.

1) **Invoke ln-512-tech-debt-cleaner** via Skill tool
   - Compute deterministic child run inputs for `ln-512`
   - Start `quality-worker-runtime` and checkpoint `child_run` before delegation
   - ln-512 consumes findings from ln-511 output (passed via coordinator context)
   - Filters to auto-fixable categories (unused imports, dead code, deprecated aliases)
   - Applies safe fixes, verifies build integrity, creates commit
   - Read only the resulting `quality-worker` artifact
2) **If ln-512 returns BUILD_FAILED** -> all changes reverted, aggregate issue, continue

**Invocation:**
```
node shared/scripts/quality-worker-runtime/cli.mjs start --skill ln-512 --story {storyId} --manifest-file .hex-skills/quality/ln-512--{storyId}_manifest.json --run-id {parent_run_id}--ln-512--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-512--{storyId}.json
node shared/scripts/quality-runtime/cli.mjs checkpoint --story {storyId} --phase PHASE_3_TECH_DEBT_CLEANUP --payload '{"child_run":{"worker":"ln-512","run_id":"{parent_run_id}--ln-512--{storyId}","summary_artifact_path":".hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-512--{storyId}.json"}}'
Skill(skill: "ln-512-tech-debt-cleaner", args: "{storyId} --run-id {parent_run_id}--ln-512--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-512--{storyId}.json")
```

### Phase 4: Agent Review Launch

> **MANDATORY STEP:** Launches agents in background, results merged in Phase 9.
> **Fast-track:** Launch 1 agent only (most available). Results merged in Phase 9 as normal.

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md`, `shared/references/agent_delegation_pattern.md`
**MANDATORY READ:** Load `shared/references/review_runtime_contract.md`

4a) Start review runtime for `ln-510` with:
    - `mode=code`
    - `identifier={storyId}`
    - `expected_agents = ["codex", "gemini"]` or single available agent in fast-track
4b) Run health check:
    - Read `.hex-skills/environment_state.json` → exclude disabled
    - Run `node shared/agents/agent_runner.mjs --health-check --json`
    - If 0 agents → checkpoint runtime with `agents_skipped_reason`, go to Phase 5
4c) Get references: `get_issue(storyId)` + `list_issues(parent=storyId, status=Done)` (exclude test tasks)
4d) Build per-agent prompt from `review_base.md` + `modes/code.md`
4e) Launch available agents with metadata files:
    `node shared/agents/agent_runner.mjs --agent {name} --prompt-file .hex-skills/agent-review/{agent}/{id}_codereview_prompt.md --output-file .hex-skills/agent-review/{agent}/{id}_codereview_result.md --metadata-file .hex-skills/agent-review/{agent}/{id}_codereview_metadata.json --cwd {project_dir}`
4f) Register each launched agent in review runtime with prompt/result/log/metadata paths
4g) Checkpoint runtime Phase 2-equivalent state, then continue to Phase 5-8 while agents work

### Phase 5: Criteria Validation

**MANDATORY READ:** Load `references/criteria_validation.md`

| Check | Description | Fail Action |
|-------|-------------|-------------|
| #1 Story Dependencies | No forward deps within Epic | [DEP-] issue |
| #2 AC-Task Coverage | STRONG/WEAK/MISSING scoring | [COV-]/[BUG-] issue |
| #3 DB Creation Principle | Schema scope matches Story | [DB-] issue |

### Phase 6: Linters
**MANDATORY READ:** `shared/references/ci_tool_detection.md` (Discovery Hierarchy + Command Registry)

1) Detect lint/typecheck commands per ci_tool_detection.md discovery hierarchy
2) Run all detected checks (timeouts per guide: 2min linters, 5min typecheck)
3) **If any check fails** -> aggregate issues, continue

### Phase 7: Regression Tests (delegate to ln-513)

1) **Invoke ln-513-regression-checker** via Skill tool
   - Compute deterministic child run inputs for `ln-513`
   - Start `quality-worker-runtime` and checkpoint `child_run` before delegation
   - Runs full test suite, reports PASS/FAIL
   - Runs AFTER ln-512 changes to verify nothing broke
   - Read only the resulting `quality-worker` artifact
2) **If regression FAIL** -> aggregate issues, continue

**Invocation:**
```
node shared/scripts/quality-worker-runtime/cli.mjs start --skill ln-513 --story {storyId} --manifest-file .hex-skills/quality/ln-513--{storyId}_manifest.json --run-id {parent_run_id}--ln-513--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-513--{storyId}.json
node shared/scripts/quality-runtime/cli.mjs checkpoint --story {storyId} --phase PHASE_7_REGRESSION_TESTS --payload '{"child_run":{"worker":"ln-513","run_id":"{parent_run_id}--ln-513--{storyId}","summary_artifact_path":".hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-513--{storyId}.json"}}'
Skill(skill: "ln-513-regression-checker", args: "{storyId} --run-id {parent_run_id}--ln-513--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-513--{storyId}.json")
```

### Phase 8: Test Log Analysis (delegate to ln-514 — runs after ln-513)

1) **Invoke ln-514-test-log-analyzer** via Skill tool with context instructions
   - Compute deterministic child run inputs for `ln-514`
   - Start `quality-worker-runtime` and checkpoint `child_run` before delegation
   - Only Real Bugs affect quality verdict; log quality issues are informational
   - Read only the resulting `quality-worker` artifact
2) **If ln-514 returns REAL_BUGS_FOUND** -> aggregate issues, continue
3) **If ln-514 returns NO_LOG_SOURCES** -> status ignored, continue
4) Post ln-514 report as Linear comment on story

**Invocation:**
```
node shared/scripts/quality-worker-runtime/cli.mjs start --skill ln-514 --story {storyId} --manifest-file .hex-skills/quality/ln-514--{storyId}_manifest.json --run-id {parent_run_id}--ln-514--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-514--{storyId}.json
node shared/scripts/quality-runtime/cli.mjs checkpoint --story {storyId} --phase PHASE_8_LOG_ANALYSIS --payload '{"child_run":{"worker":"ln-514","run_id":"{parent_run_id}--ln-514--{storyId}","summary_artifact_path":".hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-514--{storyId}.json"}}'
Skill(skill: "ln-514-test-log-analyzer", args: "{storyId} --run-id {parent_run_id}--ln-514--{storyId} --summary-artifact-path .hex-skills/runtime-artifacts/runs/{parent_run_id}/quality-worker/ln-514--{storyId}.json --log-context \"review logs since test run start, expected errors from negative test cases\"")
```

### Phase 9: Agent Merge (runs after Phase 8, when agent results arrive — SKIP if agents SKIPPED)

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md` (Critical Verification + Iterative Refinement), `shared/references/agent_review_memory.md`

9a) Sync agent state via review runtime. Do not merge until every required agent is `result_ready | dead | failed | skipped`
9b) **Critical Verification** per shared workflow — Claude evaluates each suggestion on merits
9c) **Merge accepted suggestions** into issues list (SEC-, PERF-, MNT-, ARCH-, BP-, OPT-)
    - If `area=security` or `area=correctness` → escalate aggregate to CONCERNS
9c.1) **Semantic diff snapshot (if graph indexed):**
    - Run `analyze_changes(path=codebase_root, base_ref="HEAD~1")` to capture changed symbols, deleted API warnings, and high-risk items for the current review branch state
    - Merge semantic diff findings into the same issue list before final verdict calculation
9d) **Save review summary** to `.hex-skills/agent-review/review_history.md`
9e) Checkpoint merge summary in review runtime

### Phase 10: Iterative Refinement (MANDATORY when Codex available — SKIP if agents SKIPPED)

> **PROTOCOL RULE:** Valid skip: (1) Codex unavailable in Phase 4 health check, (2) agents SKIPPED. If skipped → log `"Iterative Refinement: SKIPPED"`.

Execute per `shared/references/agent_review_workflow.md` "Step: Iterative Refinement".

1) **Artifact:** Changed files from Story scope (post-Phase 9 merge state)
2) **Loop (max 5 iterations):**
   - Build prompt → send to Codex (foreground)
   - **Kill Codex process** (`--verify-dead {pid}`) after each call
   - Parse → **Architecture Gate** (reject backward-compat shims) → AGREE/REJECT each suggestion → apply accepted
   - Quality-based exit: loop continues while MEDIUM/HIGH suggestions exist
   - Synchronous Codex calls may take 5-15 minutes per iteration — this is expected
3) **Display:** `"Iterative Refinement: {N} iterations, {total} suggestions, {applied} applied, exit: {reason}"`
4) **Persist:** `.hex-skills/agent-review/refinement/`, append to `review_history.md`
5) Checkpoint refinement summary in review runtime

### Phase 11: Calculate Verdict + Return Results

**MANDATORY READ:** Load `references/gate_levels.md`

#### Step 11.1: Normalize Component Results

Map each component status to FAIL/CONCERN/ignored using this matrix:

| Component | Status | Maps To | Penalty |
|-----------|--------|---------|---------|
| quality_check | PASS | -- | 0 |
| quality_check | CONCERNS | CONCERN | -10 |
| quality_check | ISSUES_FOUND | FAIL | -20 |
| criteria_validation | PASS | -- | 0 |
| criteria_validation | CONCERNS | CONCERN | -10 |
| criteria_validation | FAIL | FAIL | -20 |
| linters | PASS | -- | 0 |
| linters | FAIL | FAIL | -20 |
| regression | PASS | -- | 0 |
| regression | FAIL | FAIL | -20 |
| tech_debt_cleanup | CLEANED | -- | 0 |
| tech_debt_cleanup | NOTHING_TO_CLEAN | -- | 0 |
| tech_debt_cleanup | BUILD_FAILED | FAIL | -20 |
| tech_debt_cleanup | SKIPPED | ignored | 0 |
| agent_review | CODE_ACCEPTABLE | -- | 0 |
| agent_review | SUGGESTIONS (security/correctness) | CONCERN | -10 |
| agent_review | SKIPPED | ignored | 0 |
| log_analysis | CLEAN | -- | 0 |
| log_analysis | WARNINGS_ONLY | -- | 0 |
| log_analysis | REAL_BUGS_FOUND | FAIL | -20 |
| log_analysis | SKIPPED / NO_LOG_SOURCES | ignored | 0 |

#### Step 11.2: Calculate Quality Verdict

```
fail_count = count of components mapped to FAIL
concern_count = count of components mapped to CONCERN
quality_score = 100 - (20 * fail_count) - (10 * concern_count)

# Fast-fail override: any FAIL -> verdict is FAIL regardless of score
IF fail_count > 0:
  quality_verdict = FAIL
ELSE IF quality_score >= 90:
  quality_verdict = PASS
ELSE IF quality_score >= 70:
  quality_verdict = CONCERNS
ELSE:
  quality_verdict = FAIL
```

#### Step 11.3: Return Results

```yaml
verdict: PASS | CONCERNS | FAIL
quality_score: {0-100}
fail_count: {N}
concern_count: {N}
ignored_components: [tech_debt_cleanup, agent_review]  # only if SKIPPED
quality_check: PASS | CONCERNS | ISSUES_FOUND
code_quality_score: {0-100}
agent_review: CODE_ACCEPTABLE | SUGGESTIONS | SKIPPED
criteria_validation: PASS | CONCERNS | FAIL
linters: PASS | FAIL
tech_debt_cleanup: CLEANED | NOTHING_TO_CLEAN | BUILD_FAILED | SKIPPED
regression: PASS | FAIL
log_analysis: CLEAN | WARNINGS_ONLY | REAL_BUGS_FOUND | SKIPPED
issues:
  - {id: "SEC-001", severity: high, finding: "...", source: "ln-511"}
  - {id: "OPT-001", severity: medium, finding: "...", source: "agent-review"}
  - {id: "DEP-001", severity: medium, finding: "...", source: "criteria"}
  - {id: "LINT-001", severity: low, finding: "...", source: "linters"}
```

### Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Write `.hex-skills/runtime-artifacts/runs/{run_id}/story-quality/{story_id}.json` before finishing.

## TodoWrite format (mandatory)
```
- Invoke ln-511-code-quality-checker (in_progress)
- Start ln-511 child runtime + checkpoint metadata (pending)
- Invoke ln-512-tech-debt-cleaner (pending)
- Start ln-512 child runtime + checkpoint metadata (pending)
- Launch agent review (background) (pending)
- Criteria Validation (Story deps, AC coverage, DB schema) (pending)
- Run linters from tech_stack.md (pending)
- Invoke ln-513-regression-checker (pending)
- Invoke ln-514-test-log-analyzer (pending)
- Start ln-513 and ln-514 child runtimes + checkpoint metadata (pending)
- Merge agent review results (pending)
- Calculate quality_verdict + return results (pending)
```

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 2 | ln-511-code-quality-checker | Runtime-backed managed Skill call; artifact is the only completion signal |
| 3 | ln-512-tech-debt-cleaner | Runtime-backed managed Skill call; artifact is the only completion signal |
| 4 | Inline agent review (Codex + Gemini) | Background — launched after ln-512, merged in Phase 9 |
| 7 | ln-513-regression-checker | Runtime-backed managed Skill call; artifact is the only completion signal |
| 8 | ln-514-test-log-analyzer | Runtime-backed managed Skill call; artifact is the only completion signal |

**All workers:** Start `quality-worker-runtime`, checkpoint `child_run`, then invoke via Skill tool with `runId` and `summaryArtifactPath`. Agent review remains inline and separate from worker-runtime orchestration.

**Anti-Patterns:**
- Running mypy, ruff, pytest directly instead of invoking ln-511/ln-513
- Skipping agent health check or not launching agents in Phase 4
- Auto-fixing code directly instead of invoking ln-512
- Marking steps as completed without invoking the actual skill
- Skipping verdict calculation or returning raw results without normalized `verdict`

## Critical Rules
- Always calculate normalized `verdict` per normalization matrix + gate_levels.md. Final gate_verdict is ln-500's responsibility (includes tests, NFR, waivers)
- Single source of truth: rely on Linear metadata for tasks
- Language preservation in comments (EN/RU)
- Do not create tasks or change statuses; ln-500 decides next actions
- Every managed worker run must start through `quality-worker-runtime` before Skill invocation.

## Definition of Done

- [ ] ln-511 invoked (ALWAYS — full or `--skip-mcp-ref` in fast-track), code quality score returned
- [ ] ln-512 invoked (or skipped if --fast-track), tech debt cleanup results returned
- [ ] Child quality runtimes started and checkpointed before every managed worker invoke
- [ ] Agent review runtime started and Phase 4 launch checkpoint recorded
- [ ] Agent review executed inline (or skipped if --fast-track), results merged in Phase 9
- [ ] All Codex/Gemini processes verified dead after Phase 9 merge AND after each Phase 10 iteration (no orphaned processes)
- [ ] Criteria Validation completed (3 checks)
- [ ] Linters executed
- [ ] ln-513 invoked, regression results returned
- [ ] ln-514 invoked, log analysis results returned (or SKIPPED/NO_LOG_SOURCES)
- [ ] Iterative Refinement executed or SKIPPED (Phase 10)
- [ ] Normalized `verdict` calculated + aggregated results returned
- [ ] Story-quality summary artifact written to the shared location

## Phase 12: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `review-coordinator` (with agents). Run after all phases complete. Output to chat using the `review-coordinator — with agents` format.

## Reference Files
- Criteria Validation: `references/criteria_validation.md`
- Gate levels: `references/gate_levels.md`
- Workers: `../ln-511-code-quality-checker/SKILL.md`, `../ln-512-tech-debt-cleaner/SKILL.md`, `../ln-513-regression-checker/SKILL.md`, `../ln-514-test-log-analyzer/SKILL.md`
- Agent review workflow: `shared/references/agent_review_workflow.md`
- Agent delegation pattern: `shared/references/agent_delegation_pattern.md`
- Review runtime contract: `shared/references/review_runtime_contract.md`
- Agent review memory: `shared/references/agent_review_memory.md`
- Review templates: `shared/agents/prompt_templates/review_base.md` + `modes/code.md`
- Test planning (separate coordinator): `../ln-520-test-planner/SKILL.md`
- Tech stack/linters: `docs/project/tech_stack.md`

---
**Version:** 7.0.0
**Last Updated:** 2026-02-09
