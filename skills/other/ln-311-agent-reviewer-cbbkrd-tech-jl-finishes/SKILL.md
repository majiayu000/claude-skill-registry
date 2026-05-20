---
name: ln-311-agent-reviewer
description: "Worker that runs parallel external agent reviews (Codex + Gemini) on Story/Tasks. Background tasks, process-as-arrive, critical verification with debate. Returns filtered suggestions for Story validation."
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

## Inputs (from parent skill)
- `storyId`: Linear Story identifier (e.g., "PROJ-123")

## Workflow

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md` for Health Check, Ensure .agent-review/, Load Review Memory, Run Agents, Critical Verification + Debate, Aggregate + Return, Save Review Summary, Fallback Rules, Critical Rules, and Definition of Done. Load `shared/references/agent_delegation_pattern.md` for Reference Passing Pattern, Review Persistence Pattern, Agent Timeout Policy, and Debate Protocol.

### Unique Steps (before shared workflow)

1) **Health check:** per shared workflow, filter by `skill_group` = `311`.

2) **Get references:** Call Linear MCP `get_issue(storyId)` -> extract URL + identifier. Call `list_issues(filter: {parent: {id: storyId}})` -> extract child Task URLs/identifiers.
   - If project stores tasks locally (e.g., `docs/tasks/`) -> use local file paths instead of Linear URLs.

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
- **Shared workflow:** `shared/references/agent_review_workflow.md`
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template (review):** `shared/agents/prompt_templates/story_review.md`
- **Challenge schema:** `shared/agents/schemas/challenge_review_schema.json`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-11
