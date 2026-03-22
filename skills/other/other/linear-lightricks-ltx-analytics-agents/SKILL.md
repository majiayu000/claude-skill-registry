---
name: linear
description: Creates and manages Linear issues for analytics work. Also posts weekly status reports to Slack. Use when someone asks to create an issue, track a task in Linear, link work to Linear, or send a status update.
---

# Linear Issue Manager

## When to use

**Issue Management:**
- "Create a Linear issue for {task}"
- "Track this in Linear"
- "Open an issue for {problem}"
- "File a bug/task/feature request"
- "Link this to Linear"

**Status Reporting:**
- "Send PA status to Slack"
- "Post weekly status update"
- "What's the status of PA teams?"
- "Send status for all PA teams"

## What it produces

**Issue Management:**
A Linear issue in one of the PA (Product Analytics) teams with:
- Clear title and description
- Appropriate team assignment
- User-selected status
- Optional PR linking

**Status Reporting:**
A weekly status report posted to #ltx-pa Slack channel with:
- All PA team issues (PA Missions, PA - PM, PA - BI) excluding Backlog, Done, Canceled
- Issues grouped by team, then by status (In Progress, In Review, Todo)
- Issue counts and links

## Teams

The skill works with 3 Product Analytics teams:

| Team | Team ID | Prefix | Use for |
|------|---------|--------|---------|
| **PA Missions** | `b3751c9a-e25e-44c0-9056-798c7e4169950` | `PAM` | Mission-critical analytics work, strategic initiatives |
| **PA - PM** | `b6437834-b873-4c8d-aa93-e4493bab58fd` | `PAPM` | Product Manager requests, feature analytics |
| **PA - BI** | `db3fac73-5bec-4179-8081-01533b38e4fa` | `PABI` | BI infrastructure, data platform, tooling |

**Default team:** PA Missions (for most analytics/data work)

**Note:** PA - BI uses different status naming than PA Missions/PM:
- PA Missions/PM: Backlog → Todo → In Progress → In Review → Done
- PA - BI: New requests → Ready to work → Currently in work → In Review → Done

---

## Workflows

### Flow A: Create Issue

```
PHASE 1: GATHER → Issue details
  ↓
PHASE 2: CONFIRM → Show preview, ask for status
  ↓
✋ USER APPROVES
  ↓
PHASE 3: CREATE → Create in Linear
  ↓
PHASE 4: REPORT → Share issue URL
```

### Flow B: Weekly Status Report

```
PHASE 1: QUERY → Fetch all PA team issues (exclude Backlog/Done/Canceled)
  ↓
PHASE 2: FORMAT → Group by team and status, format message
  ↓
PHASE 3: POST → Send to #ltx-pa Slack channel
  ↓
PHASE 4: CONFIRM → Report summary to user
```

---

## Flow A: Create Issue

## Phase 1: Gather

**Goal:** Collect all information needed for the issue.

1. **Determine team assignment:**
   - Ask the user which team this belongs to (if not obvious)
   - Default to PA Missions for general analytics work
   - Use PA - BI for BI infrastructure, data platform, and tooling work
   - Use PA - PM for product manager requests

2. **Collect issue details:**
   - **Title** - Clear, actionable (50-70 chars max)
   - **Description** - Context, problem statement, acceptance criteria
   - **Priority** - Urgent / High / Medium / Low / No priority (default: Medium)
   - **Labels** (optional) - bug, feature, documentation, dashboard, etc.

3. **Check for PR context:**
   - If the user is creating this while working on a PR, ask if they want to link it
   - Get PR number/URL if linking

---

## Phase 2: Confirm

**Goal:** Show the user what will be created and get status.

1. **Present issue preview:**
   ```
   ## Linear Issue Preview

   **Team:** {team_name} ({prefix})
   **Title:** {title}
   **Priority:** {priority}
   **Labels:** {labels if any}

   **Description:**
   {description}

   {If PR linking: **Linked PR:** #{pr_number}}
   ```

2. **Ask for status:**

   **CRITICAL:** NEVER default to "Triage". Always ask the user to choose from available statuses.

   **PA Missions / PA - PM statuses:**
   - **Backlog** - Planned but not started
   - **Todo** - Ready to work on
   - **In Progress** - Currently being worked on
   - **In Review** - Code complete, awaiting review
   - **Done** - Completed
   - **Canceled** - Won't do
   - **Duplicate** - Duplicate issue

   **PA - BI statuses** (different naming):
   - **New requests** - Backlog (planned but not started)
   - **Ready to work** - Todo (ready to work on)
   - **Currently in work** - In Progress (actively working)
   - **In Review** - Code complete, awaiting review
   - **Done** - Completed
   - **Canceled** - Won't do
   - **Duplicate** - Duplicate issue

   **Exception:** If this issue is being created by linking to an existing PR, automatically set status to "In Review" (no need to ask).

3. **Get user approval:**
   - Wait for explicit confirmation ("yes", "go ahead", "create it")
   - If changes needed, return to Phase 1

---

## Phase 3: Create

**Goal:** Create the issue in Linear via API.

1. **Use Linear MCP or API** to create the issue with:
   - Team ID (from the selected team)
   - Title
   - Description
   - Status (from Phase 2)
   - Priority
   - Labels (if any)

2. **If PR linking requested:**
   - Create attachment linking to the PR URL
   - If PR title doesn't include Linear key, suggest updating it to `[{PREFIX}-{ID}] {original title}`

---

## Phase 4: Report

**Goal:** Confirm creation and share the issue URL.

1. **Report to user:**
   ```
   ✅ Linear issue created: {issue_url}

   {PREFIX}-{ID}: {title}
   Team: {team_name}
   Status: {status}

   {If PR linked: Linked to PR #{pr_number}}

   {If PR title needs updating:
   💡 Tip: Update your PR title to include [{PREFIX}-{ID}] for better tracking}
   ```

2. **Copy issue key to clipboard** (if possible) for easy pasting

---

## Flow B: Weekly Status Report

### Phase 1: Query

**Goal:** Fetch all active issues from all PA teams.

1. **Query Linear API** for all PA team issues with filters:
   - **Teams:** Query all 3 teams:
     - PA Missions (`b3751c9a-e25e-44c0-9056-798c7e4169950`)
     - PA - PM (`b6437834-b873-4c8d-aa93-e4493bab58fd`)
     - PA - BI (`db3fac73-5bec-4179-8081-01533b38e4fa`)
   - **Exclude status types:** backlog, completed, canceled
     - This excludes: Backlog, New requests, Done, Canceled, Duplicate
   - **Include status types:** unstarted, started
     - PA Missions/PM: Todo, In Progress, In Review
     - PA - BI: Ready to work, Currently in work, In Review

2. **Group issues by team first, then by status within each team**

### Phase 2: Format

**Goal:** Create a clear, actionable status message for Slack.

1. **Format message** using this template:

   ```
   📊 *Product Analytics - Weekly Status*
   _Week of {date}_

   ## 🎯 PA Missions
   *🔄 In Progress* ({count})
   {for each issue:}
   • [{PREFIX}-{ID}] {title} - {assignee}
     {issue_url}

   *👀 In Review* ({count})
   {for each issue:}
   • [{PREFIX}-{ID}] {title} - {assignee}
     {issue_url}

   *📋 Todo* ({count})
   {for each issue:}
   • [{PREFIX}-{ID}] {title} - {assignee}
     {issue_url}

   ## 📊 PA - PM
   *🔄 In Progress* ({count})
   {for each issue:}
   • [{PREFIX}-{ID}] {title} - {assignee}
     {issue_url}

   *👀 In Review* ({count})
   {for each issue:}
   • [{PREFIX}-{ID}] {title} - {assignee}
     {issue_url}

   *📋 Todo* ({count})
   {for each issue:}
   • [{PREFIX}-{ID}] {title} - {assignee}
     {issue_url}

   ## 🔧 PA - BI
   *🔄 Currently in work* ({count})
   {for each issue:}
   • [{PREFIX}-{ID}] {title} - {assignee}
     {issue_url}

   *👀 In Review* ({count})
   {for each issue:}
   • [{PREFIX}-{ID}] {title} - {assignee}
     {issue_url}

   *📋 Ready to work* ({count})
   {for each issue:}
   • [{PREFIX}-{ID}] {title} - {assignee}
     {issue_url}

   ---
   *Total active issues:* {total_count} (PAM: {pam_count}, PAPM: {papm_count}, PABI: {pabi_count})
   ```

2. **Order sections** by team (PA Missions → PA - PM → PA - BI), then by workflow progression within each team: In Progress → In Review → Todo

3. **Include assignee info** (if available) or mark as "Unassigned"

4. **Skip empty sections** - If a team has no issues in a particular status, omit that status section

### Phase 3: Post

**Goal:** Send the formatted message to Slack.

1. **Post to Slack channel** #ltx-pa using Slack MCP

2. **Use thread-friendly format** - main message should be scannable, details in thread if needed

### Phase 4: Confirm

**Goal:** Confirm successful posting to the user.

1. **Report to user:**
   ```
   ✅ Posted PA team status to #ltx-pa

   Summary by team:
   - PA Missions: {pam_count} active issues
   - PA - PM: {papm_count} active issues
   - PA - BI: {pabi_count} active issues
   - Total active: {total}

   {slack_message_url}
   ```

---

## Rules

**Issue Creation (Flow A):**
1. **Never default status to "Triage".** Always ask the user (except for PR-linked issues which auto-set to "In Review").
2. **Default team to PA Missions** unless the context clearly suggests PA - BI (infrastructure/tooling) or PA - PM (PM requests).
3. **Keep titles actionable** - Start with a verb when possible (e.g., "Add retention cohort to dashboard", "Fix null handling in funnel query").
4. **Include context in description** - Link to related dashboards, PRs, Slack threads, or docs.
5. **Use labels** - Help categorize: `bug`, `feature`, `dashboard`, `data-quality`, `performance`, etc.
6. **Link PRs when relevant** - If work is already in progress, link the PR to the issue.

**Status Reporting (Flow B):**
7. **All PA teams** - Weekly reports include all 3 PA teams (PA Missions, PA - PM, PA - BI), grouped by team.
8. **Exclude completed/inactive** - Never include status types: backlog, completed, canceled (Backlog, New requests, Done, Canceled, Duplicate).
9. **Post to #ltx-pa** - Always use the ltx-pa Slack channel for status reports.
10. **Show assignees** - Include who's working on each issue (or mark "Unassigned").
11. **Respect team naming** - PA - BI uses different status names (Currently in work, Ready to work) than other teams.

---

## Examples

### Example 1: Dashboard bug

**User:** "Create an issue for the retention dashboard showing wrong numbers"

**Phase 1 - Gather:**
- Team: PA Missions (dashboard analytics issue - default)
- Title: "Fix retention calculation in LTX Studio dashboard"
- Description: "The retention dashboard is showing inflated D7 numbers. Appears to be counting same-day returns. Need to add temporal ordering to the retention query."
- Priority: High
- Labels: bug, dashboard

**Phase 2 - Confirm & Status:**
Ask user: "What status should I set? (Backlog / Todo / In Progress / etc.)"
User: "Todo"

**Phase 3 - Create:**
Create PAM-XXX in PA Missions team with status "Todo"

**Phase 4 - Report:**
"✅ Created PAM-234: Fix retention calculation in LTX Studio dashboard"

---

### Example 2: PM request with PR

**User:** "Track this work in Linear" (while working on PR #15)

**Phase 1 - Gather:**
- Detect PR context (PR #15 for "Add enterprise segmentation to usage dashboard")
- Team: PA - PM (product analytics request)
- Title: "Add enterprise segmentation to usage dashboard"
- Description: "PM requested breakdown by enterprise vs self-serve in the usage dashboard. Adding segmentation using the standard CTEs from bq-schema.md."
- Priority: Medium
- Link to PR #15

**Phase 2 - Confirm & Status:**
AUTO-SET status to "In Review" (because PR exists)

**Phase 3 - Create:**
Create PAPM-XXX linked to PR #15

**Phase 4 - Report:**
"✅ Created PAPM-89: Add enterprise segmentation to usage dashboard
Linked to PR #15
Status: In Review

💡 Tip: Update PR title to [PAPM-89] Add enterprise segmentation to usage dashboard"

---

### Example 3: Weekly status report

**User:** "Send PA status to Slack"

**Phase 1 - Query:**
- Query Linear for all PA team issues
- Filter: Exclude status types backlog, completed, canceled
- Found across all teams:
  - PA Missions: 2 In Progress, 1 In Review, 3 Todo
  - PA - PM: 1 In Progress, 2 Todo
  - PA - BI: 1 Currently in work, 1 In Review, 1 Ready to work

**Phase 2 - Format:**
```
📊 *Product Analytics - Weekly Status*
_Week of Feb 23, 2026_

## 🎯 PA Missions
*🔄 In Progress* (2)
• [PAM-42] Build revenue attribution dashboard - @sarah
  https://linear.app/ltx/issue/PAM-42
• [PAM-38] Add LTX Model cost tracking - @daniel
  https://linear.app/ltx/issue/PAM-38

*👀 In Review* (1)
• [PAM-45] Fix enterprise segmentation logic - @alex
  https://linear.app/ltx/issue/PAM-45

*📋 Todo* (3)
• [PAM-47] Add API usage breakdown by endpoint - Unassigned
  https://linear.app/ltx/issue/PAM-47
• [PAM-46] Create cohort retention dashboard - Unassigned
  https://linear.app/ltx/issue/PAM-46
• [PAM-44] Optimize funnel query performance - @sarah
  https://linear.app/ltx/issue/PAM-44

## 📊 PA - PM
*🔄 In Progress* (1)
• [PAPM-23] Add usage dashboard for new feature - @mike
  https://linear.app/ltx/issue/PAPM-23

*📋 Todo* (2)
• [PAPM-24] Create retention cohort analysis - @emma
  https://linear.app/ltx/issue/PAPM-24
• [PAPM-22] Fix funnel conversion tracking - Unassigned
  https://linear.app/ltx/issue/PAPM-22

## 🔧 PA - BI
*🔄 Currently in work* (1)
• [PABI-87] Migrate to new BigQuery tables - @jordan
  https://linear.app/ltx/issue/PABI-87

*👀 In Review* (1)
• [PABI-88] Optimize BigQuery costs - @alex
  https://linear.app/ltx/issue/PABI-88

*📋 Ready to work* (1)
• [PABI-89] Update dbt models for new schema - Unassigned
  https://linear.app/ltx/issue/PABI-89

---
*Total active issues:* 12 (PAM: 6, PAPM: 3, PABI: 3)
```

**Phase 3 - Post:**
Post formatted message to #ltx-pa

**Phase 4 - Confirm:**
"✅ Posted PA team status to #ltx-pa

Summary by team:
- PA Missions: 6 active issues
- PA - PM: 3 active issues
- PA - BI: 3 active issues
- Total active: 12

https://lightricks.slack.com/archives/C123456/p1234567890"

---

## MCP Requirements

**Linear MCP (required for both flows):**
- Creating issues
- Setting status, priority, labels
- Linking attachments (PRs)
- Querying teams and workflows
- Fetching issues from all 3 PA teams for status reports

**Slack MCP (required for Flow B only):**
- Posting status reports to #ltx-pa channel

If Linear MCP is not available, provide manual instructions for creating the issue.
If Slack MCP is not available for status reports, format the report and provide it to the user to post manually.
