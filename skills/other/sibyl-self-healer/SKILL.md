---
name: sibyl-self-healer
description: Sibyl 自愈 agent - 后台自动检测修复系统错误，添加回归测试，git commit 留痕
context: fork
agent: sibyl-standard
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, Agent
---

!`.venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; print(render_skill_prompt('self_healer'))"`

## Repair Task

```json
$ARGUMENTS
```

## Workspace

Working directory: the repository root (`/Users/cwan0785/sibyl-system`).

All fixes happen on the `dev` branch. After fixing:
1. Run `.venv/bin/python3 -m pytest tests/ -x -q` to verify
2. `git add <files>` (specific files only)
3. `git commit -m "fix(self-heal): <description> [auto]"`
4. Report result via `cli_self_heal_record`
