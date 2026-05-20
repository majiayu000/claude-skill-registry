---
name: dev-buddy-review
description: Review a plan or implementation. Dispatches review executors, validates outputs, owns the review→repair→re-review loop. Appends Review Record to plan file. Use --plan for plan review, --code for code review.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TaskOutput, AskUserQuestion, Skill
---

# Review Stage Skill

Review a plan or code implementation. Dispatches reviewers, aggregates results, and appends Review Record to the plan file. Owns the review→repair→re-review loop.

**Usage:** `/dev-buddy-review --plan` or `/dev-buddy-review --code`

---

## Step 1: Determine Review Type

Parse the invocation for `--plan` or `--code` flag.
- `--plan` → plan review (uses `stages['plan-review']` executors)
- `--code` → code review (uses `stages['code-review']` executors)
- Neither → ask the user which review to run

---

## Step 2: Validate Inputs

Read the plan file and verify required sections exist:

**For plan review (`--plan`):**
- `## Requirements` section with acceptance criteria
- `## TDD Test Plan` section
- `## Risk Registry` section
- `## Implementation Steps` section

**For code review (`--code`):**
- All of the above, plus:
- Implementation steps should show some completed status
- Git diff shows actual code changes

If any required section is missing, tell the user which stage to run first.

---

## Step 3: Load Config and Resolve Executors

```bash
bun -e "
import { loadDevBuddyConfig, getProviderType } from '${CLAUDE_PLUGIN_ROOT}/scripts/pipeline-config.ts';
const config = loadDevBuddyConfig();
const stageType = '{plan-review or code-review}';
const stage = config.stages[stageType];
const executors = stage.executors.map(exec => ({
  ...exec,
  providerType: getProviderType(exec.preset)
}));
console.log(JSON.stringify({ executors, max_iterations: config.max_iterations }));
"
```

---

## Step 4: Resolve Session Variables

Same pattern as other skills — tmpdir, random ID, output directory.
Output file for executor at index `{i}`: `{TMPDIR}/.vcp/oneshot/review-{RAND}-{i}.json`

---

## Step 5: Extract Context from Plan File

Read the plan file and extract ALL relevant sections for the review prompt:
- Requirements (ACs, scope)
- TDD Test Plan (test IDs with AC mappings)
- Risk Registry
- Implementation Steps (for plan review)
- Impact Analysis
- For code review: also read git diff and implementation status

---

## Step 6: Prompt Assembly

**Plan review prompt:**
```
You are executing the PLAN REVIEW stage.
Your system prompt name is: {executor.system_prompt}
Your model is: {executor.model}
Set revision_number to: {revision_number}

PESSIMISTIC-FIRST: Assume NOTHING in this plan will work as described.
For each step:
1. What specific test would fail if this step has a bug? Reference test IDs from the TDD Test Plan.
2. Is this step truly one architectural unit? If it touches multiple modules, flag it.
3. Does it reuse existing code? If it creates new code where existing works, flag it.
4. Is the rollback specific? "Revert changes" is not acceptable.

REQUIREMENTS:
{extracted ACs}

TDD TEST PLAN:
{extracted test IDs with AC mappings}

RISK REGISTRY:
{extracted risks — flag unacknowledged}

IMPLEMENTATION STEPS:
{extracted steps with AC/test mappings}

Review and write output to {TMPDIR}/.vcp/oneshot/review-{RAND}-{i}.json
```

**Code review prompt:**
```
You are executing the CODE REVIEW stage.
Your system prompt name is: {executor.system_prompt}
Your model is: {executor.model}
Set revision_number to: {revision_number}

PESSIMISTIC-FIRST: Assume every line of changed code has a bug. Find them.
For each AC:
1. Find the specific code path that implements it — cite file:line
2. Trace input → processing → output through that path
3. Identify what would break if any step fails

REQUIREMENTS:
{extracted ACs}

TDD TEST PLAN:
{extracted tests}

GIT DIFF:
{actual code changes}

Review and write output to {TMPDIR}/.vcp/oneshot/review-{RAND}-{i}.json
```

---

## Step 7: Dispatch Executors

**Resolve system prompt with stage/role composition** (same pattern as other skills).

Route by provider type:
- **subscription:** `Task(subagent_type: "general-purpose", ...)`
- **api:** `Bash(run_in_background: true)` → `bun "${CLAUDE_PLUGIN_ROOT}/scripts/one-shot-runner.ts" --type api --output-id review-{RAND}-{i} --preset "{PRESET}" --model "{MODEL}" --cwd "${CLAUDE_PROJECT_DIR}" --task-stdin`

Dispatch ALL executors — do NOT skip any. The last executor (synthesizer) does its own review AND reads prior outputs.

---

## Step 8: Collect and Aggregate Results

Read all review output files from `{TMPDIR}/.vcp/oneshot/review-{RAND}-*.json`.

**For API/CLI executors:** The output file is wrapped in an envelope `{"event":"complete","provider":"...","model":"...","result":"..."}`. Parse the `result` field (which is a JSON string) to get the actual reviewer output. For subscription executors, the result is returned directly from the Task tool.

Parse each reviewer's JSON output. Extract:
- `status` (approved/needs_changes/needs_clarification/rejected)
- `findings[]` with `fix_type` (must_fix/advisory)
- `requirements_coverage` (plan review) or `acceptance_criteria_verification` (code review)
- `revision_number`

**Aggregation rules:**
- If ANY reviewer has `must_fix` findings → aggregate status = `needs_changes`
- If ALL reviewers approved → aggregate status = `approved`
- Compile ALL findings from all reviewers (deduplicate by contract_reference)

---

## Step 9: Handle Clarification (Check Plan File First!)

**CRITICAL RULE: Before asking the user ANY question, search the plan file for existing answers.**

Check the Impact Analysis questions, Risk Registry decisions, and user responses from the requirements phase. If the answer already exists in the plan file, do NOT re-ask.

Only use AskUserQuestion for genuinely new questions that couldn't have been anticipated during planning.

If a reviewer returned `needs_clarification` but the answer is in the plan file:
- Convert the finding to `must_fix` or resolve it
- Do NOT ask the user

---

## Step 10: Append Review Record to Plan File

**Note:** The plan file record is a **consolidated** aggregation of all executor outputs. Single-executor fields (`reviewer`, `model`) from the stage contract are merged into `reviewers: [{name, model}]` for multi-executor traceability.

**For plan review, append `## Plan Review Record`:**
```markdown
## Plan Review Record

```json
{
  "id": "review-YYYYMMDD-HHMMSS",
  "reviewer": "synthesizer system_prompt name (or first reviewer if single)",
  "model": "synthesizer model (or first reviewer model if single)",
  "revision_number": 1,
  "reviewers": [{"name": "{system_prompt}", "model": "{model}"}],
  "status": "approved|needs_changes|needs_clarification|rejected",
  "summary": "2-3 sentence consolidated summary",
  "needs_clarification": false,
  "clarification_questions": [],
  "findings": [{all must_fix and advisory findings from all reviewers, deduplicated}],
  "requirements_coverage": {
    "mapping": [{"ac_id": "AC-1", "steps": ["step 1"], "tests": ["UT-1"]}],
    "acs_without_steps": [],
    "acs_without_tests": [],
    "steps_without_ac": [],
    "steps_without_tests": [],
    "risks_unacknowledged": []
  },
  "reviewed_at": "{ISO8601}"
}
```
```

**For code review, append `## Code Review Record` and update `## Sign-off`:**
```markdown
## Code Review Record

```json
{
  "id": "code-review-YYYYMMDD-HHMMSS",
  "reviewer": "synthesizer system_prompt name",
  "model": "synthesizer model",
  "revision_number": 1,
  "reviewers": [{"name": "{system_prompt}", "model": "{model}"}],
  "status": "approved|needs_changes|needs_clarification|rejected",
  "summary": "2-3 sentence consolidated summary",
  "needs_clarification": false,
  "clarification_questions": [],
  "acceptance_criteria_verification": {
    "total": 6, "verified": 5, "missing": ["AC-3"],
    "details": [{"ac_id": "AC-1", "status": "IMPLEMENTED", "evidence": "src/auth.ts:42", "notes": ""}]
  },
  "findings": [{all must_fix and advisory findings, deduplicated}],
  "checklist": {
    "security_owasp": "PASS|WARN|FAIL",
    "error_handling": "PASS|WARN|FAIL",
    "resource_management": "PASS|WARN|FAIL",
    "configuration": "PASS|WARN|FAIL",
    "code_quality": "PASS|WARN|FAIL",
    "concurrency": "PASS|WARN|FAIL|N/A",
    "logging": "PASS|WARN|FAIL",
    "dependencies": "PASS|WARN|FAIL",
    "api_design": "PASS|WARN|FAIL|N/A",
    "backward_compatibility": "PASS|WARN|FAIL|N/A",
    "testing": "PASS|WARN|FAIL",
    "over_engineering": "PASS|WARN|FAIL"
  },
  "reviewed_at": "{ISO8601}"
}
```

## Sign-off

```json
{
  "requirements_approved": "{date}",
  "plan_approved": "{date}",
  "implementation_complete": "{date}",
  "code_review_passed": "{date or null}"
}
```
```

**If this is a re-review (revision > 1):** Replace the existing review record section instead of appending a second one.

---

## Step 11: Review → Repair → Re-Review Loop

If aggregate status is `needs_changes` and iterations < max_iterations:

1. Extract `must_fix` findings from the review record
2. **For plan review:** Dispatch `/dev-buddy-plan` via Skill tool (it will read the review findings from the plan file and re-plan)
3. **For code review:** Dispatch `/dev-buddy-implement` via Skill tool (it will read the review findings and fix)
4. After repair completes, increment revision_number
5. Delete the current review temp files
6. Re-dispatch ALL reviewers with new revision_number
7. Return to Step 8

If iterations exhausted → update status to `rejected` in the review record.

---

## Step 12: Cleanup and Report

1. Remove temp files: `rm -f "{TMPDIR}/.vcp/oneshot/review-{RAND}-"*`
2. Present to user:
   - Overall status
   - Number of findings (must_fix vs advisory)
   - AC coverage / verification status
3. If approved, suggest next step:
   - Plan review approved → `/dev-buddy-implement`
   - Code review approved → done

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Required plan file sections missing | Tell user which stage to run first |
| All reviewers fail | Report error to user |
| Single reviewer fails | Continue with remaining |
| Max iterations exceeded | Set status to rejected, report to user |
| Clarification answer in plan file | Resolve without asking user |
