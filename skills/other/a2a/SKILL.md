---
name: a2a
description: |
  Use when building agent-to-agent communication in .NET with the A2A (Agent-to-Agent) protocol. Covers agent cards, task lifecycle, streaming, push notifications, and multi-agent orchestration.
  USE FOR: agent-to-agent communication, multi-agent orchestration, agent discovery via agent cards, task-based messaging between AI agents, A2A protocol server and client implementation
  DO NOT USE FOR: Model Context Protocol tool serving (use mcp), direct LLM API calls (use microsoft-extensions-ai or azure-ai-inference), human-to-agent chat UIs, simple single-agent scenarios without inter-agent communication
license: MIT
metadata:
  displayName: "A2A Protocol"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "A2A Protocol GitHub Repository"
    url: "https://github.com/a2aproject/A2A"
  - title: "SharpA2A.Core NuGet Package"
    url: "https://www.nuget.org/packages/SharpA2A.Core"
  - title: "SharpA2A GitHub Repository"
    url: "https://github.com/darrelmiller/sharpa2a"
---

# A2A Protocol

## Overview
A2A (Agent-to-Agent) is an open protocol by Google that enables AI agents built on different frameworks to discover each other, negotiate capabilities, and collaborate on tasks. The .NET SDK (`SharpA2A`) provides a strongly-typed client and server implementation with support for agent cards, task lifecycle management, streaming via SSE, and push notifications.

## NuGet Packages
```bash
dotnet add package SharpA2A.Core
dotnet add package SharpA2A.AspNetCore
```

## Agent Cards
An agent card is a JSON metadata document that advertises an agent's capabilities, skills, and endpoint. Agents discover each other by fetching `/.well-known/agent.json`.

```csharp
using SharpA2A.Core;

var agentCard = new AgentCard
{
    Name = "ResearchAgent",
    Description = "Searches academic papers and summarizes findings",
    Url = "https://research-agent.example.com",
    Version = "1.0.0",
    Capabilities = new AgentCapabilities
    {
        Streaming = true,
        PushNotifications = false
    },
    Skills = new List<AgentSkill>
    {
        new AgentSkill
        {
            Id = "paper-search",
            Name = "Paper Search",
            Description = "Search and summarize academic papers on a given topic",
            Tags = new List<string> { "research", "academic", "papers" },
            Examples = new List<string>
            {
                "Find recent papers on transformer architectures",
                "Summarize the key findings in federated learning research"
            }
        }
    },
    DefaultInputModes = new List<string> { "text/plain" },
    DefaultOutputModes = new List<string> { "text/plain", "text/markdown" }
};
```

## A2A Server with ASP.NET Core
```csharp
using SharpA2A.Core;
using SharpA2A.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

var agentCard = new AgentCard
{
    Name = "SummaryAgent",
    Description = "Summarizes long documents into concise bullet points",
    Url = "https://localhost:5001",
    Version = "1.0.0",
    Capabilities = new AgentCapabilities { Streaming = true }
};

builder.Services.AddA2AServer(agentCard, async (taskRequest, cancellationToken) =>
{
    var userMessage = taskRequest.Messages.LastOrDefault()?.Parts
        .OfType<TextPart>().FirstOrDefault()?.Text ?? "";

    var summary = await SummarizeDocumentAsync(userMessage, cancellationToken);

    return new TaskResponse
    {
        Status = new TaskStatus { State = TaskState.Completed },
        Artifacts = new List<Artifact>
        {
            new Artifact
            {
                Name = "summary",
                Parts = new List<Part> { new TextPart { Text = summary } }
            }
        }
    };
});

var app = builder.Build();
app.MapA2AEndpoints();
app.Run();
```

## A2A Client
```csharp
using SharpA2A.Core;

var client = new A2AClient("https://research-agent.example.com");

// Discover agent capabilities
var card = await client.GetAgentCardAsync();
Console.WriteLine($"Agent: {card.Name}, Skills: {card.Skills.Count}");

// Send a task
var taskRequest = new TaskSendParams
{
    Id = Guid.NewGuid().ToString(),
    Message = new Message
    {
        Role = "user",
        Parts = new List<Part>
        {
            new TextPart { Text = "Summarize recent advances in quantum computing" }
        }
    }
};

var response = await client.SendTaskAsync(taskRequest);
Console.WriteLine($"Task state: {response.Status.State}");

foreach (var artifact in response.Artifacts ?? Enumerable.Empty<Artifact>())
{
    foreach (var part in artifact.Parts.OfType<TextPart>())
    {
        Console.WriteLine(part.Text);
    }
}
```

## Streaming Responses
```csharp
var streamRequest = new TaskSendParams
{
    Id = Guid.NewGuid().ToString(),
    Message = new Message
    {
        Role = "user",
        Parts = new List<Part>
        {
            new TextPart { Text = "Write a detailed analysis of climate data trends" }
        }
    }
};

await foreach (var update in client.SendTaskStreamingAsync(streamRequest))
{
    if (update is TaskStatusUpdateEvent statusUpdate)
    {
        Console.WriteLine($"Status: {statusUpdate.Status.State}");
        if (statusUpdate.Status.Message is { } msg)
        {
            foreach (var part in msg.Parts.OfType<TextPart>())
            {
                Console.Write(part.Text);
            }
        }
    }
    else if (update is TaskArtifactUpdateEvent artifactUpdate)
    {
        foreach (var part in artifactUpdate.Artifact.Parts.OfType<TextPart>())
        {
            Console.Write(part.Text);
        }
    }
}
```

## Task Lifecycle
The A2A protocol defines a clear task state machine:

| State | Description |
|-------|-------------|
| `Submitted` | Task received by the agent, not yet started |
| `Working` | Agent is actively processing the task |
| `InputRequired` | Agent needs additional input from the caller |
| `Completed` | Task finished successfully with artifacts |
| `Failed` | Task encountered an unrecoverable error |
| `Canceled` | Task was canceled by the caller or agent |

```csharp
// Handling multi-turn conversations (InputRequired state)
var response = await client.SendTaskAsync(initialRequest);

while (response.Status.State == TaskState.InputRequired)
{
    var followUpMessage = response.Status.Message?.Parts
        .OfType<TextPart>().FirstOrDefault()?.Text;
    Console.WriteLine($"Agent asks: {followUpMessage}");

    var userInput = Console.ReadLine()!;
    var followUp = new TaskSendParams
    {
        Id = response.Id,
        Message = new Message
        {
            Role = "user",
            Parts = new List<Part> { new TextPart { Text = userInput } }
        }
    };
    response = await client.SendTaskAsync(followUp);
}
```

## Multi-Agent Orchestration
```csharp
public class OrchestratorAgent
{
    private readonly Dictionary<string, A2AClient> _agents = new();

    public async Task RegisterAgentAsync(string agentUrl)
    {
        var client = new A2AClient(agentUrl);
        var card = await client.GetAgentCardAsync();
        _agents[card.Name] = client;
    }

    public async Task<string> DelegateTaskAsync(string skillTag, string prompt)
    {
        // Find an agent that has the required skill
        foreach (var (name, client) in _agents)
        {
            var card = await client.GetAgentCardAsync();
            var matchingSkill = card.Skills
                .FirstOrDefault(s => s.Tags.Contains(skillTag));

            if (matchingSkill is not null)
            {
                var request = new TaskSendParams
                {
                    Id = Guid.NewGuid().ToString(),
                    Message = new Message
                    {
                        Role = "user",
                        Parts = new List<Part> { new TextPart { Text = prompt } }
                    }
                };

                var result = await client.SendTaskAsync(request);
                return result.Artifacts?.FirstOrDefault()?.Parts
                    .OfType<TextPart>().FirstOrDefault()?.Text
                    ?? "No result";
            }
        }
        throw new InvalidOperationException($"No agent found with skill tag '{skillTag}'");
    }
}
```

## Best Practices
- Publish an agent card at `/.well-known/agent.json` with accurate skill descriptions and supported input/output modes so callers can discover and filter agents programmatically.
- Use unique, deterministic task IDs (e.g., combining a request correlation ID with a timestamp) to enable idempotent retries and task tracking across agents.
- Implement the `InputRequired` state for multi-turn interactions instead of trying to collect all information upfront in a single prompt.
- Return structured `Artifact` objects with explicit MIME types rather than embedding results in status messages, so downstream agents can parse outputs reliably.
- Enable streaming (`Capabilities.Streaming = true`) for long-running tasks so callers receive incremental progress rather than blocking on a single response.
- Version your agent cards and skill schemas; include a `Version` field and avoid breaking changes to skill IDs or parameter formats across releases.
- Validate incoming task messages against expected input modes before processing and return a `Failed` state with a descriptive error when validation fails.
- Register agent clients via dependency injection with `AddA2AServer` rather than constructing clients manually, to enable proper lifetime management and testability.
- Implement cancellation token propagation through the entire task handler chain so that canceled tasks release resources promptly.
- Log task state transitions with correlation IDs to enable distributed tracing across multi-agent orchestrations.
