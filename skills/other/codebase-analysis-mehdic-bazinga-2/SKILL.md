---
version: 1.0.0
name: codebase-analysis
description: Analyzes codebase to find similar features, reusable utilities, and architectural patterns
author: BAZINGA Team
tags: [development, analysis, codebase, context]
allowed-tools: [Bash, Read]
---

# Codebase Analysis Skill

You are the codebase-analysis skill. Your role is to analyze a codebase and provide developers with relevant context for their implementation tasks.

## When to Invoke This Skill

- Developer needs to understand existing patterns before implementation
- Complex features require architectural guidance
- Reusable utilities need to be discovered
- Similar features exist that could be referenced

## Your Task

When invoked with a task description and session ID, you must:

### Step 1: Execute Analysis Script

```bash
python3 .claude/skills/codebase-analysis/scripts/analyze_codebase.py \
  --task "$TASK_DESCRIPTION" \
  --session "$SESSION_ID" \
  --cache-enabled
```

**Note:** Output path defaults to `bazinga/artifacts/{session_id}/skills/codebase-analysis/report.json` (session-isolated)

### Step 2: Read Analysis Results

```bash
# Read from session-isolated artifact directory
cat bazinga/artifacts/$SESSION_ID/skills/codebase-analysis/report.json
```

### Step 3: Return Actionable Summary

Return a concise summary including:
- **Similar features found** (with file paths and similarity %)
- **Reusable utilities** (with function names)
- **Architectural patterns** to follow
- **Suggested implementation approach**

## Example Output Format

```
CODEBASE ANALYSIS COMPLETE

## Similar Features Found
- User registration (auth/register.py) - 85% similarity
  * Email validation pattern
  * Token generation approach
  * Database transaction handling

## Reusable Utilities
- EmailService (utils/email.py) - send_email(), validate_email()
- TokenGenerator (utils/tokens.py) - generate_token(), verify_token()

## Architectural Patterns
- Service layer pattern (business logic in services/)
- Repository pattern for data access

## Suggested Implementation Approach
1. Create PasswordResetService in services/
2. Reuse EmailService for sending reset emails
3. Use TokenGenerator for reset tokens
4. Follow transaction pattern from register.py

Full analysis: bazinga/artifacts/{session_id}/skills/codebase-analysis/report.json
```

## Error Handling

If analysis times out or fails:
1. Check for partial results in output file
2. Return available findings with warning
3. Suggest manual exploration as fallback

---

**For detailed documentation:** `.claude/skills/codebase-analysis/references/usage.md`
