---
name: langchain4j-tool-function-calling-patterns
description: "Provides and generates LangChain4j tool and function calling patterns: annotates methods as tools with @Tool, configures tool executors, registers tools with AiServices, validates tool parameters, and handles tool execution errors. Use when building AI agents that call tools, define function specifications, manage tool responses, or integrate external APIs with LLM-driven applications."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# LangChain4j Tool & Function Calling Patterns

Provides patterns for annotating methods as tools, configuring tool executors, registering tools with AI services, validating parameters, and handling tool execution errors in LangChain4j applications.

## Overview

LangChain4j uses the `@Tool` annotation to expose Java methods as callable functions for AI agents. The `AiServices` builder registers tools with a chat model, enabling LLMs to perform actions beyond text generation: database queries, API calls, calculations, and business system integrations. Parameters use `@P` for descriptions that guide the LLM.

## When to Use

- Building AI agents that call external tools (weather, stocks, database queries)
- Defining function specifications for LLM tool use (`@Tool`, `@P` annotations)
- Registering and managing tool sets with `AiServices.builder().tools()`
- Handling tool execution errors, timeouts, and hallucinated tool names
- Implementing context-aware tools that inject user state via `@ToolMemoryId`
- Configuring dynamic tool providers for large or conditional tool sets

## Instructions

### 1. Annotate Methods with `@Tool`

Define a tool class with methods annotated `@Tool`. Provide a description as the first parameter. Use `@P` for each parameter description.

```java
public class WeatherTools {
    private final WeatherService weatherService;

    public WeatherTools(WeatherService weatherService) {
        this.weatherService = weatherService;
    }

    @Tool("Get current weather for a city")
    public String getWeather(
            @P("City name") String city,
            @P("Temperature unit: celsius or fahrenheit") String unit) {
        return weatherService.getWeather(city, unit);
    }
}
```

**Validate**: Create an instance and confirm the class loads without errors.

### 2. Register Tools with AiServices

Use `AiServices.builder()` to register tool instances with the chat model.

```java
MathAssistant assistant = AiServices.builder(MathAssistant.class)
    .chatModel(chatModel)
    .tools(new Calculator(), new WeatherTools(weatherService))
    .build();
```

**Validate**: Call `assistant.chat("What is 2 + 2?")` and verify the LLM responds without throwing.

### 3. Test Tool Invocation End-to-End

Send a prompt that triggers tool usage and verify the tool executes and its result is incorporated.

```java
String response = assistant.chat("What is the weather in Rome?");
System.out.println(response);
```

**Validate**: Check logs for tool invocation and confirm the response uses the tool output.

### 4. Handle Tool Execution Errors

Add error handlers to gracefully manage failures without exposing stack traces.

```java
AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .tools(new ExternalServiceTools())
    .toolExecutionErrorHandler((request, exception) -> {
        logger.error("Tool '{}' failed: {}", request.name(), exception.getMessage());
        return "An error occurred while processing your request";
    })
    .hallucinatedToolNameStrategy(request ->
        ToolExecutionResultMessage.from(request,
            "Error: tool '" + request.name() + "' does not exist"))
    .toolArgumentsErrorHandler((error, context) ->
        ToolErrorHandlerResult.text("Invalid arguments: " + error.getMessage()))
    .build();
```

**Validate**: Trigger an error condition and confirm the LLM receives a safe error message.

### 5. Optimize for Performance and Scale

Enable concurrent tool execution and set timeouts for long-running tools.

```java
AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .tools(new DbTools(), new HttpTools())
    .executeToolsConcurrently(Executors.newFixedThreadPool(5))
    .toolExecutionTimeout(Duration.ofSeconds(30))
    .build();
```

**Validate**: Run concurrent requests and confirm no thread contention or deadlocks.

## Examples

### Calculator Tool with Full Class

```java
public class Calculator {
    @Tool("Perform basic arithmetic")
    public double calculate(
            @P("Expression like 2+2 or 10*5") String expression) {
        // Parse and evaluate expression
        return eval(expression);
    }
}

Assistant assistant = AiServices.builder(Assistant.class)
    .chatModel(ChatModel.builder()
        .apiKey(System.getenv("API_KEY"))
        .model("gpt-4o")
        .build())
    .tools(new Calculator())
    .build();
```

### Immediate Return Tool (No LLM Response)

```java
@Tool(value = "Send email notification", returnBehavior = ReturnBehavior.IMMEDIATELY)
public void sendEmail(@P("Recipient email address") String to,
                     @P("Email subject") String subject,
                     @P("Email body") String body) {
    emailService.send(to, subject, body);
}
```

### Dynamic Tool Provider

```java
ToolProvider provider = request -> {
    if (request.userContext().contains("admin")) {
        return List.of(new AdminTools());
    }
    return List.of(new UserTools());
};

AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .toolProvider(provider)
    .build();
```

## Best Practices

- **Descriptive `@Tool` names**: Use imperative verbs ("Get", "Send", "Calculate") with clear scope
- **Precise `@P` descriptions**: Include format, constraints, and valid values — vague descriptions cause incorrect LLM calls
- **Safe error handling**: Never expose stack traces; return user-friendly error strings
- **Timeout configuration**: Always set `.toolExecutionTimeout()` for external service calls
- **Concurrent execution**: Enable `.executeToolsConcurrently()` when tools are independent
- **Input validation**: Validate parameters inside the tool method; return descriptive errors
- **Permission checks**: Perform authorization inside the tool, not at the AI service level
- **Audit logging**: Log tool name, parameters, and execution result for debugging and compliance

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| LLM calls non-existent tool | Add `.hallucinatedToolNameStrategy()` returning a safe error message |
| Tools receive wrong parameters | Refine `@P` descriptions; add `.toolArgumentsErrorHandler()` |
| Tool execution hangs | Set `.toolExecutionTimeout(Duration.ofSeconds(N))` |
| Rate limit errors from external API | Add retry logic or rate limiter inside the tool method |
| LLM ignores tool output | Ensure the tool returns a string the LLM can interpret |

See [references/error-handling.md](references/error-handling.md) for resilience patterns and [references/core-patterns.md](references/core-patterns.md) for parameter and return type details.

## Quick Reference

| Annotation / API | Purpose |
|-----------------|---------|
| `@Tool` | Marks a method as a callable tool |
| `@P` | Describes a tool parameter for the LLM |
| `@ToolMemoryId` | Injects conversation/user ID into the tool |
| `AiServices.builder()` | Creates AI service with registered tools |
| `ReturnBehavior.IMMEDIATELY` | Execute tool without waiting for LLM response |
| `ToolProvider` | Dynamic tool provisioning based on context |
| `executeToolsConcurrently()` | Run independent tool calls in parallel |
| `toolExecutionTimeout()` | Timeout for individual tool calls |

## Constraints and Warnings

- **Sensitive data**: Never pass API keys, passwords, or credentials in `@Tool` or `@P` descriptions
- **Side effects**: Tools that modify data should warn in their description; AI models may call them multiple times
- **Large tool sets**: Excessive tools confuse LLM models — use `ToolProvider` for conditional registration
- **Blocking operations**: Tools should not perform long synchronous I/O without timeout configuration
- **Stack trace exposure**: Always route exceptions through error handlers that return safe strings
- **Parameter precision**: Vague `@P` descriptions directly cause incorrect tool calls — be specific about formats and constraints
- **Concurrent safety**: Ensure tool classes are stateless or thread-safe when using `executeToolsConcurrently()`

## Related Skills

- `langchain4j-ai-services-patterns` — High-level AI service configuration
- `langchain4j-rag-implementation-patterns` — RAG retrieval with tool integration
- `langchain4j-spring-boot-integration` — Tool registration in Spring Boot applications

## References

- **[references/setup-configuration.md](references/setup-configuration.md)** — Maven setup, chat model configuration, first tool registration
- **[references/core-patterns.md](references/core-patterns.md)** — Basic tool definition, complex parameters, return types
- **[references/advanced-features.md](references/advanced-features.md)** — Memory context, dynamic tool providers, streaming, immediate return
- **[references/error-handling.md](references/error-handling.md)** — Error handlers, retry logic, monitoring
- **[references/integration-examples.md](references/integration-examples.md)** — Database, REST API, and context-aware tool examples
