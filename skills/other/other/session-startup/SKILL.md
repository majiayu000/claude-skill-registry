---
name: session-startup
description: >
  Session initialization sequence for community-patterns development.
  Use at the start of every Claude Code session. Checks for upstream updates,
  loads workspace configuration, and ensures dev servers are running.
---

# Session Startup Sequence

**Follow these steps IN ORDER on every session:**

## Step 1: Check for Upstream Updates

**Always check for updates from upstream first:**

```bash
# Check if updates are available
git fetch upstream 2>/dev/null || echo "No upstream configured"
git status

# If behind upstream/main, pull updates
# Example output: "Your branch is behind 'upstream/main' by 3 commits"
```

**If updates available:**
```bash
# Pull updates (will update CLAUDE.md, GETTING_STARTED.md, examples, etc.)
git pull --rebase upstream main

# If rebase succeeds
git push origin main

# If conflicts (rare - user files are in their namespace)
# Show conflicts and help resolve
```

**Why this matters:**
- Gets latest CLAUDE.md (this file!) with new instructions
- Gets updated GETTING_STARTED.md and DEVELOPMENT.md
- Gets new example patterns
- Gets other users' contributed patterns

## Step 1.5: Update Labs and Patterns Repositories

**After updating community-patterns, also update labs/ and patterns/ (if they exist):**

```bash
# Get parent directory
PARENT_DIR="$(git rev-parse --show-toplevel)/.."

# Update labs (required)
if [ -d "$PARENT_DIR/labs" ]; then
  echo "Updating labs repository..."
  cd "$PARENT_DIR/labs"
  git fetch origin
  git pull --rebase origin main
  cd -
else
  echo "⚠️  labs/ not found - user may need to clone it"
fi

# Update patterns (optional)
if [ -d "$PARENT_DIR/patterns" ]; then
  echo "Updating patterns repository..."
  cd "$PARENT_DIR/patterns"
  git fetch origin
  git pull --rebase origin main
  cd -
fi
```

**Tell user:**
```
Updated dependency repositories (labs and patterns if available).
[If found updates]: Pulled latest updates! This includes:
  - Updated documentation
  - New example patterns
  - [list what changed if significant]

[If no updates]: Already up to date with upstream.
```

## Step 1.5: Check Reference Repositories (Weekly)

**If it's been a while since last check, check for reference repo updates:**

```bash
# Get parent directory
PARENT_DIR="$(git rev-parse --show-toplevel)/.."

# Check if labs or patterns need updating
cd "$PARENT_DIR/labs" && git fetch origin && git status
cd "$PARENT_DIR/patterns" && git fetch origin && git status 2>/dev/null
```

**If updates available, update automatically:**

```bash
# Pull updates
cd "$PARENT_DIR/labs" && git pull origin main

# Restart both servers using the labs script
$PARENT_DIR/labs/scripts/restart-local-dev.sh --force

echo "Both dev servers restarted with latest labs updates"
echo "Toolshed (backend): http://localhost:8000"
echo "Shell (frontend): http://localhost:5173"
echo "Logs: $PARENT_DIR/labs/packages/toolshed/local-dev-toolshed.log"
echo "      $PARENT_DIR/labs/packages/shell/local-dev-shell.log"
```

**Important Notes:**
- **labs/** updates may include new framework features, bug fixes, or documentation
- **Dev server must be restarted** after pulling labs updates
- **patterns/** (if cloned) contains example patterns - optional to update
- Check approximately weekly, or when user encounters framework issues

## Step 2: Load Workspace Configuration

**Why we need this:** Your GitHub username is used for:
- Determining which `patterns/$GITHUB_USER/` directory is yours
- Committing patterns with proper attribution
- Deploying patterns with your identity key
- Keeping your work isolated from other users

**Load cached configuration:**

```bash
# Read workspace config (created during first-time setup)
if [ -f .claude-workspace ]; then
  GITHUB_USER=$(grep "^username=" .claude-workspace | cut -d= -f2)
  IS_FORK=$(grep "^is_fork=" .claude-workspace | cut -d= -f2)
  echo "Loaded workspace: patterns/$GITHUB_USER/"
  echo "Repository type: $([ "$IS_FORK" = "true" ] && echo "fork" || echo "upstream")"
else
  echo "ERROR: .claude-workspace not found - run GETTING_STARTED.md first"
  exit 1
fi
```

**If .claude-workspace doesn't exist** (shouldn't happen after setup):
```bash
# Detect from origin remote URL (most reliable)
ORIGIN_URL=$(git remote get-url origin)
GITHUB_USER=$(echo "$ORIGIN_URL" | sed -E 's/.*[:/]([^/]+)\/community-patterns.*/\1/')

# Detect if this is a fork (has upstream remote)
if git remote get-url upstream >/dev/null 2>&1; then
  IS_FORK=true
else
  IS_FORK=false
fi

# Create workspace config file
cat > .claude-workspace << EOF
username=$GITHUB_USER
is_fork=$IS_FORK
setup_complete=true
EOF

echo "Created .claude-workspace for: $GITHUB_USER"
echo "Repository type: $([ "$IS_FORK" = "true" ] && echo "fork" || echo "upstream")"
```

**Confirm with user:**
```
Ready to work! Your workspace: patterns/$GITHUB_USER/

What would you like to work on today?
```

**About `is_fork` configuration:**
- **Fork** (`is_fork=true`): User has their own fork with `upstream` remote pointing to jkomoros/community-patterns
  - PRs go from their fork to upstream
  - Fetch/rebase from `upstream/main` before creating PRs
  - Most common scenario for contributors
- **Direct** (`is_fork=false`): User working directly on jkomoros/community-patterns (e.g., jkomoros or collaborators)
  - PRs go from feature branch to main in same repo
  - Fetch/rebase from `origin/main` before creating PRs
  - Less common, requires write access to upstream
- This value is cached to avoid repeatedly checking `git remote` - it won't change during development

## Step 3: Check and Start Dev Servers (If Needed)

**IMPORTANT: Two servers must be running:**
1. **Toolshed** (backend) - Port 8000
2. **Shell** (frontend) - Port 5173

**First, check if servers are already running:**

```bash
# Check both ports
TOOLSHED_RUNNING=$(lsof -ti:8000 > /dev/null 2>&1 && echo "yes" || echo "no")
SHELL_RUNNING=$(lsof -ti:5173 > /dev/null 2>&1 && echo "yes" || echo "no")

if [ "$TOOLSHED_RUNNING" = "yes" ] && [ "$SHELL_RUNNING" = "yes" ]; then
  echo "✓ Both dev servers already running:"
  echo "  - Toolshed (backend): http://localhost:8000"
  echo "  - Shell (frontend): http://localhost:5173"
  echo ""
  echo "Servers are ready. No need to start them."
elif [ "$TOOLSHED_RUNNING" = "yes" ]; then
  echo "✓ Toolshed already running on port 8000"
  echo "✗ Shell not running - will start it"
  NEED_SHELL=1
elif [ "$SHELL_RUNNING" = "yes" ]; then
  echo "✓ Shell already running on port 5173"
  echo "✗ Toolshed not running - will start it"
  NEED_TOOLSHED=1
else
  echo "✗ No dev servers running - will start both"
  NEED_TOOLSHED=1
  NEED_SHELL=1
fi
```

**If servers are already running, STOP HERE and skip the rest of this step.**

**Tell the user:** "I can see your dev servers are already running. Skipping server startup."

**Only if servers need to be started, run this:**

```bash
# Get labs directory
LABS_DIR="$(git rev-parse --show-toplevel)/../labs"

# Use the labs restart script (handles starting servers properly)
if [ "$NEED_TOOLSHED" = "1" ] || [ "$NEED_SHELL" = "1" ]; then
  $LABS_DIR/scripts/restart-local-dev.sh --force
  echo "Dev servers started. Access at http://localhost:8000"
  echo "Logs:"
  echo "  - Toolshed: $LABS_DIR/packages/toolshed/local-dev-toolshed.log"
  echo "  - Shell: $LABS_DIR/packages/shell/local-dev-shell.log"
fi
```

**Why this matters:**
- Patterns need both servers to deploy and test
- The user may have started servers themselves - respect that and don't restart unnecessarily
- Toolshed handles pattern deployment and data
- Shell provides the UI for viewing patterns
- Claude only starts servers if they're not already running
