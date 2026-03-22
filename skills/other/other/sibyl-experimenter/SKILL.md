---
name: sibyl-experimenter
description: Sibyl 实验执行 agent - 编写代码并在远程 GPU 上执行实验
context: fork
agent: sibyl-standard
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, WebSearch, WebFetch, mcp__ssh-mcp-server__execute-command, mcp__ssh-mcp-server__upload, mcp__ssh-mcp-server__download, mcp__ssh-mcp-server__list-servers, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('experimenter', workspace_path=ws))"`

AGENT_NAME: sibyl-experimenter
AGENT_TIER: sibyl-standard
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
MODE: $ARGUMENTS[1]
SSH server: $ARGUMENTS[2]
Remote base: $ARGUMENTS[3]
Remote env command: $ARGUMENTS[4]
GPU IDs: $ARGUMENTS[5]
Optional --tasks: $ARGUMENTS[6] (if present, format: --tasks=task_1a,task_1b)
