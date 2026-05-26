---
name: analyse
description: Investigate codebase, debug issues, or analyze patterns
argument-hint: <issue or area to investigate>
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebSearch
---

# /analyse - Code Investigation

Investigate codebase issues, debug problems, or analyze patterns.

## Purpose

Provide deep analysis by:
- Investigating bugs and issues
- Analyzing code patterns
- Tracing data flow
- Identifying root causes

## Inputs

- `$ARGUMENTS`: Issue description or area to investigate
- `${PROJECT_NAME}`: Current project context
- Error messages or symptoms if debugging

## Outputs

Analysis report at `reports/analysis/YYYY-MM-DD-topic.md`

## Workflow

### 1. Understand the Question
From `$ARGUMENTS`:
- Is this debugging an issue?
- Is this understanding a pattern?
- Is this exploring code structure?

### 2. Gather Context
- Read relevant code
- Search for patterns
- Check logs if available
- Review recent changes

### 3. Form Hypotheses
Based on initial investigation:
- What might cause this?
- What patterns are involved?
- What dependencies matter?

### 4. Investigate
For each hypothesis:
- Search for evidence
- Trace code paths
- Check data flow
- Test assumptions

### 5. Analyze Findings
Synthesize discoveries:
- What is the root cause?
- What patterns were found?
- What are the implications?

### 6. Document
Create analysis report:

```markdown
# Analysis: [Topic]

**Date**: YYYY-MM-DD
**Scope**: [What was investigated]
**Conclusion**: [Key finding]

---

## Context
[What prompted this investigation]

## Investigation

### Approach
[How the investigation was conducted]

### Findings

#### Finding 1: [Title]
[Description of finding]

**Evidence**:
- [File:line - what was found]
- [Pattern observed]

#### Finding 2: [Title]
[Description]

## Root Cause
[If applicable, the underlying issue]

## Impact
[What this affects]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

## Related
- [Links to related code]
- [Links to docs]
```

## Investigation Patterns

### Bug Investigation
1. Reproduce the issue
2. Identify symptoms
3. Trace to source
4. Identify root cause
5. Propose fix

### Pattern Analysis
1. Identify pattern instances
2. Analyze commonalities
3. Note variations
4. Document implications

### Code Structure Analysis
1. Map components
2. Trace dependencies
3. Identify boundaries
4. Document architecture

### Performance Analysis
1. Identify slow operations
2. Profile if possible
3. Analyze bottlenecks
4. Propose optimizations

## Tools for Investigation

```bash
# Search for patterns
grep -r "pattern" src/

# Find file types
find . -name "*.ts" -type f

# Git history
git log --oneline --all -- file.ts
git blame file.ts

# Test in isolation
npm test -- --grep "specific test"
```
