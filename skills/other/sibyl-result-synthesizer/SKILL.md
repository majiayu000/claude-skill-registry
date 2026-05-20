---
name: sibyl-result-synthesizer
description: Sibyl 结果辩论综合者 agent - 综合6方结果分析形成统一判断和行动计划
context: fork
agent: sibyl-heavy
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('result_synthesizer', workspace_path=ws))"`

AGENT_NAME: sibyl-result-synthesizer
AGENT_TIER: sibyl-heavy
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]

Read all analyses from $ARGUMENTS[0]/idea/result_debate/ and synthesize into unified assessment.
Write outputs to:
- $ARGUMENTS[0]/idea/result_debate/synthesis.md
- $ARGUMENTS[0]/idea/result_debate/verdict.md
