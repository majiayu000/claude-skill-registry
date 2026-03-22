---
name: sibyl-outline-writer
description: Sibyl 大纲撰写 agent - 生成论文详细大纲
context: fork
agent: sibyl-standard
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('outline_writer', workspace_path=ws))"`

AGENT_NAME: sibyl-outline-writer
AGENT_TIER: sibyl-standard
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
