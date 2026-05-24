---
name: worktree-manager
description: Create and manage git worktrees with automated setup and cleanup for AI coding agents. Use this skill when asked to "create a worktree", "new worktree", "worktree for feature/staging", "setup isolated environment", or "cleanup old worktrees". Handles smart naming, config file copying, background pnpm install, and automatic cleanup of stale worktrees.
---

# Worktree Manager

Automated git worktree management for AI coding agents (Cursor, Claude Code, etc.) with smart naming, auto-setup, and cleanup.

## Cursor Native Worktree Support

Cursor has built-in worktree support via `.cursor/worktrees.json`. When you create a worktree through Cursor's UI or this script, the following files are automatically copied:

- `.env` - Environment variables
- `.claude/settings.local.json` - AI agent local settings

Dependencies are installed in the background via `pnpm install`.

**Note:** MCP settings (`.cursor/mcp.json`, `.mcp.json`) are NOT copied because Cursor inherits MCP configuration from the main application automatically.

## Quick Start

### Create a Worktree

When the user asks to create a worktree for a feature or environment, derive a short, descriptive kebab-case name from their request:

**Naming examples:**

- "staging environment" → `staging-env`
- "add dark mode toggle" → `dark-mode`
- "fix authentication bug" → `fix-auth-bug`
- "update API endpoints" → `update-api`

Then run:

```bash
# Standard (uses shared dev database)
.claude/skills/worktree-manager/scripts/worktree.sh create <derived-name>

# Isolated (creates dedicated database with seeding)
.claude/skills/worktree-manager/scripts/worktree.sh create <derived-name> --isolated
```

**What happens:**

1. Cleans up worktrees older than 7 days
2. Creates branch: `worktree/<name>-<timestamp>`
3. Creates worktree at: `~/ai-worktrees/<project-name>/<name>-<timestamp>`
4. Copies configuration files from main repo:
   - `.env`
   - `.claude/settings.local.json`
5. Starts `pnpm install` in background
6. If `--isolated`: Creates dedicated SQLite database and seeds it with test data
7. Returns the worktree path immediately

### When to Use --isolated

Use the `--isolated` flag when:

- **Schema changes:** Testing database migrations
- **Migration testing:** Verifying migration scripts work correctly
- **Isolated experiments:** Need a clean database state
- **Breaking changes:** Don't want to affect shared dev data

For normal feature development, skip `--isolated` to use the shared database.

### List Worktrees

```bash
.claude/skills/worktree-manager/scripts/worktree.sh list
```

Shows all active worktrees for the current project with their branches.

### Manual Cleanup

```bash
# Cleanup worktrees older than 7 days (default)
.claude/skills/worktree-manager/scripts/worktree.sh cleanup

# Custom age threshold
.claude/skills/worktree-manager/scripts/worktree.sh cleanup --days 14
```

## Workflow

### 1. User Requests Worktree

User says: "I want to create a new worktree for developing a staging environment"

### 2. Derive Smart Name

Analyze the request and derive a concise kebab-case name:

- Extract key purpose: "staging environment"
- Convert to kebab-case: `staging-env`

### 3. Create Worktree

```bash
.claude/skills/worktree-manager/scripts/worktree.sh create staging-env
```

### 4. Return Path to User

The script outputs the worktree path. Return it to the user so they can open it in their preferred environment:

```
Worktree created at: ~/ai-worktrees/orient/staging-env-1736639420

pnpm install is running in the background. Check progress with:
tail -f ~/ai-worktrees/orient/staging-env-1736639420/.pnpm-install.log

You can open this worktree in:
- Cursor: File > Open Folder > navigate to path
- Terminal: cd ~/ai-worktrees/orient/staging-env-1736639420
```

## Background Installation

The worktree creation starts `pnpm install` in the background using `nohup`. This means:

- The path is returned immediately (don't wait for pnpm)
- Installation runs async and logs to `.pnpm-install.log`
- User can start working right away
- Dependencies will be available after a few moments

Check if installation is complete:

```bash
# Check if still running
ps aux | grep pnpm

# Watch the log
tail -f <worktree-path>/.pnpm-install.log
```

## Database Seeding (Isolated Mode)

When using `--isolated`, the script automatically:

1. Creates a new SQLite database: `worktree_<timestamp>.db`
2. Updates the worktree's `.env` with the new SQLITE_DB_PATH
3. Pushes schema using Drizzle
4. Seeds the database with test data

Database seeding starts after pnpm install completes. Check progress:

```bash
tail -f <worktree-path>/.db-seed.log
```

### Manual Database Seeding

If you need to seed an existing worktree:

```bash
# Seed with shared database (from .env)
./scripts/seed-worktree-db.sh

# Create isolated database and seed
ISOLATED=true ./scripts/seed-worktree-db.sh
```

## Configuration Files

The script automatically copies configuration files:

**Automatically Available (via git):**

- `.claude/skills/` - All skills are available in worktrees
- `.claude/settings.json` - Committed settings

**Automatically Copied:**

- `.env` - Environment variables for the application
- `.claude/settings.local.json` - Local settings (API keys, preferences)

**Inherited from Main App (not copied):**

- `.cursor/mcp.json` - Cursor MCP configuration
- `.mcp.json` - Root MCP configuration

Cursor inherits MCP settings from the main application, so worktrees have full MCP tool access without copying these files.

## Directory Structure

```
~/ai-worktrees/
└── <project-name>/
    ├── feature-a-1736639420/
    ├── staging-env-1736639421/
    └── fix-bug-1736639422/
```

Each project gets its own subdirectory under `~/ai-worktrees/`.

## Cleanup Policy

- **Automatic:** Runs before each worktree creation
- **Threshold:** Removes worktrees older than 7 days (based on modification time)
- **Safe:** Only removes worktrees in the AI worktree directory
- **Manual:** Can be triggered anytime with `./worktree.sh cleanup`

## .env Configuration Requirements

The `.env` file is copied to worktrees automatically. Ensure proper formatting to avoid shell parsing errors:

### Quote Special Characters

Values with special characters MUST be quoted:

```bash
# Correct - quoted values
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=".dev-data/instance-0/orient.db"
STANDUP_CRON="30 9 * * 1-5"
STANDUP_CHANNEL="#orienter-standups"

# Wrong - unquoted special chars cause shell errors
STANDUP_CRON=30 9 * * 1-5          # Shell expands * as glob
STANDUP_CHANNEL=#orienter-standups  # Shell treats # as comment
```

### Required Variables

For database operations, ensure these are set:

```bash
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=".dev-data/instance-0/orient.db"
```

## Troubleshooting

### pnpm install failed

Check the log:

```bash
cat <worktree-path>/.pnpm-install.log
```

Re-run manually if needed:

```bash
cd <worktree-path>
pnpm install
```

### Config files not copied

Copy manually:

```bash
cp <main-repo>/.env <worktree-path>/.env
cp <main-repo>/.claude/settings.local.json <worktree-path>/.claude/settings.local.json
```

### Database seeding failed

Check the log:

```bash
cat <worktree-path>/.db-seed.log
```

Common issues:

- Database directory not created: `mkdir -p .dev-data/instance-N`
- Invalid SQLITE_DB_PATH: Check quotes and format
- Missing schema: Run `pnpm --filter @orientbot/database run db:push:sqlite` first

### Worktree creation failed

Check git status and ensure:

- You're in a git repository
- Remote is accessible
- No uncommitted changes blocking the operation

## Examples

### Create worktree for a feature

User: "Create a worktree for adding OAuth support"

```bash
.claude/skills/worktree-manager/scripts/worktree.sh create oauth-support
```

### Create worktree for bug fix

User: "I need a worktree to fix the login redirect issue"

```bash
.claude/skills/worktree-manager/scripts/worktree.sh create fix-login-redirect
```

### Create worktree with isolated database

User: "I need a worktree to test new database migrations"

```bash
.claude/skills/worktree-manager/scripts/worktree.sh create test-migrations --isolated
```

### List all worktrees

User: "Show me all my worktrees"

```bash
.claude/skills/worktree-manager/scripts/worktree.sh list
```

### Cleanup old worktrees

User: "Clean up worktrees older than 3 days"

```bash
.claude/skills/worktree-manager/scripts/worktree.sh cleanup --days 3
```
