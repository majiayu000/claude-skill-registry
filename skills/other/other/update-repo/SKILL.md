---
name: update-repo
description: Update agent submodules, refresh GitHub star counts, and regenerate README table
---

# Update Repo

Update the repository's agent data: pull latest submodule commits, refresh star counts from GitHub, and regenerate the README agent table.

## Trigger

`/update-repo [agent-name]`

- With `agent-name`: update only that agent's submodule
- Without argument: update all submodules

## Steps

### 1. Update Submodules

```bash
# Update specific agent
./scripts/manage-submodules.sh update <agent-name>

# Or update all
./scripts/manage-submodules.sh update
```

### 1.5. Check Analysis Drift

For each updated agent, if `agents.yaml` has an `analyzed_commit`, compare it with the new submodule HEAD. If different, print:

> ⚠️ <agent>: submodule 从 <old-short> 更新到 <new-short>，分析文档和 demo 可能过时。运行 `/check-updates <agent>` 查看详情。

### 2. Refresh Star Counts

```bash
./scripts/update-stars.sh
```

### 3. Regenerate README Table

```bash
./scripts/gen-readme.sh
```

### 4. Show Status

```bash
./scripts/manage-submodules.sh status
```

## Notes

- If a submodule hasn't been added yet, use `./scripts/manage-submodules.sh add <agent-name>` first
- Star count update requires network access to GitHub API
- All data is sourced from `agents.yaml`
