---
name: peer-review
description: Coordinate cross-agent code reviews between Gemini and Codex to catch blind spots. The lead engineer verifies findings rather than accepting blindly.
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Peer Review Skill

## Purpose

Enable cross-agent code reviews where Gemini and Codex review each other's work to catch blind spots, with Claude Code (Lead Engineer) verifying all findings before acting on them.

## Why Peer Review Matters

Different models have different blind spots:
- Fresh eyes catch issues the original author missed
- Cross-domain review (frontend ↔ backend) reveals integration issues
- Verification step prevents false positives and wasted work

## Workflow

### Step 1: Identify Review Opportunity

**When to trigger peer review:**
- After significant implementation (new feature, refactor)
- Before merging complex changes
- When code touches critical systems (auth, payments, data model)
- When user explicitly requests review

**Examples:**
- Gemini implemented frontend → Codex reviews it
- Codex implemented backend → Gemini reviews it

### Step 2: Assign Review

As Claude Code (Lead Engineer), assign the review:

```
"[Agent name], please review [other agent]'s work in [files/directories].

Use the Code Review Checklist from CLAUDE.md and provide findings with:
- Severity levels (CRITICAL, HIGH, MEDIUM, LOW)
- File:line references
- Specific fix recommendations

Focus on:
[Specific areas to review, e.g., "auth checks", "bandwidth optimization", "error handling"]"
```

### Step 3: Reviewer Conducts Review

The reviewing agent should:

1. **Read the code** (not trust documentation)
2. **Apply Code Review Checklist** from CLAUDE.md:
   - Security & Auth
   - Performance & Bandwidth
   - TypeScript & Type Safety
   - Code Quality
   - React/Frontend (if applicable)
   - Production Readiness

3. **Provide structured findings:**

```markdown
### ✅ Looks Good
- Authentication properly implemented
- TypeScript types well-defined
- Follows bandwidth optimization patterns

### ⚠️ Issues Found
- **CRITICAL** [convex/mutations.ts:45](convex/mutations.ts:45) - Missing auth check in updateRFP
  - Fix: Add `const identity = await ctx.auth.getUserIdentity()` guard
- **HIGH** [services/api.ts:120](services/api.ts:120) - Using .collect() without limit
  - Fix: Replace with `.take(100)` or use stats aggregation
- **MEDIUM** [components/Card.tsx:30](components/Card.tsx:30) - Expensive filter in render
  - Fix: Move to useMemo

### 📊 Summary
- Files reviewed: 5
- Critical issues: 1
- High priority: 1
- Medium priority: 1
- Low priority: 0
```

### Step 4: Verify Findings (Lead Engineer)

**⚠️ CRITICAL: You (Claude Code) must verify each finding.**

The reviewer has less context than you. Don't accept findings at face value.

For each finding:

1. **Read the relevant code** - Does this issue actually exist?
2. **Check if it's a real problem** - Or is it a misunderstanding?
3. **Assess severity** - Is the severity level correct?

**Mark each finding as:**
- ✅ **Valid** - Issue exists and should be fixed
- ❌ **Invalid** - Not an issue, explain why
- 🔄 **Debatable** - Ask original implementer for context

### Step 5: Provide Consolidated Feedback

After verification, provide feedback to the original implementer:

```markdown
## Peer Review Results

[Agent name] reviewed your work. Here are the validated findings:

### Valid Issues to Address

1. **CRITICAL** [file.ts:line] - [Issue]
   - Fix: [Recommendation]
   - Rationale: [Why this matters]

2. **HIGH** [file.ts:line] - [Issue]
   - Fix: [Recommendation]

### Findings Reviewed (Not Issues)

- "Should use Promise.all instead of await loop" - Sequential is correct here due to rate limiting
- "Missing error handling" - Already handled by Convex runtime

### Next Steps

Please address the valid findings and re-submit.
```

## Example Exchange

```
User: "Codex just added the SAM.gov ingestion feature"

Claude Code: "Gemini, please review Codex's work in convex/ingestion/samGov.ts.

Focus on:
- Error handling for API failures
- Rate limiting implementation
- TypeScript types for API responses
- Bandwidth optimization patterns"

[Gemini reviews and returns 5 findings]

Claude Code: [Reads the actual code and verifies each finding]

Findings verification:
1. "Missing error handling for API timeout" ✅ Valid
2. "Should use Promise.all instead of await loop" ❌ Invalid - Sequential is correct due to rate limiting
3. "Hardcoded API key" ✅ Valid, CRITICAL
4. "Type `any` used for response" ✅ Valid, HIGH
5. "No retry logic" 🔄 Debatable - Let me ask Codex

Claude Code to Codex: "Peer review found 3 valid issues:

1. **CRITICAL** [samGov.ts:45] - API key is hardcoded
   - Fix: Move to environment variable or Convex secrets

2. **HIGH** [samGov.ts:120] - Response typed as `any`
   - Fix: Create proper interface for SAM.gov API response

3. **DEBATABLE** [samGov.ts:88] - No retry logic for API failures
   - Question: Should we implement retry, or is fail-fast acceptable here?

Please address items 1-2 and clarify item 3."
```

## Red Flags to Watch For

### Invalid Findings (Common False Positives)

- **"This could be simplified"** without clear benefit
- **"Should use pattern X"** when existing pattern is project standard
- **"Missing optimization"** for code that isn't a bottleneck
- **"Needs more error handling"** when current handling is sufficient

### Valid Findings (Don't Dismiss These)

- **Security issues** (auth bypass, injection vulnerabilities)
- **Data loss risks** (missing validation, race conditions)
- **Bandwidth violations** (unbounded queries, missing limits)
- **Type safety violations** (`any` types, missing null checks)

## Anti-Patterns to Avoid

❌ **Accepting all findings without verification**
- Results in wasted work on non-issues

❌ **Dismissing findings defensively**
- Defeats the purpose of fresh eyes

❌ **Turning review into architecture debate**
- Focus on code quality, not design preferences

✅ **Verify, prioritize, consolidate**
- Check if issue exists → assess severity → provide clear feedback

## Invocation

The user invokes this skill by typing `/peer-review` when they want to coordinate a cross-agent review.

**Usage:**
```
/peer-review [files-or-directories] [reviewer-agent]
```

**Examples:**
```
/peer-review convex/ingestion/samGov.ts Gemini
/peer-review components/AdminView.tsx Codex
/peer-review convex/ Gemini
```

If no reviewer specified, Claude Code will assign the appropriate agent based on domain (frontend vs backend).

## Notes

- **Always verify findings** - The reviewer might not have full context
- **Be specific in feedback** - File:line references, not vague comments
- **Prioritize by severity** - CRITICAL must be fixed, LOW is optional
- **This is collaborative, not combative** - Goal is better code, not proving someone wrong
