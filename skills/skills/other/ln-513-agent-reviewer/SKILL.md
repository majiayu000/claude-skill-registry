---
name: ln-513-agent-reviewer
description: "Worker that runs parallel external agent reviews (Codex + Gemini) on code changes. Background tasks, process-as-arrive, critical verification with debate. Returns filtered suggestions with confidence scoring."
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

## Inputs (from parent skill)
- `storyId`: Linear Story identifier (e.g., "PROJ-123")

## Workflow

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md` for Health Check, Ensure .agent-review/, Load Review Memory, Run Agents, Critical Verification + Debate, Aggregate + Return, Save Review Summary, Fallback Rules, Critical Rules, and Definition of Done. Load `shared/references/agent_delegation_pattern.md` for Reference Passing Pattern, Review Persistence Pattern, Agent Timeout Policy, and Debate Protocol.

### Unique Steps (before shared workflow)

1) **Health check:** per shared workflow, filter by `skill_group` = `513`.

2) **Get references:** Call Linear MCP `get_issue(storyId)` -> extract URL + identifier. Call `list_issues(filter: {parent: {id: storyId}, status: "Done"})` -> extract Done implementation Task URLs/identifiers (exclude label "tests").
   - If project stores tasks locally (e.g., `docs/tasks/`) -> use local file paths instead of Linear URLs.

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
- **Shared workflow:** `shared/references/agent_review_workflow.md`
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template (review):** `shared/agents/prompt_templates/code_review.md`
- **Challenge schema:** `shared/agents/schemas/challenge_review_schema.json`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-11
