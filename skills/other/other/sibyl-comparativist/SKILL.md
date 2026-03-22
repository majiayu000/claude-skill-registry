---
name: sibyl-comparativist
description: Sibyl 比较分析者 agent - 对标 SOTA 和同类工作，定位结果贡献
context: fork
agent: sibyl-light
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, mcp__arxiv-mcp-server__search_papers, mcp__google-scholar__search_google_scholar_key_words, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('comparativist', workspace_path=ws))"`

AGENT_NAME: sibyl-comparativist
AGENT_TIER: sibyl-light
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]

Write your output to $ARGUMENTS[0]/idea/result_debate/comparativist.md
