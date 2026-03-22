---
name: ln-310-multi-agent-validator
description: "Validates Stories, plans, or context via parallel multi-agent review with GO/NO-GO verdict. Use when changes need cross-agent validation before proceeding."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# Multi-Agent Validator

Validates Stories/Tasks (mode=story), implementation plans (mode=plan_review), or arbitrary context (mode=context) with parallel multi-agent review and critical verification.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | mode=story | args, git branch, kanban, user | Story to process |
| `plan {file}` | mode=plan_review | args or auto | Plan file to review. Auto-detected from `.claude/plans/` if Read-Only Mode active and no args |
| `context` | mode=context | conversation history, git diff | Review current discussion context + changed files |

**Mode detection:** `"plan"` or `"plan {file}"` or Read-Only Mode active with no args → mode=plan_review. `"context"` → mode=context. Anything else → mode=story.

> **Terminology:** `mode=plan_review` = review mode (evaluating a plan document). "Plan Mode" / "Read-Only Mode" = execution flag (framework-level, applies to ALL modes). These are independent concepts.

> **Plan Mode compatibility:** ln-310 runs normally in Plan Mode. `.agent-review/` is git-ignored — writing prompts, results, and context there is NOT a project modification. If the framework blocks a write, request permission — the user expects file operations in `.agent-review/`. Agent launches (Bash background) are external processes and always work.

**Resolution (mode=story):** Story Resolution Chain. **Status filter:** Backlog

## Purpose

- **mode=story:** Validate Story + Tasks (28 criteria), auto-fix, agent review, approve (Backlog→Todo)
- **mode=plan_review:** Review plans against codebase. Auto-detects in Read-Only Mode. Review with corrections
- **mode=context:** Review documents/architecture via agents + MCP Ref. Review with corrections
- **All modes:** Parallel agents (Codex + Gemini), merge, verify, debate, apply

## Progress Tracking

Create TodoWrite items from Phase headings below:
1. Each phase = todo item. Mark `in_progress` → `completed`
2. Phase 2 and Phase 5 MUST appear as explicit items (CRITICAL — DO NOT SKIP)
3. Phase 7: mark each `[ ]` → `[x]` as you go

## Workflow

### Phase 0: Tools Config

**MANDATORY READ:** Load `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider (`linear` | `file`).
- **mode=plan_review:** `tools_config.md` is optional — `task_provider` not used. If absent: `task_provider = "N/A"`, proceed silently.
- **mode=story | mode=context:** `tools_config.md` required.

Initialize: `agents_launched = UNSET`. MUST be set to `true` or `SKIPPED` in Phase 2.
> **PROTOCOL RULE:** Any reasoning that "this task is too small/simple to require agents" is a PROTOCOL VIOLATION. Task scope does NOT change the agent launch requirement.

### Phase 1: Discovery & Loading

**Step 1:** Resolve storyId per input_resolution_pattern.md

**Step 2:** Load metadata: Story ID/title/status/labels, child Task IDs/titles/status/labels
- IF `task_provider` = `linear`: `get_issue(storyId)` + `list_issues(parentId=storyId)`
- IF `task_provider` = `file`: `Read story.md` + `Glob("docs/tasks/epics/*/stories/*/tasks/*.md")`
- Auto-discover: Team ID (`docs/tasks/kanban_board.md`), project docs (`CLAUDE.md`), epic from Story.project

### Phase 2: Agent Launch (CRITICAL — DO NOT SKIP)

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md`, `shared/references/agent_delegation_pattern.md`

> **CRITICAL:** Agent launch is NOT optional. Executes for ALL modes. The ONLY valid skip: health check returned 0 agents. An Explore agent or ad-hoc research is NOT a substitute. Set `agents_launched` = `true` | `SKIPPED` before proceeding.

> **BLOCKING GATE:** If you find yourself reasoning about skipping agents due to task simplicity, small scope, or "already reviewed" — STOP. Return to the start of Phase 2. The ONLY valid exit without launching is: health_check returned 0 agents.

1) **Health Check** (all modes): Read `docs/environment_state.json` → exclude disabled. **File not found → proceed with all agents (default=enabled, no exclusions).** Run `node shared/agents/agent_runner.mjs --health-check`. 0 available → `agents_launched = SKIPPED`
2) **Prepare references:**
   - mode=story: Story/Task URLs (linear) or file paths (file)
   - mode=context: resolve identifier (default: `review_YYYYMMDD_HHMMSS`), materialize context if from chat → `.agent-review/context/{id}_context.md`
   - mode=plan_review: auto-detect plan (Glob `.claude/plans/*.md`, most recent by mtime). No plan → error. Clean `.agent-review/context/` (delete all files). Materialize: copy plan file → `.agent-review/context/{identifier}_plan.md`. Use local path as `{plan_ref}`
3) **Build prompt:** Assemble from `shared/agents/prompt_templates/review_base.md` + `modes/{mode}.md` (per shared workflow "Step: Build Prompt"). Replace mode-specific placeholders. Save to `.agent-review/{id}_{mode}review_prompt.md`
4) **Launch BOTH agents** as background tasks. `agents_launched = true`

**Exact command (per agent_delegation_pattern.md):**
```
node shared/agents/agent_runner.mjs --agent {name} --prompt-file .agent-review/{agent}/{id}_{mode}review_prompt.md --output-file .agent-review/{agent}/{id}_{mode}review_result.md --cwd {project_dir}
```

**Prompt persistence:** Save prompt to `.agent-review/` before launching agents. Agents are always launched as Bash background tasks — they are external OS processes and are not affected by Claude Code plan mode.

> **Parallelism:** Agents run in background through Phases 3-4. Results merged in Phase 5.

### Phase 3: Research & Audit

> **PREREQUISITE:** Phase 2 completed. If health check was never run → go back to Phase 2.

**MANDATORY READ:** Load `references/phase2_research_audit.md`, `shared/references/research_tool_fallback.md`

**All modes — Steps 3-4 (universal):**
- MCP Research: criteria #5 (Standards), #6 (Versions), #21 (Alternatives), #28 (Feature Utilization)
- Anti-Hallucination: verify factual claims per `shared/references/epistemic_protocol.md`

**mode=story additional (Steps 1-2, 5-7):**
- Step 1-2: Domain Extraction + Inline Documentation
- Step 5: Pre-mortem Analysis
- Step 6: Cross-Reference Analysis
- Step 7: Penalty Points Calculation (28 criteria)
- Display: Penalty Points table + Total + Fix Plan
- Save audit to `.agent-review/{storyId}_phase3_audit.md`
- **Plan Mode:** Show results → WAIT for approval
- **Normal Mode:** Proceed to Phase 4

**mode=plan_review / mode=context additional:**

**MANDATORY READ:** Load `references/context_review_pipeline.md`, `references/mcp_ref_findings_template.md`

Pipeline (while agents run in background):
1. **Applicability Check** — scan for technology decision signals. No signals → skip, go to Phase 5
2. **Stack Detection** — `query_prefix` from: conversation context > `docs/tools_config.md` > indicator files
3. **Extract Topics (3-5)** — technology decisions, score by weight
4. **Research Execution** — apply #5, #6, #21, #28 + AH per `phase2_research_audit.md` (plan/context actions)
5. **Compare & Correct** — max 5 corrections, cite RFC/standard. Apply: plan_review → edit plan file, context → edit documents. Inline rationale `"(per {RFC}: ...)"`
6. **Save Findings** → `.agent-review/context/{id}_mcp_ref_findings.md`

Then proceed to Phase 5.

### Phase 4: Auto-Fix (mode=story only)

**MANDATORY READ per group:** Load the checklist as you execute each group.

| # | Group | Checklist |
|---|-------|-----------|
| 1 | **Structural (#1-#4, #23-#24)** — template, AC, Architecture, Assumptions | `references/structural_validation.md` |
| 2 | **Standards (#5)** — RFC/OWASP (before YAGNI/KISS) | `references/standards_validation.md` |
| 3 | **Solution (#6, #21, #28)** — library versions, alternatives, feature utilization | `references/solution_validation.md` |
| 4 | **Workflow (#7-#13)** — test strategy, docs, size, YAGNI, KISS | `references/workflow_validation.md` |
| 5 | **Quality (#14-#15)** — documentation, hardcoded values | `references/quality_validation.md` |
| 6 | **Dependencies (#18-#19/#19b)** — no forward deps, parallel groups | `references/dependency_validation.md` |
| 7 | **Cross-Reference (#25-#26)** — AC overlap, task duplication | `references/cross_reference_validation.md` |
| 8 | **Risk (#20)** — implementation risk analysis | `references/risk_validation.md` |
| 9 | **Pre-mortem (#27)** — Tiger/Paper Tiger/Elephant | `references/premortem_validation.md` |
| 10 | **Verification (#22)** — AC verify methods | `references/traceability_validation.md` |
| 11 | **Traceability (#16-#17)** — Story-Task alignment, AC coverage (LAST) | `references/traceability_validation.md` |

Zero out penalty points as structural fixes applied (section added, format corrected, placeholder inserted). FLAGGED if auto-fix impossible (human judgment required) → penalty stays, user resolves. Test Strategy section: exist but empty. Maximum Penalty: 113 points.

### Phase 5: Merge + Critical Verification (MANDATORY — DO NOT SKIP)

> **PREREQUISITE:** Phase 2 MUST have completed. If `agents_launched` not set → STOP, go back to Phase 2. An Explore agent is NOT a substitute.

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md` (Critical Verification + Debate), `shared/references/agent_review_memory.md`

1) **Wait for agent results** — process-as-arrive
2) **Parse agent suggestions** from both result files
3) **MERGE** Claude's findings + Agent suggestions. Re-read lines modified in Phase 4 (agents saw pre-fix state)
4) **For EACH suggestion:** dedup (own findings + history) → evaluate → AGREE (accept) or DISAGREE (debate per shared workflow)
5) **Apply accepted** — mode=story: Story/Tasks, mode=plan_review: plan file, mode=context: documents
6) **Save review summary** → `.agent-review/review_history.md`
- SKIPPED verdict (0 agents) → proceed unchanged
- **Display:** `"Agent Review: codex ({accepted}/{total}), gemini ({accepted}/{total}), {N} applied"`

### Phase 6: Approve & Notify (mode=story only)

**mode=context/plan_review:** Skip. Return advisory output. Done.

- **Step 1 (critical):** Set Story + Tasks to Todo; update `kanban_board.md` APPROVED
  - linear: `save_issue({id, state: "Todo"})` for each
  - file: Edit `**Status:**` → `Todo` in story.md + task files
  - **MUST succeed before Step 2.** If fails → retry once → escalate as NO-GO
- **Step 2 (audit):** Summary comment — Penalty Points (Before→After=0), Auto-Fixes, Docs Created, Standards Evidence
  - linear: `save_comment({issueId, body})`
  - file: Write to `docs/tasks/epics/.../comments/{ISO-timestamp}.md`
  - If comment fails after Step 1 succeeded → WARN, do not revert status
- **Display** tabular output (Before/After scores)

## Final Assessment Model

| Metric | Before | After | Meaning |
|--------|--------|-------|---------|
| **Penalty Points** | Raw audit total | Remaining after fixes | 0 = all fixed |
| **Readiness Score** | `10 - (Before / 5)` | `10 - (After / 5)` | Quality confidence (1-10) |
| **Anti-Hallucination** | — | VERIFIED / FLAGGED | Technical claims verified via MCP Ref/Context7 |
| **AC Coverage** | — | N/N (target 100%) | Each AC mapped to >=1 Task |
| **Gate** | — | GO / NO-GO | Final verdict |

**GO:** Penalty After = 0 AND no FLAGGED. **NO-GO:** Penalty After > 0 OR any FLAGGED (auto-fix impossible → penalty stays, user resolves).

**Coverage thresholds:** 100% = no penalty. 80-99% = -3 penalty. <80% = -5 penalty, NO-GO.

## Phase 7: Workflow Completion Self-Check (MANDATORY — DO NOT SKIP)

Mark each `[x]` when verified. ALL must be checked. If ANY unchecked → go back to failed phase. Display checklist to terminal before final results.

### Stop Conditions (Self-Check)

| Condition | Action |
|-----------|--------|
| All checklist items verified | STOP — return results |
| Self-check retry count >= 2 | STOP — report with unchecked items listed as CONCERNS |
| Agents unavailable AND agent items unchecked | STOP — mark agent items SKIPPED, continue |

**All modes:**
- [ ] tools_config loaded, task_provider extracted (Phase 0)
- [ ] Metadata loaded — not skimmed (Phase 1)
- [ ] `agent_runner.mjs --health-check` executed (Phase 2)
- [ ] Agents launched as background tasks OR SKIPPED: 0 agents (Phase 2)
  > ⛔ If unchecked AND environment_state.json showed ≥1 available agent → CRITICAL VIOLATION. Do NOT return results. Return to Phase 2.
- [ ] Prompt file saved to `.agent-review/` (Phase 2)
- [ ] Agent results read and parsed OR SKIPPED (Phase 5)
- [ ] Critical Verification + Debate executed OR SKIPPED (Phase 5)
- [ ] Agent process trees verified dead OR SKIPPED (Phase 5)
- [ ] Review summary saved to `review_history.md` OR SKIPPED (Phase 5)
- [ ] MCP Ref research (#5, #6, #21, #28, AH) executed OR N/A (Phase 3)

**mode=story additional:**
- [ ] Penalty Points calculated, 28 criteria (Phase 3)
- [ ] Auto-fix executed, all 11 groups (Phase 4)
- [ ] Penalty After = 0, Readiness Score = 10 (Phase 4)
- [ ] AC Coverage: 100% (Phase 4)
- [ ] Story + Tasks → Todo, kanban updated, comment posted (Phase 6)

**mode=context / mode=plan_review additional:**
- [ ] Corrections applied to artifacts OR none needed (Phase 3)

## Definition of Done

- [ ] Tools config loaded, task_provider extracted (Phase 0)
- [ ] Metadata loaded (Phase 1)
- [ ] Agent health check executed, agents launched or SKIPPED (Phase 2)
- [ ] Agent process trees verified dead after results collection (Phase 5)
- [ ] Research/Audit completed per mode (Phase 3)
- [ ] Auto-fix executed per mode (Phase 4, mode=story only)
- [ ] Agent results merged, Critical Verification + Debate executed (Phase 5)
- [ ] Status transitions applied per mode (Phase 6, mode=story only)
- [ ] Self-Check all items verified (Phase 7)

## Phase 8: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `review-coordinator` (with agents). Run after Phase 7 completes. Output to chat using the `review-coordinator — with agents` format.

## Template Loading

**Templates:** `story_template.md`, `task_template_implementation.md`

1. Check if `docs/templates/{template}.md` exists in target project
2. IF NOT: copy `shared/templates/{template}.md` → `docs/templates/{template}.md`, replace `{{TEAM_ID}}`, `{{DOCS_PATH}}`
3. Use local copy for all validation

## Reference Files

- **Core config:** `shared/references/tools_config_guide.md`, `storage_mode_detection.md`, `input_resolution_pattern.md`, `plan_mode_pattern.md`
- **Validation criteria:** `references/phase2_research_audit.md` (28 criteria + auto-fix), `references/penalty_points.md`
- **Validation checklists:** `references/structural_validation.md` (#1-4, #23-24), `standards_validation.md` (#5), `solution_validation.md` (#6, #21, #28), `workflow_validation.md` (#7-13), `quality_validation.md` (#14-15), `dependency_validation.md` (#18-19), `risk_validation.md` (#20), `cross_reference_validation.md` (#25-26), `premortem_validation.md` (#27), `traceability_validation.md` (#16-17, #22)
- **Templates:** `shared/templates/story_template.md`, `task_template_implementation.md`; local: `docs/templates/`
- **Agent review:** `shared/references/agent_review_workflow.md`, `agent_delegation_pattern.md`, `agent_review_memory.md`; prompts: `shared/agents/prompt_templates/review_base.md` + `modes/{story,context,plan_review}.md`; challenge: `challenge_review.md`
- **Research:** `shared/references/research_tool_fallback.md`, `references/context_review_pipeline.md`, `domain_patterns.md`, `mcp_ref_findings_template.md`, `shared/references/research_methodology.md`, `shared/references/documentation_creation.md`
- **Other:** `shared/templates/linear_integration.md`, `shared/references/ac_validation_rules.md`

---
**Version:** 7.0.0
**Last Updated:** 2026-02-03
