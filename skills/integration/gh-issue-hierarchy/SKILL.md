---
name: Managing GitHub Issue Hierarchies
description: Manages GitHub issue parent-child relationships and sub-issues using REST and GraphQL APIs. Use when breaking down large work into Epics/Features/Tasks, creating work breakdown structures, converting markdown checklists to sub-issues, reordering sub-issues, or querying issue hierarchies. Handles ID confusion between REST numeric IDs and GraphQL node IDs.
---

# GitHub Issue Hierarchy

Manage GitHub issue parent-child relationships (sub-issues) using the REST and GraphQL APIs.

## What you should do

When invoked, help the user manage issue hierarchies by:

1. **Understanding the request** - Determine what hierarchy operation is needed:
   - Add sub-issue to parent
   - Remove sub-issue from parent
   - Query issue hierarchy (show tree)
   - Convert checklist items to sub-issues
   - Reorder sub-issues
   - Move sub-issue to different parent

2. **Get issue information** - If not provided, ask the user:
   - Which issue is the parent?
   - Which issue(s) should be sub-issues?
   - Repository owner and name (if not in current repo)

3. **Execute the appropriate operation** based on the request type.

## Core operations

### 1. Add sub-issue to parent

**Using REST API:**
```bash
# Get the issue ID (not node_id) from REST API
PARENT_ID=$(gh api "repos/OWNER/REPO/issues/PARENT_NUMBER" --jq '.id')
SUB_ISSUE_ID=$(gh api "repos/OWNER/REPO/issues/SUB_NUMBER" --jq '.id')

# Add sub-issue
gh api --method POST "repos/OWNER/REPO/issues/$PARENT_ID/sub_issues" \
  -f sub_issue_id="$SUB_ISSUE_ID"
```

**Using GraphQL:**
```bash
# Get node IDs
PARENT_NODE_ID=$(gh api graphql -f query='
  query {
    repository(owner: "OWNER", name: "REPO") {
      issue(number: PARENT_NUMBER) { id }
    }
  }' --jq '.data.repository.issue.id')

SUB_NODE_ID=$(gh api graphql -f query='
  query {
    repository(owner: "OWNER", name: "REPO") {
      issue(number: SUB_NUMBER) { id }
    }
  }' --jq '.data.repository.issue.id')

# Add sub-issue
gh api graphql -f query='
mutation {
  addSubIssue(input: {
    issueId: "'$PARENT_NODE_ID'"
    subIssueId: "'$SUB_NODE_ID'"
  }) {
    issue {
      number
      title
    }
  }
}'
```

### 2. Remove sub-issue from parent

**Using REST API:**
```bash
# Get IDs
PARENT_ID=$(gh api "repos/OWNER/REPO/issues/PARENT_NUMBER" --jq '.id')
SUB_ISSUE_ID=$(gh api "repos/OWNER/REPO/issues/SUB_NUMBER" --jq '.id')

# Remove sub-issue
gh api --method DELETE "repos/OWNER/REPO/issues/$PARENT_ID/sub_issues/$SUB_ISSUE_ID"
```

**Using GraphQL:**
```bash
gh api graphql -f query='
mutation {
  removeSubIssue(input: {
    issueId: "'$PARENT_NODE_ID'"
    subIssueId: "'$SUB_NODE_ID'"
  }) {
    issue {
      number
      title
    }
  }
}'
```

### 3. Get parent of an issue

**Using REST API:**
```bash
gh api "repos/OWNER/REPO/issues/ISSUE_NUMBER/parent" --jq '{number: .number, title: .title}'
```

### 4. List all sub-issues of a parent

**Using GraphQL:**
```bash
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: PARENT_NUMBER) {
      number
      title
      subIssues(first: 50) {
        nodes {
          number
          title
          state
        }
        totalCount
      }
    }
  }
}' --jq '.data.repository.issue'
```

### 5. Query full hierarchy tree

**Get complete hierarchy including nested levels:**
```bash
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: PARENT_NUMBER) {
      number
      title
      subIssues(first: 50) {
        nodes {
          number
          title
          state
          subIssues(first: 50) {
            nodes {
              number
              title
              state
            }
          }
        }
      }
    }
  }
}'
```

### 6. Reorder sub-issues

**Change position in parent's sub-issue list:**
```bash
# Move sub-issue to specific position (0-indexed)
PARENT_ID=$(gh api "repos/OWNER/REPO/issues/PARENT_NUMBER" --jq '.id')
SUB_ISSUE_ID=$(gh api "repos/OWNER/REPO/issues/SUB_NUMBER" --jq '.id')

gh api --method PATCH "repos/OWNER/REPO/issues/$PARENT_ID/sub_issues/$SUB_ISSUE_ID" \
  -f position=0  # Move to first position
```

## Key concepts

### Terminology
- **Parent issue**: Top-level issue that contains sub-issues (often an Epic or Feature)
- **Sub-issue**: Child issue that is part of a parent's work breakdown
- **Hierarchy**: Tree structure of parent-child relationships
- **Node ID**: Global GitHub identifier starting with `I_` (for GraphQL)
- **Numeric ID**: Integer ID from REST API (different from node_id!)

### Important notes

**ID confusion:**
- REST API uses numeric `id` field (integer)
- GraphQL uses `id` field (string starting with `I_`)
- `gh issue view --json id` returns node_id, NOT the REST numeric ID
- Always fetch IDs using the appropriate API method

**Inheritance:**
- Sub-issues inherit Project and Milestone from parent by default
- Cross-organization sub-issues are supported
- Sub-issues can have their own sub-issues (nested hierarchy)

### Common patterns

**Work breakdown structure:**
```
Epic #100: Add authentication system
  ├─ Feature #101: Implement JWT tokens
  ├─ Feature #102: Add login UI
  │   ├─ Task #103: Design login form
  │   └─ Task #104: Add validation
  └─ Feature #105: Add session management
```

**Release planning:**
```
Release #200: v2.0.0
  ├─ #201: Feature A
  ├─ #202: Feature B
  └─ #203: Bug fixes
```

**Milestone tracking:**
```
Milestone #300: Q1 Goals
  ├─ #301: Improve performance
  ├─ #302: Add monitoring
  └─ #303: Security audit
```

## Complete workflow examples

### Example 1: Create Epic with sub-tasks

```bash
# Create parent Epic
EPIC_NUMBER=$(gh issue create \
  --title "Add authentication system" \
  --body "Epic for implementing user authentication" \
  --label "epic" \
  --json number --jq '.number')

# Create sub-issues
TASK1=$(gh issue create --title "Implement JWT tokens" --json number --jq '.number')
TASK2=$(gh issue create --title "Add login UI" --json number --jq '.number')
TASK3=$(gh issue create --title "Add session management" --json number --jq '.number')

# Add as sub-issues
EPIC_ID=$(gh api "repos/OWNER/REPO/issues/$EPIC_NUMBER" --jq '.id')

for task in $TASK1 $TASK2 $TASK3; do
  TASK_ID=$(gh api "repos/OWNER/REPO/issues/$task" --jq '.id')
  gh api --method POST "repos/OWNER/REPO/issues/$EPIC_ID/sub_issues" \
    -f sub_issue_id="$TASK_ID"
done

echo "✅ Created Epic #$EPIC_NUMBER with 3 sub-tasks"
```

### Example 2: Convert checklist to sub-issues

```bash
# Given an issue with checklist in body:
# - [ ] Implement JWT tokens
# - [ ] Add login UI
# - [ ] Add session management

PARENT_NUMBER=100
PARENT_ID=$(gh api "repos/OWNER/REPO/issues/$PARENT_NUMBER" --jq '.id')

# Extract checklist items and create sub-issues
gh issue view $PARENT_NUMBER --json body --jq '.body' | \
  grep -E '^\s*-\s+\[ \]' | \
  sed 's/^\s*-\s*\[ \]\s*//' | \
  while read -r task; do
    echo "Creating: $task"
    ISSUE_NUM=$(gh issue create --title "$task" --json number --jq '.number')
    ISSUE_ID=$(gh api "repos/OWNER/REPO/issues/$ISSUE_NUM" --jq '.id')
    gh api --method POST "repos/OWNER/REPO/issues/$PARENT_ID/sub_issues" \
      -f sub_issue_id="$ISSUE_ID"
  done
```

### Example 3: Show hierarchy tree

```bash
# Display parent with all sub-issues
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 100) {
      number
      title
      subIssues(first: 50) {
        nodes {
          number
          title
          state
        }
        totalCount
      }
    }
  }
}' --jq '.data.repository.issue |
  "Parent: #\(.number) - \(.title)\n" +
  "Sub-issues (\(.subIssues.totalCount)):\n" +
  (.subIssues.nodes | map("  ├─ #\(.number) [\(.state)] \(.title)") | join("\n"))'
```

### Example 4: Move sub-issue to different parent

```bash
# Remove from old parent
OLD_PARENT_ID=$(gh api "repos/OWNER/REPO/issues/100" --jq '.id')
SUB_ISSUE_ID=$(gh api "repos/OWNER/REPO/issues/150" --jq '.id')

gh api --method DELETE "repos/OWNER/REPO/issues/$OLD_PARENT_ID/sub_issues/$SUB_ISSUE_ID"

# Add to new parent
NEW_PARENT_ID=$(gh api "repos/OWNER/REPO/issues/200" --jq '.id')
gh api --method POST "repos/OWNER/REPO/issues/$NEW_PARENT_ID/sub_issues" \
  -f sub_issue_id="$SUB_ISSUE_ID"

echo "✅ Moved #150 from #100 to #200"
```

## Error handling

**Common issues:**

1. **"Resource not accessible by integration"**
   - Requires write access to repository
   - Check authentication and permissions

2. **"Issue is already a sub-issue"**
   - An issue can only have one parent at a time
   - Remove from current parent before adding to new one

3. **"Circular dependency detected"**
   - Cannot make a parent a sub-issue of its own child
   - Check hierarchy before creating relationships

4. **"Invalid issue ID"**
   - Ensure using numeric `id` for REST API (not `node_id`)
   - Fetch IDs using correct API method

5. **"Sub-issue limit exceeded"**
   - GitHub may limit number of sub-issues per parent
   - Consider flattening hierarchy or grouping differently

## Best practices

**When to use sub-issues:**
- Breaking down Epics into Features/Tasks
- Organizing release checklists
- Tracking multi-step implementation work
- Creating hierarchical roadmaps

**When NOT to use sub-issues:**
- Simple task lists (use markdown checklist instead)
- Temporary relationships (use labels or milestones)
- Blocking relationships (use dependencies - see `gh-issue-dependencies`)

**Hierarchy design:**
- Keep hierarchies shallow (2-3 levels max)
- Use consistent naming (Epic → Feature → Task)
- Close parent only when all children are closed
- Use labels to indicate hierarchy level (epic, feature, task)

**Combining with other features:**
- Use dependencies for ordering (Task A blocks Task B)
- Use milestones for time-based grouping
- Use labels for categorization
- Use projects for status tracking

## Related concepts

### Sub-issues vs Dependencies

**Sub-issues** (this skill):
- Decompose work: "What are the parts of this issue?"
- Parent-child hierarchy
- Epic → Features → Tasks
- Example: Epic "Add auth" has sub-issues "JWT", "Login UI", "Sessions"

**Dependencies** (see `gh-issue-dependencies` skill):
- Ordering constraints: "What must happen before this?"
- Peer-to-peer blocking relationships
- Can span unrelated features
- Example: "API schema" blocks "API implementation"

**These can be combined:**
```
Epic #100: Add authentication
  ├─ #101: JWT tokens (blocked by #200 API schema design)
  ├─ #102: Login UI
  └─ #103: Sessions (blocked by #101)
```

## Integration with workflows

**Works well with:**
- `gh-issue-dependencies` skill - Add blocking relationships between sub-issues
- `gh-project-manage` skill - Track sub-issue progress in projects
- `gh-issue-types` skill - Assign types (Epic, Feature, Task) to hierarchy levels
- `git-issue-create` agent - Create parent and children in one workflow

**Automation ideas:**
- Auto-create sub-issues from issue template checklists
- Auto-close parent when all children are closed
- Auto-inherit labels from parent to children
- Generate progress reports (X of Y sub-issues completed)
- Create release notes from Epic hierarchies

## Example usage patterns

**Recommended hierarchy levels:**

1. **Epic** (parent) - Large feature or initiative
   - Label: `epic`
   - Value: Essential or Useful
   - Effort: Heavy
   - Project field: Set manually

2. **Feature** (child of Epic) - Distinct deliverable
   - Label: `feature`
   - Inherits project from Epic
   - Set own Value/Effort

3. **Task** (child of Feature) - Implementation step
   - Label: `task`
   - Inherits project from Feature
   - Effort: Light or Moderate

**Example hierarchy:**
```
Epic #100: User authentication system
  ├─ Feature #101: Add OAuth integration
  ├─ Feature #102: Add two-factor authentication
  └─ Feature #103: Update session management
```