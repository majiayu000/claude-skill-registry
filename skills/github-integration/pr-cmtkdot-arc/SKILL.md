---
name: pr
description: Use when the user wants to create, update, or submit a pull request or merge request. Handles GitHub (gh) and GitLab (glab) workflows with git-workflow safety rails.
invocation: agent
---

# PR/MR Description Creator

Generate PR/MR descriptions and apply directly using `gh` (GitHub) or `glab` (GitLab) CLI.

**Requires**: `gh` or `glab` CLI installed and authenticated.

Uses `git-workflow` skill for safety rails.

## Instructions

### Step 1: Detect Platform

```bash
git remote get-url origin 2>/dev/null
```

- `github.com` → GitHub → use `gh`
- `gitlab` → GitLab → use `glab`
- Unclear → Ask user

### Step 2: Validate Environment

Check CLI authentication:
```bash
gh auth status    # GitHub
glab auth status  # GitLab
```

- Not installed → Report install link
- Not authenticated → Report auth command
- On main/master → Report error (need feature branch)

### Step 3: Determine Action

```bash
gh pr view --json number -q '.number' 2>/dev/null
```

- PR/MR exists → `update`
- No PR/MR → `create`

### Step 4: Gather Git Context

```bash
git log main..HEAD --oneline
git diff main...HEAD --stat
git rev-list --count main..HEAD
```

### Step 5: Launch Agent

**REQUIRED Task tool parameters:**
```
subagent_type: "arc:pr-description-creator"
run_in_background: true
prompt: "Generate PR description:\nPlatform: <platform>\nCLI: <cli>\nAction: <action>\nBranch: <current> -> <base>\nTemplate: <custom or default>\nCommits: <count>"
```

Output a status message and **end your turn**.

### Step 6: Report Result

```
## PR/MR <CREATED/UPDATED>

**Platform**: <GitHub or GitLab>
**URL**: <url>
**Branch**: <current> -> <base>
```

## Error Handling

| Scenario | Action |
|----------|--------|
| CLI not installed | Report install link |
| Not authenticated | Report auth command |
| Can't detect platform | Ask user |
| On main/master | Report error |
