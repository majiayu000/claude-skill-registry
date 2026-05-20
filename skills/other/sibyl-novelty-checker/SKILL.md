---
name: sibyl-novelty-checker
description: Sibyl 新颖性检查 agent - 搜索文献验证 idea 是否与已有论文撞车
context: fork
agent: sibyl-standard
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, WebSearch, WebFetch, mcp__arxiv-mcp-server__search_papers, mcp__arxiv-mcp-server__download_paper, mcp__arxiv-mcp-server__read_paper, mcp__google-scholar__search_google_scholar_key_words, mcp__google-scholar__search_google_scholar_advanced, mcp__claude_ai_bioRxiv__search_preprints, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('novelty_checker', workspace_path=ws))"`

AGENT_NAME: sibyl-novelty-checker
AGENT_TIER: sibyl-standard
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
