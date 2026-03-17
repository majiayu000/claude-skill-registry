---
name: airweave-search
description: Search and retrieve context from Airweave collections. Use when users ask about their data in connected apps (Slack, GitHub, Notion, Jira, Confluence, Google Drive, Salesforce, databases, etc.), need to find documents or information from their workspace, want answers based on their company data, or need you to check app data for context to complete a task.
---

# Airweave Search

Use this skill to effectively search and retrieve context from Airweave collections, whether answering questions or gathering context to complete tasks.

## When to Search

**Search when the user:**
- Asks about data in their connected apps ("What did we discuss in Slack about...")
- Needs to find documents, messages, issues, or records
- Asks factual questions about their workspace ("Who is responsible for...", "What's our policy on...")
- References specific tools by name ("in Notion", "on GitHub", "in Jira")
- Needs recent information you don't have in your training
- Needs you to check app data for context to complete a task ("check our Notion docs", "look at the Jira ticket", "see what we decided in Slack")

**Don't search when:**
- User asks general knowledge questions (use your training)
- User is asking how to SET UP Airweave (use `airweave-setup` skill instead)
- User already provided all needed context in the conversation
- The question is about Airweave itself, not data within it

## Query Formulation

### Extract Key Concepts

Turn user intent into effective search queries:

| User Says | Search Query |
|-----------|--------------|
| "What did Sarah say about the launch?" | "Sarah product launch" |
| "Find the API documentation" | "API documentation" |
| "Any bugs reported this week?" | "bug report issues" |
| "What's our refund policy?" | "refund policy customer" |

### Query Tips

1. **Use natural language** - Airweave uses semantic search, not keyword matching
2. **Include context** - "pricing feedback" is better than just "pricing"
3. **Be specific but not too narrow** - Start moderately specific, broaden if no results
4. **Avoid filler words** - Skip "please find", "can you search for"

## Parameter Selection

Choose parameters based on user intent:

| User Intent | Parameters |
|-------------|------------|
| Recent updates/conversations | `recency_bias: 0.7-0.9` |
| Finding a specific document | `search_method: "keyword"` or `"hybrid"` |
| General topic exploration | `search_method: "hybrid"`, higher `limit` |
| High-quality results only | `enable_reranking: true` |
| Quick direct answer | `response_type: "completion"` |
| Browse/see all matches | `response_type: "raw"`, `limit: 20-50` |

### Parameter Quick Reference

| Parameter | Values | When to Use |
|-----------|--------|-------------|
| `recency_bias` | 0-1 | Higher = favor recent. Use 0.7+ for "recent", "latest", "this week" |
| `search_method` | hybrid/neural/keyword | `keyword` for exact terms, `neural` for concepts, `hybrid` for both |
| `response_type` | raw/completion | `completion` for direct answers, `raw` to show sources |
| `limit` | 1-1000 | Lower (5-10) for quick answers, higher (20-50) for exploration |
| `enable_reranking` | boolean | `true` for better relevance (slightly slower) |
| `expansion_strategy` | auto/llm/no_expansion | `auto` for most cases, `no_expansion` for exact queries |

See [PARAMETERS.md](PARAMETERS.md) for detailed guidance.

## Handling Results

### Interpreting Scores

| Score | Meaning | Action |
|-------|---------|--------|
| 0.85+ | Highly relevant | Use confidently |
| 0.70-0.85 | Likely relevant | Use with context |
| 0.50-0.70 | Possibly relevant | Mention uncertainty |
| Below 0.50 | Weak match | Consider rephrasing query |

### Synthesizing Answers

When presenting results to users:

1. **Lead with the answer** - Don't start with "I found 5 results"
2. **Cite sources** - Mention where info came from ("According to your Slack conversation...")
3. **Synthesize, don't dump** - Combine relevant parts into coherent response
4. **Acknowledge gaps** - If results don't fully answer, say so

### Handling No/Poor Results

If search returns no results or low-quality matches:

1. **Broaden the query** - Remove specific terms, use more general concepts
2. **Try different phrasing** - Rephrase using synonyms or related terms
3. **Increase limit** - Fetch more results to find relevant matches
4. **Check source availability** - The data source might not be connected
5. **Ask for clarification** - User might have more context to share

## Finding the Search Tool

Airweave MCP tools follow the naming pattern `search-{collection-name}`. Look for tools matching this pattern in your available MCP tools.

**Examples:**
- `search-acmes-slack-k8v2x1`
- `search-acmes-notion-p3m9q7`
- `search-acmes-jira-w5n4r2`

**If no Airweave search tool is available:**
- The user may not have Airweave MCP configured
- Ask if they have Airweave set up and connected to their AI assistant
- Suggest using the `airweave-setup` skill for configuration help

**Multiple collections:**
If multiple `search-*` tools are available, choose based on the collection name and the user's request. If unclear which to use, ask the user or try the most general-sounding one first.

## Calling the Search Tool

Use the `search-{collection}` MCP tool with your chosen parameters:

```
search-acmes-slack-k8v2x1({
  query: "customer feedback pricing",
  recency_bias: 0.7,
  limit: 10
})
```

```
search-acmes-notion-p3m9q7({
  query: "API authentication docs",
  search_method: "hybrid",
  enable_reranking: true
})
```

```
search-acmes-jira-w5n4r2({
  query: "What is our refund policy?",
  response_type: "completion"
})
```

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete conversation examples showing effective search patterns.

