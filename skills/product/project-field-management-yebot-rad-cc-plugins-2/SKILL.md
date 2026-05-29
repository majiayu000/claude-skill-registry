---
name: project-field-management
description: Comprehensive guide to GitHub Projects field types, configuration, and management strategies. Use when setting up fields, troubleshooting field issues, or optimizing field structures.
---

# GitHub Projects Field Management

This skill provides deep knowledge of GitHub Projects V2 custom fields, their types, capabilities, limitations, and best practices.

## Field Types Overview

### Single Select

**Purpose**: Dropdown with one choice from predefined options

**Use cases**:
- Status (Backlog, Todo, In Progress, Done)
- Priority (P0, P1, P2, P3)
- Component (Frontend, Backend, DevOps)
- Team (Team A, Team B, Team C)
- Environment (Dev, Staging, Prod)

**Characteristics**:
- Mutually exclusive choices
- Enables grouping in board views
- Filterable and searchable
- Color-coded options possible (via UI)
- Maximum ~50 options recommended

**CLI Creation**:
```bash
# IMPORTANT: Status field is built-in and already exists in new projects!
# Do NOT create a Status field - it's already there.

# For other SINGLE_SELECT fields, options are REQUIRED at creation:
gh project field-create <project-id> --owner "@me" \
  --data-type SINGLE_SELECT \
  --name "Priority" \
  --single-select-options "P0 (Critical),P1 (High),P2 (Medium),P3 (Low)"
```

**CRITICAL**:
- Options MUST be provided at creation time using `--single-select-options`
- Options cannot be added later via CLI
- Format: Comma-separated, no spaces after commas
- Status field is a built-in default field - never create it

**Best Practices**:
- Keep options list short (5-10 ideal)
- Use clear, unambiguous names
- Order logically (workflow progression)
- Avoid overlapping meanings
- Document what each option means

### Number

**Purpose**: Numeric values (integer or decimal)

**Use cases**:
- Story Points (1, 2, 3, 5, 8, 13)
- Estimated Hours (decimal)
- Customer Impact (count)
- Revenue Impact (dollars)
- Affected Users (count)
- Sprint Capacity (points)

**Characteristics**:
- Sortable and filterable
- Supports math operations (sum, average)
- No min/max validation (set via workflow norms)
- Can be decimal or integer

**CLI Creation**:
```bash
gh project field-create <project-id> --owner "@me" \
  --data-type NUMBER --name "Story Points"
```

**CLI Update**:
```bash
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --number 5
```

**Best Practices**:
- Document units (hours, points, count)
- Use consistent scale (Fibonacci for story points)
- Don't use for categorical data (use Single Select)
- Consider aggregation needs

### Date

**Purpose**: Calendar date (no time component)

**Use cases**:
- Due Date
- Start Date
- Launch Date
- Reported Date
- Target Completion
- Review By Date

**Characteristics**:
- Format: YYYY-MM-DD
- Enables timeline/roadmap views
- Sortable and filterable
- No time component (dates only)
- Past dates highlighted in red (in UI)

**CLI Creation**:
```bash
gh project field-create <project-id> --owner "@me" \
  --data-type DATE --name "Due Date"
```

**CLI Update**:
```bash
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --date "2025-12-31"
```

**Best Practices**:
- Use for deadlines and milestones
- Combine with Status for at-risk detection
- Set realistic dates (avoid always late pattern)
- Review and adjust dates as needed
- Use roadmap view for visualization

### Iteration

**Purpose**: Time-boxed planning cycles (sprints)

**Use cases**:
- 2-week sprints
- Monthly cycles
- Quarterly planning
- Release trains
- PI (Program Increment) planning

**Characteristics**:
- Fixed duration (1-4 weeks typical)
- Start and end dates
- Automatically creates future iterations
- Enables velocity tracking
- Burndown calculations
- Sortable chronologically

**CLI Creation**:
```bash
gh project field-create <project-id> --owner "@me" \
  --data-type ITERATION --name "Sprint"
```

**Configuration** (via UI):
- Set iteration duration (days)
- Set start date
- System generates future iterations

**CLI Update** (complex - requires iteration ID):
```bash
# First get iteration IDs via field-list
ITERATIONS=$(gh project field-list <project-id> --owner "@me" --format json | \
  jq '.[] | select(.name=="Sprint") | .configuration.iterations')

# Then update item with iteration ID
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --iteration-id <iteration-id>
```

**Best Practices**:
- Consistent duration (2 weeks standard)
- Start sprints on same weekday
- Name iterations clearly (Sprint 1, Sprint 2 or dates)
- Close/archive old iterations after 6 months
- Track velocity across iterations

### Text

**Purpose**: Free-form text input (single line)

**Use cases**:
- Owner name
- External ticket ID
- Slack thread link
- Sprint goal
- Related feature
- Customer name

**Characteristics**:
- Single line (not multiline)
- Searchable
- Not structured (no validation)
- Filterable (exact match or contains)
- Max length ~1000 characters

**CLI Creation**:
```bash
gh project field-create <project-id> --owner "@me" \
  --data-type TEXT --name "Owner"
```

**CLI Update**:
```bash
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --text "Alice Johnson"
```

**Best Practices**:
- Use for unstructured data only
- Consider Single Select if options are limited
- Document expected format (if any)
- Avoid using for categorical data
- Good for links and external references

## Built-in Fields

These fields exist automatically and cannot be customized:

### Title
- Item title
- Always visible
- Editable in place
- Searchable
- Required field

### Assignees
- GitHub user assignments
- Multiple assignees possible
- Inherited from issue/PR
- Can filter by assignee
- Enables workload distribution

### Labels
- Inherited from linked issue/PR
- Not directly editable in project
- Change on issue to reflect in project
- Filterable and searchable
- Color-coded

### Repository
- Where issue/PR resides
- Read-only in project
- Useful for multi-repo projects
- Filter by repo

### Milestone
- Inherited from issue/PR
- Not editable in project view
- Useful for release planning
- Can filter by milestone

### Linked Pull Requests
- PRs linked to issue
- Shows PR status
- Quick navigation
- Enables PR → Issue status sync

## Field Management Strategies

### Minimal Field Set

**Philosophy**: Only add fields you'll actively use

**Recommended minimum**:
- Status (required)
- Priority (required)
- One size/effort field (optional but recommended)

**When to use**:
- Small teams (<5 people)
- Simple projects
- Getting started with GitHub Projects
- Single-team projects

**Benefits**:
- Easy to maintain
- Low cognitive overhead
- Fast to use
- Less data entry

### Standard Field Set

**Philosophy**: Cover common planning needs

**Recommended fields**:
- Status
- Priority
- Story Points or Size
- Iteration or Sprint
- Component or Area
- Assignee (built-in)

**When to use**:
- Medium teams (5-20 people)
- Agile workflows
- Cross-functional teams
- Regular sprint planning

**Benefits**:
- Good balance of detail and simplicity
- Enables velocity tracking
- Supports sprint planning
- Reasonable overhead

### Comprehensive Field Set

**Philosophy**: Detailed tracking for complex projects

**Recommended fields**:
- Status
- Priority
- Story Points
- Sprint/Iteration
- Component
- Team
- Effort (hours)
- Customer Impact
- Due Date
- Owner
- External Ticket ID

**When to use**:
- Large organizations (>20 people)
- Multiple teams
- Regulatory requirements
- Executive reporting needs
- Complex dependencies

**Benefits**:
- Rich reporting capabilities
- Detailed tracking
- Multi-team coordination
- Audit trail

**Drawbacks**:
- High maintenance overhead
- More data entry required
- Can slow down workflow
- Risk of analysis paralysis

## Field Discovery & Querying

### Get All Fields for a Project

```bash
# List all fields with metadata
gh project field-list <project-number> --owner "@me" --format json

# Parse field names and types
gh project field-list <project-number> --owner "@me" --format json | \
  jq '.[] | {name: .name, type: .dataType, id: .id}'
```

### Get Field ID by Name

```bash
FIELDS=$(gh project field-list <project-number> --owner "@me" --format json)

# Get specific field ID
STATUS_FIELD_ID=$(echo $FIELDS | jq -r '.[] | select(.name=="Status") | .id')
```

### Get Single Select Options

```bash
# Get all options for a single-select field
gh project field-list <project-number> --owner "@me" --format json | \
  jq '.[] | select(.name=="Priority") | .options[] | {name: .name, id: .id}'

# Store for later use
PRIORITY_OPTIONS=$(gh project field-list <project-number> --owner "@me" --format json | \
  jq '.[] | select(.name=="Priority") | .options')
```

### Get Iteration IDs

```bash
# List all iterations with IDs
gh project field-list <project-number> --owner "@me" --format json | \
  jq '.[] | select(.dataType=="ITERATION") | .configuration.iterations[] | {title: .title, id: .id, startDate: .startDate, duration: .duration}'
```

## Field Value Management

### Setting Field Values

**Single Select**:
```bash
# Requires option ID, not option name
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --single-select-option-id <option-id>
```

**Number**:
```bash
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --number 8
```

**Date**:
```bash
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --date "2025-06-15"
```

**Text**:
```bash
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --text "Alice Johnson"
```

**Iteration**:
```bash
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --iteration-id <iteration-id>
```

### Clearing Field Values

```bash
# Use --clear flag to remove value
gh project item-edit --id <item-id> --project-id <project-id> \
  --field-id <field-id> --clear
```

### Batch Field Updates

```bash
# Update multiple items to same value
ITEMS=$(gh project item-list <project-number> --owner "@me" --format json)

# Filter items and update
echo $ITEMS | jq -r '.items[] | select(<filter-criteria>) | .id' | while read ITEM_ID; do
  gh project item-edit --id $ITEM_ID --project-id $PROJECT_ID \
    --field-id $FIELD_ID --single-select-option-id $OPTION_ID
  echo "Updated item $ITEM_ID"
done
```

## Common Field Configurations

**NOTE**: Status field is built-in and already exists. The configurations below show recommended options for customizing the existing Status field via the GitHub UI, and CLI commands for creating other fields.

### Agile Scrum

```yaml
Status:
  type: SINGLE_SELECT (Built-in - customize via UI)
  options: [Backlog, Todo, In Progress, In Review, Done]

Priority:
  type: SINGLE_SELECT
  options: [P0, P1, P2, P3]

Story Points:
  type: NUMBER
  values: [1, 2, 3, 5, 8, 13]

Sprint:
  type: ITERATION
  duration: 14 days
```

### Kanban Flow

```yaml
Status:
  type: SINGLE_SELECT
  options: [Ready, In Progress, Review, Done]

Priority:
  type: SINGLE_SELECT
  options: [Critical, High, Normal, Low]

Size:
  type: SINGLE_SELECT
  options: [XS, S, M, L, XL]

Type:
  type: SINGLE_SELECT
  options: [Bug, Feature, Chore, Tech Debt]
```

### Bug Tracking

```yaml
Status:
  type: SINGLE_SELECT
  options: [New, Triaged, In Progress, Fixed, Verified, Closed]

Severity:
  type: SINGLE_SELECT
  options: [Critical, High, Medium, Low]

Component:
  type: SINGLE_SELECT
  options: [Frontend, Backend, API, Database, Infrastructure]

Affected Users:
  type: NUMBER

Reported Date:
  type: DATE
```

### Product Roadmap

```yaml
Status:
  type: SINGLE_SELECT
  options: [Idea, Spec, Development, Beta, Launched]

Priority:
  type: SINGLE_SELECT
  options: [Must Have, Should Have, Nice to Have]

Quarter:
  type: SINGLE_SELECT
  options: [Q1 2025, Q2 2025, Q3 2025, Q4 2025]

Launch Date:
  type: DATE

Customer Impact:
  type: NUMBER

Owner:
  type: TEXT
```

## Troubleshooting Field Issues

### Cannot Create Status Field

**Problem**: Error when trying to create Status field

**Cause**: Status is a built-in default field that already exists in all new projects

**Solution**:
- Do NOT create a Status field
- The field already exists with default options
- Customize options via GitHub UI if needed (Project Settings → Fields → Status)

### Field Creation Fails for SINGLE_SELECT

**Problem**: `gh project field-create` succeeds but field has no options

**Cause**: Options were not provided at creation time

**Solution**:
- Always include `--single-select-options` parameter
- Format: `--single-select-options "Option1,Option2,Option3"`
- No spaces after commas
- Options cannot be added later via CLI

### Field Update Fails

**Problem**: `gh project item-edit` returns error

**Causes**:
1. Wrong field ID
2. Wrong option ID (for single-select)
3. Invalid data format (date, number)
4. Permission issue
5. Item doesn't exist in project

**Solutions**:
```bash
# Re-fetch field IDs
gh project field-list <project-number> --owner "@me" --format json

# Verify item exists in project
gh project item-list <project-number> --owner "@me" --format json | \
  jq '.items[] | select(.id=="<item-id>")'

# Check auth scopes
gh auth status
# If missing: gh auth refresh -s project
```

### Field Not Showing in Views

**Problem**: Created field doesn't appear

**Causes**:
1. View is filtered/hidden
2. Field hidden in view settings
3. Cache issue

**Solutions**:
- Refresh browser
- Check view settings → Fields → Unhide field
- Create new view to test

### Can't Add Options to Single Select

**Problem**: CLI created field has no options

**Cause**: Options were not provided at creation time (required parameter was missing)

**Solution**:
- SINGLE_SELECT fields require `--single-select-options` at creation time
- Options cannot be added later via CLI
- If field already exists without options, delete and recreate with options
- Or use GitHub UI to manually add options (Project Settings → Fields)

### Iteration Field Not Working

**Problem**: Can't set iteration or iterations don't appear

**Cause**: Iterations not configured

**Solution**:
1. Go to project settings
2. Click on Iteration field
3. Set start date and duration
4. Save (future iterations auto-generate)

### Repository Linking Fails

**Problem**: `gh project link` returns error or permission denied

**Cause**: Owner parameter doesn't match repository owner

**Solution**:
- The `--owner` parameter MUST match the repository owner exactly
- Cannot use "@me" for organization repositories
- Examples:
  ```bash
  # For personal repo
  gh project link 1 --owner "your-username" --repo your-username/repo-name

  # For org repo
  gh project link 1 --owner "org-name" --repo org-name/repo-name
  ```

## Field Best Practices Summary

1. **Start Minimal**: Add fields as needed, not preemptively
2. **Clear Names**: Use unambiguous field names (Status, not State)
3. **Consistent Options**: Standardize across projects
4. **Document Meanings**: Write down what P0 vs P1 means
5. **Avoid Duplication**: Don't create multiple fields for same purpose
6. **Use Right Type**: Single Select > Text for categorical data
7. **Regular Cleanup**: Remove unused fields
8. **Team Alignment**: Ensure team understands field purposes
9. **Automation-Friendly**: Choose fields that can be auto-populated
10. **Measure Usefulness**: Track which fields are actually used

Remember: Fields should clarify, not complicate. Every field is a cognitive burden and data entry task. Only keep fields that provide clear value to the team.
