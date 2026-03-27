---
name: ln-310-multi-agent-validator
description: "Validates Stories, plans, or context via deterministic multi-agent review with runtime-controlled status gates. Use before execution or approval."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

**Type:** L2 Coordinator
**Category:** 3XX Planning

# Multi-Agent Validator

Validates Stories/Tasks (`mode=story`), implementation plans (`mode=plan_review`), or arbitrary context (`mode=context`) with deterministic runtime state, parallel external review, critical verification, and optional approval.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | mode=story | args, git branch, kanban, user | Story to process |
| `plan {file}` | mode=plan_review | args or auto | Plan file to review. Auto-detected from `.claude/plans/` if Read-Only Mode active and no args |
| `context` | mode=context | conversation history, git diff | Review current discussion context + changed files |

**Mode detection:** `"plan"` or `"plan {file}"` or Read-Only Mode active with no args -> `mode=plan_review`. `"context"` -> `mode=context`. Anything else -> `mode=story`.

> **Terminology:** `mode=plan_review` is the review target. Plan Mode / Read-Only Mode is the framework execution flag. They are independent.

> **Plan Mode compatibility:** `.hex-skills/agent-review/` remains git-ignored. Runtime state, prompts, results, logs, and materialized context files may be written there even in Plan Mode.

**Resolution (mode=story):** Story Resolution Chain. **Status filter:** Backlog

## Purpose

- `mode=story`: validate Story + Tasks against 28 criteria, auto-fix structural issues, merge agent review, then approve (`Backlog -> Todo`) only after zero remaining blockers
- `mode=plan_review`: review plan against codebase, standards, and alternatives; apply accepted corrections
- `mode=context`: review architecture/documents/context materials; apply accepted corrections
- All modes: run deterministic agent review with runtime checkpoints, critical verification, and Codex refinement

## Progress Tracking

Create TodoWrite items from phase headings below:
1. Each phase = one todo item
2. Phase 2 and Phase 5 MUST appear explicitly
3. Phase 8 checklist items must be marked as they are verified

## Workflow

### Phase 0: Config + Runtime Start

**MANDATORY READ:** Load `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`
**MANDATORY READ:** Load `shared/references/review_runtime_contract.md`

1. Detect `task_provider` from tools config.
   - `mode=plan_review`: `tools_config.md` optional. If absent, use `task_provider = "N/A"`.
   - `mode=story | mode=context`: `tools_config.md` required.
2. Resolve `mode`, `identifier`, and storage mode.
3. Build runtime manifest with:
   - `storage_mode`
   - `story_ref | plan_ref | context_ref`
   - `expected_agents = ["codex", "gemini"]`
   - `artifact_paths` for prompt/result/log/metadata roots
   - `phase_policy` (`story`: phase4/phase7 required; others: `skipped_by_mode`)
4. Save manifest to `.hex-skills/agent-review/runtime/{identifier}_manifest.json`
5. Start runtime:

```bash
node shared/scripts/review-runtime/cli.mjs start \
  --skill ln-310 \
  --mode {mode} \
  --identifier {identifier} \
  --manifest-file .hex-skills/agent-review/runtime/{identifier}_manifest.json
```

6. Write Phase 0 checkpoint after config + runtime start succeed.

### Phase 1: Discovery & Materialization

1. Resolve primary artifact:
   - `story`: resolve Story + child Tasks
   - `plan_review`: resolve plan file, or auto-detect latest `.claude/plans/*.md`
   - `context`: resolve identifier and materialize chat-derived context if needed
2. Load metadata:
   - `linear`: `get_issue(storyId)` + `list_issues(parentId=storyId)`
   - `file`: read `story.md` + task files
3. Materialize any non-project file paths into `.hex-skills/agent-review/context/`
4. Checkpoint Phase 1 with resolved refs and metadata summary.

### Phase 2: Agent Launch

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md`, `shared/references/agent_delegation_pattern.md`

1. Run health check:

```bash
node shared/agents/agent_runner.mjs --health-check --json
```

2. Exclude agents disabled in `.hex-skills/environment_state.json`.
3. If `available_count = 0`:
   - set `agents_skipped_reason`
   - checkpoint Phase 2 with `health_check_done=true`, `agents_available=0`
   - advance to Phase 3
4. Otherwise:
   - ensure `.hex-skills/agent-review/{agent}/` exists
   - build per-agent prompt from `review_base.md` + `modes/{story,context,plan_review}.md`
   - save prompt to `.hex-skills/agent-review/{agent}/{identifier}_{review_type}_prompt.md`
5. Launch every available agent with explicit metadata file:

```bash
node shared/agents/agent_runner.mjs \
  --agent {name} \
  --prompt-file .hex-skills/agent-review/{agent}/{identifier}_{review_type}_prompt.md \
  --output-file .hex-skills/agent-review/{agent}/{identifier}_{review_type}_result.md \
  --metadata-file .hex-skills/agent-review/{agent}/{identifier}_{review_type}_metadata.json \
  --cwd {project_dir}
```

6. Register each launched agent in runtime:

```bash
node shared/scripts/review-runtime/cli.mjs register-agent \
  --skill ln-310 \
  --agent {name} \
  --prompt-file .hex-skills/agent-review/{agent}/{identifier}_{review_type}_prompt.md \
  --result-file .hex-skills/agent-review/{agent}/{identifier}_{review_type}_result.md \
  --log-file .hex-skills/agent-review/{agent}/{identifier}_{review_type}.log \
  --metadata-file .hex-skills/agent-review/{agent}/{identifier}_{review_type}_metadata.json
```

7. Checkpoint Phase 2 with `health_check_done`, `agents_available`, `agents_required`, optional `agents_skipped_reason`.

### Phase 3: Research & Audit

**MANDATORY READ:** Load `references/phase2_research_audit.md`, `shared/references/research_tool_fallback.md`

Common work:
- MCP research for #5, #6, #21, #28
- Anti-hallucination verification per `shared/references/epistemic_protocol.md`

`mode=story`:
- domain extraction + inline documentation
- pre-mortem analysis
- cross-reference analysis
- penalty points calculation across all 28 criteria
- save audit to `.hex-skills/agent-review/{storyId}_phase3_audit.md`

`mode=plan_review | mode=context`:
- **MANDATORY READ:** Load `references/context_review_pipeline.md`, `references/mcp_ref_findings_template.md`
- run applicability -> stack detection -> topics -> research -> compare/correct -> findings save

Checkpoint Phase 3 with audit/research summary.

### Phase 4: Auto-Fix (`mode=story` only)

**MANDATORY READ per group:** Load the checklist as you execute each group.

| # | Group | Checklist |
|---|-------|-----------|
| 1 | Structural (#1-#4, #23-#24) | `references/structural_validation.md` |
| 2 | Standards (#5) | `references/standards_validation.md` |
| 3 | Solution (#6, #21, #28) | `references/solution_validation.md` |
| 4 | Workflow (#7-#13) | `references/workflow_validation.md` |
| 5 | Quality (#14-#15) | `references/quality_validation.md` |
| 6 | Dependencies (#18-#19/#19b) | `references/dependency_validation.md` |
| 7 | Cross-Reference (#25-#26) | `references/cross_reference_validation.md` |
| 8 | Risk (#20) | `references/risk_validation.md` |
| 9 | Pre-mortem (#27) | `references/premortem_validation.md` |
| 10 | Verification (#22) | `references/traceability_validation.md` |
| 11 | Traceability (#16-#17) | `references/traceability_validation.md` |

Rules:
- zero out penalty points only when the defect is actually repaired
- use `FLAGGED` only when human judgment is required and auto-fix cannot safely continue
- test strategy section may exist but remain empty
- max penalty = 113

Checkpoint Phase 4 with penalty before/after, flagged items, and coverage summary.

For `mode=plan_review | mode=context`, checkpoint Phase 4 as `{"status":"skipped_by_mode"}`.

### Phase 5: Merge + Critical Verification

1. Sync every launched agent through runtime:

```bash
node shared/scripts/review-runtime/cli.mjs sync-agent --skill ln-310
```

2. Do not merge until all required agents are in `result_ready | dead | failed | skipped`.
3. Parse available result files.
4. For each suggestion:
   - deduplicate against own findings + review history
   - verify independently
   - mark `AGREE` or `REJECT`
5. Apply accepted suggestions:
   - `story`: patch Story/Tasks after re-reading Phase 4 output
   - `context`: patch target docs/context files
   - `plan_review`: prefer best `## Refined Plan`, then apply remaining accepted patches
6. Save review summary to `.hex-skills/agent-review/review_history.md`
7. Checkpoint Phase 5 with `merge_summary`.

### Phase 6: Iterative Refinement

**MANDATORY READ:** Load `shared/agents/prompt_templates/iterative_refinement.md`

1. Determine artifact:
   - `story`: Story + Tasks concatenation
   - `plan_review`: plan file
   - `context`: context docs
2. Run Codex refinement loop up to 5 iterations if Codex was available in Phase 2.
3. Skip only with machine-readable reason:
   - disabled
   - unavailable in health check
   - dead/failed after runtime sync
4. Persist prompts/results to `.hex-skills/agent-review/refinement/`
5. Checkpoint Phase 6 with `iterations`, `exit_reason`, `applied`.

### Phase 7: Approve & Notify (`mode=story` only)

1. Set Story + Tasks to `Todo`; update `kanban_board.md` to `APPROVED`.
   - `linear`: `save_issue({id, state: "Todo"})`
   - `file`: edit `**Status:** -> Todo`
2. Retry status transition once if needed. If still failing -> verdict becomes `NO_GO`.
3. Write audit comment / file with penalty before/after, fixes, docs, and standards evidence.
4. If comment fails after status success -> warn, do not revert status.
5. Checkpoint Phase 7 with approval/status result.

For `mode=plan_review | mode=context`, checkpoint Phase 7 as `{"status":"skipped_by_mode"}`.

### Phase 8: Runtime Self-Check

Build the final checklist from runtime state. This is a projection of machine-readable checkpoints, not a second source of truth.

Required checks:
- [ ] Phase 0 checkpoint exists
- [ ] Phase 1 checkpoint exists
- [ ] Phase 2 recorded health check and launch/skip result
- [ ] Phase 3 audit/research checkpoint exists
- [ ] Phase 4 checkpoint exists (`story`) or `skipped_by_mode` (`plan_review/context`)
- [ ] All required agents resolved before Phase 5 merge
- [ ] Phase 5 merge summary exists
- [ ] Phase 6 refinement exit reason exists
- [ ] Phase 7 checkpoint exists (`story`) or `skipped_by_mode`
- [ ] Final verdict and user-facing output are ready

Write Phase 8 checkpoint with `pass=true|false`. Complete runtime only after `pass=true`.

## Final Assessment Model

| Metric | Before | After | Meaning |
|--------|--------|-------|---------|
| Penalty Points | Raw audit total | Remaining after fixes | 0 = all fixed |
| Readiness Score | `10 - (Before / 5)` | `10 - (After / 5)` | Quality confidence (1-10) |
| Anti-Hallucination | — | VERIFIED / FLAGGED | Technical claims verified via MCP Ref/Context7 |
| AC Coverage | — | N/N (target 100%) | Each AC mapped to >=1 Task |
| Gate | — | GO / NO_GO | Final verdict |

Rules:
- `GO`: Penalty After = 0 and no `FLAGGED`
- `NO_GO`: Penalty After > 0 or any `FLAGGED`
- coverage: 100% = pass; 80-99% = -3 penalty; <80% = -5 penalty and `NO_GO`

## Definition of Done

- [ ] Runtime manifest created and `start` executed successfully
- [ ] Discovery/materialization checkpointed
- [ ] Agent health check executed and recorded in runtime
- [ ] Every launched agent registered with prompt/result/log/metadata paths
- [ ] Research/Audit completed per mode and checkpointed
- [ ] Story auto-fix completed or non-story Phase 4 skipped by mode
- [ ] Agent results merged only after all required agents resolved
- [ ] Review summary saved to `review_history.md`
- [ ] Iterative Refinement executed or skipped with machine-readable reason
- [ ] Story approval/status transition completed or non-story Phase 7 skipped by mode
- [ ] Phase 8 self-check passed and runtime completed

## Phase 9: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `review-coordinator` (with agents). Run after Phase 8 completes. Output to chat using the `review-coordinator — with agents` format.

## Template Loading

**Templates:** `story_template.md`, `task_template_implementation.md`

1. Check if `docs/templates/{template}.md` exists in target project
2. If not, copy `shared/templates/{template}.md` -> `docs/templates/{template}.md`
3. Use local copy for all validation

## Reference Files

- Core config: `shared/references/tools_config_guide.md`, `storage_mode_detection.md`, `input_resolution_pattern.md`, `plan_mode_pattern.md`
- Runtime: `shared/references/review_runtime_contract.md`, `shared/scripts/review-runtime/cli.mjs`
- Validation criteria: `references/phase2_research_audit.md`, `references/penalty_points.md`
- Validation checklists: `references/structural_validation.md`, `standards_validation.md`, `solution_validation.md`, `workflow_validation.md`, `quality_validation.md`, `dependency_validation.md`, `risk_validation.md`, `cross_reference_validation.md`, `premortem_validation.md`, `traceability_validation.md`
- Agent review: `shared/references/agent_review_workflow.md`, `agent_delegation_pattern.md`, `agent_review_memory.md`
- Prompt templates: `shared/agents/prompt_templates/review_base.md`, `modes/{story,context,plan_review}.md`, `iterative_refinement.md`
- Research: `shared/references/research_tool_fallback.md`, `references/context_review_pipeline.md`, `domain_patterns.md`, `mcp_ref_findings_template.md`, `shared/references/research_methodology.md`

---
**Version:** 8.0.0
**Last Updated:** 2026-03-22
