---
name: codex-validate-plan
description: Validate architecture/plan quality via claude-delegator (Plan Reviewer expert). Use after writing context.md for complex feature/refactor work.
context: fork
---

# Codex Plan Validation (via claude-delegator)

## When to use
- `complexity`: `complex`
- `taskType`: `feature` or `refactor`
- `context.md` exists or was updated

## Procedure

### Step 1: Check MCP Availability (CRITICAL - Do This First)
Before any validation work, verify Codex MCP is available:

```typescript
// Try a simple MCP call to check availability
try {
  mcp__codex__codex({
    prompt: "ping",
    sandbox: "read-only",
    cwd: process.cwd()
  })
  // If successful, MCP is available
} catch (error) {
  // MCP not available - proceed with Claude fallback
}
```

**MCP Unavailable Conditions:**
- Tool not found / not registered
- "quota exceeded", "rate limit", "API error", "unavailable"
- Connection timeout
- Any error response

### Step 2-6: Validation Process

2. Collect the path to context.md (default: `{tasksRoot}/{feature-name}/context.md`) and read its content
3. Build delegation prompt using the 7-section format below

4. **If MCP is available (from Step 1)**:
   - Call `mcp__codex__codex` (include Plan Reviewer instructions in developer-instructions)
   - If successful, proceed to step 6

5. **If MCP is unavailable (from Step 1)**:
   - Claude directly performs the plan review following the Plan Reviewer guidelines below
   - Add note: `"codex-fallback: Claude performed review directly (MCP unavailable)"`
   - Follow the same MUST DO / MUST NOT DO criteria

6. Summarize critical/warning/suggestion items and decide pass/fail
7. **Per `.claude/docs/guidelines/document-memory-policy.md`**: Store full review in `archives/review-v{n}.md`, keep only short summary in `context.md`

## Delegation Format

Use the 7-section format:

```
TASK: Review implementation plan at [context.md path] for completeness and clarity.

EXPECTED OUTCOME: APPROVE/REJECT verdict with specific feedback.

CONTEXT:
- Plan to review: [content of context.md]
- Goals: [what the plan is trying to achieve]
- Constraints: [project constraints]

MUST DO:
- Evaluate all 4 criteria (Clarity, Verifiability, Completeness, Big Picture)
- Simulate actually doing the work to find gaps
- Provide specific improvements if rejecting

MUST NOT DO:
- Rubber-stamp without real analysis
- Provide vague feedback
- Approve plans with critical gaps

OUTPUT FORMAT:
[APPROVE / REJECT]
Justification: [explanation]
Summary: [4-criteria assessment]
[If REJECT: Top 3-5 improvements needed]
```

## Tool Call (When MCP Available)

```typescript
mcp__codex__codex({
  prompt: "[7-section delegation prompt with full context]",
  "developer-instructions": "[contents of plan-reviewer.md]",
  sandbox: "read-only",  // Advisory mode
  cwd: "[current working directory]"
})
```

## Claude Fallback (When MCP Unavailable)

When MCP is not available, Claude performs the validation directly:

1. Apply the same 7-section format as a self-review checklist
2. Evaluate all 4 criteria:
   - **Clarity**: Are the goals and steps clearly defined?
   - **Verifiability**: Can success be measured objectively?
   - **Completeness**: Are all necessary steps included?
   - **Big Picture**: Does it align with overall architecture?
3. Output in the same format: APPROVE/REJECT with justification
4. Add note indicating fallback mode was used

## Output (patch)
```yaml
notes:
  - "codex-plan: [APPROVE/REJECT], warnings=[count]"
  # If fallback was used:
  - "codex-fallback: Claude performed review directly (MCP unavailable)"
```
