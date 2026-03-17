---
name: update
description: 'Reinstall all AgentOps skills globally from the latest source. Triggers: "update skills", "reinstall skills", "sync skills".'
disable-model-invocation: true
metadata:
  tier: meta
  dependencies: []
---

# /update — Reinstall AgentOps Skills

> **Purpose:** One command to pull the latest skills from the repo and install them globally across all agents.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

---

## Execution

### Step 1: Install

```bash
npx skills@latest add boshu2/agentops --all -g
```

Run this command. Wait for it to complete.

### Step 2: Verify

Confirm the output shows all skills installed with no failures.

If any skills failed to install, report which ones failed and suggest re-running or manual sync:
```bash
# Manual sync for a failed skill (replace <skill-name>):
yes | cp -r skills/<skill-name>/ ~/.claude/skills/<skill-name>/
```

### Step 3: Report

Tell the user:
1. How many skills installed successfully
2. Any failures and how to fix them

## Examples

### Routine skill update

**User says:** `/update`

**What happens:**
1. Runs `npx skills@latest add boshu2/agentops --all -g` to pull the latest skills from the repository and install them globally.
2. Verifies the output confirms all skills installed with no failures.
3. Reports the total count of successfully installed skills.

**Result:** All AgentOps skills are updated to the latest version and available globally across all agent sessions.

### Recovering from a partial failure

**User says:** `/update` (after a previous run failed for some skills)

**What happens:**
1. Runs `npx skills@latest add boshu2/agentops --all -g` which re-attempts installation of all skills from the latest source.
2. Detects that 2 of 30 skills failed to install and identifies them by name.
3. Reports the failures and provides manual sync commands (e.g., `yes | cp -r skills/<name>/ ~/.claude/skills/<name>/`) as a fallback.

**Result:** 28 skills installed successfully, with clear instructions to manually sync the 2 that failed.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `npx: command not found` | Node.js/npm is not installed or not on PATH | Install Node.js (v18+) via Homebrew (`brew install node`) or your preferred package manager |
| `ERR! 404 Not Found` from npx | The `skills` package or the `boshu2/agentops` repository is unreachable | Check network connectivity and verify the repository exists. If behind a proxy, configure npm proxy settings |
| Individual skills fail to install while others succeed | Permissions issue or corrupted skill directory in `~/.claude/skills/` | Use the manual sync fallback: `yes \| cp -r skills/<skill-name>/ ~/.claude/skills/<skill-name>/` |
| Skills installed but not available in new sessions | The global skills directory (`~/.claude/skills/`) is not on the agent's skill search path | Verify `~/.claude/skills/` exists and contains the installed skill directories. Restart the agent session |
| `EACCES: permission denied` during install | The `~/.claude/skills/` directory has restrictive permissions | Fix with `chmod -R u+rwX ~/.claude/skills/` and re-run `/update` |
