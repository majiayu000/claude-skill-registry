---
name: ln-513-agent-reviewer
description: "Worker that runs parallel external agent reviews (Codex + Gemini) on code changes. Background tasks, process-as-arrive, critical verification with debate. Returns filtered suggestions with confidence scoring."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Agent Reviewer (Code)

Runs parallel external agent reviews on code implementation, critically verifies suggestions, returns filtered improvements.

## Purpose & Scope
- Worker in ln-510 quality coordinator pipeline (invoked by ln-510 Phase 4)
- Run codex-review + gemini-review as background tasks in parallel
- Process results as they arrive (first-finished agent processed immediately)
- Critically verify each suggestion; debate with agent if Claude disagrees
- Return filtered, deduplicated, verified suggestions with confidence scoring
- Health check + prompt execution in single invocation

## When to Use
- **Invoked by ln-510-quality-coordinator** Phase 4 (Agent Review)
- All implementation tasks in Story status = Done
- Code quality (ln-511) and tech debt cleanup (ln-512) already completed

## Parameters

| Parameter | Value |
|-----------|-------|
| `review_type` | `codereview` |
| `skill_group` | `513` |
| `prompt_template` | `shared/agents/prompt_templates/code_review.md` |
| `verdict_acceptable` | `CODE_ACCEPTABLE` |

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | Yes | args, git branch, kanban, user | Story to process |

**Resolution:** Per `shared/references/input_resolution_pattern.md` — Story Resolution Chain.
**Status filter:** In Progress, To Review

## Workflow

**MANDATORY READ:** Load `shared/references/input_resolution_pattern.md`, `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, `shared/references/agent_review_workflow.md`, and `shared/references/agent_delegation_pattern.md`.

### Phase 0: Resolve Inputs & Tools Config

1. **Resolve storyId** (per input_resolution_pattern.md):
   - IF args provided → use args
   - ELSE IF git branch matches `feature/{id}-*` → extract id
   - ELSE IF kanban has exactly 1 Story in [In Progress, To Review] → suggest
   - ELSE → AskUserQuestion: show Stories from kanban filtered by [In Progress, To Review]

2. Read `docs/tools_config.md` (bootstrap if missing per tools_config_guide.md).
   Extract: `task_provider` = Task Management → Provider (`linear` | `file`).

### Unique Steps (before shared workflow)

1) **Health check:** per shared workflow, filter by `skill_group` = `513`.

2) **Get references:**
   - IF `task_provider` = `linear`: `get_issue(storyId)` → extract URL + identifier. `list_issues(filter: {parent: {id: storyId}, status: "Done"})` → extract Done implementation Task URLs/identifiers (exclude label "tests").
   - IF `task_provider` = `file`: `Read story.md` → extract path. `Glob("docs/tasks/epics/*/stories/*/tasks/*.md")` → filter Done tasks (check `**Status:** Done`), exclude label "tests".

3) **Ensure .agent-review/:** per shared workflow.

4) **Build prompt:** Read template `shared/agents/prompt_templates/code_review.md`.
   - Replace `{story_ref}` with `- Linear: {url}` or `- File: {path}`
   - Replace `{task_refs}` with bullet list: `- {identifier}: {url_or_path}` per task
   - Save to `.agent-review/{identifier}_codereview_prompt.md` (single shared file -- both agents read the same prompt)

### Shared Workflow Steps

5-8) **Load Review Memory, Run agents, Critical Verification + Debate, Aggregate + Return:** per shared workflow.
   - `{review_type}` = "Code Implementation" (for challenge template)

9) **Save Review Summary:** per shared workflow "Step: Save Review Summary".

## Output Format

```yaml
verdict: CODE_ACCEPTABLE | SUGGESTIONS | SKIPPED
suggestions:
  - area: "security | performance | architecture | correctness | best_practices"
    issue: "What is wrong"
    suggestion: "Specific fix"
    confidence: 95
    impact_percent: 15
    source: "codex-review"
    resolution: "accepted | accepted_after_debate | accepted_after_followup | rejected"
```

Agent stats and debate log per shared workflow output schema.

## Fallback Rules

Per shared workflow, plus:

| Condition | Action |
|-----------|--------|
| Parent skill (ln-510) | Falls back to Self-Review (native Claude) |

## Verdict Escalation
- Findings with `area=security` or `area=correctness` -> parent skill can escalate PASS -> CONCERNS
- This skill returns raw verified suggestions; escalation decision is made by ln-510

## Critical Rules (additional)
- **MANDATORY INVOCATION:** Parent skills MUST invoke this skill. Returns SKIPPED gracefully if agents unavailable. Parent must NOT pre-check and skip.

## Reference Files
- **Tools config:** `shared/references/tools_config_guide.md`
- **Storage mode operations:** `shared/references/storage_mode_detection.md`
- **Shared workflow:** `shared/references/agent_review_workflow.md`
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template (review):** `shared/agents/prompt_templates/code_review.md`
- **Challenge schema:** `shared/agents/schemas/challenge_review_schema.json`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-11
