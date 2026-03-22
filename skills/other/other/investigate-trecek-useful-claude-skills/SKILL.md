---
name: investigate
description: Deep investigation of errors, bugs, or codebase questions without making any code changes. Use when user mentions investigate, understand, explore, analyze, or pastes error tracebacks. Spawns parallel subagents for comprehensive exploration.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '🔍 [SKILL: investigate] Starting investigation...'"
          once: true
---

# Investigation Skill

Perform deep codebase investigation without making any changes. This skill uses parallel subagents to explore multiple aspects simultaneously.

## When to Use

- User pastes an error traceback and wants root cause analysis
- User wants to understand how a system/module works
- User asks "how did tests miss this" or similar
- User says "investigate", "explore", "understand", or "analyze"
- User explicitly says "do not change any code"

## Critical Constraints

**NEVER:**
- Modify any source code files
- Suggest backward compatibility solutions
- Suggest fallbacks that hide errors
- Create files outside `temp/investigate/` directory
- Choose or accept approaches, solutions, and/or fixes that are chosen simply because they are easier

**ALWAYS:**
- Use subagents for parallel exploration
- Write findings as a markdown report with unique name to `temp/investigate/` directory
- Identify how tests missed the issue (if applicable)
- Check for similar existing patterns in codebase
- Ensure approaches, solutions, and fixes are the appropriate long-term solutions with proper architecture

## Investigation Workflow

### Step 1: Parse the Investigation Target

Identify what needs investigation:
- **Error Investigation**: Extract error type, message, and stack trace
- **Module Investigation**: Identify the module/component to understand
- **Question Investigation**: Clarify the specific question being asked

### Step 2: Launch Parallel Subagents

Spawn explore subagents to investigate different aspects simultaneously (some aspects may and should require multiple subagents):

**Core Implementation**
- Find the primary source files
- Understand the main logic flow
- Identify key functions/classes

**Dependencies & Consumers**
- What depends on this code?
- What does this code depend on?
- Map the dependency graph

**Test Coverage**
- Find all tests for this code
- Identify what scenarios are tested
- Find gaps in test coverage

**Error Context (if error investigation)**
- Trace the error through the stack
- Find where the bad state originated
- Identify the root cause

**Similar Patterns**
- Search for similar code elsewhere
- How do other parts handle this?
- Are there established patterns?

**Architecture Context**
- Read relevant architecture.md files
- Understand design decisions
- Check for documented constraints

**External Research (Web Search)**
- Search for error messages in external sources
- Look up known issues in libraries/frameworks
- Find documentation for relevant APIs
- Check GitHub issues for similar problems
- Search for Stack Overflow discussions

### Step 3: Synthesize Findings

After subagents complete, consolidate into structured findings:

1. **Summary**: One paragraph overview
2. **Root Cause** (if error): The actual source of the problem
3. **Affected Components**: List of files/modules involved
4. **Data Flow**: How data moves through the system
5. **Test Gap Analysis**: Why tests didn't catch this
6. **Similar Patterns**: How similar issues are handled elsewhere
7. **External Research**: Relevant findings from web search (if applicable)
8. **Recommendations**: Suggested approaches (NOT implementations)

### Step 4: Write Report

Write findings to: `temp/investigate/investigation_{topic}_{date}.md`

Report structure:
```markdown
# Investigation: {Topic}

**Date:** {YYYY-MM-DD}
**Scope:** {What was investigated}

## Summary
{One paragraph overview}

## Root Cause
{If error investigation - the actual source}

## Affected Components
- {file1}: {role}
- {file2}: {role}

## Data Flow
{How data moves through the system}

## Test Gap Analysis
{Why existing tests didn't catch this}

## Similar Patterns
{How similar scenarios are handled elsewhere}

## External Research
{Relevant findings from web search - library bugs, known issues, documentation insights}
{Include source URLs for reference}

## Recommendations
{Suggested approaches - NOT code changes}
```

## Subagent Prompt Template

Use this template for each Explore subagent:

```
Investigate {specific aspect} of {target}.

Focus on:
1. {Specific question 1}
2. {Specific question 2}
3. {Specific question 3}

This is a research task - DO NOT modify any code.
Report your findings in a structured format.
```

