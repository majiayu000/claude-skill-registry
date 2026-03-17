---
id: competitive-intel
name: Competitive Intelligence
description: Market research, competitor tracking
role: marketing
requiredTools:
  - type: builtin
    tool: search_web
---

## Competitive Intelligence

When researching competitors or market context:

- Use web search to find current information on competitors, pricing, or positioning.
- Cite sources (URLs, articles) for claims about the market or specific companies.
- Summarize comparisons clearly (e.g. features, pricing, positioning).
- If information is outdated or uncertain, note that and suggest how to verify.
- Focus on publicly available information; do not speculate on confidential data.
- If **fetch_web** is available, use it to read full pages when snippets are insufficient for a claim.

## Step-by-step instructions

1. Clarify the user’s goal (e.g. competitor feature comparison, pricing, positioning).
2. Use the **search_web** tool with focused queries (company name + topic, e.g. “Acme Corp pricing 2024”).
3. Run additional searches if you need multiple competitors or angles.
4. Synthesize results into a structured comparison or summary.
5. Cite each claim with the source URL or publication.
6. If key data is missing or contradictory, state that and suggest how to verify.

## Examples of inputs and outputs

- **Input**: “How does our pricing compare to Competitor X?”  
  **Output**: Short comparison table or bullets (product, price, positioning), each point with a source URL from search_web results.

- **Input**: “What are the main features of Product Y?”  
  **Output**: Numbered or bullet list of features with links; note if info is from marketing vs. third-party review.

## Common edge cases

- **No recent results**: Say that recent public info is scarce and suggest checking the competitor’s site or a specific source.
- **Conflicting sources**: Present the main views and label them (e.g. “Source A says X; Source B says Y”).
- **Vague request**: Ask one clarifying question (e.g. “Which competitors or which product line?”) then run search.
- **Paywalled or restricted content**: Rely only on what the tool returned; do not invent content behind paywalls.

## Tool usage for specific purposes

- **search_web**: Use for all competitor/market lookups. Use specific queries (company + topic) rather than a single broad query. Call multiple times when comparing several competitors or dimensions.
