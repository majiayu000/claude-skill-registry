---
name: git-workflow-helper
description: Handle common git scenarios, conflicts, and hook failures
version: 1.1.0
tags: [git, troubleshooting, automation, ssh, github]
owner: devops
status: active
---

# Git Workflow Helper Skill

## Overview

Resolve common git interruptions and ensure correct SSH configuration.

## Usage

```
/git-workflow-helper
```

## Identity
**Role**: Git Workflow Specialist
**Objective**: Automate the resolution of common git interruptions (merge conflicts, rebase stopping, hook failures) and ensure proper SSH configuration for GitHub.

## CRITICAL: Always Use SSH for GitHub

**All GitHub operations MUST use SSH, never HTTPS.**

### Why SSH?
- No password prompts on every push/pull
- More secure (key-based authentication)
- Required for automated workflows
- Works with 2FA without tokens

### Verify Current Remote
```bash
# Check current remote URL
git remote -v

# If you see HTTPS (bad):
# origin  https://github.com/user/repo.git (fetch)

# Should be SSH (good):
# origin  git@github.com:user/repo.git (fetch)
```

### Convert HTTPS to SSH
```bash
# Convert origin from HTTPS to SSH
git remote set-url origin git@github.com:USERNAME/REPOSITORY.git

# Verify the change
git remote -v
```

### SSH URL Format
```
# GitHub SSH format
git@github.com:OWNER/REPO.git

# Examples
git@github.com:anthropics/claude-code.git
git@github.com:myorg/myproject.git
```

### Clone with SSH (Always)
```bash
# CORRECT - Use SSH
git clone git@github.com:owner/repo.git

# WRONG - Never use HTTPS
# git clone https://github.com/owner/repo.git
```

### SSH Setup (One-Time)

**1. Generate SSH Key** (if not exists):
```bash
# Check for existing keys
ls -la ~/.ssh/id_ed25519.pub

# Generate new key (Ed25519 recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Or RSA if Ed25519 not supported
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

**2. Add Key to SSH Agent**:
```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519
```

**3. Add Public Key to GitHub**:
```bash
# Copy public key
cat ~/.ssh/id_ed25519.pub
# Then add at: GitHub → Settings → SSH and GPG keys → New SSH key
```

**4. Test Connection**:
```bash
ssh -T git@github.com
# Should see: "Hi USERNAME! You've successfully authenticated..."
```

### SSH Config for Multiple Accounts
```bash
# ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work

# Usage: git clone git@github-work:company/repo.git
```

### Troubleshooting SSH

| Error | Solution |
|-------|----------|
| "Permission denied (publickey)" | Key not added to GitHub or ssh-agent |
| "Host key verification failed" | Run `ssh-keyscan github.com >> ~/.ssh/known_hosts` |
| "Connection timed out" | Firewall blocking port 22, try SSH over HTTPS port (see below) |
| "Could not resolve hostname" | DNS issue, check network connection |

**SSH Over HTTPS Port** (if port 22 blocked):
```bash
# ~/.ssh/config
Host github.com
    HostName ssh.github.com
    Port 443
    User git
    IdentityFile ~/.ssh/id_ed25519
```

### Auto-Convert HTTPS to SSH (Git Config)
```bash
# Global setting: automatically rewrite HTTPS to SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"

# Verify
git config --global --get-regexp url
```

---

## Scenarios & Playbooks

### Scenario A: Pre-Commit Hook Failure
**Trigger**: `git commit` exits with code > 0.
**Action**:
1.  **Analyze Log**: Grep stdout/stderr for keywords: `eslint`, `prettier`, `test failed`.
2.  **Fix**:
    - If lint error: Run `npm run lint:fix` (or equivalent).
    - If format error: Run `npm run format`.
    - If test failure: Check if failure is related to staged changes.
3.  **Recover**:
    - `git add <fixed-files>`
    - Retry the commit.
4.  **Fallback**: If fix is complex or manual, notify user. Only use `git commit --no-verify` if explicitly authorized.

### Scenario B: Merge/Rebase Conflict
**Trigger**: `git merge` or `git rebase` stops with "CONFLICT".
**Action**:
1.  **Identify**: Run `git status` to see `both modified` files.
2.  **Resolve**:
    - For lockfiles (`package-lock.json`, `pnpm-lock.yaml`): **Discard** changes and regenerate (`npm install`). Do not attempt text merge on lockfiles.
    - For source code:
        - Read conflict markers.
        - Start with 'Incoming Change' or 'Current Change' logic depending on context (e.g., if rebasing strict-feature on main, honor main).
3.  **Continue**:
    - `git add <resolved-files>`
    - `git rebase --continue` (or `git commit` for merge).
4.  **Abort**: If loop detected (same conflict > 2 times), run `git rebase --abort`.

### Scenario C: Undo/Rewrite
**Trigger**: User wants to undo last commit or change message.
**Action**:
- **Undo Last Commit (Soft)**: `git reset --soft HEAD~1` (keeps changes staged).
- **Amend Message**: `git commit --amend` (opens editor) or `git commit --amend -m "new message"`.
- **Discard All Local Changes**: `git reset --hard HEAD` (WARNING: Data Loss).

### Scenario D: SSH Authentication Failure
**Trigger**: `git push` or `git pull` fails with "Permission denied (publickey)" or similar.
**Action**:
1.  **Check Remote URL**:
    ```bash
    git remote -v
    ```
    - If HTTPS: Convert to SSH (see "Convert HTTPS to SSH" above).
2.  **Verify SSH Agent**:
    ```bash
    ssh-add -l
    # If "Could not open connection to agent", start it:
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
    ```
3.  **Test GitHub Connection**:
    ```bash
    ssh -T git@github.com
    ```
4.  **If Still Failing**:
    - Verify key is added to GitHub: `cat ~/.ssh/id_ed25519.pub`
    - Check SSH config: `cat ~/.ssh/config`
    - Try verbose mode: `ssh -vT git@github.com`

### Scenario E: HTTPS Remote Detected
**Trigger**: During any git operation, detect HTTPS remote.
**Action**:
1.  **Auto-Convert to SSH**:
    ```bash
    # Get current URL
    CURRENT_URL=$(git remote get-url origin)

    # If HTTPS, convert
    if [[ "$CURRENT_URL" == https://github.com/* ]]; then
        # Extract owner/repo from HTTPS URL
        SSH_URL=$(echo "$CURRENT_URL" | sed 's|https://github.com/|git@github.com:|')
        git remote set-url origin "$SSH_URL"
        echo "Converted to SSH: $SSH_URL"
    fi
    ```
2.  **Verify**: `git remote -v`
3.  **Proceed** with original operation.

## Safety Constraints
- **Never** Force Push (`git push -f`) on `main` or `master` branch.
- **Never** `git reset --hard` without explicit user confirmation of data loss.
- **Always** verify state (`git status`) before and after operations.

## Outputs

- Cleaned git state or a clear recovery path.

## Related Skills

- `/pr-create` - Create pull requests after fixes
