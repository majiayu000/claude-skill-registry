---
name: issue-creation-orchestration
description: Orchestrates issue creation with automatic review. Use when asked to "create and review issues", "create verified issues", or when you want issues automatically validated against requirements.
allowed-tools:
  - mcp__task-trellis__create_issue
  - mcp__task-trellis__get_issue
  - mcp__task-trellis__update_issue
  - mcp__task-trellis__list_issues
  - mcp__perplexity-ask__perplexity_ask
  - Task
  - TaskOutput
  - Glob
  - Grep
  - Read
  - AskUserQuestion
---

# Issue Creation with Review

Orchestrate issue creation with automatic review to ensure created issues accurately reflect the original requirements.

## Goal

Create Trellis issues using the `issue-creation` skill, then automatically verify them against the original requirements using `issue-creation-review`. Handle any questions or findings from the review before completing.

## Autonomous Operation

**When given a parent issue ID** (e.g., "F-feature-id", "E-epic-id"), proceed directly to creating child issues without asking for confirmation. The user has already decided they want child issues created by invoking this skill.

**Do not ask about granularity.** Default to coarser-grained issues that are easier for AI agents to orchestrate during implementation. Fewer, larger issues are preferred over many small ones. Use your judgment to determine appropriate scope - the user does not need to micromanage issue structure.

**Only ask clarifying questions when:**
- Requirements are genuinely ambiguous and could be interpreted multiple ways
- Critical information is missing that cannot be inferred from context
- A decision has significant irreversible consequences

Otherwise, make reasonable decisions and proceed.

## Input

`$ARGUMENTS` - The user's original requirements/instructions for issue creation

## Process

### 1. Capture Original Input

**CRITICAL**: Store the exact user instructions verbatim at the start.

```
Original User Requirements:
---
[EXACT_USER_INPUT_HERE]
---
```

This exact text will be passed to the review agent. Do not paraphrase, summarize, or modify it in any way. The reviewer needs the original requirements to verify the created issues accurately.

### 2. Research the Codebase

**CRITICAL**: Before creating any issues, you MUST research the current state of the codebase. Parent issues may have been written before other work was completed - never assume the parent issue reflects reality.

1. **Read the parent issue** to understand the intended scope
2. **Search the codebase** using Glob and Grep to understand:
   - What already exists that's relevant to this work
   - Existing patterns and conventions to follow
   - What may have already been partially implemented
   - Current architecture and file structure
3. **Compare parent issue against reality** - identify any gaps between what was written and what currently exists
4. **Adjust scope accordingly** - only create issues for work that actually needs to be done

Do not blindly create issues based on text in a parent issue. The codebase is the source of truth.

### 3. Invoke Issue Creation

Use the `issue-creation` skill to create the requested issues:

1. Determine the appropriate issue type(s) from the user's request
2. Follow the issue-creation workflow for that type
3. Create the issue(s) using the Trellis MCP tools - proceed autonomously when given a parent ID
4. Track all created issue IDs and their types

**Record created issues:**
```
Created Issues:
- [ISSUE_ID]: [ISSUE_TYPE] - [TITLE]
- [ISSUE_ID]: [ISSUE_TYPE] - [TITLE]
```

### 4. Spawn Review for Created Issues

After all issues are created, spawn `issue-creation-review` as an async subagent to verify each issue.

For each created issue (or the top-level issue if creating a hierarchy):

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Review created issue [ISSUE_ID]"
- run_in_background: true
- prompt: |
    Use the /issue-creation-review skill to verify this issue.

    **Original User Requirements** (verbatim):
    ```
    [EXACT_ORIGINAL_INPUT_FROM_STEP_1]
    ```

    **Created Issue**: [ISSUE_ID]

    **Context from Creation**:
    [Any decisions made, clarifications received, or notable choices during creation]

    Verify the issue accurately reflects the original requirements.
    Check for completeness, correctness, and appropriate scope.
    If you have questions that need user answers, return them clearly.
```

Use `TaskOutput` to wait for the review to complete.

### 5. Handle Review Results

Process the review output based on its content:

#### Review Passes (No Issues Found)

If the review returns "APPROVED" with no findings:

- Report success to the user
- Proceed to output summary

#### Review Has Questions

If the review returns with "Clarification Needed" or questions:

1. Extract the questions from the review output
2. Use `AskUserQuestion` to get answers from the user
3. Re-run the review with the answers included:

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Re-review issue [ISSUE_ID] with clarifications"
- run_in_background: true
- prompt: |
    Use the /issue-creation-review skill to verify this issue.

    **Original User Requirements** (verbatim):
    ```
    [EXACT_ORIGINAL_INPUT]
    ```

    **Created Issue**: [ISSUE_ID]

    **Previous Review Questions and Answers**:
    Q1: [Question from reviewer]
    A1: [User's answer]

    Q2: [Question from reviewer]
    A2: [User's answer]

    Continue the review with these clarifications.
```

#### Review Finds Issues

If the review returns with ANY findings (major or minor):

**CRITICAL**: You MUST address ALL findings, not just "critical" ones. Every piece of feedback matters.

1. **Evaluate each finding**:
   - Is this finding valid and applicable?
   - If you believe a finding is incorrect, document your reasoning

2. **Fix all valid findings**:
   - Use `update_issue` to make corrections for EVERY valid finding
   - This includes minor issues like documentation, wording, or clarity improvements
   - Do not skip findings because they seem small

3. **Challenge incorrect findings** (if any):
   - If you genuinely believe a finding is wrong, explain why in your response
   - You are not required to blindly follow incorrect recommendations
   - But you MUST justify why you're not addressing a specific finding

4. **Re-run review** after making fixes to verify all findings were addressed

5. **Escalate only when blocked**:
   - Use `AskUserQuestion` only if you cannot resolve a finding yourself
   - Or if fixing a finding would contradict the original requirements

**Do NOT categorize findings as "minor" and ignore them.** The review exists to improve quality - every finding deserves attention.

## Output Format

Provide a summary of the creation and review process:

```
## Issue Creation Complete

### Created Issues
- [ISSUE_ID]: [Title] ([Type])
- [ISSUE_ID]: [Title] ([Type])

### Review Results
**Status**: Passed / Passed with Findings / Required Fixes

[Summary of review outcome]

### Actions Taken
[List any fixes made based on review feedback, or note if issues were accepted as-is]

### Next Steps
[Suggestions for what the user might want to do next - implement, add more detail, etc.]
```

## Key Requirement

**The original user instructions must be preserved verbatim and passed to the review agent.** This is critical for accurate verification. The orchestrator must not paraphrase or summarize in a way that could mislead the reviewer about what was actually requested.

## Guidelines

- **Verbatim preservation**: Never modify the original requirements when passing to review
- **Transparent process**: Keep the user informed of what's happening at each step
- **Address all findings**: Fix every valid review finding, including minor ones
- **Challenge thoughtfully**: If a finding seems wrong, explain why rather than silently ignoring it
- **Single review cycle**: Aim to resolve issues in one re-review; if still failing, escalate to user

<rules>
  <critical>Preserve the original user instructions VERBATIM when passing to the review agent</critical>
  <critical>If a subagent fails or returns an error, STOP and report to the user</critical>
  <critical>Do not paraphrase or summarize requirements - the reviewer needs the exact original text</critical>
  <critical>Research the codebase before creating issues - parent issues may be outdated</critical>
  <critical>Address ALL review findings - do not ignore feedback because it seems minor</critical>
  <critical>If you skip a finding, you MUST explain why you believe it is incorrect</critical>
  <important>Proceed autonomously when given a parent issue ID - do not ask for confirmation</important>
  <important>Default to coarser-grained issues for easier AI orchestration</important>
</rules>
