---
name: create-monthly-ptsf-event
description: Use when creating a new monthly ProductTank SF event in Linear - creates event project from PRO-60 template with calculated timeline dates and task breakdown
---

# Creating Monthly ProductTank SF Events

## When to Use

Use this skill when the user asks to:
- Create a new monthly ProductTank SF event
- Set up event planning for a specific month/date
- Generate a new event from the template

**Announce at start**: "I'm using the create-monthly-ptsf-event skill to create the [Month YYYY] event."

## Prerequisites

Before starting, gather:
1. **Event date** (YYYY-MM-DD format) - typically 3rd Tuesday of the month
2. **Month abbreviation** - for title and labels (e.g., "Feb", "Mar")
3. **Year** - for project assignment (e.g., "2026")

**Constants** (do not ask user):
- Team: "Product Tank SF"
- Template source: PRO-60

## The Process

### Step 1: Calculate Timeline Dates

Use `scripts/calculate-event-date.sh` to calculate all T-minus and T-plus milestone dates.

**Required milestone offsets**:
- Pre-event: -90, -60, -45, -30, -20, -14, -7, -2
- Event day: 0 (event date itself)
- Post-event: +1, +2, +3, +10, +15

**Usage pattern**:

```bash
./scripts/calculate-event-date.sh "<YYYY-MM-DD>" "<offset>"
```

**Example** (for event on 2026-02-17):

```bash
./scripts/calculate-event-date.sh "2026-02-17" "-60"  # Returns: 2025-12-19
```

Run for all offsets to validate timeline dates before creating the project.

### Step 2: Create Event Project

Use `linear-cli p create` with these parameters:

**Fixed values**:
- `team`: "Product Tank SF"

**Dynamic values** (from user input):
- `name`: "{Month} {YYYY} - [Speaker Name]" (e.g., "Feb 2026 - [Speaker Name]")
- `targetDate`: Event date in YYYY-MM-DD format
- `labels`: ["Event", "{Month}"] (e.g., ["Event", "Feb"])

**Description construction**:
1. Read PRO-60 template: `linear-cli i get PRO-60 --output json`
2. Replace placeholders in description:
   - `[YYYY Month]` → "{Month} {YYYY}" (e.g., "Feb 2026")
   - `[Date]` → Full date string (e.g., "February 17, 2026")
   - Keep: `[Speaker Name]`, `[lead-name]`, `[co-lead-name]`, `[shadow-lead-name]`
3. **Replace all checklist issue links with `[TBD]` placeholders**:
   - Template contains links like `[PRO-61](https://linear.app/...)`
   - Replace with: `[Template]({{link-to-template}})`
   - **Why**: Prevents Linear from auto-creating relationships to template sub-issues
   - **Example**: `- [ ] Secure Speaker [PRO-61](https://...)` → `- [ ] Secure Speaker [Template](https://linear.app/product-tank-sf/issue/PRO-61/event-name-ie-jan-2026-11-secure-speaker)`
4. Preserve all template sections (Overview, Quick Links, Checklist, Metrics)

**Summary field**:
- Extract first paragraph of PRO-60 description or create concise summary (max 255 chars)
- Example: "Monthly ProductTank SF event for {Month} {YYYY}"

### Step 3: Validate Project Creation

**Verification checklist**:
- [ ] Read created project with `linear-cli p get <PROJECT_ID> --output json`
- [ ] Confirm name format: "{Month} {YYYY} - [Speaker Name]"
- [ ] Confirm team: "Product Tank SF"
- [ ] Confirm labels: "Event" and month abbreviation
- [ ] Confirm target date matches event date
- [ ] Confirm description has all template sections
- [ ] Confirm summary is present

Report project URL and ID to user.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Script not executable | `chmod +x scripts/calculate-event-date.sh` |
| Incorrect date calculations | Verify date format (YYYY-MM-DD) and offset sign (+/-) |
| Month label not found | Create label in Linear workspace before running |
| Project label not found | Create "Event" label in Linear workspace before running |

## Creating Project Tasks from Templates

After creating the event project, create 25 tasks from the template checklist in the project's Definition of Done.

### Using Sub-Agents for Parallel Creation

**CRITICAL: Use sub-agents to create tasks in parallel batches of 5.**

Each sub-agent creates ONE task following this process:

**Sub-Agent Instructions** (for each template):

1. **Read Template**: `linear-cli i get <TEMPLATE_ID> --output json`
   - Note title format: `[Event Name, ie. Jan 2026]` placeholder
   - Note description: `[Event Date - X days]` placeholder
   - Note **Target Completion** field (e.g., `[Event Date - 60 days]`)
   - Note category label (Speaker, Marketing, Venue, etc.)

2. **Calculate Due Date**:
   - Extract offset from Target Completion (e.g., `-60` from `[Event Date - 60 days]`)
   - Run: `./scripts/calculate-event-date.sh "<event-date>" "<offset>"`
   - For TBD items (no Target Completion): use `null`

3. **Create Task**: `linear-cli i create "<TITLE>" -t "Product Tank SF" --project "<PROJECT_NAME>" -l "<LABELS>"`
   - `title`: Replace `[Event Name, ie. Jan 2026]` with `{Month} {YYYY}`
   - `team`: "Product Tank SF"
   - `project`: "{Month} {YYYY} - [Speaker Name]" (the project created in Step 2)
   - `labels`: [Template's category label, Event's month label]
   - `dueDate`: Calculated date (or `null`)
   - `description`: Copy from template, replace `[Event Date - X days]` with calculated date
   - `priority`: 0

4. **Report**: Return template ID, new issue identifier, and URL

### Execution Pattern

**Launch 5 sub-agents in parallel** (single message with 5 Task tool calls):

```text
Batch 1: Templates PRO-61, PRO-83, PRO-62, PRO-63, PRO-64
Batch 2: Templates PRO-65, PRO-66, PRO-67, PRO-68, PRO-69
Batch 3: Templates PRO-70, PRO-71, PRO-72, PRO-73, PRO-88
Batch 4: Templates PRO-74, PRO-75, PRO-76, PRO-77, PRO-78
Batch 5: Templates PRO-79, PRO-80, PRO-81, PRO-82, PRO-84
```

**Context to provide each sub-agent:**
- Template ID to process (e.g., "PRO-61")
- Project name/ID - the event project created in Step 2
- Event date (for calculation)
- Event month/year labels

### After Each Batch Completes

**CRITICAL**: The orchestrating agent (not sub-agents) updates the project DoD to avoid conflicts.

1. **Collect Results**: Gather template ID → new issue mapping from all 5 sub-agents
   - Example: `{"PRO-83": "PRO-109", "PRO-62": "PRO-107", ...}`

2. **Read Current Project**: `linear-cli p get <PROJECT_ID> --output json`

3. **Update All Links**: For each template → new issue mapping:
   - Find template link in description (e.g., `[Template](https://linear.app/.../PRO-83/...)`)
   - Replace with new task link (e.g., `[PRO-109](https://linear.app/.../PRO-109/...)`)

4. **Single Update**: `linear-cli p update <PROJECT_ID> -d "<UPDATED_DESCRIPTION>"`

**Why**: Prevents concurrent update conflicts when multiple sub-agents try to update the same project simultaneously.

## Next Steps

After all tasks created and links updated:
1. Update project with speaker details and team assignments
2. Begin T-90 milestone execution

## References

- **Template Source**: [PRO-60 - Template Event](https://linear.app/product-tank-sf/issue/PRO-60/yyyy-month-speaker-name)
- **Team**: Product Tank SF
