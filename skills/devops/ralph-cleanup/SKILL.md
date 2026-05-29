---
name: ralph-cleanup
description: Remove worktrees after successful PR merge. Cleans up git worktrees, branches, and updates manifest.
triggers:
  - /ralph.cleanup
  - cleanup worktrees
  - remove agents
---

# /ralph.cleanup

Remove worktrees after successful PR merge.

## Prerequisites

- PR should be merged to main
- All agents for the epic should be COMPLETE
- Run `/ralph.memory-sync` to ensure all memories are synced before cleanup

## Process

1. **Verify PR merged**
   ```bash
   gh pr list --state merged --search "EP001"
   ```

2. **Remove worktree directories**
   ```bash
   for worktree in ../floe-agent-{epic}-*; do
     git worktree remove "$worktree" --force
   done
   ```

3. **Prune git worktree metadata**
   ```bash
   git worktree prune
   ```

4. **Delete merged branches locally**
   ```bash
   git branch -d feature/{epic}-{task}
   ```

5. **Delete remote branches**
   ```bash
   git push origin --delete feature/{epic}-{task}
   ```

6. **Update manifest.json**
   - Move agents from `active_agents` to `completed_today`
   - Update statistics

7. **Archive activity logs** (optional)
   - Move `.agent/activity.md` to `logs/{epic}/`

## Output

```
RALPH WIGGUM CLEANUP - EP001

Worktrees removed: 5
  - ../floe-agent-ep001-auth
  - ../floe-agent-ep001-catalog
  - ../floe-agent-ep001-models
  - ../floe-agent-ep001-tests
  - ../floe-agent-ep001-integration

Branches deleted (local): 5
Branches deleted (remote): 5

Manifest updated:
  Active agents: 0
  Completed today: +5 (total: 12)
  Average duration: 42 min

Git worktree status:
  (only main worktree remains)
```

## Partial Cleanup

To clean up specific worktrees:

```bash
# Remove single worktree
git worktree remove ../floe-agent-ep001-auth --force

# Delete specific branch
git branch -d feature/ep001-auth
git push origin --delete feature/ep001-auth
```

## Stale Worktree Detection

Worktrees are considered stale after 24 hours without commits:

```bash
# List stale worktrees
git worktree list | while read worktree branch _; do
  if [[ "$worktree" == *"floe-agent"* ]]; then
    last_commit=$(cd "$worktree" && git log -1 --format=%ct)
    age_hours=$(( ($(date +%s) - last_commit) / 3600 ))
    if [ $age_hours -gt 24 ]; then
      echo "STALE: $worktree (${age_hours}h)"
    fi
  fi
done
```

## Force Cleanup

To remove all agent worktrees regardless of state:

```bash
# WARNING: This will remove all work in worktrees
git worktree list | grep "floe-agent" | cut -d' ' -f1 | \
  xargs -I{} git worktree remove {} --force

git worktree prune
```

## Recovery

If cleanup was accidental:

```bash
# Branches still exist on remote
git fetch origin

# Recreate worktree from remote branch
git worktree add ../floe-agent-ep001-auth feature/ep001-auth
```

## Configuration

From `.ralph/config.yaml`:
- `auto_cleanup`: true (remove after merge)
- `stale_worktree_hours`: 24
- `archive_activity_logs`: true

## Linear Update

After cleanup, update Linear issues:

```
mcp__plugin_linear_linear__update_issue({
  "id": task_id,
  "state": "completed"
})

mcp__plugin_linear_linear__create_comment({
  "issueId": task_id,
  "body": "Task completed and merged. Worktree cleaned up."
})
```

## Related Commands

- `/ralph.spawn` - Start agents
- `/ralph.status` - Check progress
- `/ralph.integrate` - Prepare for PR
