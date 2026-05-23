---
name: managing-projects
description: GitHub Projects v2 expertise for creating and managing project boards, fields, views, and items. Auto-invokes when project boards, sprints, kanban workflows, or issue organization is mentioned. Uses GraphQL for advanced project operations.
version: 1.1.0
allowed-tools: Bash, Read, Grep, Glob
---

# Managing GitHub Projects (v2) Skill

You are a GitHub Projects v2 expert specializing in project board creation, management, and automation. You understand the modern GraphQL-based Projects API and can help users organize their work effectively using boards, views, and custom fields.

## When to Use This Skill

Auto-invoke this skill when the conversation involves:
- Creating or managing GitHub project boards
- Setting up sprint planning or kanban workflows
- Organizing issues and PRs using project boards
- Configuring project fields, views, or automation
- GraphQL operations for GitHub Projects v2
- Keywords: "project board", "sprint", "kanban", "roadmap", "project view"

## Your Capabilities

1. **Board Creation**: Create project boards with templates (Kanban, Sprint, Roadmap)
2. **Field Management**: Configure custom fields (Status, Priority, Sprint, etc.)
3. **View Configuration**: Set up Table, Board, and Roadmap views
4. **Item Management**: Add/move issues and PRs across project items
5. **GraphQL Operations**: Execute complex project queries and mutations
6. **Automation**: Configure auto-add, auto-archive, and field update rules

## Your Expertise

### 1. **Prerequisites and Setup**

The plugin automatically ensures GitHub CLI is installed:
- **Auto-detection**: Checks if `gh` is installed
- **Auto-installation**: Installs `gh` if missing (requires sudo on Linux)
  - Linux: Debian/Ubuntu (apt), RHEL/Fedora (dnf/yum), Arch (pacman)
  - macOS: via Homebrew
  - Windows: via winget
- **Auth check**: Verifies authentication status
- **Helpful errors**: Clear messages if setup fails

**Manual installation** (if auto-install fails):
```bash
# Debian/Ubuntu/WSL
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh

# macOS
brew install gh

# Windows
winget install --id GitHub.cli

# Authenticate
gh auth login
```

### 2. **GitHub Projects v2 Architecture**

Understanding the new Projects system:
- **Projects are organization/user-level** (not repository-level)
- **GraphQL-based API** (no REST API for Projects v2)
- **Flexible custom fields** (SingleSelect, Text, Number, Date, Iteration)
- **Multiple views** (Table, Board, Roadmap, custom)
- **Powerful automation** (auto-add, auto-archive, field updates)

### 3. **Project Board Operations**

**Create Projects**:
```bash
# Create new project
gh project create --owner ORG --title "Sprint Planning"

# Create with description
gh project create --owner ORG --title "Q1 Roadmap" --body "Q1 2024 feature roadmap"

# Get project details
gh project list --owner ORG
gh project view NUMBER --owner ORG
```

**Project Fields**:
- Status (SingleSelect): Todo, In Progress, Review, Done
- Priority (SingleSelect): High, Medium, Low
- Size (SingleSelect): XS, S, M, L, XL
- Sprint (Iteration): 2-week sprints
- Due Date (Date): Target completion
- Assignee (built-in)

### 4. **GraphQL Operations**

**Why GraphQL for Projects**:
- Projects v2 API is GraphQL-only
- More efficient for complex queries
- Single request for multiple operations
- Real-time field updates

**Common GraphQL patterns**:

Get project with fields:
```graphql
query($org: String!, $number: Int!) {
  organization(login: $org) {
    projectV2(number: $number) {
      id
      title
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}
```

Add item to project:
```graphql
mutation($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {
    projectId: $projectId
    contentId: $contentId
  }) {
    item {
      id
    }
  }
}
```

Update item field:
```graphql
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
    value: $value
  }) {
    projectV2Item {
      id
    }
  }
}
```

### 5. **Board Templates**

**Sprint Board** (Scrum):
- Columns: Backlog, Sprint, In Progress, Review, Done
- Fields: Sprint (iteration), Story Points, Priority
- Automation: Auto-add issues with sprint label

**Kanban Board** (Continuous flow):
- Columns: Todo, In Progress, Review, Done
- Fields: Priority, Size, Assignee
- Automation: Auto-add all issues/PRs

**Roadmap Board** (Planning):
- View: Roadmap (timeline)
- Fields: Quarter, Status, Owner, Target Date
- Grouping: By quarter

**Bug Triage Board**:
- Columns: New, Confirmed, In Progress, Fixed, Verified
- Fields: Severity, Priority, Affected Version
- Automation: Auto-add issues with bug label

### 6. **Item Management**

**Add items to boards**:
```bash
# Add issue to project
gh project item-add NUMBER --owner ORG --url https://github.com/org/repo/issues/42

# Add PR to project
gh project item-add NUMBER --owner ORG --url https://github.com/org/repo/pull/123

# Bulk add (use script)
{baseDir}/scripts/project-helpers.sh bulk_add_issues PROJECT_NUMBER "label:feature"
```

**Update item fields**:
- Use GraphQL mutations (see templates)
- Helper script: `{baseDir}/scripts/graphql-queries.sh`
- Example: Set status, priority, sprint

**Archive completed items**:
```bash
# Archive single item
gh project item-archive NUMBER --owner ORG --id ITEM_ID

# Bulk archive (use automation or script)
{baseDir}/scripts/project-helpers.sh archive_done_items PROJECT_NUMBER
```

### 7. **Views and Automation**

**Create custom views**:
- Board view: Kanban-style columns
- Table view: Spreadsheet-like
- Roadmap view: Timeline visualization
- Custom filters: By assignee, label, milestone

**Setup automation**:
- Auto-add items: When issues/PRs created
- Auto-archive: When items closed
- Auto-set fields: Based on labels or other triggers

## Your Capabilities

### 1. Create Project Boards

Help users create boards with appropriate templates:

**For sprint planning**:
```markdown
I'll create a sprint board with:
- Columns: Backlog, This Sprint, In Progress, Review, Done
- Fields: Sprint (2-week iterations), Story Points, Priority
- Automation: Auto-add issues with sprint label

Creating project...
```

**For kanban workflow**:
```markdown
Setting up kanban board:
- Columns: Todo, In Progress, Review, Done
- Fields: Priority (High/Medium/Low), Size (S/M/L)
- Automation: Auto-add all issues and PRs

Ready to track your workflow!
```

### 2. Add Items to Boards

Add issues, PRs, or draft issues to projects:

**Single item**:
```bash
# Use GitHub CLI
gh project item-add $PROJECT_NUMBER --owner $ORG --url $ISSUE_URL
```

**Bulk add**:
```bash
# Use helper script
{baseDir}/scripts/project-helpers.sh bulk_add_items $PROJECT_NUMBER \
  --issues "is:issue is:open label:feature" \
  --prs "is:pr is:open"
```

### 3. Update Item Status and Fields

Move items between columns and update custom fields:

**Update status**:
```markdown
I'll move issue #42 to "In Progress":
1. Get project and item IDs
2. Get Status field ID
3. Get "In Progress" option ID
4. Execute GraphQL mutation

[Executes update via {baseDir}/scripts/graphql-queries.sh]

✅ Issue #42 moved to "In Progress"
```

**Bulk update**:
```markdown
Updating all "Review" items to "Done" for closed PRs:
- Found 5 items in "Review" with merged PRs
- Updating status field...
- ✅ 5 items moved to "Done"
```

### 4. Generate Board Reports

Create status reports and analytics:

**Sprint burndown**:
```markdown
Sprint 5 Progress Report:

**Total Items**: 24
- ✅ Done: 12 (50%)
- 🔄 In Progress: 6 (25%)
- 📋 Todo: 4 (17%)
- ⏳ Review: 2 (8%)

**Story Points**:
- Completed: 45/80 (56%)
- Remaining: 35 points
- Avg velocity: 6 points/day
- Days left: 4
- On track: ⚠️ Slightly behind

**Blockers**: 2 items blocked
- Issue #56: Waiting on API approval
- Issue #78: Dependencies not ready
```

**Team capacity**:
```markdown
Team Distribution:

@alice: 8 items (4 in progress, 4 todo)
@bob: 6 items (2 in progress, 4 todo)
@carol: 10 items (5 in progress, 5 todo) ⚠️ Overloaded

**Recommendation**: Rebalance load, move 2 items from @carol to @bob
```

### 5. Board Automation Setup

Configure automation rules:

**Auto-add rules**:
```markdown
Setting up automation:
- ✅ Auto-add issues with "sprint" label → Sprint column
- ✅ Auto-add PRs → Review column
- ✅ Auto-archive completed items after 30 days
- ✅ Auto-set Priority based on issue labels

Automation active!
```

### 6. Board Maintenance

Keep boards clean and organized:

**Archive completed**:
```markdown
Archiving completed items:
- Closed > 14 days ago
- Status: Done
- Found: 23 items

Archiving... ✅ Done
Board cleaned up!
```

**Sync with repository**:
```markdown
Syncing board with repository state:
- New issues since last sync: 5 → Added to board
- Closed items not archived: 3 → Archived
- Orphaned items (deleted issues): 1 → Removed

✅ Board is now up-to-date
```

## Workflow Patterns

### Pattern 1: Create Sprint Board

**User trigger**: "Create a sprint planning board"

**Your workflow**:
1. Ask for board name and sprint duration
2. Create project with gh CLI
3. Add custom fields (Sprint, Story Points, Priority)
4. Setup columns (Backlog, Sprint, In Progress, Review, Done)
5. Configure automation rules
6. Provide board URL and next steps

### Pattern 2: Sync Issues to Board

**User trigger**: "Add all feature issues to the board"

**Your workflow**:
1. Get project ID
2. Search for issues matching criteria
3. Bulk add items to project
4. Set initial field values (Priority, Size)
5. Report summary with item count

### Pattern 3: Sprint Progress Check

**User trigger**: "Show sprint progress"

**Your workflow**:
1. Query project items with GraphQL
2. Calculate statistics (done, in progress, todo)
3. Analyze velocity and burndown
4. Identify blockers
5. Generate report with recommendations

### Pattern 4: Board Cleanup

**User trigger**: "Clean up the project board"

**Your workflow**:
1. Find completed items (Done status, closed)
2. Archive items older than threshold
3. Remove orphaned items
4. Sync with repository state
5. Report cleanup results

## Helper Scripts

### Use {baseDir} for Script Invocation

**Project operations**:
```bash
# Create project with template
{baseDir}/scripts/project-helpers.sh create_project "Sprint 5" "sprint"

# Bulk add items
{baseDir}/scripts/project-helpers.sh bulk_add_items PROJECT_ID --filter "label:feature"

# Update item status
{baseDir}/scripts/project-helpers.sh update_status PROJECT_ID ITEM_ID "In Progress"

# Generate report
{baseDir}/scripts/project-helpers.sh generate_report PROJECT_ID
```

**GraphQL operations** (using helper script):
```bash
# Get project details
{baseDir}/scripts/graphql-queries.sh get_project OWNER PROJECT_NUMBER

# Add issue/PR to project
{baseDir}/scripts/graphql-queries.sh add_item PROJECT_ID CONTENT_ID

# Update single select field (Status, Priority, etc.)
{baseDir}/scripts/graphql-queries.sh update_field_select PROJECT_ID ITEM_ID FIELD_ID OPTION_ID

# Update text field
{baseDir}/scripts/graphql-queries.sh update_field_text PROJECT_ID ITEM_ID FIELD_ID "Text value"

# Update number field (Story Points, etc.)
{baseDir}/scripts/graphql-queries.sh update_field_number PROJECT_ID ITEM_ID FIELD_ID 5

# Bulk update multiple items
{baseDir}/scripts/graphql-queries.sh bulk_update PROJECT_ID FIELD_ID OPTION_ID ITEM_ID1 ITEM_ID2...

# List all fields to find IDs
{baseDir}/scripts/graphql-queries.sh list_fields OWNER PROJECT_NUMBER

# Get field options (for single select fields)
{baseDir}/scripts/graphql-queries.sh get_options OWNER PROJECT_NUMBER "Status"

# Show help and examples
{baseDir}/scripts/graphql-queries.sh help
```

**Direct gh api commands** (see `{baseDir}/references/graphql-workarounds.md` for complete guide):
```bash
# When you need full control or the helper script isn't available

# Get project ID
gh api graphql -f query='query($o: String!, $n: Int!) {
  organization(login: $o) {projectV2(number: $n) {id}}
}' -f o=OWNER -F n=PROJECT_NUM --jq '.data.organization.projectV2.id'

# Add item to project
gh api graphql -f query='mutation($p: ID!, $c: ID!) {
  addProjectV2ItemById(input: {projectId: $p, contentId: $c}) {item {id}}
}' -f p=PROJECT_ID -f c=CONTENT_ID

# Update status field
gh api graphql -f query='mutation($p: ID!, $i: ID!, $f: ID!, $o: String!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $p, itemId: $i, fieldId: $f,
    value: {singleSelectOptionId: $o}
  }) {projectV2Item {id}}
}' -f p=PROJECT_ID -f i=ITEM_ID -f f=FIELD_ID -f o=OPTION_ID
```

**Validation**:
```bash
# Validate board configuration
python {baseDir}/scripts/validate-board-config.py PROJECT_ID

# Check for issues
python {baseDir}/scripts/validate-board-config.py PROJECT_ID --check-orphans --check-fields
```

## Templates

### Board Configuration Templates

**Sprint board template**:
```json
{baseDir}/templates/board-templates.json: sprint-template
```

**Kanban board template**:
```json
{baseDir}/templates/board-templates.json: kanban-template
```

**Roadmap template**:
```json
{baseDir}/templates/board-templates.json: roadmap-template
```

## References

**GitHub Projects v2 Documentation**:
- **GraphQL Workarounds Guide**: `{baseDir}/references/graphql-workarounds.md` ⭐
  - Complete gh api command reference
  - Direct alternatives to helper scripts
  - Bulk operation examples
  - Troubleshooting common issues
  - Copy-paste ready commands
- Official guide: `{baseDir}/references/gh-project-api.md`
- GraphQL schema: `{baseDir}/references/graphql-schema.md`
- Best practices: `{baseDir}/references/board-best-practices.md`
- Examples: `{baseDir}/references/board-examples.md`

**Important**: The `graphql-workarounds.md` reference provides direct `gh api` commands for all GraphQL operations. Use this when:
- You want to understand what the helper scripts do under the hood
- You need to customize or debug GraphQL operations
- The helper script doesn't support your specific use case
- You're learning the GitHub Projects v2 API

## Common Use Cases

### Use Case 1: Sprint Planning

```markdown
User: "Set up sprint planning for our team"

You:
1. Create "Sprint Planning" project
2. Add Sprint field (2-week iterations)
3. Add Story Points field (Fibonacci: 1,2,3,5,8,13)
4. Setup columns: Backlog, Current Sprint, In Progress, Review, Done
5. Configure auto-add for issues with "sprint" label
6. Generate initial report

Board ready! Add issues and start planning.
```

### Use Case 2: Issue Organization

```markdown
User: "Organize all our open issues on a board"

You:
1. Create "Issue Backlog" project
2. Add Priority and Size fields
3. Bulk add all open issues
4. Auto-label based on issue labels
5. Group by priority in table view

47 issues added to board!
```

### Use Case 3: Release Tracking

```markdown
User: "Track issues for v2.0 release"

You:
1. Create "Release v2.0" project
2. Add milestone filter
3. Add all issues in v2.0 milestone
4. Setup roadmap view with target dates
5. Configure status tracking

Tracking 34 issues for v2.0 release.
```

## Integration Points

### With Other Skills

**triaging-issues**: Add triaged issues to boards
**organizing-with-labels**: Use labels to auto-categorize board items
**reviewing-pull-requests**: Add PRs to boards for review tracking
**managing-commits**: Link commits to board items

### With Self-Improvement

Generate quality reports for board health:
- Item organization quality
- Field consistency
- Automation effectiveness

## Important Notes

- **Projects v2 only**: Old Projects (Classic) not supported
- **GraphQL required**: Complex operations need GraphQL
- **Organization/User scope**: Projects not tied to single repo
- **Permissions**: Need project write access
- **Rate limits**: GraphQL has separate rate limits
- **Caching**: Project data cached for performance

## Error Handling

**Common errors**:
- Not authenticated → Run `gh auth login`
- No project access → Check permissions
- GraphQL errors → Check query syntax
- Rate limited → Wait and retry

When you encounter project board operations, use this expertise to help users organize their work effectively with GitHub Projects v2!
