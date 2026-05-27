---
name: devcontainer-sandboxing
description: Create or harden a devcontainer-based development sandbox so coding agents run inside an isolated container with least privilege and strong guardrails (no destructive host access, controlled network/secrets, reproducible toolchain).
---

# Working Inside a Devcontainer

You are running inside an isolated devcontainer. This container IS your sandbox - it provides stronger isolation than Claude Code's built-in sandbox. Understand these rules to work effectively.

## Key Facts

1. **The container is your sandbox** - You have full permissions inside the container, but the container itself is isolated from the host
2. **Sandbox is disabled** - Claude Code's built-in sandbox causes conflicts with devcontainer isolation. Use `--dangerously-skip-permissions` or the permissive settings are already applied

**In multi-agent mode only** (when `$AGENT_ID` is set):

3. **You may be one of many agents** - Up to 20 agents can run in parallel, each in their own container, sharing the same repository
4. **You own specific packages** - Check your `AGENT_ID` and assigned packages. Only modify files in your owned directories
5. **Use your branch prefix** - All branches must start with `agent-{N}/` to avoid conflicts

## Detecting Your Environment

First, determine if you're in a devcontainer:

```bash
# If this file exists, you're in a container
[ -f /.dockerenv ] && echo "In devcontainer" || echo "On host"
```

### Single-Agent vs Multi-Agent Mode

**Multi-agent mode** (environment variables set):
```bash
echo $AGENT_ID        # Your agent number (1-20)
echo $BRANCH_PREFIX   # Your branch prefix (e.g., "agent-3")
echo $OWNED_PACKAGES  # Directories you may modify
```

**Single-agent mode** (environment variables NOT set):
- You are the only agent - you can modify any package
- Use any branch name (no prefix required)
- No coordination needed with other agents

Check which mode you're in:
```bash
if [ -n "$AGENT_ID" ]; then
  echo "Multi-agent mode: Agent $AGENT_ID"
else
  echo "Single-agent mode: Full repo access"
fi
```

## What You Can Do

- Full filesystem access within `/workspace`
- Run any shell commands
- Install packages with npm/apt (changes don't persist across container restarts)
- Push to Git remote
- Create PRs via `gh` CLI

## What You Must Not Do

1. **Modify files outside your owned packages** - Other agents own those
2. **Work on `main` branch** - Always create a feature branch with your prefix
3. **Run Claude Code with sandbox enabled** - Causes heredoc permission errors
4. **Hold Git locks** - Keep Git operations fast, don't leave uncommitted changes

## Git Workflow

```bash
# 1. Create your branch
git checkout -b $BRANCH_PREFIX/feat-my-improvement

# 2. Make changes (only in your owned packages)
# ...

# 3. Commit and push
git add -A
git commit -m "feat(package): description"
git push -u origin HEAD

# 4. Create PR
gh pr create --title "..." --body "..."
```

**If you see Git lock errors** (`Unable to create '.git/index.lock'`):
- Another agent is running a Git command
- Wait 1-2 seconds and retry
- Don't force-remove the lock file

## Verification

Before creating a PR, verify your devcontainer config passes security checks:

```bash
./verify.sh --stage=devcontainer
```

This checks:
- Non-root user
- No privileged mode
- No Docker socket mount
- Security hardening applied
- No dangerous capabilities

## Heredoc Permission Errors

If you see: `can't create temp file for here document: operation not permitted`

**Cause**: Claude Code's sandbox is conflicting with devcontainer isolation.

**Fix**: You should already be running with sandbox disabled. If not, ensure `~/.claude/settings.json` has:
```json
{
  "sandbox": { "enabled": false }
}
```

## Resource Limits

Your container has limited resources (typically 1-2 GB RAM, 1-2 CPU cores). Avoid:
- Running multiple heavy processes simultaneously
- Large `npm install` operations in parallel with builds
- Memory-intensive operations without cleanup

## Coordination with Other Agents

You share the repository with other agents. To avoid conflicts:

1. **Stay in your lane** - Only modify your owned packages
2. **Branch immediately** - Don't work on detached HEAD or main
3. **Push frequently** - Small, atomic commits reduce merge conflicts
4. **Rebase before PR** - `git pull --rebase origin main` before final push

## Security Footguns to Avoid

See `SECURITY-FOOTGUNS.md` for the full checklist. Key points:

- Never mount Docker socket
- Never run privileged
- Never add SYS_ADMIN or similar capabilities
- Never bake secrets into images
- Never commit `.env` files

## Checking Your Configuration

Verify your devcontainer is properly hardened:

```bash
# Check you're not root
whoami  # Should NOT be "root"

# Check capabilities are dropped
cat /proc/self/status | grep Cap  # CapEff should be minimal

# Check memory limit
cat /sys/fs/cgroup/memory.max  # Should show limit, not "max"
```
