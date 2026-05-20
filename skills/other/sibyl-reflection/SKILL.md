---
name: sibyl-reflection
description: Sibyl 反思 agent - 分析迭代产出，分类问题，生成改进计划
context: fork
agent: sibyl-heavy
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('reflection', workspace_path=ws))"`

AGENT_NAME: sibyl-reflection
AGENT_TIER: sibyl-heavy
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
Current iteration: $ARGUMENTS[1]
