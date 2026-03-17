---
name: 33god-creating-and-working-with-projects
description: >
  Required skill for all 33GOD project creation and task execution workflows.
  Use this skill when: (1) Creating new projects from scratch or cloning existing repos,
  (2) Starting any new task from Bloodbank commands, Plane tickets, or Yi assignments,
  (3) Managing agent worktree allocation and release, (4) Enforcing worktree-to-task
  source linking, (5) Ensuring proper agent accountability through commit requirements.
  This skill supersedes 33god-imi-worktree-management and frames iMi as the mandatory
  workflow orchestration layer for all 33GOD pipeline work.
---

# 33GOD: Creating and Working with Projects

## Core Philosophy

**iMi is the Project Registry**: Every 33GOD project must be registered through iMi. Every unit of work must be executed within an iMi-managed worktree. This is non-negotiable for the 33GOD pipeline.

**Events Drive Everything**: All 33GOD work emits events through Bloodbank. Worktrees emit `worktree.created`, tasks emit `agent.task.*`, and the heartbeat system (`system.heartbeat.tick`) orchestrates agent coordination every 60 seconds.

**Entity-Based Workspace Isolation**: All actors (humans and Yi agents) are equal **entities** with token-based authentication. Each entity has a completely isolated workspace directory. No more shared `.iMi` cluster hubs.

**Universal Identity**: Once registered, a project has a UUID that is referenced across all 33GOD components (Bloodbank events, Plane tickets, Yi orchestrations, Flume task management). Entities also have UUIDs for cross-component identity resolution.

**Worktree = Work Unit**: Each worktree represents a discrete unit of work traceable to a specific task source. All worktrees live within entity workspaces for complete isolation and accountability.

**Accountability Through Code**: Agents cannot release worktrees until changes are staged and committed. The git history + workspace access logs + Bloodbank events become the audit trail for all actions.

## When to Use This Skill

### REQUIRED: Project Creation

**Trigger**: User or agent needs to create a new 33GOD project

**Scenarios**:
1. **From Scratch**: Create new GitHub repo, initialize git, scaffold boilerplate
2. **From Existing Repo**: Clone existing GitHub repo and register as 33GOD project
3. **From PRD Document**: Generate project from specification file

**Commands**:
```bash
# New project with AI-generated scaffold
imi project create --concept "FastAPI backend for ChoreScore gamification" --name ChoreScore

# New project from PRD document
imi project create --prd ./project-specs.md

# New project with explicit stack/database payload
imi project create --payload '{"name":"MyApp","stack":"react","database":"postgres"}'

# Clone and register existing repo
git clone git@github.com:user/existing-repo.git
cd existing-repo
imi init

# Initialize local repo (already exists)
cd /path/to/existing/repo
imi init
```

**What Happens**:
1. GitHub repo created (if new) or validated (if existing)
2. Project registered in PostgreSQL with globally unique UUID
3. Entity workspace claimed for this project (e.g., `/home/you/33GOD/workspaces/delorenj/myproject/`)
4. Full clone created in entity workspace (not shared cluster hub)
5. `trunk-main` worktree created for main branch
6. Project UUID returned for reference in Bloodbank/Yi/Flume

**Critical**: `imi init` requires authentication via `$IMI_IDENTITY_TOKEN`. The entity associated with the token owns the workspace. There is no separate "register" step. Initialization = Registration + Workspace Claim.

### REQUIRED: Starting New Work

**Trigger**: Agent receives a task from any source

**Task Sources** (must link to worktree):
- **Plane Ticket**: `plane_ticket_id` from managing-tickets-and-tasks-in-plane skill
- **Bloodbank Command**: `correlation_id` from rabbitmq message
- **Yi Orchestration**: `orchestrator_id` from agent assignment
- **Sprint Board**: Task ID from external project management system

**Before Starting Work**:
```bash
# Check for in-flight work to avoid conflicts
imi list --json | jq '.data[] | select(.has_uncommitted_changes == true)'

# Check project status
imi status

# Create typed worktree linked to task source
imi add feat user-authentication
# OR: imi add fix login-bug
# OR: imi add aiops mcp-tool-refactor
# OR: imi add devops ci-migration
# OR: imi add review 123  # For PR reviews
```

**Link Task Source** (TODO - needs implementation):
```bash
# Store task source metadata in worktree
imi metadata set --worktree feat-user-authentication \
  --key plane_ticket_id \
  --value "PROJ-123"

# OR for Bloodbank task
imi metadata set --worktree feat-user-authentication \
  --key bloodbank_correlation_id \
  --value "bb-8f3a9c2e"

# OR for Yi orchestration
imi metadata set --worktree feat-user-authentication \
  --key yi_orchestrator_id \
  --value "yi-orch-5d2b1a"
```

**Agent Claim** (TODO - needs implementation):
```bash
# Claim worktree for exclusive access
imi claim feat-user-authentication --yi-id "claude-sonnet-4.5-agent-001"

# Check who owns a worktree
imi show feat-user-authentication --json | jq '.data.agent_id'
```

**What Happens**:
1. New worktree created with type-specific branch/directory naming
2. Task source metadata stored in JSONB `worktrees.metadata` column
3. Agent ID recorded in `worktrees.agent_id` column (when claim implemented)
4. `.iMi/presence/<worktree>.lock` file created for signaling
5. Worktree path returned for agent to `cd` into

## Complete Command Reference

### Project Lifecycle

#### `imi init [repo] [--force]`
Initialize iMi in current directory or clone from GitHub.

**Behaviors**:
- **No args**: Register current directory as 33GOD project
- **With repo**: Clone `owner/repo` from GitHub then register
- **With --force**: Re-initialize even if already initialized

**What It Does**:
1. Registers project in PostgreSQL (assigns UUID)
2. Creates `.iMi/` cluster hub at parent of trunk
3. Writes `.iMi/project.json` with project metadata
4. Creates `trunk-<branch>` worktree for main branch

**Example**:
```bash
# Initialize existing repo
cd /home/user/code/MyProject
imi init

# Clone and initialize
imi init delorenj/ChoreScore
```

#### `imi project create [--concept|--prd|--name|--payload]`
Bootstrap complete new project with GitHub integration.

**Parameters**:
- `--concept`: Natural language project description
- `--prd`: Path to PRD markdown file
- `--name`: Explicit project name (optional, inferred otherwise)
- `--payload`: JSON string with structured definition

**Stack Detection**:
- **PythonFastAPI**: Creates `pyproject.toml`, mise tasks, docker-compose
- **ReactVite**: Creates `package.json`, vite config, shadcn setup
- **Generic**: Creates basic README and git structure

**Example**:
```bash
imi project create \
  --concept "FastAPI task manager with Postgres and Redis" \
  --name TaskMaster
```

### Worktree Creation

#### `imi add <type> <name> [--repo] [--pr]`
Unified command to create worktrees of any type.

**Built-in Types**:
- `feat` - Feature development (branch: `feat/`, dir: `feat-`)
- `fix` - Bug fixes (branch: `fix/`, dir: `fix-`)
- `aiops` - AI operations: agents, rules, MCP configs, workflows (branch: `aiops/`, dir: `aiops-`)
- `devops` - DevOps tasks: CI, repo organization, deploys (branch: `devops/`, dir: `devops-`)
- `review` - Pull request reviews (branch: `pr-review/`, dir: `pr-review-`)

**Custom Types**:
Use `imi types add <name>` to create custom types with your own prefixes.

**Examples**:
```bash
# Create feature worktree
imi add feat user-authentication

# Create fix worktree
imi add fix login-redirect-bug

# Create AI ops worktree
imi add aiops mcp-server-integration

# Create DevOps worktree
imi add devops github-actions-ci

# Create review worktree (special - requires PR number)
imi add review 123 --pr 123
```

#### Legacy Type Commands (Deprecated)

These still work but emit deprecation warnings:
```bash
imi feat <name>       # Use: imi add feat <name>
imi fix <name>        # Use: imi add fix <name>
imi aiops <name>      # Use: imi add aiops <name>
imi devops <name>     # Use: imi add devops <name>
```

#### `imi review <pr_number> [repo]`
Create worktree for reviewing a pull request.

**Requirements**:
- GitHub CLI (`gh`) must be installed and authenticated
- PR must exist in the repository

**What It Does**:
1. Fetches PR from GitHub via `gh pr view <pr>`
2. Creates `pr-review-<number>` worktree
3. Checks out PR branch
4. Displays PR metadata (title, author, description)

**Example**:
```bash
# Review PR in current repo
imi review 456

# Review PR in specific repo
imi review 456 delorenj/ChoreScore
```

### Type Management

#### `imi types list`
List all available worktree types (built-in + custom).

**Output**:
```
Built-in Types:
  feat        Feature development (feat/, feat-)
  fix         Bug fixes (fix/, fix-)
  aiops       AI operations (aiops/, aiops-)
  devops      DevOps tasks (devops/, devops-)
  review      Pull request reviews (pr-review/, pr-review-)
  trunk       Main branch (empty prefix)

Custom Types:
  experiment  Experimental features (experiment/, experiment-)
```

#### `imi types add <name> [--branch-prefix] [--worktree-prefix] [--description]`
Add custom worktree type.

**Parameters**:
- `name`: Type name (lowercase, alphanumeric, hyphens)
- `--branch-prefix`: Branch prefix (defaults to `<type>/`)
- `--worktree-prefix`: Worktree directory prefix (defaults to `<type>-`)
- `--description`: Human-readable description

**Example**:
```bash
imi types add experiment \
  --description "Experimental features and prototypes"

# Creates type with:
# - Branch: experiment/<name>
# - Directory: experiment-<name>
```

#### `imi types remove <name>`
Remove custom worktree type.

**Protection**: Built-in types (feat, fix, aiops, devops, review, trunk) cannot be removed.

**Example**:
```bash
imi types remove experiment
```

### Navigation and Discovery

#### `imi go [query] [-r|--repo] [-w|--worktrees-only] [-a|--include-inactive]`
Navigate to worktree or repository using fuzzy search.

**Behaviors**:
- **No args**: Interactive picker of all worktrees + repos
- **With query**: Fuzzy search by name/branch/path
- **With --repo**: Limit search to specific repo
- **With --worktrees-only**: Exclude trunk and repo roots
- **With --include-inactive**: Include closed/merged worktrees

**Returns in JSON mode**:
```json
{
  "success": true,
  "data": {
    "target_path": "/home/user/code/Project/feat-user-auth",
    "worktree_name": "feat-user-auth",
    "branch_name": "feat/user-auth"
  }
}
```

**Example**:
```bash
# Interactive picker
imi go

# Fuzzy search
imi go user-auth

# Navigate and change directory
cd $(imi go user-auth --json | jq -r '.data.target_path')

# Search within specific repo
imi go auth --repo ChoreScore
```

#### `imi trunk [repo]`
Switch to trunk worktree (main branch).

**Example**:
```bash
# Switch to trunk in current repo
imi trunk

# Switch to trunk in specific repo
imi trunk ChoreScore
```

#### `imi list [--worktrees|--projects] [repo]`
List all active worktrees or projects.

**Modes**:
- **Default**: Lists both projects and their worktrees
- **--worktrees**: Only worktrees
- **--projects**: Only projects/repositories

**JSON Output** (for programmatic access):
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "feat-user-auth",
      "type": "feat",
      "branch": "feat/user-auth",
      "path": "/path/to/worktree",
      "agent_id": "claude-sonnet-4.5-001",
      "has_uncommitted_changes": true,
      "uncommitted_files_count": 5,
      "ahead_of_trunk": 3,
      "behind_trunk": 0,
      "metadata": {
        "plane_ticket_id": "PROJ-123"
      }
    }
  ]
}
```

**Example**:
```bash
# List all
imi list

# List only worktrees
imi list --worktrees

# List for specific repo
imi list ChoreScore

# JSON mode for scripting
imi list --json | jq '.data[] | select(.agent_id != null)'
```

#### `imi status [repo]`
Show comprehensive status of all worktrees.

**What It Shows**:
- Worktree name and type
- Current branch
- Uncommitted changes count
- Ahead/behind trunk status
- Agent ID (if claimed)
- Last commit info

**Example**:
```bash
# Status for all repos
imi status

# Status for specific repo
imi status ChoreScore
```

### Worktree Lifecycle

#### `imi remove <name> [--keep-branch] [--keep-remote] [repo]`
Remove a worktree.

**Default Behavior**:
- Removes worktree directory
- Deletes local branch
- Deletes remote branch (if pushed)
- Marks worktree as inactive in database

**Options**:
- `--keep-branch`: Keep local branch after removing worktree
- `--keep-remote`: Keep remote branch (requires --keep-branch)

**Safety Checks**:
- Warns if uncommitted changes exist
- Confirms before deleting branches

**Example**:
```bash
# Remove worktree and all branches
imi remove feat-user-auth

# Remove worktree but keep branches
imi remove feat-user-auth --keep-branch --keep-remote
```

#### `imi close <name> [repo]`
Close a worktree without merging (cancel the branch).

**Use Case**: Abandoned work, experimental branches, false starts

**What It Does**:
1. Removes worktree directory
2. Deletes local and remote branches
3. Marks as closed in database
4. Does NOT merge to trunk

**Example**:
```bash
imi close feat-experimental-feature
```

#### `imi merge [name] [repo]`
Merge a worktree into trunk-main and close it.

**Behaviors**:
- **No args**: Merges current branch (if in worktree)
- **With name**: Merges specified worktree

**What It Does**:
1. Switches to trunk-main
2. Merges worktree branch
3. Pushes to remote
4. Removes worktree
5. Records merge metadata in database

**Example**:
```bash
# Merge current worktree
imi merge

# Merge specific worktree
imi merge feat-user-auth
```

### Maintenance and Sync

#### `imi sync [repo]`
Synchronize database with actual Git worktrees.

**What It Does**:
- Discovers worktrees on filesystem not in database
- Marks database entries as inactive if worktree deleted
- Updates git state (uncommitted changes, ahead/behind)
- Reconciles any inconsistencies

**Use Case**: After manual git operations, after system crashes, periodic health checks

**Example**:
```bash
# Sync all repos
imi sync

# Sync specific repo
imi sync ChoreScore
```

#### `imi prune [--dry-run] [--force] [repo]`
Clean up stale worktree references from Git.

**What It Does**:
- Removes `.git/worktrees/` entries for deleted worktrees
- Cleans up orphaned directories
- Updates database to match reality

**Options**:
- `--dry-run`: Show what would be removed without doing it
- `--force`: Remove without confirmation prompts

**Example**:
```bash
# Dry run to preview
imi prune --dry-run

# Actually prune
imi prune --force
```

#### `imi repair`
Repair repository paths in database after directories moved.

**Use Case**: Moved home directory, cloned to new machine, restructured code folder

**What It Does**:
- Auto-detects moved repositories
- Updates all paths in database
- Validates git remotes match

**Example**:
```bash
imi repair
```

### Monitoring

#### `imi monitor [repo]`
Start real-time monitoring of worktree activities.

**What It Displays**:
- File changes (created, modified, deleted)
- Git commits
- Worktree switching
- Agent activities

**Use Case**: Observing agent work, debugging workflows, activity logging

**Example**:
```bash
# Monitor all repos
imi monitor

# Monitor specific repo
imi monitor ChoreScore
```

### Utilities

#### `imi completion <shell>`
Generate shell completions for iMi.

**Supported Shells**:
- bash
- zsh
- fish
- powershell

**Example**:
```bash
# Generate zsh completions
imi completion zsh > ~/.zsh/completions/_imi

# Source in .zshrc
fpath=(~/.zsh/completions $fpath)
autoload -Uz compinit && compinit
```

## Commands That Need Implementation

### `imi claim <name> --yi-id <id>`
Claim a worktree for exclusive agent access.

**What It Should Do**:
1. Check if worktree already claimed (error if so)
2. Update `worktrees.agent_id` column with Yi ID
3. Create `.iMi/presence/<worktree>.lock` file
4. Log activity to `agent_activities` table
5. Return success with worktree metadata

**Usage**:
```bash
imi claim feat-user-auth --yi-id "claude-sonnet-4.5-001"
```

**Error Cases**:
- Worktree doesn't exist
- Worktree already claimed by another agent
- Agent ID not provided

### `imi release <name> --yi-id <id>`
Release a worktree (must have clean state).

**What It Should Do**:
1. Verify agent owns the worktree (`worktrees.agent_id` matches)
2. Check for uncommitted changes (`git status`)
3. Fail if dirty state (changes not committed)
4. Clear `worktrees.agent_id` column (set to NULL)
5. Remove `.iMi/presence/<worktree>.lock` file
6. Log release activity
7. Return success

**Usage**:
```bash
# Will fail if uncommitted changes
imi release feat-user-auth --yi-id "claude-sonnet-4.5-001"
```

**Error Cases**:
- Worktree doesn't exist
- Agent doesn't own the worktree
- Uncommitted changes detected
- Yi ID not provided

**Required Flow**:
```bash
# Must commit before release
git add .
git commit -m "feat: Implement feature

Plane-Ticket: PROJ-123
Yi-ID: claude-sonnet-4.5-001

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Now release succeeds
imi release feat-user-auth --yi-id "claude-sonnet-4.5-001"
```

### `imi metadata set --worktree <name> --key <key> --value <value>`
Set metadata on a worktree.

**What It Should Do**:
1. Load worktree from database
2. Parse existing `metadata` JSONB column
3. Set key-value pair (merging with existing)
4. Update database with new metadata
5. Return success

**Usage**:
```bash
# Link to Plane ticket
imi metadata set --worktree feat-user-auth \
  --key plane_ticket_id \
  --value "PROJ-123"

# Link to Bloodbank correlation
imi metadata set --worktree feat-user-auth \
  --key bloodbank_correlation_id \
  --value "bb-8f3a9c2e"

# Link to Yi orchestrator
imi metadata set --worktree feat-user-auth \
  --key yi_orchestrator_id \
  --value "yi-orch-5d2b1a"

# Custom metadata
imi metadata set --worktree feat-user-auth \
  --key priority \
  --value "high"
```

### `imi metadata get --worktree <name> [--key <key>]`
Get metadata from a worktree.

**What It Should Do**:
1. Load worktree from database
2. If `--key` provided: return single value
3. If no key: return entire metadata object
4. Support JSON output mode

**Usage**:
```bash
# Get specific key
imi metadata get --worktree feat-user-auth --key plane_ticket_id
# Output: PROJ-123

# Get all metadata (JSON mode)
imi metadata get --worktree feat-user-auth --json
# Output: {"plane_ticket_id": "PROJ-123", "yi_orchestrator_id": "yi-orch-5d2b1a"}
```

## JSON Output Mode

**ALL commands support `--json` flag** for programmatic access.

**Standard Response Format**:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

**Error Format**:
```json
{
  "success": false,
  "data": null,
  "error": "Worktree not found: feat-nonexistent"
}
```

**Usage Examples**:
```bash
# Parse with jq
imi list --json | jq '.data[] | select(.type == "feat")'

# Extract path for cd
cd $(imi go user-auth --json | jq -r '.data.target_path')

# Check for errors in scripts
if ! result=$(imi add feat demo --json); then
  echo "Failed to create worktree"
  exit 1
fi
```

## Worktree Lifecycle Rules

### Rule 1: One Agent Per Worktree

**Enforcement**: The `worktrees.agent_id` column tracks the currently assigned agent.

**Multi-Contributor Pattern**:
- Multiple agents CAN contribute to the same worktree over time
- Only ONE agent may be active at any given moment
- `agent_activities` table tracks full history of all contributors

**Example**:
```bash
# Agent A starts work
imi claim feat-user-auth --yi-id "agent-a"
# ... agent-a works, commits, pushes ...

# Agent A hands off to Agent B
imi release feat-user-auth --yi-id "agent-a"
imi claim feat-user-auth --yi-id "agent-b"
# ... agent-b continues, commits, pushes ...
```

### Rule 2: Release Requires Clean State

**Enforcement**: `imi release` command checks for uncommitted changes before releasing.

**Release Checklist**:
- [ ] All changes staged: `git add .`
- [ ] Changes committed: `git commit -m "..."`
- [ ] Commit message includes Yi ID and task source
- [ ] Optional: Changes pushed to remote

**Commit Format** (enforced):
```bash
git commit -m "feat: Implement user authentication endpoint

Implemented JWT-based authentication with refresh tokens.
Added password hashing with bcrypt.
Created login/logout/refresh endpoints.

Plane-Ticket: PROJ-123
Yi-ID: claude-sonnet-4.5-agent-001

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Why This Matters**: The git history becomes the authoritative audit trail. If changes aren't committed, there's no record of who did what. Uncommitted changes = unaccountable work.

### Rule 3: Task Source Must Be Linkable

**Enforcement**: Every worktree must have at least ONE of these metadata keys:
- `plane_ticket_id`
- `bloodbank_correlation_id`
- `yi_orchestrator_id`
- `sprint_board_task_id`

**Verification**:
```bash
# Query worktrees missing task source links
psql -U imi -d imi -c "
SELECT id, name, agent_id
FROM worktrees
WHERE active = TRUE
  AND metadata @> '{}'::jsonb;
"
```

**Why This Matters**: Without task source linking, worktrees become orphaned. You can't trace back to "why was this work done?" or "who requested this?". Task linkage enables end-to-end traceability from request → assignment → work → completion.

## Agent Workflow Patterns

### Pattern 1: Bloodbank Task Execution

```bash
# 1. Agent receives message from Bloodbank queue
# Message contains: task_description, correlation_id, priority

# 2. Create worktree based on task type
imi add feat user-profile-page

# 3. Link Bloodbank correlation ID (TODO - needs implementation)
imi metadata set --worktree feat-user-profile-page \
  --key bloodbank_correlation_id \
  --value "bb-a3f7d9e1"

# 4. Claim worktree (TODO - needs implementation)
imi claim feat-user-profile-page --yi-id "$YI_AGENT_ID"

# 5. Navigate and work
cd $(imi go feat-user-profile-page --json | jq -r '.data.target_path')
# ... implement feature ...

# 6. Commit with metadata
git add .
git commit -m "feat: User profile page

Correlation-ID: bb-a3f7d9e1
Yi-ID: $YI_AGENT_ID"

# 7. Release worktree (TODO - needs implementation)
imi release feat-user-profile-page --yi-id "$YI_AGENT_ID"

# 8. Publish completion event to Bloodbank
# (handled by iMi internally)
```

### Pattern 2: Plane Ticket Assignment

```bash
# 1. Query next available ticket from Plane
plane_ticket=$(plane api issues list --state "todo" --limit 1 | jq -r '.[0].id')

# 2. Determine worktree type from ticket labels
ticket_type=$(plane api issues get $plane_ticket | jq -r '.labels[0].name')

# 3. Create worktree
imi add $ticket_type $(plane api issues get $plane_ticket | jq -r '.name')

# 4. Link Plane ticket (TODO - needs implementation)
imi metadata set --worktree <worktree-name> \
  --key plane_ticket_id \
  --value "$plane_ticket"

# 5. Claim, work, commit, release (same as above)

# 6. Update Plane ticket status
plane api issues update $plane_ticket --state "in_progress"
```

### Pattern 3: Yi Orchestrator Handoff

```bash
# 1. Yi assigns task to agent with orchestrator_id

# 2. Check if worktree already exists (handoff from another agent)
existing_worktree=$(imi list --json | jq -r ".data[] | select(.metadata.yi_orchestrator_id == \"$ORCHESTRATOR_ID\") | .name")

if [ -z "$existing_worktree" ]; then
  # New task - create worktree
  imi add feat $TASK_NAME
  imi metadata set --worktree feat-$TASK_NAME \
    --key yi_orchestrator_id \
    --value "$ORCHESTRATOR_ID"
else
  # Handoff - claim existing worktree
  echo "Taking over worktree: $existing_worktree"
fi

# 3. Claim worktree (TODO - needs implementation)
imi claim <worktree> --yi-id "$YI_AGENT_ID"

# 4. Work, commit, release
```

## Integration with 33GOD Components

### Bloodbank (Event Bus)

**Published Events**:
- `imi.project.created` - New project registered
- `imi.worktree.created` - New worktree allocated
- `imi.worktree.claimed` - Agent claimed worktree
- `imi.worktree.released` - Agent released worktree
- `imi.worktree.merged` - Worktree merged to trunk

**Consumed Events**:
- `task.assigned` - Trigger worktree creation
- `project.scaffold.requested` - Trigger project creation

### Plane (Sprint Board)

**Integration Points**:
- Worktree metadata stores `plane_ticket_id`
- Plane ticket custom fields store `imi_worktree_id` (UUID)
- Agent activities log references Plane ticket in description
- Plane webhooks trigger iMi worktree operations

### Yi (Agent Orchestration)

**Integration Points**:
- Yi queries iMi for available worktrees before assignment
- Yi checks `worktrees.agent_id` to avoid double-assignment
- Yi resolves working paths via `get_project_working_path()` function
- Yi monitors in-flight work via `v_inflight_work` view

### Flume (Session/Task Manager)

**Integration Points**:
- Flume sessions map 1:1 to iMi worktrees
- Flume task lifecycle tied to worktree lifecycle
- Flume queries iMi for project UUIDs when creating tasks

## MCP Tools Reference

iMi exposes 10 MCP tools via FastMCP server for Claude Desktop integration:

### Creation Tools
- `create_worktree(name, worktree_type="feat", repo=None)`
- `create_review_worktree(pr_number, repo=None)`
- `create_project(concept=None, prd=None, name=None, payload=None)`

### Navigation Tools
- `list_worktrees(repo=None)`
- `navigate_worktree(query, repo=None)`
- `show_status(repo=None)`

### Cleanup Tools
- `remove_worktree(name, repo=None, keep_branch=False)`
- `sync_worktrees(repo=None)`
- `prune_worktrees(repo=None, dry_run=False)`

### Discovery Tools
- `list_types()`

See `/home/delorenj/.claude/skills/33god-imi-worktree-management/references/mcp-tools-reference.md` for detailed schemas.

## Database Schema Reference

### Critical Tables

**projects**:
- `id` (UUID) - Globally unique project identifier
- `remote_origin` (TEXT) - 1:1 mapping to GitHub URL (unique constraint)
- `trunk_path` (TEXT) - Filesystem path to trunk worktree
- `metadata` (JSONB) - Extensible project metadata

**worktrees**:
- `id` (UUID) - Globally unique worktree identifier
- `project_id` (UUID FK) - References `projects.id`
- `type_id` (INTEGER FK) - References `worktree_types.id`
- `agent_id` (TEXT) - Currently assigned Yi agent (NULL if unclaimed)
- `has_uncommitted_changes` (BOOLEAN) - Dirty state flag
- `uncommitted_files_count` (INTEGER) - Number of uncommitted files
- `ahead_of_trunk` (INTEGER) - Commits ahead of trunk
- `behind_trunk` (INTEGER) - Commits behind trunk
- `metadata` (JSONB) - Task source links stored here
  - `plane_ticket_id`
  - `bloodbank_correlation_id`
  - `yi_orchestrator_id`

**agent_activities**:
- `id` (UUID) - Activity identifier
- `agent_id` (TEXT) - Yi agent who performed action
- `worktree_id` (UUID FK) - Worktree where action occurred
- `activity_type` (TEXT) - `created`, `modified`, `committed`, `pushed`, `merged`
- `description` (TEXT) - Human-readable description

### Critical Functions

**register_project(name, remote_origin, default_branch, trunk_path, metadata)**:
- Idempotent project registration
- Returns project UUID
- Enforces 1:1 remote_origin constraint

**register_worktree(project_id, type_id, name, branch_name, path, agent_id, metadata)**:
- Creates worktree with proper FKs
- Validates type_id exists
- Returns worktree UUID

**get_inflight_work(project_id)**:
- Returns all worktrees with uncommitted changes or divergence
- Useful for conflict detection before starting new work

**get_project_working_path(project_id, worktree_name)**:
- Resolves canonical filesystem path
- Returns trunk path if worktree_name is NULL
- Returns worktree path if worktree_name provided

## Error Handling and Edge Cases

### Uncommitted Changes on Release

**Error**: `imi release` fails if `git status` shows dirty state

**Resolution**:
```bash
# Stage changes
git add .

# Commit with proper metadata
git commit -m "feat: Description

Plane-Ticket: PROJ-123
Yi-ID: $YI_AGENT_ID"

# Retry release
imi release <worktree> --yi-id "$YI_AGENT_ID"
```

### Worktree Already Claimed

**Error**: `imi claim` fails if `agent_id` is already set

**Resolution**:
```bash
# Check current owner
imi show <worktree> --json | jq '.data.agent_id'

# Option 1: Current agent releases first
imi release <worktree> --yi-id "<current-agent>"

# Option 2: Force claim (emergency override)
imi claim <worktree> --yi-id "$YI_AGENT_ID" --force
```

### Missing Task Source Link

**Error**: Worktree created without metadata linking to task source

**Resolution**:
```bash
# Retroactively add task source
imi metadata set --worktree <worktree> \
  --key plane_ticket_id \
  --value "PROJ-123"

# Verify
imi metadata get --worktree <worktree> --key plane_ticket_id
```

### Project Already Registered

**Error**: `imi init` reports project already exists

**Behavior**: iMi is idempotent - returns existing project UUID without error

**No Action Required**: This is expected behavior for distributed registration

## Deprecation Notice

**Old Skill**: `33god-imi-worktree-management`

**Status**: Deprecated but still functional

**Migration Path**: Use `33god-creating-and-working-with-projects` instead for all new workflows. The old skill focused on iMi's technical capabilities; the new skill focuses on when and why to use iMi in 33GOD workflows.

## Implementation Roadmap

**Commands Needing Implementation**:
1. `imi claim <name> --yi-id <id>` - Agent worktree claiming
2. `imi release <name> --yi-id <id>` - Agent worktree release with clean state check
3. `imi metadata set --worktree <name> --key <k> --value <v>` - Set metadata
4. `imi metadata get --worktree <name> [--key <k>]` - Get metadata

**Database Schema**: Already supports all features (agent_id column, metadata JSONB column with GIN index)

**Implementation Path**:
- Add commands to `src/cli.rs`
- Implement handlers in `src/main.rs`
- Add database methods in `src/database.rs` for updating agent_id and metadata
- Add lock file management in `src/local.rs` for `.iMi/presence/` directory

## References

### Architecture Documentation
- `/home/delorenj/code/iMi/trunk-main/docs/architecture-imi-project-registry.md`
- PostgreSQL schema: `/home/delorenj/code/iMi/trunk-main/migrations/001_create_schema.sql`
- Helper functions: `/home/delorenj/code/iMi/trunk-main/migrations/002_functions_and_helpers.sql`

### Related Skills
- `managing-tickets-and-tasks-in-plane` - Sprint board integration
- `33god-service-development` - Microservice creation patterns
- `33god-development-lifecycle` - Meta-level orchestration

### Database Connection
```bash
# Interactive psql session
/home/delorenj/code/iMi/trunk-main/scripts/psql-imi.sh

# Query example
/home/delorenj/code/iMi/trunk-main/scripts/psql-imi.sh -c "SELECT * FROM v_inflight_work"
```
