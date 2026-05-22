---
name: langchain4j-ai-services-patterns
description: Build declarative AI Services with LangChain4j using interface-based patterns, annotations, memory management, tools integration, and advanced application patterns. Use when implementing type-safe AI-powered features with minimal boilerplate code in Java applications.
category: ai-development
tags: [langchain4j, ai-services, annotations, declarative, tools, memory, function-calling, llm, java]
version: 1.1.0
allowed-tools: Read, Write, Bash
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