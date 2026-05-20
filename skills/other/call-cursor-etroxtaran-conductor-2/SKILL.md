---
name: call-cursor
description: Invoke the Cursor CLI for security-focused plan validation and code review.
version: 1.1.0
tags: [cursor, security, review, validation]
owner: orchestration
status: active
---

# Call Cursor Skill

Wrapper for invoking Cursor agent via CLI for code review and security analysis.

## Overview

Cursor is specialized for:
- Security vulnerability detection
- Code quality assessment
- OWASP Top 10 compliance
- Best practices enforcement

## Prerequisites

- `cursor-agent` CLI installed and accessible on PATH.

## Expertise Weights

| Area | Weight | Description |
|------|--------|-------------|
| Security | 0.8 | SQL injection, XSS, auth issues |
| Code Quality | 0.7 | Style, maintainability, clarity |
| Testing | 0.7 | Coverage, test quality |

## Usage

```
/call-cursor
```

## CLI Invocation

```bash
cursor-agent --print --output-format json "<prompt>"
```

### Flags

| Flag | Purpose |
|------|---------|
| `--print` | Non-interactive mode (required) |
| `--output-format json` | Return structured JSON |
| `--force` | Skip confirmations (optional) |

**IMPORTANT**: The prompt is a POSITIONAL argument at the END, not a flag.

## Standard Prompts

### Plan Validation (Phase 2)

```bash
cursor-agent --print --output-format json "
You are reviewing an implementation plan for security and code quality.

Read the plan JSON provided by the orchestrator (phase_outputs export).

Evaluate for:
1. Security vulnerabilities in proposed changes
2. Potential for injection attacks (SQL, XSS, command)
3. Authentication/authorization concerns
4. Input validation gaps
5. Secure coding practices
6. Test coverage for security scenarios

Return your assessment as JSON:
{
  \"agent\": \"cursor\",
  \"phase\": \"validation\",
  \"approved\": true|false,
  \"score\": 1-10,
  \"assessment\": \"Brief summary of your review\",
  \"concerns\": [
    {
      \"area\": \"security|quality|testing\",
      \"severity\": \"high|medium|low\",
      \"description\": \"Specific concern\",
      \"recommendation\": \"How to address it\"
    }
  ],
  \"blocking_issues\": [\"List of issues that MUST be fixed before proceeding\"],
  \"strengths\": [\"Positive aspects of the plan\"]
}

Be thorough but fair. Only mark as blocking if it's a genuine security risk.
"
```

### Code Review (Phase 4)

```bash
cursor-agent --print --output-format json "
You are performing a security-focused code review of recently implemented changes.

Review the implementation for:
1. OWASP Top 10 vulnerabilities
2. Injection flaws (SQL, NoSQL, OS command, LDAP)
3. Broken authentication/session management
4. Sensitive data exposure
5. XML external entities (XXE)
6. Broken access control
7. Security misconfiguration
8. Cross-site scripting (XSS)
9. Insecure deserialization
10. Using components with known vulnerabilities

Also check:
- Input validation on all external data
- Output encoding
- Error handling (no sensitive info leaked)
- Logging (security events captured)
- Test coverage for security scenarios

Return your assessment as JSON:
{
  \"agent\": \"cursor\",
  \"phase\": \"verification\",
  \"approved\": true|false,
  \"score\": 1-10,
  \"assessment\": \"Brief summary of code review\",
  \"issues\": [
    {
      \"file\": \"path/to/file.py\",
      \"line\": 42,
      \"severity\": \"critical|high|medium|low\",
      \"category\": \"OWASP category or quality issue\",
      \"description\": \"What's wrong\",
      \"recommendation\": \"How to fix it\"
    }
  ],
  \"blocking_issues\": [\"Critical security issues that MUST be fixed\"],
  \"passed_checks\": [\"Security checks that passed\"]
}

Be thorough. Security issues are blocking by default.
"
```

## Outputs

- JSON review payload for validation or verification phases.

## Output Parsing

Cursor returns JSON. Parse with:

```python
import json
result = json.loads(cursor_output)
approved = result.get("approved", False)
score = result.get("score", 0)
blocking = result.get("blocking_issues", [])
```

## Error Handling

### Timeout
- Default timeout: 300 seconds
- On timeout: Retry once with 600 seconds
- If still fails: Log and continue with warning

### Parse Error
- If output is not valid JSON: Extract any JSON block from output
- If no JSON found: Treat as failure, request human review

### Agent Unavailable
- If cursor-agent not installed: Skip with warning
- Log to state.errors
- Continue workflow (Gemini alone is not sufficient for security)

## Integration with Workflow

1. **Phase 2 (Validation)**:
   - Run in parallel with Gemini
   - Store output in `phase_outputs` as `cursor_feedback`
   - Weight: 0.8 for security concerns

2. **Phase 4 (Verification)**:
   - Run in parallel with Gemini
   - Store output in `phase_outputs` as `cursor_review`

## Examples

```bash
cursor-agent --print --output-format json "Review the plan JSON provided in this prompt."
```

## Related Skills

- `/validate` - Plan validation workflow
- `/verify` - Code review workflow
- `/resolve-conflict` - Merge Cursor and Gemini feedback
   - Must approve for workflow to complete

## Approval Thresholds

| Phase | Min Score | Blocking Issues |
|-------|-----------|-----------------|
| Validation | 6.0 | None allowed |
| Verification | 7.0 | None allowed |

## Example Usage

```bash
# From project directory
cd projects/my-app

# Run validation
cursor-agent --print --output-format json "Review the plan JSON provided in this prompt for security..." > cursor-feedback.json

# Check result
cat cursor-feedback.json | jq '.approved, .score'
```

## Conflict Resolution

When Cursor disagrees with Gemini:

| Issue Type | Resolution |
|------------|------------|
| Security concern | Cursor wins (weight 0.8) |
| Architecture concern | Gemini wins (weight 0.7) |
| Code quality | Average scores |
| Both blocking | Human escalation |
