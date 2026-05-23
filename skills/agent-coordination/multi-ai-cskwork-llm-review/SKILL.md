---
name: multi-ai
description: Start the multi-AI pipeline with a given request. Guides through plan -> review -> implement -> review workflow.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Multi-AI Pipeline Orchestrator

You are starting the multi-AI pipeline. Follow this process exactly.

## Reference Documents

First, read the standards that guide all reviews:
- `skill/multi-ai/reference/standards.md` - Coding standards and review criteria

## Step 1: Clean Up Previous Task

Remove old `.task/` directory if it exists:

```bash
rm -rf .task
mkdir -p .task
```

## Step 2: Capture User Request

Write the user's request to `.task/user-request.txt`.

## Step 3: Create Initial Plan

Write `.task/plan.json`:

```json
{
  "id": "plan-YYYYMMDD-HHMMSS",
  "title": "Short descriptive title",
  "description": "What the user wants to achieve",
  "requirements": ["req1", "req2"],
  "created_at": "ISO8601",
  "created_by": "claude"
}
```

## Step 4: Refine Plan

Research the codebase and create `.task/plan-refined.json`:

```json
{
  "id": "plan-001",
  "title": "Feature title",
  "description": "What the user wants",
  "requirements": ["req1", "req2"],
  "technical_approach": "Detailed how-to",
  "files_to_modify": ["path/to/file.ts"],
  "files_to_create": ["path/to/new.ts"],
  "dependencies": [],
  "estimated_complexity": "low|medium|high",
  "potential_challenges": ["Challenge and mitigation"],
  "refined_by": "claude",
  "refined_at": "ISO8601"
}
```

## Step 5: Sequential Plan Reviews

Run reviews in sequence. Fix issues after each before continuing:

1. **Invoke /review-sonnet**
   - Read `.task/review-sonnet.json` result
   - If `needs_changes`: fix issues in plan, update `.task/plan-refined.json`

2. **Invoke /review-codex**
   - Read `.task/review-codex.json` result
   - If `needs_changes`: fix issues and **restart from step 5.1**
   - If `approved`: continue to implementation

## Step 6: Implement

**Invoke /implement-sonnet**

This skill will:
- Read the approved plan from `.task/plan-refined.json`
- Implement the code
- Add tests
- Output to `.task/impl-result.json`

## Step 7: Sequential Code Reviews

Run reviews in sequence. Fix issues after each before continuing:

1. **Invoke /review-sonnet**
   - Read `.task/review-sonnet.json` result
   - If `needs_changes`: fix code issues

2. **Invoke /review-codex**
   - Read `.task/review-codex.json` result
   - If `needs_changes`: fix issues and **restart from step 7.1**
   - If `approved`: continue to completion

## Step 8: Complete

Write `.task/state.json`:

```json
{
  "state": "complete",
  "plan_id": "plan-001",
  "completed_at": "ISO8601"
}
```

Report success to the user with:
- Summary of what was implemented
- Files changed
- Tests added

---

## Important Rules

- Follow this process exactly - no shortcuts
- Fix ALL issues raised by reviewers before continuing
- If codex rejects, restart the review cycle from sonnet
- Keep the user informed of progress at each major step

## State Files Reference

| File | Purpose |
|------|---------|
| `.task/user-request.txt` | Original user request |
| `.task/plan.json` | Initial plan |
| `.task/plan-refined.json` | Refined plan with technical details |
| `.task/impl-result.json` | Implementation result |
| `.task/review-sonnet.json` | Sonnet review output |
| `.task/review-codex.json` | Codex review output |
| `.task/state.json` | Pipeline state |

## Reference Directory

| Path | Purpose |
|------|---------|
| `skill/multi-ai/reference/standards.md` | Review criteria and coding standards |
| `skill/multi-ai/reference/schemas/` | JSON schemas for structured output |
