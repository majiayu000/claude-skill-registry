---
name: issue-creation-review
description: Verifies Trellis issues against original requirements for completeness, correctness, and appropriate scope. Use when asked to "verify issue", "validate trellis issue", "check issue completeness", or "review created issue".
context: fork
agent: general-purpose
allowed-tools:
  - Glob
  - Grep
  - LS
  - Read
  - WebFetch
  - WebSearch
  - TodoWrite
  - mcp__perplexity-ask__perplexity_ask
  - mcp__task-trellis__get_issue
  - mcp__task-trellis__list_issues
---

# Issue Creation Review

Verify that a created Trellis issue accurately reflects original requirements without over-engineering or missing critical elements.

## Required Inputs

- **Original Requirements**: The initial request or specifications
- **Created Issue**: The issue ID or full issue details
- **Additional Context** (optional): Clarifications or decisions made during creation

## Handling Missing Information

**This skill runs as a sub-agent and cannot ask questions directly.** If required inputs are missing or unclear, you must return a structured response requesting clarification instead of proceeding with assumptions.

When information is missing or ambiguous, return the following structure:

```
## Clarification Needed

### Questions
1. [Specific question about missing/unclear information]
2. [Additional questions as needed]

### Context Collected So Far
- [Summary of what you've already determined]
- [Relevant codebase findings]
- [Partial analysis completed]

### Instructions for Caller
1. Gather answers to the questions above from the user
2. Re-invoke this skill with the original inputs plus the following additional context:
   - Answers to questions: [list the questions by number]
   - Previously collected context: [reference this section]
```

**Do not make assumptions** about requirements, scope decisions, or implementation details when critical information is missing.

## Verification Process

### 1. Research Codebase Context

Before evaluating, investigate the existing system:

- Search for similar implementations to verify consistency
- Check architectural patterns used in the codebase
- Identify existing utilities/libraries that should be leveraged
- Verify integration points mentioned are valid

### 2. Completeness Check

Verify all required elements are present.

**Common to all issue types:**

- All functional requirements from input are addressed
- Acceptance criteria are measurable and complete
- Dependencies/integration points are identified

**Type-specific additions:**

| Type    | Additional Requirements                              |
| ------- | ---------------------------------------------------- |
| Project | Technical architecture specified                     |
| Epic    | Clear scope boundaries, logical feature grouping     |
| Feature | Specific user-facing capability, feature integration |
| Task    | Implementable scope, clear technical specifications  |

### 3. Correctness Check

- **Technical Accuracy**: Proposed solutions align with codebase patterns
- **Requirement Alignment**: Interpretation matches user intent
- **Feasibility**: Approach is technically viable
- **Consistency**: Aligns with existing system architecture

### 4. Scope Assessment

Evaluate for over-engineering:

- Identify additions beyond the original request
- Flag unnecessary complexity or premature optimization
- Ensure abstractions are justified by actual requirements

**Exception**: Expanded scope is acceptable if explicitly requested (e.g., "comprehensive" or "future-proofed" solution).

## Output

Provide a verification report covering:

1. **Issue Details**: Type, ID, title
2. **Completeness**: Complete/Partial/Incomplete with specific gaps
3. **Correctness**: Correct/Issues Found with specific findings and codebase alignment
4. **Scope**: Appropriate/Over-engineered with analysis of what was requested vs. created
5. **Recommendations**: Critical issues and suggested improvements
6. **Verdict**: APPROVED / NEEDS REVISION / REJECTED with summary

Use codebase evidence to support findings. Flag over-engineering only when it adds complexity without benefit.
