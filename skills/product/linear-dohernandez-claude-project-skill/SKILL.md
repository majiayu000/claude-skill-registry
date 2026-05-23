---
name: linear
description: Create and manage Linear issues using templates for the CI/E2E Runner project. Use when user says /linear.
user-invocable: true
allowed-tools: [Read, Grep, Glob, AskUserQuestion, mcp__linear-server__create_issue, mcp__linear-server__update_issue, mcp__linear-server__get_issue, mcp__linear-server__list_issues, mcp__linear-server__list_cycles, mcp__linear-server__list_teams, mcp__linear-server__list_projects, mcp__linear-server__list_issue_labels, mcp__linear-server__list_issue_statuses]
hooks:
  Stop:
    - type: command
      command: "task claude:validate-skill -- --skill linear"
---

# Linear

Create and manage Linear issues using the GenLayer issue template for the CI/E2E Runner project.

## Overview

This skill handles Linear issue management for the CI/E2E Runner project:
- Creates issues using the standard template format
- Converts plans/reports into properly formatted Linear issues
- Supports creating issues in backlog or specific cycles

## Configuration

- **Team**: Node (NOD) -- default; configurable per organization needs
- **Default State**: Backlog (unless cycle specified)

## Issue Template

All issues are created with this structure:

```markdown
## Problem Statement

[What problem are we solving and why?]

## Proposed Solution

[High-level approach]

## Acceptance Criteria

1. Given X, when Y, then Z (behavior specifications)
2. [Performance: <100ms response (if applicable)]
3. [Testing requirements (if applicable)]
4. [AI-generated code reviewed by human requirements (if applicable)]
5. [Edge cases considered beyond AI suggestions (if applicable)]

## Specific AI-Execution Plan

\`\`\`
[What parts will be solved by the AIs above]
\`\`\`

## Human Contribution Focus

[What parts will require human creativity/decision-making?]

## Technical Notes

[Implementation details, gotchas, AI limitations encountered]

## Lessons Learned *(optional)*

[What was learned while planning the ticket?]
```

**Note:** "Lessons Learned" is optional at creation. Include if there are insights discovered while planning. Omit section if empty.

## Content Extraction from Plans

When given a plan/analysis/report, extract content using these mappings:

| Template Section | Extract From Document |
|-----------------|----------------------|
| **title** | Document heading, Executive Summary first sentence |
| **problem_statement** | Executive Summary, Problem, Current Pattern sections |
| **proposed_solution** | Proposed Solution, Approach, Strategy, Key Insight |
| **acceptance_criteria** | Benefits, Expected Outcomes - convert to Given/When/Then |
| **ai_execution_plan** | Implementation Steps - actionable steps for Claude agent (see format below) |
| **human_contribution** | Risks needing judgment, Decisions Needed, Open Questions |
| **technical_notes** | Risks and Mitigations, Gotchas, Related Files |

**Priority when content fits multiple sections:**
1. problem_statement = WHY (motivation, pain)
2. proposed_solution = WHAT (high-level approach)
3. ai_execution_plan = HOW AI does it (specific steps)
4. acceptance_criteria = HOW we verify (success criteria)
5. human_contribution = WHAT humans decide
6. technical_notes = WHAT could go wrong

**Empty sections:** Omit entirely. Never use placeholder text.

## AI-Execution Plan Format

The AI-Execution Plan must be actionable steps another Claude agent can execute:

```
## AI Execution Steps

### Step 1: [Action] [What] in [Where]
- File: path/to/file.ts
- Pattern: [what to look for]
- Action: [Add/Remove/Update] [specific change]
- Verify: [how to confirm done]

### Step 2: ...
```

Each step needs:
- **File/Pattern**: Where to make changes
- **Action**: Specific change to make
- **Verify**: How to confirm it's done

## Proposal Wizard

Before creating a ticket, show a proposal for discussion:

```
## Ticket Proposal

**Title:** [inferred title]

### Metadata
| Field | Value | Reasoning |
|-------|-------|-----------|
| Labels | Productivity | CI/CD tooling improvement |
| Estimate | 2pt | 3 files, moderate changes, ~1 day |
| Cycle | next | User specified |
| State | Todo | Auto (cycle specified) |
| Related | NOD-500 | Found in plan references |

### Description Preview
[First lines of each section...]

---
**Ready to create?** Or adjust any options?
```

Wait for user approval before creating.

**CRITICAL: Re-approval Required After Changes**

When user requests ANY changes (even simple ones like "assign to X"):
1. Apply the requested changes
2. Show the FULL updated proposal again
3. Wait for EXPLICIT approval ("yes", "create it", "looks good")
4. NEVER create the ticket immediately after changes are requested

## Available Labels

| Label | Use When |
|-------|----------|
| **Bug** | Fixing broken behavior, errors, crashes |
| **Feature** | New functionality that didn't exist |
| **Improvement** | Enhancing existing functionality, refactoring, code quality |
| **Optimization** | Performance improvements, code cleanup, efficiency |
| **Productivity** | Developer tooling, automation, skills, CI/CD |
| **Documentation** | Docs updates, README, API docs |
| **Test** | Adding or improving tests |
| **Performance** | Speed/memory optimizations, benchmarks |
| **Critical Path** | Blocking other work, urgent priority |
| **Spike** | Research, exploration, proof of concept |
| **Release** | Release process tickets, version releases, changelog generation |

## Metadata Inference

| Field | Inference | How |
|-------|-----------|-----|
| **labels** | Auto | Infer from work type (see table above) |
| **project** | Auto | Infer from affected area (if projects exist) |
| **estimate** | Auto | Based on effort calculation (see below) |
| **priority** | Ask | Only infer if "critical"/"blocking" language |
| **cycle** | User | Use what user says, default backlog |
| **state** | Auto | Todo if cycle specified, else Backlog |
| **assignee** | Ask | Ask or leave unassigned |
| **related_to** | Extract | Scan for issue ID patterns (e.g., NOD-XXX) in plan |
| **links** | Extract | Scan for URLs in plan |
| **parent_id** | User | Only if explicitly requested |
| **blocks/blocked_by** | Extract | Scan for "blocks"/"depends on" language |
| **due_date** | User | Only if explicitly provided |

## Estimate Guide (Total Effort = AI + Human Review + Iterations)

| Points | Time | Scope |
|--------|------|-------|
| 1pt | ~4 hours | 1-3 files, simple, 1 iteration |
| 2pt | ~1 workday | 1-5 files, moderate, 2 iterations |
| 3pt | ~2 workdays | 5-10 files, some complexity |
| 5pt | ~2-4 workdays | 10-20 files, significant refactoring |
| 8pt | ~1 workweek | 20+ files, architectural, critical path |

**Complexity multipliers (+1 point each):**
- Touches CI pipeline / critical workflow path
- Has risks/edge cases listed
- Requires testing strategy
- Cross-module changes

## Quick Reference

### Creates
- Linear issues in the configured team with proper template formatting

### Required Fields
- **title** - Issue title
- **problem_statement** - What problem are we solving?

### Optional Template Fields
- proposed_solution, acceptance_criteria, ai_execution_plan, human_contribution, technical_notes

### Optional Metadata
| Field | Description | Example |
|-------|-------------|---------|
| assignee | Who will work on it | "me", "darien" |
| labels | Issue labels | ["Bug", "Improvement"] |
| project | Project name | "CI Infrastructure" |
| cycle | Sprint cycle | "current", "next", 26 |
| priority | 1=Urgent, 2=High, 3=Normal, 4=Low | 2 |
| estimate | Story points | 3 |
| state | Initial state (auto: Todo if cycle set) | "Backlog", "Todo" |
| due_date | Deadline | "2026-02-15" |

### Optional Relationships
| Field | Description | Example |
|-------|-------------|---------|
| parent_id | Create as sub-issue | "NOD-123" |
| links | Attach URLs | [{url, title}] |
| blocks | Issues this blocks | ["NOD-456"] |
| blocked_by | Issues blocking this | ["NOD-100"] |
| related_to | Related issues | ["NOD-310"] |

## Usage

When invoked directly by the user:
1. Request required information if not provided
2. Format content using the template
3. Create issue in Linear with appropriate metadata

## Full Documentation

See `skill.yaml` for complete procedure, patterns, and template details.
