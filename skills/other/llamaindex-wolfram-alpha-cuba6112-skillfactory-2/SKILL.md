---
name: llamaindex-wolfram-alpha
description: LlamaIndex Wolfram Alpha tool for computational knowledge queries, math solving, scientific calculations, and agent integration. Triggers: wolfram alpha, computational query, math solver, scientific calculation, WolframAlphaToolSpec.
---

## Overview

The LlamaIndex Wolfram Alpha tool enables agents to interface with the Wolfram|Alpha LLM API for computational knowledge queries. It provides concise text-based answers optimized for LLM consumption, handling complex mathematics, scientific facts, unit conversions, and visual data like molecular structures.

## When to Use

- When an agent needs to solve complex mathematical equations or calculus problems.
- When scientific facts require high-precision data (physical constants, planetary mass, chemical properties).
- When performing unit conversions or physics problems with real units.
- When the user requires visual diagrams (periodic table, molecular structures, plots).

## Decision Tree

1. Is the query mathematical or scientific?
   - YES: Use Wolfram Alpha tool.
   - NO: Use standard search or knowledge base.
2. Does the query involve scientific notation?
   - YES: Format as `6*10^14` (NEVER use `6e14`).
3. Does the response contain an 'Assumptions' block?
   - YES: Parse assumption identifier and re-query with `assumption` parameter.
4. Is the response a 501 error?
   - YES: Query is uninterpretable; simplify to keywords.

## Workflows

### 1. Basic Agent Integration

1. Register for a Wolfram AppID at the Developer Portal.
2. Install the package: `pip install llama-index-tools-wolfram-alpha`.
3. Initialize the tool spec with your AppID.
4. Convert to tool list and provide to agent.

```python
from llama_index.tools.wolfram_alpha import WolframAlphaToolSpec
from llama_index.agent.openai import OpenAIAgent

wolfram_spec = WolframAlphaToolSpec(app_id="YOUR_APP_ID")
tools = wolfram_spec.to_tool_list()

agent = OpenAIAgent.from_tools(tools, verbose=True)
response = agent.chat("What is the mass of the sun in kilograms?")
```

### 2. Query Optimization

1. Convert natural language to simplified keywords (e.g., "France population" not "how many people live in France").
2. Always send queries in English; translate beforehand if needed.
3. Use proper exponent notation: `6*10^14` never `6e14`.
4. For equations with units, solve the unitless version first.

### 3. Handling Assumptions

1. Check response for "Assumptions" block.
2. Extract the assumption identifier (e.g., `*C.pi-_*Movie-`).
3. Re-query with `assumption` parameter to disambiguate.
4. Present final answer without explaining the disambiguation.

## Non-Obvious Insights

- **Keyword Queries**: The LLM API works best with simplified keyword queries rather than full natural language sentences. Convert "how far is it from New York to Los Angeles" to "distance New York Los Angeles".
- **Exponent Notation**: Using `6e14` format will fail; always use `6*10^14` for scientific notation.
- **501 Errors**: A 501 status means the query is uninterpretable or touches restricted topics; simplify or rephrase the query.
- **Image Rendering**: Display returned image URLs with Markdown syntax `![alt](URL)` for visual data like plots and structures.
- **Assumptions Handling**: When multiple interpretations exist, Wolfram returns assumption identifiers that should be used in follow-up queries rather than rephrasing.

## Evidence

- "The wolfram_alpha_query method is used to make a query to wolfram alpha about a mathematical or scientific problem." - [LlamaIndex Docs](https://docs.llamaindex.ai/en/stable/api_reference/tools/wolfram_alpha/)
- "Convert inputs to simplified keyword queries whenever possible (e.g. convert 'how many people live in France' to 'France population')." - [Wolfram LLM API](https://products.wolframalpha.com/llm-api/documentation)
- "ALWAYS use this exponent notation: 6*10^14, NEVER 6e14." - [Wolfram LLM API](https://products.wolframalpha.com/llm-api/documentation)

## Scripts

- `scripts/llamaindex-wolfram-alpha_tool.py`: Python helper for Wolfram Alpha queries with assumption handling.
- `scripts/llamaindex-wolfram-alpha_tool.js`: Node.js wrapper for HTTP API calls.

## Dependencies

- `llama-index-tools-wolfram-alpha`
- `llama-index-core`
- Wolfram Alpha AppID (free tier: 2,000 calls/month)

## References

- [references/README.md](references/README.md)
