---
name: dev-buddy-requirements
description: Gather requirements with TDD test plans, pessimistic impact analysis, and risk registry. Appends Requirements, TDD Test Plan, and Risk Registry sections to the plan file.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TaskOutput, AskUserQuestion, WebSearch
---

# Requirements Stage Skill

Gather requirements, generate TDD test plans, and identify risks through pessimistic-first analysis. All output is appended to the plan file — no separate artifact files.

---

## Step 1: Load Config and Resolve Executors

```bash
bun -e "
import { loadDevBuddyConfig, getProviderType } from '${CLAUDE_PLUGIN_ROOT}/scripts/pipeline-config.ts';
const config = loadDevBuddyConfig();
const stage = config.stages['requirements'];
const executors = stage.executors.map(exec => ({
  ...exec,
  providerType: getProviderType(exec.preset)
}));
console.log(JSON.stringify({ executors }));
"
```

---

## Step 2: Resolve Session Variables

1. Resolve tmpdir:
   ```bash
   bun -e "console.log(require('os').tmpdir())"
   ```
   Store as `{TMPDIR}`.

2. Generate unique output ID:
   ```bash
   bun -e "console.log(require('crypto').randomBytes(4).toString('hex'))"
   ```
   Store as `{RAND}`. Output file for executor at index `{i}`: `{TMPDIR}/.vcp/oneshot/req-{RAND}-{i}.json`

3. Ensure output directory:
   ```bash
   mkdir -p "{TMPDIR}/.vcp/oneshot"
   ```

---

## Step 3: Check for RCA Context

Read the plan file. If it contains a `## RCA Diagnosis` section, this is a bug-fix requirements stage. Extract the root cause summary, affected files, and fix constraints to include as context for the requirements executor.

---

## Step 4: Prompt Assembly

For each requirements executor, construct the task prompt:

```
ORIGINAL REQUEST: {user's original request from conversation}
{If RCA context: "BUG-FIX CONTEXT — RCA Diagnosis from plan file:\nRoot Cause: {summary}\nRoot File: {file}:{line}\nFix Constraints: {constraints}"}
---

You are executing the REQUIREMENTS stage.

PESSIMISTIC-FIRST: Before defining what this feature should do, identify what it will BREAK.
1. Identify every file and integration point this change touches (use Glob/Grep)
2. For each, state the specific breakage scenario with affected file:line
3. List all questions the user must answer about failure modes
4. Generate risks with severity, affected files, and mitigation strategies

Then gather requirements:
1. Clear acceptance criteria (Given/When/Then format) with source field
2. Scope (in_scope / out_of_scope)
3. TDD test plan (unit, e2e, skill tests) mapped to ACs — tests come BEFORE planning
4. Risk registry with severity ratings

DO NOT add features not in the original request. Ask 2-3 clarifying questions max.

Write output to {TMPDIR}/.vcp/oneshot/req-{RAND}-{i}.json

Output JSON format — ALL fields required:
{
  "user_story": { "role": "...", "want": "...", "benefit": "..." },
  "acceptance_criteria": [
    { "id": "AC-1", "scenario": "...", "given": "...", "when": "...", "then": "...", "source": "original_request|user_answer" }
  ],
  "scope": { "in_scope": [...], "out_of_scope": [...], "assumptions": [...] },
  "impact_analysis": {
    "impacts": [
      { "id": "IMP-1", "affected_file": "file.ts", "affected_line": 42, "description": "...", "severity": "HIGH|MED|LOW", "evidence": "file:line — reason", "mitigation": "...", "decision_required": "..." }
    ],
    "questions": [
      { "id": "Q-1", "question": "...", "context": "IMP-1", "user_response": null }
    ]
  },
  "tdd_test_plan": {
    "unit_tests": [
      { "id": "UT-1", "description": "...", "ac_ids": ["AC-1"], "file": "tests/file.test.ts", "command": "npm test -- --grep '...'" }
    ],
    "e2e_tests": [...],
    "skill_tests": [...]
  },
  "risk_registry": [
    { "id": "R-1", "risk": "...", "severity": "HIGH|MED|LOW", "affected_files": ["..."], "mitigation": "...", "user_acknowledged": false }
  ],
  "approved_by": null,
  "approved_at": null,
  "needs_clarification": false,
  "clarification_questions": []
}
```

**Multi-executor (analysts with synthesizer):**
If multiple executors configured:
1. Non-synthesizer executors (all except last): each writes to `{TMPDIR}/.vcp/oneshot/req-{RAND}-{i}.json`
2. Last executor (synthesizer) runs last with augmented prompt to read all prior outputs and write the canonical result

---

## Step 5: Dispatch Executors

**Resolve system prompt with stage/role composition:**
```bash
bun -e "
import { loadStageDefinition, getSystemPrompt, composePrompt } from '${CLAUDE_PLUGIN_ROOT}/scripts/system-prompts.ts';
const stage = loadStageDefinition('requirements', '${CLAUDE_PLUGIN_ROOT}/stages');
const role = getSystemPrompt('{executor.system_prompt}', '${CLAUDE_PLUGIN_ROOT}/system-prompts/built-in');
if (!stage) { console.error('FATAL: Stage definition not found'); process.exit(1); }
if (!role) { console.error('FATAL: Role prompt not found'); process.exit(1); }
console.log(composePrompt(stage, role));
"
```

Route by provider type:
- **subscription:** `Task(subagent_type: "general-purpose", model: "<model>", prompt: "<composed + task prompt>")`
- **api:** `Bash(run_in_background: true)` → `bun "${CLAUDE_PLUGIN_ROOT}/scripts/one-shot-runner.ts" --type api --output-id req-{RAND}-{i} --preset "{PRESET}" --model "{MODEL}" --cwd "${CLAUDE_PROJECT_DIR}" --task-stdin`

---

## Step 6: Collect Results and Handle Clarification

Read executor output from `{TMPDIR}/.vcp/oneshot/req-{RAND}-*.json`.

**For API/CLI executors:** The output file is wrapped in an envelope `{"event":"complete","provider":"...","model":"...","result":"..."}`. Parse the `result` field (which is a JSON string) to get the actual executor output. For subscription executors, the result is returned directly from the Task tool.

Check if executor needs clarification (two possible formats):
- Field-level: executor output has `"needs_clarification": true` with `"clarification_questions": [...]`
- Status-level: executor output is `{"status": "needs_clarification", "clarification_questions": [...]}` (API executors without AskUserQuestion)

If either form detected:
1. Present questions to user via AskUserQuestion
2. Re-dispatch synthesizer with answers appended (max 3 rounds)

Check impact analysis questions:
1. Present each unresolved question to user via AskUserQuestion
2. Record user responses in the impact analysis

Check risk registry:
1. Present each unacknowledged risk to user via AskUserQuestion
2. Record user acknowledgment

---

## Step 7: Append to Plan File

Read the current plan file. Append three sections using the Edit tool.

**If plan file doesn't have a header yet, create it first:**
```markdown
# Plan: {title from user story}
**Status:** requirements
**Pipeline:** {feature|bug-fix}
**Created:** {date}

---
```

**Append `## Requirements` section:**
```markdown
## Requirements

### User Story
**As a** {role}
**I want** {want}
**So that** {benefit}

### Acceptance Criteria
- [ ] **AC-1:** Given {given}, when {when}, then {then} [source: {source}]
- [ ] **AC-2:** Given {given}, when {when}, then {then} [source: {source}]

### Scope
**In scope:** {list}
**Out of scope:** {list}
**Assumptions:** {list}

### Impact Analysis (Pessimistic-First)

```json
{
  "impacts": [{impact objects from executor output}],
  "questions": [{question objects with user_response filled in}]
}
```
```

**Append `## TDD Test Plan` section:**
```markdown
## TDD Test Plan

### Unit Tests
| ID | Description | AC | File | Command |
|----|-------------|-----|------|---------|
| UT-1 | {description} | AC-1 | {file} | {command} |

### E2E Tests
| ID | Description | AC | Command |
|----|-------------|-----|---------|
| E2E-1 | {description} | AC-2 | {command} |

### Skill Tests
| ID | Description | AC | Skill Command |
|----|-------------|-----|---------------|
| SK-1 | {description} | AC-1 | {skill_command} |
```

**Append `## Risk Registry` section:**
```markdown
## Risk Registry

```json
{
  "risks": [{risk objects from executor output, with user_acknowledged updated}]
}
```

**Unacknowledged risks block implementation.**
```

---

## Step 8: Cleanup and Report

1. Remove temp files: `rm -f "{TMPDIR}/.vcp/oneshot/req-{RAND}-"*`
2. Present to the user:
   - Number of acceptance criteria
   - Key scope items
   - Impact analysis summary
   - TDD test plan summary
   - Risk registry status (how many acknowledged)
3. Suggest next step: `/dev-buddy-plan`

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No executors configured | Report error, suggest `/dev-buddy-config` |
| All executors fail | Report error to user |
| Single executor fails | Continue with remaining |
| Clarification exceeded 3 rounds | Escalate to user |
| Plan file doesn't exist | Create with header |
