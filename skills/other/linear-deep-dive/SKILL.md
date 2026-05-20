---
name: linear-deep-dive
description: Use when given a Linear issue ID, URL, identifier, or project name/URL to analyze and plan work. For issues, fetches the issue, classifies it, explores relevant code, proposes an approach, and orchestrates the right skills. For projects, fetches the project with milestones and issues, builds a prioritized execution plan, and systematically works through issues respecting project structure and dependencies.
---

# Linear Deep Dive

Analyze a Linear issue or project end-to-end — understand it, explore the codebase, propose an approach, and orchestrate the right workflow to solve it.

## Invocation

```
/linear-deep-dive <issue ID, identifier, URL, or project name/URL>
```

Examples:
- `/linear-deep-dive DRC-2893`
- `/linear-deep-dive https://linear.app/recce/issue/DRC-2893/...`
- `/linear-deep-dive "Mypy Strict Typing"`
- `/linear-deep-dive https://linear.app/recce/project/mypy-strict-typing-abc123`

## Process

### 1. Parse Input and Detect Entry Type

Determine whether the input is an **issue** or a **project**:

| Input Pattern | Entry Type |
|---|---|
| `DRC-2893` (team prefix + number) | Issue |
| URL containing `/issue/` | Issue |
| URL containing `/project/` | Project |
| Quoted string or slug with no team prefix | Project (search by name) |

**Issue identifiers:** `DRC-2893`, `https://linear.app/recce/issue/DRC-2893/...`
**Project identifiers:** `"Mypy Strict Typing"`, `https://linear.app/recce/project/mypy-strict-typing-abc123`

For project URLs, extract the slug from the path. For plain strings without a team prefix pattern (`XXX-NNN`), treat as a project name search.

Once the entry type is determined, follow the appropriate flow:
- **Issue** → proceed to [Issue Flow](#issue-flow)
- **Project** → proceed to [Project Flow](#project-flow)

## Issue Flow

### 2. Fetch Issue

Use the Linear MCP server to retrieve the full issue with relations:

```
Tool: mcp__linear-server__get_issue
  id: <identifier>
  includeRelations: true
```

Extract and note:
- **Title and description** — the core problem statement
- **Priority** — how urgent this is
- **Status** — current workflow state
- **Labels** — issue classification (Bug, Feature, Improvement, etc.)
- **Assignee** — who owns it
- **Relations** — blocking/blocked-by/related issues
- **Key files** — any file paths mentioned in the description
- **Git branch** — the `gitBranchName` field (use this for work)

Also fetch comments for additional context:

```
Tool: mcp__linear-server__list_comments
  issueId: <issue UUID>
```

### 3. Classify the Issue

Determine the issue type from title, description, and labels. This drives which skills to invoke later.

| Classification | Signals | Primary Workflow |
|---------------|---------|-----------------|
| **Feature** | Label: Feature, "add", "new", "implement", "support" | brainstorming → writing-plans → executing-plans |
| **Bug** | Label: Bug, "fix", "broken", "regression", "error", stack traces | systematic-debugging → TDD |
| **Refactor** | Label: Improvement, "refactor", "eliminate", "simplify", "clean up" | writing-plans → TDD → executing-plans |
| **Investigation** | "investigate", "understand", "why does", "how does", question marks | codebase exploration → summary document |

If the classification is ambiguous, ask the user:

> This issue could be approached as a **refactor** or a **feature**. The description mentions eliminating a pattern (refactor) but also introduces new cache-patching behavior (feature). How would you like to approach it?

### 4. Explore Codebase

This is the core research phase. Use the Agent tool with `subagent_type: Explore` for broad discovery, and direct Read/Grep/Glob for targeted lookups.

**Step 4a — Read files mentioned in the issue:**

If the issue description references specific files (common in well-written issues), read them first. These are the author's pointers to the relevant code.

**Step 4b — Discover related code:**

Based on what you learn from the referenced files, explore outward:
- Grep for key function/variable names mentioned in the issue
- Find related test files for the affected code
- Check imports and callers of the affected modules
- Look for similar patterns elsewhere that might be affected

**Step 4c — Check related Linear issues:**

If the issue has relations (blocking, blocked-by, related), fetch those issues briefly to understand the broader context. Don't deep-dive them — just note how they connect.

**Step 4d — Check the git branch:**

If the issue has a `gitBranchName`, check its state:

```bash
git fetch origin
git branch -a | grep "<branch-name>"
git log origin/main..origin/<branch-name> --oneline  # If branch exists: what's already done?
```

If the branch already has commits, read through them to understand work-in-progress.

### 5. Build Context

Synthesize everything into a structured analysis. Write this to a temp working document:

```bash
# Save analysis to gitignored docs directory
mkdir -p docs/plans
```

**Analysis document structure:**

```markdown
# Deep Dive: <ISSUE-ID> — <Title>

## Issue Summary
<1-3 sentence distillation of the problem/request>

## Classification
**Type:** <feature | bug | refactor | investigation>
**Priority:** <from Linear>
**Labels:** <from Linear>

## Current State
<What the code does today — based on codebase exploration>

## Key Files
| File | Role | Lines of Interest |
|------|------|-------------------|
| `path/to/file.ts` | Description | L42-87: relevant function |

## Related Issues
| Issue | Title | Relationship |
|-------|-------|-------------|
| DRC-XXXX | Title | blocks / related to |

## Risks and Open Questions
- <Risk or uncertainty that needs clarification>
- <Anything the issue description assumes but code doesn't confirm>

## Proposed Approach
<See Step 6>
```

### 6. Propose Approach

Based on the classification and codebase exploration, propose a concrete approach. Present this to the user **before** executing.

**The proposal must include:**

1. **Approach summary** — 2-3 sentences on what you'll do
2. **Classification and workflow** — which skills will be invoked and why
3. **Task breakdown** — high-level steps (not full plan yet — that's for writing-plans)
4. **Scope boundaries** — what's in scope and explicitly what's NOT
5. **Risks** — anything that might complicate the work
6. **Estimated complexity** — small (1-2 files), medium (3-5 files), large (6+ files)

**Format the proposal clearly:**

```markdown
## Proposed Approach for <ISSUE-ID>

**Classification:** Refactor
**Workflow:** writing-plans → TDD → executing-plans
**Complexity:** Medium (4 files)

### What I'll Do
<2-3 sentence summary>

### Steps
1. <High-level step>
2. <High-level step>
3. ...

### Scope
**In scope:** <what's included>
**Out of scope:** <what's explicitly excluded>

### Risks
- <Risk and mitigation>

### Ready to proceed?
I'll start by invoking **writing-plans** to create a detailed implementation plan.
```

**Wait for user confirmation before proceeding.**

### 7. Orchestrate — Invoke the Right Skills

Based on classification and user confirmation, invoke the appropriate skill chain. The skill invocations below are the **default workflows** — adjust based on the specific issue.

**Before invoking any skill, update the issue status to "In Progress":**

```
Tool: mcp__linear-server__save_issue
  id: <issue identifier>
  state: "In Progress"
```

#### Feature Workflow

```
1. Invoke: superpowers:brainstorming
   - Feed it the issue summary and proposed approach
   - Let it explore alternatives and refine the design

2. Invoke: superpowers:writing-plans
   - Create detailed implementation plan from the brainstorming output
   - Plan includes exact file paths, code changes, and verification steps

3. Invoke: superpowers:executing-plans (or superpowers:subagent-driven-development)
   - Execute the plan with review checkpoints
```

#### Bug Workflow

```
1. Invoke: superpowers:systematic-debugging
   - Follow the four phases: investigate → analyze → hypothesize → implement
   - Use the issue description as the starting point for reproduction

2. Invoke: superpowers:test-driven-development
   - Write a failing test that reproduces the bug FIRST
   - Then implement the fix
   - Verify the test passes
```

#### Refactor Workflow

```
1. Invoke: superpowers:writing-plans
   - Create a detailed refactoring plan
   - Emphasize: preserve existing behavior, add tests for current behavior first

2. Invoke: superpowers:test-driven-development
   - For each refactoring step: verify existing tests pass, then refactor

3. Invoke: superpowers:executing-plans (or superpowers:subagent-driven-development)
   - Execute with frequent verification checkpoints
```

#### Investigation Workflow

```
1. Use Agent tool (subagent_type: Explore) for deep codebase analysis
2. Summarize findings in docs/plans/<date>-<issue-id>-findings.md
3. Post findings back to the Linear issue as a comment (with user permission)
```

---

## Branch Management

Before starting any implementation work:

```bash
# Check if the issue's branch already exists
BRANCH="<gitBranchName from Linear>"
git fetch origin

# If branch exists remotely, create local tracking branch
git checkout -t "origin/$BRANCH"

# If branch doesn't exist remotely, create from main
git checkout main && git pull
git checkout -b "$BRANCH"
```

Always work on the issue's designated branch. Never implement directly on `main`.

---

## Handling Edge Cases

### Issue has blockers
If the issue is blocked by other issues (`blockedBy` relations), inform the user:

> This issue is blocked by **DRC-XXXX**: "<title>". Would you like to:
> 1. Work on the blocker first
> 2. Proceed anyway (the blocker may not actually prevent progress)
> 3. Skip this issue for now

### Issue is vague or underspecified
If the issue lacks sufficient detail to propose an approach:

> The issue description doesn't specify [missing detail]. Before I can propose an approach, I need to understand:
> - [Specific question]
> - [Specific question]

### Issue spans frontend and backend
For full-stack issues, note both sides in the analysis and propose whether to tackle them together or separately. Default to **backend first** (APIs and data models), then frontend.

### Issue already has work-in-progress
If the git branch has existing commits, analyze them:
- What's already been done?
- Does it align with the issue description?
- Should we build on it or take a different approach?

Present findings to the user before proposing next steps.

---

## Project Flow

Use this flow when the input is a Linear **project** (not a single issue). A project is a collection of issues organized by milestones with a shared goal, description, and timeline.

### 8. Fetch Project

Retrieve the project with its full context:

```
Tool: mcp__linear-server__get_project
  query: <project name, slug, or ID>
  includeMilestones: true
  includeMembers: true
  includeResources: true
```

Extract and note:
- **Name and description** — the project's purpose and goals
- **`id`** — the project UUID (needed for subsequent queries)
- **`name`** — the project display name (needed for subsequent queries)
- **Status** — planned, started, paused, completed
- **Start/target dates** — timeline constraints
- **Lead** — who owns the project
- **Members** — who's involved
- **Milestones** — the project's phases/workstreams
- **Resources** — linked documents, specs, designs
- **Progress** — completion percentage

Also fetch recent status updates for additional context:

```
Tool: mcp__linear-server__get_status_updates
  type: "project"
  project: <project name or ID>
  limit: 5
```

### 9. Fetch Milestones and Issues

**IMPORTANT:** The `list_issues` and `list_milestones` tools do NOT reliably resolve URL slugs (e.g., `mypy-cleanup-ef517c78ef98`). You MUST use the **project name** or **project UUID** from the Step 8 `get_project` response. Do NOT run this step in parallel with Step 8 — wait for `get_project` to return first, then use the resolved `name` or `id`.

Retrieve the project's milestones to understand the phased structure:

```
Tool: mcp__linear-server__list_milestones
  project: <project name from get_project>   # e.g., "MyPy Cleanup", NOT the URL slug
```

Then fetch **all issues** in the project (can run in parallel with milestones):

```
Tool: mcp__linear-server__list_issues
  project: <project name from get_project>   # e.g., "MyPy Cleanup", NOT the URL slug
  limit: 250
```

For each issue, note:
- **Identifier and title**
- **Status** — backlog, todo, in progress, done, cancelled
- **Priority** — urgent (1) through low (4)
- **Labels** — bug, feature, etc.
- **Assignee** — who's working on it
- **Relations** — blocking/blocked-by dependencies between issues

### 10. Build Project Map

Synthesize the project into a structured overview. Group issues by milestone and status.

**Project map structure:**

```markdown
# Project Deep Dive: <Project Name>

## Project Summary
<2-3 sentence distillation of the project's purpose from its description>

## Status
**State:** <planned | started | paused | completed>
**Progress:** <X% complete>
**Timeline:** <start date> → <target date>
**Lead:** <name>

## Recent Updates
- <Date>: <summary of latest status update>

## Milestone Breakdown

### Milestone 1: <Name> (<status>)
**Description:** <milestone description>

| Issue | Title | Status | Priority | Assignee | Blocked By |
|-------|-------|--------|----------|----------|------------|
| DRC-XXX | ... | Todo | High | ... | DRC-YYY |

### Milestone 2: <Name> (<status>)
...

## Issues Without Milestone
| Issue | Title | Status | Priority | Assignee |
|-------|-------|--------|----------|----------|
| DRC-XXX | ... | ... | ... | ... |

## Dependency Graph
<List of blocking relationships across issues>

## Risks and Gaps
- <Issues with no assignee>
- <Blocked issues with no path to unblocking>
- <Milestones with no issues>
- <Overdue milestones>
```

Save this document to `docs/plans/<date>-project-<slug>-deep-dive.md`.

### 11. Prioritize and Propose Execution Plan

Determine the order to address issues, respecting:

1. **Milestone ordering** — earlier milestones first; don't skip ahead unless a milestone is fully blocked
2. **Dependencies** — never start an issue that is blocked by incomplete work
3. **Priority** — within a milestone, address urgent/high priority issues first
4. **Status** — skip issues that are done or cancelled; prioritize "in progress" issues (someone already started), then "todo", then "backlog"
5. **Issue type** — bugs before features within the same priority tier (bugs unblock existing functionality)

**Build an execution queue:**

```markdown
## Execution Plan

### Phase 1: <Milestone Name>

**Ready now** (no blockers, not done):
1. DRC-XXX — <title> [Priority: High, Type: Bug]
2. DRC-YYY — <title> [Priority: High, Type: Feature]

**Blocked** (waiting on other issues):
3. DRC-ZZZ — <title> [Blocked by: DRC-XXX]

### Phase 2: <Milestone Name>
...

### Recommended Starting Point
Start with **DRC-XXX** because: <reasoning — highest priority, unblocks others, etc.>
```

**Present this to the user and ask:**

> Here's the project overview and my recommended execution order. Would you like to:
> 1. **Start from the top** — work through issues in the order I've proposed
> 2. **Pick a specific issue** — jump to a particular issue you want to tackle
> 3. **Focus on a milestone** — work through a specific milestone only
> 4. **Adjust the plan** — reorder or exclude certain issues

### 12. Execute Systematically

Once the user confirms the approach, work through issues one at a time. For each issue:

1. **Deep-dive the individual issue** — follow the Issue Flow (Steps 2-7) for the selected issue, using its full context from the project map
2. **Carry forward project context** — when exploring the codebase, leverage knowledge from previous issues in the same project (shared files, patterns, architectural decisions)
3. **Respect milestone boundaries** — when finishing the last issue in a milestone, pause and report milestone completion before moving to the next
4. **Update the execution plan** — after completing each issue, reassess:
   - Are previously blocked issues now unblocked?
   - Did this work reveal new issues that should be added to the project?
   - Has the priority ordering changed?

**Between issues, report progress:**

```markdown
## Progress Update

**Completed:** DRC-XXX — <title>
**Milestone:** <Milestone Name> — X/Y issues done
**Unblocked:** DRC-ZZZ (was waiting on DRC-XXX)
**Next up:** DRC-YYY — <title>

Continue with DRC-YYY?
```

**Wait for user confirmation before starting each new issue.** The user may want to pause, switch to a different issue, or stop for the session.

### 13. Handle Project Edge Cases

#### Project has no milestones
Treat all issues as a flat list. Prioritize by: priority > status > dependencies > creation date.

#### Project has many issues (50+)
Focus the initial proposal on the top 10-15 actionable issues. Mention the total count and offer to show more:

> This project has 73 issues. I'm showing the 12 highest-priority actionable issues. Want me to expand the view?

#### Multiple milestones are in progress simultaneously
Present them as parallel workstreams and ask the user which to focus on. Don't interleave issues from different milestones unless the user requests it.

#### Issue belongs to multiple projects
Prioritize the project that was the entry point for the deep dive. Note the cross-project membership in the analysis.

#### Mid-session context: previously completed issues
If resuming work on a project across sessions, re-fetch the project state to pick up any issues that were completed outside this session (by other team members or in other sessions).

---

## Linear Issue Status Management

**You MUST update Linear issue status at each lifecycle transition.** This is not optional — it keeps the team's board accurate and prevents false progress signals.

### Status Transition Table

| Event | Action | Tool Call |
|-------|--------|-----------|
| Starting work on an issue (after user confirms approach in Step 6) | Set **In Progress** | `mcp__linear-server__save_issue` with `state: "In Progress"` |
| Creating a PR for the issue | Set **In Review** | `mcp__linear-server__save_issue` with `state: "In Review"` |
| PR merged to `main` | Set **Done** | `mcp__linear-server__save_issue` with `state: "Done"` |
| PR closed without merge | Set **In Progress** | `mcp__linear-server__save_issue` with `state: "In Progress"` |

### When to Transition

**In Progress — triggered by Step 7 (Orchestrate):**
Immediately after the user confirms the approach and before invoking any implementation skill, update the issue:

```
Tool: mcp__linear-server__save_issue
  id: <issue identifier, e.g., "DRC-2893">
  state: "In Progress"
```

**In Review — triggered by PR creation:**
When using the `create-pr` skill or running `gh pr create`, update the issue immediately after the PR is successfully created:

```
Tool: mcp__linear-server__save_issue
  id: <issue identifier>
  state: "In Review"
```

If the PR title or body references the issue (e.g., `Closes DRC-2893`), still explicitly update the status — do not rely on Linear's GitHub integration for timely status changes.

**Done — triggered only by confirmed merge:**
Only set Done after verifying the PR has been merged:

```bash
gh pr view <PR-number> --json state --jq '.state'
# Must return "MERGED"
```

```
Tool: mcp__linear-server__save_issue
  id: <issue identifier>
  state: "Done"
```

**NEVER set Done based on PR creation, CI passing, or approval.** The merge is the gate. See `references/linear-issue-lifecycle.md`.

### Project Flow Status Management

When working through a project (Steps 8-12), apply the same status transitions to each issue as you work through the execution queue. Additionally:

- When picking an issue from the execution queue to start work, set it to **In Progress**
- When all issues in a milestone are Done, note this in the progress update
- When re-fetching project state (mid-session context recovery), respect existing statuses — don't re-transition issues that are already in the correct state

---

## Iron Rules

**For all entry types:**
- **Always fetch first.** Never propose an approach based on the title alone — fetch the full issue or project.
- **Always explore the codebase.** Never propose changes to code you haven't read.
- **Always confirm with the user.** Never start implementation without presenting the approach and getting approval.
- **Respect the skill chain.** Use brainstorming for features, systematic-debugging for bugs. Don't skip steps.
- **Stay in scope.** The issue or project defines the boundaries. Don't expand scope without discussing with the user.
- **Save your analysis.** Write the deep-dive document to `docs/plans/` so it persists across sessions.

**For Linear issue status management:**
- **ALWAYS update issue status at lifecycle transitions.** Set "In Progress" when work begins, "In Review" when a PR is created. This is mandatory, not optional.
- **NEVER mark issues as "Done" until the PR has been merged to `main`.** When a PR is opened, move issues to "In Review". Only transition to "Done" after confirming the merge. See `references/linear-issue-lifecycle.md`.
- **Status flow:** Triage → In Progress (work starts) → In Review (PR opened) → Done (PR merged).

**For issues:**
- **Use the issue's git branch.** Always work on `gitBranchName` from Linear, never on `main`.

**For projects:**
- **Create a branch for the project.** If the project doesn't have a branch, create one named `project/<slug>` and work there. Never work on `main`.
- **Respect milestone order.** Don't jump ahead to later milestones while earlier ones have actionable work.
- **Respect dependencies.** Never start a blocked issue. Always check if completing an issue unblocks others.
- **Report progress between issues.** The user should always know where they are in the execution plan.
- **Pause at milestone boundaries.** Completing a milestone is a natural checkpoint — report it and confirm the next phase.
- **Carry context forward.** Reuse codebase knowledge from earlier issues — don't re-explore the same files from scratch.
