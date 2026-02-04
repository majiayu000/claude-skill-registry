---
name: microsoft-agent-framework
description: Expert guidance for building AI agents and multi-agent workflows using Microsoft Agent Framework for .NET. Use when (1) creating AI agents with OpenAI or Azure OpenAI, (2) implementing function tools and structured outputs, (3) building multi-turn conversations, (4) designing graph-based workflows with streaming/checkpointing, (5) implementing middleware pipelines, (6) orchestrating multi-agent systems with fan-out/fan-in patterns, (7) adding human-in-the-loop interactions, (8) integrating OpenTelemetry observability, or (9) exposing agents as MCP tools.
---

# Microsoft Agent Framework for .NET

## Overview

Microsoft Agent Framework is a framework for building, orchestrating, and deploying AI agents and multi-agent workflows. It provides graph-based workflows with streaming, checkpointing, human-in-the-loop, and time-travel capabilities.

## Installation

```bash
# Core AI package
dotnet add package Microsoft.Agents.AI

# OpenAI/Azure OpenAI support
dotnet add package Microsoft.Agents.AI.OpenAI --prerelease

# Google Gemini support (via Microsoft.Extensions.AI)
dotnet add package Mscc.GenerativeAI.Microsoft

# Azure identity for authentication
dotnet add package Azure.Identity
```

## Quick Start

### Basic Agent with OpenAI

```csharp
using Microsoft.Agents.AI;
using OpenAI;

var agent = new OpenAIClient("<api-key>")
    .GetOpenAIResponseClient("gpt-4o-mini")
    .CreateAIAgent(
        name: "Assistant",
        instructions: "You are a helpful assistant."
    );

Console.WriteLine(await agent.RunAsync("Hello!"));
```

### Azure OpenAI with Azure CLI Auth

```csharp
using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Agents.AI;

var agent = new AzureOpenAIClient(
    new Uri("https://<resource>.openai.azure.com/"),
    new AzureCliCredential())
    .GetChatClient("gpt-4o-mini")
    .CreateAIAgent(instructions: "You are helpful.");

Console.WriteLine(await agent.RunAsync("Tell me a joke."));
```

### Azure OpenAI with Bearer Token

```csharp
var agent = new OpenAIClient(
    new BearerTokenPolicy(
        new AzureCliCredential(),
        "https://ai.azure.com/.default"),
    new OpenAIClientOptions
    {
        Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1")
    })
    .GetOpenAIResponseClient("gpt-4o-mini")
    .CreateAIAgent(name: "Bot", instructions: "You are helpful.");
```

### Google Gemini

```csharp
using Mscc.GenerativeAI;
using Mscc.GenerativeAI.Microsoft;
using Microsoft.Agents.AI;

var googleAI = new GoogleAI("<gemini-api-key>");
var geminiModel = googleAI.GenerativeModel("gemini-2.0-flash");
IChatClient chatClient = geminiModel.AsIChatClient();

var agent = chatClient.CreateAIAgent(
    name: "Assistant",
    instructions: "You are a helpful assistant."
);

Console.WriteLine(await agent.RunAsync("Hello!"));
```

## Function Tools

Define tools using attributes:

```csharp
public class WeatherTools
{
    [Description("Gets current weather for a location")]
    public static string GetWeather(
        [Description("City name")] string city)
    {
        return $"Weather in {city}: Sunny, 72F";
    }
}

// Register tools with agent
var agent = client.GetChatClient("gpt-4o-mini")
    .CreateAIAgent(
        instructions: "Help users check weather.",
        tools: [typeof(WeatherTools)]);

await agent.RunAsync("What's the weather in Seattle?");
```

### Function Tools with Approval

For human-in-the-loop approval:

```csharp
agent.OnToolCall += (sender, args) =>
{
    Console.WriteLine($"Tool: {args.ToolName}");
    Console.Write("Approve? (y/n): ");
    args.Approved = Console.ReadLine()?.ToLower() == "y";
};
```

## Structured Output

Return strongly-typed responses:

```csharp
public class MovieRecommendation
{
    public string Title { get; set; }
    public string Genre { get; set; }
    public int Year { get; set; }
    public string Reason { get; set; }
}

var result = await agent.RunAsync<MovieRecommendation>(
    "Recommend a sci-fi movie from the 2020s");

Console.WriteLine($"{result.Title} ({result.Year}) - {result.Reason}");
```

## Multi-Turn Conversations

```csharp
var agent = client.GetChatClient("gpt-4o-mini")
    .CreateAIAgent(instructions: "You are a helpful assistant.");

// First turn
var response1 = await agent.RunAsync("My name is Alice.");

// Continues context
var response2 = await agent.RunAsync("What's my name?");
```

## Persisted Conversations

Save and restore conversation state:

```csharp
// Save state
var state = agent.GetConversationState();
await File.WriteAllTextAsync("state.json", state.ToJson());

// Restore later
var savedState = ConversationState.FromJson(
    await File.ReadAllTextAsync("state.json"));
agent.LoadConversationState(savedState);
```

## Middleware

Add custom processing pipelines:

```csharp
agent.UseMiddleware(async (context, next) =>
{
    Console.WriteLine($"Request: {context.Input}");
    var start = DateTime.UtcNow;

    await next();

    var duration = DateTime.UtcNow - start;
    Console.WriteLine($"Response time: {duration.TotalMilliseconds}ms");
});
```

## Multi-Modal (Images)

```csharp
var result = await agent.RunAsync(
    "Describe this image",
    images: [File.ReadAllBytes("photo.jpg")]);
```

## Observability with OpenTelemetry

```csharp
using var tracerProvider = Sdk.CreateTracerProviderBuilder()
    .AddSource("Microsoft.Agents")
    .AddConsoleExporter()
    .Build();

// Agent calls are now traced
await agent.RunAsync("Hello!");
```

## Dependency Injection

```csharp
services.AddSingleton<AIAgent>(sp =>
{
    var client = sp.GetRequiredService<OpenAIClient>();
    return client.GetChatClient("gpt-4o-mini")
        .CreateAIAgent(instructions: "You are helpful.");
});
```

## Agent as MCP Tool

Expose agent as Model Context Protocol tool:

```csharp
var mcpTool = agent.AsMcpTool(
    name: "research_assistant",
    description: "Researches topics and provides summaries");
```

## Agent as Function Tool

Compose agents by exposing one as a tool for another:

```csharp
var researchAgent = client.GetChatClient("gpt-4o")
    .CreateAIAgent(instructions: "You do deep research.");

var mainAgent = client.GetChatClient("gpt-4o-mini")
    .CreateAIAgent(
        instructions: "Answer questions, use research tool for complex topics.",
        tools: [researchAgent.AsFunctionTool("research", "Deep research")]);
```

## Workflows

For complex multi-agent orchestration, see [references/workflows.md](references/workflows.md).

Key workflow patterns:
- **Executors and Edges**: Basic workflow building blocks
- **Streaming**: Real-time event streaming
- **Fan-Out/Fan-In**: Parallel processing
- **Checkpointing**: Save and resume workflow state
- **Human-in-the-Loop**: Pause for user input
- **Writer-Critic**: Iterative refinement loops

## Best Practices

1. **Use Azure CLI credentials** for local development
2. **Add OpenTelemetry** for production observability
3. **Implement middleware** for logging, error handling, rate limiting
4. **Use structured outputs** when you need typed responses
5. **Persist conversation state** for stateless services
6. **Use checkpointing** in workflows for reliability
7. **Implement human-in-the-loop** for sensitive operations

## Resources

- [GitHub Repository](https://github.com/microsoft/agent-framework)
- [MS Learn Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [Quick Start Guide](https://learn.microsoft.com/agent-framework/tutorials/quick-start)
- [Samples](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples)
