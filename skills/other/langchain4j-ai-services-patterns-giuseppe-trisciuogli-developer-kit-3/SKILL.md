---
name: langchain4j-ai-services-patterns
description: Provides patterns to build declarative AI Services with LangChain4j using interface-based patterns, annotations, memory management, tools integration, and advanced application patterns. Use when implementing type-safe AI-powered features with minimal boilerplate code in Java applications.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# LangChain4j AI Services Patterns

This skill provides guidance for building declarative AI Services with LangChain4j using interface-based patterns, annotations for system and user messages, memory management, tools integration, and advanced AI application patterns that abstract away low-level LLM interactions.

## When to Use

Use this skill when:
- Building declarative AI-powered interfaces with minimal boilerplate code
- Creating type-safe AI services with Java interfaces and annotations
- Implementing conversational AI systems with memory management
- Designing AI services that can call external tools and functions
- Building multi-agent systems with specialized AI components
- Creating AI services with different personas and behaviors
- Implementing RAG (Retrieval-Augmented Generation) patterns declaratively
- Building production AI applications with proper error handling and validation
- Creating AI services that return structured data types (enums, POJOs, lists)
- Implementing streaming AI responses with reactive patterns

## Overview

LangChain4j AI Services allow you to define AI-powered functionality using plain Java interfaces with annotations, eliminating the need for manual prompt construction and response parsing. This pattern provides type-safe, declarative AI capabilities with minimal boilerplate code.

## Instructions

Follow these steps to create declarative AI Services with LangChain4j:

### 1. Define AI Service Interface

Create a Java interface with method signatures for AI interactions:

```java
public interface Assistant {
    String chat(String userMessage);
}
```

### 2. Add Annotations for Messages

Use `@SystemMessage` and `@UserMessage` annotations to define prompts:

```java
public interface CustomerSupportBot {
    @SystemMessage("You are a helpful customer support agent for TechCorp")
    String handleInquiry(String customerMessage);

    @UserMessage("Analyze sentiment: {{it}}")
    Sentiment analyzeSentiment(String feedback);
}
```

### 3. Create AI Service Instance

Use `AiServices` builder to create implementation:

```java
Assistant assistant = AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .build();
```

### 4. Configure Memory for Conversations

Add memory management for multi-turn conversations:

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

Register tools to enable AI to execute external functions:

```java
class Calculator {
    @Tool("Add two numbers") double add(double a, double b) { return a + b; }
}

MathGenius mathGenius = AiServices.builder(MathGenius.class)
    .chatModel(model)
    .tools(new Calculator())
    .build();
```

## Quick Start

### Basic AI Service Definition

```java
interface Assistant {
    String chat(String userMessage);
}

// Create instance - LangChain4j generates implementation
Assistant assistant = AiServices.create(Assistant.class, chatModel);

// Use the service
String response = assistant.chat("Hello, how are you?");
```

### System Message and Templates

```java
interface CustomerSupportBot {
    @SystemMessage("You are a helpful customer support agent for TechCorp")
    String handleInquiry(String customerMessage);

    @UserMessage("Analyze sentiment: {{it}}")
    String analyzeSentiment(String feedback);
}

CustomerSupportBot bot = AiServices.create(CustomerSupportBot.class, chatModel);
```

### Memory Management

```java
interface MultiUserAssistant {
    String chat(@MemoryId String userId, String userMessage);
}

Assistant assistant = AiServices.builder(MultiUserAssistant.class)
    .chatModel(model)
    .chatMemoryProvider(userId -> MessageWindowChatMemory.withMaxMessages(10))
    .build();
```

### Tool Integration

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