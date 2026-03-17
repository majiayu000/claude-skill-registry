---
name: koan-ai-integration
description: Chat endpoints, embeddings, RAG workflows, vector search
---

# Koan AI Integration

## Core Principle

**AI capabilities integrate seamlessly with entity patterns.** Store embeddings on entities, use vector repositories for search, and leverage standard Entity<T> patterns for AI-enriched data.

## Quick Reference

### Chat Endpoints

```csharp
public class ChatController : ControllerBase
{
    private readonly IAi _ai;

    [HttpPost]
    public async Task<IActionResult> Chat(
        [FromBody] ChatRequest request,
        CancellationToken ct)
    {
        var response = await _ai.ChatAsync(new AiChatRequest
        {
            Model = "gpt-4",
            Messages = request.Messages,
            SystemPrompt = "You are a helpful assistant.",
            Temperature = 0.7
        }, ct);

        return Ok(new { message = response.Content, usage = response.Usage });
    }
}
```

### Entity with Embeddings

```csharp
[DataAdapter("weaviate")] // Force vector database
public class ProductSearch : Entity<ProductSearch>
{
    public string ProductId { get; set; } = "";
    public string Description { get; set; } = "";

    [VectorField]
    public float[] DescriptionEmbedding { get; set; } = Array.Empty<float>();

    // Semantic search
    public static async Task<List<ProductSearch>> SimilarTo(
        string query,
        CancellationToken ct = default)
    {
        return await Vector<ProductSearch>.SearchAsync(query, limit: 10, ct);
    }
}
```

### RAG Workflow

```csharp
public class KnowledgeBaseService
{
    private readonly IAi _ai;

    public async Task<string> AnswerQuestion(string question, CancellationToken ct)
    {
        // 1. Find relevant documents via vector search
        var relevantDocs = await KnowledgeDocument.SimilarTo(question, ct);

        // 2. Build context from documents
        var context = string.Join("\n\n", relevantDocs.Select(d => d.Content));

        // 3. Query AI with context
        var response = await _ai.ChatAsync(new AiChatRequest
        {
            Model = "gpt-4",
            SystemPrompt = $"Answer based on this context:\n\n{context}",
            Messages = new[] { new AiMessage { Role = "user", Content = question } }
        }, ct);

        return response.Content;
    }
}
```

### Configuration

```json
{
  "Koan": {
    "AI": {
      "Providers": {
        "Primary": {
          "Type": "OpenAI",
          "ApiKey": "{OPENAI_API_KEY}",
          "Model": "gpt-4"
        },
        "Fallback": {
          "Type": "Ollama",
          "BaseUrl": "http://localhost:11434",
          "Model": "llama2"
        }
      }
    },
    "Data": {
      "Sources": {
        "Vectors": {
          "Adapter": "weaviate",
          "ConnectionString": "http://localhost:8080"
        }
      }
    }
  }
}
```

## When This Skill Applies

- ✅ Integrating AI features
- ✅ Semantic search
- ✅ Chat interfaces
- ✅ Embeddings generation
- ✅ RAG workflows
- ✅ AI-enriched entities

## Reference Documentation

- **Full Guide:** `docs/guides/ai-integration.md`
- **Vector How-To:** `docs/guides/ai-vector-howto.md`
- **Sample:** `samples/S5.Recs/` (AI recommendation engine)
- **Sample:** `samples/S16.PantryPal/` (Vision AI integration)
