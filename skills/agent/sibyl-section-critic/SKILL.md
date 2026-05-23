---
name: sibyl-section-critic
description: Sibyl 章节评审 agent - 评审论文特定章节
context: fork
agent: sibyl-light
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('section_critic', workspace_path=ws))"`

AGENT_NAME: sibyl-section-critic
AGENT_TIER: sibyl-light
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
Section: $ARGUMENTS[1]
Section ID: $ARGUMENTS[2]
Read: $ARGUMENTS[0]/writing/sections/$ARGUMENTS[2].md
Write critique to: $ARGUMENTS[0]/writing/critique/$ARGUMENTS[2]_critique.md
