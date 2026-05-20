---
name: eod
description: Generate a concise end-of-day summary from GitHub activity in the last 24 hours - commits, issues, and PRs
---

# End-of-Day Summary

This skill orchestrates two specialized agents to generate a concise summary of your GitHub activity for the current day.

## What This Skill Does

1. **Extracts GitHub activity data** using the `github-analyzer-agent` agent
2. **Generates a beautiful summary** using the `summarizer-agent` agent

The result is a conversational, scannable update perfect for sharing with teammates.

## Usage

Ask Claude naturally: "Generate my end-of-day summary"

Or invoke directly with the Skill tool: `shipmate:eod`

## Configuration

This skill can be configured via `shipmate.yaml` in either:

- `~/.claude/shipmate.yaml` (global)
- `<project>/.claude/shipmate.yaml` (project-specific, overrides global)

See `config.example.yaml` for configuration options.

## MANDATORY FIRST STEP: Create Todo List

**BEFORE DOING ANYTHING ELSE**, you MUST use the TodoWrite tool to create a task list with these EXACT step names:

1. "Detect GitHub organizations and username"
2. "Ask user to select activity scope"
3. "Extract GitHub activity data"
4. "Extract Claude Code sessions (if enabled)"
5. "Analyze activity and identify themes"
6. "Ask user to select main topics"
7. "Generate conversational summary"
8. "Present summary to user"
9. "Post to enabled integrations (if configured)"

Mark the first todo as `in_progress` immediately after creating the list.

**Why:** This provides visibility to the user and ensures consistent progress tracking across all skill runs.

## Process

### Step 1: Detect GitHub Organizations (MANDATORY - DO NOT SKIP)

**CRITICAL:** You MUST complete this step before proceeding. Do NOT jump to Step 3.

Run these commands to detect organizations and get the username:

```bash
gh api user/orgs --jq '.[].login'
```

```bash
gh api user --jq '.login'
```

Store both the list of organizations and the username.

### Step 2: Ask User for Scope (MANDATORY - DO NOT SKIP)

**CRITICAL:** You MUST ask the user which scope they want. Do NOT assume or skip this step.

Use the AskUserQuestion tool with this EXACT question:

**Question:** "Which GitHub activity would you like to include in your end-of-day summary?"

**Options** (create one option for each scenario):

- **Personal account only** ({username}) - "Only activity from your personal GitHub account"
- **Organization: {org_name}** - "Only activity from the {org_name} organization" (one option per org discovered)
- **All accounts** - "Activity from your personal account and all organizations"

**IMPORTANT:**

- If the user belongs to multiple organizations, include one option for EACH organization
- Always include the "Personal account only" option
- Always include the "All accounts" option
- Do NOT proceed to Step 3 until the user has made a selection

Store the user's selection for use in Step 3.

### Step 2.5: Read Configuration and Detect Script Paths

**A. Read configuration from `shipmate.yaml`:**

Check for configuration in these locations (project-specific overrides global):

- `<project>/.claude/shipmate.yaml`
- `~/.claude/shipmate.yaml`

Extract these values from the `claude_sessions` section:

- `enabled` (default: true)
- `time_window_hours` (default: 24)
- `correlation_window_hours` (default: 2)
- `min_duration_minutes` (default: 2)

Extract these values from the `integrations` section:

- `notion.enabled` (default: false)
- `notion.daily_log_url` (required if notion.enabled is true)

Set `HAS_INTEGRATIONS` flag:

- `true` if any integration is enabled (e.g., `notion.enabled` is true)
- `false` if no integrations are enabled

**B. Detect script paths for agents:**

Run these commands separately to find the shipmate plugin directory and set script paths:

```bash
find ~/.claude/plugins -name "shipmate" -type d 2>/dev/null | head -1
```

If the command returns a path (plugin is installed):

- Set `GITHUB_SCRIPT` to `{plugin_dir}/scripts/fetch-github-activity.sh`
- Set `CLAUDE_SCRIPT` to `{plugin_dir}/scripts/parse-claude-sessions.js`

If the command returns nothing (running locally):

- Set `GITHUB_SCRIPT` to `./scripts/fetch-github-activity.sh`
- Set `CLAUDE_SCRIPT` to `./scripts/parse-claude-sessions.js`

Store these paths and flags for use in later steps.

### Step 3: Invoke Data Extraction Agents in Parallel

**Mark todo #2 as completed, todos #3 and #4 as in_progress.**

**IMPORTANT: Run both agents in PARALLEL using a single message with TWO Task tool calls.**

**Agent 1 - GitHub Analyzer:**

Use the Task tool to invoke the `shipmate:github-analyzer-agent` agent (subagent_type="shipmate:github-analyzer-agent"):

```text
Please extract GitHub activity data for the last 24 hours with the following scope: [user's selection from Step 2]

Use the bundled script at this path: {GITHUB_SCRIPT from Step 2.5}

Run it as:
{GITHUB_SCRIPT} [scope] {username} [{org_name}]

Where:
- scope: "personal", "org", or "all" based on user selection
- username: {username from Step 1}
- org_name: {org_name from Step 1} (only if scope is "org")

The script returns consolidated JSON with commits, issues, and PRs.
```

**Agent 2 - Claude Analyzer (Conditional):**

**Check if Claude sessions integration is enabled** from the configuration read in Step 2.5.

**If `claude_sessions.enabled` is true:**

Use the Task tool to invoke the `shipmate:claude-analyzer-agent` agent (subagent_type="shipmate:claude-analyzer-agent", model="haiku") **IN THE SAME MESSAGE as Agent 1**:

```text
Extract Claude Code sessions from the last {time_window_hours} hours with minimum duration {min_duration_minutes} minutes.

Use the bundled script at this path: {CLAUDE_SCRIPT from Step 2.5}

Run it as:
node {CLAUDE_SCRIPT} {time_window_hours} {min_duration_minutes}

The script returns JSON with session metadata including:
- session_id, project_path
- start_time, end_time, duration_minutes
- message_count, summary
- tool_usage (file_edits, bash_commands, reads)
- metadata (time_window_hours, min_duration_minutes, total_sessions)
```

**If `claude_sessions.enabled` is false:**

Skip the Claude analyzer agent. Set `CLAUDE_SESSIONS` to empty result:

```json
{
  "sessions": [],
  "metadata": {
    "time_window_hours": 24,
    "min_duration_minutes": 2,
    "total_sessions": 0
  }
}
```

**IMPORTANT:**

- Launch both agents in parallel (single message with 2 Task calls) when sessions are enabled
- Use Haiku model for Claude analyzer (fast, cheap execution)
- Both agents run independently and return results simultaneously
- Store GitHub data in `GITHUB_ACTIVITIES` variable
- Store Claude data in `CLAUDE_SESSIONS` variable

Once both agents return data (or Claude sessions disabled), mark todos #3 and #4 as completed.

### Step 4: Analyze Activity and Identify Key Themes

**Mark todo #5 as in_progress.**

Review the data from Step 3 and identify distinct themes/topics based on:

- Issue bodies and titles (what questions were being answered?)
- Commit messages and patterns
- Repositories affected
- Type of work (investigation, feature, bugfix, tooling, etc.)

For each theme, create a clear, descriptive label like:

- "Investigated AWS infrastructure"
- "Investigated Railway deployments"
- "Investigated Auth0 setup"
- "Set up secret detection"
- "Added markdown linting"
- "Documentation improvements"

**IMPORTANT**: Identify ALL distinct themes, not just major ones. Include both substantial investigations and smaller tasks.

### Step 4.5: Correlate Claude Sessions with GitHub Activity (Conditional)

**Before marking todo #5 as completed**, check if correlation is needed.

**If `CLAUDE_SESSIONS.metadata.total_sessions` is 0:**

- Skip correlation entirely (no sessions to correlate)
- Set `ENRICHED_ACTIVITIES` to `GITHUB_ACTIVITIES` (pass through unchanged)
- Set `ORPHANED_SESSIONS` to empty array
- Mark todo #5 as completed and proceed to Step 5

**If `CLAUDE_SESSIONS.metadata.total_sessions` > 0:**

Use the Task tool to invoke the `shipmate:correlation-agent` agent (subagent_type="shipmate:correlation-agent", model="haiku"):

```text
Correlate Claude Code sessions with GitHub activities using time proximity and path matching.

Input:
- GitHub Activities: {JSON from Step 3}
- Claude Sessions: {JSON from Step 3}
- Correlation Window: {correlation_window_hours from config}

Match sessions to activities by:
1. Path matching (normalized repo names)
2. Time proximity (±{correlation_window_hours} hours)

Return enriched activities with related_sessions and identify orphaned sessions (investigation work without commits).
```

**IMPORTANT:**

- Use Haiku model for fast, cheap correlation
- The agent will return enriched activities with `related_sessions` arrays
- Orphaned sessions represent investigation/exploration work
- Store the agent's output in `ENRICHED_ACTIVITIES` and `ORPHANED_SESSIONS` for use in Step 6

Once the agent returns data (or correlation was skipped), mark todo #5 as completed.

### Step 5: Ask User to Select Main Topics

**Mark todo #6 as in_progress.**

Use the AskUserQuestion tool with multiSelect enabled:

**Question:** "Which topics should be highlighted as main accomplishments? (Select 2-4. Everything else will be grouped as 'Housekeeping')"

**Options**: Create one option for each theme identified in Step 4, ordered by estimated importance/time spent (most significant first)

Example:

```text
- "Investigated AWS infrastructure" - "Documented IAM setup, S3 buckets, VPC config, and admin access"
- "Investigated Railway deployments" - "Found two projects, identified active vs inactive deployments"
- "Set up secret detection" - "Added pre-commit hooks with gitleaks to prevent credential leaks"
- "Added markdown linting" - "Configured markdownlint-cli2 with auto-fix"
```

Store the user's selections (2-4 topics).

Once the user has made their selections, mark todo #6 as completed.

### Step 6: Invoke Activity Summarizer Agent

**Mark todo #7 as in_progress.**

Use the Task tool to invoke the `shipmate:summarizer-agent` agent (subagent_type="shipmate:summarizer-agent"):

```text
Please create a team standup summary from this GitHub activity data:

[Paste the enriched GitHub activities from Step 4.5, including any related_sessions]

Orphaned Claude sessions (investigation work without commits):
[Paste orphaned sessions from Step 4.5, if any]

The user has selected these topics to highlight as main accomplishments:
[List the topics selected in Step 5]

Generate a conversational summary following the format with:
- Selected topics as separate bullets with detailed findings and insights
- All other activities grouped as "Housekeeping"
- Plain URLs to documentation artifacts
- Past tense, casual tone
- Weave in session insights naturally where related_sessions exist (see agent instructions for guidance)
```

**IMPORTANT**:

- Pass the enriched GitHub activities with related_sessions (from Step 4.5)
- Pass orphaned sessions separately
- Include correlation window hours in context
- Clearly indicate which topics the user selected to highlight
- Everything NOT selected should be grouped into "Housekeeping"
- The agent will return the formatted summary

Once the agent returns the summary, mark todo #7 as completed.

### Step 7: Present Summary to User

**Mark todo #8 as in_progress.**

Display the summary returned by the summarizer agent.

**Optional Polish**: If the `elements-of-style:writing-clearly-and-concisely` skill is available, you may optionally use it to polish the summary further, but the summarizer agent already applies these principles.

Once the summary is displayed, mark todo #8 as completed.

### Step 8: Post to Enabled Integrations (if configured)

**Mark todo #9 as in_progress.**

Check the `HAS_INTEGRATIONS` flag set in Step 2.5.

**If `HAS_INTEGRATIONS` is false:**

- Skip integration posting entirely
- Mark todo #9 as completed
- You're done!

**If `HAS_INTEGRATIONS` is true:**

Proceed to Step 9 to post to enabled integrations.

### Step 9: Post to Notion Daily Log (if enabled)

If Notion integration is enabled in config:

1. Get today's date in "Month Day, Year" format (e.g., "November 4, 2025")
2. Fetch the Daily Log page URL from config: `integrations.notion.daily_log_url`
3. Format the summary using the user's preferred bullet format:

```markdown
## {Date}

### What I accomplished today

- **{Topic 1}** - {Description from summary}
 - [{Link text}]({{URL}})
- **{Topic 2}** - {Description from summary}
 - [{Link text}]({{URL}})
- **{Topic 3}** - {Description from summary}
 - [{Link text}]({{URL}})
- **Housekeeping** - {Description from summary}
```

**IMPORTANT Formatting Rules**:

- Each main accomplishment is a top-level bullet with bold topic name
- Key artifacts (1-3 per topic) are nested bullets (indented with tab) under each accomplishment
- Include the most relevant links: documentation files, PRs, and issues that capture the work
- Use plain markdown links like `[Auth0 Documentation]({{URL}})` or `[PR #123]({{URL}})`
- Extract actual GitHub URLs from the summary text and raw activity data
- Prioritize comprehensive documentation links over minor commits
- The Housekeeping item does NOT have nested links unless there are specific artifacts to link

1. If the page already has content, prepend the new entry at the top (most recent first)
2. If the page is blank, just add the new entry
3. Use the `mcp__notion__notion-update-page` tool with appropriate command (`replace_content` or `insert_content_after`)

Once posted to Notion (or if Notion is not enabled), mark todo #8 as completed.

**Example of final Notion format**:

```markdown
## November 4, 2025

### What I accomplished today

- **Investigated Auth0 setup** - Dug through the whole Auth0 configuration to see what we're actually using. Found we have one production tenant with three main applications. Turns out we're using Google and Microsoft for social logins, have MFA set up but not enforced, and have a bunch of roles configured. Documented all the apps, APIs, connections, rules, hooks, and who has admin access.
 - [Auth0 Documentation]({{https://github.com/example-org/docs/blob/main/infrastructure/auth0.md}})
 - [Issue #7: Auth0 Configuration Inventory]({{https://github.com/example-org/docs/issues/7}})
- **Investigated AWS infrastructure** - Went through the AWS account to figure out what we have. Found IAM users and roles, data in S3 buckets, VPC configuration, and mapped out who has admin access. Got it all documented so we can plan the migration.
 - [AWS Documentation]({{https://github.com/example-org/docs/blob/main/infrastructure/aws.md}})
- **Investigated deployment process** - Figured out how we actually ship code to production. Frontend deploys manually, backend auto-deploys from GitHub.
 - [Deployment Process Documentation]({{https://github.com/example-org/docs/blob/main/infrastructure/deployment-process.md}})
 - [Issue #5]({{https://github.com/example-org/docs/issues/5}})
- **Housekeeping** - Set up pre-commit hooks with gitleaks to prevent secrets from leaking into the repo, added markdownlint for documentation quality.
```

## Agent Roles

### github-analyzer-agent

- **Specialty**: GitHub CLI (`gh`) expertise
- **Tools**: Bash
- **Model**: Haiku (fast, cost-effective for data extraction)
- **Output**: Structured JSON data about commits, issues, PRs

### summarizer-agent

- **Specialty**: Writing conversational, scannable summaries
- **Tools**: None (pure analysis and writing)
- **Model**: Sonnet (better at nuanced writing)
- **Output**: Formatted markdown summary ready to share

## Why Two Agents?

**Separation of Concerns**:

- **Analyzer** focuses on technical data gathering (parallel queries, timezone handling, error handling)
- **Summarizer** focuses on human communication (tone, grouping, insights)

**Optimized Models**:

- Use fast/cheap Haiku for repetitive data extraction
- Use smart Sonnet for nuanced writing and analysis

**Maintainability**:

- Each agent has a single, clear responsibility
- Can improve or swap agents independently
- Easier to test and debug

## Important Notes

- **Performance**: The analyzer agent runs all GitHub queries in parallel (~2-3 seconds total)
- **Time Range**: Last 24 hours from current time (not calendar day)
- **Scope**: Supports personal, organization-specific, or all-account views
- **Artifacts**: Includes links to documentation produced
- **Tone**: Conversational and scannable, optimized for team standups

## Error Handling

If the github-analyzer-agent fails:

- Check `gh auth status`
- Verify `gh` CLI is installed (requires 2.23.0+)
- Verify organization membership for org-scoped queries

If the summarizer-agent produces unexpected format:

- Ensure you passed complete raw data from analyzer
- Verify the analyzer included issue bodies for closed issues

## Customization

To customize:

- Edit `agents/github-analyzer-agent.md` for different data sources
- Edit `agents/summarizer-agent.md` for different summary formats
- Modify this skill to change orchestration logic
- Add new integrations in `integrations/` directory

## Example Flow

```text
User: /shipmate:eod

Skill: [Detects orgs: example-org]
Skill: [Asks user: "Personal, example-org, or all?"]
User: "example-org"

Skill: [Invokes github-analyzer-agent]
Analyzer: [Runs 5 parallel gh queries, returns JSON]

Skill: [Analyzes data, identifies themes]
Skill: [Presents themes to user with multiSelect question]
Themes identified:
  - Investigated AWS infrastructure
  - Investigated Railway deployments
  - Investigated Auth0 setup
  - Investigated deployment process
  - Set up secret detection
  - Added markdown linting
  - Documentation improvements

User: [Selects: AWS, Railway, Auth0, Deployment process]

Skill: [Invokes summarizer-agent with data + selected topics]
Summarizer: [Creates summary with 4 main bullets + Housekeeping group]

Skill: [Presents summary to user]
Skill: [Checks config for enabled integrations]
Skill: [If Notion enabled, posts to Notion Daily Log]
Skill: "Posted to Notion Daily Log!" (if applicable)
```

## Files

This skill uses:

- `agents/github-analyzer-agent.md` - Data extraction agent
- `agents/summarizer-agent.md` - Summary writing agent
- `skills/shipmate:end-of-day-summary/SKILL.md` - This orchestration skill
- `commands/shipmate:eod.md` - Slash command shortcut
- `integrations/notion/` - Optional Notion integration

---

**Version:** 1.1.5  
**Last Updated:** 2025-11-05
