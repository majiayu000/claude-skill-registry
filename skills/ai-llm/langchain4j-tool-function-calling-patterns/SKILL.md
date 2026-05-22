---
name: langchain4j-tool-function-calling-patterns
description: Tool and function calling patterns with LangChain4j. Define tools, handle function calls, and integrate with LLM agents. Use when building agentic applications that interact with tools.
category: ai-development
tags: [langchain4j, tools, function-calling, "@Tool", ToolProvider, ToolExecutor, dynamic-tools, parameter-descriptions, java]
version: 1.1.0
allowed-tools: Read, Write, Bash, WebFetch
---

# LangChain4j Tool & Function Calling Patterns

Define tools and enable AI agents to interact with external systems, APIs, and services using LangChain4j's annotation-based and programmatic tool system.

## When to Use This Skill

Use this skill when:
- Building AI applications that need to interact with external APIs and services
- Creating AI assistants that can perform actions beyond text generation
- Implementing AI systems that need access to real-time data (weather, stocks, etc.)
- Building multi-agent systems where agents can use specialized tools
- Creating AI applications with database read/write capabilities
- Implementing AI systems that need to integrate with existing business systems
- Building context-aware AI applications where tool availability depends on user state
- Developing production AI applications that require robust error handling and monitoring

## Setup and Configuration

### Basic Tool Registration

```java
// Define tools using @Tool annotation
public class CalculatorTools {
    @Tool("Add two numbers")
    public double add(double a, double b) {
        return a + b;
    }
}

// Register with AiServices builder
interface MathAssistant {
    String ask(String question);
}

MathAssistant assistant = AiServices.builder(MathAssistant.class)
    .chatModel(chatModel)
    .tools(new CalculatorTools())
    .build();
```

### Builder Configuration Options

```java
AiServices.builder(AssistantInterface.class)

    // Static tool registration
    .tools(new Calculator(), new WeatherService())

    // Dynamic tool provider
    .toolProvider(new DynamicToolProvider())

    // Concurrent execution
    .executeToolsConcurrently()

    // Error handling
    .toolExecutionErrorHandler((request, exception) -> {
        return "Error: " + exception.getMessage();
    })

    // Memory for context
    .chatMemoryProvider(userId -> MessageWindowChatMemory.withMaxMessages(20))

    .build();
```

## Core Patterns

### Basic Tool Definition

Use `@Tool` annotation to define methods as executable tools:

```java
public class BasicTools {

    @Tool("Add two numbers")
    public int add(@P("first number") int a, @P("second number") int b) {
        return a + b;
    }

    @Tool("Get greeting")
    public String greet(@P("name to greet") String name) {
        return "Hello, " + name + "!";
    }
}
```

### Parameter Descriptions and Validation

Provide clear parameter descriptions using `@P` annotation:

```java
public class WeatherService {

    @Tool("Get current weather conditions")
    public String getCurrentWeather(
        @P("City name or coordinates") String location,
        @P("Temperature unit (celsius, fahrenheit)", required = false) String unit) {

        // Implementation with validation
        if (location == null || location.trim().isEmpty()) {
            return "Location is required";
        }

        return weatherClient.getCurrentWeather(location, unit);
    }
}
```

### Complex Parameter Types

Use Java records and descriptions for complex objects:

```java
public class OrderService {

    @Description("Customer order information")
    public record OrderRequest(
        @Description("Customer ID") String customerId,
        @Description("List of items") List<OrderItem> items,
        @JsonProperty(required = false) @Description("Delivery instructions") String instructions
    ) {}

    @Tool("Create customer order")
    public String createOrder(OrderRequest order) {
        return orderService.processOrder(order);
    }
}
```

## Advanced Features

### Memory Context Integration

Access user context using `@ToolMemoryId`:

```java
public class PersonalizedTools {

    @Tool("Get user preferences")
    public String getPreferences(
        @ToolMemoryId String userId,
        @P("Preference category") String category) {

        return preferenceService.getPreferences(userId, category);
    }
}
```

### Dynamic Tool Provisioning

Create tools that change based on context:

```java
public class ContextAwareToolProvider implements ToolProvider {

    @Override
    public ToolProviderResult provideTools(ToolProviderRequest request) {
        String message = request.userMessage().singleText().toLowerCase();
        var builder = ToolProviderResult.builder();

        if (message.contains("weather")) {
            builder.add(weatherToolSpec, weatherExecutor);
        }

        if (message.contains("calculate")) {
            builder.add(calcToolSpec, calcExecutor);
        }

        return builder.build();
    }
}
```

### Immediate Return Tools

Return results immediately without full AI response:

```java
public class QuickTools {

    @Tool(value = "Get current time", returnBehavior = ReturnBehavior.IMMEDIATE)
    public String getCurrentTime() {
        return LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
    }
}
```

## Error Handling

### Tool Error Handling

Handle tool execution errors gracefully:

```java
AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .tools(new ExternalServiceTools())
    .toolExecutionErrorHandler((request, exception) -> {
        if (exception instanceof ApiException) {
            return "Service temporarily unavailable: " + exception.getMessage();
        }
        return "An error occurred while processing your request";
    })
    .build();
```

### Resilience Patterns

Implement circuit breakers and retries:

```java
public class ResilientService {

    private final CircuitBreaker circuitBreaker = CircuitBreaker.ofDefaults("external-api");

    @Tool("Get external data")
    public String getExternalData(@P("Data identifier") String id) {
        return circuitBreaker.executeSupplier(() -> {
            return externalApi.getData(id);
        });
    }
}
```

## Integration Examples

### Multi-Domain Tool Service

```java
@Service
public class MultiDomainToolService {

    public String processRequest(String userId, String request, String domain) {
        String contextualRequest = String.format("[Domain: %s] %s", domain, request);

        Result<String> result = assistant.chat(userId, contextualRequest);

        // Log tool usage
        result.toolExecutions().forEach(execution ->
            analyticsService.recordToolUsage(userId, domain, execution.request().name()));

        return result.content();
    }
}
```

### Streaming with Tool Execution

```java
interface StreamingAssistant {
    TokenStream chat(String message);
}

StreamingAssistant assistant = AiServices.builder(StreamingAssistant.class)
    .streamingChatModel(streamingChatModel)
    .tools(new Tools())
    .build();

TokenStream stream = assistant.chat("What's the weather and calculate 15*8?");

stream
    .onToolExecuted(execution ->
        System.out.println("Executed: " + execution.request().name()))
    .onPartialResponse(System.out::print)
    .onComplete(response -> System.out.println("Complete!"))
    .start();
```

## Best Practices

### Tool Design Guidelines

1. **Descriptive Names**: Use clear, actionable tool names
2. **Parameter Validation**: Validate inputs before processing
3. **Error Messages**: Provide meaningful error messages
4. **Return Types**: Use appropriate return types that LLMs can understand
5. **Performance**: Avoid blocking operations in tools

### Security Considerations

1. **Permission Checks**: Validate user permissions before tool execution
2. **Input Sanitization**: Sanitize all tool inputs
3. **Audit Logging**: Log tool usage for security monitoring
4. **Rate Limiting**: Implement rate limiting for external APIs

### Performance Optimization

1. **Concurrent Execution**: Use `executeToolsConcurrently()` for independent tools
2. **Caching**: Cache frequently accessed data
3. **Monitoring**: Monitor tool performance and error rates
4. **Resource Management**: Handle external service timeouts gracefully

## Reference Documentation

For detailed API reference, examples, and advanced patterns, see:

- [API Reference](./references/references.md) - Complete API documentation
- [Implementation Patterns](./references/implementation-patterns.md) - Advanced implementation examples
- [Examples](./references/examples.md) - Practical usage examples

## Common Issues and Solutions

### Tool Not Found

**Problem**: LLM calls tools that don't exist

**Solution**: Implement hallucination handler:

```java
.hallucinatedToolNameStrategy(request -> {
    return ToolExecutionResultMessage.from(request,
        "Error: Tool '" + request.name() + "' does not exist");
})
```

### Parameter Validation Errors

**Problem**: Tools receive invalid parameters

**Solution**: Add input validation and error handlers:

```java
.toolArgumentsErrorHandler((error, context) -> {
    return ToolErrorHandlerResult.text("Invalid arguments: " + error.getMessage());
})
```

### Performance Issues

**Problem**: Tools are slow or timeout

**Solution**: Use concurrent execution and resilience patterns:

```java
.executeToolsConcurrently(Executors.newFixedThreadPool(5))
.toolExecutionTimeout(Duration.ofSeconds(30))
```

## Related Skills

- `langchain4j-ai-services-patterns`
- `langchain4j-rag-implementation-patterns`
- `langchain4j-spring-boot-integration`

## References

- [LangChain4j Tool & Function Calling - API References](./references/references.md)
- [LangChain4j Tool & Function Calling - Implementation Patterns](./references/implementation-patterns.md)
- [LangChain4j Tool & Function Calling - Examples](./references/examples.md)
