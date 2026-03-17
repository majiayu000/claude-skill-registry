---
name: worktree-operations
description: Guide for working within git worktrees in the Orient monorepo. Use this skill when you detect you're working in a worktree (path contains "skill-worktrees", "app-worktrees", or is outside the main project directory), when asked to "set up worktree", "install dependencies in worktree", "build in worktree", "merge worktree", or when troubleshooting worktree-specific issues. Covers pnpm/turbo commands, environment setup, git workflows (merging, conflict resolution, cleanup), and common worktree pitfalls.
---

# Worktree Operations

## Detecting a Worktree

You're in a worktree if:

- Path contains `skill-worktrees` or `claude-worktrees` (e.g., `~/claude-worktrees/orienter/my-feature-123456`)
- Path is outside the main project directory but contains project files
- Branch name starts with `skill/` or `worktree/`

Worktrees are isolated checkouts used for skill development without affecting the main checkout.

### Multi-Instance Support

**Worktrees automatically get unique instance IDs** for running multiple bot instances in parallel:

- Main repo: **Instance 0** (original ports)
- Worktrees: **Instance 1-9** (auto-assigned, ports offset by instance_id × 1000)

See the `multi-instance-development` skill for complete details.

### Slack Bot Instance Isolation (CRITICAL)

**Only ONE Slack bot instance can be connected at a time.** Unlike WhatsApp which uses phone-based sessions, Slack uses Socket Mode which means all instances try to connect to the same workspace. Running multiple Slack bots simultaneously causes:

- Connection conflicts and dropped messages
- Duplicate responses
- Session instability

#### Before Testing Slack Features

Always ensure only one Slack bot instance is running:

```bash
# 1. Kill ALL Slack bot processes across all worktrees
pkill -f "tsx.*slack-bot" || true
pkill -f "node.*bot-slack" || true

# 2. Verify no orphaned processes
ps aux | grep -E "slack.*tsx|tsx.*slack" | grep -v grep

# 3. Stop other worktree dev environments
# If you have other worktrees running ./run.sh dev, stop them first:
cd ~/claude-worktrees/other-worktree
./run.sh dev stop

# 4. Start Slack bot in your target worktree only
./run.sh dev
```

#### Checking for Running Slack Instances

```bash
# Quick check: Count Slack bot processes
ps aux | grep -E "slack.*tsx|tsx.*slack|bot-slack" | grep -v grep | wc -l
# Should be 0 before starting, 1-2 after (tsx watch spawns child process)

# Detailed view: See all Slack-related processes
ps aux | grep -E "slack.*tsx|tsx.*slack|bot-slack" | grep -v grep

# Check which ports are in use (Slack doesn't use a port, but check related services)
lsof -i :4099  # OpenCode server
```

#### Killing Orphaned Slack Processes

```bash
# If you see multiple Slack processes or stale processes:

# Option 1: Kill by pattern (recommended)
pkill -f "tsx.*slack-bot"
pkill -f "tsx.*watch.*slack"

# Option 2: Kill specific PIDs
ps aux | grep "slack" | grep -v grep | awk '{print $2}' | xargs kill -9

# Option 3: Use run.sh stop (cleans up properly)
./run.sh dev stop
```

#### Best Practices for Multi-Worktree Development with Slack

1. **Designate one worktree for Slack testing** - Don't run Slack in multiple worktrees
2. **Stop Slack in main repo when testing in worktree** - Run `./run.sh dev stop` in main repo first
3. **Use `--no-slack` flag** when you don't need Slack: `./run.sh dev --no-slack`
4. **Check logs for connection issues**:
   ```bash
   tail -f logs/instance-0/slack-bot.log | grep -E "(connected|error|conflict)"
   ```
5. **Verify single connection** before testing:
   ```bash
   # Should see exactly one "Now connected to Slack" message
   grep "Now connected to Slack" logs/instance-0/slack-bot.log | tail -1
   ```

#### Troubleshooting Slack Connection Issues

**Symptom**: Bot doesn't respond to messages

```bash
# Check if bot is connected
grep -E "(connected|error|disconnect)" logs/instance-0/slack-bot.log | tail -10

# Kill all instances and restart fresh
pkill -f "slack-bot"
sleep 2
./run.sh dev
```

**Symptom**: Duplicate responses or messages lost

```bash
# Multiple bots are likely running - kill all and restart one
pkill -f "tsx.*slack"
./run.sh dev stop  # In ALL worktrees
./run.sh dev       # In ONLY the worktree you want to use
```

**Symptom**: "socket hang up" or connection errors

```bash
# OpenCode server might be down
curl -s http://localhost:4099/global/health || echo "OpenCode not running"

# Restart everything
./run.sh dev stop && ./run.sh dev
```

## Initial Setup (After Worktree Creation)

When a worktree is first created, run these commands:

```bash
# Copy environment from main worktree (already done by cursor worktrees.json)
# cp $ROOT_WORKTREE_PATH/.env .env

# Install dependencies with pnpm (runs automatically via worktrees.json)
pnpm install
```

## Database Setup in Worktrees

Worktrees can use either a **shared database** (default) or an **isolated database** (for schema testing).

### Shared Database (Default)

Uses the same database as your main development environment. No additional setup needed.

```bash
# Your .env already points to the shared dev database
# Just start developing!
pnpm run dev
```

### Isolated Database (For Schema Testing)

When you need a separate database (for migrations, schema changes, or isolated testing):

```bash
# Create isolated database and seed it with test data
ISOLATED=true ./scripts/seed-worktree-db.sh
```

This automatically:

1. Creates a new SQLite database: `.dev-data/worktree_<timestamp>/orient.db`
2. Updates your `.env` with the new SQLITE_DB_PATH
3. Runs all migrations
4. Seeds with:
   - 5 agents (pm-assistant, communicator, scheduler, explorer, app-builder)
   - 6 context rules (platform/environment routing)
   - 6 test permissions (sample WhatsApp and Slack permissions)
   - 4 sample prompts (default system prompts)

### Manual Database Operations

```bash
# Run migrations only
npm run db:migrate

# Seed agents only
npm run agents:seed

# Seed all data (agents + permissions + prompts)
npx tsx data/seeds/index.ts

# Force re-seed (clears existing data first)
npx tsx data/seeds/index.ts --force

# Verify database tables
npm run db:migrate:status
```

### When to Use Isolated Database

Use isolated database when:

- Testing new migrations before merging
- Developing schema changes
- Running destructive tests
- Need a clean database state

Skip isolated database when:

- Normal feature development
- Bug fixes
- Frontend work
- Changes that don't touch the database

## Common Commands (pnpm + turbo)

### Building

```bash
# Build all packages
pnpm run build

# Build a specific package
pnpm --filter @orientbot/core run build
pnpm --filter @orientbot/bot-whatsapp run build

# Build with turbo (uses caching)
pnpm turbo run build
```

### Testing

```bash
# Run all tests
pnpm test

# Run unit tests only
pnpm run test:unit

# Run tests for a specific package
pnpm --filter @orientbot/core run test

# Run with turbo (respects dependencies)
pnpm turbo run test
```

### Running Evals in Worktrees

**Important**: Focused worktrees may lack the full eval runner setup (`src/eval/cli.ts`). Use these alternatives:

#### Option 1: Validate YAML Schema (Always Available)

```bash
# Validate all eval YAML files against schema
npx tsx evals/validate-evals.test.ts

# Or manually with Node.js
node -e "
const yaml = require('js-yaml');
const fs = require('fs');
const data = yaml.load(fs.readFileSync('evals/response-quality/pm-assistant-greeting-no-tools.yaml', 'utf8'));
console.log('✅ Valid YAML:', data.name);
"
```

#### Option 2: JSON Config Validation

```bash
# Validate opencode.json structure and check for tool guidelines
node -e "
const data = JSON.parse(require('fs').readFileSync('opencode.json', 'utf8'));
Object.entries(data.agent || {}).forEach(([name, config]) => {
  const hasGuidelines = (config.prompt || '').includes('Tool Usage Guidelines');
  console.log(name + ': ' + (hasGuidelines ? '✅ Has guidelines' : '⚠️  No guidelines'));
});
"
```

#### Option 3: Full Eval Runner (Requires Full Repo)

If you need the full eval runner:

```bash
# Check if eval CLI exists
ls src/eval/cli.ts 2>/dev/null && echo "✅ Eval runner available" || echo "❌ Eval runner not in this worktree"

# If available, run evals
pnpm eval                    # Run all evals
pnpm eval:fast               # Run with fast matrix
pnpm eval:full               # Run full matrix

# Run specific eval types
pnpm eval -- --type tool_selection
pnpm eval -- --agent pm-assistant
```

#### Option 4: Merge to Full Repo and Test

For comprehensive eval testing:

```bash
# 1. Commit your changes
git add -A && git commit -m "feat: add tool usage guidelines"

# 2. Push to remote
git push origin HEAD

# 3. In the main repo (with full eval setup)
git fetch origin
git checkout your-branch
pnpm install
pnpm eval
```

#### What Each Validation Approach Tests

| Approach         | Tests                                   | Use When                            |
| ---------------- | --------------------------------------- | ----------------------------------- |
| YAML Schema      | YAML syntax, required fields, structure | Quick validation of new evals       |
| JSON Config      | JSON syntax, prompt content             | Checking system instruction changes |
| Full Eval Runner | Actual agent behavior with LLM          | Pre-merge comprehensive testing     |
| Merge & Test     | End-to-end in CI/CD                     | Final validation before deploy      |

### Development

```bash
# Start development mode
pnpm run dev

# Run linting
pnpm run lint
pnpm run lint:fix

# Type checking
pnpm run typecheck
```

## Package Structure

This is a pnpm workspace monorepo with turbo:

```
packages/
├── core/           # Shared utilities and config
├── database/       # Database client and schema
├── mcp-tools/      # MCP tool definitions
├── bot-whatsapp/   # WhatsApp bot
├── bot-slack/      # Slack bot
├── api-gateway/    # API server
├── dashboard/      # Admin dashboard
└── test-utils/     # Testing utilities
```

### Referencing Packages

Use workspace protocol in `package.json`:

```json
{
  "dependencies": {
    "@orientbot/core": "workspace:*",
    "@orientbot/database": "workspace:*"
  }
}
```

## pnpm and Turbo in Monorepos

This section covers pnpm-specific patterns, common issues, and turbo build caching in the monorepo context, especially important for worktree development.

### pnpm Workspace Architecture

**How pnpm Works**:

- Content-addressable store at `~/.pnpm-store`
- Symlinked `node_modules` (not flat like npm)
- Shared dependencies across all worktrees
- Hard links from store to project `node_modules`

**Directory Structure**:

```
project/
├── node_modules/
│   ├── .pnpm/                    # Actual packages (symlinked)
│   ├── @orientbot/core -> .pnpm/...  # Workspace packages
│   └── react -> .pnpm/...        # External packages
├── packages/
│   ├── core/
│   │   └── node_modules/ -> ../../node_modules
│   └── dashboard/
│       └── node_modules/ -> ../../node_modules
└── pnpm-lock.yaml               # Lock file (CRITICAL)
```

### Dependency Installation Patterns

#### Pattern 1: Root Level Dependencies (Shared)

```bash
# Install dependency for all packages
pnpm add -w typescript  # -w = workspace root

# Install dev dependency at root
pnpm add -D -w eslint

# Common use: Build tools, linters, formatters
```

#### Pattern 2: Package-Specific Dependencies

```bash
# Install in specific package
pnpm --filter @orientbot/core add lodash

# Install in package by path
pnpm --filter ./packages/dashboard add express

# Install dev dependency in package
pnpm --filter @orientbot/core add -D jest
```

#### Pattern 3: Frontend Package Dependencies

**Issue Encountered**: Installing UI libraries in nested frontend directories.

```bash
# ❌ WRONG - Installing at root doesn't add to frontend package
pnpm add lucide-react  # Adds to root, not frontend

# ✅ CORRECT - Navigate to frontend and install
cd src/dashboard/frontend
npm install lucide-react  # Uses npm in subdirectory
# OR: pnpm add lucide-react (if package.json exists)

# Return to root and rebuild
cd ../../..
pnpm run build
```

**Alternative**: Use filter from root

```bash
# From monorepo root
pnpm --filter dashboard-frontend add lucide-react

# Or if package name differs:
pnpm --filter "$(cat src/dashboard/frontend/package.json | jq -r .name)" add lucide-react
```

#### Pattern 4: Workspace Protocol Dependencies

```json
// packages/dashboard/package.json
{
  "dependencies": {
    "@orientbot/core": "workspace:*", // Any version
    "@orientbot/database": "workspace:^1.0.0", // Specific range
    "react": "^18.2.0" // External dependency
  }
}
```

**When published to npm**, workspace protocol is replaced with actual version:

```json
{
  "dependencies": {
    "@orientbot/core": "1.2.3" // Resolved version
  }
}
```

### Lock File Management

#### Understanding pnpm-lock.yaml

**Critical File**: `pnpm-lock.yaml` must be committed and kept in sync.

```yaml
lockfileVersion: '6.0'
dependencies:
  '@orientbot/core':
    specifier: workspace:*
    version: link:packages/core
  react:
    specifier: ^18.2.0
    version: 18.2.0
```

**Lock File Rules**:

1. ✅ Commit `pnpm-lock.yaml` to git
2. ✅ Never manually edit lock file
3. ✅ Run `pnpm install` after pulling changes
4. ❌ Don't ignore lock file in `.gitignore`

#### Handling Lock File Conflicts

**Scenario**: Merge conflict in `pnpm-lock.yaml`

**Solution**:

```bash
# During merge conflict
git status  # Shows pnpm-lock.yaml as conflicted

# Option 1: Accept theirs and regenerate (RECOMMENDED)
git checkout --theirs pnpm-lock.yaml
pnpm install  # Regenerates lock file with your changes

# Option 2: Accept ours and reinstall
git checkout --ours pnpm-lock.yaml
pnpm install

# Option 3: Abort merge and rebase instead
git merge --abort
git rebase origin/main  # Often cleaner for lock files

# After resolving
git add pnpm-lock.yaml
git commit --no-edit
```

### Common pnpm Issues in Worktrees

#### Issue 1: .pnpm-install.pid Blocking Operations

**Problem**: Process ID file left over from previous `pnpm install`

**Symptoms**:

- Merge conflicts on `.pnpm-install.pid`
- "Another pnpm install is running"
- File blocks git merge operations

**Solutions**:

```bash
# Before merging branches
rm .pnpm-install.pid
rm -f .pnpm-install.pid  # Force removal

# If locked by process
lsof .pnpm-install.pid  # Find process using file
kill <PID>  # Kill the process
rm .pnpm-install.pid

# Preventive: Add to .gitignore
echo ".pnpm-install.pid" >> .gitignore
git add .gitignore
git commit -m "chore: ignore pnpm install pid file"
```

**During Merge**:

```bash
# Conflict on .pnpm-install.pid
git checkout --theirs .pnpm-install.pid  # Take their version
rm .pnpm-install.pid  # Then delete it
git add .pnpm-install.pid
git commit --no-edit
```

#### Issue 2: node_modules Symlink Confusion

**Problem**: pnpm uses symlinks extensively, can confuse some tools

**Understanding the Structure**:

```bash
# Real packages are in .pnpm
ls -la node_modules/.pnpm/

# Packages symlink to .pnpm
ls -la node_modules/react  # -> .pnpm/react@18.2.0/node_modules/react

# Workspace packages also symlink
ls -la node_modules/@orientbot/core  # -> ../packages/core
```

**Issues This Causes**:

- Some editors don't follow symlinks correctly
- Docker builds may need `--follow-symlinks`
- Jest may need `moduleNameMapper` configuration

**Solutions**:

```javascript
// jest.config.js - Handle pnpm symlinks
module.exports = {
  moduleNameMapper: {
    '^@orientbot/(.*)$': '<rootDir>/packages/$1/src',
  },
  // Or use pnpm's resolution
  resolver: 'jest-pnpm-resolver',
};
```

```dockerfile
# Dockerfile - Copy pnpm structure correctly
COPY pnpm-lock.yaml ./
COPY .npmrc ./
RUN pnpm install --frozen-lockfile

# Copy source (follows symlinks automatically)
COPY packages ./packages
```

#### Issue 3: Workspace Dependencies Not Updating

**Problem**: Changed code in `@orientbot/core` but dashboard doesn't see it

**Cause**: Build artifacts not updated

**Solution**:

```bash
# Rebuild affected packages
pnpm --filter @orientbot/core run build

# Or rebuild everything
pnpm run build

# With turbo (respects dependencies)
pnpm turbo run build

# Force rebuild (ignore cache)
pnpm turbo run build --force
```

#### Issue 4: Phantom Dependencies

**Problem**: Code works locally but fails in CI/CD

**Cause**: Accessing dependency not declared in package.json (phantom dependency)

```typescript
// packages/dashboard/src/app.ts
import lodash from 'lodash'; // Works locally but not in CI!
// Why? @orientbot/core depends on lodash, and pnpm hoists it
```

**Solution**: Declare all direct dependencies

```bash
# Add lodash to dashboard's dependencies
pnpm --filter @orientbot/dashboard add lodash
```

**Prevention**: Use `shamefully-hoist=false` in `.npmrc`

```ini
# .npmrc
shamefully-hoist=false  # Strict mode - no phantom dependencies
```

#### Issue 5: Different pnpm Versions

**Problem**: `pnpm-lock.yaml` shows different version, install fails

**Symptoms**:

```
ERR_PNPM_LOCKFILE_VERSION_MISMATCH
```

**Solution**:

```bash
# Check required version
cat package.json | jq .packageManager
# "pnpm@8.10.0"

# Install correct version globally
npm install -g pnpm@8.10.0

# Or use Corepack (recommended)
corepack enable
corepack prepare pnpm@8.10.0 --activate

# Verify
pnpm --version
```

**Best Practice**: Specify in `package.json`

```json
{
  "packageManager": "pnpm@8.10.0",
  "engines": {
    "pnpm": ">=8.10.0"
  }
}
```

### Turbo Build Caching

#### How Turbo Works

**Concept**: Caches build outputs based on inputs (source files, deps)

```javascript
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],  // Build dependencies first
      "outputs": ["dist/**", "build/**"],  // Cache these
      "inputs": ["src/**", "package.json"]  // Watch these
    },
    "test": {
      "dependsOn": ["build"],  // Test after build
      "outputs": ["coverage/**"],
      "cache": true
    }
  }
}
```

#### Turbo in Worktrees

**Issue**: Turbo cache is worktree-local

```bash
# In worktree A
pnpm turbo run build  # Builds and caches

# Switch to worktree B
cd ~/worktrees/feature-b
pnpm turbo run build  # Rebuilds (different cache)
```

**Workaround**: Share cache between worktrees

```bash
# Set shared cache location
export TURBO_CACHE_DIR=~/.turbo-cache

# Or in package.json scripts
"build": "TURBO_CACHE_DIR=~/.turbo-cache turbo run build"
```

#### Cache Invalidation

**When cache is invalidated**:

- Source files changed
- Dependencies updated
- `package.json` modified
- Env vars in `turbo.json` changed

**Manual cache clearing**:

```bash
# Clear turbo cache
pnpm turbo run build --force  # Bypass cache

# Delete cache directory
rm -rf node_modules/.cache/turbo

# Or use global cache
rm -rf ~/.turbo-cache
```

#### Debugging Turbo

```bash
# See what turbo is doing
pnpm turbo run build --dry-run

# Verbose output
pnpm turbo run build --verbose

# Show cache hits/misses
pnpm turbo run build --summarize

# Why was task not cached?
pnpm turbo run build --dry-run --verbose | grep "cache"
```

### pnpm Commands Reference

#### Installation

```bash
# Install all dependencies (respects lock file)
pnpm install

# Install with frozen lock file (CI mode)
pnpm install --frozen-lockfile

# Install with prefer-offline (faster)
pnpm install --prefer-offline

# Force reinstall everything
pnpm install --force
```

#### Adding Dependencies

```bash
# Add to root workspace
pnpm add -w <package>

# Add to specific package
pnpm --filter <package-name> add <dependency>

# Add to all packages matching pattern
pnpm --filter "./packages/*" add <dependency>

# Add with version constraint
pnpm add react@^18.0.0

# Add from git repo
pnpm add user/repo#branch
```

#### Removing Dependencies

```bash
# Remove from specific package
pnpm --filter <package-name> remove <dependency>

# Remove from workspace root
pnpm remove -w <package>

# Prune orphaned packages
pnpm prune
```

#### Updating Dependencies

```bash
# Update all packages
pnpm update

# Update specific package
pnpm update react

# Update to latest (ignore semver)
pnpm update --latest react

# Check for outdated packages
pnpm outdated
```

#### Workspace Commands

```bash
# Run script in all packages
pnpm -r run build  # -r = recursive

# Run in specific package
pnpm --filter @orientbot/core run test

# Run in packages matching glob
pnpm --filter "./packages/bot-*" run start

# Run with dependencies first
pnpm --filter @orientbot/dashboard... run build
# ... = include dependencies
```

### Best Practices for pnpm in Worktrees

1. **✅ Keep lock file in sync**

   ```bash
   # After every pull
   git pull origin main
   pnpm install
   ```

2. **✅ Clean install for stale worktrees**

   ```bash
   # For old worktrees
   rm -rf node_modules
   rm pnpm-lock.yaml
   git checkout main -- pnpm-lock.yaml
   pnpm install
   ```

3. **✅ Use consistent pnpm version**

   ```json
   {
     "packageManager": "pnpm@8.10.0"
   }
   ```

4. **✅ Ignore temporary files**

   ```gitignore
   # .gitignore
   .pnpm-install.pid
   .pnpm-debug.log
   node_modules/.cache/
   ```

5. **✅ Understand workspace dependencies**

   ```bash
   # See dependency tree
   pnpm list --depth 1

   # See why package is installed
   pnpm why lodash
   ```

6. **✅ Use filters for focused work**

   ```bash
   # Build only dashboard and its deps
   pnpm --filter @orientbot/dashboard... run build

   # Test only changed packages (with turbo)
   pnpm turbo run test --filter=[HEAD^1]
   ```

7. **✅ Handle lock file conflicts properly**

   ```bash
   # Don't manually resolve - regenerate
   git checkout --theirs pnpm-lock.yaml
   pnpm install
   git add pnpm-lock.yaml
   ```

8. **✅ Clean up before merging**

   ```bash
   # Remove temporary files
   rm .pnpm-install.pid
   rm -rf node_modules/.cache

   # Ensure clean state
   pnpm install
   pnpm run build
   git status  # Should be clean
   ```

9. **❌ Don't mix npm and pnpm**

   ```bash
   # Bad
   npm install  # Creates package-lock.json
   pnpm install  # Conflicts with npm

   # Good
   pnpm install  # Consistent tool
   ```

10. **❌ Don't commit node_modules**
    ```gitignore
    # .gitignore
    node_modules/
    .pnpm-store/
    ```

### Troubleshooting pnpm Issues

**"EBUSY: resource busy or locked"**

```bash
# Kill pnpm processes
pkill -f pnpm
rm .pnpm-install.pid
pnpm install
```

**"Cannot find module '@orientbot/core'"**

```bash
# Rebuild workspace packages
pnpm --filter @orientbot/core run build
# Or rebuild all
pnpm run build
```

**"integrity check failed"**

```bash
# Lock file out of sync
rm pnpm-lock.yaml
pnpm install
git add pnpm-lock.yaml
```

**"Package 'X' not found"**

```bash
# Clear store and reinstall
pnpm store prune
rm -rf node_modules
pnpm install
```

**"peer dependencies not met"**

```bash
# Install missing peer dependencies
pnpm install <peer-dep>
# Or use --force to ignore
pnpm install --force
```

## React Frontend Development in Monorepos

This section covers React-specific patterns for building frontend components in the monorepo, based on lessons from implementing the miniapp editor UI.

### Frontend Package Structure

**Typical Frontend Package Layout**:

```
src/dashboard/frontend/
├── src/
│   ├── components/           # React components
│   │   ├── AppsTab.tsx      # Main tab components
│   │   └── MiniAppEditor/   # Feature-specific components
│   │       ├── MiniAppEditorModal.tsx
│   │       ├── AppEditorForm.tsx
│   │       ├── GenerationProgress.tsx
│   │       └── PreviewPanel.tsx
│   ├── api.ts               # API client functions
│   ├── App.tsx              # Root component
│   └── main.tsx             # Entry point
├── package.json             # Frontend dependencies
├── vite.config.ts           # Build configuration
├── tailwind.config.js       # Tailwind CSS config
└── tsconfig.json            # TypeScript config
```

### Installing Frontend Dependencies

**Critical Pattern**: Navigate to frontend package directory before installing UI libraries.

#### Pattern 1: Install in Frontend Package (Recommended)

```bash
# From monorepo root
cd src/dashboard/frontend

# Install UI library
npm install lucide-react
# or: pnpm add lucide-react

# Verify it's in package.json
cat package.json | grep lucide-react

# Return to root and rebuild
cd ../../..
pnpm run build
```

**Why This Works**:

- Adds dependency to correct `package.json`
- Frontend build includes the package
- No confusion about where dependency lives

#### Pattern 2: Use pnpm Filter (Advanced)

```bash
# From monorepo root
pnpm --filter dashboard-frontend add lucide-react

# Or by path
pnpm --filter ./src/dashboard/frontend add lucide-react
```

**Common Mistake**:

```bash
# ❌ WRONG - Installs at root, not in frontend
pnpm add lucide-react

# Frontend build fails:
# Error: Cannot find module 'lucide-react'
```

### Component Creation Patterns

#### Pattern 1: Feature-Based Component Organization

**Create Feature Directory**:

```bash
mkdir -p src/dashboard/frontend/src/components/MiniAppEditor
```

**Component Structure** (MiniAppEditorModal.tsx example):

```typescript
// 1. Imports - External first, then internal
import { useState, useEffect } from 'react';
import { X, ExternalLink } from 'lucide-react';
import { editApp, buildApp, getHistory } from '../../api';

// 2. Type Definitions
interface MiniAppEditorModalProps {
  appName: string;
  createNew?: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

interface EditSession {
  sessionId: string;
  portalUrl: string;
  commitHash: string;
}

// 3. Component
export default function MiniAppEditorModal({
  appName,
  createNew = false,
  onClose,
  onSuccess,
}: MiniAppEditorModalProps) {
  // 4. State Management
  const [session, setSession] = useState<EditSession | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 5. Effects
  useEffect(() => {
    // Load initial data
  }, [appName]);

  // 6. Event Handlers
  const handleSubmit = async (prompt: string) => {
    setIsGenerating(true);
    try {
      const response = await editApp(appName, prompt, createNew);
      setSession({
        sessionId: response.sessionId,
        portalUrl: response.portalUrl,
        commitHash: response.commitHash,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Generation failed');
    } finally {
      setIsGenerating(false);
    }
  };

  // 7. Render
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl w-full max-w-6xl h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold">Edit with AI: {appName}</h2>
          <button onClick={onClose}>
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden">
          {/* Component content */}
        </div>
      </div>
    </div>
  );
}
```

#### Pattern 2: Reusable Form Components

**Form Component** (AppEditorForm.tsx):

```typescript
import { useState, FormEvent } from 'react';
import { Sparkles } from 'lucide-react';

interface AppEditorFormProps {
  onSubmit: (prompt: string) => void;
  disabled?: boolean;
  initialPrompt?: string;
}

export default function AppEditorForm({
  onSubmit,
  disabled = false,
  initialPrompt = '',
}: AppEditorFormProps) {
  const [prompt, setPrompt] = useState(initialPrompt);
  const minLength = 10;
  const isValid = prompt.trim().length >= minLength;

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (isValid && !disabled) {
      onSubmit(prompt.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">
          Describe what you want to create or change
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="E.g., Create a todo list app with add, complete, and delete features..."
          className="w-full h-32 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
          disabled={disabled}
        />
        <p className="text-sm text-gray-500 mt-2">
          Characters: {prompt.length} / {minLength} minimum
        </p>
      </div>

      <button
        type="submit"
        disabled={!isValid || disabled}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <Sparkles className="h-5 w-5" />
        {disabled ? 'Generating...' : 'Generate Code'}
      </button>
    </form>
  );
}
```

### TypeScript Component Typing

#### Best Practices

**1. Props Interface**:

```typescript
// ✅ GOOD - Explicit interface
interface ComponentProps {
  id: string;
  name: string;
  optional?: boolean;
  onEvent: (data: string) => void;
}

export default function Component(props: ComponentProps) {
  // ...
}

// ❌ BAD - Inline types
export default function Component({ id, name }: { id: string; name: string }) {
  // Hard to reuse, hard to read
}
```

**2. State Typing**:

```typescript
// ✅ GOOD - Explicit state types
interface User {
  id: string;
  name: string;
  email: string;
}

const [user, setUser] = useState<User | null>(null);
const [users, setUsers] = useState<User[]>([]);
const [loading, setLoading] = useState<boolean>(false);

// ❌ BAD - Implicit any
const [data, setData] = useState(null); // type: null
```

**3. Event Handlers**:

```typescript
// ✅ GOOD - Typed event handlers
import { FormEvent, ChangeEvent } from 'react';

const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  // ...
};

const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

// ❌ BAD - Untyped
const handleSubmit = (e) => {
  // implicitly any
  e.preventDefault();
};
```

**4. Children Props**:

```typescript
import { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode; // ✅ Accepts any React content
}

// Or more specific:
interface ButtonProps {
  children: string; // ✅ Only accepts string
}
```

### Icon Library Integration (lucide-react)

#### Installation

```bash
cd src/dashboard/frontend
npm install lucide-react
```

#### Usage Patterns

**Import Icons**:

```typescript
import {
  X, // Close icon
  Check, // Checkmark
  Loader2, // Spinner
  AlertCircle, // Error
  ExternalLink, // External link
  RefreshCw, // Refresh
  GitCommit, // Git commit
  Sparkles, // AI/magic
} from 'lucide-react';
```

**Icon Sizing**:

```tsx
{
  /* Small icon (16px) */
}
<X className="h-4 w-4" />;

{
  /* Medium icon (20px) */
}
<Check className="h-5 w-5" />;

{
  /* Large icon (24px) */
}
<Loader2 className="h-6 w-6" />;
```

**Animated Icons**:

```tsx
{
  /* Spinning loader */
}
<Loader2 className="h-5 w-5 animate-spin" />;

{
  /* Bouncing dots */
}
<div className="flex gap-1">
  <div
    className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
    style={{ animationDelay: '0ms' }}
  />
  <div
    className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
    style={{ animationDelay: '150ms' }}
  />
  <div
    className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
    style={{ animationDelay: '300ms' }}
  />
</div>;
```

**Icon Colors**:

```tsx
{
  /* Text color */
}
<AlertCircle className="h-5 w-5 text-red-500" />;

{
  /* Hover color */
}
<X className="h-5 w-5 text-gray-400 hover:text-gray-600" />;

{
  /* Dark mode */
}
<Check className="h-5 w-5 text-gray-700 dark:text-gray-300" />;
```

### Tailwind CSS Configuration

#### Setup

**tailwind.config.js**:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class', // Enable dark mode with class
  theme: {
    extend: {
      colors: {
        // Custom colors
        'brand-purple': {
          50: '#f5f3ff',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
        },
      },
    },
  },
  plugins: [],
};
```

#### Common Patterns

**Layout**:

```tsx
{
  /* Flexbox layout */
}
<div className="flex items-center justify-between gap-4">
  <div className="flex-1">Content</div>
  <button>Action</button>
</div>;

{
  /* Grid layout */
}
<div className="grid grid-cols-2 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
</div>;

{
  /* Responsive grid */
}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Scales with screen size */}
</div>;
```

**Modals**:

```tsx
{
  /* Modal overlay */
}
<div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
  {/* Modal content */}
  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl w-full max-w-4xl">
    <div className="p-6">{/* Content */}</div>
  </div>
</div>;
```

**Forms**:

```tsx
{
  /* Input field */
}
<input
  type="text"
  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
/>;

{
  /* Textarea */
}
<textarea className="w-full h-32 px-4 py-3 border rounded-lg resize-none" />;

{
  /* Button */
}
<button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
  Submit
</button>;
```

**Dark Mode**:

```tsx
{
  /* Colors that adapt */
}
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
  <p className="text-gray-600 dark:text-gray-400">Description</p>
</div>;

{
  /* Borders */
}
<div className="border border-gray-200 dark:border-gray-700">Content</div>;
```

### State Management with Hooks

#### useState Patterns

**Simple State**:

```typescript
const [count, setCount] = useState(0);
const [name, setName] = useState('');
const [isLoading, setIsLoading] = useState(false);
```

**Complex State**:

```typescript
interface FormState {
  name: string;
  email: string;
  errors: Record<string, string>;
}

const [form, setForm] = useState<FormState>({
  name: '',
  email: '',
  errors: {},
});

// Update single field
setForm((prev) => ({ ...prev, name: 'John' }));

// Update nested property
setForm((prev) => ({
  ...prev,
  errors: { ...prev.errors, name: 'Required' },
}));
```

**Array State**:

```typescript
const [items, setItems] = useState<string[]>([]);

// Add item
setItems((prev) => [...prev, 'new item']);

// Remove item
setItems((prev) => prev.filter((item) => item !== 'remove this'));

// Update item
setItems((prev) => prev.map((item) => (item === 'old' ? 'new' : item)));
```

#### useEffect Patterns

**Fetch Data on Mount**:

```typescript
useEffect(() => {
  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await api.getData();
      setData(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  fetchData();
}, []); // Empty deps = run once on mount
```

**Sync with Props**:

```typescript
useEffect(() => {
  // When appName changes, reload data
  loadAppData(appName);
}, [appName]);
```

**Cleanup**:

```typescript
useEffect(() => {
  const interval = setInterval(() => {
    checkStatus();
  }, 5000);

  return () => clearInterval(interval); // Cleanup on unmount
}, []);
```

#### Custom Hooks

**Example: useAsync**:

```typescript
function useAsync<T>(asyncFn: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const execute = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await asyncFn();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, execute };
}

// Usage
const { data, loading, error, execute } = useAsync(() => editApp(appName, prompt));
```

### Component Integration Patterns

#### Integrating into Existing Components

**Example: Adding Modal to AppsTab**:

```typescript
// AppsTab.tsx
import { useState } from 'react';
import MiniAppEditorModal from './MiniAppEditor/MiniAppEditorModal';

export default function AppsTab() {
  const [apps, setApps] = useState<App[]>([]);
  const [showEditorModal, setShowEditorModal] = useState(false);
  const [editorAppName, setEditorAppName] = useState('');

  const handleEditClick = (appName: string) => {
    setEditorAppName(appName);
    setShowEditorModal(true);
  };

  const handleSuccess = () => {
    setShowEditorModal(false);
    loadApps(); // Reload apps after successful edit
  };

  return (
    <div>
      {/* Existing table */}
      <table>
        {apps.map(app => (
          <tr key={app.name}>
            <td>{app.name}</td>
            <td>
              <button onClick={() => handleEditClick(app.name)}>
                Edit with AI
              </button>
            </td>
          </tr>
        ))}
      </table>

      {/* Modal (rendered conditionally) */}
      {showEditorModal && (
        <MiniAppEditorModal
          appName={editorAppName}
          onClose={() => setShowEditorModal(false)}
          onSuccess={handleSuccess}
        />
      )}
    </div>
  );
}
```

### Build and Dev Server Patterns

#### Vite Configuration

**vite.config.ts**:

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:4098',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
        },
      },
    },
  },
});
```

#### Package Scripts

**package.json**:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "typecheck": "tsc --noEmit",
    "lint": "eslint src --ext ts,tsx"
  }
}
```

#### Development Workflow

**From Monorepo Root**:

```bash
# Start frontend dev server
cd src/dashboard/frontend
npm run dev

# In another terminal, start backend
cd ../../..
pnpm --filter dashboard run dev

# Or use monorepo script
pnpm run dev  # Starts all services
```

**From Frontend Directory**:

```bash
cd src/dashboard/frontend

# Install new dependency
npm install lucide-react

# Build
npm run build

# Type check
npm run typecheck

# Return to root
cd ../../..
```

### Frontend-Specific Build Artifacts

#### What Gets Generated

```
src/dashboard/frontend/
├── dist/                  # Build output (gitignore)
│   ├── index.html
│   ├── assets/
│   │   ├── index-abc123.js
│   │   └── index-xyz789.css
│   └── favicon.ico
├── node_modules/          # Dependencies (gitignore)
└── .vite/                 # Vite cache (gitignore)
```

#### Gitignore Patterns

```gitignore
# Frontend build artifacts
**/dist/
**/build/
**/.vite/

# Dependencies
node_modules/

# Environment
.env.local
.env.*.local

# Editor
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### Common Frontend Issues in Monorepos

#### Issue 1: Icon Library Not Found

**Problem**: `Cannot find module 'lucide-react'`

**Cause**: Installed at wrong level

**Solution**:

```bash
# Navigate to frontend package
cd src/dashboard/frontend

# Install there
npm install lucide-react

# Verify
cat package.json | grep lucide-react

# Rebuild
cd ../../..
pnpm run build
```

#### Issue 2: TypeScript Errors in Components

**Problem**: `Property 'X' does not exist on type 'Y'`

**Solution**: Add proper types

```typescript
// Define interface for props
interface Props {
  appName: string;
  onClose: () => void;
}

// Use in component
export default function Component({ appName, onClose }: Props) {
  // TypeScript now knows the types
}
```

#### Issue 3: Styles Not Applied

**Problem**: Tailwind classes don't work

**Cause**: Content paths not configured

**Solution**: Update `tailwind.config.js`

```javascript
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}', // ✅ Include all files
  ],
  // ...
};
```

#### Issue 4: Hot Reload Not Working

**Problem**: Changes don't reflect in browser

**Solutions**:

```bash
# Restart dev server
Ctrl+C
npm run dev

# Clear Vite cache
rm -rf .vite
npm run dev

# Check proxy configuration in vite.config.ts
```

### Best Practices Summary

1. **✅ Install frontend deps in frontend package directory**
2. **✅ Use TypeScript interfaces for all component props**
3. **✅ Organize components by feature, not type**
4. **✅ Use Tailwind for styling (consistent design system)**
5. **✅ Import icons from lucide-react (tree-shakeable)**
6. **✅ Manage state with useState/useEffect patterns**
7. **✅ Create custom hooks for reusable logic**
8. **✅ Use dark mode classes for theme support**
9. **✅ Proxy API calls through Vite dev server**
10. **✅ Build frontend before committing (catch type errors)**

## Critical Monorepo Code Organization

### Where to Place Code

**Root `src/` vs Package-Specific `packages/*/src/`**

Place code in **root `src/`** when:

- ✅ Services are shared across multiple packages
- ✅ Utilities need to be imported by different packages
- ✅ You want to avoid TypeScript rootDir conflicts

Place code in **`packages/*/src/`** when:

- ✅ Code is specific to that package only
- ✅ It's a UI component for a frontend package
- ✅ It's package-specific business logic

**Example from miniapp editor implementation:**

```
✅ CORRECT:
src/services/miniappEditService.ts     # Shared across packages
src/services/miniappEditDatabase.ts    # Used by dashboard and potentially others
packages/dashboard/src/server/routes/apps.routes.ts  # Dashboard-specific routes

❌ INCORRECT:
packages/dashboard/src/services/miniappEditService.ts  # Causes TS6059 errors!
```

### Import Path Patterns

When importing from root `src/` into packages:

```typescript
// From packages/dashboard/src/server/index.ts
import { createMiniappEditService } from '../../../../src/services/miniappEditService.js';
import { createMiniappEditDatabase } from '../../../../src/services/miniappEditDatabase.js';
import { createAppGitService } from '../../../../src/services/appGitService.js';
```

**Key Rules:**

1. Use relative paths with `../../../../src/` to go up from package to root
2. Always include `.js` extension in imports (ESM requirement)
3. Count directory levels: `packages/dashboard/src/server/` needs 4 levels up

### TypeScript Configuration Pitfalls

**❌ ERROR: TS6059 - File is not under 'rootDir'**

This happens when you try to import files from outside a package's configured rootDir:

```
Error: File '/Users/.../src/services/appGitService.ts' is not under 'rootDir'
'/Users/.../packages/dashboard/src'
```

**✅ SOLUTION:**

- Move shared services to root `src/` directory
- Or add the file to the package's TypeScript compilation scope
- Use relative imports instead of package aliases for cross-boundary imports

### API Client Function Names

When adding frontend API functions, **always verify the correct function name**:

```typescript
// ❌ WRONG - fetchAPI doesn't exist
return fetchAPI(`/apps/${appName}/edit`, {...});

// ✅ CORRECT - use apiRequest (the authenticated request function)
return apiRequest(`/apps/${appName}/edit`, {...});
```

**How to verify:**

1. Read `src/dashboard/frontend/src/api.ts` to see existing patterns
2. Look for the authenticated request wrapper (usually `apiRequest` or `api`)
3. Never assume function names - always check first

## Monorepo Service Layer Patterns

### Service Architecture Overview

The Orient uses a layered service architecture where services are initialized in the dashboard server and passed to route handlers. This pattern enables:

- Dependency injection for testing
- Graceful degradation if services fail to initialize
- Clear separation of concerns
- Reusable service instances

### Service Initialization Pattern

**Location**: `packages/dashboard/src/server/index.ts`

All services are initialized in the `initializeServices()` function with a consistent pattern:

```typescript
async function initializeServices(): Promise<DashboardServices> {
  // Core services (required)
  const database = createDatabase(databaseUrl);
  await database.initialize();

  // Optional services wrapped in try-catch
  let miniappEditService: MiniappEditService | undefined;
  try {
    // 1. Initialize dependencies
    const miniappEditDb = createMiniappEditDatabase(databaseUrl);
    await miniappEditDb.initialize();

    const appGitService = createAppGitService({
      repoPath: process.env.REPO_PATH || process.cwd(),
      worktreeBase: process.env.APP_WORKTREES_PATH,
    });

    const openCodeClient = createOpenCodeClient(
      process.env.OPENCODE_SERVER_URL || 'http://localhost:4099',
      process.env.OPENCODE_DEFAULT_MODEL
    );

    // 2. Create service with dependencies
    miniappEditService = createMiniappEditService({
      appGitService,
      openCodeClient,
      database: miniappEditDb,
      portalBaseUrl: process.env.OPENCODE_PORTAL_URL || 'http://localhost:4099',
    });

    logger.info('Miniapp edit service initialized');
  } catch (error) {
    // 3. Log warning but don't crash server
    logger.warn('Failed to initialize miniapp edit service', { error });
  }

  return {
    database,
    miniappEditService,
    // ... other services
  };
}
```

### Key Service Integration Steps

#### 1. Define Service in DashboardServices Type

**Location**: `packages/dashboard/src/server/types.ts` (or wherever types are defined)

```typescript
export interface DashboardServices {
  database: Database;
  miniappEditService?: MiniappEditService; // Optional with ?
  // ... other services
}
```

#### 2. Add Service Factory Functions

Service factories should be in root `src/services/`:

```typescript
// src/services/miniappEditService.ts
export function createMiniappEditService(config: MiniappEditServiceConfig): MiniappEditService {
  return new MiniappEditServiceImpl(config);
}

// src/services/miniappEditDatabase.ts
export function createMiniappEditDatabase(connectionString: string): MiniappEditDatabase {
  return new MiniappEditDatabaseImpl(connectionString);
}
```

#### 3. Initialize in Dashboard Server

**Pattern**: Try-catch wrapping prevents cascading failures

```typescript
// In initializeServices()
let myNewService: MyNewService | undefined;
try {
  // Initialize dependencies first
  const dependency1 = createDependency1();
  const dependency2 = createDependency2();

  // Create service
  myNewService = createMyNewService({
    dependency1,
    dependency2,
    config: process.env.MY_CONFIG,
  });

  logger.info('My new service initialized');
} catch (error) {
  logger.warn('Failed to initialize my new service', { error });
  // Service remains undefined - server continues without it
}

return { myNewService, ...otherServices };
```

#### 4. Mount Routes Conditionally

**Location**: `packages/dashboard/src/server/routes.ts`

```typescript
export function createDashboardRouter(services: DashboardServices): Router {
  const { miniappEditService } = services;

  // Only mount routes if service initialized
  if (miniappEditService) {
    router.use('/apps', createAppsRoutes(miniappEditService, requireAuth));
    logger.info('Apps routes mounted');
  } else {
    logger.warn('Miniapp edit service not available - routes not mounted');
  }

  return router;
}
```

### Environment Variable Requirements

Services typically require environment variables. Document them clearly:

**For Miniapp Edit Service:**

```bash
# Required for miniapp editing feature
OPENCODE_SERVER_URL=http://localhost:4099       # OpenCode API endpoint
OPENCODE_PORTAL_URL=http://localhost:4099       # OpenCode web portal
REPO_PATH=/path/to/repo                         # Git repository path (defaults to cwd)
APP_WORKTREES_PATH=~/app-worktrees              # Where to create worktrees

# Optional
OPENCODE_DEFAULT_MODEL=claude-sonnet-4-5        # AI model to use
```

**For Other Services:**

```bash
# AppGitService
REPO_PATH=/path/to/repo                         # Git repository root
APP_WORKTREES_PATH=~/app-worktrees              # Worktree storage location

# OpenCodeClient
OPENCODE_SERVER_URL=http://localhost:4099       # API endpoint
OPENCODE_DEFAULT_MODEL=claude-sonnet-4-5        # Model identifier
```

### Service Dependency Graph

```
MiniappEditService
    ↓
    ├─→ AppGitService
    │       ↓
    │       └─→ Git Repository (filesystem)
    │
    ├─→ OpenCodeClient
    │       ↓
    │       └─→ OpenCode Server (HTTP)
    │
    └─→ MiniappEditDatabase
            ↓
            └─→ SQLite (file)
```

**Initialization Order**:

1. Initialize leaf dependencies first (database, git, API clients)
2. Then initialize services that depend on them
3. Finally, mount routes that use the services

### Troubleshooting Service Initialization

#### Problem: Service fails to initialize silently

**Symptom**: Routes return 404, no error messages

**Debug Steps**:

```bash
# 1. Check server logs for initialization warnings
grep "Failed to initialize" logs/dashboard.log

# 2. Verify environment variables are set
echo $OPENCODE_SERVER_URL
echo $REPO_PATH

# 3. Test service dependencies independently
curl $OPENCODE_SERVER_URL/health
sqlite3 "$SQLITE_DB_PATH" "SELECT 1"
ls -la $REPO_PATH
```

**Common Causes**:

- Missing environment variables
- Service endpoint unreachable
- Database connection failed
- File system permissions

#### Problem: Try-catch swallows useful error details

**Solution**: Enhance error logging

```typescript
try {
  miniappEditService = createMiniappEditService(config);
  logger.info('Service initialized');
} catch (error) {
  // Log full error details
  logger.error('Service initialization failed', {
    error: error instanceof Error ? error.message : String(error),
    stack: error instanceof Error ? error.stack : undefined,
    config: {
      openCodeUrl: process.env.OPENCODE_SERVER_URL,
      repoPath: process.env.REPO_PATH,
      // Don't log sensitive values
    },
  });
}
```

#### Problem: Service initialized but routes don't work

**Symptom**: Service logs "initialized" but API calls fail

**Debug Steps**:

```typescript
// In routes.ts, add debug logging
if (miniappEditService) {
  logger.debug('Mounting apps routes with service', {
    serviceType: miniappEditService.constructor.name,
    hasDatabase: !!miniappEditService.database,
  });
  router.use('/apps', createAppsRoutes(miniappEditService, requireAuth));
} else {
  logger.warn('Service is undefined - routes not mounted');
}
```

#### Problem: Cascading initialization failures

**Symptom**: One service failure prevents others from initializing

**Solution**: Isolate each service initialization in its own try-catch

```typescript
// ❌ BAD - All services fail if one fails
try {
  const service1 = createService1();
  const service2 = createService2();
  const service3 = createService3();
} catch (error) {
  logger.error('Service initialization failed', { error });
}

// ✅ GOOD - Each service fails independently
let service1, service2, service3;

try {
  service1 = createService1();
  logger.info('Service1 initialized');
} catch (error) {
  logger.warn('Service1 failed', { error });
}

try {
  service2 = createService2();
  logger.info('Service2 initialized');
} catch (error) {
  logger.warn('Service2 failed', { error });
}

try {
  service3 = createService3();
  logger.info('Service3 initialized');
} catch (error) {
  logger.warn('Service3 failed', { error });
}
```

### Testing Service Integration

#### Unit Testing Services

```typescript
// test-miniapp-edit.ts
import { createMiniappEditDatabase } from './services/miniappEditDatabase';

async function testService() {
  const db = createMiniappEditDatabase(process.env.SQLITE_DB_PATH!);
  await db.initialize();

  const session = await db.createSession({
    id: 'test-1',
    appName: 'test-app',
    sessionId: 'test-session-1',
    worktreePath: '/tmp/worktree',
    branchName: 'test-branch',
  });

  console.log('✅ Session created:', session);
  await db.close();
}

testService().catch(console.error);
```

#### Integration Testing APIs

```bash
# test-api-routes.sh
TOKEN=$(curl -X POST http://localhost:4098/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' \
  | jq -r '.token')

# Test service endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:4098/api/apps/sessions/active

# Should return:
# {"success":true,"sessions":[]}
```

### Best Practices Summary

1. **✅ Place shared services in root `src/services/`** - Avoids TypeScript rootDir errors
2. **✅ Wrap initialization in try-catch** - Prevents cascading failures
3. **✅ Mark optional services with `?` in types** - Makes optionality explicit
4. **✅ Conditionally mount routes** - Check service exists before mounting
5. **✅ Log initialization status** - Both success and failure cases
6. **✅ Document environment variables** - In README and skill docs
7. **✅ Provide fallback defaults** - Use `process.env.VAR || 'default'`
8. **✅ Test services independently** - Unit tests before integration tests
9. **✅ Use factory functions** - Easier to mock for testing
10. **✅ Follow dependency injection** - Pass dependencies to constructors

### Database Service Integration for Bots

**Critical Pattern**: When integrating services like PromptService into bot entry points, you must understand which database types implement which interfaces.

#### Understanding Database Type Requirements

**The Key Concept**: Different services require different database interfaces. Using the wrong database type will cause TypeScript compilation errors.

**Common TypeScript Error**:

```typescript
// ❌ WRONG - TypeScript compilation error
import { createSlackDatabase, createPromptService } from '@orientbot/database-services';

const slackDatabase = createSlackDatabase();
const promptService = createPromptService(slackDatabase); // ERROR!

// Error: Argument of type 'SlackDatabase' is not assignable to parameter of type 'PromptDatabaseInterface'.
// Type 'SlackDatabase' is missing properties: getSystemPromptText, getSystemPrompt, setSystemPrompt, deleteSystemPrompt, etc.
```

**Why This Fails**:

- `PromptService` requires a database implementing `PromptDatabaseInterface`
- `SlackDatabase` implements `SlackDatabaseInterface` (platform-specific operations)
- `MessageDatabase` implements `PromptDatabaseInterface` (cross-platform operations including prompts)

#### Correct Pattern: Using MessageDatabase

**Bot Entry Point Pattern** (`packages/bot-slack/src/main.ts`):

```typescript
import { createSlackBotService } from './services/index.js';
import { createServiceLogger, loadConfig, getConfig } from '@orientbot/core';
import {
  createSecretsService,
  createSlackDatabase, // Platform-specific database
  createMessageDatabase, // Cross-platform database (for prompts)
  createPromptService,
} from '@orientbot/database-services';

const logger = createServiceLogger('slack-bot');

async function main(): Promise<void> {
  try {
    // ... config loading ...

    // Initialize BOTH databases
    const slackDatabase = createSlackDatabase(); // For Slack-specific data
    const messageDatabase = createMessageDatabase(); // For cross-platform data

    // PromptService uses MessageDatabase (implements PromptDatabaseInterface)
    const promptService = createPromptService(messageDatabase);
    logger.info('Prompt service initialized');

    // Create bot with platform-specific database
    const slackBot = createSlackBotService(config, slackDatabase);

    // Attach prompt service to bot
    slackBot.setPromptService(promptService);
    logger.info('Prompt service configured for Slack bot');

    await slackBot.start();
  } catch (error) {
    logger.error('Failed to start Slack Bot', { error });
    process.exit(1);
  }
}
```

#### Why Multiple Databases?

**Database Separation by Concern**:

```
Platform-Specific Databases:
├─ SlackDatabase
│  ├─ slack_channels (Slack channel metadata)
│  ├─ slack_messages (Slack-specific message fields)
│  └─ slack_threads (thread tracking)
│
└─ WhatsAppDatabase
   ├─ whatsapp_contacts (contact info)
   ├─ whatsapp_groups (group metadata)
   └─ whatsapp_media (media references)

Cross-Platform Database:
└─ MessageDatabase (implements PromptDatabaseInterface)
   ├─ messages (normalized cross-platform messages)
   ├─ system_prompts (shared prompts for all platforms)
   └─ message_context (conversation context)
```

**Design Rationale**:

- **Prompts are cross-platform**: Same prompt system works for Slack, WhatsApp, Discord, etc.
- **Platform-specific data stays isolated**: Slack threads don't mix with WhatsApp groups
- **Services use appropriate database**: PromptService → MessageDatabase, SlackService → SlackDatabase

#### Verifying Service Initialization in Logs

After starting a bot, verify services initialized correctly by checking logs:

**Log File Location**:

```bash
# For Slack bot
tail -f logs/instance-9/slack-dev.log

# For WhatsApp bot
tail -f logs/instance-9/whatsapp-dev.log
```

**Expected Log Sequence**:

```
2026-01-19 06:27:14.601 [INFO] [slack-db] Slack database initialized
  → {
    "databasePath": ".dev-data/instance-9/orient.db"
  }

2026-01-19 06:27:14.601 [INFO] [message-db] Database initialized
  → {
    "databasePath": ".dev-data/instance-9/orient.db"
  }

2026-01-19 06:27:14.602 [INFO] [prompt-service] Prompt service initialized
  → {
    "cacheEnabled": true
  }

2026-01-19 06:27:14.602 [INFO] [slack-bot] Prompt service initialized

2026-01-19 06:27:14.621 [INFO] [slack-bot] Prompt service configured for Slack bot

2026-01-19 06:27:15.327 [INFO] [slack-bot] Slack Bot is ready!
```

**Key Log Indicators**:

1. ✅ `[slack-db] Slack database pool created` - Platform database initialized
2. ✅ `[message-db] Database pool created` - Cross-platform database initialized
3. ✅ `[prompt-service] Prompt service initialized` - Service created successfully
4. ✅ `[slack-bot] Prompt service configured` - Service attached to bot
5. ✅ `[slack-bot] Slack Bot is ready!` - Bot fully operational

**Missing Log Indicators** (problems):

```bash
# If you see this but NOT the message-db/prompt-service logs:
[INFO] [slack-bot] Starting Slack Bot...
[INFO] [slack-db] Slack database pool created
[ERROR] [slack-bot] Failed to handle message: Cannot read property 'getSystemPromptText' of undefined

# Cause: PromptService was never initialized in main.ts
```

#### Common Mistakes and Fixes

**Mistake 1: Using Platform Database Instead of MessageDatabase**

```typescript
// ❌ WRONG - TypeScript error
const slackDatabase = createSlackDatabase();
const promptService = createPromptService(slackDatabase);

// Error: Type 'SlackDatabase' is not assignable to 'PromptDatabaseInterface'

// ✅ CORRECT
const slackDatabase = createSlackDatabase();
const messageDatabase = createMessageDatabase();
const promptService = createPromptService(messageDatabase);
```

**Mistake 2: Forgetting to Import MessageDatabase**

```typescript
// ❌ WRONG - Missing import
import {
  createSlackDatabase,
  createPromptService, // No createMessageDatabase!
} from '@orientbot/database-services';

// ✅ CORRECT
import {
  createSlackDatabase,
  createMessageDatabase, // Added
  createPromptService,
} from '@orientbot/database-services';
```

**Mistake 3: Forgetting to Attach Service to Bot**

```typescript
// ❌ WRONG - Service created but never used
const promptService = createPromptService(messageDatabase);
const slackBot = createSlackBotService(config, slackDatabase);
// Missing: slackBot.setPromptService(promptService)

await slackBot.start(); // Bot will crash when trying to use prompts

// ✅ CORRECT
const promptService = createPromptService(messageDatabase);
logger.info('Prompt service initialized');

const slackBot = createSlackBotService(config, slackDatabase);

slackBot.setPromptService(promptService); // Attach it!
logger.info('Prompt service configured for Slack bot');

await slackBot.start();
```

**Mistake 4: Not Logging Initialization Steps**

```typescript
// ❌ BAD - Silent failures hard to debug
const messageDatabase = createMessageDatabase();
const promptService = createPromptService(messageDatabase);
slackBot.setPromptService(promptService);

// ✅ GOOD - Clear audit trail
const messageDatabase = createMessageDatabase();
logger.info('Message database initialized');

const promptService = createPromptService(messageDatabase);
logger.info('Prompt service initialized');

slackBot.setPromptService(promptService);
logger.info('Prompt service configured for Slack bot');
```

#### Troubleshooting Service Integration

**Problem: Bot crashes on message handling**

```bash
# Symptom in logs:
[ERROR] Cannot read property 'getSystemPromptText' of undefined

# Debug steps:
1. Check if PromptService was initialized:
   grep "Prompt service initialized" logs/instance-9/slack-dev.log

2. If missing, check main.ts for initialization code

3. Verify MessageDatabase import and initialization

4. Rebuild and restart:
   pnpm --filter @orientbot/bot-slack run build
   ./run.sh dev
```

**Problem: TypeScript compilation fails**

```bash
# Error:
src/main.ts(121,47): error TS2345: Argument of type 'SlackDatabase' is not assignable to parameter of type 'PromptDatabaseInterface'.

# Fix:
1. Check which database you're passing to createPromptService()
2. Replace with createMessageDatabase()
3. Import createMessageDatabase from @orientbot/database-services
```

**Problem: Service initialized but prompts don't work**

```bash
# Logs show initialization but bot ignores custom prompts

# Debug:
1. Verify service was attached:
   grep "Prompt service configured" logs/instance-9/slack-dev.log

2. Check if setPromptService() was called after creating bot

3. Test prompt API endpoint:
   curl http://localhost:13098/api/prompts

4. Verify custom prompt exists in database:
   sqlite3 "$SQLITE_DB_PATH" "SELECT * FROM system_prompts WHERE platform='slack';"
```

#### When to Apply This Pattern

Use this multiple-database pattern when:

1. **Adding PromptService to any bot**: Slack, WhatsApp, Discord, Telegram, etc.
2. **Integrating cross-platform services**: Any service that works across multiple messaging platforms
3. **Creating new bot integrations**: Template for adding new messaging platform support
4. **Debugging bot crashes**: If bot fails when handling messages, check service initialization

#### Testing Database Service Integration

**Unit Test Pattern**:

```typescript
// __tests__/main.test.ts
import { createMessageDatabase, createPromptService } from '@orientbot/database-services';

describe('Database Service Integration', () => {
  it('should initialize PromptService with MessageDatabase', () => {
    const messageDatabase = createMessageDatabase();
    const promptService = createPromptService(messageDatabase);

    expect(promptService).toBeDefined();
    expect(typeof promptService.getSystemPromptText).toBe('function');
  });

  it('should throw TypeScript error if using wrong database', () => {
    // This won't compile (that's the point!)
    // const slackDatabase = createSlackDatabase();
    // const promptService = createPromptService(slackDatabase); // TS Error
  });
});
```

**Integration Test Pattern**:

```bash
# Start bot and verify initialization
./run.sh dev

# Check logs for proper sequence
tail -f logs/instance-9/slack-dev.log | grep -E "(message-db|prompt-service|configured)"

# Expected output shows all three initialization steps
```

## Worktree-Specific Considerations

### 1. Shared node_modules

pnpm uses a content-addressable store - dependencies are shared across worktrees. This means:

- `pnpm install` is fast (most packages are already cached)
- No duplicate storage of identical packages
- Lock file (`pnpm-lock.yaml`) must stay in sync

### 2. Build Artifacts

Each worktree has its own `dist/` directories. When switching between worktrees:

- Build artifacts are NOT shared
- Always run `pnpm run build` after switching if needed

### 3. Turbo Caching

Turbo caches build outputs. In worktrees:

- Cache is local to each worktree
- Use `pnpm turbo run build --force` to bypass cache if needed

### 4. Environment Files

Environment files (`.env`, `.env.local`) should be copied from main worktree:

```bash
cp $ROOT_WORKTREE_PATH/.env .env
cp $ROOT_WORKTREE_PATH/.env.local .env.local 2>/dev/null || true
```

### 5. Multi-Instance Environment (NEW)

**Each worktree runs as a separate instance with isolated resources:**

- **Instance ID**: Auto-assigned (1-9) based on worktree name hash
- **Ports**: Automatically offset by `instance_id × 1000`
- **Database**: Separate SQLite database per instance (e.g., `.dev-data/instance-1/orient.db`)
- **Storage**: Separate MinIO bucket per instance
- **Containers**: Isolated Docker containers and networks

**Port Allocation Example:**

```
Main repo (Instance 0):  http://localhost:80    (ports: 80, 4098, 9000)
Worktree 1 (Instance 1): http://localhost:1080  (ports: 1080, 5098, 10000)
Worktree 2 (Instance 2): http://localhost:2080  (ports: 2080, 6098, 11000)
```

**Check your instance:**

```bash
source scripts/instance-env.sh
echo "Instance ID: $AI_INSTANCE_ID"
echo "Dashboard: http://localhost:$NGINX_PORT"
```

**List all running instances:**

```bash
./run.sh instances
```

**WhatsApp Safety:**

- WhatsApp is **disabled by default** in worktrees to avoid session conflicts
- Only one instance should run WhatsApp at a time
- Override with: `./run.sh dev --enable-whatsapp` (stop main repo WhatsApp first)

**Troubleshooting Port Conflicts:**

```bash
# Check what's using a port
lsof -ti :1080

# Force kill if needed
lsof -ti :1080 | xargs kill -9

# Manually set instance ID if auto-detection fails
export AI_INSTANCE_ID=3
./run.sh dev
```

See `multi-instance-development` skill for comprehensive documentation.

### Docker Compose Schema Validation (IMPORTANT)

**Problem**: Docker Compose v2.32+ has strict schema validation that does NOT allow variable interpolation in top-level volume and network key names.

**Error You'll See**:

```
validating docker-compose.yml: volumes Additional property minio-data-${AI_INSTANCE_ID:-0} is not allowed
```

**❌ WRONG - Variables in top-level keys**:

```yaml
# This causes schema validation errors in Docker Compose v2.32+
networks:
  orienter-network-${AI_INSTANCE_ID:-0}: # ❌ Variable in key name
    driver: bridge

volumes:
  minio-data-${AI_INSTANCE_ID:-0}: # ❌ Variable in key name
    driver: local
```

**✅ CORRECT - Static names with COMPOSE_PROJECT_NAME isolation**:

```yaml
# Use static names - Docker Compose prefixes with COMPOSE_PROJECT_NAME
networks:
  orienter-network: # ✅ Static name
    driver: bridge

volumes:
  minio-data: # ✅ Static name
    driver: local
```

**How Isolation Works**:

- `COMPOSE_PROJECT_NAME=orienter-instance-0` → volumes become `orienter-instance-0_minio-data`
- `COMPOSE_PROJECT_NAME=orienter-instance-1` → volumes become `orienter-instance-1_minio-data`
- Each instance gets completely separate volumes and networks automatically
- Database: SQLite files are stored in `.dev-data/instance-{id}/orient.db`

**Container Names ARE Different** - Variables work in service definitions:

```yaml
services:
  minio:
    container_name: orienter-minio-${AI_INSTANCE_ID:-0} # ✅ Works fine
    volumes:
      - minio-data:/data # ✅ Reference static name
    networks:
      - orienter-network # ✅ Reference static name
```

**Status Check Pattern** - When checking containers by instance:

```bash
# ❌ WRONG - Looking for compose project prefix
docker ps | grep "$COMPOSE_PROJECT_NAME"    # Won't find orienter-minio-0

# ✅ CORRECT - Look for container name pattern
docker ps | grep -E "orienter-.*-${AI_INSTANCE_ID}"  # Finds orienter-minio-0
```

**Key Takeaways**:

1. Top-level `volumes:` and `networks:` keys must be static strings
2. Service-level `container_name`, `environment`, `ports` can use variables
3. `COMPOSE_PROJECT_NAME` provides automatic isolation via prefixing
4. Container names follow the pattern `orienter-<service>-<instance_id>`
5. When scripting, match container names directly, not compose project names

### 6. Instance-Specific Environment Variable Configuration

**Critical Setup**: When copying `.env` from the main repo to a worktree, you MUST update instance-specific values or services will use the wrong database and storage.

#### The Problem

**Symptom**: Services fail to start, or you accidentally use instance 0's database from instance 9.

**Root Cause**: `.env` contains hard-coded values for instance 0:

```bash
SQLITE_DB_PATH=.dev-data/instance-0/orient.db
S3_ENDPOINT=http://localhost:9000
```

When you copy this to a worktree with instance ID 9, services try to use:

- SQLite database `.dev-data/instance-0/orient.db` instead of `.dev-data/instance-9/orient.db`
- MinIO on port **9000** (instance 0) instead of **18000** (instance 9)

#### Auto-Detecting Instance ID

The instance ID is calculated from the worktree path:

```bash
# Source instance environment variables
source scripts/instance-env.sh

# This sets:
echo $AI_INSTANCE_ID      # e.g., 9
echo $SQLITE_DB_PATH      # e.g., .dev-data/instance-9/orient.db
echo $MINIO_API_PORT      # e.g., 18000 (9000 + 9×1000)
echo $DASHBOARD_PORT      # e.g., 13098 (4098 + 9×1000)
```

**How Instance ID is Calculated**:

```bash
# From scripts/instance-env.sh (simplified)
WORKTREE_PATH=$(pwd)
WORKTREE_NAME=$(basename "$WORKTREE_PATH")

# Hash worktree name to get instance ID (1-9)
HASH=$(echo -n "$WORKTREE_NAME" | md5sum | cut -c1-8)
INSTANCE_ID=$((16#$HASH % 9 + 1))

# For main repo (no worktree)
if [ "$IS_WORKTREE" = "false" ]; then
  INSTANCE_ID=0
fi
```

#### Fixing SQLITE_DB_PATH

**Manual Fix**:

```bash
# 1. Source instance environment
source scripts/instance-env.sh

# 2. Update SQLITE_DB_PATH in .env
sed -i '' "s|^SQLITE_DB_PATH=.*|SQLITE_DB_PATH=.dev-data/instance-${AI_INSTANCE_ID}/orient.db|" .env

# 3. Create the directory if needed
mkdir -p ".dev-data/instance-${AI_INSTANCE_ID}"

# 4. Verify
echo "Updated SQLITE_DB_PATH:"
grep SQLITE_DB_PATH .env
```

**Expected Result**:

```bash
# Before (instance 0):
SQLITE_DB_PATH=.dev-data/instance-0/orient.db

# After (instance 9):
SQLITE_DB_PATH=.dev-data/instance-9/orient.db
```

#### Adding S3_ENDPOINT (MinIO)

MinIO also needs instance-specific configuration:

```bash
# Source instance environment
source scripts/instance-env.sh

# Check if S3_ENDPOINT exists in .env
if grep -q "^S3_ENDPOINT=" .env; then
  # Update existing
  sed -i '' "s|^S3_ENDPOINT=.*|S3_ENDPOINT=http://localhost:${MINIO_API_PORT}|" .env
else
  # Add new
  echo "S3_ENDPOINT=http://localhost:${MINIO_API_PORT}" >> .env
fi

# Also add AI_INSTANCE_ID for clarity
if ! grep -q "^AI_INSTANCE_ID=" .env; then
  echo "AI_INSTANCE_ID=${AI_INSTANCE_ID}" >> .env
fi

echo "Updated MinIO configuration:"
grep -E "(S3_ENDPOINT|AI_INSTANCE_ID)" .env
```

**Expected Result**:

```bash
S3_ENDPOINT=http://localhost:18000
AI_INSTANCE_ID=9
```

#### Complete Worktree .env Setup Script

**Automated setup** when creating a new worktree:

```bash
#!/bin/bash
# setup-worktree-env.sh
# Run after copying .env from main repo

set -e

echo "=== Configuring .env for Worktree Instance ==="

# 1. Source instance environment
source scripts/instance-env.sh

echo "📋 Instance Configuration:"
echo "   AI_INSTANCE_ID:    $AI_INSTANCE_ID"
echo "   SQLITE_DB_PATH:    $SQLITE_DB_PATH"
echo "   MINIO_API_PORT:    $MINIO_API_PORT"
echo ""

# 2. Fix SQLITE_DB_PATH
echo "🔧 Fixing SQLITE_DB_PATH..."
mkdir -p ".dev-data/instance-${AI_INSTANCE_ID}"
sed -i '' "s|^SQLITE_DB_PATH=.*|SQLITE_DB_PATH=.dev-data/instance-${AI_INSTANCE_ID}/orient.db|" .env
echo "   ✅ SQLITE_DB_PATH: .dev-data/instance-${AI_INSTANCE_ID}/orient.db"

# 3. Fix/Add S3_ENDPOINT
echo "🔧 Configuring MinIO endpoint..."
if grep -q "^S3_ENDPOINT=" .env; then
  sed -i '' "s|^S3_ENDPOINT=.*|S3_ENDPOINT=http://localhost:${MINIO_API_PORT}|" .env
else
  echo "S3_ENDPOINT=http://localhost:${MINIO_API_PORT}" >> .env
fi
echo "   ✅ S3_ENDPOINT: http://localhost:${MINIO_API_PORT}"

# 4. Add AI_INSTANCE_ID
if ! grep -q "^AI_INSTANCE_ID=" .env; then
  echo "" >> .env
  echo "# Instance-specific configuration (auto-generated)" >> .env
  echo "AI_INSTANCE_ID=${AI_INSTANCE_ID}" >> .env
  echo "   ✅ Added AI_INSTANCE_ID=${AI_INSTANCE_ID}"
fi

echo ""
echo "✅ Environment configured for instance $AI_INSTANCE_ID"
echo ""
echo "Verify with:"
echo "  grep -E '(SQLITE_DB_PATH|S3_ENDPOINT|AI_INSTANCE_ID)' .env"
```

**Usage**:

```bash
# After copying .env from main repo
cp $ROOT_WORKTREE_PATH/.env .env

# Run setup script
./scripts/setup-worktree-env.sh

# Or manually:
source scripts/instance-env.sh
# ... run the sed commands above ...
```

#### Migrating Secrets to Database

After fixing `.env`, migrate secrets from `.env` to the database:

```bash
# Set master encryption key (from main repo's .env)
export ORIENT_MASTER_KEY="your-master-key-from-main-env"

# Run migration script
npx tsx scripts/migrate-secrets-to-db.ts

# Expected output:
# ✅ Migrated 7 secrets:
#    - SLACK_BOT_TOKEN
#    - SLACK_APP_TOKEN
#    - SLACK_SIGNING_SECRET
#    - SLACK_USER_TOKEN
#    - OPENAI_API_KEY
#    - ANTHROPIC_API_KEY
```

**What This Does**:

1. Reads secrets from `.env` (e.g., `SLACK_BOT_TOKEN=xoxb-...`)
2. Encrypts them using `ORIENT_MASTER_KEY`
3. Stores encrypted values in `secrets` table
4. Services load secrets from database instead of `.env`

**Important**: The migration script uses `SQLITE_DB_PATH` from `.env`, which is why fixing it first is critical!

#### Verification Checklist

After configuring `.env`, verify instance isolation:

```bash
# 1. Check environment variables
source scripts/instance-env.sh
echo "Instance ID: $AI_INSTANCE_ID"

# 2. Verify SQLITE_DB_PATH
DB_PATH=$(grep SQLITE_DB_PATH .env | cut -d'=' -f2)
echo "SQLITE_DB_PATH: $DB_PATH (expected: .dev-data/instance-$AI_INSTANCE_ID/orient.db)"

# 3. Verify MinIO endpoint
MINIO_PORT=$(grep S3_ENDPOINT .env | grep -oE ':[0-9]+' | tr -d ':')
echo "MinIO port: $MINIO_PORT (expected: $MINIO_API_PORT)"

# 4. Test database connection
sqlite3 "$DB_PATH" "SELECT 1" >/dev/null && \
  echo "✅ Database connection successful" || \
  echo "❌ Database connection failed (file may not exist yet)"
```

#### Common Issues

**Issue 1: Database file not found**

```bash
# Error: unable to open database file
# Cause: SQLITE_DB_PATH points to wrong instance directory

# Fix:
source scripts/instance-env.sh
mkdir -p ".dev-data/instance-${AI_INSTANCE_ID}"
sed -i '' "s|^SQLITE_DB_PATH=.*|SQLITE_DB_PATH=.dev-data/instance-${AI_INSTANCE_ID}/orient.db|" .env
```

**Issue 2: Services use wrong instance database**

```bash
# Symptom: Instance 9 sees data from instance 0
# Cause: SQLITE_DB_PATH still points to instance-0

# Fix database path:
source scripts/instance-env.sh
sed -i '' "s|instance-[0-9]|instance-${AI_INSTANCE_ID}|g" .env
```

**Issue 3: MinIO bucket not found**

```bash
# Error: Bucket 'orient-data' not found
# Cause: S3_ENDPOINT not set, defaults to instance 0

# Fix:
source scripts/instance-env.sh
echo "S3_ENDPOINT=http://localhost:${MINIO_API_PORT}" >> .env
```

#### Environment Variable Reference

**Instance-Specific Variables** (must be updated per instance):

| Variable         | Instance 0                       | Instance 9                       | Formula                        |
| ---------------- | -------------------------------- | -------------------------------- | ------------------------------ |
| `AI_INSTANCE_ID` | `0`                              | `9`                              | Auto-detected                  |
| `SQLITE_DB_PATH` | `.dev-data/instance-0/orient.db` | `.dev-data/instance-9/orient.db` | `.dev-data/instance-${ID}/...` |
| `S3_ENDPOINT`    | `http://localhost:9000`          | `http://localhost:18000`         | 9000 + (ID × 1000)             |
| `DASHBOARD_PORT` | `4098`                           | `13098`                          | 4098 + (ID × 1000)             |
| `OPENCODE_PORT`  | `4099`                           | `13099`                          | 4099 + (ID × 1000)             |

**Shared Variables** (same across all instances):

- `ORIENT_MASTER_KEY` - Encryption key for secrets
- `SLACK_BOT_TOKEN` - Stored in database, not `.env`
- `OPENAI_API_KEY` - Stored in database, not `.env`
- Most service credentials (migrate to database)

### 7. Verifying Instance Isolation

**CRITICAL**: When running multiple instances, you MUST verify that your `.env` file is properly configured for your instance. A common issue is copying `.env` from the main repo without updating instance-specific values.

#### Quick Verification Command

Run this one-liner to check if your `.env` matches your instance:

```bash
source scripts/instance-env.sh && echo "Instance: $AI_INSTANCE_ID" && \
grep SQLITE_DB_PATH .env | grep -q "instance-$AI_INSTANCE_ID" && echo "✅ SQLITE_DB_PATH OK" || echo "❌ SQLITE_DB_PATH WRONG (expected instance-$AI_INSTANCE_ID)"
```

#### Comprehensive Isolation Check Script

Create or run this script to verify full isolation:

```bash
#!/bin/bash
# verify-instance-isolation.sh
# Run from worktree root directory

set -e

echo "=== Instance Isolation Verification ==="
echo ""

# Source instance environment
source scripts/instance-env.sh

echo "📋 Instance Configuration:"
echo "   AI_INSTANCE_ID:    $AI_INSTANCE_ID"
echo "   COMPOSE_PROJECT:   $COMPOSE_PROJECT_NAME"
echo "   Expected ports:"
echo "     - Nginx:         $NGINX_PORT"
echo "     - MinIO API:     $MINIO_API_PORT"
echo "     - MinIO Console: $MINIO_CONSOLE_PORT"
echo "     - Dashboard:     $DASHBOARD_PORT"
echo "     - OpenCode:      $OPENCODE_PORT"
echo "   Expected database:"
echo "     - SQLITE_DB_PATH: .dev-data/instance-$AI_INSTANCE_ID/orient.db"
echo ""

ERRORS=0

# Check SQLITE_DB_PATH
echo "🔍 Checking SQLITE_DB_PATH..."
CURRENT_DB_PATH=$(grep "^SQLITE_DB_PATH=" .env 2>/dev/null | cut -d'=' -f2-)
if [ -z "$CURRENT_DB_PATH" ]; then
  echo "   ❌ SQLITE_DB_PATH not found in .env"
  ((ERRORS++))
else
  EXPECTED_DB_PATH=".dev-data/instance-$AI_INSTANCE_ID/orient.db"
  if [ "$CURRENT_DB_PATH" != "$EXPECTED_DB_PATH" ]; then
    echo "   ❌ SQLITE_DB_PATH is '$CURRENT_DB_PATH', expected '$EXPECTED_DB_PATH'"
    ((ERRORS++))
  else
    echo "   ✅ SQLITE_DB_PATH is correct"
  fi
fi

# Check S3_ENDPOINT / MinIO
echo ""
echo "🔍 Checking S3/MinIO configuration..."
S3_ENDPOINT=$(grep "^S3_ENDPOINT=" .env 2>/dev/null | cut -d'=' -f2-)
if [ -z "$S3_ENDPOINT" ]; then
  echo "   ⚠️  S3_ENDPOINT not set (will default to localhost:9000 - instance 0)"
  echo "   Expected: http://localhost:$MINIO_API_PORT"
  ((ERRORS++))
else
  MINIO_PORT_IN_ENV=$(echo "$S3_ENDPOINT" | grep -oE ':[0-9]+' | tr -d ':')
  if [ "$MINIO_PORT_IN_ENV" != "$MINIO_API_PORT" ]; then
    echo "   ❌ S3_ENDPOINT uses port $MINIO_PORT_IN_ENV, expected $MINIO_API_PORT"
    ((ERRORS++))
  else
    echo "   ✅ S3_ENDPOINT port is correct ($MINIO_PORT_IN_ENV)"
  fi
fi

# Check AI_INSTANCE_ID in .env
echo ""
echo "🔍 Checking AI_INSTANCE_ID in .env..."
ENV_INSTANCE_ID=$(grep "^AI_INSTANCE_ID=" .env 2>/dev/null | cut -d'=' -f2-)
if [ -z "$ENV_INSTANCE_ID" ]; then
  echo "   ⚠️  AI_INSTANCE_ID not set in .env (relies on auto-detection)"
elif [ "$ENV_INSTANCE_ID" != "$AI_INSTANCE_ID" ]; then
  echo "   ❌ AI_INSTANCE_ID in .env ($ENV_INSTANCE_ID) differs from detected ($AI_INSTANCE_ID)"
  ((ERRORS++))
else
  echo "   ✅ AI_INSTANCE_ID matches ($ENV_INSTANCE_ID)"
fi

# Check for Docker containers
echo ""
echo "🔍 Checking Docker containers for instance $AI_INSTANCE_ID..."
NGINX_CONTAINER="orienter-nginx-$AI_INSTANCE_ID"
MINIO_CONTAINER="orienter-minio-$AI_INSTANCE_ID"

for container in "$NGINX_CONTAINER" "$MINIO_CONTAINER"; do
  if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${container}$"; then
    echo "   ✅ $container is running"
  else
    echo "   ⚠️  $container is NOT running"
  fi
done

# Check for port conflicts
echo ""
echo "🔍 Checking for port conflicts..."
for port_var in NGINX_PORT MINIO_API_PORT DASHBOARD_PORT OPENCODE_PORT; do
  port_value=$(eval echo \$$port_var)
  pid=$(lsof -ti :$port_value 2>/dev/null | head -1)
  if [ -n "$pid" ]; then
    proc_name=$(ps -p $pid -o comm= 2>/dev/null)
    echo "   Port $port_value ($port_var): in use by $proc_name (PID $pid)"
  else
    echo "   Port $port_value ($port_var): available"
  fi
done

# Summary
echo ""
echo "=== Summary ==="
if [ $ERRORS -eq 0 ]; then
  echo "✅ All isolation checks passed!"
else
  echo "❌ Found $ERRORS isolation issue(s) - see above for details"
  echo ""
  echo "To fix SQLITE_DB_PATH, run:"
  echo "  sed -i '' 's|instance-[0-9]|instance-$AI_INSTANCE_ID|g' .env"
  echo ""
  echo "To add S3_ENDPOINT, run:"
  echo "  echo 'S3_ENDPOINT=http://localhost:$MINIO_API_PORT' >> .env"
fi
```

#### Auto-Fix Database Path

If your SQLITE_DB_PATH points to the wrong instance, run this to fix it:

```bash
# Source instance env to get correct paths
source scripts/instance-env.sh

# Create the directory if needed
mkdir -p ".dev-data/instance-${AI_INSTANCE_ID}"

# Fix SQLITE_DB_PATH in .env
sed -i '' "s|^SQLITE_DB_PATH=.*|SQLITE_DB_PATH=.dev-data/instance-${AI_INSTANCE_ID}/orient.db|" .env

# Verify
echo "Updated SQLITE_DB_PATH:"
grep SQLITE_DB_PATH .env
```

#### Auto-Fix MinIO Endpoint

```bash
# Source instance env
source scripts/instance-env.sh

# Check if S3_ENDPOINT exists
if grep -q "^S3_ENDPOINT=" .env; then
  # Update existing
  sed -i '' "s|^S3_ENDPOINT=.*|S3_ENDPOINT=http://localhost:${MINIO_API_PORT}|" .env
else
  # Add new
  echo "S3_ENDPOINT=http://localhost:${MINIO_API_PORT}" >> .env
fi

# Also add AI_INSTANCE_ID for clarity
if ! grep -q "^AI_INSTANCE_ID=" .env; then
  echo "AI_INSTANCE_ID=${AI_INSTANCE_ID}" >> .env
fi

echo "Updated .env:"
grep -E "(S3_ENDPOINT|AI_INSTANCE_ID)" .env
```

#### Detecting Database Sharing Issues

**Symptom**: Changes in one worktree appear in another, or data conflicts occur.

**Detection**:

```bash
# From each worktree, run:
source scripts/instance-env.sh
echo "Instance $AI_INSTANCE_ID using database:"
grep SQLITE_DB_PATH .env

# If two worktrees show the same SQLITE_DB_PATH, they're sharing!
```

**Fix**: Run the auto-fix script above in the worktree that has the wrong SQLITE_DB_PATH.

#### Port Collision Detection

When starting services, check for port conflicts:

```bash
# Quick check before starting
source scripts/instance-env.sh
echo "Checking ports for instance $AI_INSTANCE_ID..."

for port in $NGINX_PORT $MINIO_API_PORT $DASHBOARD_PORT $OPENCODE_PORT; do
  if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port $port is already in use!"
    lsof -Pi :$port -sTCP:LISTEN
  fi
done
```

**Resolving Port Conflicts**:

```bash
# Option 1: Kill the process using the port
lsof -ti :6080 | xargs kill -9

# Option 2: Use a different instance ID
export AI_INSTANCE_ID=7  # Try a different instance
source scripts/instance-env.sh
./run.sh dev

# Option 3: Stop other instances first
./run.sh stop  # Stop this instance's containers
```

#### Troubleshooting Common Isolation Issues

**Issue: "Database file not found" error**

```bash
# Check if database file exists
ls -la ".dev-data/instance-$AI_INSTANCE_ID/orient.db"

# If missing, create directory and start services (will auto-create)
source scripts/instance-env.sh
mkdir -p ".dev-data/instance-$AI_INSTANCE_ID"
./run.sh dev  # Will create database on startup
```

**Issue: Two instances writing to same database**

```bash
# Fix: Ensure each worktree has correct SQLITE_DB_PATH
# In worktree 1:
grep SQLITE_DB_PATH .env  # Should show instance-1
# In worktree 6:
grep SQLITE_DB_PATH .env  # Should show instance-6
```

**Issue: MinIO bucket conflicts**

```bash
# Each instance should use its own MinIO
# Check current MinIO endpoint
grep S3_ENDPOINT .env

# List buckets in your instance's MinIO
docker exec orienter-minio-$AI_INSTANCE_ID mc ls local/
```

#### Environment Template for Worktrees

When creating a new worktree, use this template to ensure proper isolation:

```bash
# Copy .env from main and fix instance-specific values
cp /path/to/main/repo/.env .env

# Auto-configure for this instance
source scripts/instance-env.sh

# Create database directory
mkdir -p ".dev-data/instance-$AI_INSTANCE_ID"

# Update instance-specific values
cat >> .env << EOF

# Instance $AI_INSTANCE_ID configuration (auto-generated)
AI_INSTANCE_ID=$AI_INSTANCE_ID
S3_ENDPOINT=http://localhost:$MINIO_API_PORT
EOF

# Fix SQLITE_DB_PATH
sed -i '' "s|^SQLITE_DB_PATH=.*|SQLITE_DB_PATH=.dev-data/instance-${AI_INSTANCE_ID}/orient.db|" .env

echo "✅ Environment configured for instance $AI_INSTANCE_ID"
```

### 7. Database (Legacy Notes)

In multi-instance setups, each worktree has its own database. For legacy single-instance behavior, database connections would be shared.

### 8. Frontend Dependencies

When adding UI components that use new icon libraries or utilities:

```bash
# Navigate to the specific frontend package
cd src/dashboard/frontend

# Install the dependency
npm install lucide-react
# or
pnpm add lucide-react

# Then rebuild from root
cd ../../..
pnpm run build
```

**Common missing dependencies:**

- `lucide-react` - Icon components
- `react-hook-form` - Form handling
- `zod` - Schema validation

## Common Issues

### "Cannot find module" errors

```bash
# Reinstall dependencies
pnpm install

# If still failing, clear and reinstall
rm -rf node_modules
pnpm install
```

### TypeScript errors after package changes

```bash
# Rebuild all packages
pnpm turbo run build --force
```

### TS6059: File is not under 'rootDir'

```bash
# This means you're importing from root src/ into a package incorrectly
# SOLUTION 1: Move the service to root src/ (recommended for shared services)
mv packages/dashboard/src/services/myService.ts src/services/myService.ts

# SOLUTION 2: Use relative imports
# Change: import { foo } from '@orientbot/core'
# To:     import { foo } from '../../../../src/services/myService.js'
```

### Build succeeds but frontend shows errors

```bash
# Check if frontend-specific dependencies are missing
cd src/dashboard/frontend
npm install

# If icons/components don't work, install the library
npm install lucide-react  # or whatever is missing

# Rebuild everything
cd ../../..
pnpm run build
```

### Import path confusion (relative vs package aliases)

```typescript
// ❌ AVOID cross-package aliases in worktrees (causes build issues)
import { createLogger } from '@orientbot/core';

// ✅ USE relative paths for root imports
import { createLogger } from '../../../../src/utils/logger.js';

// ✅ USE package aliases ONLY within same package
import { AppConfig } from './config.js';
```

### Service initialization fails silently

```typescript
// In packages/dashboard/src/server/index.ts
// The service initialization is wrapped in try-catch with only a warning

// Check logs for:
logger.warn('Failed to initialize miniapp edit service', { error });

// Common causes:
// 1. Missing environment variables (OPENCODE_SERVER_URL, REPO_PATH)
// 2. Database connection issues
// 3. Missing dependencies in service files
```

### Stale worktree

```bash
# Fetch and rebase from main
git fetch origin
git rebase origin/main
pnpm install
pnpm run build
```

## Development Workflow Best Practices

### Step-by-Step Implementation in Worktrees

When implementing a feature across multiple layers (backend + API + frontend):

**1. Start with Backend Services (root `src/`)**

```bash
# Create services in root src/
touch src/services/myNewService.ts
touch src/services/myNewDatabase.ts

# Write tests alongside
touch test-my-new-feature.ts

# Test database layer first
npx tsx test-my-new-feature.ts
```

**2. Add API Routes (packages)**

```bash
# Create package-specific routes
touch packages/dashboard/src/server/routes/myFeature.routes.ts

# Wire into server
# Edit: packages/dashboard/src/server/routes/index.ts (export route creator)
# Edit: packages/dashboard/src/server/routes.ts (mount routes)
# Edit: packages/dashboard/src/server/index.ts (initialize services)

# Test build
pnpm run build
```

**3. Add Frontend Components**

```bash
# Navigate to frontend package
cd src/dashboard/frontend

# Install any new UI dependencies FIRST
npm install lucide-react  # or whatever you need

# Create components
mkdir -p src/components/MyFeature
touch src/components/MyFeature/MyFeatureModal.tsx
touch src/components/MyFeature/MyForm.tsx

# Add API client functions
# Edit: src/api.ts (add new API functions using apiRequest)

# Return to root and build
cd ../../..
pnpm run build
```

**4. Integration Testing**

```bash
# Start dev environment
./run.sh dev

# Test manually in browser
# Check API endpoints with curl
curl -H "Authorization: Bearer $TOKEN" http://localhost:4098/api/my-feature/test

# Fix issues and rebuild as needed
```

### Pre-Commit Checklist

Before committing in a worktree:

- [ ] All backend tests pass (`npx tsx test-*.ts`)
- [ ] Build succeeds (`pnpm run build`)
- [ ] TypeScript has no errors (`pnpm run typecheck`)
- [ ] Linting passes (`pnpm run lint`)
- [ ] Manual testing in dev environment complete
- [ ] No console.log statements left behind
- [ ] Environment variables documented if new ones added
- [ ] API functions use correct names (apiRequest, not fetchAPI)
- [ ] Services placed in correct directories (root vs package)

## Committing Changes in Worktree

```bash
# Stage changes
git add -A

# Commit with descriptive message
git commit -m "feat(miniapp): add AI-powered editor with OpenCode integration

- Add MiniappEditService and MiniappEditDatabase
- Create REST API routes for editing, rollback, history
- Implement frontend modal with preview and commit history
- Support iterative editing and build verification"

# Push branch
git push -u origin HEAD
```

### Creating a Pull Request from Worktree

```bash
# Use gh CLI to create PR
gh pr create --title "feat(miniapp): AI-powered editor" --body "$(cat <<'EOF'
## Summary
- Backend: Service layer with database tracking
- API: REST endpoints for edit operations
- Frontend: Modal UI with live preview

## Test Plan
- [x] Backend tests pass
- [x] API endpoints tested
- [x] Build succeeds
- [x] Manual testing in dev

## Files Changed
- src/services/miniappEditService.ts (550 lines)
- packages/dashboard/src/server/routes/apps.routes.ts (255 lines)
- src/dashboard/frontend/src/components/MiniAppEditor/* (580 lines)
EOF
)"
```

## Common Git Worktree Workflows

This section covers common git operations when working with worktrees, based on real-world usage patterns from miniapp editor development.

### Workflow 1: Merging Worktree Branch to Staging

**Scenario**: You've completed work in a worktree and want to merge to staging for testing.

**Steps**:

```bash
# 1. Ensure worktree changes are committed and pushed
cd ~/app-worktrees/miniapp-ai-editor-1768300530
git status  # Should show "working tree clean"
git push origin worktree/miniapp-ai-editor-1768300530

# 2. Navigate to staging worktree (or checkout staging in main repo)
cd ~/app-worktrees/staging-env-1768247120
# OR: git checkout staging (if not in worktree)

# 3. Update staging to latest
git pull origin staging

# 4. Clean up any temporary files that would conflict
rm .pnpm-install.pid  # Common: pnpm process ID files
rm -rf node_modules/.cache  # Optional: clear build caches

# 5. Merge feature branch
git merge worktree/miniapp-ai-editor-1768300530 --no-edit

# 6. If conflicts occur, resolve them:
git status  # Shows conflicted files
# Edit conflicted files, resolve markers
git add <resolved-files>
git commit --no-edit

# 7. Push to staging
git push origin staging
```

**Common Conflicts**:

- `.pnpm-install.pid` - Temporary file, safe to remove before merge
- `package-lock.json` / `pnpm-lock.yaml` - Accept incoming changes usually
- Environment files (`.env`) - Keep staging's version

### Workflow 2: Merging Worktree to Main (via PR)

**Best Practice**: Always merge to main via Pull Request for review.

**Steps**:

```bash
# 1. Ensure branch is pushed
cd ~/app-worktrees/my-feature-1234567
git push -u origin worktree/my-feature-1234567

# 2. Create PR using gh CLI
gh pr create \
  --base main \
  --head worktree/my-feature-1234567 \
  --title "feat: my feature" \
  --body "$(cat <<'EOF'
## Summary
Brief description of changes

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing complete

## Files Changed
- List major files changed
EOF
)"

# 3. Wait for review and approval

# 4. Merge PR (via GitHub UI or CLI)
gh pr merge <pr-number> --squash --delete-branch

# 5. Clean up worktree after merge
cd /path/to/main/repo
git worktree remove ~/app-worktrees/my-feature-1234567
git fetch origin --prune  # Remove remote-tracking branch
```

### Workflow 3: Syncing Worktree with Main Branch

**Scenario**: Your worktree branch is behind main and you need latest changes.

**Steps**:

```bash
# 1. Navigate to worktree
cd ~/app-worktrees/my-feature-1234567

# 2. Stash any uncommitted changes
git stash push -m "WIP: before sync"

# 3. Fetch latest from origin
git fetch origin main

# 4. Rebase onto main (cleaner history)
git rebase origin/main

# If conflicts occur:
# - Edit conflicted files
# - git add <resolved-files>
# - git rebase --continue
# - Repeat until rebase completes

# OR: Merge main (preserves merge commits)
# git merge origin/main

# 5. Restore stashed changes
git stash pop

# 6. Rebuild dependencies and code
pnpm install
pnpm run build

# 7. Force push if you rebased (rewrites history)
git push origin HEAD --force-with-lease
```

**When to Rebase vs Merge**:

- **Rebase**: Feature branches, want clean history, haven't pushed yet
- **Merge**: Shared branches, after pushing, when history matters

### Workflow 4: Handling Stale Worktrees

**Scenario**: Worktree was created days/weeks ago and may be out of sync.

**Detection**:

```bash
# Check if worktree exists but branch is gone
git worktree list
git branch -a | grep worktree/my-old-feature  # Empty = branch deleted

# Check how far behind main
cd ~/app-worktrees/my-old-feature
git fetch origin
git log --oneline HEAD..origin/main  # Shows commits you're missing
```

**Option A: Update and Continue Working**

```bash
cd ~/app-worktrees/my-old-feature

# 1. Fetch latest
git fetch origin --prune

# 2. Check if base branch still exists
git branch -r | grep origin/main  # Should exist

# 3. Rebase or merge latest changes
git rebase origin/main
# OR: git merge origin/main

# 4. Update dependencies (critical for stale worktrees)
pnpm install  # Might take time if lock file changed

# 5. Rebuild everything
pnpm run build --force

# 6. Test that everything works
pnpm test
./run.sh dev  # Start dev server
```

**Option B: Abandon and Remove**

```bash
# From main repo directory
cd /path/to/main/repo

# 1. Remove worktree (even if dirty)
git worktree remove ~/app-worktrees/my-old-feature --force

# 2. Delete local branch
git branch -D worktree/my-old-feature

# 3. Delete remote branch if exists
git push origin --delete worktree/my-old-feature

# 4. Prune remote references
git fetch origin --prune
```

### Workflow 5: Environment Synchronization

**Problem**: Worktree needs same environment as main repo but files differ.

**Solution A: Copy from Main** (recommended for new worktrees)

```bash
# Get main repo path
MAIN_REPO=/path/to/main/repo

# Copy all environment files
cp $MAIN_REPO/.env .env
cp $MAIN_REPO/.env.local .env.local 2>/dev/null || true
cp $MAIN_REPO/.env.staging .env.staging 2>/dev/null || true

# Copy credentials if needed
cp $MAIN_REPO/.credentials/* .credentials/ 2>/dev/null || true
```

**Solution B: Use Environment Variables** (recommended for automation)

```bash
# Set in .bashrc or .zshrc
export ROOT_WORKTREE_PATH=/path/to/main/repo

# Then in any worktree:
cp $ROOT_WORKTREE_PATH/.env .env
```

**Solution C: Symlink** (advanced, be careful)

```bash
# Link to main repo's .env (changes affect all worktrees!)
ln -s $ROOT_WORKTREE_PATH/.env .env

# Good for: Read-only access to shared config
# Bad for: Worktree-specific changes (they affect main repo)
```

**What NOT to Sync**:

- `node_modules/` - Should be installed per worktree
- `dist/`, `build/` - Build artifacts are worktree-specific
- `.pnpm-install.pid` - Process-specific temporary files
- `logs/` - Each worktree has its own logs

### Workflow 6: Safe Worktree Removal

**Before Removing** - Checklist:

```bash
cd ~/app-worktrees/my-feature

# 1. Check if there are uncommitted changes
git status

# If uncommitted changes exist:
# - Option A: Commit them
git add -A && git commit -m "WIP: save progress"

# - Option B: Stash them
git stash push -m "WIP before removal"

# - Option C: Create a backup branch
git branch backup/my-feature-$(date +%s)
git push origin backup/my-feature-$(date +%s)

# 2. Check if branch is pushed
git log origin/worktree/my-feature..HEAD
# Empty = all commits are pushed
# Non-empty = unpushed commits exist

# If unpushed commits:
git push origin HEAD
```

**Removal Steps**:

```bash
# From main repo (NOT from worktree directory)
cd /path/to/main/repo

# 1. List all worktrees
git worktree list

# 2. Remove specific worktree
git worktree remove ~/app-worktrees/my-feature

# If worktree is dirty or locked:
git worktree remove ~/app-worktrees/my-feature --force

# 3. Delete branch (if no longer needed)
git branch -D worktree/my-feature

# 4. Delete remote branch (if merged or no longer needed)
git push origin --delete worktree/my-feature

# 5. Prune stale remote references
git fetch origin --prune

# 6. Clean up orphaned worktree directories (if removal failed)
git worktree prune
```

**Automated Cleanup Script**:

```bash
#!/bin/bash
# cleanup-worktree.sh

WORKTREE_PATH=$1
BRANCH_NAME=$2

if [ -z "$WORKTREE_PATH" ] || [ -z "$BRANCH_NAME" ]; then
  echo "Usage: cleanup-worktree.sh <worktree-path> <branch-name>"
  exit 1
fi

# Remove worktree
git worktree remove "$WORKTREE_PATH" --force

# Delete local branch
git branch -D "$BRANCH_NAME"

# Delete remote branch
git push origin --delete "$BRANCH_NAME" 2>/dev/null || echo "Remote branch already deleted"

# Prune
git fetch origin --prune
git worktree prune

echo "✅ Worktree cleaned up: $WORKTREE_PATH"
```

### Conflict Resolution Patterns

**Common Conflict Scenarios**:

**1. Package Lock File Conflicts**

```bash
# Conflict in pnpm-lock.yaml or package-lock.json

# Solution: Accept theirs (staging/main version) and reinstall
git checkout --theirs pnpm-lock.yaml
pnpm install  # Regenerates lock file
git add pnpm-lock.yaml
git commit --no-edit
```

**2. Build Artifact Conflicts**

```bash
# Conflict in dist/ or compiled .js files

# Solution: Delete and rebuild
rm -rf dist/
rm -rf src/**/*.js src/**/*.d.ts
git add -A
pnpm run build
git add dist/
git commit --no-edit
```

**3. Environment File Conflicts**

```bash
# Conflict in .env or config files

# Solution: Keep target branch version (staging/main)
git checkout --theirs .env
git checkout --theirs .env.local
git add .env .env.local
git commit --no-edit
```

**4. Documentation Conflicts**

```bash
# Conflict in README.md or docs

# Solution: Manually merge (keep both changes)
# Edit the file to combine both versions
nano README.md
git add README.md
git commit --no-edit
```

### Worktree Branch Naming Conventions

**Recommended Patterns**:

```bash
# Feature development
worktree/feature-name-<timestamp>
worktree/miniapp-ai-editor-1768300530

# Skill development
skill/skill-name-<timestamp>
skill/worktree-operations-1768247120

# Bug fixes
worktree/fix-bug-description-<timestamp>

# Environment-specific
worktree/staging-env-<timestamp>
```

**Benefits**:

- Timestamp prevents name collisions
- Prefix identifies worktree type
- Easy to identify and clean up old branches

### Troubleshooting Common Issues

**Issue: "fatal: 'branch' is already checked out"**

```bash
# You can't checkout same branch in multiple worktrees
# Solution: Create new branch from it
git worktree add ~/worktrees/new -b new-branch existing-branch
```

**Issue: Worktree directory deleted but git still tracks it**

```bash
# Git thinks worktree exists but directory is gone
git worktree list  # Shows missing worktree

# Solution: Prune it
git worktree prune
```

**Issue: Cannot remove worktree - "uncommitted changes"**

```bash
# Worktree has uncommitted changes
# Solution: Force removal
git worktree remove ~/worktrees/feature --force

# Or commit changes first
cd ~/worktrees/feature
git add -A && git commit -m "WIP"
cd /main/repo
git worktree remove ~/worktrees/feature
```

**Issue: Merge conflicts in multiple files**

```bash
# Many files conflict during merge
# Solution: Abort and rebase instead
git merge --abort
git fetch origin
git rebase origin/staging

# Or use merge strategy
git merge -X theirs origin/staging  # Prefer their changes
git merge -X ours origin/staging    # Prefer our changes
```

## Merging Branches in Worktrees

This section covers the complete workflow for merging branches, handling conflicts, and rebuilding after merges.

### Standard Merge Workflow

**Step 1: Fetch and Merge**

```bash
# Fetch latest from remote
git fetch origin dev

# Merge into your worktree branch
git merge origin/dev --no-edit
```

**Step 2: Handle Conflicts (if any)**

See conflict resolution patterns below.

**Step 3: Rebuild After Merge**

```bash
# Install dependencies (lock file may have changed)
pnpm install

# Build with turbo (handles dependency order)
pnpm turbo run build --force
```

### Conflict Resolution Patterns

#### Pattern 1: pnpm-lock.yaml Conflicts

**Problem**: Lock file conflicts are common when merging branches with different dependency versions.

```bash
# ❌ DON'T manually resolve pnpm-lock.yaml conflicts

# ✅ DO accept theirs and regenerate
git checkout --theirs pnpm-lock.yaml
pnpm install  # Regenerates lock file with your package.json changes
git add pnpm-lock.yaml
git commit --no-edit
```

**Why this works**: pnpm regenerates the lock file based on your current `package.json` files, ensuring consistency.

#### Pattern 2: .pnpm-install.pid Conflicts

**Problem**: This temporary file tracks running pnpm processes and often causes merge conflicts.

```bash
# This file should NEVER be committed
# If you see it in conflicts:

# Option 1: Remove before merge
rm .pnpm-install.pid
git merge origin/dev --no-edit

# Option 2: Remove during conflict resolution
git checkout --theirs .pnpm-install.pid 2>/dev/null || true
rm -f .pnpm-install.pid
git add .pnpm-install.pid  # Stages deletion

# Verify it's in .gitignore
grep -q ".pnpm-install.pid" .gitignore || echo ".pnpm-install.pid" >> .gitignore
```

#### Pattern 3: Environment File Conflicts (.env, .env.local)

**Problem**: Worktree-specific environment values conflict with merged changes.

```bash
# Keep your worktree's environment (usually correct)
git checkout --ours .env
git checkout --ours .env.local 2>/dev/null || true
git add .env .env.local

# If you need to merge new variables from dev:
# 1. Save your current env
cp .env .env.backup

# 2. Accept theirs
git checkout --theirs .env

# 3. Manually merge new variables
diff .env.backup .env  # See what changed
# Add any new variables you need to .env.backup
mv .env.backup .env
git add .env
```

#### Pattern 4: Build Artifact Conflicts (dist/, _.js, _.d.ts)

**Problem**: Compiled TypeScript files conflict.

```bash
# Build artifacts should not be committed
# If they are, remove and rebuild

rm -rf packages/*/dist
rm -rf src/**/dist
git add -A
pnpm turbo run build --force
```

### TypeScript Module Resolution Errors After Merge

**Common Error**: `Cannot find module '@orientbot/core'` or similar after merging from dev.

**Cause**: Build order dependencies - packages must be built in the correct order.

**Solution 1: Force Rebuild with Turbo**

```bash
# Turbo handles dependency ordering automatically
pnpm turbo run build --force

# The --force flag bypasses cache, ensuring fresh builds
```

**Solution 2: Clean Install and Build**

```bash
# Nuclear option - clean everything and rebuild
rm -rf node_modules
rm -rf packages/*/node_modules
rm -rf packages/*/dist
pnpm install
pnpm turbo run build --force
```

**Solution 3: Build Specific Package First**

```bash
# If you know which package is missing, build it first
pnpm --filter @orientbot/core run build
pnpm --filter @orientbot/database run build

# Then build the rest
pnpm turbo run build
```

**Understanding Turbo Build Order**:

```
@orientbot/core           (no dependencies)
    ↓
@orientbot/database       (depends on core)
    ↓
@orientbot/agents         (depends on core, database)
    ↓
@orientbot/bot-whatsapp   (depends on agents)
@orientbot/dashboard      (depends on multiple packages)
```

Turbo reads `turbo.json` and `package.json` dependencies to determine build order. When merging introduces new dependencies, turbo ensures they're built first.

### Complete Merge Workflow Example

Here's a full example of merging from dev with all best practices:

```bash
# 1. Pre-merge cleanup
rm -f .pnpm-install.pid
git stash push -m "WIP before merge" 2>/dev/null || true

# 2. Fetch and merge
git fetch origin dev
git merge origin/dev --no-edit

# 3. If conflicts occur:
# Handle lock file
if git diff --name-only --diff-filter=U | grep -q "pnpm-lock.yaml"; then
  git checkout --theirs pnpm-lock.yaml
fi

# Handle .env (keep ours)
if git diff --name-only --diff-filter=U | grep -q ".env"; then
  git checkout --ours .env
fi

# Remove temp files from conflicts
rm -f .pnpm-install.pid
git add .pnpm-install.pid 2>/dev/null || true

# Complete merge
git add pnpm-lock.yaml .env 2>/dev/null || true
git commit --no-edit 2>/dev/null || true

# 4. Reinstall and rebuild
pnpm install
pnpm turbo run build --force

# 5. Restore stashed changes
git stash pop 2>/dev/null || true

# 6. Verify
pnpm run typecheck
echo "✅ Merge complete!"
```

### Troubleshooting Post-Merge Issues

**Issue: "TS2307: Cannot find module" after merge**

```bash
# Cause: Package build order issue
# Solution: Force rebuild with turbo
pnpm turbo run build --force

# If still failing, check specific package
pnpm --filter @orientbot/core run build
# Then rebuild all
pnpm turbo run build
```

**Issue: "ENOENT: no such file or directory" for dist files**

```bash
# Cause: dist/ directories not built
# Solution: Build everything
pnpm turbo run build --force

# If persists, clean and rebuild
rm -rf packages/*/dist
pnpm turbo run build --force
```

**Issue: pnpm install fails with integrity errors**

```bash
# Cause: Lock file out of sync
# Solution: Regenerate lock file
rm pnpm-lock.yaml
pnpm install
git add pnpm-lock.yaml
git commit -m "chore: regenerate pnpm-lock.yaml"
```

**Issue: Tests fail after merge but build succeeds**

```bash
# Cause: Test cache or mock files stale
# Solution: Clear caches and rerun
rm -rf node_modules/.cache
pnpm test -- --clearCache
pnpm test
```

### Best Practices Summary

1. **✅ Always remove .pnpm-install.pid before merging**
2. **✅ Use `git checkout --theirs pnpm-lock.yaml` for lock conflicts**
3. **✅ Keep your .env file (use `git checkout --ours .env`)**
4. **✅ Run `pnpm turbo run build --force` after every merge**
5. **✅ Use `pnpm install` before building (lock file may have changed)**
6. **❌ Don't manually edit pnpm-lock.yaml**
7. **❌ Don't commit build artifacts (dist/)**
8. **❌ Don't skip the rebuild step after merging**

## Cleanup

When done with a worktree, follow the safe removal workflow above.

The `GitWorktreeService` in `src/services/gitWorktreeService.ts` handles this automatically when using the skill editing tools.
