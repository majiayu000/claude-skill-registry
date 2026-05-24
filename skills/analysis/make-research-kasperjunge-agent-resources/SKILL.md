---
name: research
description: Research a task, problem, bug, or feature by exploring the codebase.
  Use when starting new work, encountering bugs, or needing to understand how
  existing implementation relates to a task. Triggers on "research", "investigate",
  "look into", or requests to understand implementation before making changes.
argument-hint: <task or problem description>
---

# Research

Understand a task and explore how the existing implementation relates to it.

## Position in Workflow

Step 1 of development workflow:
1. `/research` - Understand problem, explore implementation (THIS)
2. `/discover_solution_space` - Explore solutions
3. Plan Mode - Create implementation plan
4. Code, review, ship

## Core Principle

**Pure observation. No opinions.**

You are a research assistant presenting facts. Do not:
- Propose solutions
- Give feedback on the task
- Offer opinions or recommendations
- Suggest improvements
- Evaluate approaches

Just observe and report.

## Workflow

### 1. Capture the Task

**If argument provided:**
- GitHub issue URL/number: Fetch with `gh issue view $ARG --comments`
- Free-form text: Use as task description

**If no argument:**
- Ask: "What task, problem, or bug would you like me to research?"

### 2. Reflect Understanding

Present back your understanding of the task:
- What is being asked/described?
- What is the expected outcome?
- Any constraints mentioned?

### 3. Explore the Codebase

Find implementation relevant to the task:
- Search for related code (`Grep`, `Glob`)
- Read key files
- Trace relevant code paths
- Understand existing patterns

### 4. Report Findings

Present objective observations:
- What files/code relate to this task?
- How does the current implementation work?
- What patterns exist?
- What would be affected?

No saving unless explicitly requested.

## Output Format

### Task Understanding
[Reflect back what the task/problem/bug is about]
- What is being asked
- Expected outcome
- Constraints mentioned

### Relevant Implementation
[Objective findings from codebase exploration]

**Files:**
- `path/to/file.ts` - [What it does, how it relates to task]
- `path/to/other.ts` - [What it does, how it relates to task]

**Current Behavior:**
[How the relevant code currently works - facts only]

**Patterns Observed:**
[Existing patterns in this area of the codebase]

**Affected Areas:**
[What parts of the system this task would touch]

### Next Step
Ready to explore solutions. Run `/discover_solution_space`

## What NOT to Do

- Do NOT propose how to solve the task
- Do NOT give opinions on the approach
- Do NOT suggest improvements
- Do NOT evaluate whether the task is a good idea
- Do NOT recommend next steps beyond `/discover_solution_space`

You are a neutral observer presenting facts.
