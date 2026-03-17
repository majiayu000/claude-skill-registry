---
name: evaluations
description: |
  Use when evaluating AI model outputs, prompts, and LLM application quality in .NET. Covers Microsoft.Extensions.AI.Evaluation for scoring, reporting, and automated test pipelines.
  USE FOR: evaluating LLM response quality, measuring prompt effectiveness, automated AI output scoring, building evaluation pipelines for chat applications, comparing model performance across providers
  DO NOT USE FOR: unit testing non-AI code (use xunit/nunit), load testing HTTP APIs (use k6 or NBomber), monitoring production metrics (use OpenTelemetry), training ML models (use mlnet)
license: MIT
metadata:
  displayName: "AI Evaluations"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: ".NET AI Documentation"
    url: "https://learn.microsoft.com/dotnet/ai"
  - title: "Microsoft.Extensions.AI.Evaluation NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.Extensions.AI.Evaluation"
  - title: ".NET Extensions GitHub Repository"
    url: "https://github.com/dotnet/extensions"
---

# AI Evaluations

## Overview
Microsoft.Extensions.AI.Evaluation provides a structured framework for scoring and reporting on the quality of AI model outputs in .NET applications. It includes built-in evaluators for relevance, coherence, fluency, and groundedness, as well as support for custom evaluators. The framework integrates with `IChatClient` from Microsoft.Extensions.AI to evaluate chat-based interactions end-to-end.

## NuGet Packages
```bash
dotnet add package Microsoft.Extensions.AI.Evaluation
dotnet add package Microsoft.Extensions.AI.Evaluation.Quality
dotnet add package Microsoft.Extensions.AI.Evaluation.Reporting
dotnet add package Microsoft.Extensions.AI
```

## Built-in Evaluators
The Quality package provides pre-built evaluators that use an LLM as a judge to score responses.

```csharp
using Microsoft.Extensions.AI;
using Microsoft.Extensions.AI.Evaluation;
using Microsoft.Extensions.AI.Evaluation.Quality;

// Create an evaluator that scores on multiple quality dimensions
var evaluators = new IEvaluator[]
{
    new RelevanceEvaluator(),
    new CoherenceEvaluator(),
    new FluencyEvaluator(),
    new GroundednessEvaluator()
};

var chatClient = new ChatCompletionsClient(endpoint, credential)
    .AsChatClient("gpt-4o");

var evaluatorClient = chatClient;  // Can use same or different model as judge

var chatOptions = new ChatOptions { Temperature = 0.7f };

// The conversation to evaluate
var messages = new List<ChatMessage>
{
    new(ChatRole.System, "You are a helpful assistant that answers questions about .NET."),
    new(ChatRole.User, "What is dependency injection in .NET?")
};

var response = await chatClient.GetResponseAsync(messages, chatOptions);

// Run evaluation
var context = new EvaluationContext
{
    Messages = messages,
    Response = response,
    GroundTruth = "Dependency injection is a design pattern where objects receive their dependencies from external sources rather than creating them internally. In .NET, it is built into the framework via Microsoft.Extensions.DependencyInjection."
};

var results = new List<EvaluationResult>();
foreach (var evaluator in evaluators)
{
    var result = await evaluator.EvaluateAsync(context, evaluatorClient);
    results.Add(result);
    Console.WriteLine($"{evaluator.Name}: {result.Score:F2} - {result.Explanation}");
}
```

## Evaluation Result Scores

| Evaluator | Score Range | Measures |
|-----------|-----------|----------|
| `RelevanceEvaluator` | 1-5 | How well the response addresses the user's question |
| `CoherenceEvaluator` | 1-5 | Logical flow and consistency of the response |
| `FluencyEvaluator` | 1-5 | Grammatical correctness and readability |
| `GroundednessEvaluator` | 1-5 | Factual accuracy against provided ground truth |

## Custom Evaluators
Build domain-specific evaluators by implementing the `IEvaluator` interface.

```csharp
using Microsoft.Extensions.AI.Evaluation;

public class CodeQualityEvaluator : IEvaluator
{
    public string Name => "CodeQuality";

    public async Task<EvaluationResult> EvaluateAsync(
        EvaluationContext context, IChatClient judgeChatClient,
        CancellationToken cancellationToken = default)
    {
        var responseText = context.Response?.Messages
            .LastOrDefault()?.Text ?? "";

        // Use LLM as judge for code quality
        var judgePrompt = $"""
            Evaluate the following code response for quality on a scale of 1-5:
            1 = Does not compile or has critical errors
            2 = Compiles but has significant issues
            3 = Functional but lacks best practices
            4 = Good quality with minor improvements possible
            5 = Excellent, production-ready code

            Response to evaluate:
            {responseText}

            Return ONLY a JSON object: {{"score": <number>, "explanation": "<reason>"}}
            """;

        var judgeMessages = new List<ChatMessage>
        {
            new(ChatRole.User, judgePrompt)
        };

        var judgeResponse = await judgeChatClient.GetResponseAsync(
            judgeMessages, cancellationToken: cancellationToken);

        var parsed = JsonSerializer.Deserialize<JudgeResult>(
            judgeResponse.Messages.Last().Text!);

        return new EvaluationResult
        {
            Score = parsed?.Score ?? 0,
            Explanation = parsed?.Explanation ?? "Failed to parse judge response"
        };
    }
}

record JudgeResult(float Score, string Explanation);
```

## Evaluation Reporting
Generate structured reports from evaluation runs.

```csharp
using Microsoft.Extensions.AI.Evaluation.Reporting;

var reportBuilder = new EvaluationReportBuilder("ChatBot Evaluation Run");

var testCases = new[]
{
    ("What is LINQ?", "LINQ is Language Integrated Query in .NET."),
    ("Explain async/await.", "Async/await enables asynchronous programming in C#."),
    ("What is EF Core?", "Entity Framework Core is an ORM for .NET.")
};

foreach (var (question, groundTruth) in testCases)
{
    var messages = new List<ChatMessage>
    {
        new(ChatRole.System, "You are a .NET expert."),
        new(ChatRole.User, question)
    };

    var response = await chatClient.GetResponseAsync(messages);

    var context = new EvaluationContext
    {
        Messages = messages,
        Response = response,
        GroundTruth = groundTruth
    };

    var scores = new Dictionary<string, EvaluationResult>();
    foreach (var evaluator in evaluators)
    {
        var result = await evaluator.EvaluateAsync(context, evaluatorClient);
        scores[evaluator.Name] = result;
    }

    reportBuilder.AddEntry(new EvaluationReportEntry
    {
        Input = question,
        Output = response.Messages.Last().Text ?? "",
        GroundTruth = groundTruth,
        Scores = scores
    });
}

var report = reportBuilder.Build();
Console.WriteLine($"Average Relevance: {report.AverageScore("Relevance"):F2}");
Console.WriteLine($"Average Coherence: {report.AverageScore("Coherence"):F2}");
```

## Integration with Test Frameworks
```csharp
using Xunit;
using Microsoft.Extensions.AI.Evaluation;
using Microsoft.Extensions.AI.Evaluation.Quality;

public class ChatBotEvaluationTests
{
    private readonly IChatClient _chatClient;
    private readonly IChatClient _judgeClient;

    public ChatBotEvaluationTests()
    {
        _chatClient = CreateChatClient();
        _judgeClient = CreateJudgeClient();
    }

    [Theory]
    [InlineData("What is C#?", 3.5f)]
    [InlineData("Explain generics in .NET.", 3.5f)]
    [InlineData("How does garbage collection work?", 3.0f)]
    public async Task Response_MeetsQualityThreshold(string question, float minScore)
    {
        var messages = new List<ChatMessage>
        {
            new(ChatRole.System, "You are a .NET expert. Be concise and accurate."),
            new(ChatRole.User, question)
        };

        var response = await _chatClient.GetResponseAsync(messages);

        var evaluator = new RelevanceEvaluator();
        var context = new EvaluationContext
        {
            Messages = messages,
            Response = response
        };

        var result = await evaluator.EvaluateAsync(context, _judgeClient);

        Assert.True(result.Score >= minScore,
            $"Relevance score {result.Score} below threshold {minScore}. " +
            $"Explanation: {result.Explanation}");
    }

    [Fact]
    public async Task Response_IsGroundedInProvidedContext()
    {
        var context = "ASP.NET Core supports Kestrel and IIS as web servers.";
        var question = "What web servers does ASP.NET Core support?";

        var messages = new List<ChatMessage>
        {
            new(ChatRole.System, $"Answer based on this context: {context}"),
            new(ChatRole.User, question)
        };

        var response = await _chatClient.GetResponseAsync(messages);

        var evaluator = new GroundednessEvaluator();
        var evalContext = new EvaluationContext
        {
            Messages = messages,
            Response = response,
            GroundTruth = context
        };

        var result = await evaluator.EvaluateAsync(evalContext, _judgeClient);
        Assert.True(result.Score >= 4.0f, $"Groundedness: {result.Score} - {result.Explanation}");
    }
}
```

## Batch Evaluation Pipeline
```csharp
public class EvaluationPipeline
{
    private readonly IChatClient _targetClient;
    private readonly IChatClient _judgeClient;
    private readonly IEvaluator[] _evaluators;

    public EvaluationPipeline(
        IChatClient targetClient, IChatClient judgeClient, params IEvaluator[] evaluators)
    {
        _targetClient = targetClient;
        _judgeClient = judgeClient;
        _evaluators = evaluators;
    }

    public async Task<EvaluationSummary> RunAsync(
        IReadOnlyList<EvaluationTestCase> testCases,
        CancellationToken cancellationToken = default)
    {
        var allResults = new List<(string TestCase, Dictionary<string, float> Scores)>();

        foreach (var testCase in testCases)
        {
            var messages = new List<ChatMessage>
            {
                new(ChatRole.System, testCase.SystemPrompt),
                new(ChatRole.User, testCase.UserMessage)
            };

            var response = await _targetClient.GetResponseAsync(
                messages, cancellationToken: cancellationToken);

            var context = new EvaluationContext
            {
                Messages = messages,
                Response = response,
                GroundTruth = testCase.ExpectedAnswer
            };

            var scores = new Dictionary<string, float>();
            foreach (var evaluator in _evaluators)
            {
                var result = await evaluator.EvaluateAsync(
                    context, _judgeClient, cancellationToken);
                scores[evaluator.Name] = result.Score;
            }

            allResults.Add((testCase.UserMessage, scores));
        }

        return new EvaluationSummary(allResults);
    }
}

public record EvaluationTestCase(
    string SystemPrompt, string UserMessage, string ExpectedAnswer);

public record EvaluationSummary(
    List<(string TestCase, Dictionary<string, float> Scores)> Results)
{
    public float AverageScore(string evaluatorName) =>
        Results.Average(r => r.Scores.GetValueOrDefault(evaluatorName, 0));
}
```

## Best Practices
- Use a stronger or equal-capability model as the judge (e.g., GPT-4o judging GPT-4o-mini outputs) because weaker models produce unreliable quality assessments.
- Include ground truth / reference answers in `EvaluationContext.GroundTruth` for `GroundednessEvaluator` to measure factual accuracy against known-correct information.
- Run evaluations on at least 50-100 diverse test cases per prompt variation to get statistically meaningful quality scores rather than relying on a handful of examples.
- Set a temperature of 0.0 on the judge model to ensure deterministic, reproducible scoring across evaluation runs.
- Create domain-specific evaluators (e.g., `CodeQualityEvaluator`, `ToneEvaluator`) for aspects that generic evaluators do not cover, using structured JSON output prompts for reliable score parsing.
- Integrate evaluation tests into CI/CD pipelines with minimum score thresholds so that prompt regressions are caught before deployment.
- Version your evaluation datasets and prompts alongside application code so that score changes can be attributed to specific code or prompt modifications.
- Log individual evaluation scores with the prompt version, model name, and timestamp to build trend dashboards that reveal quality degradation over time.
- Use separate evaluator instances for different quality dimensions rather than combining multiple criteria into a single prompt, which reduces judge accuracy.
- Compare evaluation results across model providers (e.g., GPT-4o vs. Mistral Large) using identical test cases and evaluators to make data-driven model selection decisions.
