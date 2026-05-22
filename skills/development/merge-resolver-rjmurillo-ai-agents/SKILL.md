---
name: merge-resolver
version: 2.0.0
description: Resolve merge conflicts by analyzing git history and commit intent. Use when PR has conflicts with base branch, can't merge due to conflicts, or need to fix merge conflicts systematically with session protocol validation.
license: MIT
model: claude-opus-4-5
metadata:
  domains:
  - git
  - github
  - merge-conflicts
  - pr-maintenance
  type: workflow
  complexity: advanced
  adr: ADR-015
---
# Merge Resolver

Resolve merge conflicts by analyzing git history and commit intent.

## Triggers

Use this skill when you encounter:

- `resolve merge conflicts for PR #123`
- `PR has conflicts with main`
- `can't merge - conflicts detected`
- `fix the merge conflicts in this branch`
- `help me resolve conflicts for this pull request`

## Process

### Phase 1: Context Gathering

| Step | Action | Verification |
|------|--------|--------------|
| 1.1 | Fetch PR metadata | JSON response received |
| 1.2 | Checkout PR branch | `git branch --show-current` matches |
| 1.3 | Attempt merge with base | Conflict markers created |
| 1.4 | List conflicted files | `git diff --name-only --diff-filter=U` output |

### Phase 2: Analysis and Resolution

| Step | Action | Verification |
|------|--------|--------------|
| 2.1 | Classify files (auto-resolvable vs manual) | Classification logged |
| 2.2 | Auto-resolve template/session files | Accept --theirs successful |
| 2.3 | For manual: Run git blame, analyze intent | Commit messages captured |
| 2.4 | Apply manual resolutions per strategy | Conflict markers removed |
| 2.5 | Stage all resolved files | `git diff --check` clean |

### Phase 3: Validation (BLOCKING)

| Step | Action | Verification |
|------|--------|--------------|
| 3.1 | Verify session log exists | File at `.agents/sessions/` |
| 3.2 | Run session protocol validator | Exit code 0 |
| 3.3 | Run markdown lint | No errors |
| 3.4 | Commit merge resolution | Commit SHA recorded |
| 3.5 | Push to remote | Push successful |

## Workflow (Quick Reference)

1. **Fetch PR context** - Get title, description, commits
2. **Identify conflicts** - Find conflicted files in working directory
3. **Analyze each conflict** - Use git blame and commit messages
4. **Determine intent** - Classify changes by type
5. **Apply resolution** - Keep, merge, or discard based on analysis
6. **Stage resolved files** - Prepare for commit
7. **Validate session protocol** - BLOCKING: Run validation before push

## Step 1: Fetch PR Context

```bash
# Get PR metadata
gh pr view <number> --json title,body,commits,headRefName,baseRefName

# Checkout the PR branch
gh pr checkout <number>

# Attempt merge with base (creates conflict markers)
git merge origin/<base-branch> --no-commit
```

## Step 2: Identify Conflicts

```bash
# List conflicted files
git diff --name-only --diff-filter=U

# Show conflict details
git status --porcelain | grep "^UU"
```

## Step 3: Analyze Each Conflict

For each conflicted file:

```bash
# View the conflict
git diff --check

# Get blame for conflicting lines (base version)
git blame <base-branch> -- <file> | grep -n "<line-content>"

# Get blame for conflicting lines (head version)
git blame HEAD -- <file> | grep -n "<line-content>"

# Show commits touching this file on each branch
git log --oneline <base-branch>..<head-branch> -- <file>
git log --oneline <head-branch>..<base-branch> -- <file>

# View specific commit details
git show --stat <commit-sha>
```

## Step 4: Determine Intent

Classify each side's changes:

| Type | Indicators | Priority |
|------|------------|----------|
| Bugfix | "fix", "bug", "patch", "hotfix" in message; small, targeted change | Highest |
| Security | "security", "vuln", "CVE" in message | Highest |
| Refactor | "refactor", "cleanup", "rename"; no behavior change | Medium |
| Feature | "feat", "add", "implement"; new functionality | Medium |
| Style | "style", "format", "lint"; whitespace/formatting only | Lowest |

## Step 5: Apply Resolution

**Decision Framework:**

1. **Same intent, compatible changes** - Merge both
2. **Bugfix vs feature** - Bugfix wins, integrate feature around it
3. **Conflicting logic** - Prefer the more recent or more tested change
4. **Style conflicts** - Accept either, prefer consistency with surrounding code
5. **Deletions vs modifications** - Investigate why; deletion usually intentional

**Resolution Commands:**

```bash
# Accept theirs (base branch)
git checkout --theirs <file>

# Accept ours (PR branch)
git checkout --ours <file>

# Manual edit then mark resolved
git add <file>
```

**For manual resolution:**

1. Open file in editor
2. Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Combine changes logically based on intent analysis
4. Verify syntax and logic
5. Stage the file

## Step 6: Stage and Verify

```bash
# Stage all resolved files
git add <resolved-files>

# Verify no remaining conflicts
git diff --check

# Show staged changes
git diff --cached --stat
```

## Step 7: Validate Session Protocol (BLOCKING)

**MUST complete before pushing.** This step prevents CI failures from incomplete session logs.

### Why This Matters

Session protocol validation is a CI blocking gate. Pushing without completing session requirements causes:

- CI failures with "MUST requirement(s) not met" errors
- Wasted review cycles
- Confusion about root cause (often misidentified as template sync issues)

### Validation Steps

```bash
# 1. Ensure session log exists
SESSION_LOG=$(ls -t .agents/sessions/*.md 2>/dev/null | head -1)
if [ -z "$SESSION_LOG" ]; then
    echo "ERROR: No session log found. Create one before pushing."
    exit 1
fi

# 2. Run session protocol validator
pwsh scripts/Validate-SessionJson.ps1 -SessionLogPath "$SESSION_LOG"

# 3. If validation fails, fix issues before proceeding
if [ $? -ne 0 ]; then
    echo "ERROR: Session protocol validation failed."
    echo "Complete all MUST requirements in your session log before pushing."
    exit 1
fi
```

### Session End Checklist (REQUIRED)

Before pushing, verify your session log contains:

| Req | Step | Status |
|-----|------|--------|
| MUST | Complete session log (all sections filled) | [ ] |
| MUST | Update Serena memory (cross-session context) | [ ] |
| MUST | Run markdown lint | [ ] |
| MUST | Route to qa agent (feature implementation) | [ ] |
| MUST | Commit all changes (including .serena/memories) | [ ] |
| MUST NOT | Update `.agents/HANDOFF.md` directly | [ ] |

### Common Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `E_TEMPLATE_DRIFT` | Session checklist outdated | Copy canonical checklist from SESSION-PROTOCOL.md |
| `E_QA_EVIDENCE` | QA row checked but no report path | Add QA report or use "SKIPPED: docs-only" for docs-only sessions |
| `E_DIRTY_WORKTREE` | Uncommitted changes | Stage and commit all files including `.agents/` |

## Resolution Strategies

See `references/strategies.md` for detailed patterns:

**Code Conflicts:**

- Combining additive changes
- Handling moved code
- Resolving import conflicts
- Dealing with deleted code
- Conflicting logic resolution

**Infrastructure Conflicts:**

- Package lock files (regenerate, don't merge)
- Configuration files (JSON/YAML semantic merge)
- Database migrations (renumber, preserve order)

**Documentation Conflicts:**

- Numbered documentation (ADR, RFC) - renumber incoming to next available
- Template-generated files - resolve in template, regenerate outputs
- Rebase add/add conflicts - per-commit resolution during rebase

## Auto-Resolution Script

For automated conflict resolution in CI/CD, use `scripts/Resolve-PRConflicts.ps1`:

```powershell
# Resolve conflicts for a PR
pwsh .claude/skills/merge-resolver/scripts/Resolve-PRConflicts.ps1 \
    -PRNumber 123 \
    -BranchName "fix/my-feature" \
    -TargetBranch "main"
```

### Auto-Resolvable Files

The following files are automatically resolved by accepting the target branch version:

| Pattern | Rationale |
|---------|-----------|
| `.agents/*` | Session artifacts, constantly changing |
| `.serena/*` | Serena memories, auto-generated |
| `.claude/skills/*/*.md` | Skill definitions, main is authoritative |
| `.claude/commands/*` | Command definitions, main is authoritative |
| `.claude/agents/*` | Agent definitions, main is authoritative |
| `templates/*` | Template files, main is authoritative |
| `src/copilot-cli/*` | Platform agent definitions |
| `src/vs-code-agents/*` | Platform agent definitions |
| `src/claude/*` | Platform agent definitions |
| `.github/agents/*` | GitHub agent configs |
| `.github/prompts/*` | GitHub prompts |
| `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` | Lock files, regenerate from main |

### Script Output

Returns JSON:

```json
{
  "Success": true,
  "Message": "Successfully resolved conflicts for PR #123",
  "FilesResolved": [".agents/HANDOFF.md"],
  "FilesBlocked": []
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - conflicts resolved and pushed |
| 1 | Failure - conflicts in non-auto-resolvable files |

### Security

ADR-015 compliance:

- Branch name validation (prevents command injection)
- Worktree path validation (prevents path traversal)
- Handles both GitHub Actions runner and local environments

## Verification

### Success Criteria

| Criterion | Evidence |
|-----------|----------|
| All conflicts resolved | `git diff --check` returns empty |
| No merge markers remain | `grep -r "<<<<<<" .` returns nothing |
| Session protocol valid | `Validate-SessionJson.ps1` exits 0 |
| Markdown lint passes | `npx markdownlint-cli2` exits 0 |
| Push successful | Remote ref updated |

### Completion Checklist

- [ ] All conflicted files staged (`git add`)
- [ ] No UU status in `git status --porcelain`
- [ ] Session log at `.agents/sessions/YYYY-MM-DD-session-NN.json`
- [ ] Session End checklist completed
- [ ] Serena memory updated
- [ ] Merge commit created
- [ ] Branch pushed to origin

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| Push without session validation | CI blocks with MUST violations | Run `Validate-SessionJson.ps1` first |
| Manual edit of generated files | Changes lost on regeneration | Edit template, run generator |
| Accept --ours for HANDOFF.md | Branch version often stale | Accept --theirs (main is canonical) |
| Merge lock files manually | JSON corruption, broken deps | Accept base, regenerate with npm/yarn |
| Skip git blame analysis | Wrong intent inference | Always check commit messages |
| Resolve before fetching | Missing context, wrong base | Always `gh pr view` first |
| Forget to stage .agents/ | Dirty worktree CI failure | Include all `.agents/` changes |

## Extension Points

### Custom Auto-Resolvable Patterns

Add patterns to `$script:AutoResolvableFiles` in `Resolve-PRConflicts.ps1`:

```powershell
$script:AutoResolvableFiles += @(
    'your/custom/path/*',
    'another/pattern/**'
)
```

### Custom Resolution Strategies

Create new entries in `references/strategies.md` for domain-specific conflicts:

1. Document the conflict pattern
2. Add investigation commands
3. Define resolution priority
4. Provide copy-paste commands

### Integration with CI/CD

The script supports GitHub Actions via environment detection:

```yaml
# In workflow YAML
- name: Resolve conflicts
  env:
    PR_NUMBER: ${{ github.event.pull_request.number }}
    HEAD_REF: ${{ github.head_ref }}
    BASE_REF: ${{ github.base_ref }}
  run: |
    pwsh .claude/skills/merge-resolver/scripts/Resolve-PRConflicts.ps1 \
      -PRNumber "$env:PR_NUMBER" \
      -BranchName "$env:HEAD_REF" \
      -TargetBranch "$env:BASE_REF"
```

### Dry-Run Mode

Use `-WhatIf` for testing without side effects:

```powershell
pwsh scripts/Resolve-PRConflicts.ps1 -PRNumber 123 -BranchName "fix/test" -WhatIf
```

## Related

- **ADR-015**: Security validation for branch names and paths
- **SESSION-PROTOCOL.md**: Session end requirements (blocking gate)
- **strategies.md**: Detailed resolution patterns for edge cases
- **merge-resolver-session-protocol-gap**: Memory documenting root cause analysis
