---
name: ctx
description: Use when starting a session on a project, returning after time away, or before making significant changes. Essential for building comprehensive understanding of project state through total recall and oracle-driven exploration.
---

# Contextualize

You need to fully contextualize yourself in this repository before doing any work.

## Step 1: Search Total Recall

First, search Total Recall for relevant context about this project:

```
mcp__plugin_totalrecall_memory-total-recall__synthesis_search({
  query: "project name/key terms recent work decisions made",
  max_results: 15
})
```

Look for:
- Recent conversations about this project
- Decisions that were made
- Problems that were solved
- Patterns established
- Gotchas discovered

## Step 2: Dispatch the Oracle for Deep Context

Use the Oracle to gather comprehensive context:

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
  You are The Oracle - contextualize yourself deeply in this repository.

  MISSION: Build comprehensive understanding of the current project state.

  INVESTIGATE:

  1. **Project Identity**
     - Read CLAUDE.md, README.md, package.json (or equivalent)
     - What is this project? What does it do?
     - What are the core technologies and patterns?
     - What are the established conventions?

  2. **Current Work Status**
     - Check .plans/ directory for active plans
     - Check .tasks/ or TODO files for pending work
     - Check git status and recent commits (git log -10 --oneline)
     - What was being worked on? What's in progress?

  3. **Decision History**
     - Check .plans/DECISIONS.md or .plans/decisions/
     - What major decisions have been made?
     - What constraints exist from past choices?

  4. **Architecture Overview**
     - Map the key directories and their purposes
     - Identify core modules/services
     - Understand the data flow

  5. **Pain Points & Context**
     - Look for TODOs, FIXMEs, HACKs in code
     - Check for any KNOWN_ISSUES or TROUBLESHOOTING docs
     - Identify technical debt markers

  DELIVERABLE:
  Provide a structured context report:

  ## Project Summary
  [What this is, in 2-3 sentences]

  ## Current Status
  - Active work: [what's in progress]
  - Blocked items: [if any]
  - Recent changes: [last few commits summary]

  ## Key Decisions to Remember
  - [Decision 1]
  - [Decision 2]

  ## Established Patterns
  - [Pattern 1]: [where/how used]
  - [Pattern 2]: [where/how used]

  ## Conventions & Constraints
  - [Convention from CLAUDE.md]
  - [Technical constraint]

  ## Recommended Next Steps
  Based on current state, suggest what to focus on.

  Be thorough. This context will guide all subsequent work.
  """
)
```

## Step 3: Synthesize and Report

After gathering context from memory and Oracle:

1. **Summarize** the key findings for the user
2. **Highlight** anything that seems urgent or blocked
3. **Confirm** understanding of current priorities
4. **Ask** if there's specific context you're missing

## When to Use This Command

- Starting a new session on a project
- Returning to a project after time away
- Before making significant changes
- When feeling uncertain about project state
- After another developer has made changes

**Remember**: Context prevents mistakes. Take the time to understand before acting.
