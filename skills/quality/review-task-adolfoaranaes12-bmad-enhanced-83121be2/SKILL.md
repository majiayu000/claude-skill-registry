---
name: review-task
description: Orchestrate comprehensive quality assessment by executing 5 specialized quality skills in sequence and synthesizing results into a unified quality gate decision. This skill should be used when performing final review of completed implementation.
acceptance:
  - all_assessments_completed: "All 5 quality skills executed successfully (risk-profile, test-design, trace-requirements, nfr-assess, quality-gate)"
  - gate_decision_made: "Quality gate decision generated (PASS/CONCERNS/FAIL/WAIVED) with overall quality score"
  - reports_generated: "Assessment reports created in .claude/quality/ (assessments/*.md, gates/*.yaml, gates/*.md)"
  - task_updated: "Task file Quality Review section updated with summary and report links"
inputs:
  task_file:
    type: string
    required: true
    description: "Path to task file in .claude/tasks/{task-id}.md format"
  execution_mode:
    type: enum
    values: ["full", "individual", "resume"]
    default: "full"
    description: "Execution mode: full (all 5 skills), individual (selected skills), resume (continue partial review)"
  selected_skills:
    type: array
    required: false
    description: "For individual mode: which skills to execute (risk-profile, test-design, trace-requirements, nfr-assess, quality-gate)"
outputs:
  gate_decision:
    type: object
    description: "Quality gate decision with status, score, blockers, action items"
  assessment_reports:
    type: object
    description: "File paths to all generated assessment reports"
  review_summary:
    type: string
    description: "Human-readable summary of quality review results"
telemetry:
  emit: "skill.review-task.completed"
  track:
    - task_id
    - execution_mode
    - duration_ms
    - skills_executed
    - gate_decision
    - overall_score
---

# Quality Review Orchestrator

Orchestrate comprehensive quality assessment by executing 5 specialized quality skills in sequence and synthesizing results into a unified quality gate decision.

## Purpose

This skill coordinates execution of 5 specialized quality skills to provide comprehensive quality assessment:

1. **risk-profile** → Assess implementation risks using P×I methodology
2. **test-design** → Design comprehensive test strategy with P0/P1/P2 priorities
3. **trace-requirements** → Map AC → Implementation → Tests with gap analysis
4. **nfr-assess** → Assess non-functional requirements (security, performance, reliability, etc.)
5. **quality-gate** → Synthesize all assessments into final gate decision

## When to Use This Skill

**This skill should be used when:** Comprehensive quality review of completed task (status "Review"), preparing for merge/deploy decision

**Individual assessments:** Invoke specific skills directly (risk-profile, test-design, trace-requirements, nfr-assess, quality-gate)

**This skill should NOT be used when:** Task in progress, reviewing drafts, quick spot checks

## Architecture

```
Quality Review Orchestration Flow:

Step 0: Configuration & Verification
  ↓
Step 1: risk-profile → .claude/quality/assessments/{task-id}-risk-{date}.md
  ↓
Step 2: test-design → .claude/quality/assessments/{task-id}-test-design-{date}.md
  ↓
Step 3: trace-requirements → .claude/quality/assessments/{task-id}-trace-{date}.md
  ↓
Step 4: nfr-assess → .claude/quality/assessments/{task-id}-nfr-{date}.md
  ↓
Step 5: quality-gate → .claude/quality/gates/{task-id}-gate-{date}.{yaml,md}
  ↓
Step 6: Update Task File
  ↓
Step 7: Present Summary
```

Each skill builds on previous results. Execution order is critical.

## File Modification Permissions

**AUTHORIZED:** Read task/implementation files, execute quality skills, generate reports, update task "Quality Review" section only

**NOT AUTHORIZED:** Modify task Objective/AC/Context/Tasks/Implementation, modify code, change status to "Done", bypass skills

## Sequential Orchestration Execution

### Step 0: Configuration and Verification

**Purpose:** Load configuration, verify task readiness, determine execution mode.

**Actions:**
1. Load configuration from `.claude/config.yaml`
2. Verify task file exists, status is "Review", implementation complete
3. Determine execution mode (Full/Individual/Resume)
4. Check existing assessments (for resume mode)

**Halt if:** Config missing, task not ready, status not "Review"

**See:** `references/execution-modes-guide.md` for detailed flow and `references/templates.md` for configuration format

---

### Step 1: Execute Risk Profile Skill

**Purpose:** Assess implementation risks using P×I (Probability × Impact) methodology.

**Actions:**

1. Invoke risk-profile.md skill:
   ```
   Executing: .claude/skills/quality/risk-profile.md
   Task: {task-id}
   ```

2. Skill executes 7-step risk assessment process:
   - Identify risk areas (10-20 risks)
   - Score risks (P×I, scale 1-9)
   - Develop mitigation strategies
   - Prioritize test scenarios
   - Generate risk profile report

3. Capture results: risk count, critical/high risks, mitigation coverage, report path

**Error Handling:** If skill fails, ask user to fix and re-run, or skip and continue (impacts gate confidence).

**See:** `references/templates.md` for output format and captured data structure

---

### Step 2: Execute Test Design Skill

**Purpose:** Design comprehensive test strategy with P0/P1/P2 priorities and mock strategies.

**Actions:**

1. Invoke test-design.md skill:
   ```
   Executing: .claude/skills/quality/test-design.md
   Task: {task-id}
   Risk Profile: {risk-file} (for risk-informed test prioritization)
   ```

2. Skill executes 7-step test design process:
   - Analyze test requirements per AC
   - Design test scenarios (Given-When-Then)
   - Develop mock strategies
   - Plan CI/CD integration
   - Generate test design document

3. Capture results: total tests, P0/P1/P2 counts, test levels, report path

**See:** `references/templates.md` for output format

---

### Step 3: Execute Requirements Traceability Skill

**Purpose:** Map acceptance criteria → implementation → tests with gap analysis.

**Actions:**

1. Invoke trace-requirements.md skill:
   ```
   Executing: .claude/skills/quality/trace-requirements.md
   Task: {task-id}
   Risk Profile: {risk-file}
   Test Design: {test-file}
   ```

2. Skill executes 7-step traceability process:
   - Build forward traceability (AC → Implementation)
   - Build backward traceability (Tests → AC)
   - Identify coverage gaps
   - Create traceability matrix
   - Generate recommendations

3. Capture results: traceability score, implementation/test coverage, gaps, report path

**Error Handling:** Traceability is CRITICAL for quality gate. Must fix and re-run if fails.

**See:** `references/templates.md` for output format

---

### Step 4: Execute NFR Assessment Skill

**Purpose:** Assess non-functional requirements across 6 categories.

**Actions:**

1. Invoke nfr-assess.md skill:
   ```
   Executing: .claude/skills/quality/nfr-assess.md
   Task: {task-id}
   Risk Profile: {risk-file}
   Traceability: {trace-file}
   Test Design: {test-file}
   ```

2. Skill executes 8-step NFR assessment:
   - Security assessment (validation, auth, encryption, vulnerabilities)
   - Performance assessment (response time, queries, caching)
   - Reliability assessment (error handling, logging, monitoring)
   - Maintainability assessment (code quality, docs, coverage)
   - Scalability assessment (stateless, indexing, async processing)
   - Usability assessment (API design, error messages, docs)

3. Capture results: overall NFR score, category scores (security/performance/reliability/maintainability/scalability/usability), critical gaps, report path

**See:** `references/templates.md` for output format

---

### Step 5: Execute Quality Gate Skill

**Purpose:** Synthesize all assessments and make final PASS/CONCERNS/FAIL/WAIVED decision.

**Actions:**

1. Invoke quality-gate.md skill:
   ```
   Executing: .claude/skills/quality/quality-gate.md
   Task: {task-id}
   Risk Profile: {risk-file}
   Test Design: {test-file}
   Traceability: {trace-file}
   NFR Assessment: {nfr-file}
   ```

2. Skill executes 8-step gate synthesis:
   - Synthesize risk management dimension
   - Synthesize test coverage dimension
   - Synthesize traceability dimension
   - Synthesize NFR dimension
   - Synthesize implementation quality dimension
   - Synthesize compliance dimension
   - Calculate overall quality score
   - Make gate decision (PASS/CONCERNS/FAIL/WAIVED)

3. Capture results: gate decision (PASS/CONCERNS/FAIL/WAIVED), overall score, can proceed status, blockers, action items, report paths (YAML + MD)

**Error Handling:** Gate decision is CRITICAL. Must fix and re-run if fails.

**See:** `references/templates.md` for output format

---

### Step 6: Update Task File with Quality Review Summary

**Purpose:** Update task file Quality Review section with synthesized summary.

**Actions:**
1. Generate quality review summary from gate decision
2. Update task file Quality Review section (preserve all other sections)

**See:** `references/templates.md` for task file update template

---

### Step 7: Present Unified Quality Review Summary

**Purpose:** Present comprehensive summary synthesizing all 5 skill results with gate decision, dimension scores, findings, action items, and next steps.

**Actions:**
- Display gate decision and overall score
- Show quality dimension scores (risk, test, trace, NFR, implementation, compliance)
- List critical findings and action items (P0/P1)
- Present generated report links
- Collect user decision (accept/review/address/waive/rerun)

**See:** `references/templates.md` for complete summary template and user decision handling

---

## Execution Complete

Quality review orchestration complete when:

- [x] All 5 skills executed successfully (or skipped intentionally)
- [x] Quality gate decision made
- [x] Gate reports generated (YAML + Markdown)
- [x] Task file Quality Review section updated
- [x] Unified summary presented to user
- [x] User decision collected and actioned

## Best Practices

1. **Run full review when possible** - Most comprehensive assessment
2. **Use individual skills during development** - Faster feedback loops
3. **Re-run specific skills when data changes** - Don't redo entire review
4. **Always start with gate report** - Best overview, links to all details
5. **Track action items in issue system** - Don't lose follow-up work
6. **Document waivers properly** - Include justification, timeline, owner
7. **Automate in CI/CD** - Use gate YAML for automated checks

## References

- `references/execution-modes-guide.md` - Execution flow for full/individual/resume modes
- `references/error-handling-guide.md` - Error scenarios, graceful degradation, fallback strategies
- `references/orchestration-guide.md` - Skill coordination and sequencing details
- `references/synthesis-summary-guide.md` - Summary generation and presentation
- `references/templates.md` - Output templates, task file updates, user decision handling
