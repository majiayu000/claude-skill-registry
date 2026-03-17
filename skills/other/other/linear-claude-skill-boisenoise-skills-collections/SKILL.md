---
name: Linear
description: Managing Linear issues, projects, and teams. Use when working with Linear tasks, creating issues, updating status, querying projects, or managing team workflows.
allowed-tools:
  - mcp__linear
  - WebFetch(domain:linear.app)
  - Bash
---

# Linear

Tools and workflows for managing issues, projects, and teams in Linear.

---

## ⚠️ Tool Availability (READ FIRST)

**This skill supports multiple tool backends. Use whichever is available:**

1. **MCP Tools (mcp__linear)** - Use if available in your tool set
2. **Linear CLI (`linear` command)** - Always available via Bash
3. **Helper Scripts** - For complex operations

**If MCP tools are NOT available**, use the Linear CLI via Bash:

```bash
# View an issue
linear issues view SMI-123

# Create an issue
linear issues create --title "Issue title" --description "Description"

# Update issue status (get state IDs first)
linear issues update SMI-123 -s "STATE_ID"

# Add a comment
linear issues comment add SMI-123 -m "Comment text"

# List issues
linear issues list
```

**Do NOT report "MCP tools not available" as a blocker** - use CLI instead.

---

## 🔐 Security: Varlock Integration

**CRITICAL**: Never expose API keys in terminal output or Claude's context.

### Safe Commands (Always Use)

```bash
# Validate LINEAR_API_KEY is set (masked output)
varlock load 2>&1 | grep LINEAR

# Run commands with secrets injected
varlock run -- npx tsx scripts/query.ts "query { viewer { name } }"

# Check schema (safe - no values)
cat .env.schema | grep LINEAR
```

### Unsafe Commands (NEVER Use)

```bash
# ❌ NEVER - exposes key to Claude's context
linear config show
echo $LINEAR_API_KEY
printenv | grep LINEAR
cat .env
```

### Setup for New Projects

1. Create `.env.schema` with `@sensitive` annotation:
   ```bash
   # @type=string(startsWith=lin_api_) @required @sensitive
   LINEAR_API_KEY=
   ```

2. Add `LINEAR_API_KEY` to `.env` (never commit this file)

3. Configure MCP to use environment variable:
   ```json
   {
     "mcpServers": {
       "linear": {
         "env": { "LINEAR_API_KEY": "${LINEAR_API_KEY}" }
       }
     }
   }
   ```

4. Use `varlock load` to validate before operations

---

## Quick Start (First-Time Users)

### 1. Check Your Setup

Run the setup check to verify your configuration:

```bash
npx tsx ~/.claude/skills/linear/scripts/setup.ts
```

This will check:
- LINEAR_API_KEY is set and valid
- @linear/sdk is installed
- Linear CLI availability (optional)
- MCP configuration (optional)

### 2. Get API Key (If Needed)

If setup reports a missing API key:

1. Open [Linear](https://linear.app) in your browser
2. Go to **Settings** (gear icon) -> **Security & access** -> **Personal API keys**
3. Click **Create key** and copy the key (starts with `lin_api_`)
4. Add to your environment:

```bash
# Option A: Add to shell profile (~/.zshrc or ~/.bashrc)
export LINEAR_API_KEY="lin_api_your_key_here"

# Option B: Add to Claude Code environment
echo 'LINEAR_API_KEY=lin_api_your_key_here' >> ~/.claude/.env

# Then reload your shell or restart Claude Code
```

### 3. Test Connection

Verify everything works:

```bash
npx tsx ~/.claude/skills/linear/scripts/query.ts "query { viewer { name } }"
```

You should see your name from Linear.

### 4. Common Operations

Use the high-level operations script for simple commands:

```bash
# Create an issue in a project
npx tsx scripts/linear-ops.ts create-issue "My Project" "Fix login bug" "Users cannot log in" --priority 2

# Create a sub-issue under an existing issue
npx tsx scripts/linear-ops.ts create-sub-issue ENG-100 "Add unit tests" "Unit tests for this feature" --priority 2

# Set parent-child relationships for existing issues
npx tsx scripts/linear-ops.ts set-parent ENG-100 ENG-101 ENG-102

# List sub-issues of a parent
npx tsx scripts/linear-ops.ts list-sub-issues ENG-100

# Create an initiative
npx tsx scripts/linear-ops.ts create-initiative "Q1 Goals" "Key initiatives for Q1"

# Create a project linked to an initiative
npx tsx scripts/linear-ops.ts create-project "Phase 1" "Q1 Goals"

# Update project state (backlog, planned, in-progress, paused, completed, canceled)
npx tsx scripts/linear-ops.ts project-status "Phase 1" in-progress
npx tsx scripts/linear-ops.ts project-status "Phase 1" completed

# Link/unlink projects to initiatives
npx tsx scripts/linear-ops.ts link-initiative "Phase 1" "Q1 Goals"
npx tsx scripts/linear-ops.ts unlink-initiative "Phase 1" "Q1 Goals"

# Update issue status (PREFERRED over MCP)
node scripts/linear-helpers.mjs update-status Done 123 124 125

# List initiatives
npx tsx scripts/linear-ops.ts list-initiatives

# Show current user
npx tsx scripts/linear-ops.ts whoami
```

### 5. Getting Help

```bash
# Show all available commands
npx tsx scripts/linear-ops.ts help

# Re-run setup check anytime
npx tsx scripts/setup.ts
```

---

## Project Planning Workflow

### Create Issues in the Correct Project from the Start

**Best Practice**: When planning a new phase or initiative, create the project and its issues together in a single planning session. Avoid creating issues in a catch-all project and moving them later.

#### Recommended Workflow

1. **Create the project first**:
   ```bash
   npx tsx scripts/linear-ops.ts create-project "Phase X: Feature Name" "Skillsmith"
   ```

2. **Set project state to Planned**:
   ```bash
   npx tsx scripts/linear-ops.ts project-status "Phase X: Feature Name" planned
   ```

3. **Create issues directly in the project**:
   ```bash
   npx tsx scripts/linear-ops.ts create-issue "Phase X: Feature Name" "Parent task" "Description"
   npx tsx scripts/linear-ops.ts create-sub-issue SMI-XXX "Sub-task 1" "Description"
   npx tsx scripts/linear-ops.ts create-sub-issue SMI-XXX "Sub-task 2" "Description"
   ```

4. **Update project state when work begins**:
   ```bash
   npx tsx scripts/linear-ops.ts project-status "Phase X: Feature Name" in-progress
   ```

#### Why This Matters

- **Traceability**: Issues are linked to their project from creation
- **Metrics**: Project progress tracking is accurate from day one
- **Workflow**: No time wasted moving issues between projects
- **Organization**: Linear views and filters work correctly

#### Anti-Pattern to Avoid

❌ Creating issues in a "holding" project and moving them later:
```bash
# Don't do this
create-issue "Phase 6A" "New feature"  # Wrong project
# Later: manually move to Phase X      # Extra work
```

---

## Project Management Commands

### project-status

Update a project's state in Linear. Accepts user-friendly terminology that maps to Linear's API.

```bash
npx tsx scripts/linear-ops.ts project-status <project-name> <state>
```

**Valid States:**
| Input | Description | API Value |
|-------|-------------|-----------|
| `backlog` | Not yet started | backlog |
| `planned` | Scheduled for future | planned |
| `in-progress` | Currently active | started |
| `paused` | Temporarily on hold | paused |
| `completed` | Successfully finished | completed |
| `canceled` | Will not be done | canceled |

**Examples:**
```bash
# Start working on a project
npx tsx scripts/linear-ops.ts project-status "Phase 8: MCP Decision Engine" in-progress

# Mark project complete
npx tsx scripts/linear-ops.ts project-status "Phase 8" completed

# Partial name matching works
npx tsx scripts/linear-ops.ts project-status "Phase 8" paused
```

### link-initiative

Link an existing project to an initiative.

```bash
npx tsx scripts/linear-ops.ts link-initiative <project-name> <initiative-name>
```

**Examples:**
```bash
# Link Phase 8 to Skillsmith initiative
npx tsx scripts/linear-ops.ts link-initiative "Phase 8: MCP Decision Engine" "Skillsmith"

# Partial matching works
npx tsx scripts/linear-ops.ts link-initiative "Phase 8" "Skillsmith"
```

### unlink-initiative

Remove a project from an initiative.

```bash
npx tsx scripts/linear-ops.ts unlink-initiative <project-name> <initiative-name>
```

**Examples:**
```bash
# Remove incorrect link
npx tsx scripts/linear-ops.ts unlink-initiative "Phase 8" "Linear Skill"

# Clean up test links
npx tsx scripts/linear-ops.ts unlink-initiative "Test Project" "Q1 Goals"
```

**Error Handling:**
- Returns error if project is not linked to the specified initiative
- Returns error if project or initiative not found

### Complete Project Lifecycle Example

```bash
# 1. Create project linked to initiative
npx tsx scripts/linear-ops.ts create-project "Phase 11: New Feature" "Skillsmith"

# 2. Set state to planned
npx tsx scripts/linear-ops.ts project-status "Phase 11" planned

# 3. Create issues in the project
npx tsx scripts/linear-ops.ts create-issue "Phase 11" "Parent task" "Description"
npx tsx scripts/linear-ops.ts create-sub-issue SMI-XXX "Sub-task 1" "Details"

# 4. Start work - update to in-progress
npx tsx scripts/linear-ops.ts project-status "Phase 11" in-progress

# 5. Mark issues done
npx tsx scripts/linear-ops.ts status Done SMI-XXX SMI-YYY

# 6. Complete project
npx tsx scripts/linear-ops.ts project-status "Phase 11" completed

# 7. (Optional) Link to additional initiative
npx tsx scripts/linear-ops.ts link-initiative "Phase 11" "Q2 Goals"
```

---

## Tool Selection

Choose the right tool for the task:

1. **MCP tools (Official Server)** - **PREFERRED** for most operations when using `mcp.linear.app`
2. **Helper Scripts / GraphQL API** - Use for bulk operations or when MCP unavailable
3. **SDK scripts** - Use for complex operations (loops, bulk updates, conditional logic, data transformations)

### MCP Server Selection (CRITICAL)

**Always use the official Linear MCP server** at `mcp.linear.app`. Configure in your MCP settings:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.linear.app/sse"],
      "env": { "LINEAR_API_KEY": "your_api_key" }
    }
  }
}
```

> **WARNING**: Do NOT use deprecated community servers (`linear-mcp-server` npm package, `jerhadf/linear-mcp-server`). They have critical bugs including a schema mismatch where `status` parameter fails because it's passed directly as `stateId` (requires UUID, not name).

### MCP Reliability Matrix (Official Server)

The **official Linear MCP server** (`mcp.linear.app`) is significantly more reliable than community alternatives:

| Operation | MCP Tool | Reliability | Notes |
|-----------|----------|-------------|-------|
| Create issue | `create_issue` | ✅ High | Full support |
| **Update issue status** | `update_issue` | ✅ **Works with names!** | Use `state: "Done"` directly |
| List issues | `list_issues` | ✅ High | Supports filters |
| Search issues | `list_issues` with `query` | ✅ High | Use query parameter |
| Get user issues | `list_issues` with `assignee: "me"` | ✅ High | Reliable |
| Add comment | `create_comment` | ✅ High | Works with issue IDs |

**Key Improvement**: The official server accepts human-readable state names (e.g., `state: "Done"`, `state: "In Progress"`) and resolves them to UUIDs internally. No need for manual UUID lookups!

### Quick Status Update

**With the official MCP server**, you can now update status directly using human-readable names:

```
# Via MCP (official server) - NOW WORKS!
update_issue with id="issue-uuid", state="Done"
update_issue with id="issue-uuid", state="In Progress"
```

**Alternative: API wrapper** (for bulk operations or when MCP unavailable):

```bash
# Update single issue (use issue identifier like PROJ-123)
node ~/.claude/skills/linear/scripts/linear-api.mjs update-status --issue <TEAM>-123 --status Done

# Available states: Backlog, Todo, In Progress, In Review, Done, Canceled
```

### Linear API Wrapper (scripts/linear-api.mjs)

A complete API wrapper with proper JSON escaping and error handling:

```bash
# Create issue (replace <TEAM> with your team key, e.g., ENG, PROJ)
node ~/.claude/skills/linear/scripts/linear-api.mjs create-issue \
  --team <TEAM> --title "New feature" --description "Details here" --priority 2

# Update status (replace <TEAM>-123 with your issue identifier)
node ~/.claude/skills/linear/scripts/linear-api.mjs update-status \
  --issue <TEAM>-123 --status done

# Add comment
node ~/.claude/skills/linear/scripts/linear-api.mjs add-comment \
  --issue <TEAM>-123 --body "Fixed in PR #25"

# Add project update
node ~/.claude/skills/linear/scripts/linear-api.mjs add-project-update \
  --project <PROJECT_UUID> --body "## Status Update\n\nProgress details..." --health onTrack

# List issues
node ~/.claude/skills/linear/scripts/linear-api.mjs list-issues \
  --team <TEAM> --status "In Progress" --limit 20

# List labels
node ~/.claude/skills/linear/scripts/linear-api.mjs list-labels --team <TEAM>

# Help
node ~/.claude/skills/linear/scripts/linear-api.mjs help
```

**Benefits over MCP:**
- Proper JSON escaping (no shell parsing issues)
- Reliable status updates (uses correct GraphQL types)
- Batch-friendly for scripting
- Can be imported as ES module for programmatic use

**Why not MCP?** The `linear_update_issue` MCP tool frequently fails with schema validation errors and timeouts. The helper script uses direct GraphQL which is 100% reliable.

### Quick Comment by Issue Number

Add comments without needing to look up UUIDs:

```bash
# Simple comment (use the issue number, e.g., 123 for PROJ-123)
node scripts/linear-helpers.mjs add-comment 123 "Fixed in PR #25"

# Multi-line comment (use quotes)
node scripts/linear-helpers.mjs add-comment 123 "## Resolved

Implementation complete. All tests passing."
```

**Pattern**: Use MCP for issue creation, helper scripts for status updates and comments, and direct GraphQL for searches and complex queries.

### Historical: Why Community MCP Servers Failed

> **Note**: These issues are **resolved** with the official Linear MCP server at `mcp.linear.app`. This section is preserved for reference when troubleshooting deprecated community server configurations.

#### Issue 1: Status Update Schema Mismatch (FIXED in Official Server)

The deprecated `linear-mcp-server` (npm) had a critical bug:

| Community Server | Official Server |
|------------------|-----------------|
| `status: "Done"` → passed as `stateId` (UUID required) → ❌ Fails | `state: "Done"` → resolved internally → ✅ Works |

**The official server correctly resolves state names to UUIDs internally.**

#### Issue 2: SSE Connection Timeouts

Both servers can experience SSE connection drops after extended idle periods. The official server has improved keep-alive handling, but for very long operations, helper scripts remain a reliable fallback.

**Best Practice**: Use the official MCP server for most operations. Fall back to helper scripts for bulk operations or timeout-prone scenarios.

## Critical Requirements

### ⚠️ MANDATORY: Issues → Projects → Initiatives

**Every issue MUST be attached to a project. Every project MUST be linked to an initiative.**

Orphaned issues and projects are invisible in roadmap views and break tracking.

| Entity | Must Link To | Consequence if Missing |
|--------|--------------|------------------------|
| Issue | Project | Not visible in project board |
| Project | Initiative | Not visible in initiative roadmap |

**Anti-Pattern (NEVER DO):**
```bash
# ❌ Creating orphaned issues
mcp__linear__linear_create_issue with title="My task"
# Issue exists but is not part of any project!
```

**Correct Pattern (ALWAYS DO):**
```bash
# ✅ Create issue AND add to project in same workflow
mcp__linear__linear_create_issue with title="My task" ...
node scripts/linear-helpers.mjs add-issues-to-project <projectId> <issueNumber>

# ✅ Create project AND link to initiative
linear projects create --name "Phase N: Name"
node scripts/linear-helpers.mjs link-project <projectId>
```

### Helper Script: Update Issue Status

**⚡ PRIMARY METHOD** - Always use the helper script for status updates (API-first for reliability):

```bash
# Update multiple issues to Done (use issue numbers without prefix)
node scripts/linear-helpers.mjs update-status Done 101 102 103

# Available states: Backlog, Todo, In Progress, In Review, Done, Canceled
```

**Never use MCP's `linear_update_issue`** - it fails ~50% of the time with schema validation errors. The helper script uses direct GraphQL API calls which are 100% reliable.

---

## Conventions

### Issue Status

When creating issues, set the appropriate status based on assignment:

- **Assigned to me** (`assignee: "me"`): Set `state: "Todo"`
- **Unassigned**: Set `state: "Backlog"`

Example:
```typescript
// Issue for myself (replace "TEAM" with your team key)
await linear.create_issue({
  team: "TEAM",
  title: "Fix authentication bug",
  assignee: "me",
  state: "Todo"
})

// Unassigned issue
await linear.create_issue({
  team: "TEAM",
  title: "Research API performance",
  state: "Backlog"
})
```

### Querying Issues

Use `assignee: "me"` to filter issues assigned to the authenticated user:

```typescript
// My issues
await linear.list_issues({ assignee: "me" })

// Team backlog (replace "TEAM" with your team key)
await linear.list_issues({ team: "TEAM", state: "Backlog" })
```

### Labels

This skill uses a **domain-based label taxonomy** for consistent categorization. See [docs/labels.md](docs/labels.md) for the complete guide.

**Key rules:**
- Always apply exactly ONE Type label: `feature`, `bug`, `refactor`, `chore`, or `spike`
- Apply 1-2 Domain labels for agent routing: `security`, `backend`, `frontend`, etc.
- Add Scope labels only when applicable: `blocked`, `breaking-change`, `tech-debt`, etc.

**Taxonomy commands:**
```bash
# Show full taxonomy
npx tsx scripts/linear-ops.ts labels taxonomy

# Validate labels before creating issues
npx tsx scripts/linear-ops.ts labels validate "feature,security,breaking-change"

# Suggest labels based on issue title
npx tsx scripts/linear-ops.ts labels suggest "Fix XSS vulnerability in login form"

# Show agent recommendations for labels
npx tsx scripts/linear-ops.ts labels agents "security,performance"
```

You can use label names directly in `create_issue` and `update_issue` - no need to look up IDs:

```typescript
await linear.create_issue({
  team: "TEAM",
  title: "Update documentation",
  labels: ["documentation", "chore"]  // Use taxonomy labels
})
```

## SDK Automation Scripts

**Use only when MCP tools are insufficient.** For complex operations involving loops, mapping, or bulk updates, write TypeScript scripts using `@linear/sdk`. See `sdk.md` for:

- Complete script patterns and templates
- Common automation examples (bulk updates, filtering, reporting)
- Tool selection criteria

Scripts provide full type hints and are easier to debug than raw GraphQL for multi-step operations.

## GraphQL API

**Fallback only.** Use when operations aren't supported by MCP or SDK. See `api.md` for documentation on using the Linear GraphQL API directly.

### Timeout Handling Patterns

When operations take longer than expected, use these patterns to maintain reliability:

**1. Progress Notifications**
For bulk operations, notify the user of progress:

```javascript
const issues = ['PROJ-101', 'PROJ-102', 'PROJ-103'];
for (let i = 0; i < issues.length; i++) {
  console.log(`Processing ${i + 1}/${issues.length}: ${issues[i]}`);
  // ... operation
}
```

**2. Chunked Batch Operations**
Break large batches into smaller chunks to avoid timeouts:

```javascript
const BATCH_SIZE = 10;
const DELAY_MS = 150; // Avoid rate limiting

for (let i = 0; i < issues.length; i += BATCH_SIZE) {
  const batch = issues.slice(i, i + BATCH_SIZE);
  console.log(`Batch ${Math.floor(i / BATCH_SIZE) + 1}: Processing ${batch.length} issues`);

  for (const issue of batch) {
    await processIssue(issue);
    await new Promise(r => setTimeout(r, DELAY_MS));
  }
}
```

**3. Fallback on Timeout**
Detect timeouts and fall back to GraphQL:

```javascript
try {
  // Try MCP first (faster when it works)
  await mcp__linear__linear_search_issues({ query: "keyword" });
} catch (error) {
  if (error.message.includes('timeout') || error.message.includes('ETIMEDOUT')) {
    console.log('MCP timed out, falling back to GraphQL...');
    // Use GraphQL workaround (see below)
  }
}
```

**4. Bulk Sync Script**
Use `scripts/sync.ts` for reliable bulk state updates:

```bash
# Update multiple issues to Done state (replace PROJ with your team prefix)
LINEAR_API_KEY=lin_api_xxx npx tsx scripts/sync.ts --issues PROJ-101,PROJ-102,PROJ-103 --state Done

# Preview changes without applying
LINEAR_API_KEY=lin_api_xxx npx tsx scripts/sync.ts --issues PROJ-101,PROJ-102 --state Done --dry-run

# Add comment with state change
LINEAR_API_KEY=lin_api_xxx npx tsx scripts/sync.ts --issues PROJ-101 --state Done --comment "Completed in PR #42"
```

### MCP Timeout Workarounds

When MCP times out or fails, use these direct GraphQL patterns:

#### ⚠️ Shell Script Compatibility

**IMPORTANT**: When writing inline Node.js scripts in bash, avoid JavaScript features that confuse shell parsing:

| Feature | Problem | Solution |
|---------|---------|----------|
| Optional chaining `?.` | Shell sees `?` as glob | Use explicit null checks |
| Nullish coalescing `??` | Double `?` confuses parser | Use ternary `? :` |
| Heredocs with `${}` | Shell interpolation | Use `<< 'EOF'` (quoted) |

**Anti-Pattern (breaks in bash):**
```javascript
// ❌ Optional chaining breaks shell parsing
const name = project.status?.name;
```

**Correct Pattern:**
```javascript
// ✅ Explicit null check works everywhere
const name = project.status ? project.status.name : 'No status';
```

**Heredoc Pattern:**
```bash
# ✅ Use quoted EOF to prevent shell interpolation
node --input-type=module << 'ENDSCRIPT'
const value = obj.prop ? obj.prop.nested : 'default';
ENDSCRIPT
```

#### Search Issues (when MCP times out)

```javascript
// Inline GraphQL via node --experimental-fetch
node --experimental-fetch -e "
async function searchIssues() {
  const query = \`
    query {
      issues(filter: {
        team: { key: { eq: \"TEAM\" } }
        state: { type: { nin: [\"completed\", \"canceled\"] } }
      }, first: 25) {
        nodes {
          id identifier title state { name } priority
        }
      }
    }
  \`;

  const res = await fetch('https://api.linear.app/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': process.env.LINEAR_API_KEY
    },
    body: JSON.stringify({ query })
  });

  const data = await res.json();
  data.data.issues.nodes.forEach(i => {
    console.log(\`\${i.identifier}: \${i.title} [\${i.state.name}]\`);
  });
}
searchIssues();
"
```

#### Update Issue Status (when MCP is unreliable)

```javascript
// First get the workflow state ID for "Done"
const stateQuery = \`
  query {
    workflowStates(filter: { team: { key: { eq: \"TEAM\" } }, name: { eq: \"Done\" } }) {
      nodes { id name }
    }
  }
\`;

// Then update the issue
const mutation = \`
  mutation {
    issueUpdate(id: "\${issueUuid}", input: { stateId: "\${doneStateId}" }) {
      success
      issue { identifier state { name } }
    }
  }
\`;
```

#### Add Comment (MCP fails with UUIDs)

```javascript
// Get issue UUID from identifier
const issueQuery = \`
  query {
    issues(filter: { number: { in: [123, 124, 125] } }) {
      nodes { id identifier }
    }
  }
\`;

// Add comment using UUID
const mutation = \`
  mutation {
    commentCreate(input: {
      issueId: "\${issueUuid}",
      body: "Implementation complete. See PR #42."
    }) { success }
  }
\`;
```

**Pro Tip**: Store frequently-used IDs (team UUID, common state UUIDs) in your project's CLAUDE.md to avoid repeated lookups.

### Ad-Hoc Queries

Use `scripts/query.ts` to execute GraphQL queries:

```bash
LINEAR_API_KEY=lin_api_xxx node scripts/query.ts "query { viewer { id name } }"
```

If `LINEAR_API_KEY` is not provided to the Claude process, inform the user that GraphQL queries cannot be executed without an API key.

## Projects & Initiatives

### MANDATORY: Project Content & Updates

**Every project operation MUST include these steps. Never skip them.**

When **creating** a project:
1. ✅ Set `content` (full markdown for main panel)
2. ✅ Set `description` (255 char summary for lists)
3. ✅ Link to parent initiative
4. ✅ Add resource links (docs, repos)
5. ✅ Create initial project update with scope

When **updating** project status:
1. ✅ Update `statusId` to new status
2. ✅ Create project update documenting the change
3. ✅ Include progress metrics (X/Y issues complete)

When **completing** work:
1. ✅ Update issue statuses to Done
2. ✅ Update project status to match
3. ✅ Create final project update with summary

**Example: Mandatory Project Update**

```javascript
// ALWAYS create an update when project status changes
node --experimental-fetch -e "
const PROJECT_ID = '<uuid>';

const update = \`## Status: In Progress 🚀

**Date:** $(date '+%Y-%m-%d')

### Completed
- ✅ Task 1 done
- ✅ Task 2 done

### In Progress
- 🔄 Task 3 in progress

### Up Next
- 📝 Task 4 pending
\`;

const mutation = \`mutation {
  projectUpdateCreate(input: {
    projectId: \\\"\${PROJECT_ID}\\\",
    body: \${JSON.stringify(update)},
    health: onTrack
  }) { success projectUpdate { url } }
}\`;

fetch('https://api.linear.app/graphql', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Authorization': process.env.LINEAR_API_KEY },
  body: JSON.stringify({ query: mutation })
}).then(r => r.json()).then(d => console.log('Update created:', d.data?.projectUpdateCreate?.projectUpdate?.url));
"
```

---

### Content vs Description (CRITICAL)

Linear has **two text fields** - using the wrong one causes blank displays:

| Field | Limit | Shows In | Use For |
|-------|-------|----------|---------|
| `description` | 255 chars | List views, tooltips | Short summary |
| `content` | Unlimited | **Main detail panel** | Full markdown documentation |

**Always set BOTH when creating/updating projects:**

```graphql
# Content is what users see in the main panel!
mutation {
  projectUpdate(id: "<uuid>", input: {
    content: "# Project Title\n\nFull markdown description...",
    description: "Short 255 char summary for list views"
  }) { success }
}
```

### Discovery Before Creation (MANDATORY)

**ALWAYS check Linear before creating ANY project or issue.** Skipping this step causes duplicate projects and wasted effort.

```bash
# Check for existing projects
linear projects list | grep -i "phase\|<feature-name>"

# Check for existing issues (MCP may timeout - use CLI as fallback)
linear issues list --filter "title:Phase N"
# Or: mcp__linear__linear_search_issues with query="Phase N feature"
```

**Checklist before ANY create operation:**

| Check | Command | Action if Found |
|-------|---------|-----------------|
| Project exists? | `linear projects list \| grep -i "name"` | Use existing UUID, skip creation |
| Issues exist? | `linear issues list --filter "title:keyword"` | Review existing, update if needed |
| Initiative linked? | Check project in Linear UI | Skip link-project step |

**NEVER skip discovery. Duplicate projects waste time and create confusion.**

---

### Codebase Verification Before Work (MANDATORY)

**ALWAYS verify codebase state before accepting Linear issue scope at face value.**

Issue descriptions may be **outdated** or **speculative** — written before code exploration. This is especially common when:
- Issues were created during planning, not after code review
- The codebase evolved since the issue was created
- API endpoints or features were implemented but not documented in Linear

**Key Lesson**: Issues describing "missing" APIs or features may already be implemented.

```bash
# Before starting any API/feature implementation issue:

# 1. Search for existing implementations
grep -r "apiEndpoint\|functionName" src/

# 2. Check if files already exist
ls src/pages/api/admin/members/  # If issue says "implement members API"

# 3. Read existing code
cat src/pages/api/admin/members/index.ts  # May already be complete!

# 4. Run tests to see what's actually failing
npx playwright test tests/e2e/journeys/admin/
```

**Checklist before accepting issue scope:**

| Check | Method | If Found |
|-------|--------|----------|
| API exists? | `ls src/pages/api/**/*.ts` | Update issue scope to "verify/test" |
| Feature implemented? | `grep -r "featureName" src/` | Mark implementation subtasks as done |
| Tests passing? | Run test suite | Focus on fixing failures, not reimplementing |
| Only tests skipped? | Check for `test.skip` | Real work is un-skipping + fixing assertions |

**Example: Scope Discovery**

Issue says: "Implement /api/admin/members CRUD endpoints"

**BEFORE starting:**
```bash
# Check if files exist
ls src/pages/api/admin/members/
# Output: index.ts  [id].ts  ← Files exist!

# Read the implementation
cat src/pages/api/admin/members/index.ts | head -50
# Output: Full implementation with GET, POST, auth checks

# Check why tests fail
grep -r "test.describe.skip" tests/e2e/journeys/admin/
# Output: member-management.spec.ts uses test.describe.skip
```

**CORRECTED scope**: "Un-skip E2E tests and fix any assertion failures" (not "implement API")

**Update Linear immediately when scope changes:**
```bash
node scripts/linear-helpers.mjs add-comment 123 "## Scope Update

**Discovery:** API endpoints are ALREADY COMPLETE!

### Actual Remaining Work
1. Un-skip journey tests
2. Fix any test assertion failures
3. Verify tests pass"
```

**NEVER assume issue descriptions are accurate. Verify codebase state first.**

---

## Sub-Issue Management (Parent-Child Relationships)

Linear supports hierarchical issue organization through parent-child relationships. Sub-issues (children) appear nested under their parent issue in the UI and inherit certain properties.

### When to Use Sub-Issues

| Scenario | Use Sub-Issues | Example |
|----------|----------------|---------|
| Feature breakdown | ✅ Yes | ENG-100 "Auth System" → ENG-101 "TDD tests", ENG-102 "E2E tests" |
| Related but independent | ❌ No | Two bugs in different areas (use labels instead) |
| Sequential phases | ✅ Yes | ENG-200 "Phase 1" → ENG-201 "Setup", ENG-202 "Implementation" |
| Tracking subtasks | ✅ Yes | Break down a large issue into trackable pieces |

### Commands

```bash
# Create a sub-issue (child) under a parent issue
# Inherits team and project from parent automatically
npx tsx scripts/linear-ops.ts create-sub-issue <parent-issue> <title> [description] [--priority 1-4] [--labels label1,label2]

# Set existing issues as children of a parent
npx tsx scripts/linear-ops.ts set-parent <parent-issue> <child-issues...>

# List all sub-issues of a parent
npx tsx scripts/linear-ops.ts list-sub-issues <parent-issue>
```

### Examples

```bash
# Create a sub-issue for unit tests under a parent feature issue
npx tsx scripts/linear-ops.ts create-sub-issue ENG-100 "Add unit tests" "Unit tests for new feature" --priority 2 --labels testing

# Link existing issues as children of a parent
npx tsx scripts/linear-ops.ts set-parent ENG-100 ENG-101 ENG-102

# List all sub-issues of a parent
npx tsx scripts/linear-ops.ts list-sub-issues ENG-100
```

### Notes

- **Inheritance**: Sub-issues automatically inherit the team from the parent
- **Project linking**: If the parent is in a project, sub-issues can also be added
- **Status independence**: Each issue maintains its own status (completing a sub-issue doesn't auto-complete the parent)
- **UI display**: Sub-issues appear indented under their parent in list views

---

### Linking Projects to Initiatives

**Use `initiativeToProjectCreate` to link an existing project to an initiative:**

```graphql
mutation {
  initiativeToProjectCreate(input: {
    initiativeId: "<initiative-uuid>",
    projectId: "<project-uuid>"
  }) {
    success
    initiativeToProject { id }
  }
}
```

**Example using query.ts:**

```bash
npx tsx ~/.claude/skills/linear/scripts/query.ts 'mutation {
  initiativeToProjectCreate(input: {
    initiativeId: "<initiative-uuid>",
    projectId: "<project-uuid>"
  }) {
    success
  }
}'
```

**Note:** This is different from setting `initiativeId` at project creation time. Use this mutation when:
- A project was created without an initiative link
- You need to add a project to an additional initiative
- Reorganizing projects between initiatives

---

### New Phase Project Pattern

**Step 0: Run Discovery Checks (see above)**

When creating a new phase, follow this complete workflow:

```bash
# 0. DISCOVERY - Check for existing project/issues first!
linear projects list | grep -i "phase N"

# 1. Create project via CLI (ONLY if Step 0 found nothing)
linear projects create --name "Phase N: Name" --description "Short summary"

# 2. Link to initiative (use initiativeToProjectCreate mutation - see above)
npx tsx scripts/query.ts 'mutation { initiativeToProjectCreate(input: { initiativeId: "<uuid>", projectId: "<uuid>" }) { success } }'

# 3. Set content (main UI panel)
# Use GraphQL to set full markdown content

# 4. Add resource link to implementation doc
# Use entityExternalLinkCreate mutation

# 5. Create milestone for Definition of Done
# Use projectMilestoneCreate mutation

# 6. Create issues via MCP (check for existing first!)
# 7. Add issues to project
```

---

## ⚠️ MANDATORY: Project Creation Checklist

> **CRITICAL**: Every script that creates projects MUST follow this checklist.
> Skipping steps causes recurring issues with orphaned projects and missing links.

### Required Steps

| # | Step | How | Verify |
|---|------|-----|--------|
| 1 | **Link to initiative** | `initiativeToProjectCreate` mutation | Check initiative.projects |
| 2 | **Set description** | `description` field (255 char limit) | View in sidebar |
| 3 | **Set content** | `content` field via `projectUpdate` | View main panel |
| 4 | **Add resource links** | `entityExternalLinkCreate` mutation | Check Resources section |
| 5 | **Create milestones** | `projectMilestoneCreate` mutation | Check Milestones tab |
| 6 | **Ensure labels exist** | Use `lib/labels.ts` utilities | Query labels before/after |
| 7 | **Create issues with labels** | Include `labelIds` in `createIssue` | View issue labels |
| 8 | **Verify issue count** | Compare expected vs actual | Log counts |
| 9 | **Run verification** | Use `lib/verify.ts` | Check output |
| 10 | **Report failures** | Log all errors, don't fail silently | Review logs |

### Using Shared Utilities

**Always use the lib/ utilities** to avoid common mistakes:

```typescript
import {
  linkProjectToInitiative,
  ensureLabelsExist,
  verifyProjectCreation,
  createProject,
  createProjectWithDefaults,
  DEFAULT_INITIATIVE_ID
} from './lib'

// Option 1: Full template with explicit initiative
const result = await createProject(teamId, {
  name: 'My Project Phase X: Name',
  shortDescription: 'Short 255 char description',
  content: '# Full markdown content...',
  state: 'planned',
  initiative: '<your-initiative-uuid>',
  issues: [
    { title: 'Issue', description: 'Desc', labels: ['label1'] }
  ]
})

// Option 2: Use environment variable for initiative
// Requires: LINEAR_DEFAULT_INITIATIVE_ID=<uuid>
const result2 = await createProjectWithDefaults({
  name: 'My Project Phase X: Name',
  shortDescription: 'Short description',
  content: '# Full content...',
  state: 'planned',
  issues: []
})

// Option 3: Manual with utilities
const linkResult = await linkProjectToInitiative(projectId, initiativeId)
const labelResult = await ensureLabelsExist(teamId, ['label1', 'label2'])
const verification = await verifyProjectCreation('Phase X', expectedCount, undefined, initiativeId)
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LINEAR_API_KEY` | Yes | Your Linear API key |
| `LINEAR_DEFAULT_INITIATIVE_ID` | No | Default initiative for `createProjectWithDefaults()` |

### Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Using `initiativeIds` on `projectUpdate` | Silent failure | Use `initiativeToProjectCreate` mutation |
| Long description | Truncated in UI | Use `content` for full text, `description` for summary |
| Case-sensitive label lookup | Labels not applied | Use case-insensitive map (`name.toLowerCase()`) |
| Silent failures | Missing issues/labels | Always check result, log errors |
| No post-verification | Issues discovered later | Run `lib/verify.ts` after creation |

### Resource Links

Add clickable links to projects/initiatives (shows in Resources section):

```graphql
mutation {
  entityExternalLinkCreate(input: {
    url: "https://github.com/org/repo/blob/main/docs/implementation/phase-N.md",
    label: "Implementation Doc",
    projectId: "<project-uuid>"
  }) { success }
}
```

**Standard resource links for phases:**
- `Implementation Doc` → docs/implementation/phase-N-*.md
- `Production Site` → deployment URL (for initiative)
- `Repository` → GitHub repo link (for initiative)

### Project Milestones (Definition of Done)

Track completion criteria with milestones:

```graphql
mutation {
  projectMilestoneCreate(input: {
    projectId: "<uuid>",
    name: "DoD: Testing",
    description: "Unit tests, E2E tests, 100% coverage"
  }) { success }
}
```

**Standard DoD milestones:**
- `DoD: Core Feature` - Main functionality complete
- `DoD: Testing` - All tests pass, coverage met
- `DoD: Security` - Security requirements verified
- `DoD: Accessibility` - A11y requirements met

### Project Status (IMPORTANT)

**Project status is NOT auto-updated when issues move.** You must explicitly update project status.

#### Project Status vs Issue Status

| Concept | Applies To | Field | Auto-Updates? |
|---------|------------|-------|---------------|
| **Issue Status** | Individual issues | `stateId` | Yes (via workflow) |
| **Project Status** | Entire project | `statusId` | ❌ No - manual only |

#### Status Types and UUIDs

Query your workspace's status UUIDs (workspace-specific):

```graphql
query { projectStatuses { nodes { id name type } } }
```

**Standard Status Types:**

| Status | Type | When to Use |
|--------|------|-------------|
| `Backlog` | `backlog` | Project created but not started |
| `Planned` | `planned` | Project scheduled, issues created |
| `In Progress` | `started` | **Issues actively being worked** |
| `Completed` | `completed` | All issues done |
| `Canceled` | `canceled` | Project abandoned |

#### When to Update Project Status

Update project status at these transition points:

| Trigger | New Status | Check |
|---------|------------|-------|
| First issue moves to "In Progress" | `In Progress` | Any issue has `started` state |
| All issues complete | `Completed` | No issues in backlog/progress |
| Work begins on phase | `In Progress` | Manual or first issue started |
| Phase fully implemented | `Completed` | All tests pass, PR merged |

#### Update Project Status

```graphql
mutation {
  projectUpdate(id: "<project-uuid>", input: {
    statusId: "<status-uuid>"
  }) {
    success
    project { name status { name } }
  }
}
```

#### Check Project Issue Progress

Before updating status, check issue states:

```graphql
query {
  project(id: "<project-uuid>") {
    name
    status { name }
    issues {
      nodes {
        identifier
        state { name type }
      }
    }
  }
}
```

**Logic for auto-determining status:**
- If ANY issue has `state.type = "started"` → Project is `In Progress`
- If ALL issues have `state.type = "completed"` → Project is `Completed`
- If NO issues started → Project is `Planned` or `Backlog`

#### Helper: Update Project Status Script

```javascript
// Check project issues and update status accordingly
node -e "
const PROJECT_ID = '<project-uuid>';

// Status UUIDs (query your workspace for these)
const STATUS = {
  backlog: '1ed7da89-db44-4339-b0d7-ce37d8ff9604',
  planned: '33ebbb84-53ea-4dd8-a8db-49a8b3b9c502',
  inProgress: '71d18c8f-53de-4752-be37-a6d529cb9c97',
  completed: '54294a72-010d-4ae7-9829-bed76232fb66'
};

async function updateProjectStatus() {
  // Get project issues
  const issueQuery = \`query {
    project(id: \"${PROJECT_ID}\") {
      name
      issues { nodes { state { type } } }
    }
  }\`;

  const res = await fetch('https://api.linear.app/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': process.env.LINEAR_API_KEY },
    body: JSON.stringify({ query: issueQuery })
  });
  const { data } = await res.json();

  const issues = data.project.issues.nodes;
  const states = issues.map(i => i.state.type);

  // Determine appropriate status
  let newStatus;
  if (states.every(s => s === 'completed')) {
    newStatus = STATUS.completed;
  } else if (states.some(s => s === 'started')) {
    newStatus = STATUS.inProgress;
  } else {
    newStatus = STATUS.planned;
  }

  // Update project
  const mutation = \`mutation {
    projectUpdate(id: \"${PROJECT_ID}\", input: { statusId: \"${newStatus}\" }) {
      success
      project { name status { name } }
    }
  }\`;

  const updateRes = await fetch('https://api.linear.app/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': process.env.LINEAR_API_KEY },
    body: JSON.stringify({ query: mutation })
  });
  const result = await updateRes.json();
  console.log('Updated:', result.data.projectUpdate.project);
}

updateProjectStatus();
"
```

### Project Updates (Status Reports)

Post status updates to a project's Updates tab. These are visible at `/project/{slug}/updates`.

#### Create Project Update

```graphql
mutation {
  projectUpdateCreate(input: {
    projectId: "<project-uuid>",
    body: "## Status Update\n\nMarkdown content here...",
    health: onTrack
  }) {
    success
    projectUpdate {
      id
      url
      createdAt
    }
  }
}
```

**Health Options:**
- `onTrack` - 🟢 Project proceeding as planned
- `atRisk` - 🟡 Issues that may cause delays
- `offTrack` - 🔴 Project is behind schedule

#### Example: Post Progress Update

```javascript
node -e "
const projectId = '<project-uuid>';

const updateBody = \`## Status: In Progress 🚀

**Swarm execution started** — agents actively implementing features.

### Progress
- **32% complete** (9/28 issues done)
- Project status updated to **In Progress**

### Completed
- ✅ Foundation setup
- ✅ Core configuration

### In Progress
- 🔄 Main feature implementation
- 🔄 UI components

### Up Next
- Testing suite
- Documentation
\`;

const mutation = \`mutation {
  projectUpdateCreate(input: {
    projectId: \\\"\${projectId}\\\",
    body: \${JSON.stringify(updateBody)},
    health: onTrack
  }) {
    success
    projectUpdate { id }
  }
}\`;

fetch('https://api.linear.app/graphql', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Authorization': process.env.LINEAR_API_KEY },
  body: JSON.stringify({ query: mutation })
}).then(r => r.json()).then(d => console.log(JSON.stringify(d, null, 2)));
"
```

#### When to Post Updates

| Trigger | Health | Content |
|---------|--------|---------|
| Work starts (swarm launched) | `onTrack` | Progress %, what's in progress |
| Milestone reached | `onTrack` | Completed items, next steps |
| Blockers encountered | `atRisk` | Issue description, mitigation plan |
| Deadline at risk | `offTrack` | Root cause, revised timeline |
| Phase complete | `onTrack` | Summary, metrics, lessons learned |

---

## Sync Patterns (Bulk Operations)

For bulk synchronization of code changes to Linear, see `sync.md`.

### Quick Sync Commands

```bash
# Bulk update issues to Done (replace PROJ with your team prefix)
npx ts-node scripts/sync.ts --issues PROJ-101,PROJ-102,PROJ-103 --state Done

# Update project status
npx ts-node scripts/sync.ts --project "My Project" --state completed

# Verify sync completed
npx ts-node scripts/sync.ts --verify PROJ-101,PROJ-102 --expected-state Done
```

### Agent-Spawned Sync

Spawn a parallel agent for autonomous sync:

```javascript
Task({
  description: "Sync project issues to Linear",
  prompt: "Update PROJ-101,102,103 to Done. Then update project 'My Project' to completed.",
  subagent_type: "general-purpose"
})
```

### Hook-Triggered Sync

Auto-suggest sync after code edits. Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/skills/linear/hooks/post-edit.sh"
      }]
    }]
  }
}
```

See `sync.md` for complete patterns including AgentDB integration and swarm coordination.

---

## Reference

- Linear MCP: https://linear.app/docs/mcp.md
- GraphQL API: See `api.md`
- SDK Automation: See `sdk.md`
- Bulk Sync: See `sync.md`
