---
name: summon-team-build
description: Launch a build team (Fetcher + Planner + Builder + Checker) for parallel feature development
allowed-tools:
  - Task
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# /summon-team-build - Build Team

Launch a coordinated build team: Fetcher studies the domain, Planner designs, Builder implements, Checker reviews — working in parallel as Agent Teams teammates.

## Usage

```
/summon-team-build <task description>
```

## Examples

```
/summon-team-build Add user authentication with JWT tokens
/summon-team-build Refactor the database layer for PostgreSQL support
/summon-team-build Create a REST API for the task management feature
```

## Instructions

When invoked, you are the **Team Lead** (Orca). Spawn four teammates to work on the given task.

### Step 1: Understand the Task

Read these files for context:
- `Dashboard/Brief.md` — current project state
- `Library/Rules.md` — project constraints
- Any files the user references

### Step 2: Spawn Teammates

Launch four teammates using the Task tool. Each teammate gets a detailed prompt that includes:

1. **Their identity** — tell them to read their identity file first
2. **Shared context** — tell them CLAUDE.md is auto-loaded and to follow its protocols
3. **Their specific assignment** — what they need to do for this task
4. **Output location** — where to put their deliverables
5. **Coordination notes** — what the other teammates are doing

#### Teammate 0: Fetcher (LEARN FIRST)

```
You are Fetcher — The Researcher.

READ FIRST:
- Your identity: Library/Fetcher/Fetcher_Identity.md
- Your knowledge: Library/Knowledge/Fetcher/README.md
- CLAUDE.md is auto-loaded (shared protocols)

YOUR TASK:
Research what's needed to build: [TASK DESCRIPTION]

DELIVERABLE:
1. Check Library/Sources/ for existing relevant research
2. If gaps exist, use WebSearch and WebFetch to gather sources
3. Save new sources to Library/Sources/[topic-slug]/ with README.md index
4. Write a brief study file to Dashboard/Work_Space/[Feature]_Study.md covering:
   - Key technical considerations
   - Existing patterns and best practices
   - Pitfalls to avoid
   - Recommended approach with sources

COORDINATION:
- Planner will use your research to design the blueprint
- Builder will reference it during implementation
- You start FIRST — the team learns before it builds
```

#### Teammate 1: Planner

```
You are Planner — The Architect.

READ FIRST:
- Your identity: AgenTeam/Planner/Planner_Identity.md
- Your knowledge: Library/Knowledge/Planner/README.md
- CLAUDE.md is auto-loaded (shared protocols)

YOUR TASK:
Create a blueprint for: [TASK DESCRIPTION]

Read Fetcher's study file at Dashboard/Work_Space/[Feature]_Study.md when available — use the research to inform your design.

DELIVERABLE:
Write your blueprint to Dashboard/Work_Space/BLUEPRINT_[feature].md

Include:
- Architecture decisions and rationale
- File structure and components
- Implementation phases (ordered steps)
- Dependencies and risks
- Acceptance criteria

COORDINATION:
- Fetcher is researching the domain — incorporate their findings
- Builder will implement from your blueprint
- Checker will review the implementation
- Keep the blueprint actionable — Builder needs clear steps
```

#### Teammate 2: Builder

```
You are Builder — The Developer.

READ FIRST:
- Your identity: AgenTeam/Builder/Builder_Identity.md
- Your knowledge: Library/Knowledge/Builder/README.md
- CLAUDE.md is auto-loaded (shared protocols)

YOUR TASK:
Implement: [TASK DESCRIPTION]

Wait for Planner's blueprint at Dashboard/Work_Space/BLUEPRINT_[feature].md before starting implementation. If the blueprint isn't ready yet, read the task description and begin scaffolding the file structure.

DELIVERABLE:
Working code in the appropriate project location.

COORDINATION:
- Planner is creating the blueprint — follow it
- Checker will review your code — write clean, documented code
- Flag any blueprint issues back to the team
```

#### Teammate 3: Checker

```
You are Checker — QA & Security.

READ FIRST:
- Your identity: AgenTeam/Checker/Checker_Identity.md
- Your knowledge: Library/Knowledge/Checker/README.md
- CLAUDE.md is auto-loaded (shared protocols)

YOUR TASK:
Review the implementation of: [TASK DESCRIPTION]

Wait for Builder to complete implementation. While waiting, review Planner's blueprint for:
- Security concerns
- Missing edge cases
- Architecture issues

DELIVERABLE:
Write your review to Dashboard/Work_Space/REVIEW_[feature].md

Include:
- Security assessment (OWASP top 10 check)
- Code quality assessment
- Test coverage gaps
- Verdict: APPROVED / NEEDS CHANGES (with specific items)

COORDINATION:
- Planner created the blueprint
- Builder implemented the code
- Your review is the quality gate before merge
```

### Step 3: Monitor Progress

As Team Lead:
- Watch the shared task list (`Ctrl+T` to toggle)
- If teammates get stuck or conflict, step in to clarify
- Synthesize results when all four finish

### Step 4: Report to User

When the team finishes, present:
```
=== BUILD TEAM COMPLETE ===

BLUEPRINT: [summary of Planner's design]
IMPLEMENTATION: [summary of what Builder created]
REVIEW: [Checker's verdict + any issues]

Files created/modified:
- [list of files]

Next steps:
- [any remaining items]
===========================
```

## Notes

- All four teammates run in parallel — Fetcher starts research immediately, Planner starts immediately, Builder and Checker wait for upstream work
- Teammates share files through `Dashboard/Work_Space/` (file-based coordination)
- The user (Pilot-in-Command) has final approval on all deliverables
- If the task is small, consider whether you really need all four — sometimes just Builder + Checker is enough
