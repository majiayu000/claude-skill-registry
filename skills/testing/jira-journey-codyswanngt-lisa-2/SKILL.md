---
name: jira-journey
description: "Read a JIRA ticket's Validation Journey section, execute the steps using Playwright MCP browser tools across all defined viewports, capture screenshots at each marker, generate evidence templates, and post to JIRA + GitHub PR using the jira-evidence skill."
---

# JIRA Validation Journey

Read a JIRA ticket's Validation Journey, execute it via Playwright MCP browser tools, capture screenshots at every `[SCREENSHOT: name]` marker across all viewports, and post evidence to both JIRA and GitHub PR.

## Arguments

`$ARGUMENTS`: `<TICKET_ID> [PR_NUMBER]`

- `TICKET_ID` (required): JIRA ticket key (e.g., `PROJ-123`)
- `PR_NUMBER` (optional): GitHub PR number to update description

## Prerequisites

- `JIRA_API_TOKEN` environment variable set
- `jira-cli` configured (`~/.config/.jira/.config.yml`)
- `gh` CLI authenticated
- Playwright MCP server running (browser tools available)
- Dev server running

## Workflow

### Step 1: Parse the Validation Journey

Run the parser script to extract the Validation Journey from the JIRA ticket description:

```bash
python3 .claude/skills/jira-journey/scripts/parse-plan.py <TICKET_ID>
```

The script outputs JSON to stdout:

```json
{
  "ticket": "PROJ-123",
  "prerequisites": [
    "Backend dev server running",
    "Admin user with test credentials"
  ],
  "steps": [
    {"number": 1, "text": "Navigate to Players page", "screenshot": null},
    {"number": 5, "text": "Open transfer modal", "screenshot": "confirm-step-disabled"}
  ],
  "viewports": [
    {"name": "Desktop", "width": 1512, "height": 768},
    {"name": "Mobile", "width": 375, "height": 812}
  ],
  "assertions": [
    "Modal fills entire screen on mobile (no horizontal overflow)"
  ]
}
```

Read the JSON output and use it to drive the Playwright session.

### Step 2: Satisfy Prerequisites

Before starting the journey, verify each prerequisite:

1. Check if the dev server is running (try `browser_navigate` to the app URL)
2. Authenticate if needed (use test credentials from `.env.localhost` or `.env.local`)
3. Navigate to the starting point described in step 1

### Step 3: Execute Steps at Each Viewport

For **each viewport** defined in the journey:

1. Use `browser_resize` to set the viewport dimensions
2. Execute each step sequentially using Playwright MCP tools
3. At each step with a `screenshot` marker, use `browser_take_screenshot` to capture the screenshot

#### Screenshot Naming Convention

Screenshots are named: `{NN}-{screenshot-name}-{viewport-name}.png`

- `NN`: zero-padded sequential number (01, 02, 03...)
- `screenshot-name`: the value from `[SCREENSHOT: name]` in the JIRA step
- `viewport-name`: lowercase viewport name from the Viewports table

Example: For a journey with 3 screenshot markers and 2 viewports:

```text
evidence/
  01-search-step-desktop.png
  02-confirm-step-desktop.png
  03-success-step-desktop.png
  04-search-step-mobile.png
  05-confirm-step-mobile.png
  06-success-step-mobile.png
  comment.txt
  comment.md
```

#### Viewport Execution Strategy

Execute the **full journey once per viewport**. Between viewports:

1. Resize the browser using `browser_resize`
2. Navigate back to the starting point
3. Re-execute all steps from the beginning

This ensures each screenshot is captured at the correct viewport dimensions with the correct application state.

### Step 4: Generate Evidence Templates

After capturing all screenshots, run the template generator:

```bash
python3 .claude/skills/jira-journey/scripts/generate-templates.py \
  <TICKET_ID> \
  <PR_NUMBER> \
  <BRANCH_NAME> \
  ./evidence
```

This generates `evidence/comment.txt` (JIRA wiki markup) and `evidence/comment.md` (GitHub markdown) with:

- PR and branch metadata
- All screenshots organized by viewport
- The verification journey steps
- Assertions as verification results

### Step 5: Post Evidence

Use the jira-evidence skill to post everything:

```bash
bash .claude/skills/jira-evidence/scripts/post-evidence.sh <TICKET_ID> ./evidence <PR_NUMBER>
```

### Step 6: Verify

Confirm images render inline at both the JIRA ticket and GitHub PR.

## Validation Journey Format in JIRA

The JIRA ticket description must contain a section with this structure:

### ADF Structure

```text
h2. Validation Journey

h3. Prerequisites
- App running locally or on dev
- Authenticated as test user
- Required feature flags enabled

h3. Steps
1. Navigate to the relevant page
2. Perform the first action
3. Click on the element [SCREENSHOT: element-state]
4. Complete the flow
5. Verify the final state [SCREENSHOT: final-state]

h3. Viewports
||Name||Width||Height||
|Desktop|1512|768|
|Mobile|375|812|

h3. Assertions
- Visual assertion about expected behavior
- Another assertion about responsive layout
```

### Key Rules

1. **`[SCREENSHOT: name]`** markers define where to capture. The `name` is used in the filename.
2. **Steps without markers** are executed but not captured.
3. **Viewports** define all resolutions to test. Each viewport runs the full journey.
4. **Assertions** describe what to verify visually in each screenshot.
5. **Prerequisites** describe what must be true before starting.

## Troubleshooting

### Modal closes on viewport resize

Some modals close when the viewport changes. The viewport execution strategy (full journey per viewport) handles this — each viewport starts fresh.

### Authentication required at each viewport

If the app requires re-authentication after resize/navigation, include the auth steps in the journey.

### Screenshot markers in conditional steps

If a step is conditional, capture the screenshot at the state described in the step text, not after the conditional action.
