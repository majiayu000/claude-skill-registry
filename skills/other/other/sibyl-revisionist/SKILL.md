---
name: sibyl-revisionist
description: Sibyl 修正主义者 agent - 基于实验结果反思假设，提出修正方向
context: fork
agent: sibyl-light
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('revisionist', workspace_path=ws))"`

AGENT_NAME: sibyl-revisionist
AGENT_TIER: sibyl-light
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]

Write your output to $ARGUMENTS[0]/idea/result_debate/revisionist.md
