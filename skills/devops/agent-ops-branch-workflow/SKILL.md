---
name: agent-ops-branch-workflow
description: "Standardized branch creation with type detection, issue ID extraction, and worktree setup. Creates working branches (-WB) and integrates with selective-copy for clean PRs."
category: utility
invokes: [agent-ops-git, agent-ops-selective-copy, agent-ops-interview]
invoked_by: []
state_files:
  read: [focus.md, constitution.md]
  write: [focus.md]
reference: [../../.agent/issues/references/FEAT-0305@p8q9r0.md]
---

# Branch Workflow — Standardized Branch Creation

> Create working branches with consistent naming from task descriptions. Platform agnostic.

**Works with or without `aoc` CLI.** Uses standard git commands.

---

## Purpose

Standardize branch creation with:
1. **Type detection** — Auto-detect bug/feature/refactor from description
2. **Issue ID extraction** — JIRA, GitHub, or internal issue references
3. **Slug generation** — Short, URL-safe names from descriptions
4. **Worktree setup** — Parallel development without branch switching
5. **Clean branch integration** — Seamless handoff to selective-copy

---

## CRITICAL: No Assumptions

> **NEVER assume. NEVER guess. ALWAYS ask.**

**Before creating ANY branch, confirm with user:**

| If unclear about... | ASK |
|---------------------|-----|
| Task description | "What is the task? Please include issue ID if available." |
| Source branch | "Which branch should I base this on? (e.g., develop, main)" |
| Branch type | "I detected this as a [type]. Is that correct?" |
| Issue ID | "I found [ID]. Is this the correct issue reference?" |
| Generated name | "I'll create branch `{name}`. Does this look right?" |

**If ANY of these are ambiguous:**
1. Stop
2. Ask ONE question at a time
3. Wait for explicit confirmation
4. Only proceed when ALL inputs are confirmed

**NEVER:**
- Guess the source branch
- Assume `main` or `develop` without asking
- Create a branch without showing the user the exact name first
- Proceed if the task description is vague

---

## Branch Naming Convention

```
Working branch: {type}/{ID}-{slug}-WB
Clean branch:   {type}/{ID}-{slug}
```

**Examples:**
| Task | Working Branch | Clean Branch |
|------|---------------|--------------|
| "GATS-0666: Add auth support" | `feature/GATS-0666-add-auth-WB` | `feature/GATS-0666-add-auth` |
| "Fix #123 login timeout" | `bugfix/123-login-timeout-WB` | `bugfix/123-login-timeout` |
| "Refactor database layer" | `refactor/db-layer-WB` | `refactor/db-layer` |

---

## Invocation

User says something like:
- "Create a branch for GATS-0666: Add authentication"
- "Start working on fix for login timeout bug"
- "New feature branch based on develop"

---

## Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `task_description` | Description of work (for type/ID/slug detection) | Yes | - |
| `source_branch` | Branch to base new branch on | Yes | - |
| `branch_name` | Override auto-generated name | No | Auto-generated |

---

## Phase 1: Create Working Branch

### Step 1: Gather Requirements

**If not provided, ask:**

```
To create your working branch, I need:

1. What's the task? (include issue ID if you have one)
   Example: "GATS-0666: Add OAuth2 authentication support"

2. Which branch should I base this on?
   Example: develop, main, release/v2.0
```

### Step 2: Detect Branch Type

Analyze the task description to determine type:

| Keywords | Type |
|----------|------|
| hotfix, critical, urgent, emergency | `hotfix/` |
| fix, bug, error, crash, broken, issue | `bugfix/` |
| refactor, cleanup, restructure, reorganize | `refactor/` |
| doc, readme, changelog, documentation | `docs/` |
| chore, deps, dependency, maintenance, update | `chore/` |
| *(default)* feature, add, implement, create | `feature/` |

```powershell
# PowerShell - Type Detection
function Get-BranchType {
    param([string]$Description)
    
    $desc = $Description.ToLower()
    
    if ($desc -match 'hotfix|critical|urgent|emergency') { return 'hotfix' }
    if ($desc -match 'fix|bug|error|crash|broken|issue') { return 'bugfix' }
    if ($desc -match 'refactor|cleanup|restructure|reorganize') { return 'refactor' }
    if ($desc -match 'doc|readme|changelog') { return 'docs' }
    if ($desc -match 'chore|deps|dependency|maintenance|update') { return 'chore' }
    
    return 'feature'
}
```

```bash
# Bash - Type Detection
get_branch_type() {
    local desc="${1,,}"  # lowercase
    
    if [[ "$desc" =~ hotfix|critical|urgent|emergency ]]; then echo "hotfix"; return; fi
    if [[ "$desc" =~ fix|bug|error|crash|broken|issue ]]; then echo "bugfix"; return; fi
    if [[ "$desc" =~ refactor|cleanup|restructure|reorganize ]]; then echo "refactor"; return; fi
    if [[ "$desc" =~ doc|readme|changelog ]]; then echo "docs"; return; fi
    if [[ "$desc" =~ chore|deps|dependency|maintenance|update ]]; then echo "chore"; return; fi
    
    echo "feature"
}
```

### Step 3: Extract Issue ID

Look for issue identifiers in the description:

| Pattern | Example | Type |
|---------|---------|------|
| `[A-Z]{2,10}-\d+` | GATS-0666, PROJ-123 | JIRA |
| `#\d+` | #456 | GitHub |
| `[A-Z]+-\d+@\w+` | FEAT-0305@p8q9r0 | Internal |

```powershell
# PowerShell - Issue ID Extraction
function Get-IssueId {
    param([string]$Description)
    
    # JIRA pattern: PROJECT-123
    if ($Description -match '([A-Z]{2,10}-\d+)') {
        return @{ Id = $Matches[1]; Type = 'jira' }
    }
    
    # GitHub pattern: #123
    if ($Description -match '#(\d+)') {
        return @{ Id = $Matches[1]; Type = 'github' }
    }
    
    # Internal AgentOps pattern
    if ($Description -match '([A-Z]+-\d+)@\w+') {
        return @{ Id = $Matches[1]; Type = 'internal' }
    }
    
    return @{ Id = $null; Type = 'none' }
}
```

```bash
# Bash - Issue ID Extraction
get_issue_id() {
    local desc="$1"
    
    # JIRA pattern
    if [[ "$desc" =~ ([A-Z]{2,10}-[0-9]+) ]]; then
        echo "${BASH_REMATCH[1]}"
        return
    fi
    
    # GitHub pattern
    if [[ "$desc" =~ \#([0-9]+) ]]; then
        echo "${BASH_REMATCH[1]}"
        return
    fi
    
    # Internal pattern
    if [[ "$desc" =~ ([A-Z]+-[0-9]+)@ ]]; then
        echo "${BASH_REMATCH[1]}"
        return
    fi
    
    echo ""
}
```

### Step 4: Generate Slug

Create a short, URL-safe name from the description:

```powershell
# PowerShell - Slug Generation
function Get-BranchSlug {
    param(
        [string]$Description,
        [string]$IssueId,
        [int]$MaxLength = 30
    )
    
    $text = $Description
    
    # Remove issue ID
    if ($IssueId) {
        $text = $text -replace [regex]::Escape($IssueId), ''
    }
    
    # Remove common prefixes
    $text = $text -replace '^(fix|bug|feature|add|implement|create|update|refactor)[:.\s]+', ''
    
    # Convert to lowercase, replace non-alphanumeric with dashes
    $slug = ($text.ToLower() -replace '[^a-z0-9]+', '-').Trim('-')
    
    # Truncate at word boundary
    if ($slug.Length -gt $MaxLength) {
        $slug = $slug.Substring(0, $MaxLength)
        if ($slug.Contains('-')) {
            $slug = $slug.Substring(0, $slug.LastIndexOf('-'))
        }
    }
    
    if ([string]::IsNullOrEmpty($slug)) { $slug = 'work' }
    
    return $slug
}
```

```bash
# Bash - Slug Generation
get_branch_slug() {
    local desc="$1"
    local issue_id="$2"
    local max_length="${3:-30}"
    
    local text="$desc"
    
    # Remove issue ID
    if [ -n "$issue_id" ]; then
        text="${text//$issue_id/}"
    fi
    
    # Remove common prefixes
    text=$(echo "$text" | sed -E 's/^(fix|bug|feature|add|implement|create|update|refactor)[:. ]+//i')
    
    # Convert to lowercase, replace non-alphanumeric with dashes
    local slug=$(echo "$text" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//;s/-$//')
    
    # Truncate
    if [ ${#slug} -gt $max_length ]; then
        slug="${slug:0:$max_length}"
        slug="${slug%-*}"  # Remove partial word
    fi
    
    [ -z "$slug" ] && slug="work"
    
    echo "$slug"
}
```

### Step 5: Build Branch Name

```powershell
# PowerShell
$type = Get-BranchType -Description $TaskDescription
$issueInfo = Get-IssueId -Description $TaskDescription
$slug = Get-BranchSlug -Description $TaskDescription -IssueId $issueInfo.Id

if ($BranchName) {
    $workingBranch = $BranchName
} elseif ($issueInfo.Id) {
    $workingBranch = "$type/$($issueInfo.Id)-$slug-WB"
} else {
    $workingBranch = "$type/$slug-WB"
}

Write-Host "Branch type: $type"
Write-Host "Issue ID: $($issueInfo.Id ?? 'none')"
Write-Host "Slug: $slug"
Write-Host "Working branch: $workingBranch"
```

```bash
# Bash
type=$(get_branch_type "$task_description")
issue_id=$(get_issue_id "$task_description")
slug=$(get_branch_slug "$task_description" "$issue_id")

if [ -n "$branch_name" ]; then
    working_branch="$branch_name"
elif [ -n "$issue_id" ]; then
    working_branch="${type}/${issue_id}-${slug}-WB"
else
    working_branch="${type}/${slug}-WB"
fi

echo "Branch type: $type"
echo "Issue ID: ${issue_id:-none}"
echo "Slug: $slug"
echo "Working branch: $working_branch"
```

### Step 6: Create Worktree

```powershell
# PowerShell
# Calculate worktree path (replace / with - for filesystem)
$worktreePath = "../$($workingBranch -replace '/', '-')"

# Ensure source branch exists and is up to date
git fetch origin $SourceBranch 2>$null

# Create worktree with new branch
git worktree add -b $workingBranch $worktreePath "origin/$SourceBranch"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Working branch created successfully" -ForegroundColor Green
    Write-Host "  Branch: $workingBranch"
    Write-Host "  Path: $worktreePath"
    Write-Host "  Based on: $SourceBranch"
    Write-Host "`nTo start working:"
    Write-Host "  cd $worktreePath"
} else {
    Write-Error "Failed to create worktree"
}
```

```bash
# Bash
# Calculate worktree path
worktree_path="../${working_branch//\//-}"

# Ensure source branch exists and is up to date
git fetch origin "$source_branch" 2>/dev/null

# Create worktree with new branch
if git worktree add -b "$working_branch" "$worktree_path" "origin/$source_branch"; then
    echo ""
    echo "✓ Working branch created successfully"
    echo "  Branch: $working_branch"
    echo "  Path: $worktree_path"
    echo "  Based on: $source_branch"
    echo ""
    echo "To start working:"
    echo "  cd $worktree_path"
else
    echo "Error: Failed to create worktree" >&2
    exit 1
fi
```

### Step 7: Update Focus State

After creating the branch, update `.agent/focus.md`:

```powershell
# PowerShell
$cleanBranch = $workingBranch -replace '-WB$', ''

$focusUpdate = @"

## Branch Info

- working_branch: $workingBranch
- clean_branch: $cleanBranch (pending - use selective-copy)
- source_branch: $SourceBranch
- issue_id: $($issueInfo.Id ?? 'none')
- task: $TaskDescription
- worktree_path: $worktreePath
"@

# Append to focus.md or create section
Add-Content -Path ".agent/focus.md" -Value $focusUpdate
```

---

## Phase 2: Create Clean Branch (for PR)

When ready for code review, use `selective-copy` to create the clean branch:

```powershell
# PowerShell
# The clean branch is the working branch without -WB suffix
$cleanBranch = $workingBranch -replace '-WB$', ''

# Invoke selective-copy (manually or via skill)
# This will:
# 1. Create $cleanBranch from $workingBranch
# 2. Exclude .agent/, .github/, and logged files
# 3. Create exclusion log for selective-merge
```

**User command:**
```
Create a clean branch for PR
```

The `selective-copy` skill will:
- Detect the working branch (ends with `-WB`)
- Auto-generate clean branch name (remove `-WB`)
- Exclude agent-ops files
- Create exclusion log

---

## Complete Workflow Example

```powershell
# === PHASE 1: Start Work ===

# User: "Create a branch for GATS-0666: Add OAuth2 authentication"
# Source: develop

# Agent detects:
# - Type: feature
# - Issue ID: GATS-0666
# - Slug: oauth2-auth

# Agent creates:
git worktree add -b feature/GATS-0666-oauth2-auth-WB ../feature-GATS-0666-oauth2-auth-WB origin/develop

# === WORK HAPPENS HERE ===
# Agent assists with implementation in the worktree
# Files logged to .agent/log/created-files.log

# === PHASE 2: Ready for PR ===

# User: "Create a clean branch for PR"
# Agent invokes selective-copy:
# - source: feature/GATS-0666-oauth2-auth-WB
# - target: feature/GATS-0666-oauth2-auth

# Push for review:
cd ../feature-GATS-0666-oauth2-auth
git push origin feature/GATS-0666-oauth2-auth

# === REVIEW CYCLE ===
# After feedback, use selective-merge to sync changes
```

---

## Verification

After branch creation:

```powershell
# PowerShell
Write-Host "`n=== Branch Verification ===" -ForegroundColor Cyan

# List worktrees
Write-Host "`nWorktrees:"
git worktree list

# Show branch info
Write-Host "`nNew branch:"
git -C $worktreePath branch -vv

# Show files
Write-Host "`nFiles in worktree:"
Get-ChildItem $worktreePath -Name | Select-Object -First 10
```

```bash
# Bash
echo ""
echo "=== Branch Verification ==="

# List worktrees
echo ""
echo "Worktrees:"
git worktree list

# Show branch info
echo ""
echo "New branch:"
git -C "$worktree_path" branch -vv

# Show files
echo ""
echo "Files in worktree:"
ls "$worktree_path" | head -10
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Branch already exists" | Name collision | Append timestamp: `{branch}-{yyyyMMdd}` |
| "Source branch not found" | Invalid source | Run `git fetch origin`, verify name |
| "Worktree path exists" | Directory collision | Remove old worktree or use different path |
| "fatal: not a git repository" | Wrong directory | Navigate to git repo root |

### Branch Name Collision

```powershell
# PowerShell - Handle existing branch
$baseBranch = $workingBranch
$counter = 1

while (git show-ref --verify --quiet "refs/heads/$workingBranch") {
    $workingBranch = "$baseBranch-$counter"
    $counter++
}
```

---

## Cleanup

After PR is merged:

```powershell
# PowerShell
# Remove worktree
git worktree remove $worktreePath

# Delete working branch locally
git branch -d $workingBranch

# Delete clean branch locally  
git branch -d $cleanBranch

# Delete remote branches (if desired)
git push origin --delete $workingBranch
git push origin --delete $cleanBranch
```

```bash
# Bash
# Remove worktree
git worktree remove "$worktree_path"

# Delete branches locally
git branch -d "$working_branch"
git branch -d "$clean_branch"

# Delete remote branches (if desired)
git push origin --delete "$working_branch"
git push origin --delete "$clean_branch"
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `agent-ops-selective-copy` | Creates clean branch from working branch |
| `agent-ops-selective-merge` | Syncs working → clean after review feedback |
| `agent-ops-git` | Underlying git operations |
| `agent-ops-implementation` | Logs created files in working branch |
