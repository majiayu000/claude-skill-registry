---
name: sibyl-idea-validation-decision
description: Sibyl pilot 验证决策 agent - 根据小实验结果决定 ADVANCE / REFINE / PIVOT
context: fork
agent: sibyl-heavy
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('idea_validation_decision', workspace_path=ws))"`

AGENT_NAME: sibyl-idea-validation-decision
AGENT_TIER: sibyl-heavy
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
