---
name: jira-add-journey
description: "Add a Validation Journey section to an existing JIRA ticket by reading the ticket description, understanding the feature, and generating the journey steps, viewports, and assertions."
---

# Add Validation Journey to Existing JIRA Ticket

Read an existing JIRA ticket, understand the feature or fix it describes, analyze the codebase to determine the user flow, and append a Validation Journey section to the ticket description.

## Arguments

`$ARGUMENTS`: `<TICKET_ID>`

- `TICKET_ID` (required): JIRA ticket key (e.g., `PROJ-123`)

## Prerequisites

- `JIRA_API_TOKEN` environment variable set
- `jira-cli` configured (`~/.config/.jira/.config.yml`)

## Workflow

### Step 1: Read the Ticket

Use the Atlassian MCP or jira-cli to read the full ticket details:

```bash
jira issue view <TICKET_ID>
```

Extract:
- Title and description (what the feature/fix is)
- Acceptance criteria (what needs to be verified)
- Components or labels (frontend, mobile, responsive, etc.)
- Any linked tickets or parent epic context

### Step 2: Check for Existing Journey

Run the parser to see if a Validation Journey already exists:

```bash
python3 .claude/skills/jira-journey/scripts/parse-plan.py <TICKET_ID> 2>&1
```

If the parser succeeds and returns steps, the ticket already has a journey. Report this to the user and stop.

### Step 3: Analyze the Feature

Based on the ticket description and acceptance criteria:

1. **Identify the UI surface** — Which pages, modals, or components are affected?
2. **Identify the user flow** — What steps does a user take to exercise the feature?
3. **Identify visual checkpoints** — At which states should screenshots be captured?
4. **Identify viewports** — Does this feature have responsive behavior? Always include Desktop. Add Mobile for responsive changes.
5. **Identify assertions** — What must be visually true for the feature to be correct?

Use the Explore agent or read the codebase directly to understand:
- Which components are involved (search by ticket ID, feature name, or file paths mentioned in the ticket)
- What testIDs exist (for Playwright interaction)
- What the user flow looks like (Container/View structure, navigation, modals)

### Step 4: Draft the Validation Journey

Compose the journey following the format:

```text
h2. Validation Journey

h3. Prerequisites
- List what must be true before starting (backend, auth, feature flags)

h3. Steps
1. First action the user takes
2. Second action [SCREENSHOT: descriptive-name]
3. Continue the flow
4. Final verification [SCREENSHOT: final-state]

h3. Viewports
||Name||Width||Height||
|Desktop|1512|768|
|Mobile|375|812|

h3. Assertions
- Testable visual statement about the expected behavior
- Another assertion about responsive layout
```

### Guidelines for Drafting

1. **3-7 screenshot markers** — Enough to prove the feature, not so many that execution is slow
2. **Concrete steps** — "Click the 'Add action' button" not "Interact with the controls"
3. **Include auth if needed** — If the journey requires login, include credentials in Prerequisites
4. **Name feature flags explicitly** — If the feature is behind a PostHog flag, name it
5. **Assertions must be testable** — "Buttons stacked vertically on mobile" not "Layout looks good"
6. **Screenshot names in kebab-case** — `confirm-step-disabled`, `modal-open`, `form-error`

### Step 5: Present to User for Approval

Display the drafted Validation Journey to the user and ask for confirmation before appending it to the ticket. The user may want to:
- Add or remove steps
- Change screenshot markers
- Adjust viewports or assertions
- Modify prerequisites

### Step 6: Append to Ticket Description

After user approval, use the JIRA REST API to append the Validation Journey to the existing ticket description.

Use the Atlassian MCP `updateJiraIssue` to update the description field. The journey section must be appended **after** the existing description content, not replace it.

### Step 7: Verify

Run the parser again to confirm the journey was added correctly:

```bash
python3 .claude/skills/jira-journey/scripts/parse-plan.py <TICKET_ID>
```

The parser should now return the steps, viewports, and assertions from the newly added section.

## When to Use This Skill

- Ticket was created before the Validation Journey convention was established
- Ticket was created manually without following `jira-create` guidelines
- Ticket needs a journey added or updated based on implementation progress
- During sprint planning, to ensure all frontend tickets have journeys before work starts
