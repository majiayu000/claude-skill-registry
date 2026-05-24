---
name: Managing GitHub Projects
description: Manages GitHub Projects V2 items and custom fields using GitHub CLI commands. Use when adding issues/PRs to projects, updating Status (Backlog/Todo/Doing/Done), Value (Essential/Useful/Nice-to-have), or Effort (Light/Moderate/Heavy) fields, querying project data, or performing bulk operations.
---

# GitHub Projects Management

Manage GitHub Projects V2 items and custom fields using the GitHub CLI.

## What you should do

When invoked, help the user manage project items by:

1. **Understanding the request** - Determine what operation is needed:
   - Update item field values (Status, Value, Effort, or other custom fields)
   - Add issues/PRs to projects
   - Query project items and their field values
   - List available fields and options
   - Bulk operations on multiple items

2. **Gather required information** - You may need:
   - Project number or ID
   - Repository owner (org or user)
   - Issue/PR number (for adding to project)
   - Item ID (for updating existing items)
   - Field name and new value

3. **Execute the appropriate operation** based on the request type.

## Core operations

### 1. Add item to project

```bash
# Add issue to project
gh project item-add <project-number> --owner <org> --url <issue-url>

# Example
gh project item-add 1 --owner kynoptic --url https://github.com/kynoptic/ultimate-ranks-data/issues/310
```

### 2. List project fields

```bash
# Get all fields
gh project field-list <project-number> --owner <org> --format json

# Get specific field ID
gh project field-list <project-number> --owner <org> --format json \
  --jq '.fields[] | select(.name == "Status") | .id'

# Get field options (for single-select fields)
gh project field-list <project-number> --owner <org> --format json \
  --jq '.fields[] | select(.name == "Status") | .options[] | {name, id}'
```

### 3. List project items

```bash
# Get all items with details
gh project item-list <project-number> --owner <org> --format json --limit 100

# Get specific item by issue number
gh project item-list <project-number> --owner <org> --format json \
  --jq '.items[] | select(.content.number == 307) | {id, number: .content.number, title: .content.title}'
```

### 4. Update item fields

**Single-select fields (Status, Value, Effort):**
```bash
gh project item-edit \
  --id <item-id> \
  --project-id <project-id> \
  --field-id <field-id> \
  --single-select-option-id <option-id>
```

**Text fields:**
```bash
gh project item-edit \
  --id <item-id> \
  --project-id <project-id> \
  --field-id <field-id> \
  --text "new text value"
```

**Date fields:**
```bash
gh project item-edit \
  --id <item-id> \
  --project-id <project-id> \
  --field-id <field-id> \
  --date "2025-10-18"
```

**Number fields:**
```bash
gh project item-edit \
  --id <item-id> \
  --project-id <project-id> \
  --field-id <field-id> \
  --number 42
```

**Clear a field:**
```bash
gh project item-edit \
  --id <item-id> \
  --project-id <project-id> \
  --field-id <field-id> \
  --clear
```

## Project-specific configuration

To use this skill effectively, you'll need to identify the project-specific IDs for your repository. Use the commands below to discover these values:

```bash
# Get project number and ID
gh project list --owner <org-or-user> --format json | jq '.[] | {title, number, id}'

# Get custom field IDs
gh project field-list <project-number> --owner <org-or-user> --format json
```

**Example custom fields configuration:**

### Status field
- **Field ID**: `PVTSSF_lAHOAvtmyM4BCtNbzg01sVQ`
- **Type**: Single-select
- **Options**:
  - `Backlog` (ID: `6a4c50b0`) - Not yet prioritized or ready to start
  - `Todo` (ID: `f75ad846`) - Ready to start, requirements clear
  - `Doing` (ID: `47fc9ee4`) - Currently being worked on
  - `Done` (ID: `98236657`) - Completed and merged

**Workflow:**
- `Backlog` → Items not yet ready or prioritized
- `Todo` → Requirements defined, ready to pick up
- `Doing` → Active work in progress
- `Done` → Work completed and merged

**Note:** Use issue dependencies (blockedBy/blocking) to indicate when items cannot proceed.

### Value field
- **Field ID**: `PVTSSF_lAHOAvtmyM4BCtNbzg01ul0`
- **Type**: Single-select
- **Options**:
  - `Essential` (ID: `5885ea3a`) - Critical functionality, must have
  - `Useful` (ID: `50c89511`) - Valuable improvement, should have
  - `Nice-to-have` (ID: `1e7b8c9e`) - Optional enhancement, could have

**When to use:**
- `Essential`: Core features, security fixes, data integrity issues, blocking bugs
- `Useful`: Significant improvements, important refactors, common use cases
- `Nice-to-have`: Minor enhancements, edge cases, cosmetic improvements

*Note: These values align conceptually with the "Must fix/Should fix/Nice to have" framework commonly used in code reviews and development prioritization.*

### Effort field
- **Field ID**: `PVTSSF_lAHOAvtmyM4BCtNbzg02ZGg`
- **Type**: Single-select
- **Options**:
  - `Light` (ID: `449696b6`) - Quick task, minimal complexity
  - `Moderate` (ID: `6ec15605`) - Standard task, some complexity
  - `Heavy` (ID: `187484d1`) - Complex task, significant work

**When to use:**
- `Light`: Simple changes, typo fixes, small refactors, minor features
- `Moderate`: Standard features, multi-file changes, moderate complexity
- `Heavy`: Major features, architectural changes, large refactors, cross-cutting concerns

## Complete workflow example

**Goal**: Add issue #310 to project and set Status=Todo, Value=Useful, Effort=Moderate

```bash
# Step 1: Add to project
ITEM_ID=$(gh project item-add 1 --owner kynoptic \
  --url https://github.com/kynoptic/ultimate-ranks-data/issues/310 \
  --format json | jq -r '.id')

# Step 2: Set constant IDs (from configuration above)
PROJECT_ID="PVT_kwHOAvtmyM4BCtNb"
STATUS_FIELD_ID="PVTSSF_lAHOAvtmyM4BCtNbzg01sVQ"
VALUE_FIELD_ID="PVTSSF_lAHOAvtmyM4BCtNbzg01ul0"
EFFORT_FIELD_ID="PVTSSF_lAHOAvtmyM4BCtNbzg02ZGg"

# Option IDs (from configuration above)
TODO_ID="f75ad846"
USEFUL_ID="50c89511"
MODERATE_ID="6ec15605"

# Step 3: Update fields
gh project item-edit --id "$ITEM_ID" --project-id "$PROJECT_ID" \
  --field-id "$STATUS_FIELD_ID" --single-select-option-id "$TODO_ID"

gh project item-edit --id "$ITEM_ID" --project-id "$PROJECT_ID" \
  --field-id "$VALUE_FIELD_ID" --single-select-option-id "$USEFUL_ID"

gh project item-edit --id "$ITEM_ID" --project-id "$PROJECT_ID" \
  --field-id "$EFFORT_FIELD_ID" --single-select-option-id "$MODERATE_ID"
```

## Efficient patterns

### Pattern 1: Load configuration from project config file

**Recommended**: Use the project configuration file created by `gh-project-setup`:

```bash
# Load configuration from standard location (.github/project-config.json)
CONFIG_FILE=".github/project-config.json"

# Extract IDs from config using jq
PROJECT_ID=$(jq -r '.project.id' "$CONFIG_FILE")
STATUS_FIELD_ID=$(jq -r '.fields.status.id' "$CONFIG_FILE")
BACKLOG_ID=$(jq -r '.fields.status.options.Backlog.id' "$CONFIG_FILE")

# Use in project commands
gh project item-edit --id "$ITEM_ID" --project-id "$PROJECT_ID" \
  --field-id "$STATUS_FIELD_ID" --single-select-option-id "$BACKLOG_ID"
```

**Best practice**: Store project config in `.github/project-config.json` (not `docs/`):
- ✅ Standard location for GitHub-specific configuration
- ✅ Alongside workflows, issue templates, and other automation
- ✅ Separates infrastructure config from user documentation
- ✅ Created automatically by `gh-project-setup` skill

**Alternative**: Query and cache field IDs dynamically (if config file doesn't exist):

```bash
# Get all field configurations once
gh project field-list 1 --owner kynoptic --format json > /tmp/project-fields.json

# Extract IDs as needed
STATUS_BACKLOG=$(jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "Backlog") | .id' /tmp/project-fields.json)
```

### Pattern 2: Bulk updates

Update multiple items with the same field value:

```bash
# Get all items in "Todo" status
TODO_ITEMS=$(gh project item-list 1 --owner kynoptic --format json \
  --jq '.items[] | select(.status.name == "Todo") | .id')

# Move selected items to "Doing"
PROJECT_ID="PVT_kwHOAvtmyM4BCtNb"
STATUS_FIELD_ID="PVTSSF_lAHOAvtmyM4BCtNbzg01sVQ"
DOING_ID="47fc9ee4"

for item_id in $TODO_ITEMS; do
  gh project item-edit --id "$item_id" --project-id "$PROJECT_ID" \
    --field-id "$STATUS_FIELD_ID" --single-select-option-id "$DOING_ID"
done
```

### Pattern 3: Update from issue metadata

Set project fields based on issue labels:

```bash
# If issue has "bug" label, set Value=Essential
if gh issue view 123 --json labels --jq '.labels[].name' | grep -q "bug"; then
  PROJECT_ID="PVT_kwHOAvtmyM4BCtNb"
  VALUE_FIELD_ID="PVTSSF_lAHOAvtmyM4BCtNbzg01ul0"
  ESSENTIAL_ID="5885ea3a"

  gh project item-edit --id "$ITEM_ID" --project-id "$PROJECT_ID" \
    --field-id "$VALUE_FIELD_ID" --single-select-option-id "$ESSENTIAL_ID"
fi
```

## Error handling

**Common issues:**

1. **"project scope required"**
   ```bash
   gh auth refresh -s project
   ```

2. **"Field type not supported"**
   - Some field types (like parent_issue) cannot be edited via API
   - Use web UI for unsupported fields

3. **"Item not found"**
   - Verify item is in the project
   - Check that item ID is correct (starts with `PVTI_`)

4. **"Invalid option ID"**
   - Option IDs change if field options are modified
   - Re-fetch field configuration to get current IDs

## Best practices

**Value/Effort prioritization matrix:**
- **Essential + Light** = Quick wins (do first!)
- **Essential + Moderate** = Core work (plan and execute)
- **Essential + Heavy** = Strategic investments (careful planning required)
- **Useful + Light** = Easy improvements (fill-in tasks)
- **Useful + Moderate** = Standard backlog work
- **Useful + Heavy** = Consider scope reduction or phasing
- **Nice-to-have + Light** = Low priority improvements
- **Nice-to-have + Moderate/Heavy** = Usually defer or reject

**Status workflow:**
- `Backlog` → Items not yet prioritized or lacking clear requirements
- `Todo` → Requirements defined, ready to pick up (next in queue)
- `Doing` → Active work in progress
- `Done` → Work completed and merged

**Use issue dependencies instead of "Blocked" status:**
- Set `blockedBy` relationships using the `gh-issue-dependencies` skill
- Dependencies are more explicit and trackable than status alone
- Status should reflect work state, dependencies reflect constraints

**Maintenance:**
- Keep Status current as work progresses
- Set Value/Effort during triage and planning sessions
- Review `Backlog` periodically to prune or promote items to `Todo`
- Move completed items to `Done` when merged

## Integration with workflows

**Works well with:**
- `gh-issue-dependencies` skill - Set Status=Blocked when dependencies exist
- `git-issue-create` agent - Add to project and set fields when creating issues
- `git-issue-deliver` agent - Update Status as work progresses
- GitHub Actions - Automate field updates on events

**Automation ideas:**
- Auto-set Status=Doing when PR opens (work in progress)
- Auto-set Status=Done when PR merges
- Auto-set Value=Essential for security/critical labels
- Alert on Essential + Heavy items (require careful planning)
- Auto-promote Todo items to Doing when branch created