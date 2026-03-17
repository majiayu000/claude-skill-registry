---
name: verify-code
description: Run Phase 4 verification with Cursor and Gemini code review.
version: 1.1.0
tags: [verification, review, security]
owner: orchestration
status: active
---

# Verify Code Skill

Run Phase 4 verification with Cursor and Gemini code review.

## Overview

This skill coordinates parallel code review of the implementation by:
- **Cursor**: Security audit and code quality review
- **Gemini**: Architecture compliance and design review

**BOTH agents must approve** before completing the workflow.

## Prerequisites

- Phase 3 (Implementation) completed
- All tasks marked as "completed"
- Tests passing

## Execution Steps

### 1. Prepare Verification Storage

Ensure verification outputs will be stored in `phase_outputs` and `logs` (no local directories).

### 2. Gather Implementation Summary

Collect information for reviewers:
- List of files created/modified
- Test results summary
- Task completion records

### 3. Run Agents in Parallel

Execute BOTH Bash commands simultaneously:

**Cursor Code Review**:
```bash
cursor-agent --print --output-format json "
# Code Review - Security & Quality Audit

## Implementation Summary
Read: implementation summary from `phase_outputs` (type=implementation_result)

## Files to Review
Review files changed by the implementation (focus on changed files first).

## Your Review Focus

### Security Audit (CRITICAL)
1. **Injection Vulnerabilities**
   - SQL injection
   - Command injection
   - XSS (Cross-site scripting)
   - LDAP injection

2. **Authentication/Authorization**
   - Proper authentication checks
   - Authorization on all endpoints
   - Session management
   - Password handling

3. **Data Protection**
   - Sensitive data encryption
   - PII handling
   - Secure transmission (HTTPS)
   - Proper logging (no secrets)

4. **Input Validation**
   - All user input validated
   - Proper sanitization
   - Type checking
   - Boundary validation

### Code Quality
1. Error handling completeness
2. Resource cleanup (connections, files)
3. Race conditions
4. Null/undefined handling

### Test Coverage
1. Security scenarios tested
2. Edge cases covered
3. Error paths tested

## Output Format
{
  \"agent\": \"cursor\",
  \"phase\": \"verification\",
  \"approved\": true|false,
  \"score\": 1-10,
  \"assessment\": \"Summary\",
  \"security_audit\": {
    \"vulnerabilities_found\": [
      {
        \"severity\": \"critical|high|medium|low\",
        \"type\": \"OWASP category\",
        \"file\": \"path/to/file\",
        \"line\": 42,
        \"description\": \"What's wrong\",
        \"fix\": \"How to fix\"
      }
    ],
    \"passed_checks\": [\"List of passed security checks\"]
  },
  \"quality_issues\": [
    {
      \"file\": \"path\",
      \"line\": 0,
      \"issue\": \"description\",
      \"severity\": \"high|medium|low\"
    }
  ],
  \"blocking_issues\": [\"MUST fix before approval\"],
  \"recommendations\": [\"Nice to have improvements\"]
}

IMPORTANT: Any security vulnerability of severity 'high' or 'critical' is automatically blocking.
" > cursor-review.json
```

**Gemini Code Review**:
```bash
gemini --yolo "
# Code Review - Architecture & Design Audit

## Implementation Summary
Read: implementation summary from `phase_outputs` (type=implementation_result)

## Original Plan
Read: plan from `phase_outputs` (type=plan)

## Your Review Focus

### Architecture Compliance
1. Does implementation match the plan?
2. Are design patterns correctly applied?
3. Is the architecture consistent?

### Design Quality
1. **Separation of Concerns**
   - Single responsibility principle
   - Proper layering
   - Clear boundaries

2. **Modularity**
   - Component independence
   - Clear interfaces
   - Minimal coupling

3. **Extensibility**
   - Easy to extend
   - Open/closed principle
   - No hardcoded assumptions

4. **Maintainability**
   - Code clarity
   - Proper naming
   - Documentation
   - Reasonable complexity

### Performance Considerations
1. Obvious bottlenecks
2. Resource efficiency
3. Scalability concerns

## Output Format
\`\`\`json
{
  \"agent\": \"gemini\",
  \"phase\": \"verification\",
  \"approved\": true|false,
  \"score\": 1-10,
  \"assessment\": \"Summary\",
  \"architecture_compliance\": {
    \"matches_plan\": true|false,
    \"deviations\": [\"List any deviations from plan\"],
    \"justification\": \"If deviations are acceptable, why\"
  },
  \"design_review\": {
    \"patterns_used\": [\"Patterns identified\"],
    \"patterns_misused\": [\"Incorrectly applied patterns\"],
    \"modularity_score\": 1-10,
    \"maintainability_score\": 1-10
  },
  \"issues\": [
    {
      \"file\": \"path\",
      \"concern\": \"description\",
      \"severity\": \"high|medium|low\",
      \"category\": \"architecture|design|performance\"
    }
  ],
  \"blocking_issues\": [\"Critical design flaws\"],
  \"recommendations\": [\"Suggested improvements\"]
}
\`\`\`

Focus on significant issues. Don't block for style preferences.
" > gemini-review.json
```

### 4. Parse Results

Read both review files and parse JSON (extract from code block for Gemini).

### 5. Evaluate Approval

**Approval Criteria (Phase 4 - Stricter)**:

| Criterion | Requirement |
|-----------|-------------|
| Cursor Score | >= 7.0 |
| Gemini Score | >= 7.0 |
| Cursor Approved | **Yes (required)** |
| Gemini Approved | **Yes (required)** |
| Blocking Issues | **None from either** |
| Security Vulnerabilities | **None high/critical** |

**BOTH agents must approve. No exceptions.**

### 6. Handle Non-Approval

If either agent doesn't approve:

1. **Security Issues (Cursor)**:
   - Return to Phase 3
   - Create fix tasks for each vulnerability
   - Re-implement with security focus
   - Re-verify

2. **Architecture Issues (Gemini)**:
   - Evaluate severity
   - Minor: Document as technical debt
   - Major: Return to Phase 3 for refactoring

3. **Both Have Issues**:
   - Prioritize security fixes
   - Then architecture fixes
   - May need planning revision

### 7. Create Consolidated Review

Write consolidated output to `phase_outputs` (type=verification_consolidated):

```json
{
  "verification_result": "approved|needs_fixes|rejected",
  "cursor": {
    "approved": true,
    "score": 8.0,
    "security_vulnerabilities": 0,
    "blocking_issues": []
  },
  "gemini": {
    "approved": true,
    "score": 7.5,
    "architecture_compliant": true,
    "blocking_issues": []
  },
  "combined_score": 7.75,
  "all_issues": [...],
  "proceed_to_completion": true
}
```

### 8. Update State

**If Approved**:
```json
{
  "current_phase": 5,
  "phase_status": {
    "verification": "completed",
    "completion": "in_progress"
  },
  "verification_feedback": {
    "cursor": { ... },
    "gemini": { ... }
  }
}
```

**If Not Approved**:
```json
{
  "current_phase": 3,
  "phase_status": {
    "verification": "needs_fixes"
  },
  "verification_feedback": { ... },
  "fix_tasks": [
    {
      "id": "FIX-1",
      "type": "security",
      "description": "Fix SQL injection in user.py",
      "from_agent": "cursor"
    }
  ]
}
```

## Fix Task Generation

When issues are found, generate fix tasks:

```json
{
  "id": "FIX-{N}",
  "title": "Fix: {issue description}",
  "from_review": "cursor|gemini",
  "severity": "high",
  "files_to_modify": ["affected/file.py"],
  "acceptance_criteria": [
    "Issue resolved",
    "No regression in tests",
    "Re-verification passes"
  ]
}
```

## Retry Limits

- Max verification attempts: 3
- After 3 failures: Human escalation
- Document all attempts in state

## Outputs

- `phase_outputs` entries: `cursor_review`, `gemini_review`, `verification_consolidated`.

## Error Handling

- If one agent fails, proceed with the other and mark the consolidation as partial.
- If both fail, escalate to human review.

## Related Skills

- `/implement-task` - Previous phase
- `/call-cursor` - Cursor agent details
- `/call-gemini` - Gemini agent details
- `/resolve-conflict` - Conflict resolution
- `/orchestrate` - Main workflow
