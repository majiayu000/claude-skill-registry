---
name: validate-plan
description: Run Phase 2 validation with Cursor and Gemini in parallel.
version: 1.1.0
tags: [validation, plan, review]
owner: orchestration
status: active
---

# Validate Plan Skill

Run Phase 2 validation with Cursor and Gemini in parallel.

## Overview

This skill coordinates parallel review of the implementation plan by:
- **Cursor**: Security and code quality focus
- **Gemini**: Architecture and scalability focus

Both agents must approve before proceeding to implementation.

## Prerequisites

- Phase 1 (Planning) completed
- Plan available in `phase_outputs` (type=plan)
- Cursor and Gemini CLIs available

## Execution Steps

### 1. Prepare Validation Storage

Ensure validation outputs will be stored in `phase_outputs` and `logs` (no local directories).

### 2. Read the Plan

```
Read plan from `phase_outputs` (type=plan)
```

### 3. Run Agents in Parallel

Execute BOTH Bash commands simultaneously:

**Cursor Validation**:
```bash
cursor-agent --print --output-format json "
# Plan Validation - Security & Code Quality Review

## Plan to Review
Read: plan JSON provided in this prompt (from phase_outputs export)

## Your Focus Areas
1. **Security Analysis**
   - Identify potential vulnerabilities in proposed changes
   - Check for injection risks (SQL, XSS, command)
   - Evaluate authentication/authorization design
   - Assess data validation approach

2. **Code Quality**
   - Review proposed file structure
   - Check for maintainability concerns
   - Evaluate test coverage plan
   - Identify potential code smells

3. **Risk Assessment**
   - Highlight high-risk changes
   - Suggest additional safeguards

## Output Format
Return JSON:
{
  \"agent\": \"cursor\",
  \"phase\": \"validation\",
  \"approved\": true|false,
  \"score\": 1-10,
  \"assessment\": \"Summary of your review\",
  \"security_findings\": [
    {\"severity\": \"high|medium|low\", \"finding\": \"\", \"recommendation\": \"\"}
  ],
  \"quality_concerns\": [
    {\"area\": \"\", \"concern\": \"\", \"suggestion\": \"\"}
  ],
  \"blocking_issues\": [],
  \"strengths\": []
}
" > cursor-feedback.json
```

**Gemini Validation**:
```bash
gemini --yolo "
# Plan Validation - Architecture & Scalability Review

## Plan to Review
Read: plan JSON provided in this prompt (from phase_outputs export)

## Your Focus Areas
1. **Architecture Review**
   - Evaluate design patterns chosen
   - Check component modularity
   - Assess separation of concerns
   - Review data flow design

2. **Scalability Assessment**
   - Identify potential bottlenecks
   - Evaluate performance implications
   - Check resource utilization patterns

3. **Maintainability**
   - Assess long-term maintenance burden
   - Check for technical debt introduction
   - Review extensibility

## Output Format
Return JSON in a code block:
\`\`\`json
{
  \"agent\": \"gemini\",
  \"phase\": \"validation\",
  \"approved\": true|false,
  \"score\": 1-10,
  \"assessment\": \"Summary of your review\",
  \"architecture_review\": {
    \"patterns\": [{\"pattern\": \"\", \"appropriate\": true|false, \"notes\": \"\"}],
    \"modularity_score\": 1-10,
    \"concerns\": []
  },
  \"scalability_review\": {
    \"bottlenecks\": [],
    \"recommendations\": []
  },
  \"blocking_issues\": [],
  \"strengths\": []
}
\`\`\`
" > gemini-feedback.json
```

### 4. Parse Results

Read both feedback files:
- `phase_outputs` entry `cursor_feedback`
- `phase_outputs` entry `gemini_feedback`

For Gemini, extract JSON from markdown code block if needed.

### 5. Evaluate Approval

**Approval Criteria (Phase 2)**:

| Criterion | Requirement |
|-----------|-------------|
| Cursor Score | >= 6.0 |
| Gemini Score | >= 6.0 |
| Combined Average | >= 6.0 |
| Blocking Issues | None from either agent |

### 6. Handle Conflicts

If agents disagree (one approves, one doesn't):

| Conflict Type | Resolution |
|---------------|------------|
| Security concern | Cursor wins (weight 0.8) |
| Architecture concern | Gemini wins (weight 0.7) |
| Both have blocking | Human escalation required |

Use `/resolve-conflict` skill for complex disagreements.

### 7. Create Consolidated Feedback

Write consolidated output to `phase_outputs` (type=validation_consolidated):

```json
{
  "validation_result": "approved|needs_changes|rejected",
  "cursor": {
    "approved": true,
    "score": 7.5,
    "blocking_issues": []
  },
  "gemini": {
    "approved": true,
    "score": 8.0,
    "blocking_issues": []
  },
  "combined_score": 7.75,
  "all_concerns": [...],
  "resolution": "Both agents approved",
  "proceed_to_implementation": true
}
```

### 8. Update State

**If Approved**:
```json
{
  "current_phase": 3,
  "phase_status": {
    "validation": "completed",
    "implementation": "in_progress"
  },
  "validation_feedback": {
    "cursor": { ... },
    "gemini": { ... }
  }
}
```

**If Not Approved**:
```json
{
  "current_phase": 1,
  "phase_status": {
    "validation": "needs_revision"
  },
  "validation_feedback": { ... },
  "iteration_count": 2
}
```

Return to planning with feedback to address concerns.

## Retry Logic

- Max iterations: 3
- After 3 failed validations: Escalate to human
- Each retry should address previous concerns

## Outputs

| Output Type | Purpose |
|-------------|---------|
| `cursor_feedback` | Raw Cursor response |
| `gemini_feedback` | Raw Gemini response |
| `validation_consolidated` | Merged evaluation |

## Error Handling

### Agent Timeout
- Retry once with doubled timeout
- If still fails: Proceed with available agent
- Log warning in consolidated feedback

### Parse Failure
- Try to extract partial JSON
- If completely unparseable: Treat as soft failure
- Request human review

### Both Agents Fail
- Cannot proceed automatically
- Escalate to human with error details

## Related Skills

- `/plan-feature` - Previous phase (planning)
- `/call-cursor` - Cursor agent details
- `/call-gemini` - Gemini agent details
- `/resolve-conflict` - Conflict resolution
- `/implement-task` - Next phase (implementation)
