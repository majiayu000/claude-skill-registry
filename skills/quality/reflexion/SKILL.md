---
name: reflexion
description: Capture significant errors, root causes, and prevention strategies for future reference
argument-hint: [issue description]
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Glob
---

# /reflexion - Error Learning and Prevention

Capture significant issues encountered during development for future reference.

## Purpose

Document errors and their resolutions to:
- Prevent repeating the same mistakes
- Build a knowledge base of solutions
- Enable pattern matching for similar issues
- Improve agent effectiveness over time

## Inputs

- `$ARGUMENTS`: Description of the issue (optional, can be inferred from context)
- `${PROJECT_NAME}`: Current project context
- `${CLAUDE_SESSION_ID}`: Session identifier for linking
- Current conversation context (errors, debugging, resolutions)

## Outputs

Reflexion record stored in Serena project memory under `reflexion/` namespace.

## High Signal/Noise Threshold

Only record issues that are:
- **Significant**: Required meaningful debugging effort
- **Non-Obvious**: The solution wasn't immediately clear
- **Preventable**: Could be avoided in future with the right knowledge
- **Generalizable**: Applies beyond this specific instance

Do NOT record:
- Simple typos or syntax errors
- Issues fixed in seconds
- One-off configuration problems
- Highly project-specific issues with no general lesson

## Workflow

### 1. Identify the Issue
From context or `$ARGUMENTS`:
- What went wrong?
- What was the symptom?
- When did it manifest?

### 2. Analyze Root Cause
- Why did this happen?
- What assumption was incorrect?
- What information was missing?
- Was documentation unclear or absent?

### 3. Document Solution
- What fixed the issue?
- What was the key insight?
- How long did resolution take?

### 4. Define Prevention
- How can this be avoided in future?
- What should be checked first?
- Are there patterns to recognize?
- Should documentation be updated?

### 5. Store Reflexion
Create a reflexion record with the schema below.

## Reflexion Schema

```yaml
# reflexion/YYYY-MM-DD-short-description.md
---
date: YYYY-MM-DD
session_id: ${CLAUDE_SESSION_ID}
agent: [Which agent encountered this]
task: [What task was being performed]
severity: low | medium | high | critical
tags:
  - [category]
  - [technology]
---

## Known Issue
[Clear description of what went wrong]

## Symptoms
- [Observable symptom 1]
- [Observable symptom 2]

## Root Cause
[Why this happened - the underlying issue]

## Solution
1. [Step 1 of the fix]
2. [Step 2 of the fix]
3. [Verification step]

## Prevention
- [How to avoid this in future]
- [What to check first when seeing similar symptoms]
- [Patterns to recognize]

## Related
- [Link to relevant docs]
- [Similar past issues]
```

## Example

```yaml
---
date: 2026-01-24
session_id: abc123
agent: Developer
task: Implement OAuth authentication
severity: high
tags:
  - authentication
  - token-refresh
  - error-handling
---

## Known Issue
Authentication fails silently when refresh token expires during long-running session.

## Symptoms
- Users logged out unexpectedly after ~1 hour
- No error messages displayed
- Network tab showed 401 responses being swallowed

## Root Cause
Token refresh endpoint returns 401 when refresh token is expired, but error handler was catching all 401s and returning a generic "unauthorized" without distinguishing between invalid token and expired refresh token.

## Solution
1. Added explicit check for refresh token expiry in 401 handler
2. Implemented token refresh retry logic with exponential backoff
3. Added user notification prompting re-authentication when refresh fails

## Prevention
- Always handle 401 responses explicitly in auth flows
- Distinguish between token types (access vs refresh) in error handling
- Add logging for token lifecycle events
- Consider health check endpoint for token validity before operations
```

## Validation Checklist
- [ ] Issue is significant (worth recording)
- [ ] Root cause is identified (not just symptoms)
- [ ] Solution is actionable and specific
- [ ] Prevention strategies are generalizable
- [ ] Severity accurately reflects impact
