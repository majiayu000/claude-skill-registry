---
name: ln-005-agent-reviewer
description: "Universal context reviewer: delegates arbitrary context (plans, decisions, documents, architecture proposals) to external agents (Codex + Gemini) for independent review with debate protocol. Context always passed via files."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Agent Reviewer (Universal)

Runs parallel external agent reviews on arbitrary context, critically verifies suggestions, returns filtered improvements.

## Purpose & Scope
- Standalone utility in 0XX category (like ln-003, ln-004)
- Delegate any context to codex-review + gemini-review as background tasks in parallel
- Context always passed via file references (never inline in prompt)
- Process results as they arrive (first-finished agent processed immediately)
- Critically verify each suggestion; debate with agent if Claude disagrees
- Return filtered, deduplicated, verified suggestions

## When to Use
- Manual invocation by user for independent review of any artifact
- Called by any skill needing external second opinion on plans, decisions, documents
- NOT tied to Linear, NOT tied to any pipeline
- Works with any context that can be saved to a file

## Parameters

| Parameter | Value |
|-----------|-------|
| `review_type` | `contextreview` |
| `skill_group` | `005` |
| `prompt_template` | `shared/agents/prompt_templates/context_review.md` |
| `verdict_acceptable` | `CONTEXT_ACCEPTABLE` |

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `context_files` | Yes | List of file paths containing context to review (relative to CWD) |
| `identifier` | No | Short label for file naming (default: `review_YYYYMMDD_HHMMSS`) |
| `focus` | No | List of areas to focus on (default: all 6) |
| `review_title` | No | Human-readable title (default: `"Context Review"`) |

**Context delivery rule:** Context is ALWAYS passed via files.
- If context already exists as files (plans, docs, code) -> pass file paths directly
- If context is a statement/decision from chat -> caller creates a temporary file in `.agent-review/context/` with the content, then passes the file path

## Workflow

**MANDATORY READ:** Load `shared/references/agent_review_workflow.md` for Health Check, Ensure .agent-review/, Load Review Memory, Run Agents, Critical Verification + Debate, Aggregate + Return, Save Review Summary, Fallback Rules, Critical Rules, and Definition of Done. Load `shared/references/agent_delegation_pattern.md` for Reference Passing Pattern, Review Persistence Pattern, Agent Timeout Policy, and Debate Protocol.

### Unique Steps (before shared workflow)

1) **Health check:** per shared workflow, filter by `skill_group` = `005`.

2) **Resolve identifier:** If `identifier` not provided, generate `review_YYYYMMDD_HHMMSS`. Sanitize: lowercase, replace spaces with hyphens, ASCII only.

3) **Ensure .agent-review/:** per shared workflow. Additionally create `.agent-review/context/` subdir if it doesn't exist (for materialized context files).

4) **Materialize context (if needed):** If context is from chat/conversation (not an existing file):
   - Write content to `.agent-review/context/{identifier}_context.md`
   - Add this path to `context_files` list

5) **Build prompt:** Read template `shared/agents/prompt_templates/context_review.md`.
   - Replace `{review_title}` with title or `"Context Review"`
   - Replace `{context_refs}` with bullet list: `- {path}` per context file
   - Replace `{focus_areas}` with filtered subset or `"All default areas"` if no focus specified
   - Save to `.agent-review/{identifier}_contextreview_prompt.md` (single shared file -- both agents read the same prompt)

### Shared Workflow Steps

6-9) **Load Review Memory, Run agents, Critical Verification + Debate, Aggregate + Return:** per shared workflow.
   - `{review_type}` in challenge template = review_title or "Context Review"
   - `{story_ref}` in challenge template = identifier

10) **Save Review Summary:** per shared workflow "Step: Save Review Summary".

## Output Format

```yaml
verdict: CONTEXT_ACCEPTABLE | SUGGESTIONS | SKIPPED
suggestions:
  - area: "logic | feasibility | completeness | consistency | best_practices | risk"
    issue: "What is wrong or could be improved"
    suggestion: "Specific actionable change"
    confidence: 95
    impact_percent: 15
    source: "codex-review"
    resolution: "accepted | accepted_after_debate | accepted_after_followup | rejected"
```

Agent stats and debate log per shared workflow output schema.

## Verdict Escalation
- **No escalation.** Suggestions are advisory only.
- Caller decides how to apply accepted suggestions.

## Reference Files
- **Shared workflow:** `shared/references/agent_review_workflow.md`
- **Agent delegation pattern:** `shared/references/agent_delegation_pattern.md`
- **Prompt template (review):** `shared/agents/prompt_templates/context_review.md`
- **Review schema:** `shared/agents/schemas/context_review_schema.json`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-25
