---
name: sibyl-experiment-supervisor
description: Sibyl 后台实验监督 agent - 持续刷新 GPU 空闲状态、动态派发排队实验、处理运行时间/状态漂移
context: fork
agent: sibyl-standard
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, Skill, Agent, mcp__ssh-mcp-server__execute-command, mcp__ssh-mcp-server__upload, mcp__ssh-mcp-server__download, mcp__ssh-mcp-server__list-servers
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('experiment_supervisor', workspace_path=ws))"`

AGENT_NAME: sibyl-experiment-supervisor
AGENT_TIER: sibyl-standard
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
MODE: $ARGUMENTS[1]
SSH server: $ARGUMENTS[2]
Remote base: $ARGUMENTS[3]
Remote env command: $ARGUMENTS[4]
Task IDs CSV: $ARGUMENTS[5]
Supervisor poll interval sec: $ARGUMENTS[6]
GPU poll interval sec: $ARGUMENTS[7]
GPU free threshold MB: $ARGUMENTS[8]
Max GPUs: $ARGUMENTS[9]
Aggressive mode: $ARGUMENTS[10]
Aggressive threshold pct: $ARGUMENTS[11]
