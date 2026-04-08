---
name: ln-813-optimization-plan-validator
description: "Validates optimization plan via multi-agent review before execution. Use when verifying feasibility of optimization hypotheses."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-813-optimization-plan-validator

**Type:** L3 Worker
**Category:** 8XX Optimization

Validates optimization plan (performance_map + hypotheses + context) via parallel agent review before committing to code changes. Catches feasibility issues, missing hypotheses, and incorrect conflict mappings before the strike.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | `.hex-skills/optimization/{slug}/context.md` (performance_map, hypotheses, suspicion_stack) |
| **Output** | Verdict (GO / GO_WITH_CONCERNS / NO_GO), corrected context.md, agent feedback summary |
| **Pattern** | Parallel agent review (Codex + Gemini) + own feasibility check → merge → verdict |

---

## Workflow

**Phases:** Load Context + Health Check → Materialize for Agents → Launch Agents → Feasibility Check → Merge + Verify → Verdict

---

## Phase 0: Load Context + Health Check

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md`
**MANDATORY READ:** Load `shared/references/agent_delegation_pattern.md`
**MANDATORY READ:** Load `shared/references/review_runtime_contract.md`

### Slug Resolution

- If invoked via Agent with contextStore containing `slug` — use directly.
- If invoked standalone — ask user for `.hex-skills/optimization/` target directory or scan for single slug.

### Step 1: Load Context

Read `.hex-skills/optimization/{slug}/context.md` from project root. Verify required sections present:

| Section | Required | Verify |
|---------|----------|--------|
| Performance Map | Yes | `performance_map.baseline` has measurements |
| Hypotheses | Yes | At least 1 hypothesis with `files_to_modify` |
| Suspicion Stack | Yes | At least 1 confirmed suspicion |
| Test Command | Yes | Non-empty `test_command` |

If missing → Block: "context.md incomplete — run profiler and researcher first."

### Step 2: Agent Health Check

```
node shared/agents/agent_runner.mjs --health-check --json
```

- Start review runtime for `ln-813` with `mode=plan_review`, `identifier={slug}`, and `expected_agents=["codex","gemini"]`
- 0 agents available → checkpoint runtime with `agents_skipped_reason`, proceed with own feasibility check only
- Agents available → continue to Phase 1

---

## Phase 1: Materialize Context for Agents

Prepare context for external agents (they cannot read `.hex-skills/optimization/` directly):

1. Ensure `.hex-skills/agent-review/` directory exists (with `.gitignore` containing `*`)
2. Copy `.hex-skills/optimization/{slug}/context.md` → `.hex-skills/agent-review/context/{id}_optimization_plan.md`
3. Build per-agent prompts per `agent_review_workflow.md` Step: Build Prompt (steps 1-9). Use `review_base.md` + `modes/plan_review.md`

### Optimization-Specific Focus Areas

Replace default `{focus_areas}` in prompt with:

**MANDATORY READ:** Load [optimization_review_focus.md](references/optimization_review_focus.md)

4. Save per-agent prompts to `.hex-skills/agent-review/{agent}/{id}_optimization_review_prompt.md`

---

## Phase 2: Launch Agents (Background)

Launch available agents as background tasks and register them in review runtime:

```bash
node shared/agents/agent_runner.mjs \
  --agent codex \
  --prompt-file .hex-skills/agent-review/codex/{id}_optimization_review_prompt.md \
  --output-file .hex-skills/agent-review/codex/{id}_optimization_review.md \
  --metadata-file .hex-skills/agent-review/codex/{id}_optimization_review_metadata.json \
  --cwd {project_root}

node shared/agents/agent_runner.mjs \
  --agent gemini \
  --prompt-file .hex-skills/agent-review/gemini/{id}_optimization_review_prompt.md \
  --output-file .hex-skills/agent-review/gemini/{id}_optimization_review.md \
  --metadata-file .hex-skills/agent-review/gemini/{id}_optimization_review_metadata.json \
  --cwd {project_root}
```

After each launch:
- register agent in review runtime with prompt/result/log/metadata paths
- checkpoint launch summary (`health_check_done`, `agents_available`, `agents_required`)

Proceed to Phase 3 while agents work.

---

## Phase 3: Own Feasibility Check (while agents run)

Perform independent validation of the optimization plan:

| Check | How | Fail Action |
|-------|-----|-------------|
| Files exist | For each hypothesis: verify every file in `files_to_modify` exists | Flag hypothesis as INVALID |
| No file conflicts | Check uncontested hypotheses don't modify same file lines | Flag overlap as CONCERN |
| Suspicion coverage | Cross-reference `suspicion_stack` (confirmed) with hypotheses | Flag uncovered suspicions as MISSING_HYPOTHESIS |
| Evidence backing | Each hypothesis should trace to a profiler finding or research source | Flag unsupported as WEAK_EVIDENCE |
| Conflicts correct | Verify `conflicts_with` mappings make sense (H1 really makes H3 unnecessary?) | Flag incorrect as BAD_CONFLICT |
| Fix Hierarchy | Verify hypotheses ordered Configuration→...→Removal. Flag if top hypothesis is level 4-5 | CONCERN: "config-level fix may be available" |
| Removal guard | Any "remove feature" hypothesis MUST have paired "optimize feature" alternative | CONCERN: "removal without optimization alternative" |
| Assumption verification | Each hypothesis's premises — verified by profiler data or just assumed? | Flag: "assumption not verified: {premise}" |
| Depth check | Did profiler go inside all accessible slow services? Check performance_map for surface-level entries | CONCERN: "service X profiled at surface level only" |

### Output

```
feasibility_result:
  valid_hypotheses: [H1, H2, H4]
  invalid_hypotheses: [{id: H3, reason: "file not found: src/cache.py"}]
  concerns: [{type: "file_overlap", detail: "H1 and H2 both modify src/api.py"}]
  missing: [{suspicion: "N+1 in loop at handler.py:45", note: "no hypothesis addresses this"}]
```

---

## Phase 4: Merge Agent Feedback

Sync review runtime agent state, then merge per `shared/references/agent_review_workflow.md`:

1. Do not merge until every required agent is `result_ready | dead | failed | skipped`
2. Parse agent suggestions from all available result files
3. Merge with own feasibility findings (Phase 3)
4. For EACH suggestion: dedup → evaluate → AGREE or REJECT (per shared workflow)
5. Apply accepted corrections directly to `.hex-skills/optimization/{slug}/context.md`:
   - Remove invalid hypotheses
   - Add warnings to concerns
   - Adjust `conflicts_with` if agents found errors
   - Add missing hypotheses if agents identified gaps

Save review summary → `.hex-skills/agent-review/review_history.md`
Checkpoint merge summary in review runtime

Display: `"Agent Review: codex ({accepted}/{total}), gemini ({accepted}/{total}), {N} corrections applied"`

---

## Phase 5: Iterative Refinement (MANDATORY when Codex available)

> **PROTOCOL RULE:** Valid skip: Codex unavailable in health check. If skipped → log `"Iterative Refinement: SKIPPED (Codex unavailable)"`.

Execute per `shared/references/agent_review_workflow.md` "Step: Iterative Refinement".

1) **Artifact:** `.hex-skills/optimization/{slug}/context.md` (post-Phase 4 merge state)
2) **Loop (max 5 iterations):**
   - Build prompt → Codex (foreground)
   - **Kill Codex process** (`--verify-dead {pid}`) after each call
   - Parse → **Architecture Gate** (reject backward-compat shims) → AGREE/REJECT → apply accepted
   - Quality-based exit: loop continues while MEDIUM/HIGH suggestions exist
   - Synchronous Codex calls may take 5-15 minutes per iteration — this is expected
3) **Display + Persist** per shared workflow
4) Checkpoint refinement summary in review runtime

---

## Phase 6: Verdict

| Verdict | Condition |
|---------|-----------|
| **GO** | All hypotheses valid, no critical issues, agents agree plan is feasible |
| **GO_WITH_CONCERNS** | Minor issues found and documented as warnings in context.md. Safe to proceed |
| **NO_GO** | Critical feasibility issue (files missing, fundamental approach flaw, both agents reject) |

### Output

```
validation_result:
  verdict: "GO" | "GO_WITH_CONCERNS" | "NO_GO"
  corrections_applied: <number>
  hypotheses_removed: [<ids>]
  hypotheses_added: [<ids>]
  concerns: [<list>]
  agent_summary: "codex: PLAN_ACCEPTABLE, gemini: SUGGESTIONS (2 accepted)"
```

Return verdict. On NO_GO, present issues to user.

---

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Emit an `optimization-worker` summary envelope.

Managed mode:
- `ln-810` passes deterministic `runId` and exact `summaryArtifactPath`
- write the summary to the provided `summaryArtifactPath`

Standalone mode:
- omit `runId` and `summaryArtifactPath`
- write `.hex-skills/runtime-artifacts/runs/{run_id}/optimization-worker/ln-813--{identifier}.json`

## Error Handling

| Error | Recovery |
|-------|----------|
| Context file missing | Block: "run profiler and researcher first" |
| Both agents unavailable | Proceed with own feasibility check only (reduced confidence) |
| Agent timeout | Use results from available agent + own check |
| Context file malformed | Block: "context.md missing required sections" |

---

## References

- `shared/references/agent_review_workflow.md` — merge + verification protocol
- `shared/references/agent_delegation_pattern.md` — agent invocation pattern
- `shared/references/review_runtime_contract.md` — deterministic runtime contract
- `shared/agents/prompt_templates/modes/plan_review.md` — plan review template
- [optimization_review_focus.md](references/optimization_review_focus.md) — optimization-specific focus areas

---

## Definition of Done

- [ ] Context file loaded and validated (all required sections present)
- [ ] Agent health check performed
- [ ] Review runtime started and launch checkpoint recorded
- [ ] Context materialized to `.hex-skills/agent-review/` for agents
- [ ] Both agents launched (or SKIPPED if unavailable)
- [ ] Own feasibility check completed (files exist, no conflicts, evidence backing)
- [ ] Agent results merged and verified
- [ ] All Codex/Gemini processes verified dead after Phase 4 merge AND after each Phase 5 iteration (no orphaned processes)
- [ ] Corrections applied to context.md
- [ ] Iterative Refinement executed or SKIPPED (Phase 5)
- [ ] Verdict issued (GO / GO_WITH_CONCERNS / NO_GO)
- [ ] Review summary saved to `.hex-skills/agent-review/review_history.md`
- [ ] Optimization validation artifact written to the shared location

---

**Version:** 1.0.0
**Last Updated:** 2026-03-15
