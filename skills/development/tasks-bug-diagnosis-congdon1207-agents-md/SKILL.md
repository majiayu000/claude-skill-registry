---
name: tasks-bug-diagnosis
description: Use when diagnosing bugs, analyzing errors/stack traces, or performing root cause analysis with evidence-based debugging protocols.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, TodoWrite
---

> **Skill Variant:** Use this skill for **autonomous, structured debugging workflows** with comprehensive verification protocols. For interactive debugging sessions with user feedback, use `bug-diagnosis` instead.

# Bug Diagnosis Workflow

## Core Anti-Hallucination Protocols

### ASSUMPTION_VALIDATION_CHECKPOINT

Before every major operation:

1. "What assumptions am I making about [X]?"
2. "Have I verified this with actual code evidence?"
3. "Could I be wrong about [specific pattern/relationship]?"

### EVIDENCE_CHAIN_VALIDATION

Before claiming any relationship:

- "I believe X calls Y because..." → show actual code
- "This follows pattern Z because..." → cite specific examples
- "Service A owns B because..." → grep for actual boundaries

### CONTEXT_ANCHOR_SYSTEM

Every 10 operations:

1. Re-read the original task
2. Verify current operation aligns with goals
3. Check if solving the right problem

---

## Quick Verification Checklist

**Before removing/changing ANY code:**

- [ ] Searched static imports?
- [ ] Searched string literals in code?
- [ ] Checked dynamic invocations (attributes, reflection)?
- [ ] Read actual implementations?
- [ ] Traced who depends on this?
- [ ] Assessed what breaks if removed?
- [ ] Documented evidence clearly?
- [ ] Declared confidence level?

**If ANY unchecked → DO MORE INVESTIGATION**
**If confidence < 90% → REQUEST USER CONFIRMATION**

---

## Phase 1: Bug Report Analysis

Create analysis document in `.ai/workspace/analysis/[bug-name].md`:

```markdown
## Bug Report Analysis

### Reported Behavior

[What is happening]

### Expected Behavior

[What should happen]

### Reproduction Steps

[How to reproduce]

### Error Message

[If available]

### Stack Trace

[If available]

### Environment

[Dev/Staging/Prod, browser, etc.]

### Affected Services

[TextSnippet, TextSnippet, TextSnippet, etc.]
```

---

## Phase 2: Evidence Gathering

### Multi-Pattern Search Strategy

```bash
# 1. Exact class/method name
grep -r "ExactClassName" --include="*.cs" --include="*.ts"

# 2. Partial variations (camelCase, PascalCase, snake_case)
grep -r "ClassName\|className\|class_name" --include="*.cs"

# 3. String literals (runtime/config references)
grep -r '"ClassName"' --include="*.cs" --include="*.json" --include="*.config"

# 4. Reflection/dynamic usage
grep -r "typeof(.*ClassName)\|nameof(.*ClassName)" --include="*.cs"

# 5. Configuration files
grep -r "ClassName" --include="*.json" --include="appsettings*.json"

# 6. Attribute-based usage
grep -r "\[.*ClassName.*\]" --include="*.cs"
```

### Dependency Tracing

```bash
# Direct usages (imports)
grep -r "using.*{Namespace}" --include="*.cs"

# Interface implementations
grep -r ": I{ClassName}\|: I{ClassName}," --include="*.cs"

# Base class inheritance
grep -r ": {BaseClassName}" --include="*.cs"

# DI registrations
grep -r "AddScoped.*{ClassName}\|AddTransient.*{ClassName}\|AddSingleton.*{ClassName}" --include="*.cs"

# Test references
grep -r "{ClassName}" --include="*Test*.cs" --include="*Spec*.cs"
```

### Error-Specific Searches

```bash
# Find exception handling
grep -r "catch.*{ExceptionType}" --include="*.cs"

# Find validation logic
grep -r "Validate.*{EntityName}\|{EntityName}.*Validate" --include="*.cs"

# Find error messages
grep -r "error message text from report" --include="*.cs" --include="*.ts"
```

### EasyPlatform-Specific Searches

```bash
# EventHandlers for entity
grep -r ".*EventHandler.*{EntityName}|{EntityName}.*EventHandler" --include="*.cs"

# Background jobs
grep -r ".*BackgroundJob.*{EntityName}|{EntityName}.*BackgroundJob" --include="*.cs"

# Message bus consumers
grep -r ".*Consumer.*{EntityName}|{EntityName}.*Consumer" --include="*.cs"

# Platform validation
grep -r "PlatformValidationResult\|EnsureValid\|EnsureFound" --include="*.cs"
```

---

## Phase 3: Root Cause Analysis

### Analysis Dimensions

```markdown
## Root Cause Analysis

### 1. Technical Dimension

- Code defects identified: [List]
- Architectural issues: [List]
- Race conditions possible: [Yes/No, evidence]

### 2. Business Logic Dimension

- Rule violations: [List]
- Validation failures: [List]
- Edge cases missed: [List]

### 3. Data Dimension

- Data integrity issues: [List]
- State corruption possible: [Yes/No]
- Migration issues: [Yes/No]

### 4. Integration Dimension

- Cross-service failures: [List]
- API contract violations: [List]
- Message bus issues: [List]
- LastMessageSyncDate race conditions: [Yes/No]

### 5. Environment Dimension

- Configuration issues: [List]
- Environment-specific: [Dev/Staging/Prod differences]
```

### Ranked Causes

```markdown
## Potential Root Causes (Ranked by Probability)

1. **[Cause 1]** - Confidence: XX%
    - Evidence: [What supports this]
    - Location: [file:line]

2. **[Cause 2]** - Confidence: XX%
    - Evidence: [What supports this]
    - Location: [file:line]
```

---

## Phase 4: Solution Proposal

```markdown
## Proposed Fix

### Solution Description

[Describe the fix approach]

### Code Changes

- File: `path/to/file.cs`
- Lines: XX-YY
- Change: [Description]

### Risk Assessment

- **Impact Level**: Low | Medium | High
- **Regression Risk**: [What could break]
- **Affected Components**: [List]

### Testing Strategy

- [ ] Unit test for the fix
- [ ] Regression tests for affected area
- [ ] Integration test if cross-service
- [ ] Manual testing checklist

### Rollback Plan

[How to revert if fix causes issues]
```

---

## Phase 5: Approval Gate

**CRITICAL**: Present analysis and proposed fix for approval before implementing.

Format:

```markdown
## Bug Analysis Complete - Approval Required

### Root Cause Summary

[Primary root cause with evidence]

### Proposed Fix

[Fix description with specific files and changes]

### Risk Assessment

- **Risk Level**: [Low/Medium/High]
- **Regression Risk**: [assessment]

### Confidence Level: [X%]

### Files to Modify:

1. `path/to/file.cs:line` - [change description]

**Awaiting approval to proceed.**
```

**DO NOT implement without user approval.**

---

## Confidence Levels

| Level  | Range   | Criteria                                                      | Action                                 |
| ------ | ------- | ------------------------------------------------------------- | -------------------------------------- |
| High   | 90-100% | Multiple evidence sources, clear code path, no contradictions | Proceed with fix                       |
| Medium | 70-89%  | Some evidence, some uncertainty                               | Present findings, request confirmation |
| Low    | < 70%   | Limited evidence, multiple interpretations                    | MUST request user confirmation         |

---

## Evidence Documentation Template

```markdown
## Investigation Evidence

### Searches Performed

1. Pattern: `{search1}` - Found: [X files]
2. Pattern: `{search2}` - Found: [Y files]

### Key Findings

- File: `path/to/file.cs:123` - [What was found]
- File: `path/to/another.cs:45` - [What was found]

### Not Found (Important Negatives)

- Expected `{pattern}` but not found in `{location}`
- No references to `{component}` in `{scope}`

### Confidence Level: [XX]%

### Remaining Uncertainties

1. [Uncertainty 1 - how to resolve]
2. [Uncertainty 2 - how to resolve]

### Recommendation

[Clear recommendation with reasoning]
```

---

## Common Bug Categories

### Null Reference Exceptions

```bash
grep -r "\.{PropertyName}" --include="*.cs" -A 2 -B 2
# Check for null checks before access
```

### Validation Failures

```bash
grep -r "Validate\|EnsureValid\|IsValid\|PlatformValidationResult" --include="*.cs"
# Trace validation chain
```

### Cross-Service Issues

```bash
grep -r "Consumer.*{Entity}\|Producer.*{Entity}" --include="*.cs"
# Check message bus communication
grep -r "LastMessageSyncDate" --include="*.cs"
# Check for race condition handling
```

### Authorization Issues

```bash
grep -r "PlatformAuthorize\|RequestContext.*Role\|HasRole" --include="*.cs"
# Check auth patterns
```

### Frontend Issues

```bash
grep -r "observerLoadingErrorState\|tapResponse\|untilDestroyed" --include="*.ts"
# Check state management patterns
```

---

## Verification Before Closing

- [ ] Root cause identified with evidence
- [ ] Fix addresses root cause, not symptoms
- [ ] No new issues introduced
- [ ] Tests cover the fix
- [ ] Confidence level declared
- [ ] User confirmed if confidence < 90%

---

## See Also

- `.github/AI-DEBUGGING-PROTOCOL.md` - Comprehensive debugging protocol
- `bug-diagnosis` skill - Interactive debugging with user feedback
- `.ai/prompts/context.md` - Platform patterns and context
