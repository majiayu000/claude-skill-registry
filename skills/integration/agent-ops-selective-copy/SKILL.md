---
name: agent-ops-selective-copy
description: "Create clean git branches from feature work, excluding agent-ops files. Use for PR preparation."
category: utility
invokes: [agent-ops-git, agent-ops-interview]
invoked_by: []
state_files:
  read: [log/created-files.log]
  write: [log/selective-copy-*.log]
reference: [../../reference/file-audit-trail.md]
---

# Selective Copy — Clean Branch Creation

> Create a clean git branch from feature work, excluding specific paths. Platform agnostic.

**Works with or without `aoc` CLI.** Uses standard git commands.

---

## Purpose

Create a new branch containing feature work while excluding agent/workflow files for clean PRs.

---

## CRITICAL: No Assumptions

> **NEVER assume. NEVER guess. ALWAYS ask.**

**Before creating ANY clean branch, confirm with user:**

| If unclear about... | ASK |
|---------------------|-----|
| Source branch | "Which branch contains your feature work?" |
| Clean branch name | "I'll create `{name}`. Does this look right?" |
| Base branch | "Which branch should excluded paths be restored from? (e.g., develop, main)" |
| What to exclude | "What paths should I exclude? (Default: .agent/, .github/)" |

**If ANY of these are ambiguous:**
1. Stop
2. Ask ONE question at a time
3. Wait for explicit confirmation
4. Only proceed when ALL inputs are confirmed

**NEVER:**
- Guess the base branch
- Assume exclusions without asking
- Create a branch without showing the user the exact name first
- Proceed if source branch is unclear

---

## Prerequisites

### MANDATORY: File Audit Trail

**The file-created.log MUST exist before proceeding.** This ensures we know which files to exclude.

If `.agent/log/created-files.log` does not exist:
1. **Generate it** from git history (see Generation Procedure below)
2. **Present to user** for validation
3. **Only proceed** after user confirms the list

This prevents accidental inclusion of agent-ops files in the clean branch.

---

## Invocation

User says something like:
- "Create a clean branch for PR"
- "Make a branch without .agent and .github changes"
- "Prepare my feature for code review"

---

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `source_branch` | Feature branch with work | Current branch |
| `new_branch` | Name for clean branch | `{source_branch}-clean` |
| `base_branch` | Branch to restore excluded paths from | Auto-detect |
| `exclusions` | Paths/patterns to exclude | Prompt user |

---

## Workflow

### 1. Gather Requirements

**If not provided, ask:**

1. **Source branch** (default: current)
2. **New branch name** (default: `{current}-clean`)
3. **Base branch** — try auto-detect first:

```powershell
# PowerShell: Find merge-base with main or develop
$mainBase = git merge-base HEAD main 2>$null
$devBase = git merge-base HEAD develop 2>$null

if ($mainBase) { $baseBranch = "main" }
elseif ($devBase) { $baseBranch = "develop" }
else { 
    # Ask user
    Write-Host "Could not auto-detect base branch. Which branch was this feature branched from?"
}
```

```bash
# Bash: Find merge-base
main_base=$(git merge-base HEAD main 2>/dev/null)
dev_base=$(git merge-base HEAD develop 2>/dev/null)

if [ -n "$main_base" ]; then
    base_branch="main"
elif [ -n "$dev_base" ]; then
    base_branch="develop"
else
    echo "Could not auto-detect base branch. Which branch was this feature branched from?"
fi
```

4. **Exclusions** — if not specified, prompt:

```
Would you like to exclude agent-ops files? This includes:
- `.agent/` directory
- `.github/skills/`, `.github/prompts/`, `.github/agents/`

Additionally, agent-ops created these files outside .agent/:
{list from .agent/log/created-files.log}

[1] Exclude all agent-ops files (recommended)
[2] Exclude only .agent/ and .github/
[3] Let me specify custom paths
[4] Don't exclude anything
```

### 2. Check and Generate Audit Trail (MANDATORY)

**Before proceeding, verify `.agent/log/created-files.log` exists.**

```powershell
# PowerShell
$logPath = ".agent/log/created-files.log"
if (-not (Test-Path $logPath)) {
    Write-Host "⚠️  File audit trail not found: $logPath" -ForegroundColor Yellow
    Write-Host "Generating from git history..." -ForegroundColor Cyan
    # Proceed to generation
} else {
    Write-Host "✓ Audit trail found: $logPath" -ForegroundColor Green
    # Skip to step 3
}
```

```bash
# Bash
log_path=".agent/log/created-files.log"
if [ ! -f "$log_path" ]; then
    echo "⚠️  File audit trail not found: $log_path"
    echo "Generating from git history..."
    # Proceed to generation
else
    echo "✓ Audit trail found: $log_path"
    # Skip to step 3
fi
```

**If log is missing, generate it:**

#### Generation Procedure

1. **Find the branch point** (where feature diverged from base):

```powershell
# PowerShell
$baseBranch = "develop"  # or auto-detected
$branchPoint = git merge-base HEAD $baseBranch
Write-Host "Branch point: $branchPoint"
```

```bash
# Bash
base_branch="develop"
branch_point=$(git merge-base HEAD "$base_branch")
echo "Branch point: $branch_point"
```

2. **List files added since branch point** (excluding .agent/ and .github/):

```powershell
# PowerShell
$addedFiles = git diff --name-status --diff-filter=A $branchPoint HEAD |
    ForEach-Object { ($_ -split "\t")[1] } |
    Where-Object { 
        $_ -notmatch "^\.agent/" -and 
        $_ -notmatch "^\.github/skills/" -and 
        $_ -notmatch "^\.github/prompts/" -and 
        $_ -notmatch "^\.github/agents/"
    }

Write-Host "`nFiles added since branch point:" -ForegroundColor Cyan
$addedFiles | ForEach-Object { Write-Host "  CREATE $_" }
Write-Host "`nTotal: $($addedFiles.Count) files"
```

```bash
# Bash
added_files=$(git diff --name-status --diff-filter=A "$branch_point" HEAD | 
    cut -f2 | 
    grep -v "^\.agent/" | 
    grep -v "^\.github/skills/" | 
    grep -v "^\.github/prompts/" | 
    grep -v "^\.github/agents/")

echo ""
echo "Files added since branch point:"
echo "$added_files" | while read -r file; do
    [ -n "$file" ] && echo "  CREATE $file"
done
echo ""
echo "Total: $(echo "$added_files" | grep -c .)"
```

3. **Present to user for validation** (MANDATORY):

```
📋 Generated file list from git history:

  CREATE src/utils/helper.py
  CREATE tests/test_helper.py
  CREATE docs/PLANNING.md

Total: 3 files

⚠️  Please review this list carefully.

These files will be EXCLUDED from the clean branch.
Missing files may leak into PR. Extra files may be wrongly excluded.

Options:
[1] Approve and continue
[2] Edit list (will open in editor)
[3] Abort
```

4. **Save after user approval**:

```powershell
# PowerShell (only after user confirms)
$logDir = ".agent/log"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"

# Write header
@"
# Agent-Ops File Creation Audit Trail
# Generated from git history on $timestamp
# Branch point: $branchPoint (from $baseBranch)
# User validated: YES
# --- Log entries below this line ---
"@ | Out-File -FilePath $logPath -Encoding utf8

# Write entries
foreach ($file in $addedFiles) {
    Add-Content -Path $logPath -Value "$timestamp CREATE $file"
}

Write-Host "✓ Audit trail saved: $logPath" -ForegroundColor Green
```

```bash
# Bash (only after user confirms)
log_dir=".agent/log"
mkdir -p "$log_dir"

timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Write header
cat > "$log_path" << EOF
# Agent-Ops File Creation Audit Trail
# Generated from git history on $timestamp
# Branch point: $branch_point (from $base_branch)
# User validated: YES
# --- Log entries below this line ---
EOF

# Write entries
echo "$added_files" | while read -r file; do
    [ -n "$file" ] && echo "$timestamp CREATE $file" >> "$log_path"
done

echo "✓ Audit trail saved: $log_path"
```

### 3. Read Audit Trail

Check `.agent/log/created-files.log` for files created outside `.agent/`:

```powershell
# PowerShell
$logPath = ".agent/log/created-files.log"
$createdFiles = Get-Content $logPath | 
    Where-Object { $_ -match "^\d{4}-\d{2}-\d{2}" } |
    ForEach-Object { 
        $parts = $_ -split " ", 3
        [PSCustomObject]@{
            Timestamp = $parts[0]
            Action = $parts[1]
            Path = $parts[2]
        }
    } |
    Where-Object { $_.Action -eq "CREATE" } |
    Select-Object -ExpandProperty Path

Write-Host "Files created by agent-ops:"
$createdFiles | ForEach-Object { Write-Host "  - $_" }
```

```bash
# Bash
echo "Files created by agent-ops:"
grep "^[0-9]" .agent/log/created-files.log | 
    awk '$2 == "CREATE" { print "  - " $3 }'
```

### 4. Execute (Git-Based)

#### Step 1: Create worktree with new branch

```powershell
# PowerShell
$sourceBranch = git branch --show-current
$newBranch = "$sourceBranch-clean"
$worktreePath = "../$newBranch"

git worktree add -b $newBranch $worktreePath HEAD
Set-Location $worktreePath
```

```bash
# Bash
source_branch=$(git branch --show-current)
new_branch="${source_branch}-clean"
worktree_path="../${new_branch}"

git worktree add -b "$new_branch" "$worktree_path" HEAD
cd "$worktree_path"
```

#### Step 2: Restore excluded directories from base branch

```powershell
# PowerShell
$baseBranch = "develop"  # or detected/user-provided
$excludeDirs = @(".github", ".agent")

foreach ($dir in $excludeDirs) {
    git checkout $baseBranch -- $dir 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Restored $dir from $baseBranch"
    } else {
        Write-Host "$dir doesn't exist in $baseBranch (new directory)"
    }
}
```

```bash
# Bash
base_branch="develop"
exclude_dirs=(".github" ".agent")

for dir in "${exclude_dirs[@]}"; do
    if git checkout "$base_branch" -- "$dir" 2>/dev/null; then
        echo "Restored $dir from $base_branch"
    else
        echo "$dir doesn't exist in $base_branch (new directory)"
    fi
done
```

#### Step 3: Remove NEW files that don't exist in base

For files logged in audit trail that are new (not in base branch):

```powershell
# PowerShell
foreach ($file in $createdFiles) {
    # Check if file exists in base branch
    $existsInBase = git ls-tree -r $baseBranch --name-only | Where-Object { $_ -eq $file }
    
    if (-not $existsInBase) {
        # File is new, remove from git tracking
        git rm --cached $file 2>$null
        Write-Host "Removed new file from tracking: $file"
    } else {
        # File exists in base, restore it
        git checkout $baseBranch -- $file 2>$null
        Write-Host "Restored $file from $baseBranch"
    }
}
```

```bash
# Bash
for file in "${created_files[@]}"; do
    if git ls-tree -r "$base_branch" --name-only | grep -q "^${file}$"; then
        # File exists in base, restore it
        git checkout "$base_branch" -- "$file" 2>/dev/null
        echo "Restored $file from $base_branch"
    else
        # File is new, remove from git tracking
        git rm --cached "$file" 2>/dev/null
        echo "Removed new file from tracking: $file"
    fi
done
```

#### Step 4: Commit the exclusions

```powershell
# PowerShell
git add -A
git commit -m "chore: prepare clean branch for PR (exclude agent-ops files)"
```

```bash
# Bash
git add -A
git commit -m "chore: prepare clean branch for PR (exclude agent-ops files)"
```

#### Step 5: Create Exclusion Log

Create a log file for selective-merge to use later:

```powershell
# PowerShell
$timestamp = Get-Date -Format "yyyy-MM-dd-HHmmss"
$logFile = ".agent/log/selective-copy-$newBranch-$timestamp.log"
$cleanBranchHash = git rev-parse HEAD
$sourceBranchHash = git rev-parse $sourceBranch

# Create log directory if needed
New-Item -ItemType Directory -Path ".agent/log" -Force | Out-Null

# Write log header
@"
# Selective Copy Exclusion Log
# Generated: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ssK")
# Source Branch: $sourceBranch ($sourceBranchHash)
# Clean Branch: $newBranch ($cleanBranchHash)
# Base Branch: $baseBranch
# Excluded Paths: $($excludeDirs -join ", ")

# Format: {ACTION} {path}
# RESTORE = restored from base branch
# REMOVE = removed from tracking (new file not in base)

"@ | Out-File -FilePath $logFile -Encoding utf8

# Log each excluded directory
foreach ($dir in $excludeDirs) {
    Add-Content -Path $logFile -Value "RESTORE $dir"
}

# Log removed files from audit trail
foreach ($file in $createdFiles) {
    $existsInBase = git ls-tree -r $baseBranch --name-only | Where-Object { $_ -eq $file }
    if (-not $existsInBase) {
        Add-Content -Path $logFile -Value "REMOVE $file"
    } else {
        Add-Content -Path $logFile -Value "RESTORE $file"
    }
}

Write-Host "Exclusion log created: $logFile"
```

```bash
# Bash
timestamp=$(date +"%Y-%m-%d-%H%M%S")
log_file=".agent/log/selective-copy-${new_branch}-${timestamp}.log"
clean_branch_hash=$(git rev-parse HEAD)
source_branch_hash=$(git rev-parse "$source_branch")

# Create log directory if needed
mkdir -p ".agent/log"

# Write log header
cat > "$log_file" << EOF
# Selective Copy Exclusion Log
# Generated: $(date -Iseconds)
# Source Branch: $source_branch ($source_branch_hash)
# Clean Branch: $new_branch ($clean_branch_hash)
# Base Branch: $base_branch
# Excluded Paths: ${exclude_dirs[*]}

# Format: {ACTION} {path}
# RESTORE = restored from base branch
# REMOVE = removed from tracking (new file not in base)

EOF

# Log each excluded directory
for dir in "${exclude_dirs[@]}"; do
    echo "RESTORE $dir" >> "$log_file"
done

# Log removed files from audit trail
for file in "${created_files[@]}"; do
    if git ls-tree -r "$base_branch" --name-only | grep -q "^${file}$"; then
        echo "RESTORE $file" >> "$log_file"
    else
        echo "REMOVE $file" >> "$log_file"
    fi
done

echo "Exclusion log created: $log_file"
```

### 5. Verify

```powershell
# PowerShell
Write-Host "`n=== Verification ===" -ForegroundColor Cyan

# Check status
git status

# Compare with base branch
Write-Host "`nChanges compared to ${baseBranch}:"
git diff $baseBranch --stat

# Verify excluded paths match base
Write-Host "`nVerifying exclusions:"
foreach ($dir in $excludeDirs) {
    $diff = git diff $baseBranch -- $dir
    if ([string]::IsNullOrEmpty($diff)) {
        Write-Host "  $dir matches $baseBranch ✓" -ForegroundColor Green
    } else {
        Write-Host "  $dir has differences from $baseBranch" -ForegroundColor Yellow
    }
}
```

```bash
# Bash
echo ""
echo "=== Verification ==="

# Check status
git status

# Compare with base branch
echo ""
echo "Changes compared to ${base_branch}:"
git diff "$base_branch" --stat

# Verify excluded paths match base
echo ""
echo "Verifying exclusions:"
for dir in "${exclude_dirs[@]}"; do
    if [ -z "$(git diff "$base_branch" -- "$dir")" ]; then
        echo "  $dir matches $base_branch ✓"
    else
        echo "  $dir has differences from $base_branch"
    fi
done
```

### 6. Report to User

```
✅ Clean branch created: {new_branch}

Location: {worktree_path}

Excluded:
- .github/ (restored from {base_branch})
- .agent/ (restored from {base_branch})
- {N} files from audit trail

Changes from {base_branch}:
{git diff --stat output}

Next steps:
1. Review changes: cd {worktree_path} && git log --oneline {base_branch}..HEAD
2. Push for PR: git push -u origin {new_branch}
3. Cleanup when done: git worktree remove {worktree_path}
```

---

## Cleanup

When done with the clean branch:

```powershell
# PowerShell
# Return to original repo
Set-Location ../{original-repo}

# Remove worktree (keeps branch)
git worktree remove ../{new_branch}

# Delete branch if no longer needed
git branch -D {new_branch}
```

```bash
# Bash
# Return to original repo
cd ../{original-repo}

# Remove worktree (keeps branch)
git worktree remove "../${new_branch}"

# Delete branch if no longer needed
git branch -D "${new_branch}"
```

---

## Common Exclusion Presets

### Clean PR (Recommended)
```
Directories: .github, .agent
Files: All from audit trail
```

### Feature Only
```
Directories: .github, .agent, .vscode, docs
Files: *.md at root, audit trail files
```

### Minimal (Agent Core Only)
```
Directories: .agent
Files: None
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| "fatal: not a git repository" | Must run from git repo |
| "error: branch already exists" | Use different name or delete existing |
| "fatal: worktree already exists" | Remove existing worktree first |
| "error: pathspec did not match" | Path doesn't exist in base branch (ok to skip) |

---

## Related Skills

- `agent-ops-git` — General git operations
- `agent-ops-implementation` — Creates files that get logged
- `agent-ops-validation` — Run before creating clean branch
