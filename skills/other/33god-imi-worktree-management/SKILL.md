---
name: 33god-imi-worktree-management
description: >
  **DEPRECATED**: This skill is deprecated in favor of 33god-creating-and-working-with-projects.
  The new skill frames iMi from the perspective of 33GOD project lifecycle and agent workflow
  orchestration rather than technical capabilities. Use the new skill for all project creation
  and task execution workflows. This skill remains for reference only.
deprecated: true
superseded_by: 33god-creating-and-working-with-projects
---

# 33GOD iMi Worktree Management

> **⚠️ DEPRECATION NOTICE**
>
> This skill has been deprecated in favor of `33god-creating-and-working-with-projects`.
>
> **Why the change?**
> - New skill focuses on *when* and *why* to use iMi (workflow-oriented)
> - Old skill focused on *what* iMi can do (capability-oriented)
> - New skill emphasizes mandatory worktree-to-task-source linking
> - New skill covers agent accountability and release protocols
>
> **Migration Path**: Use `33god-creating-and-working-with-projects` for all new work.
> This skill remains for technical reference only.

## Overview

iMi is a Rust CLI tool providing opinionated git worktree management integrated with the 33GOD agentic pipeline. It serves as the **Project Registry** - the single source of truth for all 33GOD projects with strict 1:1 mapping between `project_id` and GitHub remote origins. It enforces strict naming conventions, maintains a PostgreSQL database of project and worktree metadata, and exposes operations via both CLI (with JSON output) and MCP tools for Claude Desktop integration.

**Core Philosophy:** Convention over configuration. iMi's opinionated structure enables predictable worktree layouts, type-based workflows, and seamless 33GOD ecosystem integration.

**Project Registry Role:**
- Assigns unique UUIDs to all 33GOD projects
- Enforces 1:1 mapping: `project_id` ↔ `git@github.com:user/repo.git`
- Tracks in-flight work (uncommitted changes, unmerged worktrees, branch divergence)
- Provides deterministic working paths for all 33GOD components
- Prevents duplicate project registrations across distributed hosts

## Core Capabilities

### 1. Database-Driven Worktree Types

iMi uses a normalized PostgreSQL schema with proper UUID-based foreign keys. The `worktree_types` table defines both built-in and custom worktree types with associated naming conventions:

**Built-in Types:**
- `feat` - Feature development (branch: `feat/`, worktree: `feat-`)
- `fix` - Bug fixes (branch: `fix/`, worktree: `fix-`)
- `aiops` - AI operations: agents, rules, MCP configs, workflows (branch: `aiops/`, worktree: `aiops-`)
- `devops` - DevOps tasks: CI, repo organization, deploys (branch: `devops/`, worktree: `devops-`)
- `review` - Pull request reviews (branch: `pr-review/`, worktree: `pr-review-`)
- `trunk` - Main branch worktree (branch: ``, worktree: `trunk-`)

**Custom Types:**
Users can define custom types with `imi types add <name>` to extend the type system.

**Schema Design:**
- `projects` table: Unique UUID for each project, unique constraint on `remote_origin`
- `worktrees` table: UUID primary key, foreign keys to `projects.id` and `worktree_types.id`
- `agent_activities` table: Audit log of all agent actions across worktrees
- JSONB metadata columns on all tables for extensibility without migrations
- Partial indexes on active records only for performance
- Views for common queries (`v_inflight_work`, `v_worktrees_detail`, `v_projects_summary`)

### 2. Hierarchical Command Structure

**Unified Worktree Creation:**
```bash
imi add <type> <name>     # Create worktree of specified type
imi add feat user-auth    # Creates feat-user-auth worktree, feat/user-auth branch
```

**Type Management:**
```bash
imi types list              # Show all available types
imi types add experiment    # Add custom type
imi types remove experiment # Remove custom type (builtins protected)
```

**Legacy Commands (Deprecated):**
Old flat commands still work but emit deprecation warnings:
```bash
imi feat user-auth  # ⚠️ Deprecated: use 'imi add feat user-auth'
```

### 3. Project Creation and Scaffolding

Bootstrap complete projects with GitHub integration:

```bash
imi project create --concept "FastAPI task manager with Postgres" --name TaskMaster
imi project create --prd ./specs.md
imi project create --payload '{"name":"MyApp","stack":"react","database":"postgres"}'
```

**Scaffolding Includes:**
- GitHub repository creation via REST API
- Stack detection (Generic, PythonFastAPI, ReactVite)
- Boilerplate generation:
  - Python: `pyproject.toml` with UV + hatchling, mise tasks
  - React: `package.json` with bun + vite + shadcn
  - Docker: `compose.yml` for services
- Git initialization and remote push

### 4. MCP Tool Integration

iMi exposes 10 MCP tools via FastMCP server for Claude Desktop:

**Tool Categories:**
- **Creation:** `create_worktree`, `create_review_worktree`, `create_project`
- **Navigation:** `list_worktrees`, `navigate_worktree`, `show_status`
- **Cleanup:** `remove_worktree`, `sync_worktrees`, `prune_worktrees`
- **Discovery:** `list_types`

See [mcp-tools-reference.md](references/mcp-tools-reference.md) for detailed tool schemas and examples.

### 5. Opinionated Worktree Conventions

**Directory Structure:**
```
/home/delorenj/code/
├── ProjectName/                  # IMI_PATH (sandbox/cluster directory)
│   ├── .iMi/                     # Cluster hub (shared by all worktrees)
│   │   ├── presence/             # Lock files for agent signaling
│   │   ├── links/                # Shared environment files
│   │   └── registry.toml         # Fast metadata cache (data plane)
│   ├── trunk-main/               # Main branch worktree (never commit directly)
│   ├── feat-user-auth/           # Feature worktree
│   ├── fix-login-bug/            # Fix worktree
│   ├── aiops-mcp-server/         # AI operations worktree
│   ├── devops-ci-pipeline/       # DevOps worktree
│   └── pr-review-123/            # PR review worktree
```

**Dual-Plane Architecture:**
iMi implements a two-tier data architecture for optimal performance:

- **Control Plane (PostgreSQL)**: Durable state management, normalized schema with proper FKs, complex queries, historical tracking, ACID guarantees
- **Data Plane (`.iMi/` filesystem)**: High-speed metadata access for shell integrations (Starship)

The `.iMi/` directory exists at the **cluster hub level** (parent of all worktrees), NOT inside individual worktrees. This enables:
- Instant worktree type lookups without database queries (via `registry.toml`)
- Agent presence signaling through lock files (`.iMi/presence/*.lock`)
- Shared configuration across worktrees (`.iMi/links/`)

Both planes are kept in sync via dual-write on worktree create/remove operations.

**PostgreSQL Features:**
- **In-Flight Work Tracking**: Denormalized fields track `has_uncommitted_changes`, `ahead_of_trunk`, `behind_trunk` for each worktree
- **Helper Functions**: 20+ functions for common operations (`register_project()`, `register_worktree()`, `update_worktree_git_state()`, `get_inflight_work()`)
- **Triggers**: Auto-updating timestamps, state synchronization between fields
- **Extensibility**: JSONB metadata columns with GIN indexes for fast queries
- **Concurrent Access**: Multiple agents can safely register projects and worktrees across distributed 33GOD hosts

**Naming Rules:**
- Worktree directory: `<type-prefix><name>` (e.g., `feat-user-auth`)
- Git branch: `<type-prefix>/<name>` (e.g., `feat/user-auth`)
- Trunk worktree: Always `trunk-<default-branch>` (e.g., `trunk-main`)

**Workflow Pattern:**
1. Create feature worktree: `imi add feat user-auth`
2. Navigate to worktree: `cd $(imi go user-auth --json | jq -r '.data.target_path')`
3. Develop, commit, push
4. Create PR via `gh pr create`
5. Review in dedicated worktree: `imi review 123`
6. Merge and cleanup: `imi remove feat-user-auth`

See [worktree-conventions.md](references/worktree-conventions.md) for deep dive on conventions and workflows.

## 33GOD Ecosystem Integration

iMi is a core component of the 33GOD agentic pipeline:

**Bloodbank Integration:**
- Publishes events: `imi.worktree.created`, `imi.project.created`
- Consumes events: External triggers for project creation, worktree orchestration

**Jelmore Integration:**
- Session-aware worktree context
- Agent coordination across worktrees

**Flume Integration:**
- Task management tied to worktree lifecycle
- Automatic task creation for new worktrees

**Directory Convention:**
All 33GOD projects follow iMi's `/home/delorenj/code/<project>/<worktree>/` structure.

## JSON Output Mode

All iMi commands support `--json` flag for programmatic access:

```bash
imi types list --json
imi add feat demo --json
imi list --json
```

**Response Format:**
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

This enables MCP tool integration and Bloodbank event publishing.

## Common Workflows

**Feature Development:**
```bash
imi add feat user-authentication
cd feat-user-authentication
# ... develop, commit, push ...
gh pr create
imi go trunk-main && git pull
imi remove feat-user-authentication
```

**PR Review:**
```bash
imi review 456  # Fetches PR #456 with gh CLI
cd pr-review-456
# ... review, test, comment ...
imi remove pr-review-456
```

**Project Bootstrapping:**
```bash
imi project create --concept "FastAPI backend for task management" --name TaskMaster
cd TaskMaster
mise install && uv sync
mise run dev
```

**Custom Type Creation:**
```bash
imi types add experiment --description "Experimental features and prototypes"
imi add experiment neural-net
```

## Error Handling

**Common Issues:**
- GitHub token missing: Set `GITHUB_TOKEN` env var or run `gh auth login`
- Type not found: Run `imi types list` to see available types
- Worktree already exists: Use `imi list` to find existing worktrees
- Database sync issues: Run `imi sync` to reconcile database with git state

## Resources

### references/
- **mcp-tools-reference.md**: Detailed MCP tool schemas, parameters, and usage examples
- **worktree-conventions.md**: Deep dive on iMi's opinionated structure and workflow patterns
- **project-creation.md**: Stack detection logic, boilerplate templates, and scaffolding patterns

### scripts/
Not applicable - iMi CLI and MCP tools handle all operations.

### assets/
Not applicable - no templates or assets needed for worktree management.
