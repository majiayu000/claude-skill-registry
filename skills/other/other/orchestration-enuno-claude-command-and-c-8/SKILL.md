---
name: worktree-manager
version: 1.0.0
author: claude-command-and-control
created: 2025-11-29
last_updated: 2025-11-29
status: active
complexity: moderate
category: orchestration
tags: [git-worktree, workspace-isolation, branch-management, merge-strategy, conflict-prevention]
---

# Worktree Manager Skill

## Description
Comprehensive git worktree lifecycle management providing automated creation, configuration replication, health monitoring, intelligent cleanup, and merge strategy enforcement. This skill enables safe parallel development by isolating agent workspaces, preventing conflicts, and ensuring consistent environment configuration across all worktrees.

## When to Use This Skill
- "Set up worktrees for parallel development of authentication feature across 4 agents"
- "Create isolated workspaces for agents working on microservices extraction"
- "Manage git worktrees for concurrent API endpoint implementation"
- "Clean up completed worktrees after parallel execution finishes"
- "Isolate agent work in branches to prevent main branch contamination during development"

## When NOT to Use This Skill
- Single agent development without isolation needs → Use standard git workflow
- Trivial changes not requiring parallel work → Work directly in main workspace
- Read-only analysis or research tasks → No worktree needed
- Hotfix requiring immediate main branch commit → Use direct approach

## Prerequisites
- Git repository initialized with at least one commit
- Clean working directory (no uncommitted changes)
- Sufficient disk space (minimum 5GB free per worktree)
- Write permissions to parent directory for worktree creation
- Git version ≥2.5 (worktree feature introduced)

## Workflow

### Phase 1: Pre-Creation Validation and Planning
**Purpose**: Verify environment readiness and determine optimal worktree strategy

#### Step 1.1: Validate Git Repository State
Check repository is ready for worktree creation:

```bash
#!/bin/bash

function validate_git_state() {
  # Check if in git repository
  if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "ERROR: Not in a git repository"
    return 1
  fi

  # Check for uncommitted changes
  if ! git diff-index --quiet HEAD --; then
    echo "ERROR: Uncommitted changes in working directory"
    git status --short
    return 1
  fi

  # Check if on valid branch
  current_branch=$(git rev-parse --abbrev-ref HEAD)
  if [ "$current_branch" == "HEAD" ]; then
    echo "ERROR: Detached HEAD state, cannot create worktrees safely"
    return 1
  fi

  # Verify repository has commits
  if ! git rev-parse HEAD > /dev/null 2>&1; then
    echo "ERROR: Repository has no commits"
    return 1
  fi

  echo "✅ Git state validated successfully"
  return 0
}
```

**Validation Checklist**:
- [ ] Inside git repository
- [ ] No uncommitted changes
- [ ] On valid branch (not detached HEAD)
- [ ] Repository has at least one commit
- [ ] No ongoing merge/rebase/cherry-pick
- [ ] Git version ≥2.5

**Expected Output**: Validated git environment or specific error preventing worktree creation

#### Step 1.2: Check Disk Space and Resources
Ensure sufficient resources for worktrees:

```bash
function check_resources() {
  local num_worktrees=$1
  local repo_size=$(du -sm . | cut -f1)

  # Calculate required space (repo size × num worktrees + 20% buffer)
  local required_mb=$((repo_size * num_worktrees * 120 / 100))

  # Check available space in parent directory
  local available_mb=$(df -m ../ | tail -1 | awk '{print $4}')

  if [ $available_mb -lt $required_mb ]; then
    echo "ERROR: Insufficient disk space"
    echo "  Required: ${required_mb}MB"
    echo "  Available: ${available_mb}MB"
    return 1
  fi

  echo "✅ Sufficient disk space: ${available_mb}MB available, ${required_mb}MB required"
  return 0
}
```

**Expected Output**: Resource availability confirmation or insufficient resource warning

#### Step 1.3: Plan Worktree Structure
Design directory layout and naming convention:

**Worktree Naming Convention**:
```
Format: [agent-role]-[task-slug]-[timestamp]

Examples:
- builder-jwt-service-20251129143052
- validator-auth-tests-20251129143055
- architect-api-design-20251129143058
```

**Directory Structure**:
```
project-root/
├── .git/                    # Main git directory
├── main/                    # Primary workspace (renamed from root)
│   ├── src/
│   ├── tests/
│   └── package.json
└── worktrees/              # Worktree parent directory
    ├── builder-1/
    │   ├── src/
    │   ├── tests/
    │   ├── .env            # Copied from main
    │   ├── .claude/        # Copied from main
    │   └── package.json    # Symlinked or copied
    ├── builder-2/
    └── validator-1/
```

**Decision Point**:
- IF repository large (>1GB) → Use sparse checkout for worktrees
- ELSE IF node_modules present → Use symlinks to share dependencies
- ELSE → Full clone worktrees

**Expected Output**: Planned directory structure with naming conventions

### Phase 2: Worktree Creation and Configuration
**Purpose**: Create isolated workspaces with proper configuration replication

#### Step 2.1: Create Worktree with Branch
Generate worktree and associated branch:

```bash
function create_worktree() {
  local agent_name=$1
  local task_slug=$2
  local base_branch=${3:-main}

  # Generate unique branch name
  local timestamp=$(date +%Y%m%d%H%M%S)
  local branch_name="agent/${agent_name}/${task_slug}"
  local worktree_path="worktrees/${agent_name}"

  # Create parent directory if needed
  mkdir -p worktrees

  # Create worktree with new branch
  if git worktree add "$worktree_path" -b "$branch_name" "$base_branch"; then
    echo "✅ Created worktree: $worktree_path"
    echo "   Branch: $branch_name"
    echo "   Based on: $base_branch"
  else
    echo "ERROR: Failed to create worktree"
    return 1
  fi

  # Track worktree metadata
  cat >> .git/worktree-registry.json <<EOF
{
  "agent": "$agent_name",
  "worktree_path": "$worktree_path",
  "branch_name": "$branch_name",
  "base_branch": "$base_branch",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "active"
}
EOF

  return 0
}
```

**Expected Output**: Created worktree directory with clean branch checked out

#### Step 2.2: Replicate Environment Configuration
Copy configuration files to maintain consistency:

```bash
function replicate_configuration() {
  local worktree_path=$1
  local main_path="."

  echo "Replicating configuration to $worktree_path..."

  # Copy environment files
  if [ -f "$main_path/.env" ]; then
    cp "$main_path/.env" "$worktree_path/.env"
    echo "  ✅ Copied .env"
  fi

  if [ -f "$main_path/.env.local" ]; then
    cp "$main_path/.env.local" "$worktree_path/.env.local"
    echo "  ✅ Copied .env.local"
  fi

  # Copy Claude configuration
  if [ -d "$main_path/.claude" ]; then
    cp -r "$main_path/.claude" "$worktree_path/.claude"
    echo "  ✅ Copied .claude/ directory"
  fi

  # Copy editor configuration
  for config_file in .editorconfig .prettierrc .eslintrc.json .vscode; do
    if [ -e "$main_path/$config_file" ]; then
      cp -r "$main_path/$config_file" "$worktree_path/"
      echo "  ✅ Copied $config_file"
    fi
  done

  # Handle node_modules (symlink or install)
  if [ -d "$main_path/node_modules" ]; then
    # Option 1: Symlink (faster but shared)
    # ln -s "$(pwd)/node_modules" "$worktree_path/node_modules"

    # Option 2: Separate install (isolated but slower)
    cd "$worktree_path"
    npm ci --silent
    cd - > /dev/null
    echo "  ✅ Installed dependencies"
  fi

  # Create worktree-specific directories
  mkdir -p "$worktree_path/logs"
  mkdir -p "$worktree_path/outputs"

  echo "✅ Configuration replication complete"
}
```

**Configuration Files to Replicate**:
- **.env** and **.env.local**: Environment variables
- **.claude/**: Agent configurations and commands
- **.editorconfig**: Editor settings
- **.prettierrc**: Code formatting
- **.eslintrc.json**: Linting rules
- **.vscode/**: VS Code settings
- **tsconfig.json**: TypeScript configuration
- **jest.config.js**: Test configuration

**Expected Output**: Worktree with identical configuration to main workspace

#### Step 2.3: Create Agent-Specific Context
Set up agent context files:

```bash
function create_agent_context() {
  local worktree_path=$1
  local agent_name=$2
  local task_description=$3

  cat > "$worktree_path/AGENT_CONTEXT.md" <<EOF
# Agent Context: $agent_name

## Worktree Information
- **Path**: $worktree_path
- **Branch**: $(git -C "$worktree_path" rev-parse --abbrev-ref HEAD)
- **Base Branch**: $(git merge-base --fork-point main $(git -C "$worktree_path" rev-parse --abbrev-ref HEAD) | xargs git name-rev --name-only)
- **Created**: $(date)

## Task Assignment
$task_description

## Success Criteria
[To be defined by task assignment]

## Communication
- **Status Updates**: Update status/agent-status.json
- **Logs**: Write to logs/${agent_name}.log
- **Output**: Place artifacts in outputs/

## Handoff Protocol
When task complete:
1. Run all tests: \`npm test\`
2. Run linting: \`npm run lint\`
3. Commit changes: \`git commit -am "Complete: [task description]"\`
4. Update status: Mark as COMPLETE in status file
5. Notify orchestrator: Update MULTI_AGENT_PLAN.md

## Emergency Contacts
- Orchestrator: See MULTI_AGENT_PLAN.md
- Other agents: See worktrees/*/AGENT_CONTEXT.md
EOF

  # Create status tracking file
  cat > "$worktree_path/status/agent-status.json" <<EOF
{
  "agent": "$agent_name",
  "status": "initialized",
  "progress_percent": 0,
  "current_step": "Setup complete, ready to start",
  "last_update": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "has_error": false
}
EOF

  echo "✅ Created agent context files"
}
```

**Expected Output**: Agent context documentation and status tracking infrastructure

### Phase 3: Health Monitoring and Maintenance
**Purpose**: Monitor worktree health, detect issues, and maintain consistency

#### Step 3.1: Implement Health Checks
Periodic validation of worktree integrity:

```bash
function health_check_worktree() {
  local worktree_path=$1

  echo "Running health check for $worktree_path..."

  # Check 1: Worktree still registered in git
  if ! git worktree list | grep -q "$worktree_path"; then
    echo "  ⚠️  WARNING: Worktree not in git registry"
    return 1
  fi

  # Check 2: Branch exists and is valid
  local branch=$(git -C "$worktree_path" rev-parse --abbrev-ref HEAD)
  if [ -z "$branch" ] || [ "$branch" == "HEAD" ]; then
    echo "  ⚠️  WARNING: Invalid or detached HEAD"
    return 1
  fi

  # Check 3: No corrupted git objects
  if ! git -C "$worktree_path" fsck --no-progress > /dev/null 2>&1; then
    echo "  ❌ ERROR: Git object corruption detected"
    return 1
  fi

  # Check 4: Configuration files still present
  if [ ! -f "$worktree_path/.env" ] || [ ! -d "$worktree_path/.claude" ]; then
    echo "  ⚠️  WARNING: Configuration files missing"
    return 1
  fi

  # Check 5: No merge conflicts
  if git -C "$worktree_path" ls-files -u | grep -q '^'; then
    echo "  ⚠️  WARNING: Unresolved merge conflicts"
    return 1
  fi

  # Check 6: Disk space sufficient
  local available_mb=$(df -m "$worktree_path" | tail -1 | awk '{print $4}')
  if [ $available_mb -lt 1000 ]; then
    echo "  ⚠️  WARNING: Low disk space (${available_mb}MB remaining)"
    return 1
  fi

  echo "  ✅ Health check passed"
  return 0
}
```

**Health Check Schedule**:
- Every 5 minutes during active agent execution
- Before merging worktree changes
- After any git operation failure
- On manual request

**Expected Output**: Health status report with pass/warning/fail status

#### Step 3.2: Synchronize with Base Branch
Keep worktree updated with base branch changes:

```bash
function sync_with_base() {
  local worktree_path=$1
  local base_branch=${2:-main}

  cd "$worktree_path"

  echo "Syncing $worktree_path with $base_branch..."

  # Fetch latest changes
  git fetch origin "$base_branch"

  # Check if sync needed
  local behind_count=$(git rev-list --count HEAD..origin/"$base_branch")

  if [ $behind_count -eq 0 ]; then
    echo "  ✅ Already up to date"
    return 0
  fi

  echo "  Behind by $behind_count commits, syncing..."

  # Check for uncommitted changes
  if ! git diff-index --quiet HEAD --; then
    echo "  ⚠️  Uncommitted changes detected, stashing..."
    git stash push -m "Auto-stash before sync $(date)"
  fi

  # Rebase onto base branch
  if git rebase "origin/$base_branch"; then
    echo "  ✅ Rebased successfully"

    # Restore stashed changes if any
    if git stash list | grep -q "Auto-stash before sync"; then
      git stash pop
    fi

    return 0
  else
    echo "  ❌ Rebase conflict, manual intervention required"
    git rebase --abort

    # Try merge instead
    if git merge "origin/$base_branch"; then
      echo "  ✅ Merged successfully (rebase failed)"
      return 0
    else
      echo "  ❌ Merge also failed, worktree needs manual resolution"
      return 1
    fi
  fi
}
```

**Sync Strategy**:
- **Automatic**: Sync before agent starts work (if idle >1 hour)
- **Manual**: On request from orchestrator
- **Pre-merge**: Always sync before integrating changes back
- **Conflict handling**: Prefer rebase, fallback to merge

**Expected Output**: Synchronized worktree or conflict notification

### Phase 4: Merge Strategy and Integration
**Purpose**: Safely integrate worktree changes back to main branch

#### Step 4.1: Pre-Merge Validation
Validate worktree ready for merge:

```bash
function pre_merge_validation() {
  local worktree_path=$1
  local target_branch=${2:-main}

  cd "$worktree_path"

  echo "Running pre-merge validation..."

  # Validation 1: All tests passing
  if ! npm test; then
    echo "  ❌ Tests failing, cannot merge"
    return 1
  fi

  # Validation 2: Linting clean
  if ! npm run lint; then
    echo "  ❌ Linting errors, cannot merge"
    return 1
  fi

  # Validation 3: Build successful
  if ! npm run build; then
    echo "  ❌ Build failing, cannot merge"
    return 1
  fi

  # Validation 4: No uncommitted changes
  if ! git diff-index --quiet HEAD --; then
    echo "  ❌ Uncommitted changes, commit first"
    return 1
  fi

  # Validation 5: Synced with target branch
  git fetch origin "$target_branch"
  local behind_count=$(git rev-list --count HEAD..origin/"$target_branch")
  if [ $behind_count -gt 0 ]; then
    echo "  ⚠️  Behind target branch by $behind_count commits, sync recommended"
    # Don't fail, but warn
  fi

  # Validation 6: Check for potential conflicts
  git fetch origin "$target_branch"
  if ! git merge-tree $(git merge-base HEAD origin/"$target_branch") HEAD origin/"$target_branch" | grep -q '^@@'; then
    echo "  ✅ No merge conflicts predicted"
  else
    echo "  ⚠️  Potential merge conflicts detected"
  fi

  echo "  ✅ Pre-merge validation passed"
  return 0
}
```

**Expected Output**: Validation report with go/no-go merge decision

#### Step 4.2: Execute Merge Strategy
Merge worktree changes using appropriate strategy:

```bash
function merge_worktree() {
  local worktree_path=$1
  local target_branch=${2:-main}
  local merge_strategy=${3:-squash}  # Options: squash, merge, rebase

  local source_branch=$(git -C "$worktree_path" rev-parse --abbrev-ref HEAD)

  echo "Merging $source_branch → $target_branch (strategy: $merge_strategy)"

  # Switch to target branch in main workspace
  git checkout "$target_branch"
  git pull origin "$target_branch"

  case "$merge_strategy" in
    squash)
      # Squash merge: Combine all commits into one
      if git merge --squash "$source_branch"; then
        git commit -m "Merge agent work: $source_branch

Completed task from worktree: $worktree_path

Squashed commits:
$(git log --oneline $target_branch..$source_branch)
"
        echo "  ✅ Squash merge completed"
        return 0
      fi
      ;;

    merge)
      # Regular merge: Preserve commit history
      if git merge --no-ff "$source_branch" -m "Merge agent work: $source_branch"; then
        echo "  ✅ Merge completed"
        return 0
      fi
      ;;

    rebase)
      # Rebase: Linear history
      if git rebase "$source_branch"; then
        echo "  ✅ Rebase completed"
        return 0
      fi
      ;;

    *)
      echo "  ❌ Unknown merge strategy: $merge_strategy"
      return 1
      ;;
  esac

  # If we get here, merge failed
  echo "  ❌ Merge failed, resolving conflicts..."
  return 1
}
```

**Merge Strategy Decision Tree**:
- **Squash**: Clean history, single commit per feature (DEFAULT)
- **Merge**: Preserve detailed history, multiple developers
- **Rebase**: Linear history, advanced use cases

**Expected Output**: Successfully merged changes or conflict resolution instructions

### Phase 5: Cleanup and Archival
**Purpose**: Remove completed worktrees and archive important information

#### Step 5.1: Archive Worktree Artifacts
Save important files before deletion:

```bash
function archive_worktree() {
  local worktree_path=$1
  local agent_name=$2

  local timestamp=$(date +%Y%m%d%H%M%S)
  local archive_dir="archives/worktrees"
  local archive_name="${agent_name}_${timestamp}.tar.gz"

  mkdir -p "$archive_dir"

  echo "Archiving $worktree_path..."

  # Create archive with important files
  tar -czf "$archive_dir/$archive_name" \
    -C "$worktree_path" \
    logs/ \
    outputs/ \
    AGENT_CONTEXT.md \
    status/ \
    2>/dev/null

  # Store git metadata
  cat > "$archive_dir/${agent_name}_${timestamp}_metadata.json" <<EOF
{
  "agent": "$agent_name",
  "worktree_path": "$worktree_path",
  "branch": "$(git -C "$worktree_path" rev-parse --abbrev-ref HEAD)",
  "final_commit": "$(git -C "$worktree_path" rev-parse HEAD)",
  "archived_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "files_modified": $(git -C "$worktree_path" diff --name-only main | wc -l),
  "commits_created": $(git -C "$worktree_path" log --oneline main..HEAD | wc -l)
}
EOF

  echo "  ✅ Archived to $archive_dir/$archive_name"
}
```

**Files to Archive**:
- logs/ - All agent execution logs
- outputs/ - Generated artifacts
- AGENT_CONTEXT.md - Task description and context
- status/ - Progress tracking files
- Git metadata (branch name, commits, diffs)

**Expected Output**: Compressed archive and metadata JSON

#### Step 5.2: Remove Worktree Safely
Delete worktree after archival:

```bash
function remove_worktree() {
  local worktree_path=$1
  local delete_branch=${2:-false}

  local branch_name=$(git -C "$worktree_path" rev-parse --abbrev-ref HEAD)

  echo "Removing worktree: $worktree_path"

  # Remove the worktree
  if git worktree remove "$worktree_path" --force; then
    echo "  ✅ Worktree removed"
  else
    echo "  ❌ Failed to remove worktree"
    return 1
  fi

  # Optionally delete the branch
  if [ "$delete_branch" == "true" ]; then
    if git branch -D "$branch_name"; then
      echo "  ✅ Branch deleted: $branch_name"
    else
      echo "  ⚠️  Failed to delete branch: $branch_name"
    fi
  else
    echo "  ℹ️  Branch preserved: $branch_name"
  fi

  # Update registry
  jq "del(.[] | select(.worktree_path == \"$worktree_path\"))" \
    .git/worktree-registry.json > .git/worktree-registry.json.tmp
  mv .git/worktree-registry.json.tmp .git/worktree-registry.json

  return 0
}
```

**Safety Checks Before Removal**:
- [ ] Worktree archived successfully
- [ ] Changes merged to target branch OR explicitly abandoned
- [ ] No uncommitted changes OR user confirmed abandonment
- [ ] No background processes using worktree

**Expected Output**: Removed worktree directory and updated git registry

#### Step 5.3: Bulk Cleanup Operation
Clean up multiple worktrees:

```bash
function cleanup_completed_worktrees() {
  local archive=${1:-true}

  echo "Scanning for completed worktrees..."

  # Get list of all worktrees
  git worktree list --porcelain | grep -A 2 "^worktree" | while read -r line; do
    if [[ $line == worktree* ]]; then
      worktree_path=$(echo "$line" | awk '{print $2}')

      # Skip main worktree
      if [ "$worktree_path" == "$(pwd)" ]; then
        continue
      fi

      # Check if marked as complete
      if [ -f "$worktree_path/status/agent-status.json" ]; then
        status=$(jq -r '.status' "$worktree_path/status/agent-status.json")

        if [ "$status" == "completed" ] || [ "$status" == "merged" ]; then
          echo "Found completed worktree: $worktree_path"

          if [ "$archive" == "true" ]; then
            archive_worktree "$worktree_path" "$(basename "$worktree_path")"
          fi

          remove_worktree "$worktree_path" true
        fi
      fi
    fi
  done

  echo "✅ Cleanup complete"
}
```

**Expected Output**: Summary of cleaned worktrees

## Examples

### Example 1: Parallel Feature Development with 3 Agents
**Context**: Setting up isolated worktrees for 3 builder agents to work on authentication feature

**Input:**
```bash
# Create worktrees for parallel development
create_worktree "builder-1" "jwt-service" "main"
create_worktree "builder-2" "user-model" "main"
create_worktree "builder-3" "auth-endpoints" "main"
```

**Execution Flow:**
1. Phase 1: Validated git state, 15GB disk space available
2. Phase 2: Created 3 worktrees in parallel (1 minute total)
3. Phase 2: Replicated configuration to all worktrees
4. Phase 2: Created agent context files
5. Agents executed work in isolation
6. Phase 4: Pre-merge validation passed for all
7. Phase 4: Squash merged all branches to main
8. Phase 5: Archived artifacts and removed worktrees

**Expected Output:**
```
Worktree Creation Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ builder-1
   Path: worktrees/builder-1
   Branch: agent/builder-1/jwt-service
   Config: Replicated (8 files)
   Status: Ready

✅ builder-2
   Path: worktrees/builder-2
   Branch: agent/builder-2/user-model
   Config: Replicated (8 files)
   Status: Ready

✅ builder-3
   Path: worktrees/builder-3
   Branch: agent/builder-3/auth-endpoints
   Config: Replicated (8 files)
   Status: Ready

Total disk usage: 4.2GB
Estimated parallel capacity: 7 agents
```

**Rationale**: Demonstrates full lifecycle from creation through cleanup for typical parallel development scenario

### Example 2: Worktree Health Monitoring During Long-Running Tasks
**Context**: Monitoring worktree health over 6-hour parallel execution

**Input:**
```bash
# Start health monitoring
while true; do
  for worktree in worktrees/*; do
    health_check_worktree "$worktree"
  done
  sleep 300  # Check every 5 minutes
done
```

**Expected Output:**
```
Health Check Report - 2025-11-29 15:45:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

worktrees/builder-1 ✅ HEALTHY
  Git status: Clean
  Configuration: Present
  Disk space: 8.3GB available
  Last commit: 12 minutes ago

worktrees/builder-2 ⚠️  WARNING
  Git status: Clean
  Configuration: Present
  Disk space: 1.2GB available (LOW)
  Last commit: 3 hours ago (STALE?)
  Action: Monitor disk space

worktrees/validator-1 ✅ HEALTHY
  Git status: Clean
  Configuration: Present
  Disk space: 12.1GB available
  Last commit: 5 minutes ago

Summary: 2 healthy, 1 warning, 0 critical
```

**Rationale**: Shows proactive health monitoring catching potential issues before they cause failures

### Example 3: Conflict-Free Merge Strategy
**Context**: Merging 4 worktrees with overlapping file modifications

**Input:**
```bash
# Merge worktrees sequentially with conflict detection
for worktree in worktrees/*; do
  pre_merge_validation "$worktree" "main"
  merge_worktree "$worktree" "main" "squash"
  npm test  # Verify integration after each merge
done
```

**Expected Output:**
```
Merge Sequence Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. builder-1 (jwt-service) → main
   Strategy: Squash
   Files modified: 3
   Tests: ✅ 157/157 passing
   Status: ✅ MERGED

2. builder-2 (user-model) → main
   Strategy: Squash
   Files modified: 5
   Tests: ✅ 175/175 passing (18 new)
   Status: ✅ MERGED

3. builder-3 (auth-endpoints) → main
   Strategy: Squash
   Files modified: 4 (1 overlap with builder-2)
   Conflicts: Auto-resolved (non-conflicting changes)
   Tests: ✅ 198/198 passing (23 new)
   Status: ✅ MERGED

4. validator-1 (integration-tests) → main
   Strategy: Squash
   Files modified: 2
   Tests: ✅ 243/243 passing (45 new)
   Status: ✅ MERGED

Summary:
  Total merges: 4/4 successful
  Conflicts: 0 manual interventions
  Final test suite: 243 tests passing
  Total execution: 23 minutes
```

**Rationale**: Demonstrates sequential merge strategy preventing integration conflicts

## Quality Standards

### Output Requirements
- All worktrees must have identical configuration files (validated with checksums)
- Every worktree must have AGENT_CONTEXT.md and status tracking files
- Worktree registry must be kept in sync with actual worktrees
- All archived worktrees must include metadata JSON file
- Health checks must run at ≤5 minute intervals during active work

### Performance Requirements
- Worktree creation: ≤30 seconds per worktree (excluding dependency installation)
- Configuration replication: ≤10 seconds
- Health check execution: ≤5 seconds per worktree
- Merge operation: ≤2 minutes per worktree
- Cleanup operation: ≤1 minute per worktree

### Integration Requirements
- Integrates with parallel-executor-skill for workspace provisioning
- Provides worktree paths to agent-communication-skill for message routing
- Reports health status to orchestrator for monitoring dashboards
- Supports MULTI_AGENT_PLAN.md task assignments

## Common Pitfalls

### Pitfall 1: Node Modules Duplication Consuming Disk Space
**Issue**: Each worktree has full node_modules copy, consuming 1GB+ per worktree
**Why it happens**: npm ci runs in each worktree independently
**Solution**:
- Use symlinks to share node_modules from main workspace
- Use npm workspaces feature for shared dependencies
- Use pnpm which has built-in content-addressable storage
- Implement sparse worktrees excluding node_modules

### Pitfall 2: Configuration Drift Between Worktrees
**Issue**: Main workspace configuration changes not reflected in active worktrees
**Why it happens**: Configuration copied at creation time, not synced
**Solution**:
- Use symlinks for configuration files instead of copies
- Implement periodic configuration sync during health checks
- Validate configuration checksums before critical operations
- Notify agents when configuration updates required

### Pitfall 3: Orphaned Worktrees After Crashes
**Issue**: Git crash leaves worktrees in registry but directories deleted/corrupted
**Why it happens**: Incomplete cleanup, power loss, process termination
**Solution**:
- Run `git worktree prune` periodically to clean registry
- Implement worktree validation checking directory existence
- Use worktree registry to track state independently
- Implement recovery procedures for orphaned entries

### Pitfall 4: Merge Conflicts from Concurrent File Edits
**Issue**: Multiple agents editing same files causing merge conflicts
**Why it happens**: Poor task decomposition, overlapping responsibilities
**Solution**:
- Better task planning to minimize file overlap
- Merge worktrees sequentially, not all at once
- Use merge preview to detect conflicts before merging
- Implement file locking or ownership tracking

### Pitfall 5: Branch Pollution from Failed Experiments
**Issue**: Many abandoned branches from failed agent tasks
**Why it happens**: Branches not deleted after worktree removal
**Solution**:
- Always use `remove_worktree` with `delete_branch=true` for failed tasks
- Implement periodic branch cleanup (delete merged branches)
- Name branches clearly to identify agent experiments
- Archive branch metadata before deletion

## Integration with Command & Control

### Related Agents
- **Orchestrator Agent**: Requests worktree creation for parallel execution
- **Worker Agents**: Execute tasks within isolated worktrees
- **DevOps Agent**: May create worktrees for infrastructure testing

### Related Commands
- `/start-session`: May create worktree for session isolation
- `/cleanup`: Invokes worktree cleanup for completed work
- `/handoff`: May create worktree for receiving agent

### Related Skills
- **parallel-executor-skill**: Primary consumer, requests worktrees for agents (dependency)
- **multi-agent-planner-skill**: Plans which worktrees needed for parallel groups
- **agent-communication-skill**: Uses worktree paths for message routing
- **verification-before-completion**: Validates worktree state before merge

### MCP Dependencies
- **Git MCP**: All git operations (worktree add, remove, merge)
- **Filesystem MCP**: Directory creation, file copying, archival
- **Process MCP**: Running npm commands in worktrees

### Orchestration Notes
- **Invoked by**: parallel-executor-skill (workspace setup), orchestrator agent
- **Invokes**: None (leaf skill in dependency graph)
- **Chained with**: Always used before parallel-executor-skill

## Troubleshooting

### Issue: "fatal: 'worktrees/agent-1' already exists"
**Symptoms**: Cannot create worktree, path already exists
**Diagnosis**:
```bash
# Check if directory exists
ls -la worktrees/agent-1

# Check git worktree registry
git worktree list
```
**Solution**:
1. If directory exists but not in git registry: `rm -rf worktrees/agent-1`
2. If in registry but directory gone: `git worktree prune`
3. If both exist: Choose different worktree name or remove old one

### Issue: Worktree Out of Sync with Main Branch
**Symptoms**: Agent getting merge conflicts, working with stale code
**Diagnosis**:
```bash
cd worktrees/agent-1
git log --oneline main..HEAD  # Commits ahead
git log --oneline HEAD..main  # Commits behind
```
**Solution**:
```bash
# Sync with main branch
cd worktrees/agent-1
git fetch origin main
git rebase origin/main

# Or use sync function
sync_with_base "worktrees/agent-1" "main"
```

### Issue: Cannot Remove Worktree - "is dirty"
**Symptoms**: `git worktree remove` fails with uncommitted changes
**Diagnosis**:
```bash
cd worktrees/agent-1
git status
```
**Solution**:
```bash
# Option 1: Commit changes
git add -A
git commit -m "Final changes before cleanup"

# Option 2: Abandon changes
git reset --hard HEAD

# Option 3: Force remove (if certain)
git worktree remove --force worktrees/agent-1
```

### Issue: Disk Space Exhausted from Multiple Worktrees
**Symptoms**: "No space left on device" errors
**Diagnosis**:
```bash
du -sh worktrees/*
df -h
```
**Solution**:
```bash
# Remove completed worktrees immediately
cleanup_completed_worktrees

# Use symlinks for node_modules
for wt in worktrees/*; do
  rm -rf "$wt/node_modules"
  ln -s "$(pwd)/node_modules" "$wt/node_modules"
done

# Implement sparse checkout (advanced)
git sparse-checkout init --cone
```

## Version History
- 1.0.0 (2025-11-29): Initial release
  - Automated worktree creation with branch management
  - Configuration replication and environment setup
  - Health monitoring and validation
  - Intelligent merge strategies
  - Conflict prevention and detection
  - Cleanup and archival automation
  - Integration with parallel execution ecosystem
  - Comprehensive troubleshooting guidance
