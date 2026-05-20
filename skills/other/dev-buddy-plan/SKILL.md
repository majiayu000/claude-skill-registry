---
name: dev-buddy-plan
description: Create granular implementation plan from requirements in the plan file. Reads Requirements + TDD Test Plan sections, dispatches planners, appends Implementation Steps to plan file.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TaskOutput, AskUserQuestion
---

# Planning Stage Skill

Create a granular, TDD-mapped implementation plan from existing requirements. Reads Requirements and TDD Test Plan sections from the plan file, dispatches planning executors, and appends Implementation Steps to the plan file.

---

## Step 1: Validate Inputs

Read the plan file and verify it contains:
- `## Requirements` section with acceptance criteria
- `## TDD Test Plan` section with test IDs mapped to ACs
- `## Risk Registry` section

If any section is missing, tell the user to run `/dev-buddy-requirements` first.

**If this is a re-plan after review failure:** Check if the plan file already has a `## Plan Review Record` section with `"status": "needs_changes"` in its fenced JSON block. If so, read the `must_fix` findings from the review record and inject them into the planning prompt.

---

## Step 2: Load Config and Resolve Executors

```bash
bun -e "
import { loadDevBuddyConfig, getProviderType } from '${CLAUDE_PLUGIN_ROOT}/scripts/pipeline-config.ts';
const config = loadDevBuddyConfig();
const stage = config.stages['planning'];
const executors = stage.executors.map(exec => ({
  ...exec,
  providerType: getProviderType(exec.preset)
}));
console.log(JSON.stringify({ executors }));
"
```

---

## Step 3: Resolve Session Variables

1. Resolve tmpdir and generate unique output ID (same pattern as RCA skill)
2. Output file for executor at index `{i}`: `{TMPDIR}/.vcp/oneshot/plan-{RAND}-{i}.json`
3. Ensure output directory exists

---

## Step 4: Extract Context from Plan File

Read the plan file and extract:
1. All acceptance criteria (AC IDs, given/when/then)
2. All test IDs from TDD Test Plan (unit, e2e, skill tests) with their AC mappings
3. Impact analysis (what could break)
4. Risk registry (acknowledged risks)
5. RCA diagnosis (if bug-fix pipeline)
6. Review findings to fix (if re-plan after review failure)

---

## Step 5: Prompt Assembly

For each planning executor:

```
You are executing the PLANNING stage.

REQUIREMENTS (from plan file):
{extracted acceptance criteria}

TDD TEST PLAN (tests already defined — your steps must MAP to these):
{extracted test IDs with AC mappings}

IMPACT ANALYSIS:
{extracted impacts}

RISK REGISTRY:
{extracted risks}

{If re-plan: "REVIEW FINDINGS TO ADDRESS:\n{must_fix findings from review record}"}

---

PESSIMISTIC-FIRST PLANNING:
- Assume every feature you design WILL become a maintenance liability
- For each step: Why could this become technical debt? How do you prevent it?
- Search the codebase FIRST — reuse existing code, do NOT create new abstractions unless justified
- Document what you searched and why new code is necessary (if it is)

GRANULAR AGILE UNITS:
- Each step must be ONE architectural unit (single module/function/component)
- Each step must map to at least one AC and one test ID
- Each step must have a specific rollback procedure
- Each step must be implementable without design decisions from the implementer
- If a step needs more than ~50 lines of changes, split it

Write output to {TMPDIR}/.vcp/oneshot/plan-{RAND}-{i}.json

Output JSON format — ALL fields required:
{
  "id": "plan-YYYYMMDD-HHMMSS",
  "title": "Implementation plan title",
  "summary": "2-3 sentence overview",
  "technical_approach": {
    "pattern": "...",
    "rationale": "...",
    "alternatives_considered": [{"approach": "...", "rejected_because": "..."}],
    "existing_code_reused": [{"file": "...", "function": "...", "purpose": "..."}]
  },
  "steps": [
    {
      "id": 1,
      "title": "Short step title",
      "description": "Detailed instruction — what to do and why",
      "ac_ids": ["AC-1"],
      "test_ids": ["UT-1", "SK-1"],
      "files_to_modify": ["path/to/file.ts"],
      "files_to_create": [],
      "existing_code_to_reuse": ["src/utils/validate.ts:validateInput"],
      "rollback": "Specific undo procedure",
      "debt_risk": "Why this step won't become technical debt",
      "dependencies": []
    }
  ],
  "files_to_modify": ["..."],
  "files_to_create": ["..."],
  "needs_clarification": false,
  "clarification_questions": []
}
```

**Multi-executor:** Same pattern as requirements — non-synthesizers write analysis files, synthesizer reads all and writes canonical output.

---

## Step 6: Dispatch Executors

**Resolve system prompt with stage/role composition:**
```bash
bun -e "
import { loadStageDefinition, getSystemPrompt, composePrompt } from '${CLAUDE_PLUGIN_ROOT}/scripts/system-prompts.ts';
const stage = loadStageDefinition('planning', '${CLAUDE_PLUGIN_ROOT}/stages');
const role = getSystemPrompt('{executor.system_prompt}', '${CLAUDE_PLUGIN_ROOT}/system-prompts/built-in');
if (!stage) { console.error('FATAL: Stage definition not found'); process.exit(1); }
if (!role) { console.error('FATAL: Role prompt not found'); process.exit(1); }
console.log(composePrompt(stage, role));
"
```

Route by provider type:
- **subscription:** `Task(subagent_type: "general-purpose", model: "<model>", prompt: "<composed + task prompt>")`
- **api:** `Bash(run_in_background: true)` → `bun "${CLAUDE_PLUGIN_ROOT}/scripts/one-shot-runner.ts" --type api --output-id plan-{RAND}-{i} --preset "{PRESET}" --model "{MODEL}" --cwd "${CLAUDE_PROJECT_DIR}" --task-stdin`

---

## Step 7: Collect Results and Handle Clarification

Read executor output from `{TMPDIR}/.vcp/oneshot/plan-{RAND}-*.json`.

**For API/CLI executors:** The output file is wrapped in an envelope `{"event":"complete","provider":"...","model":"...","result":"..."}`. Parse the `result` field (which is a JSON string) to get the actual planner output. For subscription executors, the result is returned directly from the Task tool.

Check if executor needs clarification (two possible formats):
- Field-level: executor output has `"needs_clarification": true` with `"clarification_questions": [...]`
- Status-level: executor output is `{"status": "needs_clarification", "clarification_questions": [...]}` (API executors without AskUserQuestion)

If either form detected:
1. Present questions to user via AskUserQuestion
2. Re-dispatch synthesizer with answers (max 3 rounds)

---

## Step 8: Validate Plan Quality

Before appending to plan file, validate:
1. Every step has `ac_ids[]` — no speculative steps
2. Every step has `test_ids[]` — no untestable steps
3. Every step has a specific `rollback` (not "revert changes")
4. Every step has `debt_risk` explanation
5. Every AC from requirements is covered by at least one step
6. Every test ID from TDD Test Plan is covered by at least one step

If validation fails, present the gaps and ask the planner to fix them (re-dispatch with feedback).

---

## Step 9: Append to Plan File

Update the plan file status to `planning`, then append the Implementation Steps section using Edit tool:

```markdown
## Implementation Steps

**Technical Approach:** {pattern} — {rationale}
**Alternatives Considered:** {list}
**Existing Code Reused:** {list}

### Step 1: {title}
**AC:** {ac_ids} | **Tests:** {test_ids}
**Files:** {files_to_modify + files_to_create}
**What to do:** {description}
**Reuses:** {existing_code_to_reuse}
**Rollback:** {rollback}
**Debt Risk:** {debt_risk}
**Dependencies:** {dependency step numbers, or "none"}
**Status:** [ ] not started

### Step 2: {title}
**AC:** {ac_ids} | **Tests:** {test_ids}
**Files:** {files}
**What to do:** {description}
**Reuses:** {existing_code_to_reuse}
**Rollback:** {rollback}
**Debt Risk:** {debt_risk}
**Dependencies:** {dependency step numbers, or "none"}
**Status:** [ ] not started

{...repeat for all steps...}
```

**If this is a re-plan (review repair):** Replace the existing `## Implementation Steps` section with the new one instead of appending.

---

## Step 10: Cleanup and Report

1. Remove temp files: `rm -f "{TMPDIR}/.vcp/oneshot/plan-{RAND}-"*`
2. Present to user:
   - Number of steps
   - AC coverage (which ACs are covered by which steps)
   - Test coverage (which tests map to which steps)
   - Existing code being reused
3. Suggest next step: `/dev-buddy-review --plan`

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No planners configured | Report error, suggest `/dev-buddy-config` |
| Requirements section missing | Tell user to run `/dev-buddy-requirements` first |
| All executors fail | Report error to user |
| Step has no AC mapping | Validation failure — re-dispatch planner with feedback |
| Step has no test mapping | Validation failure — re-dispatch planner with feedback |
