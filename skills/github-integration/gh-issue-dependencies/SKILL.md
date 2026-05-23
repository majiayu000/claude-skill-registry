---
name: Managing GitHub Issue Dependencies
description: Manages GitHub issue blocking/blocked-by relationships using the native dependencies feature via GraphQL API. Use when showing that one issue must complete before another can proceed, querying dependency relationships, or preventing circular dependencies.
---

# GitHub Issue Dependencies

Manage GitHub issue dependencies (blocking/blocked-by relationships) using the native GitHub dependencies feature.

## What you should do

When invoked, help the user manage issue dependencies by:

1. **Understanding the request** - Determine what dependency operation is needed:
   - Add a blocking relationship (issue X blocks issue Y)
   - Remove a blocking relationship (only for active blockers; do NOT remove when blocker is closed)
   - Query existing dependencies
   - Bulk operations on multiple issues

2. **Get issue information** - If not provided, ask the user:
   - Which issue is being blocked?
   - Which issue is blocking it?
   - Repository owner and name (if not in current repo)

3. **Execute the appropriate operation**:

   **Add blocking relationship:**
   ```bash
   gh api graphql -f query='
   mutation {
     addBlockedBy(input: {
       issueId: "BLOCKED_ISSUE_NODE_ID"
       blockingIssueId: "BLOCKING_ISSUE_NODE_ID"
     }) {
       issue {
         number
         title
       }
     }
   }'
   ```

   **Remove blocking relationship:**
   ```bash
   gh api graphql -f query='
   mutation {
     removeBlockedBy(input: {
       issueId: "BLOCKED_ISSUE_NODE_ID"
       blockingIssueId: "BLOCKING_ISSUE_NODE_ID"
     }) {
       issue {
         number
         title
       }
     }
   }'
   ```

   **Query dependencies:**
   ```bash
   gh api graphql -f query='
   query {
     repository(owner: "OWNER", name: "REPO") {
       issue(number: NUMBER) {
         number
         title
         blockedBy(first: 10) {
           nodes {
             number
             title
           }
           totalCount
         }
         blocking(first: 10) {
           nodes {
             number
             title
           }
           totalCount
         }
       }
     }
   }'
   ```

4. **Get node IDs when needed** - Convert issue numbers to node IDs:
   ```bash
   gh api graphql -f query='
   query {
     repository(owner: "OWNER", name: "REPO") {
       issue(number: NUMBER) {
         id
       }
     }
   }'
   ```

5. **Verify the operation** - After adding/removing, query to confirm the change was successful.

6. **Provide clear output** - Show the user:
   - What relationship was created/removed
   - Current state of dependencies
   - Any errors or warnings

## Key concepts

**Terminology:**
- **Blocked by**: Issue X is blocked by issue Y means Y must be resolved before X can proceed
- **Blocking**: Issue Y is blocking issue X means X cannot proceed until Y is resolved
- **Node ID**: Global GitHub identifier starting with `I_` (required for mutations)

### Conservative approach to blocking relationships

**CRITICAL: Only create blocking relationships when truly necessary.**

A blocking relationship should **only** be created when:
- The blocked issue **literally cannot be worked on** without the blocker being resolved first
- There is a **technical dependency** that makes the work impossible to do
- The blocked issue would require **complete rework** if done before the blocker

**Do NOT create blocking relationships for:**
- "Nice to have done first" scenarios
- Preferred sequencing or best practices
- Quality improvements that should happen eventually
- Architectural preferences without technical barriers
- Issues that would be **easier** if another is done first (but still doable)

**Examples of what IS a true blocker:**
- ✅ API schema design blocks API implementation (can't implement without knowing the schema)
- ✅ Database migration blocks feature using new tables (tables must exist first)
- ✅ Authentication system blocks features requiring auth (no way to secure without it)

**Examples of what is NOT a true blocker:**
- ❌ Test coverage should be improved before refactoring (refactor can proceed, just riskier)
- ❌ File should be reorganized before adding mappings (can add to current structure)
- ❌ Architecture should be unified before adding features (features can work with either)
- ❌ Security assessment should happen before replacement (can research alternatives anytime)

**When in doubt, don't block.** Let teams decide their own sequencing rather than enforcing it through dependencies.

**Resolved blockers (IMPORTANT):**
- GitHub **automatically marks dependencies as "resolved"** when the blocking issue closes
- **DO NOT manually remove** dependencies when the blocking issue is closed
- Resolved blockers are **automatically lifted** - the blocked issue is no longer prevented from being worked on
- Keep the dependency relationship for **historical context** - it shows what was needed and when it was completed
- Only remove blocking relationships when they were added in error or are no longer valid while both issues are still open

**Common patterns:**
- **Design decision blocks implementation**: Only if implementation literally cannot proceed without the design
- **Dependencies between features**: Only if Feature B cannot function without Feature A's code/API
- **Bug fixes blocking releases**: Only if the bug makes the release non-functional

**Best practices:**
- Be conservative: only block when there's no way to proceed
- Add comments explaining the technical reason for the dependency
- Update issue bodies to reference blockers with rationale
- Use in conjunction with project management for visibility
- Don't create circular dependencies
- Keep dependencies to closed issues for historical tracking

## Examples

**Example 1: Simple blocking relationship**
```
User: "Make issue 310 block issue 307"
Assistant:
1. Gets node IDs for both issues
2. Executes addBlockedBy mutation
3. Verifies with query
4. Reports: "✅ Issue #310 is now blocking issue #307"
```

**Example 2: Query dependencies**
```
User: "What's blocking issue 307?"
Assistant:
1. Queries issue 307's blockedBy field
2. Reports: "Issue #307 is blocked by:
   - #310: Scope validation system doesn't accommodate legitimate temporal concepts"
```

**Example 3: Remove blocking**
```
User: "Issue 310 is resolved, unblock 307"
Assistant:
1. Executes removeBlockedBy mutation
2. Verifies removal
3. Reports: "✅ Issue #310 no longer blocks issue #307"
```

## Error handling

**Common issues:**
- **404 Not Found**: Issue number doesn't exist
- **Invalid node ID**: Check that IDs start with `I_` and are for the correct repository
- **Circular dependencies**: GitHub may prevent creating circular blocks
- **Permissions**: Requires write access to the repository

## Integration tips

**Works well with:**
- `git-issue-create` agent - Add dependencies when creating issues
- `git-issue-deliver` agent - Check for blockers before starting work
- Project management - Dependencies visible in GitHub Projects
- PR workflows - PRs linked to blocked issues show dependency status

**Enhances workflow when:**
- Breaking down large features into dependent tasks
- Managing release blockers
- Coordinating across teams
- Tracking technical debt resolution order