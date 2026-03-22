---
name: sibyl-theoretical
description: Sibyl 理论研究者 agent - 注重数学基础和理论保证的研究提案
context: fork
agent: sibyl-standard
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, WebSearch, WebFetch, mcp__arxiv-mcp-server__search_papers, mcp__arxiv-mcp-server__download_paper, mcp__arxiv-mcp-server__read_paper, mcp__google-scholar__search_google_scholar_key_words, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('theoretical', workspace_path=ws))"`

AGENT_NAME: sibyl-theoretical
AGENT_TIER: sibyl-standard
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
Topic (may contain spaces): $ARGUMENTS[1]

Write your output to $ARGUMENTS[0]/idea/perspectives/theoretical.md
