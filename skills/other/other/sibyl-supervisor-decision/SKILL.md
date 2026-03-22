---
name: sibyl-supervisor-decision
description: Sibyl 监督决策 agent - 分析实验结果决定 PIVOT 还是 PROCEED
context: fork
agent: sibyl-heavy
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('supervisor_decision', workspace_path=ws))"`

AGENT_NAME: sibyl-supervisor-decision
AGENT_TIER: sibyl-heavy
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]

SPECIAL TASK: Analyze experiment results and the debate opinions.
Read:
- $ARGUMENTS[0]/exp/results/summary.md
- $ARGUMENTS[0]/idea/result_debate/optimist.md
- $ARGUMENTS[0]/idea/result_debate/skeptic.md
- $ARGUMENTS[0]/idea/result_debate/strategist.md
- $ARGUMENTS[0]/idea/proposal.md

Determine: PIVOT or PROCEED?
Write to $ARGUMENTS[0]/supervisor/experiment_analysis.md
End with exactly: DECISION: PIVOT or DECISION: PROCEED
