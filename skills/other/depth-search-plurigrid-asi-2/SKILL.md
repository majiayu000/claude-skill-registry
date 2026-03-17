---
name: depth-search
description: Deep multi-source research combining academic MCPs (arxiv, semantic-scholar, paper-search, deepwiki), Exa semantic search, and local ~/.topos knowledge base. Use for comprehensive research requiring multiple sources. NEVER fall back to web_search - ask user for help instead.
---

# Depth Search

Comprehensive multi-source research skill. Searches across academic databases, semantic web search, and local knowledge before asking the user for help.

## Search Order

Execute searches in this order, using parallel subagents where possible:

### 1. Local Knowledge Base (~/.topos)
Search `~/.topos` directory first for existing research, notes, and cached data:
- Use `glob` and `Grep` to find relevant files
- Check `.md`, `.org`, `.jl`, `.py`, `.json` files
- Look in subdirectories: `skills/`, `archived/`, `Gay.jl/`, etc.

### 2. Academic MCPs (parallel)
Launch parallel subagents to search all 4 academic sources:

| MCP | Tools | Best For |
|-----|-------|----------|
| **arxiv** | `search_papers`, `get_paper`, `download_paper` | Preprints, CS/physics/math papers |
| **semantic-scholar** | `paper_relevance_search`, `paper_details`, `paper_citations` | Citation analysis, author profiles |
| **paper-search** | `search_arxiv`, `search_pubmed`, `search_biorxiv`, etc. | Multi-source aggregation |
| **deepwiki** | `read_wiki_structure`, `read_wiki_contents`, `ask_question` | GitHub repo documentation |

### 3. Exa Semantic Search
Use Exa MCP for high-quality web search:
- `web_search_exa` - Semantic web search
- `crawling_exa` - Extract web content
- `company_research_exa` - Company research
- `deep_researcher_start` / `deep_researcher_check` - Deep research tasks

### 4. Ask User for Help
If all sources fail to find what's needed:
- **DO NOT fall back to `web_search`** - it's basic keyword matching only
- Instead, ask the user:
  - "I couldn't find [X] in academic databases, Exa, or local files. Can you provide a link, paper title, or more context?"
  - Suggest specific sources they might check manually
  - Offer to try different search terms

## Critical Rules

1. **NEVER use `web_search` as a fallback** - it's not equivalent to Exa
2. **NEVER use `web_search` in Task subagents** - use Exa tools instead
3. **Always search local ~/.topos first** - may have cached/annotated versions
4. **Use parallel subagents** for academic MCPs to maximize speed
5. **Ask user for help** rather than guessing or using inferior search

## Example Workflow

```
User: "Find papers on world models for LLMs"

1. Search ~/.topos for existing notes/papers
2. Launch 4 parallel Task subagents:
   - arxiv: search_papers("world models LLM")
   - semantic-scholar: paper_relevance_search("world models language models")
   - paper-search: search across all sources
   - deepwiki: check relevant GitHub repos
3. If needed, use Exa: web_search_exa("world models LLM research")
4. Synthesize results from all sources
5. If still not found: ask user for clarification
```

## Parallel Subagent Template

When searching academic sources, use this pattern:

```
Launch 4 parallel Task subagents:
- Task 1: Use arxiv MCP to search for [query]
- Task 2: Use semantic-scholar MCP to search for [query]  
- Task 3: Use paper-search MCP to search for [query]
- Task 4: Use deepwiki MCP to find related repos/docs
```

## What NOT To Do

❌ `web_search` as fallback when Exa fails  
❌ Single-source search when multiple are available  
❌ Skipping local ~/.topos search  
❌ Guessing answers without exhausting sources  
❌ Sequential searches when parallel is possible  

## What TO Do

✅ Search ~/.topos first for cached knowledge  
✅ Parallel subagents for academic MCPs  
✅ Exa for semantic web search  
✅ Ask user when sources are exhausted  
✅ Synthesize results from multiple sources  
