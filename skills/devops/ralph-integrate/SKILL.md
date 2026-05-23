---
name: ralph-integrate
description: Integrate completed agent work by rebasing all feature branches on main. Prepares for pre-PR review phase.
triggers:
  - /ralph.integrate
  - integrate branches
  - prepare for review
---

# /ralph.integrate [epic]

Rebase all completed feature branches on main and prepare for pre-PR review.

## Prerequisites

- **Pre-flight check**: Run `/ralph.preflight` to verify Linear MCP is authenticated
- All agents for the epic should be COMPLETE
- Run `/ralph.status` to verify completion

## Process

1. **Verify all agents complete**
   ```bash
   cat .ralph/manifest.json | jq '.active_agents[] | select(.epic == "EP001")'
   ```

2. **Fetch latest main**
   ```bash
   git fetch origin main
   ```

3. **Rebase each feature branch**
   ```bash
   for worktree in ../floe-agent-{epic}-*; do
     cd "$worktree"
     git rebase origin/main
   done
   ```

4. **Detect and report conflicts**
   - If rebase fails, report conflicting files
   - Signal for human intervention

5. **Run full test suite** on rebased code
   ```bash
   uv run pytest tests/ -v
   ```

6. **Update manifest** with integration status

## Output

### Success

```
INTEGRATION STATUS - EP001

Worktrees to integrate: 5
Rebased successfully: 5
Conflicts detected: 0

All tests pass: YES (47/47)

Ready for pre-PR review:
  /speckit.test-review
  /security-review
  /arch-review
```

### Conflict Detected

```
INTEGRATION STATUS - EP001

Worktrees to integrate: 5
Rebased successfully: 4
Conflicts detected: 1 (T003)

Conflict in T003:
  - packages/floe-core/schemas.py
  - Cause: CompiledArtifacts schema changed on main

Action required: Resolve T003 conflict before proceeding

To resolve:
  cd ../floe-agent-ep001-t003
  git status  # See conflicting files
  # Edit files to resolve conflicts
  git add -A
  git rebase --continue
```

## Conflict Resolution

### Manual Resolution

```bash
# 1. Enter conflicting worktree
cd ../floe-agent-ep001-t003

# 2. See conflicting files
git status

# 3. Edit and resolve conflicts
# ... make changes ...

# 4. Mark resolved
git add -A

# 5. Continue rebase
git rebase --continue

# 6. Re-run integration
/ralph.integrate EP001
```

### Abort and Reschedule

```bash
# If conflict is complex
cd ../floe-agent-ep001-t003
git rebase --abort

# Option: Merge instead of rebase
git merge origin/main
# Resolve conflicts
git commit
```

## Pre-PR Review Checklist

After successful integration:

1. **Test Quality**
   ```
   /speckit.test-review
   ```

2. **Security Review**
   ```
   /security-review
   ```

3. **Architecture Review**
   ```
   /arch-review
   ```

4. **PR Creation** (after reviews pass)
   ```bash
   gh pr create --base main --title "EP001: Feature implementation"
   ```

## Configuration

From `.ralph/config.yaml`:
- `rebase_strategy`: "rebase" (default) or "merge"
- `run_tests_after_rebase`: true

## Related Commands

- `/ralph.spawn` - Start agents
- `/ralph.status` - Check progress
- `/ralph.cleanup` - Clean up after merge
- `/speckit.test-review` - Test quality review
- `/security-review` - Security scan
- `/arch-review` - Architecture alignment
