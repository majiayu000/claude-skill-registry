---
name: sibyl-methodologist
description: Sibyl 方法论者 agent - 审查实验方法的内外部效度和可复现性
context: fork
agent: sibyl-light
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('methodologist', workspace_path=ws))"`

AGENT_NAME: sibyl-methodologist
AGENT_TIER: sibyl-light
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]

Write your output to $ARGUMENTS[0]/idea/result_debate/methodologist.md
