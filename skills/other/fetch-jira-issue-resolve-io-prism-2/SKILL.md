---
name: fetch-jira-issue
description: Use when user mentions a Jira issue key (e.g., PLAT-123) or needs context from Jira. Retrieves and formats issue details for PRISM agent workflows.
---
# Task: Fetch Jira Issue

## Purpose
Retrieve and format Jira issue details (Epic, Story, Bug, Task) to provide context for PRISM agent workflows.

## Quick Start

1. Detect or receive Jira issue key (e.g., PLAT-123)
2. Load Jira config from `core-config.yaml`
3. Call Jira REST API via curl
4. Format response for PRISM workflow context
5. Return structured issue details

## When to Use
- User mentions a Jira issue key (e.g., PLAT-123)
- Agent needs context for decomposition, validation, or implementation
- Explicit `*jira {issueKey}` command

## Prerequisites
- Jira integration enabled in core-config.yaml
- Valid Jira credentials configured
- Issue key provided or detected

## Process

### Step 1: Detect or Request Issue Key
**If issue key mentioned in user message:**
- Extract issue key using pattern from config (default: `[A-Z]+-\d+`)
- Inform user: "I found reference to {issueKey}. Let me fetch the details..."

**If no issue key detected:**
- Ask user: "Great! Let's take a look at that. Do you have a JIRA ticket number so I can get more context?"
- Wait for user response
- If provided, proceed with fetch
- If not provided or user declines, continue without Jira context

### Step 2: Read Jira Configuration
**Load config values from `../core-config.yaml`:**
```yaml
jira:
  baseUrl: {url}
  email: {email}
  token: {token}
  defaultProject: {project}
```

**Validate configuration:**
- Ensure jira.enabled is true
- Verify all required fields present
- If missing, inform user and proceed without Jira context

### Step 3: Construct API Request
**Build Jira REST API URL:**
```
{baseUrl}/rest/api/3/issue/{issueKey}
```

**Prepare authentication:**
- Use Basic Auth with email:token
- Format: Authorization header with base64(email:token)

**For WebFetch, construct authenticated URL:**
```
https://{email}:{token}@{hostname}/rest/api/3/issue/{issueKey}
```

### Step 4: Fetch Issue Details
**Use WebFetch tool with extraction prompt:**
```
Extract and format the following information from this Jira issue:

## Issue Identification
- Issue Key and Type (Epic/Story/Bug/Task/etc)
- Status and Priority
- Project and Components

## Content
- Summary (title)
- Description (full text, preserve formatting)
- Acceptance Criteria (if present in description or as custom field)

## People & Dates
- Assignee
- Reporter
- Created and Updated dates
- Due Date (if set)

## Estimation & Progress
- Story Points (if applicable)
- Original Estimate
- Time Spent
- Sprint (if applicable)

## Relationships
- Epic Link (what epic this belongs to)
- Parent Issue (if subtask)
- Child Issues (count and list)
- Linked Issues (Blocks, Blocked by, Relates to, etc.)

## Additional Context
- Labels
- Fix Versions
- Last 3 comments (with author and date)
- Attachments (count and types)

Format as a clear, structured markdown summary optimized for development context.
If any field is missing or empty, note it as "Not specified" rather than omitting.
```

### Step 5: Handle Response

**Success (200 OK):**
- Format and display issue summary to user
- Store issue data in conversation context for agent reference
- Include clickable link: `[{issueKey}]({baseUrl}/browse/{issueKey})`
- Proceed with agent workflow using fetched context

**Issue Not Found (404):**
- Display: "Could not find Jira issue {issueKey}. Please verify the issue key."
- Ask user if they want to:
  - Try a different issue key
  - Search for issues
  - Proceed without Jira context

**Permission Denied (403):**
- Display: "Access denied to {issueKey}. This may require different Jira permissions."
- Suggest:
  - Verify issue key is correct
  - Check Jira permissions for the account
  - Contact Jira administrator
- Offer to proceed without Jira context

**Authentication Failed (401):**
- Display: "Jira authentication failed. Please check credentials in core-config.yaml."
- Do not proceed with Jira operations
- Continue agent workflow without Jira context

**Network/API Error:**
- Display: "Unable to connect to Jira at this time. Proceeding without issue context."
- Log error details for troubleshooting
- Continue agent workflow without Jira context

### Step 6: Present Formatted Summary

**Display format:**
```markdown
## ðŸ“‹ {IssueKey}: {Summary}

**Type:** {Type} | **Status:** {Status} | **Priority:** {Priority}
**Assignee:** {Assignee} | **Reporter:** {Reporter}

### Description
{Description}

### Acceptance Criteria
{Acceptance Criteria or "Not specified"}

### Epic Context
{Epic Link and summary, if applicable}

### Related Issues
- Blocks: {list}
- Blocked by: {list}
- Relates to: {list}
- Child Issues: {count} issues

### Estimation
- Story Points: {points}
- Time Spent: {time}

### Additional Details
- Labels: {labels}
- Components: {components}
- Last Updated: {date}

[View in Jira]({link})
```

### Step 7: Context Integration

**For different issue types:**

**Epic:**
- Fetch child issues count
- Extract epic goals and scope
- Identify existing stories to avoid duplication

**Story:**
- Extract acceptance criteria carefully
- Note dependencies and blockers
- Check for technical notes in comments

**Bug:**
- Extract reproduction steps from description
- Review existing comments for additional context
- Note severity and customer impact

**Task:**
- Extract deliverables and requirements
- Check for related technical documentation
- Note any dependencies

### Step 8: Offer Follow-up Actions

**Based on issue type and agent, offer:**
- "Would you like me to fetch the epic details?" (if story has epic link)
- "Shall I retrieve all child stories?" (if epic has children)
- "Would you like to see the linked issues?" (if has dependencies)
- "Ready to proceed with {agent task}?" (to continue workflow)

## Error Recovery

**Invalid Issue Key Format:**
- Display: "'{input}' doesn't match Jira issue key format (e.g., PLAT-123)"
- Ask for correct issue key or offer to proceed without

**Multiple Issue Keys Detected:**
- List all detected keys
- Ask user which one to fetch first
- Offer to fetch all

**Jira Configuration Missing:**
- Display: "Jira integration not configured. Proceeding without issue context."
- Continue agent workflow
- Do not block on missing Jira config

## Agent-Specific Integration

**Story Master (sm):**
- When decomposing epic: fetch epic + all existing child stories
- When creating story: check for duplicate summaries in epic
- When estimating: review similar completed stories (if available)

**Product Owner (po):**
- When validating story: fetch full acceptance criteria
- When refining: check for missing fields or incomplete descriptions
- When prioritizing: review linked dependencies

**Support (support):**
- When investigating bug: fetch full reproduction steps and comments
- When creating tasks: link to original bug report
- When escalating: include all bug context

**QA (qa):**
- When creating tests: fetch acceptance criteria and edge cases
- When validating: check test requirements from story
- When reporting: link test results to original story

**Dev (dev):**
- When implementing: fetch technical notes from comments
- When fixing bug: review reproduction steps
- When completing: verify acceptance criteria met

**Architect (architect):**
- When reviewing epic: fetch scope and technical requirements
- When designing: review architectural decisions in comments
- When approving: check component relationships

**Peer (peer):**
- When reviewing: fetch story context and acceptance criteria
- When approving: verify implementation matches requirements
- When suggesting changes: reference architectural constraints

## Best Practices

1. **Always ask first** if context is ambiguous
2. **Cache fetched data** for the conversation session
3. **Format consistently** for readability
4. **Handle errors gracefully** - never block workflow on Jira failures
5. **Respect privacy** - only fetch explicitly referenced issues
6. **Link issues** - always include clickable Jira links
7. **Extract acceptance criteria carefully** - critical for implementation
8. **Note blocking issues** - important for planning
9. **Preserve formatting** - maintain description structure
10. **Offer follow-ups** - suggest related fetches when relevant

## Output

**On Success:**
- Formatted issue summary displayed to user
- Issue context available for agent workflow
- Clickable Jira link included
- Follow-up actions offered

**On Failure:**
- Clear error message
- Recovery options offered
- Workflow continues without Jira context
- No blocking behavior

## Completion Criteria

- Issue details retrieved or error handled gracefully
- Formatted summary displayed to user (if successful)
- Issue context integrated into agent workflow
- User can proceed with requested task
- No workflow blocking on Jira failures

