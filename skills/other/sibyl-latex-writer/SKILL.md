---
name: sibyl-latex-writer
description: Sibyl LaTeX 排版 agent - 将论文转为 NeurIPS LaTeX 格式并编译
context: fork
agent: sibyl-standard
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, mcp__ssh-mcp-server__execute-command, mcp__ssh-mcp-server__upload, mcp__ssh-mcp-server__download, mcp__ssh-mcp-server__list-servers, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('latex_writer', workspace_path=ws))"`

AGENT_NAME: sibyl-latex-writer
AGENT_TIER: sibyl-standard
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
SSH server: $ARGUMENTS[1]
Remote base: $ARGUMENTS[2]
