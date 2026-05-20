---
id: exa-semantic-research
name: Exa Semantic Research
description: Conceptual and semantic web search; cite sources
role: product
requiredTools:
  - type: builtin
    tool: exa_search
---

## Exa Semantic Research

When using Exa for semantic or conceptual search:

- Use **exa_search** (or the actual Exa tool name as provided) for conceptual and semantic queries rather than simple keyword match.
- Cite sources (URLs, titles) for each claim or finding; Exa returns relevant links and snippets.
- Combine with **search_web** when both are available for broader coverage (keyword + semantic).
- Prefer clear, concept-based queries (e.g. "approaches to X", "comparisons of Y and Z") to get the best semantic results.
- If results are thin or off-topic, rephrase the query to be more specific or try a different angle.

## Step-by-step instructions

1. Turn the user's question into a conceptual or semantic query (what concept or relationship they care about).
2. Call **exa_search** with that query; use any filters or options the tool supports (e.g. date, type) when relevant.
3. Read the returned results (snippets, URLs, titles) and select the most relevant for the answer.
4. Summarize findings and cite each point with the source URL or title.
5. If the user asked for a comparison or list, structure the answer (bullets or numbered) and cite per item.
6. When both **exa_search** and **search_web** are available, use Exa for conceptual depth and search_web for recency or keyword-focused backup.

## Examples of inputs and outputs

- **Input**: "What are the main approaches to implementing feature flags?"  
  **Output**: Short list of approaches with a source URL or title per approach from **exa_search** results; conceptual query works well with Exa.

- **Input**: "Find comparisons of tool A vs tool B."  
  **Output**: Structured comparison (e.g. pros/cons, use cases) with citations from **exa_search**; note if info is from marketing vs third-party.

## Common edge cases

- **No good results**: Say that semantic search didn't return strong matches and suggest a more specific or rephrased query, or try **search_web** if available.
- **Conflicting info**: Present the main views and cite each source; do not pick one without noting others.
- **User asks for "everything about X"**: Give a structured summary (overview, key points, sources) and offer to go deeper on one aspect.
- **Exa vs search_web**: Use Exa for conceptual/semantic questions; use search_web for very recent or keyword-heavy queries when both are enabled.

## Tool usage for specific purposes

- **exa_search**: Use for conceptual and semantic queries (e.g. "approaches to X", "how Y relates to Z"); cite returned URLs/titles; combine with search_web when both available for comprehensive research.
