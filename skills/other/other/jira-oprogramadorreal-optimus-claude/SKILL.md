---
description: Fetches and optimizes context from a JIRA issue for AI-assisted development. Searches assigned issues or fetches by key. Distills title, description, acceptance criteria, sprint context, and comments into a structured task description. Analyzes the codebase to surface missing criteria, scope, and risks. Optionally improves the JIRA issue itself. Use before /optimus:tdd, /optimus:brainstorm, or /optimus:branch to pull task context from JIRA.
disable-model-invocation: true
---

# JIRA Context

Fetch a JIRA issue, distill it into an optimized task description for Claude Code, analyze the codebase to surface missing criteria, scope, and risks, and optionally improve the issue's description in JIRA. The skill works with any JIRA MCP server (Atlassian Rovo or community servers like sooperset/mcp-atlassian) and guides first-time setup when no server is configured.

## Step 1: Detect JIRA MCP Server

Read `$CLAUDE_PLUGIN_ROOT/skills/jira/references/jira-mcp-detection.md` and follow the **Detection Procedure**.

- **Server detected** → record `jira-server-name` and tool prefix, proceed to Step 2
- **No server detected** → follow the **Guided Setup Procedure** in the same reference. If setup completes successfully, proceed to Step 2. If the user skips setup, stop

## Step 2: Find the Issue

Two modes based on whether the user provided an issue key inline.

### Direct fetch

If the user provided an issue key inline (e.g., `/optimus:jira PROJ-123`):
1. Validate format — must match `[A-Z][A-Z0-9]+-\d+` (e.g., `PROJ-123`, `AB-1`)
2. If valid → proceed to Step 3 with this key
3. If invalid → inform the user and use `AskUserQuestion` to request a corrected key

### Search mode

If no issue key was provided (e.g., `/optimus:jira` with no argument), use `AskUserQuestion` — header "Find issue", question "How would you like to find your JIRA issue?":
- **Enter issue key** — "I know the key (e.g., PROJ-123)"
- **My open issues** — "Search my assigned open issues"
- **Search by project** — "List recent issues in a specific project"

**Enter issue key:** Use `AskUserQuestion` — header "Issue key", question "Enter the JIRA issue key:". Validate and proceed to Step 3.

**My open issues:** Read `$CLAUDE_PLUGIN_ROOT/skills/jira/references/jira-context-extraction.md`, section **Search: Assigned Issues**. Execute the JQL search, present results as a numbered list (max 10). Use `AskUserQuestion` — header "Select issue", question "Which issue are you working on?" with each issue as an option (label: `KEY — Summary`, description: `[Type, Priority]`). Proceed to Step 3 with the selected key.

**Search by project:** Use `AskUserQuestion` — header "Project", question "Enter the JIRA project key (e.g., PROJ):". Execute the project search from the extraction reference. Present results and let the user pick, same as above. Proceed to Step 3 with the selected key.

## Step 3: Fetch Issue Context

Read `$CLAUDE_PLUGIN_ROOT/skills/jira/references/jira-context-extraction.md` and follow the **Fetch Procedure** for the selected issue key:

1. Fetch issue details (summary, description, type, status, priority, assignee, sprint, parent/epic)
2. Fetch linked issues and subtasks (keys + summaries only)
3. Fetch recent comments (last 10, truncated to 2000 characters total)
4. Fetch sprint context (sprint name, goal, sibling issues)

Handle errors according to the **Error Handling** table in the reference. If a critical error occurs (401, 403, 404), report it to the user with the specified message and stop.

## Step 4: Distill into Structured Task

Assemble the fetched data into the **Structured Output Format** from the extraction reference:

```
## Task: [Issue Key] — [Summary]

### Goal
[Single-sentence distilled goal]

### Acceptance Criteria
[Extracted or inferred acceptance criteria as a numbered list]

### Context
- Type: [Issue type]
- Status: [Current status]
- Priority: [Priority]
- Assignee: [Name]
- Sprint: [Sprint name — sprint goal]
- Parent: [Epic key — Epic summary]
- Linked issues: [KEY — summary (link type)]
- Subtasks: [KEY — summary (status)]
- Related sprint work: [Sibling issues in the same sprint]

### Key Decisions (from comments)
[Distilled decisions and context from comments]
```

Omit sections that have no data (e.g., no sprint, no linked issues, no comments with decisions).

Present the structured task to the user. Use `AskUserQuestion` — header "Task review", question "Does this capture the task correctly?":
- **Looks good** — "Use this task description"
- **Adjust** — "I want to refine before continuing"

If "Adjust": use `AskUserQuestion` — header "Refinement", question "What would you like to change?" (free text). Apply the changes and present the updated version. Re-confirm.

### Save task context to file

After the user confirms the structured task, save it to a persistent file so downstream skills (`/optimus:tdd`, `/optimus:brainstorm`) can auto-detect it without copy-paste.

1. Create the `docs/jira/` directory at the project root if it doesn't exist
2. Write the structured task to `docs/jira/<ISSUE-KEY>.md` (e.g., `docs/jira/AUTH-456.md`) with YAML frontmatter:

```markdown
---
source: jira
issue: [ISSUE-KEY]
date: [YYYY-MM-DD]
---

[The full structured task content from above — Goal, Acceptance Criteria, Context, Key Decisions]
```

3. If a file for the same issue key already exists, overwrite it (the user re-fetched for fresh context)
4. Report the file path: "Task context saved to `docs/jira/<ISSUE-KEY>.md`"

## Step 5: Analyze Against Codebase

Read `$CLAUDE_PLUGIN_ROOT/skills/jira/references/jira-codebase-analysis.md` and follow the **Analysis Procedure** using the Goal and Acceptance Criteria from Step 4.

Present the **Impact Summary** to the user.

Use `AskUserQuestion` — header "Codebase impact", question "How would you like to use these findings?":
- **Update JIRA and local context** — "Add suggested criteria to the JIRA issue and enrich the local task file"
- **Update local context only** — "Add findings to `docs/jira/<ISSUE-KEY>.md` but don't touch JIRA"
- **Skip** — "Proceed without changes"

If **Update JIRA and local context**: update the `docs/jira/<ISSUE-KEY>.md` file following the **Task File Update** procedure in the reference, then proceed to Step 6 — include the suggested criteria from the codebase analysis if the user chooses to improve the JIRA description.

If **Update local context only**: update the `docs/jira/<ISSUE-KEY>.md` file following the **Task File Update** procedure. Proceed to Step 6.

If **Skip**: proceed to Step 6.

## Step 6: Improve JIRA Issue (optional)

Use `AskUserQuestion` — header "Improve issue", question "Would you like to improve this JIRA issue's description? This adds structured acceptance criteria and better formatting directly in JIRA.":
- **Improve description** — "Update the JIRA issue with the structured content above"
- **Skip** — "Keep the JIRA issue as-is"

If **Skip** → if the user chose "Update JIRA and local context" in Step 5, warn: "Note: the codebase-suggested criteria will not be added to JIRA. They are still saved in your local task file." Then proceed to Step 7.

If **Improve description**:

1. Generate an improved description for the JIRA issue:
   - Preserve the original description's intent and content
   - Add structured acceptance criteria (if not already present)
   - If the user chose "Update JIRA and local context" in Step 5, merge the suggested criteria from the codebase analysis into the acceptance criteria section
   - Improve formatting (headers, lists, clear sections)
   - Do not remove any information from the original

2. Present a before/after comparison to the user:

```
## Proposed JIRA Update: [Issue Key]

### Current Description
[Original description, truncated to 1000 chars if longer]

### Proposed Description
[Improved description]

### Changes
- [What was added/restructured — e.g., "Added 5 acceptance criteria",
  "Restructured into Goal/Criteria/Notes sections",
  "Merged 2 codebase-informed criteria from impact analysis"]
```

3. Use `AskUserQuestion` — header "Confirm update", question "Apply this update to the JIRA issue?":
   - **Apply** — "Update the JIRA issue now"
   - **Edit first** — "Let me adjust the proposed description"
   - **Cancel** — "Don't update the JIRA issue"

4. If **Apply**: use the MCP update tool to write the improved description. Report success or failure.
5. If **Edit first**: let the user describe changes, regenerate, and re-confirm.
6. If **Cancel**: proceed to Step 7 without writing.

## Step 7: Recommend Next Step

First, handle tech debt and refactoring tickets separately — they have a fixed route:

- **Refactoring / Tech debt** → "Recommend running `/optimus:refactor` to restructure the code. **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch."

For stories, features, and bugs, use the **Scope Assessment** from Step 5 as the primary complexity signal. When the scope assessment is inconclusive, supplement with the structured task's acceptance criteria count and context.

After giving the recommendation for any path above (including refactoring), also mention `/optimus:branch` if the user hasn't created a feature branch yet.

### Simple (codebase assessment: simple, or 1–3 acceptance criteria with single component)

> Recommend running `/optimus:tdd` to implement this test-first. It will auto-detect the task file at `docs/jira/<ISSUE-KEY>.md`. **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.

### Medium (codebase assessment: medium, or 4–6 acceptance criteria across 2–3 components)

> This task has a few moving parts — recommend exploring the codebase in plan mode before implementing.

Use `AskUserQuestion` — header "Plan mode", question "Would you like a plan-mode prompt for this task? It will help you explore the codebase and plan the implementation before coding.":
- **Generate prompt** — "Create a ready-to-paste plan-mode prompt"
- **Skip to TDD** — "I'll go straight to `/optimus:tdd`"

If **Generate prompt**: assemble a self-contained plan-mode prompt pre-filled from the structured task (and codebase impact findings if available from Step 5):

````
```
## Goal
[Goal from the structured task]

## Context
[Acceptance criteria + context fields + key decisions from the structured task.
If Step 5 produced a codebase impact summary, include the Files Affected and
Risks sections here.]

## Starting Hints
- Task context: docs/jira/<ISSUE-KEY>.md
[If Step 5 ran, add key files identified in the impact summary]

## What to Figure Out
1. Which existing files and modules need to be modified or extended?
2. What's the right implementation sequence given the acceptance criteria?
3. Are there existing patterns in the codebase to follow or reuse?
4. What are the risks or edge cases not covered by the acceptance criteria?

## Plan Deliverable
The plan should include:
- Proposed approach with rationale
- Files to create or modify, with what changes
- Implementation sequence and dependencies
- Test strategy for each acceptance criterion

## Scope
- Focus on: [component/area from the structured task context]
- Out of scope: [anything explicitly excluded in the JIRA issue]

## How this conversation should run
Treat this conversation as a review loop — validate the plan against the actual codebase and iterate with me. When I say I'm done iterating, acknowledge but do not write yet — plan mode is read-only. I will then toggle plan mode off and send a short follow-up message (e.g. "go"). On that follow-up, append a "Refined plan" section to `docs/jira/<ISSUE-KEY>.md` to capture the refined plan, and stop. I will start a fresh conversation to run `/optimus:tdd`.
```
````

When emitting both the plan-mode prompt above and the execution prompt below, substitute `<ISSUE-KEY>` with the real key so each pasted block is self-contained.

Tell the user:

> 1. Start a fresh Claude Code conversation in **plan mode** (CLI: press `Shift+Tab` until the mode indicator shows plan mode; other clients: use the equivalent toggle). Paste the prompt above.
> 2. Iterate with Claude. **Do not approve the plan** — approval executes immediately and skips `/optimus:tdd`'s Red-Green-Refactor discipline. When you're satisfied, tell Claude you're done iterating; Claude will acknowledge. Then toggle plan mode off using the same control **and send a short follow-up message (e.g. "go")** — Claude will append a "Refined plan" section to `docs/jira/<ISSUE-KEY>.md` in response.
> 3. Start a **second fresh conversation** and paste the execution prompt below.

Then emit the **execution prompt** as a second copyable block, pre-filled from the task file:

````
```
## Goal
Run `/optimus:tdd` to implement the refined plan in `docs/jira/<ISSUE-KEY>.md` test-first.

## Starting Hints
- JIRA task (with "Refined plan" section): docs/jira/<ISSUE-KEY>.md
- Acceptance criteria: [carry forward from the task file]

## Scope
- Focus on: [component/area from the structured task context]
- Out of scope: [anything explicitly excluded in the JIRA issue]
```
````

See `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md` for the full handoff convention and why plan mode is used review-only.

If **Skip to TDD**: Recommend running `/optimus:tdd` to implement this test-first. It will auto-detect the task file at `docs/jira/<ISSUE-KEY>.md`. **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.

### Complex (codebase assessment: complex, or 7+ acceptance criteria, multiple components, architecture/migration mentions, or unclear design direction)

> This task needs design thinking before implementation. Recommend running `/optimus:brainstorm` to explore design approaches — it will auto-detect the task file at `docs/jira/<ISSUE-KEY>.md`.

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
