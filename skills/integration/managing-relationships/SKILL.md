---
name: managing-relationships
description: Expert at managing GitHub issue relationships including parent/sub-issues, blocking dependencies, and tracking links using the GraphQL API. Auto-invokes when creating issue hierarchies, setting parent-child relationships, managing dependencies, or linking related issues.
version: 1.0.0
allowed-tools: Read, Bash, Grep, Glob
---

# Managing Relationships Skill

You are an expert at managing GitHub issue relationships using the GraphQL API. This skill provides capabilities beyond the standard `gh issue` CLI, enabling proper parent-child hierarchies, dependency tracking, and issue linking.

## When to Use This Skill

Auto-invoke this skill when the conversation involves:
- Creating parent-child issue relationships (sub-issues)
- Setting up issue hierarchies or epics
- Managing blocking/blocked-by dependencies
- Linking related issues
- Querying issue relationship graphs
- Keywords: "parent issue", "sub-issue", "child issue", "blocked by", "blocking", "depends on", "epic", "hierarchy"

## Your Capabilities

### 1. **Sub-Issue Management (Parent-Child)**

Create explicit parent-child relationships using GitHub's sub-issues feature.

**Add Sub-Issue:**
```bash
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue \
  --parent 67 \
  --child 68
```

**Remove Sub-Issue:**
```bash
python3 {baseDir}/scripts/manage-relationships.py remove-sub-issue \
  --parent 67 \
  --child 68
```

**List Sub-Issues:**
```bash
python3 {baseDir}/scripts/manage-relationships.py list-sub-issues --issue 67
```

### 2. **Dependency Management (Blocking)**

Track blocking dependencies between issues.

**View Dependencies:**
```bash
python3 {baseDir}/scripts/manage-relationships.py show-dependencies --issue 68
```

### 3. **Relationship Queries**

Query complex relationship graphs.

**Get Parent:**
```bash
python3 {baseDir}/scripts/manage-relationships.py get-parent --issue 68
```

**Get All Relationships:**
```bash
python3 {baseDir}/scripts/manage-relationships.py show-all --issue 67
```

## GraphQL API Reference

### Key Mutations

#### addSubIssue
Creates a parent-child relationship.

```graphql
mutation {
  addSubIssue(input: {
    issueId: "PARENT_NODE_ID",
    subIssueId: "CHILD_NODE_ID"
  }) {
    issue { number title }
    subIssue { number title }
  }
}
```

**Input Fields:**
- `issueId` (required): Parent issue node ID
- `subIssueId`: Child issue node ID
- `subIssueUrl`: Alternative - child issue URL
- `replaceParent`: Boolean to replace existing parent

#### removeSubIssue
Removes a parent-child relationship.

```graphql
mutation {
  removeSubIssue(input: {
    issueId: "PARENT_NODE_ID",
    subIssueId: "CHILD_NODE_ID"
  }) {
    issue { number }
    subIssue { number }
  }
}
```

#### reprioritizeSubIssue
Reorders sub-issues within a parent.

```graphql
mutation {
  reprioritizeSubIssue(input: {
    issueId: "PARENT_NODE_ID",
    subIssueId: "CHILD_NODE_ID",
    afterId: "SIBLING_NODE_ID"
  }) {
    issue { number }
  }
}
```

### Key Query Fields

#### Issue Relationships

```graphql
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 67) {
      # Parent-child
      parent { number title }
      subIssues(first: 50) {
        nodes { number title state }
      }
      subIssuesSummary {
        total
        completed
        percentCompleted
      }

      # Dependencies
      blockedBy(first: 10) {
        nodes { number title }
      }
      blocking(first: 10) {
        nodes { number title }
      }

      # Tracking (from task lists)
      trackedInIssues(first: 10) {
        nodes { number title }
      }
      trackedIssues(first: 10) {
        nodes { number title }
      }
      trackedIssuesCount
    }
  }
}
```

## Direct GraphQL Usage

For operations not covered by scripts, use `gh api graphql` directly:

### Get Issue Node IDs

```bash
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 67) { id }
  }
}'
```

### Add Multiple Sub-Issues

```bash
gh api graphql -f query='
mutation {
  add1: addSubIssue(input: {issueId: "PARENT_ID", subIssueId: "CHILD1_ID"}) {
    subIssue { number }
  }
  add2: addSubIssue(input: {issueId: "PARENT_ID", subIssueId: "CHILD2_ID"}) {
    subIssue { number }
  }
}'
```

### Query Full Hierarchy

```bash
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    issue(number: 67) {
      number
      title
      subIssues(first: 100) {
        nodes {
          number
          title
          state
          subIssues(first: 10) {
            nodes { number title }
          }
        }
      }
    }
  }
}'
```

## Workflow Patterns

### Pattern 1: Create Issue Hierarchy

When creating a parent issue with children:

1. Create all issues first
2. Get node IDs for parent and children
3. Add each child as sub-issue of parent
4. Verify relationships

```bash
# Step 1: Get IDs
python3 {baseDir}/scripts/manage-relationships.py get-ids --issues 67,68,69,70

# Step 2: Add relationships
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue --parent 67 --child 68
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue --parent 67 --child 69
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue --parent 67 --child 70

# Step 3: Verify
python3 {baseDir}/scripts/manage-relationships.py list-sub-issues --issue 67
```

### Pattern 2: Epic with Nested Sub-Issues

For complex hierarchies:

```
Epic (#1)
├── Feature A (#2)
│   ├── Task A1 (#5)
│   └── Task A2 (#6)
└── Feature B (#3)
    └── Task B1 (#7)
```

```bash
# Top-level children
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue --parent 1 --child 2
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue --parent 1 --child 3

# Nested children
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue --parent 2 --child 5
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue --parent 2 --child 6
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue --parent 3 --child 7
```

### Pattern 3: Move Issue to New Parent

```bash
# Use replaceParent flag
python3 {baseDir}/scripts/manage-relationships.py add-sub-issue \
  --parent 100 \
  --child 68 \
  --replace-parent
```

## Error Handling

### Common Errors

**"Issue may not contain duplicate sub-issues"**
- Child is already a sub-issue of this parent
- Check existing relationships first

**"Sub issue may only have one parent"**
- Child already has a different parent
- Use `--replace-parent` flag or remove from current parent first

**"Issue not found"**
- Verify issue numbers exist
- Check repository owner/name

### Troubleshooting

```bash
# Check if issue has parent
python3 {baseDir}/scripts/manage-relationships.py get-parent --issue 68

# List all relationships
python3 {baseDir}/scripts/manage-relationships.py show-all --issue 68
```

## Integration with Other Skills

### With creating-issues skill
- After creating issues, use this skill to establish relationships
- Reference parent in issue body: "Part of #67"

### With organizing-with-labels skill
- Labels indicate type, relationships indicate structure
- Use together for complete issue organization

### With managing-projects skill
- Sub-issues appear in project boards
- Track hierarchy progress in projects

## Environment Requirements

This skill requires:
- `gh` CLI authenticated with appropriate permissions
- Repository with Issues enabled
- GraphQL API access

## Best Practices

1. **Create issues first, then relationships** - Ensure all issues exist before linking
2. **Document relationships in body** - Add "Part of #X" for visibility
3. **Check for existing parents** - Avoid orphaning issues
4. **Use hierarchies sparingly** - Deep nesting (>3 levels) becomes hard to manage
5. **Combine with labels** - Use `type:epic` label for parent issues

## Limitations

- **One parent per issue** - Cannot have multiple parents
- **No circular references** - A cannot be parent of B if B is ancestor of A
- **API rate limits** - Batch operations carefully
- **Blocking relationships** - Currently read-only via API (manage in UI)

## Resources

### Scripts
- **manage-relationships.py**: Main CLI for relationship operations

### References
- **graphql-schema.md**: Full GraphQL schema documentation
- **relationship-patterns.md**: Common hierarchy patterns

## Common Mistakes

### Mistake 1: Using Task Lists Instead of Sub-Issues API

```markdown
❌ WRONG - Task lists create "tracked" relationships, not parent-child:
## Child Issues
- [ ] #68
- [ ] #69
- [ ] #70

✅ CORRECT - Use GraphQL addSubIssue mutation:
python manage-relationships.py add-sub-issue --parent 67 --child 68
python manage-relationships.py add-sub-issue --parent 67 --child 69
python manage-relationships.py add-sub-issue --parent 67 --child 70
```

**Why it matters**:
- Task lists only create "tracked by" links visible in the issue sidebar
- Sub-issues create true parent-child hierarchy with:
  - Progress tracking (3/4 completed, 75%)
  - Hierarchical navigation in GitHub UI
  - Sub-issue aggregation and rollup

### Mistake 2: Not Getting Issue Node IDs First

```markdown
❌ WRONG - Using issue numbers directly in GraphQL:
mutation {
  addSubIssue(input: {issueId: "67", subIssueId: "68"}) { ... }
}

✅ CORRECT - Get node IDs first, then use them:
# Step 1: Get node IDs
python manage-relationships.py get-ids --issues 67,68

# Step 2: Use node IDs in mutation
mutation {
  addSubIssue(input: {
    issueId: "I_kwDOQTQw6c7Z4spt",
    subIssueId: "I_kwDOQTQw6c7Z4swL"
  }) { ... }
}
```

**Why it matters**: GraphQL uses node IDs (not issue numbers). The script handles this automatically, but direct API calls require the conversion.

### Mistake 3: Not Checking for Existing Parent

```markdown
❌ WRONG - Adding sub-issue without checking existing parent:
python manage-relationships.py add-sub-issue --parent 100 --child 68
# Error: Sub issue may only have one parent

✅ CORRECT - Check first, then use --replace-parent if needed:
# Check existing parent
python manage-relationships.py get-parent --issue 68

# If has parent, use replace flag
python manage-relationships.py add-sub-issue --parent 100 --child 68 --replace-parent
```

**Why it matters**: Each issue can only have one parent. Attempting to add to a new parent without the replace flag will fail.

### Mistake 4: Creating Circular References

```markdown
❌ WRONG - Creating cycles in hierarchy:
# A is parent of B
python manage-relationships.py add-sub-issue --parent A --child B
# Then trying to make B parent of A
python manage-relationships.py add-sub-issue --parent B --child A
# Error: Cannot create circular reference

✅ CORRECT - Plan hierarchy before creating:
Epic (#1)
├── Feature A (#2)
│   └── Task A1 (#5)
└── Feature B (#3)
    └── Task B1 (#7)
```

**Why it matters**: GitHub prevents circular references. Plan your hierarchy structure before creating relationships.

### Mistake 5: Not Verifying After Creation

```markdown
❌ WRONG - Adding relationships without verification:
python manage-relationships.py add-sub-issue --parent 67 --child 68
# Just assume it worked

✅ CORRECT - Verify relationships were created:
python manage-relationships.py add-sub-issue --parent 67 --child 68
python manage-relationships.py list-sub-issues --issue 67
# Confirms: Sub-issues (4): #68, #69, #70, #71
```

**Why it matters**: API calls can fail silently or partially. Always verify the result matches expectations.

### Mistake 6: Deep Nesting (>3 Levels)

```markdown
❌ WRONG - Too many levels of nesting:
Epic
└── Theme
    └── Feature
        └── Story
            └── Task
                └── Subtask (6 levels!)

✅ CORRECT - Keep hierarchy shallow (2-3 levels):
Epic
├── Feature A
│   ├── Task A1
│   └── Task A2
└── Feature B
    └── Task B1
```

**Why it matters**: Deep nesting becomes hard to manage and navigate. Most projects work well with 2-3 levels maximum.

## Important Notes

- The standard `gh issue` CLI does NOT support relationship management
- Always use GraphQL API via `gh api graphql` for relationships
- Sub-issues appear in GitHub UI with progress tracking
- Task list checkboxes (`- [ ] #68`) create "tracked" relationships, not parent-child
- Each issue can have only ONE parent (no multiple inheritance)
- Verify relationships after creation to confirm success
