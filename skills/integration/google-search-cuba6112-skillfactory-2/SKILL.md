---
name: google-search
description: Integration patterns for web search grounding, including query operator usage, API-based search orchestration, and citation metadata mapping. Triggers: google-search, grounding, search-api, citations, search-operators, web-search.
---

# Google Search Grounding

## Overview
Google Search grounding allows LLM applications to access real-time information and provide verifiable citations. This skill covers both direct tool integration (like Gemini's `google_search`) and custom API implementations.

## When to Use
- **Fact-Checking**: When the LLM needs to confirm recent events (e.g., Euro 2024 results).
- **Source Attribution**: When user trust requires seeing direct links to the information source.
- **Niche Research**: Using operators like `site:` to restrict information to specific domains.

## Decision Tree
1. Does the model support built-in grounding (e.g., Gemini)? 
   - YES: Enable `google_search` tool.
   - NO: Use Custom Search API.
2. Do you need to restrict search to specific sites? 
   - YES: Use `site:example.com` operator (no spaces).
3. Do you need to exclude terms? 
   - YES: Use `-term` operator.

## Workflows

### 1. Implementing Search Grounding (Tool-based)
1. Enable the `google_search` tool in the model configuration.
2. Send a user prompt to the API and receive the response containing `groundingMetadata`.
3. Extract `webSearchQueries` for debugging and `groundingChunks` for source links.
4. Render the response with citations by mapping `groundingSupports` indices to the source URLs.

### 2. Precise Source Targeting
1. Use the `site:` operator to restrict searches to trusted domains (e.g., `site:nytimes.com`).
2. Combine multiple operators (e.g., `site:github.com "error 404"`) for specific technical queries.
3. Exclude irrelevant results using the `-` operator (e.g., `jaguar speed -car`).

### 3. Custom Search API Integration
1. Create a Programmable Search Engine ID in the Google control panel.
2. Generate an API key for Custom Search.
3. Perform GET requests to the API with the `q` parameter and parse the resulting JSON search results.

## Non-Obvious Insights
- **Strict Operators**: Search operators like `site:` must NOT have spaces between the colon and the value (e.g., `site:nytimes.com` works, `site: nytimes.com` fails).
- **Citations Metadata**: Grounding metadata uses `groundingSupports` to map specific text segments to source indices, allowing for precise, multi-source citations in a single sentence.
- **Synthesis Loop**: The Gemini tool doesn't just return links; it analyzes the prompt, generates multiple refined queries, and synthesizes a grounded answer.

## Evidence
- "The model analyzes the prompt and determines if a Google Search can improve the answer." - [Google AI](https://ai.google.dev/gemini-api/docs/grounding)
- "Do not put spaces between the operator and your search term." - [Google Search Help](https://support.google.com/websearch/answer/2466433)
- "Spain won Euro 2024...[1](https://...)" - [Google AI Grounding Example](https://ai.google.dev/gemini-api/docs/grounding)

## Scripts
- `scripts/google-search_tool.py`: Implementation of Custom Search API requests.
- `scripts/google-search_tool.js`: Example of parsing grounding metadata for citations.

## Dependencies
- `google-api-python-client` (for Custom Search API)
- `google-generativeai` (for Gemini Tool-use)

## References
- [references/README.md](references/README.md)