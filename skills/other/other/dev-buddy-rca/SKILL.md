---
name: dev-buddy-rca
description: Root cause analysis for bugs. Dispatches RCA executors in parallel, consolidates findings, and appends RCA Diagnosis to the plan file.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TaskOutput, AskUserQuestion
---

# RCA Stage Skill

Diagnose a bug by dispatching root cause analysis executors. Consolidates findings and appends the RCA Diagnosis section to the plan file.

---

## Step 1: Load Config and Resolve Executors

```bash
bun -e "
import { loadDevBuddyConfig, getProviderType } from '${CLAUDE_PLUGIN_ROOT}/scripts/pipeline-config.ts';
const config = loadDevBuddyConfig();
const stage = config.stages['rca'];
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

2. Generate unique output IDs:
   ```bash
   bun -e "console.log(require('crypto').randomBytes(4).toString('hex'))"
   ```
   Store as `{RAND}`. Output file for executor at index `{i}`: `{TMPDIR}/.vcp/oneshot/rca-{RAND}-{i}.json`

3. Ensure output directory:
   ```bash
   mkdir -p "{TMPDIR}/.vcp/oneshot"
   ```

---

## Step 3: Prompt Assembly

For each RCA executor:

```
ORIGINAL REQUEST: {user's bug description from conversation}
---

You are executing the ROOT CAUSE ANALYSIS stage.

Diagnose the bug described above. Do NOT fix it — diagnosis only.

PESSIMISTIC-FIRST: Do NOT assume the obvious cause is the root cause.
- Trace the data flow from symptom to source. Cite git blame, stack traces, or log evidence.
- Ask "why" five times. The root cause is rarely where the error message points.
- Every claim must cite file:line. No speculation without code evidence.

Process:
1. Reproduce the bug (if possible)
2. Trace the data flow from symptom to source
3. Identify the root cause with evidence
4. Document affected files and fix constraints

Write output to {TMPDIR}/.vcp/oneshot/rca-{RAND}-{i}.json

Output JSON format (must match stage definition contract):
{
  "id": "rca-YYYYMMDD-HHMMSS",
  "reviewer": "your-model-id",
  "bug_report": {
    "title": "Short bug title",
    "reported_behavior": "What the bug does",
    "expected_behavior": "What should happen",
    "reproduction_steps": ["Step 1", "Step 2"],
    "reproduction_result": "pass|fail|inconclusive",
    "reproduction_output": "Truncated terminal output"
  },
  "root_cause": {
    "summary": "One-sentence root cause",
    "detailed_explanation": "Multi-sentence causal chain",
    "category": "logic_error|race_condition|missing_validation|...",
    "root_file": "path/to/file.ts",
    "root_line": 42,
    "confidence": "high|medium|low"
  },
  "impact_analysis": {
    "affected_files": ["path/to/file1.ts"],
    "affected_functions": ["functionName"],
    "blast_radius": "isolated|module|cross-module|system-wide",
    "regression_risk": "low|medium|high"
  },
  "fix_constraints": {
    "must_preserve": ["Behaviors that must not break"],
    "safe_to_change": ["Areas where changes are safe"],
    "existing_tests": ["path/to/test.ts"]
  },
  "recommended_approach": {
    "strategy": "Brief fix direction (do NOT implement)",
    "estimated_complexity": "trivial|minor|moderate|major"
  }
}
```

---

## Step 4: Dispatch Executors

**Resolve system prompt with stage/role composition:**
```bash
bun -e "
import { loadStageDefinition, getSystemPrompt, composePrompt } from '${CLAUDE_PLUGIN_ROOT}/scripts/system-prompts.ts';
const stage = loadStageDefinition('rca', '${CLAUDE_PLUGIN_ROOT}/stages');
const role = getSystemPrompt('{executor.system_prompt}', '${CLAUDE_PLUGIN_ROOT}/system-prompts/built-in');
if (!stage) { console.error('FATAL: Stage definition not found for rca'); process.exit(1); }
if (!role) { console.error('FATAL: Role prompt not found: {executor.system_prompt}'); process.exit(1); }
console.log(composePrompt(stage, role));
"
```

Route by provider type:
- **subscription:** `Task(subagent_type: "general-purpose", model: "<model>", prompt: "<composed_prompt>\n---\n<assembled RCA prompt>")`
- **api:** `Bash(run_in_background: true)` → `bun "${CLAUDE_PLUGIN_ROOT}/scripts/one-shot-runner.ts" --type api --output-id rca-{RAND}-{i} --preset "{PRESET}" --model "{MODEL}" --cwd "${CLAUDE_PROJECT_DIR}" --task-stdin <<'{DELIM}'`

Group adjacent `parallel: true` executors → dispatch simultaneously. Sequential executors → one at a time.

---

## Step 5: Collect and Consolidate

After all executors complete, read all output files from `{TMPDIR}/.vcp/oneshot/rca-{RAND}-*.json`.

**For API/CLI executors:** The output file is wrapped in an envelope `{"event":"complete","provider":"...","model":"...","result":"..."}`. Parse the `result` field (which is a JSON string) to get the actual executor output. For subscription executors, the result is returned directly from the Task tool.

**If RCAs agree** (same root_file, similar root_cause):
- Use the most detailed diagnosis
- Merge evidence from all

**If RCAs disagree** (different root_file or contradictory causes):
- Present both diagnoses to the user via AskUserQuestion
- Ask: "Two analyses disagree on the root cause. Which is correct?"
- Use the user's choice

---

## Step 6: Append RCA Diagnosis to Plan File

Read the current plan file. If no plan file exists, this is likely the first phase — the plan file header will be created by the orchestrator.

**Append the `## RCA Diagnosis` section to the plan file** using the Edit tool:

```markdown
## RCA Diagnosis

**Root Cause:** {consolidated root_cause.summary}
**Root File:** {root_file}:{root_line}
**Confidence:** {confidence}
**Category:** {category}

**Evidence:**
- {evidence item 1 — with file:line}
- {evidence item 2 — with file:line}

**Affected Files:**
- {file 1}
- {file 2}

**Fix Constraints:**
- {constraint 1}
- {constraint 2}

**Excluded Hypotheses:**
- {hypothesis 1 — ruled out because...}

```json
{
  "root_cause_summary": "{summary}",
  "root_file": "{file}",
  "root_line": {line},
  "confidence": "{high|medium|low}",
  "category": "{category}",
  "affected_files": ["{file1}", "{file2}"],
  "fix_constraints": ["{constraint1}"],
  "sources": ["rca-{RAND}-0", "rca-{RAND}-1"]
}
```
```

---

## Step 7: Cleanup and Report

1. Remove temp files: `rm -f "{TMPDIR}/.vcp/oneshot/rca-{RAND}-"*`
2. Present the diagnosis to the user:
   - Root cause summary
   - Root file and line
   - Confidence level
   - Affected files
3. Suggest next: `/dev-buddy-requirements` (or continue in pipeline automatically)

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No RCA executors configured | Report error, suggest configuring via `/dev-buddy-config` |
| All executors fail | Report error to user — cannot diagnose |
| Single executor fails | Continue with remaining (if any succeeded) |
| Executors disagree | AskUserQuestion — let user choose |
