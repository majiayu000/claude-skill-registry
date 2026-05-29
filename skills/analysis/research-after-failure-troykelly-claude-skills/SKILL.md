---
name: research-after-failure
description: Use after 2 consecutive failed attempts at solving a problem - STOP guessing and research documentation, codebase, and online resources before resuming
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
model: opus
---

# Research After Failure

## Overview

After 2 failed attempts, stop and research. Don't keep trying the same thing.

**Core principle:** Insanity is doing the same thing and expecting different results.

**Trigger:** Two consecutive failed attempts at solving a problem.

**Announce at start:** "I've failed twice. I'm stopping to research before trying again."

## The Rule

```
Attempt 1: Try solution
            │
            ▼
         Failed?
            │
     ┌──────┴──────┐
     │             │
    Yes           No → Done
     │
     ▼
Attempt 2: Try different approach
            │
            ▼
         Failed?
            │
     ┌──────┴──────┐
     │             │
    Yes           No → Done
     │
     ▼
    STOP
     │
     ▼
  RESEARCH ← You are here
     │
     ▼
Attempt 3: Try with new knowledge
```

## What Counts as a Failure

| Failure | Not a Failure |
|---------|---------------|
| Tests don't pass | Minor syntax error fixed |
| Build breaks | Typo corrected |
| Feature doesn't work | IDE autocomplete issue |
| Same error recurs | Different error (progress) |
| No progress made | Partial progress |

## The Research Protocol

### Step 1: Document the Failures

Before researching, document what was tried:

```markdown
## Failed Attempts

### Attempt 1
**Approach:** [What was tried]
**Result:** [What happened]
**Error:** [Error message if any]

### Attempt 2
**Approach:** [What was tried]
**Result:** [What happened]
**Error:** [Error message if any]

### Pattern
[What do these failures have in common?]
```

### Step 2: Research Repository Documentation

```bash
# Check README
cat README.md

# Check docs directory
ls -la docs/
cat docs/[relevant-topic].md

# Check CONTRIBUTING
cat CONTRIBUTING.md

# Search for relevant docs
grep -r "[keyword]" docs/
```

**Questions to answer:**
- Is there documented guidance for this?
- Are there examples of similar work?
- Are there known issues or limitations?

### Step 3: Research Existing Codebase

```bash
# Find similar patterns
grep -r "[pattern]" src/

# Find how others solved similar problems
git log --all --oneline --grep="[keyword]"

# Look at test files for usage examples
grep -r "[function/class]" **/*.test.ts
```

**Questions to answer:**
- How does existing code handle this?
- What patterns are established?
- Are there utility functions I'm missing?

### Step 4: Research Online

Use web search for:

1. **Error messages** - Exact error text
2. **Library documentation** - Official docs
3. **Stack Overflow** - Similar problems
4. **GitHub Issues** - Known bugs

```markdown
Search queries to try:
- "[exact error message]"
- "[library name] [problem description]"
- "[framework] [what you're trying to do]"
```

### Step 5: Synthesize Findings

```markdown
## Research Findings

### From Repository Docs
- [Finding 1]
- [Finding 2]

### From Codebase
- [Pattern found]
- [Example found]

### From Online
- [Solution found]
- [Workaround found]

### New Approach
Based on research, the new approach is:
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

### Step 6: Update Issue

Post research findings to the issue:

```bash
gh issue comment [ISSUE_NUMBER] --body "## Research After Failed Attempts

### What Was Tried
1. [Attempt 1]
2. [Attempt 2]

### Research Findings
[Summary of findings]

### New Approach
[How this will be solved now]
"
```

### Step 7: Resume with New Knowledge

Apply findings to the next attempt.

If third attempt also fails → Consider escalating to human.

## When to Escalate

After research + third attempt, if still failing:

```markdown
## Escalation: Need Human Input

**Issue:** #[NUMBER]

**Attempted:**
1. [Approach 1] - [Result]
2. [Approach 2] - [Result]
3. [Approach 3 after research] - [Result]

**Researched:**
- [Sources checked]
- [Findings]

**Current Understanding:**
[What we know now]

**Blocking Question:**
[Specific question that needs human insight]
```

Mark issue as Blocked and await response.

## Research Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Keep trying same thing | Stop and research |
| Research indefinitely | Time-box to 15-30 min |
| Ignore error messages | Search exact error text |
| Skip local docs | Check README first |
| Guess at solutions | Understand problem first |

## What to Research First

Priority order:

1. **Error message** - Often contains the answer
2. **Local documentation** - Project-specific guidance
3. **Existing code** - Established patterns
4. **Library docs** - Official guidance
5. **Online search** - Community solutions

## Time Boxing

Research should be focused:

| Resource | Time Limit |
|----------|------------|
| Local docs | 5 minutes |
| Codebase search | 10 minutes |
| Online search | 15 minutes |
| Total research | 30 minutes max |

After 30 minutes without breakthrough → Escalate.

## Checklist

When triggered by 2 failures:

- [ ] Document what failed and why
- [ ] Check repository documentation
- [ ] Search existing codebase
- [ ] Search online resources
- [ ] Synthesize findings
- [ ] Update issue with research
- [ ] Formulate new approach
- [ ] If still failing, escalate

## Integration

This skill is triggered by:
- `issue-driven-development` - Step 8 (verification loop)

This skill calls:
- `issue-lifecycle` - Post research findings
- `memory-integration` - Store findings for future reference
