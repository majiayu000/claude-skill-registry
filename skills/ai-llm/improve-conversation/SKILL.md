---
name: improve-conversation
description: Analyze conversations to identify improvements for prompts, instructions, skills, or workflows. Use when something went wrong, behavior didn't match expectations, you want to improve AI interactions, or when the user says "improve", "improve chat", or "/improve".
---

# Conversation Improvement Skill

Quick-trigger skill for analyzing conversations and improving AI behavior. This skill provides a streamlined version of the conversation-improver agent for immediate feedback and fixes.

## When This Activates

This skill auto-activates when you:
- Say "improve", "improve chat", or "/improve"
- Ask about what went wrong
- Want to analyze conversation issues
- Need to fix AI behavior problems
- Ask for retrospective analysis

## Quick Improvement Process

### 1. Identify the Issue (Ask if unclear)

**Quick questions:**
- What specific action didn't match your expectations?
- What should have happened instead?
- Is this recurring or one-time?
- Should the fix apply broadly or in specific contexts?

### 2. Analyze Root Cause

Quickly identify:
- **Scope Creep** - Did extra work
- **Wrong Interpretation** - Misunderstood request
- **Missing Guardrail** - No rule to prevent this
- **Over-Caution** - Too many questions
- **Under-Caution** - Acted without confirmation
- **Tool Misuse** - Wrong tool choice

### 3. Propose Fix

Target the right location:
- **Skill** → Domain-specific behavior (`.github/skills/`)
- **Custom Instructions** → Project-wide rules (`.github/copilot-instructions.md`)
- **Agent** → Workflow-specific (`.github/agents/`)

### 4. Present Solution

```markdown
## Improvement Analysis

**Issue**: [What went wrong]
**Root Cause**: [Why it happened]
**Proposed Fix**: [Where and what to change]

### Target File
[Path to file that needs updating]

### Change
```
[Exact text to add/replace]
```

### Risk
Low/Medium/High - [Why]
```

## Quality Checks

Before proposing changes, verify:
- ✓ **Specific** enough to prevent the issue?
- ✓ **General** enough for future cases?
- ✓ **No conflicts** with existing rules?
- ✓ **Testable** - can user verify?
- ✓ **Minimal** - smallest change?

## Output Options

Based on user preference:
1. **Analysis Only** - Report without changes
2. **Proposed Patch** - Show changes for approval
3. **Apply Changes** - Make changes and summarize

## Anti-Patterns to Avoid

- ❌ Shotgun fixes (multiple files for one issue)
- ❌ Over-specification (too narrow rules)
- ❌ Vague language ("be careful", "consider")
- ❌ Rule duplication (same rule in multiple places)

## Example Usage

**User**: "improve - you kept refactoring files I didn't ask you to touch"

**Response**:
```markdown
### Issue: Scope Creep
AI modified files outside the requested scope.

### Root Cause
Instructions allow "fixing issues in vicinity" but "vicinity" is subjective.

### Proposed Fix
**Target**: `.github/copilot-instructions.md`

Add this rule:
> Only modify files explicitly mentioned in the request.
> Fix critical issues ONLY if they cause build/test failures.
> "Vicinity" means same function—never other files.

**Risk**: Low - Narrows behavior without blocking legitimate fixes.

Would you like me to apply this change?
```

## For More Complex Analysis

For deeper investigation or complex issues, invoke the full **conversation-improver agent**:
```
/agent
> Select: conversation-improver
```

This provides comprehensive root cause analysis with full validation checks.

## Remember

- Focus on patterns, not individual mistakes
- Prefer minimal, surgical changes
- Get user confirmation before applying
- Document why the change helps
