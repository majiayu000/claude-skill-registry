---
name: sibyl-section-writer
description: Sibyl 章节撰写 agent - 撰写论文特定章节
context: fork
agent: sibyl-standard
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('section_writer', workspace_path=ws))"`

AGENT_NAME: sibyl-section-writer
AGENT_TIER: sibyl-standard
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
Section: $ARGUMENTS[1]
Section ID: $ARGUMENTS[2]
Write to: $ARGUMENTS[0]/writing/sections/$ARGUMENTS[2].md
