---
name: Work on Ticket
description: Fetches Jira ticket details, creates an appropriately named branch, and initiates the task planning workflow. Use when the user says "work on [TICKET_ID]" or similar phrases.
license: MIT
compatibility: opencode
---

# Work on Ticket

Streamlined workflow to start work on a Jira ticket by fetching ticket details, creating a branch, and initiating task planning.

## When to Use This Skill

Activate this skill when:

- The user says "work on AGP-123" or "start work on AGP-123"
- The user says "pick up AGP-123" or "begin AGP-123"
- The user mentions starting work on a specific Jira ticket ID
- Pattern: `work on [TICKET_ID]` or similar intent

## Workflow

### 1. Parse Ticket ID

Extract the Jira ticket ID from the user's message. Common patterns:

- `work on AGP-782`
- `start AGP-782`
- `pick up PROJ-123`

Ticket ID format: `[A-Z]+-[0-9]+` (e.g., AGP-782, AICC-123)

### 2. Fetch Jira Ticket Details

Use the MCP Zapier tool to fetch the ticket:

```typescript
mcp__zapier-frontend__jira_software_cloud_find_issue_by_key({
  instructions: "Get details for ticket [TICKET_ID]",
  key: "[TICKET_ID]",
  fields: "summary,description,issuetype,priority,status"
})
```

**Extract from response:**

- Summary (title)
- Description
- Issue type
- Status
- Any other relevant context

### 3. Generate Branch Name

Create a branch name using this format:

```
[TICKET_ID]-[kebab-case-summary]
```

**Branch Naming Rules:**

- Start with the ticket ID (e.g., `AGP-782-`)
- Convert summary to kebab-case (lowercase, dashes instead of spaces)
- Remove special characters
- Keep it concise (max 50 characters total)
- Use meaningful words from the summary

**Examples:**

- `AGP-782-migrate-existing-mcp-server`
- `AICC-123-fix-auth-token-expiry`
- `PROJ-456-add-user-settings-page`

**Implementation:**

```bash
# Convert summary to kebab-case
# Example: "Migrate existing MCP server" -> "migrate-existing-mcp-server"
```

### 4. Check Current Git State

Before creating a branch, check the current state:

```bash
# Check current branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain
```

**If uncommitted changes exist:**

- STOP and inform User
- Suggest: "You have uncommitted changes. Should I commit them first, stash them, or continue anyway?"
- Wait for User's decision

**If not on staging/main:**

- STOP and inform User
- Suggest: "You're currently on branch [CURRENT_BRANCH]. Should I switch to staging first?"
- Wait for User's decision

### 5. Create Branch

Once it's safe to proceed:

```bash
# Ensure we're on the latest staging
git checkout staging
git pull origin staging

# Create and checkout new branch
git checkout -b [TICKET_ID]-[kebab-case-summary]
```

Confirm to User: "Created and checked out branch: [BRANCH_NAME]"

### 6. Build Task Planning Prompt

Analyze the Jira ticket and create a comprehensive prompt for the `/eng:chore` command:

**Prompt should include:**

- The ticket summary
- Key details from the description
- Any acceptance criteria mentioned
- Relevant technical context

**Example prompt construction:**

```
Summary: [ticket.summary]

Description: [ticket.description]

Acceptance Criteria:
[extracted criteria if present]
```

### 7. Execute Task Planning

Run the `/eng:chore` slash command with the ticket number and constructed prompt:

```bash
/eng:chore [TICKET_ID] [CONSTRUCTED_PROMPT]
```

**Example:**

```bash
AGP-782 Migrate existing MCP server implementation to new architecture

Description: We need to refactor the MCP server to use the new modular architecture. This includes updating the tool registry, migrating existing tools, and ensuring backward compatibility.

Acceptance Criteria:
- All existing tools work with new architecture
- Tests pass
- No breaking changes to API
```

## Error Handling

**If ticket not found:**

- Inform User: "Couldn't find ticket [TICKET_ID] in Jira. Please check the ticket ID."
- STOP - don't proceed with branch creation

**If branch already exists:**

- Inform User: "Branch [BRANCH_NAME] already exists."
- Ask: "Should I check it out, create a new branch with a different name, or stop?"
- Wait for decision

**If git operations fail:**

- Show the error to User
- STOP - don't proceed to task planning

## Example Usage

### Example 1: Simple Ticket

**User:** "work on AGP-782"

**Claude:**

1. Fetches AGP-782 from Jira
2. Finds summary: "Migrate existing MCP server"
3. Checks git state (clean, on staging)
4. Creates branch: `AGP-782-migrate-existing-mcp-server`
5. Runs: `/eng:chore AGP-782 Migrate existing MCP server implementation...`

### Example 2: With Uncommitted Changes

**User:** "work on AICC-456"

**Claude:**

1. Fetches AICC-456 from Jira
2. Checks git state - finds uncommitted changes
3. **STOPS** and asks: "You have uncommitted changes. Should I commit them first, stash them, or continue anyway?"
4. Waits for User's decision

### Example 3: Ticket Not Found

**User:** "work on BAD-999"

**Claude:**

1. Tries to fetch BAD-999 from Jira
2. Ticket not found
3. Informs User: "Couldn't find ticket BAD-999 in Jira. Please check the ticket ID."
4. STOPS

## Coding Standards

**CRITICAL RULE - NESTED CONDITIONALS:**

- **NEVER EVER EVER USE NESTED CONDITIONALS** when working on tickets
- If you find yourself nesting if statements, STOP immediately
- Refactor using early returns, guard clauses, or extract functions
- This rule applies to all code written while working on any ticket
- Violation of this rule is FAILURE

**Why this matters:**

- Nested conditionals reduce readability and increase cognitive load
- They make code harder to test and maintain
- Early returns and guard clauses are always clearer

**Instead of:**

```typescript
if (condition1) {
  if (condition2) {
    // do something
  }
}
```

**Do this:**

```typescript
if (!condition1) return;
if (!condition2) return;
// do something
```

**CRITICAL RULE - NO UNNECESSARY INLINE COMMENTS:**

- **NEVER add simple, obvious inline comments** that just restate what the code does
- Code should be self-documenting through clear variable names, function names, and structure
- Only add comments when they explain **WHY** something is done, not **WHAT** is being done
- Remove unnecessary comments during refactoring
- This rule applies to all code written while working on any ticket
- Violation of this rule is FAILURE

**Bad comments (obvious, unnecessary):**

```typescript
// Set the user's name
user.name = "Alice";

// Loop through the items
for (const item of items) {
  // Process the item
  processItem(item);
}

// Return true if valid
return isValid;
```

**Good comments (explain WHY, add context):**

```typescript
// Cache user data for 5 minutes to reduce API calls
const cachedUser = await cache.get(userId, { ttl: 300 });

// Process items in batches to avoid memory issues with large datasets
for (const batch of chunkArray(items, 100)) {
  await processBatch(batch);
}

// Skip validation for admin users per security requirement SEC-123
if (user.isAdmin) return true;
```

**When comments ARE appropriate:**

- Explaining non-obvious business logic or requirements
- Documenting workarounds for external bugs (with issue links)
- Clarifying performance optimizations
- Noting security considerations
- Referencing ticket numbers or external documentation

**When to use NO comments:**

- If the code is self-explanatory
- If a better variable/function name would make it clear
- If the comment just repeats what the code obviously does

**CRITICAL RULE - VITEST TESTING:**

- **ALWAYS use the Vitest TDD Expert skill** when writing or working with Vitest tests
- Before writing any Vitest tests, activate the Vitest TDD Expert skill by invoking it with the Skill tool
- The Vitest TDD Expert skill enforces:
  - **Red-Green-Refactor TDD cycle** (test first, always)
  - **95%+ coverage requirements** with quality metrics
  - **FIRST principles** (Fast, Independent, Repeatable, Self-validating, Timely)
  - **Behavior-focused testing** (not implementation details)
  - **Comprehensive edge case coverage** and error path testing
  - **Anti-pattern avoidance** (no brittle tests, no excessive mocking)
- This ensures high-quality, maintainable test suites that provide confidence
- Violation of this rule means tests may be brittle, incomplete, or low quality

**When to activate Vitest TDD Expert:**

```typescript
// Before writing Vitest tests, invoke:
Skill({ skill: "vitest-tdd" })
```

## Important Notes

- **Always check git state** before creating branches
- **Never force-create branches** or overwrite existing branches
- **Never proceed** if there are uncommitted changes without User's approval
- **Keep branch names concise** - aim for clarity over completeness
- **Include ticket context** in the task planning prompt to give the planner maximum context
- **The `/eng:chore` command** will handle the detailed planning - this skill just sets up the environment

## Success Criteria

The skill is successful when:

1. ✅ Jira ticket is fetched successfully
2. ✅ Appropriate branch name is generated
3. ✅ Git state is verified (no uncommitted changes or user approved)
4. ✅ New branch is created and checked out
5. ✅ `/eng:chore` command is executed with ticket context
6. ✅ User is informed of each major step
