---
name: Linear
description: Managing Linear issues, projects, and teams. Use when working with Linear tasks, creating issues, updating status, querying projects, or managing team workflows.
version: 3.2.0
author: Ryan Smith <ryan@smithhorn.ca>
tags:
  - linear
  - issue-tracking
  - project-management
  - mcp
  - graphql
  - workflow
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
linear issues view ENG-123

# Create an issue
linear issues create --title "Issue title" --description "Description"

# Update issue status (get state IDs first)
linear issues update ENG-123 -s "STATE_ID"

# Add a comment
linear issues comment add ENG-123 -m "Comment text"

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
varlock run -- npm run query -- "query { viewer { name } }"

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
npm run setup
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
npm run query -- "query { viewer { name } }"
```

You should see your name from Linear.

### 4. Common Operations

```bash
# Create issue in a project
npm run ops -- create-issue "Project" "Add rate limiting to auth endpoints" "Auth endpoints have no rate limiting, allowing brute-force attacks. Add configurable limits per endpoint with 429 responses when exceeded."

# Update issue status
npm run ops -- status Done ENG-123 ENG-124

# Create sub-issue
npm run ops -- create-sub-issue ENG-100 "Sub-task" "Details"

# Update project status
npm run ops -- project-status "Phase 1" completed

# Show all commands
npm run ops -- help
```

See [Project Management Commands](#project-management-commands) for full reference.

---

## Issue Creation Checklist (Required)

**When creating a Linear issue, always complete these three steps — even if the user doesn't mention them.**

1. **Detailed description with Acceptance Criteria.** Every issue description MUST include an `## Acceptance Criteria` section with at least 2 concrete, testable checklist items. See [docs/issue-template.md](docs/issue-template.md) for the canonical template plus a populated full example. The CLI `create-issue` / `create-sub-issue` will reject descriptions missing this structure; for MCP `save_issue` callers, validate the draft first with `npm run ops -- validate-description --stdin` (see below). If the user provides only a title, draft the description yourself using the template below.

   **Depth — default to the full six-section template.** Unless the user's phrasing clearly signals brevity (*"quick issue"*, *"one-liner"*, *"just the AC"*, *"brief"*, *"terse"*, *"minimum"*, *"short"*), structure the body as **Context → Problem → Proposal → Acceptance Criteria → Verification → Out of scope**. The 120-char / 2-item floor is what the validator *rejects*, not what reviewers *want*. If the user gives you only a title, draft a verbose body from the full template — ask follow-up questions rather than shipping the floor. For trivial changes (typo fix, one-line config tweak), collapsing `Problem` into `Context` and dropping `Verification` is fine when the AC is self-evidently testable — collapse deliberately, not by default.

   ```markdown
   ## Context
   **Title:** <title>

   <What is changing and why. 2-4 sentences. Link prior issues, docs, or incidents that motivate this.>

   ## Problem
   <What specifically is broken, missing, or insufficient today. Name the file, flow, or behavior.>

   ## Proposal
   <What you intend to do about it. High-level approach, not implementation line-by-line.>

   ## Acceptance Criteria
   - [ ] <Concrete, testable outcome>
   - [ ] <Concrete, testable outcome>

   ## Verification
   <How the AC will actually be checked. Manual steps, test command, or review instruction.>

   ## Out of Scope
   - <What this issue does NOT cover — redirect to the follow-up or explain why it's deferred>
   ```

   Print the template on demand with: `npm run ops -- create-issue --template`. See [docs/issue-template.md](docs/issue-template.md) for a fully populated example.

2. **Labels.** Apply from the [label taxonomy](docs/labels.md):
   - Exactly ONE type label (`feature`, `bug`, `refactor`, `chore`, `spike`)
   - 1-2 domain labels (`backend`, `frontend`, `security`, `infrastructure`, etc.)
   - Scope labels if relevant (`blocked`, `breaking-change`, `tech-debt`)

3. **Project assignment.** Assign to the appropriate project based on context (active sprint, feature area, or user instruction). If no project is obvious, ask the user. In batch/subagent context, use the project associated with the parent issue or the default initiative project.

**When updating** an existing issue, preserve existing labels and project — only add missing labels or correct misassigned ones.

> **MCP tools.** Before calling `mcp__linear__save_issue` (or any MCP issue-create tool), pipe the draft description through `validate-description --stdin` and only call `save_issue` if it exits 0:
>
> ```bash
> echo "$DRAFT_BODY" | npm run ops -- validate-description --stdin
> # exit 0 → safe to call save_issue
> # exit 5 → fix the description; re-pipe; try again
> ```
>
> The CLI already gates this for `create-issue` / `create-sub-issue`. MCP has no server-side gate — this pre-flight + the retroactive `npm run lint-issues` audit are the only enforcement for the MCP path. For longer drafts in a file, use `--file <path>` instead of `--stdin`.
>
> **Depth ≠ validation.** Validation passing (exit 0) only means the 120-char / 2-AC floor is met. Structure the body as the full six-section template (Context → Problem → Proposal → AC → Verification → Out of Scope) unless the user explicitly asked for brevity — see bullet #1 above.
>
> **Enforcement model.** CLI + SDK paths are hard-gated; the MCP path is instruction + audit. A PreToolUse hook that intercepts `save_issue` was considered and rejected: it only fires when Claude Code is the runtime, install is per-user, and the payload shape is harness-version-dependent. Run `npm run lint-issues -- --since 24h` locally or in CI to catch instruction-layer drift retroactively.

---

## Project Planning Workflow

> See [Issue Creation Checklist](#issue-creation-checklist-required) — descriptions, labels, and project assignment are required for every issue.

### Create Issues in the Correct Project from the Start

**Best Practice**: When planning a new phase or initiative, create the project and its issues together in a single planning session. Avoid creating issues in a catch-all project and moving them later.

#### Recommended Workflow

1. **Create the project first**:
   ```bash
   npm run ops -- create-project "Phase X: Feature Name" "My Initiative"
   ```

2. **Set project state to Planned**:
   ```bash
   npm run ops -- project-status "Phase X: Feature Name" planned
   ```

3. **Create issues directly in the project** (use `--template` to print the canonical template first, or pass a multi-line description via heredoc):
   ```bash
   # Print the template to seed your description
   npm run ops -- create-issue --template

   # Create the issue with a template-shaped description
   npm run ops -- create-issue "Phase X: Feature Name" "Parent task" "$(cat <<'EOF'
   ## Context
   Implement the core feature with integration tests and documentation.

   ## Acceptance Criteria
   - [ ] All API endpoints return correct responses
   - [ ] Test coverage >80% on new modules
   EOF
   )" --labels feature,backend

   npm run ops -- create-sub-issue ENG-XXX "Sub-task 1" "$(cat <<'EOF'
   ## Context
   Set up database schema and migrations for the new feature tables.

   ## Acceptance Criteria
   - [ ] Migration runs cleanly on a fresh database
   - [ ] Rollback migration restores prior schema
   EOF
   )"
   ```

4. **Update project state when work begins**:
   ```bash
   npm run ops -- project-status "Phase X: Feature Name" in-progress
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
npm run ops -- project-status <project-name> <state>
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
npm run ops -- project-status "Phase 8: MCP Decision Engine" in-progress

# Mark project complete
npm run ops -- project-status "Phase 8" completed

# Partial name matching works
npm run ops -- project-status "Phase 8" paused
```

### link-initiative

Link an existing project to an initiative.

```bash
npm run ops -- link-initiative <project-name> <initiative-name>
```

**Examples:**
```bash
# Link a project to an initiative
npm run ops -- link-initiative "Phase 8: MCP Decision Engine" "Q1 Goals"

# Partial matching works
npm run ops -- link-initiative "Phase 8" "Q1 Goals"
```

### unlink-initiative

Remove a project from an initiative.

```bash
npm run ops -- unlink-initiative <project-name> <initiative-name>
```

**Examples:**
```bash
# Remove incorrect link
npm run ops -- unlink-initiative "Phase 8" "Linear Skill"

# Clean up test links
npm run ops -- unlink-initiative "Test Project" "Q1 Goals"
```

**Error Handling:**
- Returns error if project is not linked to the specified initiative
- Returns error if project or initiative not found

### Complete Project Lifecycle Example

```bash
# 1. Create project linked to initiative
npm run ops -- create-project "Phase 11: New Feature" "Q1 Goals"

# 2. Set state to planned
npm run ops -- project-status "Phase 11" planned

# 3. Create issues in the project
npm run ops -- create-issue "Phase 11" "Parent task" "Description"
npm run ops -- create-sub-issue ENG-XXX "Sub-task 1" "Details"

# 4. Start work - update to in-progress
npm run ops -- project-status "Phase 11" in-progress

# 5. Mark issues done
npm run ops -- status Done ENG-XXX ENG-YYY

# 6. Complete project
npm run ops -- project-status "Phase 11" completed

# 7. (Optional) Link to additional initiative
npm run ops -- link-initiative "Phase 11" "Q2 Goals"
```

---

## Tool Selection

Choose the right tool for the task:

| Priority | Tool | When to Use |
|----------|------|-------------|
| 1 | **MCP (Official Server)** | Most operations - PREFERRED |
| 2 | **`lin` CLI** | Fast-path for reads/status updates when installed (optional) |
| 3 | **Helper Scripts** | Bulk operations, label taxonomy, project workflows |
| 4 | **SDK scripts** | Complex operations (loops, conditionals) |
| 5 | **GraphQL API** | Operations not supported by above |

### `lin` CLI (Optional Fast-Path)

If the [`lin`](https://github.com/aaronkwhite/linear-cli) Rust binary is installed, the skill uses it automatically for:
- Issue status updates (`status`, `done`, `wip`)
- Listing initiatives
- Searching issues (`search <query>`)
- Listing issues (`list-issues [--team X] [--state Y]`)
- User info (`whoami`)

All operations fall back silently to the SDK when `lin` is unavailable.

**Install** (optional):
```bash
brew install aaronkwhite/tap/lin    # macOS (Homebrew)
cargo install lincli                # Any platform with Rust
```

**Disable**: Set `LINEAR_USE_LIN=0` to skip `lin` even when installed.

### MCP Server Configuration

**Use the official Linear MCP server** at `mcp.linear.app`:

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

> **WARNING**: Do NOT use deprecated community servers. See [troubleshooting.md](troubleshooting.md) for details.

### MCP Reliability (Official Server)

| Operation | Reliability | Notes |
|-----------|-------------|-------|
| Create issue | ✅ High | Full support |
| Update status | ✅ High | Use `state: "Done"` directly |
| List/Search issues | ✅ High | Supports filters, queries |
| Add comment | ✅ High | Works with issue IDs |

### Quick Status Update

```bash
# Via MCP - use human-readable state names
update_issue with id="issue-uuid", state="Done"

# Via helper script (bulk operations)
node scripts/linear-helpers.mjs update-status Done 123 124 125
```

### Helper Script Reference

For detailed helper script usage, see **[troubleshooting.md](troubleshooting.md)**.

### Parallel Agent Execution

For bulk operations or background execution, use the `Linear-specialist` subagent:

```javascript
Task({
  description: "Update Linear issues",
  prompt: "Mark ENG-101, ENG-102, ENG-103 as Done",
  subagent_type: "Linear-specialist"
})
```

**When to use `Linear-specialist` (parallel):**
- Bulk status updates (3+ issues)
- Project status changes
- Creating multiple issues
- Sync operations after code changes

**When to use direct execution:**
- Single issue queries
- Viewing issue details
- Quick status checks
- Operations needing immediate results

See **[sync.md](sync.md)** for parallel execution patterns.

## Image Uploads

### Step 1: Extract the image from conversation context

Images shared inline in Claude Code are **not** saved to disk automatically — they live as base64 in the session JSONL. Use the extraction script:

```bash
# Find the current session JSONL
ls -t ~/.claude/projects/<project-path>/*.jsonl | head -1

# Extract all inline images (saves to /tmp by default)
npm run extract-image -- <path-to-session.jsonl>

# Or specify a custom output directory
npm run extract-image -- <path-to-session.jsonl> ~/Desktop
```

This saves images to `/tmp/shared-image-0.png`, `/tmp/shared-image-1.png`, etc.

> **Always verify** the extracted image with the Read tool before uploading.

### Step 2: Create the issue

```bash
# Standard approach
npm run ops -- create-issue "Project Name" "Issue title" "Description"
```

> **Note**: If you need to target a specific team and `create-issue` picks the wrong one, use GraphQL with explicit `teamId`:
>
> ```bash
> # Get the project's team
> npm run query -- 'query { projects(filter: { name: { containsIgnoreCase: "PROJECT NAME" } }) { nodes { id name teams { nodes { id name key } } } } }'
>
> # Create with explicit teamId
> npm run query -- 'mutation { issueCreate(input: { teamId: "TEAM_UUID", projectId: "PROJECT_UUID", title: "Issue title", description: "Description" }) { success issue { id identifier url } } }'
> ```

### Step 3: Upload the image and attach to the issue

```bash
npm run upload-image -- /tmp/shared-image-0.png ENG-123 "Optional comment text"
```

The script will:
1. Upload the file to Linear's S3 storage
2. Post a comment on the issue with the image embedded as markdown

**Supported formats**: PNG, JPG/JPEG, GIF, WebP, SVG, PDF

### Known pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `create-issue` picks wrong team | Multiple teams in workspace | Use GraphQL with explicit teamId (see Step 2) |
| `upload-image.ts` "Issue not found" | Issue was deleted before attaching | Ensure issue exists first |
| Image not found on disk | Shared inline, not as file | Extract from session JSONL (Step 1) |

---

## Critical Requirements

### Issues → Projects → Initiatives

**Every issue MUST be attached to a project. Every project MUST be linked to an initiative.**

| Entity | Must Link To | If Missing |
|--------|--------------|------------|
| Issue | Project | Not visible in project board |
| Project | Initiative | Not visible in roadmap |

See **[projects.md](projects.md)** for complete project creation checklist.

---

## Conventions

### Issue Status

- **Assigned to me**: Set `state: "Todo"`
- **Unassigned**: Set `state: "Backlog"`

### Labels

Uses **domain-based label taxonomy** — see [Issue Creation Checklist](#issue-creation-checklist-required) for required rules and [docs/labels.md](docs/labels.md) for the full taxonomy.

```bash
# Validate labels
npm run ops -- labels validate "feature,security"

# Suggest labels for issue
npm run ops -- labels suggest "Fix XSS vulnerability"
```

## SDK Automation Scripts

**Use only when MCP tools are insufficient.** For complex operations involving loops, mapping, or bulk updates, write TypeScript scripts using `@linear/sdk`. See `sdk.md` for:

- Complete script patterns and templates
- Common automation examples (bulk updates, filtering, reporting)
- Tool selection criteria

Scripts provide full type hints and are easier to debug than raw GraphQL for multi-step operations.

## GraphQL API

**Fallback only.** Use when operations aren't supported by MCP or SDK.

See **[api.md](api.md)** for complete documentation including:
- Authentication and setup
- Example queries and mutations
- Timeout handling patterns
- MCP timeout workarounds
- Shell script compatibility

**Quick ad-hoc query:**

```bash
npm run query -- "query { viewer { name } }"
```

## Projects & Initiatives

For advanced project and initiative management patterns, see **[projects.md](projects.md)**.

**Quick reference** - common project commands:

```bash
# Create project linked to initiative
npm run ops -- create-project "Phase X: Name" "My Initiative"

# Update project status
npm run ops -- project-status "Phase X" in-progress
npm run ops -- project-status "Phase X" completed

# Link/unlink projects to initiatives
npm run ops -- link-initiative "Phase X" "My Initiative"
npm run ops -- unlink-initiative "Phase X" "Old Initiative"
```

**Key topics in projects.md:**
- Project creation checklist (mandatory steps)
- Content vs Description fields
- Discovery before creation
- Codebase verification before work
- Sub-issue management
- Project status updates
- Project updates (status reports)

---

## Sync Patterns (Bulk Operations)

For bulk synchronization of code changes to Linear, see **[sync.md](sync.md)**.

**Quick sync commands:**

```bash
# Bulk update issues to Done
npm run ops -- status Done ENG-101 ENG-102 ENG-103

# Update project status
npm run ops -- project-status "My Project" completed
```

---

## Reference

| Document | Purpose |
|----------|---------|
| [api.md](api.md) | GraphQL API reference, timeout handling |
| [sdk.md](sdk.md) | SDK automation patterns |
| [sync.md](sync.md) | Bulk sync patterns |
| [projects.md](projects.md) | Project & initiative management |
| [troubleshooting.md](troubleshooting.md) | Common issues, MCP debugging |
| [docs/labels.md](docs/labels.md) | Label taxonomy |

**External:** [Linear MCP Documentation](https://linear.app/docs/mcp.md)