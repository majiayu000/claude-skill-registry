---
name: define-issue
description: Create well-defined issues (bugs, features, tasks) using Socratic questioning to eliminate ambiguity. Use when creating new Linear or Jira issues, when the user mentions Linear, Jira, or needs to define work items with proper acceptance criteria and relationships.
invocation: /define
---

<objective>
Guide the creation of precise, unambiguous issues through the Socratic method. Ask targeted questions to uncover edge cases, acceptance criteria, relationships, and constraints before creating the issue. A well-defined issue prevents thrashing and enables clear work execution.
</objective>

<backend_detection>
Read backend from mobius config (`mobius.config.yaml` or `~/.config/mobius/config.yaml`).
Default to 'linear' if not specified.

```yaml
# mobius.config.yaml
backend: linear  # or 'jira'
```

The backend determines which MCP tools to use for issue operations.
</backend_detection>

<backend_context>
<linear>
**Linear MCP Tools**:
- `mcp__plugin_linear_linear__create_issue` - Create issues
- `mcp__plugin_linear_linear__list_issues` - Search existing issues
- `mcp__plugin_linear_linear__get_issue` - Get issue details
- `mcp__plugin_linear_linear__list_teams` - List available teams
- `mcp__plugin_linear_linear__list_issue_labels` - List available labels

**Linear Concepts**:
- **States**: Backlog, Todo, In Progress, Done, Canceled, Duplicate
- **Labels**: Bug, Feature, Improvement (and custom labels)
- **Priority**: 0 (No priority), 1 (Urgent), 2 (High), 3 (Normal), 4 (Low)
- **Relationships**: blocks, blockedBy, relatedTo, duplicateOf
- **Hierarchy**: Issues can have parent issues (sub-issues)
</linear>

<jira>
**Jira MCP Tools**:
- `mcp_plugin_atlassian_jira__create_issue` - Create issues
- `mcp_plugin_atlassian_jira__list_issues` - Search existing issues
- `mcp_plugin_atlassian_jira__get_issue` - Get issue details
- `mcp_plugin_atlassian_jira__list_projects` - List available projects

**Jira Configuration**:
Requires `project_key` from jira config section:

```yaml
# mobius.config.yaml
backend: jira
jira:
  base_url: https://yourcompany.atlassian.net
  project_key: PROJ
```

**Jira Concepts**:
- **Statuses**: To Do, In Progress, Done (varies by workflow)
- **Issue Types**: Bug, Story, Task, Epic, Sub-task
- **Priority**: Highest, High, Medium, Low, Lowest
- **Links**: blocks, is blocked by, relates to, duplicates
- **Hierarchy**: Epics contain Stories/Tasks; Tasks can have Sub-tasks
</jira>
</backend_context>

<quick_start>
<initial_gate>
**CRITICAL - Run this BEFORE investigation**

If user provides no context (just invoked the skill), use AskUserQuestion:

Question: "What kind of issue do you need to create?"

Options:
1. **Bug report** - Something is broken or not working as expected
2. **Feature request** - New capability or enhancement
3. **Task** - General work item
4. **Improvement** - Enhancement to existing functionality
</initial_gate>

<workflow>
1. **Determine issue type** - Bug, feature, task, or improvement
2. **Identify team/project** - Use `list_teams` (Linear) or `list_projects` (Jira)
3. **Gather core information** - Title, description, affected areas
4. **Investigate with Socratic questions** - Ask until no ambiguities remain
5. **Define acceptance criteria** - Verifiable outcomes
6. **Identify relationships** - What blocks this? What does this block?
7. **Set priority and metadata** - Priority, labels/issue type, project
8. **Present for approval** - Show complete issue before creating
9. **Create with MCP tool** - Execute the appropriate create_issue tool
</workflow>
</quick_start>

<socratic_investigation>
<purpose>
Uncover hidden requirements, edge cases, and ambiguities through targeted questioning. Each question should reveal information that prevents incorrect implementation or scope creep.
</purpose>

<question_categories>
<bug_questions>
- "What is the expected behavior vs actual behavior?"
- "Can you reproduce this consistently? What are the exact steps?"
- "Does this affect all users or specific scenarios?"
- "What error messages or logs are shown?"
- "When did this start happening? Any recent changes?"
- "What is the impact - blocking users, data loss, degraded experience?"
</bug_questions>

<feature_questions>
- "Who is the primary user of this feature?"
- "What problem does this solve? What's the current workaround?"
- "What is the minimum viable version of this feature?"
- "Are there related features this should integrate with?"
- "What should happen at the edges - empty input, maximum values, errors?"
- "How will we know this feature is successful?"
</feature_questions>

<task_questions>
- "What is the definition of done for this task?"
- "What existing code or systems does this touch?"
- "Are there dependencies that must complete first?"
- "Who needs to be informed when this is complete?"
- "What could block progress on this?"
</task_questions>

<universal_questions>
- "What priority does this have? 1 (Urgent) to 4 (Low)?"
- "Is there a deadline or due date?"
- "Who should own this work?"
- "Are there labels that should be applied?"
- "Does this relate to any existing issues?"
- "Should this be part of a project?"
- "How will we verify each criterion is met?" (test command, manual step, or observable outcome)
</universal_questions>
</question_categories>

<questioning_protocol>
1. Start with 2-3 high-value questions using AskUserQuestion
2. Based on answers, identify remaining ambiguities
3. Ask follow-up questions until answers create no new questions
4. Confirm understanding by summarizing back
5. Only proceed to issue creation when requirements are clear

Use AskUserQuestion with descriptive options where applicable. For open-ended information gathering, direct questions in chat are acceptable.
</questioning_protocol>

<latent_error_prevention>
Watch for these common sources of unclear issues:

- **Assumed context**: "The usual flow" - which flow exactly?
- **Implicit scope**: "Handle errors" - which errors? How?
- **Missing acceptance criteria**: "Should work better" - how do we verify?
- **Hidden dependencies**: "After the API is ready" - which issue?
- **Vague priority**: "Soon" - Urgent or Low?
</latent_error_prevention>
</socratic_investigation>

<issue_structure>
<description_template>
A well-structured description includes:

```markdown
## Summary
[1-2 sentence overview of the issue]

## Current Behavior (bugs only)
[What happens now that shouldn't]

## Expected Behavior
[What should happen instead]

## Reproduction Steps (bugs only)
1. Step one
2. Step two
3. Observe issue

## Acceptance Criteria
- [ ] Criterion 1 with verifiable outcome
  - **Verification**: `test command` | manual step | observable
- [ ] Criterion 2 with test method
  - **Verification**: `test command` | manual step | observable
- [ ] Criterion 3 with manual verification step
  - **Verification**: `test command` | manual step | observable

## Additional Context
[Screenshots, logs, related issues]
```
</description_template>

<acceptance_criteria_rules>
Write criteria as **behavioral outcomes**, not implementation details:

**GOOD (outcomes)**:
- "User can deactivate schedule without error"
- "All team members see updated schedule within 30 seconds"
- "Error message displays with actionable guidance"

**BAD (implementation)**:
- "Add try/catch around database call"
- "Use WebSocket for real-time sync"
- "Call scheduleService.deactivate()"

Each criterion should be:
1. **Observable** - Can be seen or measured
2. **Verifiable** - Has a test or check method
3. **Unambiguous** - Only one interpretation
</acceptance_criteria_rules>
</issue_structure>

<checkpoint_issues>
<purpose>
Checkpoint issues represent decision points where human input is required before work can proceed. They're used when the implementation approach is genuinely ambiguous and an agent cannot make the decision autonomously.
</purpose>

<when_to_create_checkpoints>
Create a checkpoint issue when:
- **Technology choice** - Multiple valid libraries/frameworks could solve the problem
- **Architecture decision** - The approach has long-term implications
- **Business logic ambiguity** - The "right" behavior depends on product decisions
- **Trade-off evaluation** - Options have meaningfully different pros/cons

Do NOT create checkpoints for:
- Implementation details an agent can reasonably decide
- Standard patterns with clear best practices
- Decisions that can be easily changed later
- Personal style preferences
</when_to_create_checkpoints>

<checkpoint_template>
```markdown
## Summary
[Brief description of the decision that needs to be made]

## Type: checkpoint:decision

## Decision Required
[Specific question that needs answering - one decision per checkpoint]

## Options
1. **Option A** - [Name]
   - Pros: [Benefits of this approach]
   - Cons: [Drawbacks or trade-offs]
   - Example: [Code snippet or reference if helpful]

2. **Option B** - [Name]
   - Pros: [Benefits of this approach]
   - Cons: [Drawbacks or trade-offs]
   - Example: [Code snippet or reference if helpful]

3. **Option C** - [Name] (optional)
   - Pros: [Benefits of this approach]
   - Cons: [Drawbacks or trade-offs]
   - Example: [Code snippet or reference if helpful]

## Recommendation
[If the agent has a recommendation, state it with reasoning. Otherwise: "No strong recommendation - depends on team preference."]

## Default Behavior
If no decision is made within [timeframe, e.g., "24 hours" or "before next sprint"], proceed with: **[Option X]**
Reason: [Why this is a safe default]

## Blocks
This decision blocks: [List of dependent sub-tasks or issues]
```
</checkpoint_template>

<checkpoint_example>
**Scenario**: Implementing dark mode feature requires deciding how to persist theme preference.

```markdown
## Summary
Choose the approach for persisting user theme preference.

## Type: checkpoint:decision

## Decision Required
How should we persist the user's theme preference across sessions?

## Options
1. **localStorage only**
   - Pros: Simple implementation, no server changes, immediate read
   - Cons: Not available during SSR, can flash wrong theme on load
   - Example: `localStorage.setItem('theme', 'dark')`

2. **Cookie only**
   - Pros: Available during SSR, no theme flash
   - Cons: Sent with every request, 4KB limit, requires cookie parsing
   - Example: `document.cookie = 'theme=dark; max-age=31536000'`

3. **Cookie + localStorage hybrid**
   - Pros: SSR-friendly AND fast client reads, best UX
   - Cons: More complex, must keep in sync
   - Example: Cookie for SSR, localStorage for client preference changes

## Recommendation
**Option 3 (hybrid)** if SSR is used, otherwise **Option 1 (localStorage)**.
Our app uses Next.js with SSR, so the hybrid approach prevents theme flash.

## Default Behavior
If no decision is made within 24 hours, proceed with: **Option 1 (localStorage)**
Reason: Simplest implementation; theme flash is acceptable for initial release.

## Blocks
This decision blocks: MOB-125 (Create ThemeProvider), MOB-126 (Add useTheme hook)
```
</checkpoint_example>

<timeout_handling>
Every checkpoint must have a default behavior to prevent indefinite blocking:

1. **Specify a timeout** - Usually 24-48 hours or "before next sprint"
2. **Choose a safe default** - The option that is easiest to change later
3. **Explain the reasoning** - Why this default won't cause problems

If the checkpoint is critical and has no safe default, escalate to the issue creator.
</timeout_handling>

<checkpoint_resolution>
When a decision is made:
1. Add a comment with the decision and reasoning
2. Update the issue description with "**Decision**: Option X selected"
3. Move the checkpoint to Done
4. Unblock dependent issues

The agent executing dependent tasks should read the checkpoint's decision before implementing.
</checkpoint_resolution>
</checkpoint_issues>

<context_gathering>
<linear_context>
Before creating an issue with Linear backend:

```
# List existing issues that might be related
mcp__plugin_linear_linear__list_issues with query parameter

# Get issue details including relationships
mcp__plugin_linear_linear__get_issue with includeRelations: true

# List available teams
mcp__plugin_linear_linear__list_teams

# List available labels
mcp__plugin_linear_linear__list_issue_labels
```
</linear_context>

<jira_context>
Before creating an issue with Jira backend:

```
# Search for related issues
mcp_plugin_atlassian_jira__list_issues with JQL query

# Get issue details
mcp_plugin_atlassian_jira__get_issue

# List available projects
mcp_plugin_atlassian_jira__list_projects
```
</jira_context>

<relationship_discovery>
Ask about relationships using context from the backend:

- "I found these related open issues: [list]. Does this new issue depend on any of them?"
- "Should any existing issues be blocked by this work?"
- "Is this related to an existing issue?"

**Linear relationships** (at creation time):
- `blocks`: Issues this one blocks
- `blockedBy`: Issues blocking this one
- `relatedTo`: Related issues
- `duplicateOf`: If this duplicates another issue

**Jira links** (at creation or via separate call):
- blocks / is blocked by
- relates to
- duplicates / is duplicated by
</relationship_discovery>
</context_gathering>

<priority_guidelines>
<priority_matrix>
| Priority | Linear | Jira | When to use |
|----------|--------|------|-------------|
| Urgent | 1 | Highest | Production down, data loss, security |
| High | 2 | High | Major feature broken, many users affected |
| Normal | 3 | Medium | Important but not urgent, default |
| Low | 4 | Low | Nice to have, improvements |
| None | 0 | Lowest | Not yet triaged |
</priority_matrix>

<priority_questions>
Use AskUserQuestion for priority:

Question: "What priority should this have?"

Options:
1. **Urgent** - Production impact, must fix immediately
2. **High** - Major functionality affected, fix soon
3. **Normal** - Important but not urgent (recommended default)
4. **Low** - Enhancement, can wait
</priority_questions>
</priority_guidelines>

<approval_workflow>
<before_creating>
Present the complete issue in chat:

"Here is the issue I'll create:

**Title**: [title]
**Team/Project**: [team or project name]
**Type/Labels**: [Bug/Feature/Improvement or issue type]
**Priority**: [Urgent/High/Normal/Low]
**State/Status**: [initial state]
**Description**:
[full description with acceptance criteria]

**Relationships**: [if any]
**Parent**: [if applicable]

Ready to create this issue?"

Use AskUserQuestion:
- **Create issue** - Issue looks correct, create it
- **Make changes** - I need to modify something
- **Add more context** - I have additional information
- **Cancel** - Don't create this issue
</before_creating>

<create_command>
After approval, use the appropriate MCP tool based on backend:

**Linear**:
```
mcp__plugin_linear_linear__create_issue
  team: "Team Name"
  title: "Issue title"
  description: "Full markdown description"
  labels: ["Bug"] or ["Feature"] or ["Improvement"]
  priority: 1-4
  state: "Backlog" or "Todo"
  blocks: ["ISSUE-123"]  # optional
  blockedBy: ["ISSUE-456"]  # optional
  relatedTo: ["ISSUE-789"]  # optional
```

**Jira**:
```
mcp_plugin_atlassian_jira__create_issue
  project: "PROJECT_KEY"
  summary: "Issue title"
  description: "Full markdown description"
  issuetype: "Bug" or "Story" or "Task"
  priority: "High" or "Medium" or "Low"
```
</create_command>

<after_creation>
Confirm: "Created issue [ID]: [title]

Would you like to:
- Create related issues
- Set up additional relationships
- Add this to a project/epic"
</after_creation>
</approval_workflow>

<examples>
<bug_example>
User: "There's a bug with schedules"

Response flow:
1. "What is happening vs what should happen?"
2. "Can you reproduce this? What are the steps?"
3. "Does this affect all users or specific scenarios?"
4. "What error message do you see?"

**Linear** resulting issue:
```
mcp__plugin_linear_linear__create_issue
  team: "Engineering"
  title: "Schedule deactivation throws 500 error"
  description: "## Summary
Users receive HTTP 500 error when deactivating schedules.

## Current Behavior
Clicking 'Deactivate' shows error toast and schedule remains active.

## Expected Behavior
Schedule deactivates successfully with confirmation message.

## Reproduction Steps
1. Navigate to Schedule Settings
2. Click 'Deactivate Schedule'
3. Observe 500 error in toast

## Acceptance Criteria
- [ ] User can deactivate schedule without error
  - **Verification**: Manual test - click Deactivate, observe success toast
- [ ] Schedule status updates to 'inactive'
  - **Verification**: `npm test -- --grep 'schedule deactivation'`
- [ ] Team members see schedule status change
  - **Verification**: Manual test - check team view after deactivation
- [ ] Error logs capture root cause for monitoring
  - **Verification**: Observable - check logs after fix deployment"
  labels: ["Bug"]
  priority: 1
  state: "Todo"
```

**Jira** resulting issue:
```
mcp_plugin_atlassian_jira__create_issue
  project: "PROJ"
  summary: "Schedule deactivation throws 500 error"
  description: "...same description..."
  issuetype: "Bug"
  priority: "Highest"
```
</bug_example>

<feature_example>
User: "We need to add dark mode"

Response flow:
1. "Who is the primary user of this feature?"
2. "Should it follow system preferences or be manually toggled?"
3. "Which screens/components need dark mode support?"
4. "How will we know this feature is successful?"

Resulting issue (backend-agnostic description):
```
Title: "Add dark mode theme support"
Description: "## Summary
Add dark mode support with system preference detection and manual toggle.

## Expected Behavior
- App detects system dark mode preference on launch
- User can manually toggle between light/dark/system
- All screens render correctly in both modes

## Acceptance Criteria
- [ ] Theme follows system preference by default
  - **Verification**: `npm test -- --grep 'theme system preference'`
- [ ] Settings screen has theme toggle (Light/Dark/System)
  - **Verification**: Manual test - navigate to Settings, verify toggle exists
- [ ] All text maintains 4.5:1 contrast ratio in both modes
  - **Verification**: `npm run test:a11y` or Lighthouse accessibility audit
- [ ] Theme preference persists across app restarts
  - **Verification**: Manual test - set theme, restart app, verify theme persists
- [ ] No flash of wrong theme on app launch
  - **Verification**: Observable - launch app in dark mode, no white flash"
```
</feature_example>
</examples>

<anti_patterns>
**Don't accept vague requirements**:
- BAD: "Fix the scheduling bug"
- GOOD: "Fix 500 error on schedule deactivation affecting all users"

**Don't skip acceptance criteria**:
- BAD: Create issue with just title and description
- GOOD: Every issue has verifiable acceptance criteria

**Don't assume priority**:
- BAD: Default everything to Normal
- GOOD: Ask about impact and urgency to determine priority

**Don't ignore relationships**:
- BAD: Create isolated issues
- GOOD: Search for related issues and set up relationship links

**Don't create compound issues**:
- BAD: "Fix deactivation and add team sync and improve UI"
- GOOD: Create separate issues for each concern

**Don't write untestable acceptance criteria**:
- BAD: "System should be faster" (unmeasurable)
- BAD: "UI should look better" (subjective)
- GOOD: "Page load time < 2 seconds" with `Verification: Lighthouse performance score > 90`
- GOOD: "Button uses primary color from design system" with `Verification: Visual regression test`
</anti_patterns>

<success_criteria>
An issue is ready when:

- [ ] Type/labels match the nature of the work (Bug/Feature/Task)
- [ ] Title is specific and actionable
- [ ] Description includes all relevant context
- [ ] Acceptance criteria are behavioral outcomes
- [ ] Each criterion is verifiable
- [ ] Priority reflects actual urgency/impact
- [ ] Relationships are identified and linked
- [ ] Project is set (if applicable)
- [ ] User has approved before creation
</success_criteria>
