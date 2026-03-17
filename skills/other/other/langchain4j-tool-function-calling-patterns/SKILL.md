---
name: langchain4j-tool-function-calling-patterns
description: Provides tool and function calling patterns with LangChain4j. Handles defining tools, function calls, and LLM agent integration. Use when building agentic applications that interact with tools.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# LangChain4j Tool & Function Calling Patterns

Define tools and enable AI agents to interact with external systems, APIs, and services using LangChain4j's annotation-based and programmatic tool system.

## Overview

LangChain4j's tool system enables AI agents to execute external functions through declarative annotations and programmatic interfaces. Tools are defined using the `@Tool` annotation and automatically registered with AI services, allowing LLMs to perform actions beyond text generation such as database queries, API calls, and calculations.

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

## Instructions

Follow these steps to implement tools with LangChain4j:

### 1. Define Tool Methods

Create methods annotated with `@Tool` in a class:

```java
public class WeatherTools {
    @Tool("Get current weather for a city")
    public String getWeather(
        @P("City name") String city,
        @P("Temperature unit (celsius or fahrenheit)", required = false) String unit) {
        // Implementation
        return weatherService.getWeather(city, unit);
    }
}
```

### 2. Configure Parameter Descriptions

Use `@P` annotation for clear parameter descriptions that help the LLM understand how to call the tool:

```java
@Tool("Calculate total order amount")
public double calculateOrderTotal(
    @P("List of product IDs") List<String> productIds,
    @P("Customer discount percentage", required = false) Double discount) {
    // Implementation
}
```

### 3. Register Tools with AI Service

Connect tools to an AI service using the AiServices builder:

```java
MathAssistant assistant = AiServices.builder(MathAssistant.class)
    .chatModel(chatModel)
    .tools(new Calculator(), new WeatherService())
    .build();
```

### 4. Handle Tool Execution Errors

Implement error handling for tool failures:

```java
AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .tools(new ExternalServiceTools())
    .toolExecutionErrorHandler((request, exception) -> {
        log.error("Tool execution failed: {}", exception.getMessage());
        return "An error occurred while processing your request";
    })
    .build();
```

### 5. Monitor Tool Usage

Track tool calls for debugging and analytics:

```java
Result<String> result = assistant.chat(question);
result.toolExecutions().forEach(execution ->
    log.info("Executed tool: {} in {}ms",
        execution.request().name(),
        execution.duration().toMillis())
);
```

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

## Examples

### Simple Calculator Tool

```java
public class CalculatorTools {

    @Tool("Add two numbers")
    public double add(@P("First number") double a,
                      @P("Second number") double b) {
        return a + b;
    }

    @Tool("Multiply two numbers")
    public double multiply(@P("First number") double a,
                           @P("Second number") double b) {
        return a * b;
    }
}

// Usage
interface MathAssistant {
    String ask(String question);
}

MathAssistant assistant = AiServices.builder(MathAssistant.class)
    .chatModel(chatModel)
    .tools(new CalculatorTools())
    .build();

String result = assistant.ask("What is 15 times 7 plus 3?");
```

### Database Access Tool

```java
@Component
public class DatabaseTools {

    private final CustomerRepository repository;

    @Tool("Get customer information by ID")
    public Customer getCustomer(@P("Customer ID") Long customerId) {
        return repository.findById(customerId)
            .orElseThrow(() -> new IllegalArgumentException("Customer not found"));
    }

    @Tool("Update customer email address")
    public String updateEmail(
        @P("Customer ID") Long customerId,
        @P("New email address") String newEmail) {
        Customer customer = repository.findById(customerId)
            .orElseThrow(() -> new IllegalArgumentException("Customer not found"));
        customer.setEmail(newEmail);
        repository.save(customer);
        return "Email updated successfully";
    }
}
```

### REST API Tool

```java
@Component
public class ApiTools {

    private final WebClient webClient;

    @Tool("Get current stock price")
    public String getStockPrice(@P("Stock symbol") String symbol) {
        return webClient.get()
            .uri("/api/stocks/{symbol}", symbol)
            .retrieve()
            .bodyToMono(String.class)
            .block();
    }
}
```

### Context-Aware Tool with Memory ID

```java
public class UserPreferencesTools {

    @Tool("Get user preferences for a category")
    public String getPreferences(
        @ToolMemoryId String userId,
        @P("Preference category (e.g., theme, language)") String category) {
        return preferencesService.getPreferences(userId, category);
    }

    @Tool("Set user preference")
    public String setPreference(
        @ToolMemoryId String userId,
        @P("Preference category") String category,
        @P("Preference value") String value) {
        preferencesService.setPreference(userId, category, value);
        return "Preference saved";
    }
}
```

### Dynamic Tool Provider

```java
public class DynamicToolProvider implements ToolProvider {

    private final Map<String, Object> availableTools = new HashMap<>();

    public void registerTool(String name, ToolSpecification spec, ToolExecutor executor) {
        availableTools.put(name, new ToolWithSpec(spec, executor));
    }

    @Override
    public ToolProviderResult provideTools(ToolProviderRequest request) {
        var builder = ToolProviderResult.builder();
        String message = request.userMessage().singleText().toLowerCase();

        // Dynamically filter tools based on user message
        if (message.contains("weather")) {
            builder.add(weatherToolSpec, weatherExecutor);
        }
        if (message.contains("calculate") || message.contains("math")) {
            builder.add(calculatorToolSpec, calculatorExecutor);
        }

        return builder.build();
    }
}
```

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

## Constraints and Warnings

- Tools with side effects should have clear descriptions warning about potential impacts.
- AI models may call tools in unexpected orders or with unexpected parameters.
- Tool execution can be expensive; implement rate limiting and timeout handling.
- Never pass sensitive data (API keys, passwords) in tool descriptions or responses.
- Large tool sets can confuse AI models; consider using dynamic tool providers.
- Tool execution errors should be handled gracefully; never expose stack traces to AI models.
- Be cautious with tools that modify data; AI models may call them multiple times.
- Parameter descriptions should be precise; vague descriptions lead to incorrect tool usage.
- Tools with long execution times should implement timeout handling.
- Test tools thoroughly before exposing them to AI models to prevent unexpected behavior.
