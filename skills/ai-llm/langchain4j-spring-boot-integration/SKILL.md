---
name: langchain4j-spring-boot-integration
description: Integration patterns for LangChain4j with Spring Boot. Auto-configuration, dependency injection, and Spring ecosystem integration. Use when embedding LangChain4j into Spring Boot applications.
category: ai-development
tags: [langchain4j, spring-boot, ai, llm, rag, chatbot, integration, configuration, java]
version: 1.1.0
allowed-tools: Read, Write, Bash, Grep
---

# LangChain4j Spring Boot Integration

To accomplish integration of LangChain4j with Spring Boot applications, follow this comprehensive guidance covering auto-configuration, declarative AI Services, chat models, embedding stores, and production-ready patterns for building AI-powered applications.

## When to Use

To accomplish integration of LangChain4j with Spring Boot when:
- Integrating LangChain4j into existing Spring Boot applications
- Building AI-powered microservices with Spring Boot
- Setting up auto-configuration for AI models and services
- Creating declarative AI Services with Spring dependency injection
- Configuring multiple AI providers (OpenAI, Azure, Ollama, etc.)
- Implementing RAG systems with Spring Boot
- Setting up observability and monitoring for AI components
- Building production-ready AI applications with Spring Boot

## Overview

LangChain4j Spring Boot integration provides declarative AI Services through Spring Boot starters, enabling automatic configuration of AI components based on properties. The integration combines the power of Spring dependency injection with LangChain4j's AI capabilities, allowing developers to create AI-powered applications using interface-based definitions with annotations.

## Core Concepts

To accomplish basic setup of LangChain4j with Spring Boot:

**Add Dependencies:**
```xml
<!-- Core LangChain4j -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-spring-boot-starter</artifactId>
    <version>1.8.0</version> // Use latest version
</dependency>

<!-- OpenAI Integration -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai-spring-boot-starter</artifactId>
    <version>1.8.0</version>
</dependency>
```

**Configure Properties:**
```properties
# application.properties
langchain4j.open-ai.chat-model.api-key=${OPENAI_API_KEY}
langchain4j.open-ai.chat-model.model-name=gpt-4o-mini
langchain4j.open-ai.chat-model.temperature=0.7
```

**Create Declarative AI Service:**
```java
@AiService
interface CustomerSupportAssistant {
    @SystemMessage("You are a helpful customer support agent for TechCorp.")
    String handleInquiry(String customerMessage);
}
```

## Configuration

To accomplish Spring Boot configuration for LangChain4j:

**Property-Based Configuration:** Configure AI models through application properties for different providers.

**Manual Bean Configuration:** For advanced configurations, define beans manually using @Configuration.

**Multiple Providers:** Support for multiple AI providers with explicit wiring when needed.

## Declarative AI Services

To accomplish interface-based AI service definitions:

**Basic AI Service:** Create interfaces with @AiService annotation and define methods with message templates.

**Streaming AI Service:** Implement streaming responses using Reactor or Project Reactor.

**Explicit Wiring:** Specify which model to use with @AiService(wiringMode = EXPLICIT, chatModel = "modelBeanName").

## RAG Implementation

To accomplish RAG system implementation:

**Embedding Stores:** Configure various embedding stores (PostgreSQL/pgvector, Neo4j, Pinecone, etc.).

**Document Ingestion:** Implement document processing and embedding generation.

**Content Retrieval:** Set up content retrieval mechanisms for knowledge augmentation.

## Tool Integration

To accomplish AI tool integration:

**Spring Component Tools:** Define tools as Spring components with @Tool annotations.

**Database Access Tools:** Create tools for database operations and business logic.

**Tool Registration:** Automatically register tools with AI services.

## Examples

To understand implementation patterns, refer to the comprehensive examples in [references/examples.md](references/examples.md).

## Best Practices

To accomplish production-ready AI applications:

- **Use Property-Based Configuration:** External configuration over hardcoded values
- **Implement Proper Error Handling:** Graceful degradation and meaningful error responses
- **Use Profiles for Different Environments:** Separate configurations for development, testing, and production
- **Implement Proper Logging:** Debug AI service calls and monitor performance
- **Secure API Keys:** Use environment variables and never commit to version control
- **Handle Failures:** Implement retry mechanisms and fallback strategies
- **Monitor Performance:** Add metrics and health checks for observability

## References

For detailed API references, advanced configurations, and additional patterns, refer to:

- [API Reference](references/references.md) - Complete API reference and configurations
- [Examples](references/examples.md) - Comprehensive implementation examples
- [Configuration Guide](references/configuration.md) - Deep dive into configuration options
