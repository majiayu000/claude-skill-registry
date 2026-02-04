---
name: exa-search
description: Use Exa for semantic/neural web search. Exa understands context and returns high-quality results. Use this skill when you need to search the web for documentation, research, or any information that requires understanding meaning rather than just keyword matching. NEVER substitute web_search for Exa - they serve completely different purposes.
version: 1.0.0
---


# Exa Semantic Search

Exa provides neural/semantic search via MCP. Use it for high-quality web search that understands context.

## When to Use Exa

- Searching for documentation or technical information
- Research requiring semantic understanding
- Finding information where exact keywords are unknown
- Company research and LinkedIn searches
- Deep research tasks

## When NOT to Use Exa

- Never use `web_search` as a substitute - it's basic keyword matching only
- If Exa fails, troubleshoot Exa - don't fall back to `web_search`

## Available Tools

The Exa MCP server provides these tools:

- `web_search_exa` - Semantic web search
- `crawling_exa` - Crawl and extract web content
- `company_research_exa` - Research companies
- `linkedin_search_exa` - Search LinkedIn profiles
- `deep_researcher_start` - Start deep research task
- `deep_researcher_check` - Check deep research status

## Configuration

Exa is configured as a remote HTTP MCP in `~/.mcp.json`:

```json
{
  "exa": {
    "type": "http",
    "url": "https://mcp.exa.ai/mcp?tools=web_search_exa,crawling_exa,company_research_exa,linkedin_search_exa,deep_researcher_start,deep_researcher_check"
  }
}
```

## Usage Examples

### Basic Search
Use the Exa MCP tools directly when semantic search is needed.

### Deep Research
1. Start with `deep_researcher_start` for complex topics
2. Poll with `deep_researcher_check` until complete
3. Get comprehensive, synthesized results

## Critical Rules

1. **NEVER replace Exa with web_search** - they are fundamentally different
2. **NEVER use web_search in Task sub-agents** as a substitute for Exa
3. If Exa fails, troubleshoot Exa - do not substitute



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `algorithms`: 19 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
exa-search (−) + SDF.Ch10 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch4: Pattern Matching

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.