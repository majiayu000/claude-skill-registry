---
name: langchain4j-ai-services-patterns
description: Provides patterns to build declarative AI Services with LangChain4j for LLM integration, chatbot development, AI agent implementation, and conversational AI in Java. Generates type-safe AI services using interface-based patterns, annotations, memory management, and tools integration. Use when creating AI-powered Java applications with minimal boilerplate, implementing conversational AI with memory, or building AI agents with function calling.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# LangChain4j AI Services Patterns

This skill provides guidance for building declarative AI Services with LangChain4j using interface-based patterns, annotations for system and user messages, memory management, tools integration, and advanced AI application patterns that abstract away low-level LLM interactions.

## Overview

LangChain4j AI Services define AI functionality using Java interfaces with annotations, providing type-safe, declarative AI with minimal boilerplate.

## When to Use

Use this skill when:
- Building declarative AI services with minimal boilerplate using Java interfaces
- Creating type-safe conversational AI with memory management
- Implementing AI agents with function/tool calling capabilities
- Designing AI services returning structured data (enums, POJOs, lists)
- Integrating RAG patterns declaratively

## Instructions

Follow these steps to create declarative AI Services with LangChain4j:

### 1. Define AI Service Interface

Create a Java interface with method signatures for AI interactions:

```java
interface Assistant {
    String chat(String userMessage);
}
```

### 2. Add Annotations for System and User Messages

Use `@SystemMessage` and `@UserMessage` annotations to define prompts:

```java
interface CustomerSupportBot {
    @SystemMessage("You are a helpful customer support agent for TechCorp")
    String handleInquiry(String customerMessage);

    @UserMessage("Analyze sentiment: {{it}}")
    Sentiment analyzeSentiment(String feedback);
}
```

### 3. Create AI Service Instance

Use `AiServices` builder or create to instantiate the service:

```java
// Simple creation
Assistant assistant = AiServices.create(Assistant.class, chatModel);

// Or with builder for advanced configuration
Assistant assistant = AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .build();
```

### 4. Configure Memory for Multi-turn Conversations

Add memory management using `@MemoryId` for multi-user scenarios:

```java
interface MultiUserAssistant {
    String chat(@MemoryId String userId, String userMessage);
}

Assistant assistant = AiServices.builder(MultiUserAssistant.class)
    .chatModel(model)
    .chatMemoryProvider(userId -> MessageWindowChatMemory.withMaxMessages(10))
    .build();
```

### 5. Integrate Tools for Function Calling

Register tools using `@Tool` annotation to enable AI function execution:

```java
class Calculator {
    @Tool("Add two numbers") double add(double a, double b) { return a + b; }
}

interface MathGenius {
    String ask(String question);
}

MathGenius mathGenius = AiServices.builder(MathGenius.class)
    .chatModel(model)
    .tools(new Calculator())
    .build();
```

### 6. Validate and Test

Test AI services with concrete validation patterns:

```java
// 1. Test with sample inputs
String response = assistant.chat("Hello, how are you?");
assert response != null && !response.isEmpty();

// 2. Validate structured outputs with assertions
Sentiment result = bot.analyzeSentiment("Great product!");
assert result == Sentiment.POSITIVE;

// 3. Log tool calls with side effects for audit
MathGenius math = AiServices.builder(MathGenius.class)
    .chatModel(model)
    .tools(new Calculator())
    .build();

// 4. Test memory isolation between users
String userA = assistant.chat("User A message", "session-a");
String userB = assistant.chat("User B message", "session-b");
assert !userA.equals(userB); // Verify memory isolation
```

## Examples

See [examples.md](references/examples.md) for comprehensive practical examples including:
- Basic chat interfaces
- Stateful assistants with memory
- Multi-user scenarios
- Structured output extraction
- Tool calling and function execution
- Streaming responses
- Error handling
- RAG integration
- Production patterns

## API Reference

Complete API documentation, annotations, interfaces, and configuration patterns are available in [references.md](references/references.md).

## Best Practices

1. **Use type-safe interfaces** instead of string-based prompts
2. **Implement proper memory management** with appropriate limits
3. **Design clear tool descriptions** with parameter documentation
4. **Handle errors gracefully** with custom error handlers
5. **Use structured output** for predictable responses
6. **Implement validation** for user inputs
7. **Monitor performance** for production deployments

## Dependencies

```xml
<!-- Maven -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j</artifactId>
    <version>1.8.0</version>
</dependency>
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai</artifactId>
    <version>1.8.0</version>
</dependency>
```

```gradle
// Gradle
implementation 'dev.langchain4j:langchain4j:1.8.0'
implementation 'dev.langchain4j:langchain4j-open-ai:1.8.0'
```

## References

- [LangChain4j Documentation](https://langchain4j.com/docs/)
- [LangChain4j AI Services - API References](references/references.md)
- [LangChain4j AI Services - Practical Examples](references/examples.md)

## Constraints and Warnings

- AI Services rely on LLM responses which are non-deterministic; tests should account for variability.
- Memory providers store conversation history; ensure proper cleanup for multi-user scenarios.
- Tool execution can be expensive; implement rate limiting and timeout handling.
- Never pass sensitive data (API keys, passwords) in system or user messages.
- Large context windows can lead to high token costs; implement message pruning strategies.
- Streaming responses require proper error handling for partial failures.
- AI-generated outputs should be validated before use in production systems.
- Be cautious with tools that have side effects; AI models may call them unexpectedly.
- Token limits vary by model; ensure prompts and context fit within model constraints.