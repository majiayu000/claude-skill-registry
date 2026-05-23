---
name: microsoft-extensions-ai
description: |
  Use when building provider-agnostic AI applications with Microsoft.Extensions.AI. Covers IChatClient, IEmbeddingGenerator, middleware pipelines, caching, telemetry, and DI integration for chat completions and embeddings.
  USE FOR: provider-agnostic AI abstractions, dependency-injected chat clients, embedding generation, middleware pipelines (caching, logging, rate limiting), switching between OpenAI/Azure/Ollama without code changes
  DO NOT USE FOR: Azure-specific model catalog features (use azure-ai-inference), building agent workflows with tools and orchestration (use agent-framework), MCP tool serving (use mcp), ML model training (use mlnet)
license: MIT
metadata:
  displayName: "Microsoft.Extensions.AI"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: ".NET AI Documentation"
    url: "https://learn.microsoft.com/dotnet/ai"
  - title: "Microsoft.Extensions.AI NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.Extensions.AI"
  - title: ".NET Extensions GitHub Repository"
    url: "https://github.com/dotnet/extensions"
---

# Microsoft.Extensions.AI

## Overview
Microsoft.Extensions.AI provides a set of provider-agnostic abstractions for AI services in .NET, centered on `IChatClient` for chat completions and `IEmbeddingGenerator<,>` for vector embeddings. It follows the same patterns as `ILogger` and `HttpClient` in .NET -- services program against interfaces, providers are configured at the composition root, and middleware can be composed in pipelines for caching, telemetry, rate limiting, and function calling.

## NuGet Packages
```bash
dotnet add package Microsoft.Extensions.AI
dotnet add package Microsoft.Extensions.AI.OpenAI        # OpenAI / Azure OpenAI provider
dotnet add package Microsoft.Extensions.AI.Ollama        # Ollama local models
dotnet add package Microsoft.Extensions.AI.AzureAIInference  # Azure AI model catalog
```

## Basic Chat Completion
```csharp
using Microsoft.Extensions.AI;

IChatClient chatClient = new OllamaChatClient(new Uri("http://localhost:11434"), "llama3.1");

var response = await chatClient.GetResponseAsync("What is dependency injection?");
Console.WriteLine(response.Messages.Last().Text);
```

## Streaming Chat Completion
```csharp
using Microsoft.Extensions.AI;

IChatClient chatClient = new OpenAIChatClient("gpt-4o", apiKey);

await foreach (var update in chatClient.GetStreamingResponseAsync("Explain SOLID principles"))
{
    Console.Write(update.Text);
}
Console.WriteLine();
```

## Multi-Turn Conversations
```csharp
var messages = new List<ChatMessage>
{
    new(ChatRole.System, "You are a C# tutor. Give concise explanations with code examples."),
    new(ChatRole.User, "What are records in C#?")
};

var response = await chatClient.GetResponseAsync(messages);
Console.WriteLine(response.Messages.Last().Text);

// Continue the conversation
messages.AddRange(response.Messages);
messages.Add(new ChatMessage(ChatRole.User, "How do they differ from classes?"));

var followUp = await chatClient.GetResponseAsync(messages);
Console.WriteLine(followUp.Messages.Last().Text);
```

## Chat Options
```csharp
var options = new ChatOptions
{
    Temperature = 0.3f,
    MaxOutputTokens = 2048,
    TopP = 0.9f,
    StopSequences = new[] { "```" },
    ResponseFormat = ChatResponseFormat.Json
};

var response = await chatClient.GetResponseAsync(
    "Return a JSON object with fields: name, age, city", options);
Console.WriteLine(response.Messages.Last().Text);
```

## Embedding Generation
```csharp
using Microsoft.Extensions.AI;

IEmbeddingGenerator<string, Embedding<float>> embeddingGenerator =
    new OllamaEmbeddingGenerator(new Uri("http://localhost:11434"), "all-minilm");

var embeddings = await embeddingGenerator.GenerateAsync(new[]
{
    "Dependency injection in .NET",
    "Entity Framework Core migrations",
    "ASP.NET Core middleware pipeline"
});

foreach (var embedding in embeddings)
{
    Console.WriteLine($"Dimensions: {embedding.Vector.Length}");
    Console.WriteLine($"First 5: [{string.Join(", ", embedding.Vector.ToArray().Take(5))}]");
}

// Cosine similarity between two embeddings
float CosineSimilarity(ReadOnlyMemory<float> a, ReadOnlyMemory<float> b)
{
    var aSpan = a.Span;
    var bSpan = b.Span;
    float dot = 0, normA = 0, normB = 0;
    for (int i = 0; i < aSpan.Length; i++)
    {
        dot += aSpan[i] * bSpan[i];
        normA += aSpan[i] * aSpan[i];
        normB += bSpan[i] * bSpan[i];
    }
    return dot / (MathF.Sqrt(normA) * MathF.Sqrt(normB));
}

float similarity = CosineSimilarity(embeddings[0].Vector, embeddings[1].Vector);
Console.WriteLine($"Similarity: {similarity:F4}");
```

## Tool Calling (Function Calling)
```csharp
using Microsoft.Extensions.AI;
using System.ComponentModel;

[Description("Gets the current weather for a city")]
static string GetWeather([Description("City name")] string city) =>
    city.ToLower() switch
    {
        "seattle" => "62F, cloudy",
        "new york" => "75F, sunny",
        _ => "Unknown"
    };

[Description("Calculates the tip amount")]
static decimal CalculateTip(
    [Description("Bill amount")] decimal amount,
    [Description("Tip percentage")] decimal percentage) =>
    amount * percentage / 100;

var chatOptions = new ChatOptions
{
    Tools = new AITool[]
    {
        AIFunctionFactory.Create(GetWeather),
        AIFunctionFactory.Create(CalculateTip)
    },
    ToolMode = ChatToolMode.Auto
};

var messages = new List<ChatMessage>
{
    new(ChatRole.User, "What's the weather in Seattle? Also, what's a 20% tip on $85?")
};

var response = await chatClient.GetResponseAsync(messages, chatOptions);
Console.WriteLine(response.Messages.Last().Text);
```

## Middleware Pipelines
Compose cross-cutting concerns as middleware layers around any `IChatClient`.

```csharp
using Microsoft.Extensions.AI;
using Microsoft.Extensions.Caching.Distributed;
using Microsoft.Extensions.Caching.Memory;

IChatClient pipeline = new ChatClientBuilder(new OpenAIChatClient("gpt-4o", apiKey))
    .UseDistributedCache(new MemoryDistributedCache(
        Options.Create(new MemoryDistributedCacheOptions())))
    .UseOpenTelemetry()
    .UseFunctionInvocation()
    .Build();

// All calls through this pipeline get caching, telemetry, and auto function invocation
var response = await pipeline.GetResponseAsync("What is LINQ?");
```

## Provider Comparison

| Provider Package | Backend | Use Case |
|-----------------|---------|----------|
| `Microsoft.Extensions.AI.OpenAI` | OpenAI API | Cloud-hosted GPT models |
| `Microsoft.Extensions.AI.AzureAIInference` | Azure AI | Enterprise Azure models |
| `Microsoft.Extensions.AI.Ollama` | Ollama | Local/self-hosted models |

## Dependency Injection
```csharp
var builder = WebApplication.CreateBuilder(args);

// Register IChatClient -- swap provider here without changing consuming code
builder.Services.AddChatClient(sp =>
    new ChatClientBuilder(new OpenAIChatClient("gpt-4o", apiKey))
        .UseDistributedCache(sp.GetRequiredService<IDistributedCache>())
        .UseOpenTelemetry()
        .UseFunctionInvocation()
        .Build());

builder.Services.AddEmbeddingGenerator<string, Embedding<float>>(sp =>
    new OllamaEmbeddingGenerator(new Uri("http://localhost:11434"), "all-minilm"));

builder.Services.AddDistributedMemoryCache();

var app = builder.Build();

app.MapPost("/chat", async (ChatRequest request, IChatClient chatClient) =>
{
    var messages = new List<ChatMessage>
    {
        new(ChatRole.User, request.Message)
    };
    var response = await chatClient.GetResponseAsync(messages);
    return Results.Ok(new { reply = response.Messages.Last().Text });
});

app.MapPost("/embed", async (EmbedRequest request,
    IEmbeddingGenerator<string, Embedding<float>> generator) =>
{
    var embeddings = await generator.GenerateAsync(new[] { request.Text });
    return Results.Ok(new { vector = embeddings[0].Vector.ToArray() });
});

app.Run();

record ChatRequest(string Message);
record EmbedRequest(string Text);
```

## Service Pattern with IChatClient
```csharp
public sealed class SummaryService(IChatClient chatClient)
{
    public async Task<string> SummarizeAsync(string text, CancellationToken ct = default)
    {
        var messages = new List<ChatMessage>
        {
            new(ChatRole.System, "Summarize the following text in 3 bullet points."),
            new(ChatRole.User, text)
        };

        var options = new ChatOptions
        {
            Temperature = 0.2f,
            MaxOutputTokens = 512
        };

        var response = await chatClient.GetResponseAsync(messages, options, ct);
        return response.Messages.Last().Text ?? "";
    }
}

public sealed class ClassificationService(IChatClient chatClient)
{
    public async Task<string> ClassifyAsync(string input, string[] categories, CancellationToken ct = default)
    {
        var categoryList = string.Join(", ", categories);
        var messages = new List<ChatMessage>
        {
            new(ChatRole.System,
                $"Classify the input into one of these categories: {categoryList}. Return only the category name."),
            new(ChatRole.User, input)
        };

        var options = new ChatOptions
        {
            Temperature = 0.0f,
            MaxOutputTokens = 50
        };

        var response = await chatClient.GetResponseAsync(messages, options, ct);
        return response.Messages.Last().Text?.Trim() ?? "";
    }
}
```

## Best Practices
- Program against `IChatClient` and `IEmbeddingGenerator<,>` interfaces in all service code; configure the concrete provider (`OpenAIChatClient`, `OllamaChatClient`) only at the composition root to enable swapping providers without code changes.
- Use `ChatClientBuilder` to compose middleware (caching, telemetry, function invocation) in a pipeline rather than implementing cross-cutting concerns in every service method.
- Register `IChatClient` via `AddChatClient` in DI and inject it with constructor injection; avoid resolving clients from `IServiceProvider` manually.
- Set `Temperature = 0.0f` for deterministic tasks (classification, extraction, structured output) and `0.7f-1.0f` for creative tasks (writing, brainstorming).
- Always pass `CancellationToken` through to `GetResponseAsync` and `GetStreamingResponseAsync` so that HTTP request cancellations propagate to the underlying provider.
- Use `ChatResponseFormat.Json` with structured output prompts when you need machine-parseable responses rather than free-form text.
- Cache embedding results with `UseDistributedCache` when the same texts are embedded repeatedly (e.g., static document chunks) to avoid redundant API calls.
- Create focused service classes (e.g., `SummaryService`, `ClassificationService`) that encapsulate system prompts and chat options rather than spreading prompt engineering across controllers.
- Use `AIFunctionFactory.Create` to wrap strongly-typed C# methods as tools with automatic schema generation from `[Description]` attributes, rather than manually defining JSON schemas.
- Monitor token usage and latency by adding `UseOpenTelemetry()` to the pipeline and exporting traces to your observability backend (Jaeger, Application Insights, Aspire Dashboard).
