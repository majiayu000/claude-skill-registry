---
name: toolfs-rag
description: Semantic search over vector databases for document retrieval. Use this skill when the user requests searching documents, finding relevant content, or performing semantic queries such as "Search for information about X", "Find documents related to Y", or "Query the knowledge base".
metadata:
  author: toolfs
  version: "1.0.0"
  module: rag
---

# ToolFS RAG

Semantic search over vector databases for document retrieval. RAG (Retrieval-Augmented Generation) enables finding relevant documents and content based on semantic similarity rather than exact keyword matches.

## How It Works

1. **Vector Search**: Queries are converted to embeddings and compared against document vectors
2. **Similarity Scoring**: Results are ranked by semantic similarity scores
3. **Top-K Results**: Returns the most relevant documents up to the specified limit
4. **Metadata Filtering**: Results include metadata for context and filtering

## Usage

### Semantic Search

**ToolFS Path:**
```
/toolfs/rag/query?text=<query_text>&top_k=<number>
```

**Parameters:**
- `text` or `q`: The search query (URL-encoded)
- `top_k`: Number of results to return (default: 5)

**Example:**
```json
GET /toolfs/rag/query?text=ToolFS%20skill%20architecture&top_k=3

// Response
{
  "query": "ToolFS skill architecture",
  "top_k": 3,
  "results": [
    {
      "id": "doc-001",
      "content": "ToolFS provides a skill system that supports WASM modules for sandboxed execution. Skills can be mounted to virtual paths and executed through the Skill API.",
      "score": 0.95,
      "metadata": {
        "source": "documentation",
        "section": "skills",
        "title": "Skill System Overview"
      }
    },
    {
      "id": "doc-002",
      "content": "The skill architecture allows mounting custom handlers to virtual paths, enabling extensible functionality within the ToolFS framework.",
      "score": 0.87,
      "metadata": {
        "source": "documentation",
        "section": "architecture",
        "title": "Architecture Design"
      }
    },
    {
      "id": "doc-003",
      "content": "WASM skills are executed in a sandboxed environment with resource limits and security constraints to ensure safe operation.",
      "score": 0.82,
      "metadata": {
        "source": "documentation",
        "section": "sandboxing",
        "title": "Security Model"
      }
    }
  ]
}
```

## When to Use This Skill

Use RAG skill when you need to:

- **Semantic Search**: Find documents based on meaning, not just keywords
- **Knowledge Retrieval**: Query a knowledge base or document collection
- **Context Gathering**: Gather relevant context for generating responses
- **Document Discovery**: Discover related content across a corpus

Common use cases:
- "Search for information about ToolFS skills"
- "Find documents related to vector databases"
- "Query the knowledge base for best practices"
- "Find relevant documentation about RAG systems"

## Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` or `q` | string | Yes | - | Search query text (URL-encoded) |
| `top_k` | integer | No | 5 | Number of results to return |

## Result Structure

Each result includes:

- **id**: Document identifier
- **content**: Document content snippet
- **score**: Similarity score (0.0 to 1.0, higher is better)
- **metadata**: Optional metadata (source, title, section, etc.)

## Output Format

RAG operations return standardized result structures:

```json
{
  "type": "rag",
  "source": "/toolfs/rag/query",
  "content": {
    "query": "...",
    "top_k": 3,
    "results": [...]
  },
  "success": true,
  "error": "error message if failed"
}
```

## Present Results to User

When presenting RAG search results:

```
✓ RAG search completed

Query: ToolFS skill architecture
Results: 3 matches found

1. doc-001 (score: 0.95)
   Source: documentation > skills
   Title: Skill System Overview
   Content: ToolFS provides a skill system that supports WASM modules...

2. doc-002 (score: 0.87)
   Source: documentation > architecture
   Title: Architecture Design
   Content: The skill architecture allows mounting custom handlers...

3. doc-003 (score: 0.82)
   Source: documentation > sandboxing
   Title: Security Model
   Content: WASM skills are executed in a sandboxed environment...
```

## Troubleshooting

### No Results Found

If search returns no results:

1. Try a different query or rephrase the search
2. Reduce specificity to broaden results
3. Verify the RAG store is populated with documents
4. Check if the query is properly URL-encoded

### Low Quality Results

If results are not relevant:

1. Increase `top_k` to see more options
2. Refine the query with more specific terms
3. Check if document embeddings are up to date
4. Verify the RAG store contains relevant documents

## Best Practices

1. **Use Semantic Queries**: RAG works best with natural language queries, not just keywords
2. **Adjust top_k**: Start with 5-10 results, adjust based on use case
3. **Review Scores**: Higher scores (>0.8) indicate strong relevance
4. **Check Metadata**: Use metadata to filter or categorize results
5. **Combine Results**: Combine multiple search queries for comprehensive coverage

---

*This skill is part of ToolFS. See [main SKILL.md](../SKILL.md) for overview.*

