---
name: airweave-setup
description: Set up and integrate Airweave into applications. Use when the user wants to install Airweave, create collections, connect data sources, configure MCP servers, or set up the SDK to integrate Airweave into their app. For developers building with Airweave.
---

# Airweave Setup & Integration

Airweave is an open-source platform that makes any app searchable for AI agents. It connects to apps, productivity tools, databases, or document stores and transforms their contents into searchable knowledge bases.

## Quick Start

### Option 1: Airweave Cloud (Recommended)

1. Sign up at https://app.airweave.ai
2. Get your API key from the dashboard
3. Install the SDK:

```bash
pip install airweave-sdk   # Python
npm install @airweave/sdk  # TypeScript
```

### Option 2: Self-Hosted

```bash
git clone https://github.com/airweave-ai/airweave.git
cd airweave
chmod +x start.sh
./start.sh
```

Access the dashboard at http://localhost:8080

## Core Workflow

The typical Airweave workflow follows these steps:

### 1. Create a Collection

A collection groups multiple data sources into a single searchable endpoint.

**Python:**
```python
from airweave import AirweaveSDK

client = AirweaveSDK(
    api_key="YOUR_API_KEY",
    base_url="https://api.airweave.ai"  # or http://localhost:8001 for self-hosted
)

collection = client.collections.create(name="My Knowledge Base")
print(f"Collection ID: {collection.readable_id}")
```

**TypeScript:**
```typescript
import { AirweaveSDKClient } from "@airweave/sdk";

const client = new AirweaveSDKClient({ apiKey: "YOUR_API_KEY" });
const collection = await client.collections.create({ name: "My Knowledge Base" });
```

### 2. Add Source Connections

Connect data sources to your collection. 40+ sources supported including:
- **Productivity**: Notion, Google Drive/Docs/Slides, Dropbox, OneDrive, SharePoint, Box, Airtable
- **Communication**: Slack, Gmail, Outlook, Teams, Google Calendar
- **Project Management**: Jira, Linear, Asana, Trello, Monday, ClickUp, Todoist
- **Development**: GitHub, GitLab, Bitbucket, Confluence
- **CRM & Sales**: Salesforce, HubSpot, Attio, Zendesk, Pipedrive, Shopify
- **Data**: Stripe, PostgreSQL

See [SDK-REFERENCE.md](SDK-REFERENCE.md) for the complete list of source short names.

**Python (API Key sources like Stripe, Linear):**
```python
source = client.source_connections.create(
    name="My Stripe Connection",
    short_name="stripe",
    readable_collection_id=collection.readable_id,
    authentication={
        "credentials": {"api_key": "sk_live_your_stripe_key"}
    }
)
```

**OAuth sources (Slack, Google, Microsoft, etc.):**

Most sources use OAuth for authentication. Use the Airweave UI at https://app.airweave.ai to connect these sources—it handles the OAuth flow automatically.

### 3. Search Your Data

Once synced, search across all connected sources with a single query:

**Python:**
```python
results = client.collections.search(
    readable_id=collection.readable_id,
    query="customer feedback about pricing"
)

for result in results.results:
    print(f"Source: {result['payload']['source_name']}")
    print(f"Content: {result['payload']['md_content'][:200]}...")
    print(f"Score: {result['score']}")
```

## Advanced Search Features

Airweave provides powerful search capabilities:

### Search Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Natural language search query |
| `search_type` | "semantic" \| "hybrid" | Semantic (default) or hybrid search |
| `limit` | number | Max results (default: 100) |
| `offset` | number | Skip results for pagination |
| `recency_bias` | 0-1 | Prioritize recent results (0=none, 1=most recent) |
| `enable_reranking` | boolean | AI reranking for better relevance |
| `enable_query_expansion` | boolean | Expand query with variations |
| `response_type` | "raw" \| "completion" | Raw results or AI-generated answer |
| `top_k` | number | Internal retrieval count before reranking |

### Example: Advanced Search

```python
results = client.collections.search(
    readable_id=collection.readable_id,
    query="technical documentation",
    search_type="hybrid",
    enable_query_expansion=True,
    enable_reranking=True,
    recency_bias=0.5,
    top_k=50,
    limit=20
)
```

### Example: AI-Generated Answer

```python
answer = client.collections.search(
    readable_id=collection.readable_id,
    query="What are our customer refund policies?",
    response_type="completion",
    enable_reranking=True
)
# Returns a synthesized answer instead of raw results
```

## MCP Integration for AI Agents

Airweave exposes search via MCP (Model Context Protocol) for seamless AI agent integration.

### Setup for Claude Desktop / Cursor

Add to your MCP configuration (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "airweave-search": {
      "command": "npx",
      "args": ["airweave-mcp-search"],
      "env": {
        "AIRWEAVE_API_KEY": "your-api-key",
        "AIRWEAVE_COLLECTION": "your-collection-id",
        "AIRWEAVE_BASE_URL": "https://api.airweave.ai"
      }
    }
  }
}
```

### Hosted MCP Server

For cloud-based AI platforms like OpenAI Agent Builder:
- URL: `https://mcp.airweave.ai`
- Uses Streamable HTTP transport (MCP 2025-03-26)

See [MCP-SETUP.md](MCP-SETUP.md) for detailed configuration.

## Common Patterns

### Pattern 1: Search with Source Filtering

```python
from airweave import SearchRequest, Filter, FieldCondition, MatchAny

search_request = SearchRequest(
    query="project updates",
    filter=Filter(
        must=[
            FieldCondition(
                key="source_name",
                match=MatchAny(any=["Slack", "GitHub"])
            )
        ]
    )
)

results = client.collections.search_advanced(
    readable_id=collection.readable_id,
    search_request=search_request
)
```

### Pattern 2: Recent Documents First

```python
results = client.collections.search(
    readable_id=collection.readable_id,
    query="critical bugs",
    recency_bias=0.8,  # Strongly prefer recent
    limit=10
)
```

### Pattern 3: High-Quality Results with Reranking

```python
results = client.collections.search(
    readable_id=collection.readable_id,
    query="API documentation",
    enable_reranking=True,
    top_k=30,
    limit=10
)
```

## Troubleshooting

### No Results Found
- Check that sync has completed (can take a few minutes for large sources)
- Verify the collection ID is correct
- Try a broader search query

### Authentication Errors
- Verify your API key is valid
- Check that the API key has access to the collection
- For OAuth sources, the token may have expired—reconnect in the UI

### Rate Limits
- The API has rate limits for protection
- Implement exponential backoff for retries
- Contact support for higher limits

## Additional Resources

- **Documentation**: https://docs.airweave.ai
- **API Reference**: https://api.airweave.ai/docs (Swagger)
- **GitHub**: https://github.com/airweave-ai/airweave
- **Discord**: https://discord.gg/484HY9Ehxt

For detailed SDK reference, see [SDK-REFERENCE.md](SDK-REFERENCE.md).
For advanced search patterns, see [SEARCH-PATTERNS.md](SEARCH-PATTERNS.md).

