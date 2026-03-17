---
name: ln-311-agent-reviewer
description: "Worker that runs parallel external agent reviews (Codex + Gemini) on Story/Tasks. Background tasks, process-as-arrive, critical verification with debate. Returns filtered suggestions for Story validation."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Agent Reviewer (Story)

Runs parallel external agent reviews on validated Story and Tasks, critically verifies suggestions, returns editorial improvements.

## Purpose & Scope
- Worker in ln-310 validation pipeline (invoked in Phase 5)
- Run codex-review + gemini-review as background tasks in parallel
- Process results as they arrive (first-finished agent processed immediately)
- Critically verify each suggestion; debate with agent if Claude disagrees
- Return filtered, deduplicated, verified suggestions for Story/Tasks improvement
- Health check + prompt execution in single invocation

## When to Use
- **Invoked by ln-310-story-validator** Phase 5 (Agent Review)
- After Phase 4 auto-fixes applied, Penalty Points = 0
- Story and Tasks are in their final form before approval

## Parameters

| Parameter | Value |
|-----------|-------|
| `review_type` | `storyreview` |
| `skill_group` | `311` |
| `prompt_template` | `shared/agents/prompt_templates/story_review.md` |
| `verdict_acceptable` | `STORY_ACCEPTABLE` |

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | Yes | args, git branch, kanban, user | Story to process |

**Resolution:** Per `shared/references/input_resolution_pattern.md` — Story Resolution Chain.
**Status filter:** Backlog

## Workflow

**MANDATORY READ:** Load `shared/references/input_resolution_pattern.md`, `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, `shared/references/agent_review_workflow.md`, and `shared/references/agent_delegation_pattern.md`.

### Phase 0: Resolve Inputs & Tools Config

1. **Resolve storyId** (per input_resolution_pattern.md):
   - IF args provided → use args
   - ELSE IF git branch matches `feature/{id}-*` → extract id
   - ELSE IF kanban has exactly 1 Story in [Backlog] → suggest
   - ELSE → AskUserQuestion: show Stories from kanban filtered by [Backlog]

2. Read `docs/tools_config.md` (bootstrap if missing per tools_config_guide.md).
   Extract: `task_provider` = Task Management → Provider (`linear` | `file`).

### Unique Steps (before shared workflow)

1) **Health check:** per shared workflow, filter by `skill_group` = `311`.

2) **Get references:**
   - IF `task_provider` = `linear`: `get_issue(storyId)` → extract URL + identifier. `list_issues(filter: {parent: {id: storyId}})` → extract child Task URLs/identifiers.
   - IF `task_provider` = `file`: `Read story.md` → extract path. `Glob("docs/tasks/epics/*/stories/*/tasks/*.md")` → extract child Task file paths.

3) **Ensure .agent-review/:** per shared workflow.

4) **Build prompt:** Read template `shared/agents/prompt_templates/story_review.md`.
   - Replace `{story_ref}` with `- Linear: {url}` or `- File: {path}`
   - Replace `{task_refs}` with bullet list: `- {identifier}: {url_or_path}` per task
   - Save to `.agent-review/{identifier}_storyreview_prompt.md` (single shared file -- both agents read the same prompt)

### Shared Workflow Steps

5-8) **Load Review Memory, Run agents, Critical Verification + Debate, Aggregate + Return:** per shared workflow.
   - `{review_type}` = "Story/Tasks" (for challenge template)

9) **Save Review Summary:** per shared workflow "Step: Save Review Summary".

## Output Format

```yaml
verdict: STORY_ACCEPTABLE | SUGGESTIONS | SKIPPED
suggestions:
  - area: "security | performance | architecture | feasibility | best_practices | risk_analysis"
    issue: "What is wrong or could be improved"
    suggestion: "Specific change to Story or Tasks"
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
| Parent skill (ln-310) | Falls back to Self-Review (native Claude) |

## Verdict Escalation
- **No escalation.** Suggestions are editorial only -- they modify Story/Tasks text.
- Parent skill (ln-310) Gate verdict remains unchanged by agent suggestions.

## Critical Rules (additional)
- **MANDATORY INVOCATION:** Parent skills MUST invoke this skill. Returns SKIPPED gracefully if agents unavailable. Parent must NOT pre-check and skip.

## Reference Files
- **Tools config:** `shared/references/tools_config_guide.md`
- **Storage mode operations:** `shared/references/storage_mode_detection.md`
- **Shared workflow:** `shared/references/agent_review_workflow.md`
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template (review):** `shared/agents/prompt_templates/story_review.md`
- **Challenge schema:** `shared/agents/schemas/challenge_review_schema.json`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-11
