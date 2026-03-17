---
name: oh-my-ccg-review
description: 独立双模型交叉审查（随时可用）
---

# oh-my-ccg Review Phase

You are executing an independent dual-model cross-review. This can be run at any time.

## Workflow

### Step 1: Collect Artifacts
Determine what to review:
- If RPI state exists with a change: use `rpi_state_read` MCP tool to load the change's implementation details
- If git diff has changes: review the diff
- Otherwise: ask user what to review

### Step 2: Dual-Model Review (PARALLEL — MANDATORY)
Launch BOTH models **in a single message** using MCP tools:

**Codex** (code-reviewer role) — use `ask_codex` tool:
- `agent_role`: "code-reviewer"
- `prompt`: Include the code to review, ask for logic/security analysis
- `context_files`: All changed files
- `background`: true

**Gemini** (designer role) — use `ask_gemini` tool:
- `agent_role`: "designer"
- `prompt`: Include the code to review, ask for pattern/maintainability analysis
- `files`: All changed files
- `background`: true

Then use `check_job_status` for both job IDs to collect results.

### Step 3: Synthesize Findings
Merge findings from both models:
- Deduplicate overlapping issues
- Classify severity: Critical / Warning / Info
- Cross-reference: issues found by BOTH models get elevated severity

### Step 4: Present Report
```
## Review Report

### Critical (must fix)
- [C1] file:line — description (found by: Codex/Gemini/Both)

### Warning (should fix)
- [W1] file:line — description

### Info (nice to have)
- [I1] file:line — description

### Summary
- Total findings: X (C: N, W: N, I: N)
- Cross-validated: N issues found by both models
```

### Step 5: Decision Gate
Ask user:
- **Fix**: Address Critical/Warning issues → loop back to executor
- **Accept**: Archive the review, proceed
- **Defer**: Note issues for later, proceed

If fixing: use `rpi_state_write` MCP tool to record review findings and transition back to impl.
