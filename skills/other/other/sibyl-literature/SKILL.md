---
name: sibyl-literature
description: Sibyl 文献调研 agent - 使用 arXiv + Web 双源搜索进行系统性文献调研
context: fork
agent: sibyl-standard
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, Bash, WebSearch, WebFetch, mcp__arxiv-mcp-server__search_papers, mcp__arxiv-mcp-server__download_paper, mcp__arxiv-mcp-server__read_paper, mcp__arxiv-mcp-server__list_papers, mcp__google-scholar__search_google_scholar_key_words, mcp__google-scholar__search_google_scholar_advanced, mcp__google-scholar__get_author_info, mcp__claude_ai_bioRxiv__search_preprints, mcp__claude_ai_bioRxiv__get_preprint, Skill
---

!`SIBYL_WORKSPACE="$ARGUMENTS[0]" .venv/bin/python3 -c "from sibyl.orchestrate import render_skill_prompt; import os; ws = os.environ.get('SIBYL_WORKSPACE', ''); print(render_skill_prompt('literature_researcher', workspace_path=ws))"`

AGENT_NAME: sibyl-literature
AGENT_TIER: sibyl-standard
SIBYL_ROOT: /Users/cwan0785/sibyl-system

Workspace path: $ARGUMENTS[0]
研究主题 (may contain spaces): $ARGUMENTS[1]

请同时使用 mcp__arxiv-mcp-server__search_papers 和 WebSearch 进行调研，将结果写入 $ARGUMENTS[0]/context/literature.md
