---
name: phase-3-outline
description: Two-track solution outline creation - Simple Track for localized changes, Complex Track for codebase-wide discovery
user-invocable: false
allowed-tools: Read, Glob, Grep, Bash, Task, AskUserQuestion
---

# Phase Outline Skill

**Role**: Two-track workflow skill for creating solution outlines. Routes based on track selection from phase-2-refine.

**Prerequisite**: Request must be refined (phase-2-refine completed) with track field set.

---

## Two-Track Design

| Track | When Used | Approach |
|-------|-----------|----------|
| **Simple** | Localized changes (single_file, single_module, few_files) | Direct deliverable creation from module_mapping |
| **Complex** | Codebase-wide changes (multi_module, codebase_wide) | Load domain skill for discovery/analysis |

**Track determined by**: phase-2-refine (stored in references.toon)

---

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `plan_id` | string | Yes | Plan identifier |

---

## Workflow Overview

```
Step 1: Load Inputs → Step 2: Route by Track → {Simple: Steps 3-5 | Complex: Steps 6-9} → Step 10: Return
```

---

## Step 1: Load Inputs

**Purpose**: Load track, request, compatibility, and context from phase-2-refine output and sinks.

**Note**: This skill receives `track`, `track_reasoning`, `scope_estimate`, `compatibility`, and `compatibility_description` from the phase-2-refine return output. These values are passed as input parameters.

### 1.1 Receive Track from Phase-2-Refine Output

The `track` value (simple | complex) is received from the phase-2-refine return output, not read from references.toon.

**If track not provided in input**, extract from decision.log:
```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  read --plan-id {plan_id} --type decision | grep "(pm-workflow:phase-2-refine) Track:"
```
Parse the output to extract track value from: `(pm-workflow:phase-2-refine) Track: {track} - {reasoning}`

### 1.2 Read Request

Read request (automatically uses clarified_request if available, otherwise body):

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents request read \
  --plan-id {plan_id} \
  --section clarified_request
```

### 1.3 Read Module Mapping

Read from work directory (persisted by phase-2-refine):

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files read \
  --plan-id {plan_id} \
  --file work/module_mapping.toon
```

### 1.4 Read Domains

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references get \
  --plan-id {plan_id} --field domains
```

### 1.5 Receive Compatibility from Phase-2-Refine Output

The `compatibility` and `compatibility_description` values are received from the phase-2-refine return output.

**If compatibility not provided in input**, read from marshal.json:
```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-2-refine get --field compatibility --trace-plan-id {plan_id}
```

Store as `compatibility` and derive `compatibility_description` from the value:
- `breaking` → "Clean-slate approach, no deprecation nor transitionary comments"
- `deprecation` → "Add deprecation markers to old code, provide migration path"
- `smart_and_ask` → "Assess impact and ask user when backward compatibility is uncertain"

### 1.6 Log Context (to work.log - status, not decision)

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[STATUS] (pm-workflow:phase-3-outline) Starting outline: track={track}, domains={domains}, compatibility={compatibility}"
```

---

## Step 2: Route by Track

Based on `track` from Step 1.1:

```
IF track == "simple":
  → Execute Simple Track (Steps 3-5)
ELSE:  # track == "complex"
  → Execute Complex Track (Steps 6-9)
```

---

# Simple Track (Steps 3-5)

For localized changes where targets are already known from module_mapping.

---

## Step 3: Validate Targets

**Purpose**: Verify target files/modules exist and match domain.

### 3.1 Validate Target Files Exist

For each target in module_mapping:

```bash
# For file targets
ls -la {target_path}
```

If target doesn't exist, ERROR: "Target not found: {target}"

### 3.2 Log Validation

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-3-outline) Validated {N} targets in {domain}"
```

---

## Step 4: Create Deliverables

**Purpose**: Direct mapping from module_mapping to deliverables.

### 4.1 Build Deliverables from Module Mapping

For each entry in module_mapping:

1. Determine change_type from request (create, modify, migrate, refactor)
2. Determine execution_mode (automated)
3. Map domain from references.toon
4. Use module from module_mapping

### 4.2 Deliverable Structure

Use template from `pm-workflow:manage-solution-outline/templates/deliverable-template.md`:

```markdown
### {N}. {Action Verb} {Component Type}: {Name}

**Metadata:**
- change_type: {create|modify|migrate|refactor}
- execution_mode: automated
- domain: {domain}
- module: {module}
- depends: none

**Profiles:**
- implementation
- testing (if module has test infrastructure)

**Affected files:**
- `{explicit/path/to/file1}`
- `{explicit/path/to/file2}`

**Change per file:** {What will be created or modified}

**Verification:**
- Command: {verification command}
- Criteria: {success criteria}

**Success Criteria:**
- {Specific criterion 1}
- {Specific criterion 2}
```

### 4.3 Log Deliverable Creation

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-3-outline) Created deliverable for {target}"
```

---

## Step 5: Simple Q-Gate

**Purpose**: Lightweight verification for simple track.

### 5.1 Verify Deliverables

For each deliverable:

1. **Target exists?** - Already validated in Step 3
2. **Deliverable aligns with request intent?** - Compare deliverable scope with request

### 5.2 Log Q-Gate Result

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-3-outline:qgate) Simple: Deliverable {N}: pass"
```

→ **Continue to Step 10** (Write Solution and Return)

---

# Complex Track (Steps 6-9)

For codebase-wide changes requiring discovery and analysis.

---

## Step 6: Resolve Domain Skill

**Purpose**: Find the outline skill for each domain.

### 6.1 Resolve Skill

For each domain in references.toon:

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  resolve-workflow-skill-extension --domain {domain} --type outline --trace-plan-id {plan_id}
```

**Output** (TOON):
```toon
status: success
domain: {domain}
type: outline
extension: pm-plugin-development:ext-outline-plugin  # or null if no extension
```

### 6.2 Log Resolution

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-3-outline) Resolved skill: {skill_notation}"
```

**If no skill found**: Use generic module-based workflow (see "Generic Workflow" section below).

---

## Step 7: Load Domain Skill

**Purpose**: Load the resolved outline skill to handle discovery, analysis, and deliverable creation.

### 7.1 Load Skill

```
Skill: {resolved_skill_notation}
  Input:
    plan_id: {plan_id}
```

The skill handles the complete Complex Track workflow internally:
- Discovery (using domain-specific scripts)
- Analysis (spawning sub-agents if needed via Task tool)
- Persist assessments → assessments.jsonl
- Confirm uncertainties with user
- Group into deliverables
- Write solution_outline.md (must include `compatibility: {value} — {description}` in header metadata, read from references.toon)

### 7.2 Log Skill Load

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-3-outline) Loaded {skill} for {domain}"
```

---

## Step 8: Skill Completion

**Purpose**: Skill returns minimal status; data is in sinks.

### 8.1 Skill Return Value

```toon
status: success
plan_id: {plan_id}
deliverable_count: {N}
```

### 8.2 Log Skill Completion

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-3-outline) Skill complete: {deliverable_count} deliverables"
```

**If skill returns error**: HALT and return error.

---

## Step 9: Q-Gate Verification

**Purpose**: Verify skill output meets quality standards.

### 9.1 Spawn Q-Gate Agent

```
Task: pm-workflow:q-gate-validation-agent
  Input:
    plan_id: {plan_id}
```

**Q-Gate reads from**:
- `solution_outline.md` (written by domain skill)
- `artifacts/assessments.jsonl` (written by domain skill)
- `request.md` (clarified_request or body)

**Q-Gate verifies**:
- Each deliverable fulfills request intent
- Deliverables respect architecture constraints
- No false positives (files that shouldn't be changed)
- No missing coverage (files that should be changed but aren't)

**Q-Gate writes**:
- `artifacts/findings.jsonl` - Any triage findings
- `logs/decision.log` - Q-Gate verification results

### 9.2 Q-Gate Return Value

```toon
status: success
plan_id: {plan_id}
deliverables_verified: {N}
passed: {count}
flagged: {count}
```

### 9.3 Log Q-Gate Result

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-3-outline:qgate) Full: {passed} passed, {flagged} flagged"
```

### 9.4 Handle Q-Gate Corrections (if flagged > 0)

If Q-Gate flagged false positives or missing coverage:

1. **Update solution_outline.md** with corrections using `--force`:

```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline write \
  --plan-id {plan_id} --force <<'EOF'
{corrected solution document}
EOF
```

2. **Update references** (e.g., remove false positives from modified_files):

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references set-list \
  --plan-id {plan_id} --field modified_files --values "{corrected file list}"
```

3. **Log the correction**:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[ARTIFACT] (pm-workflow:phase-3-outline) Updated solution_outline.md - {correction reason}"
```

→ **Continue to Step 10**

---

# Generic Workflow (No Domain Skill)

For domains without outline skills (e.g., Java, frontend), use module-based workflow.

---

## Generic Step A: Read Module Mapping

Module mapping from phase-2-refine specifies target modules.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references get \
  --plan-id {plan_id} --field module_mapping
```

---

## Generic Step B: Create Deliverables per Module

For each module in module_mapping:

1. Create deliverable with appropriate profile
2. No discovery needed - modules already identified in phase-2-refine

### Check Module Test Infrastructure

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture modules \
  --command module-tests \
  --trace-plan-id {plan_id}
```

Use result to determine if `testing` profile applies.

### Deliverable Structure

Use same template as Simple Track (Step 4.2).

---

## Generic Step C: Write Solution Outline

```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline write \
  --plan-id {plan_id} <<'EOF'
{solution document with deliverables}
EOF
```

---

## Generic Step D: Log Completion

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-3-outline) Generic workflow: {N} deliverables"
```

→ **Continue to Step 10**

---

# Step 10: Write Solution and Return

---

## Step 10.1: Write Solution Document (Simple Track only)

For Simple Track, write solution_outline.md:

```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline write \
  --plan-id {plan_id} <<'EOF'
# Solution: {title}

plan_id: {plan_id}
compatibility: {compatibility} — {compatibility_description}

## Summary

{2-3 sentence summary of the solution}

## Overview

{ASCII diagram showing solution structure}

## Deliverables

{deliverables from Step 4}
EOF
```

**Note**: Complex Track - skill already wrote solution_outline.md in Step 7.

---

## Step 10.2: Log Completion

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[ARTIFACT] (pm-workflow:phase-3-outline) Created solution_outline.md"
```

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-3-outline) Complete: {N} deliverables, Q-Gate: {pass/fail}"
```

---

## Step 10.3: Return Results

Return minimal status - all data is in sinks:

```toon
status: success
plan_id: {plan_id}
track: {simple|complex}
deliverable_count: {N}
qgate_passed: {true|false}
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Track not set | Return `{status: error, message: "phase-2-refine incomplete - track not set"}` |
| Target not found (Simple) | Return error with invalid target |
| Skill not found (Complex) | Fall back to Generic Workflow |
| Skill fails (Complex) | Return error, do not fall back |
| Q-Gate fails | Return with `qgate_passed: false` and findings |
| Request not found | Return `{status: error, message: "Request not found"}` |

**CRITICAL**: If Complex Track skill fails, do NOT fall back to grep/search. Fail clearly.

---

## Integration

**Invoked by**: `pm-workflow:solution-outline-agent` (thin agent)

**Script Notations** (use EXACTLY as shown):
- `pm-workflow:manage-files:manage-files` - Read module_mapping from work/module_mapping.toon
- `pm-workflow:manage-plan-documents:manage-plan-documents` - Read request
- `pm-workflow:manage-references:manage-references` - Read domains
- `pm-workflow:manage-solution-outline:manage-solution-outline` - Write solution document
- `plan-marshall:manage-plan-marshall-config:plan-marshall-config` - Resolve domain skill, read compatibility (fallback)
- `plan-marshall:manage-logging:manage-log` - Decision and work logging

**Loads** (Complex Track):
- Domain outline skill (e.g., `pm-plugin-development:ext-outline-plugin`)

**Spawns** (Complex Track):
- `pm-workflow:q-gate-validation-agent` (Q-Gate verification)

**Consumed By**:
- `pm-workflow:phase-4-plan` skill (reads deliverables for task creation)

---

## Related Documents

- [outline-extension.md](../../workflow-extension-api/standards/extensions/outline-extension.md) - Skill-based extension contract
- [deliverable-contract.md](../../manage-solution-outline/standards/deliverable-contract.md) - Deliverable structure
- [workflow-architecture](../../workflow-architecture) - Workflow architecture overview
