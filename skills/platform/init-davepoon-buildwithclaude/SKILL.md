---
name: uctm-init
description: Initialize uc-taskmanager for the current project. Creates works/ directory and configures Bash permissions in .claude/settings.local.json. Use when the user says "uctm init", "initialize uctm", "uctm 초기화", or "초기화".
---

# uc-taskmanager Init

Initialize the current project for uc-taskmanager pipeline execution.

## Steps

### 1. Create works/ directory

```
if works/ does not exist:
  create works/
  report: ✓ works/ directory created
else:
  report: - works/ already exists
```

### 2. Configure Bash Permissions

**Ask the user first:** "에이전트에 필요한 Bash 권한을 .claude/settings.local.json에 자동 설정할까요? (recommended) [Y/n]"

If the user approves (or says yes/Y/확인):

Read `.claude/settings.local.json` (create if not exists). Merge the following permissions into `permissions.allow` array — **skip any that already exist** (do not duplicate):

```json
[
  "Read(/**)",
  "Edit(/**)",
  "Write(/**)",
  "Read(**)",
  "Edit(**)",
  "Write(**)",
  "Bash(ls:*)",
  "Bash(cat:*)",
  "Bash(mkdir:*)",
  "Bash(basename:*)",
  "Bash(find:*)",
  "Bash(wc:*)",
  "Bash(sort:*)",
  "Bash(tail:*)",
  "Bash(head:*)",
  "Bash(echo:*)",
  "Bash(printf:*)",
  "Bash(grep:*)",
  "Bash(sed:*)",
  "Bash(cut:*)",
  "Bash(tr:*)",
  "Bash(node:*)",
  "Bash(npm run:*)",
  "Bash(npm test:*)",
  "Bash(bun run:*)",
  "Bash(yarn:*)",
  "Bash(cargo:*)",
  "Bash(go build:*)",
  "Bash(go test:*)",
  "Bash(python:*)",
  "Bash(ruff:*)",
  "Bash(make:*)",
  "Bash(git:*)",
  "Bash(curl:*)"
]
```

Preserve any existing entries in `permissions.allow` and `permissions.deny` — only add missing ones.

```
if permissions added:
  report: ✓ {N} permissions added to .claude/settings.local.json (total: {T})
else if skipped by user:
  report: - Skipped permission setup
else:
  report: - All permissions already configured
```

### 3. Summary

After all steps, show a summary:

```
uc-taskmanager initialized!

  ✓ works/ directory ready
  ✓ Bash permissions configured

  Next: Type [new-feature] Add a hello world feature
```

## Arguments

$ARGUMENTS
