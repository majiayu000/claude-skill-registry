---
name: langchain4j-spring-boot-integration
description: Provides integration patterns for LangChain4j with Spring Boot. Configures AI model beans, sets up chat memory with Spring context, integrates RAG pipelines with Spring Data, and handles auto-configuration, dependency injection, and Spring ecosystem integration. Use when embedding LangChain4j into Spring Boot applications, building Java LLM applications with @Bean configuration, or setting up Spring AI patterns.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# LangChain4j Spring Boot Integration

Integrate LangChain4j with Spring Boot using declarative AI Services, auto-configuration, and Spring Boot starters. Configure AI model beans, set up chat memory, implement RAG pipelines with Spring Data, and build production-ready AI applications.

## When to Use

Use this skill when:
- Integrating LangChain4j into existing Spring Boot applications
- Building AI-powered microservices with Spring Boot
- Configuring AI model beans with `@Bean` annotations
- Setting up auto-configuration for AI models and services
- Creating declarative AI Services with Spring dependency injection
- Implementing RAG systems with Spring Data integrations
- Setting up chat memory with Spring context management
- Configuring multiple AI providers (OpenAI, Azure, Ollama, Anthropic)
- Building production-ready AI applications with Spring Boot

## Overview

LangChain4j Spring Boot integration provides declarative AI Services through Spring Boot starters, enabling automatic configuration of AI components based on properties. Combine Spring dependency injection with LangChain4j's AI capabilities using interface-based definitions with annotations.

## Instructions

### 1. Add Dependencies

```xml
<!-- Core LangChain4j Spring Boot Starter -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-spring-boot-starter</artifactId>
    <version>1.8.0</version>
</dependency>

<!-- OpenAI Spring Boot Starter -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai-spring-boot-starter</artifactId>
    <version>1.8.0</version>
</dependency>
```

### 2. Configure Application Properties

```properties
# application.properties
langchain4j.open-ai.chat-model.api-key=${OPENAI_API_KEY}
langchain4j.open-ai.chat-model.model-name=gpt-4o-mini
langchain4j.open-ai.chat-model.temperature=0.7
langchain4j.open-ai.chat-model.timeout=PT60S
langchain4j.open-ai.chat-model.max-tokens=1000
```

Or using YAML:

```yaml
langchain4j:
  open-ai:
    chat-model:
      api-key: ${OPENAI_API_KEY}
      model-name: gpt-4o-mini
      temperature: 0.7
      timeout: 60s
      max-tokens: 1000
```

### 3. Create Declarative AI Service

```java
import dev.langchain4j.service.spring.AiService;

@AiService
public interface CustomerSupportAssistant {

    @SystemMessage("You are a helpful customer support agent for TechCorp.")
    String handleInquiry(String customerMessage);

    @UserMessage("Translate to {{language}}: {{text}}")
    String translate(String text, String language);
}
```

### 4. Enable Component Scanning

```java
@SpringBootApplication
@ComponentScan(basePackages = {
    "com.yourcompany",
    "dev.langchain4j.service.spring"
})
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 5. Inject and Use the AI Service

```java
@Service
public class CustomerService {

    private final CustomerSupportAssistant assistant;

    public CustomerService(CustomerSupportAssistant assistant) {
        this.assistant = assistant;
    }

    public String processCustomerQuery(String query) {
        return assistant.handleInquiry(query);
    }
}
```

### 6. Verify the Integration

After setup, verify the configuration:
1. Start the application and check logs for `LangChain4jSpringBootAutoConfiguration` activation
2. Confirm AI service beans are registered: look for `CustomerSupportAssistant` in Spring context
3. Test the service: invoke `assistant.handleInquiry("test")` and verify a response is returned

## Configuration

**Property-Based Configuration:** Configure AI models through `application.properties` for different providers.

**Manual Bean Configuration:** For advanced configurations, define beans manually:

```java
@Configuration
public class AiConfig {

    @Bean
    public ChatModel chatModel(@Value("${OPENAI_API_KEY}") String apiKey) {
        return OpenAiChatModel.builder()
            .apiKey(apiKey)
            .modelName("gpt-4o-mini")
            .temperature(0.7)
            .build();
    }
}
```

**Multiple Providers:** Use explicit wiring when configuring multiple AI providers:

```java
@AiService(wiringMode = WiringMode.EXPLICIT)
interface MultiProviderAssistant {
    @AiServiceAnnotation
    ChatModel openAiModel;

    @AiServiceAnnotation
    ChatModel azureModel;
}
```

## Declarative AI Services

**Basic AI Service:** Create interfaces with `@AiService` annotation and define methods with message templates.

**Streaming AI Service:** Implement streaming responses using Project Reactor:

```java
@AiService
public interface StreamingAssistant {
    @SystemMessage("You are a helpful assistant.")
    Flux<String> chatStream(String message);
}
```

**Chat Memory:** Set up conversation memory with Spring context:

```java
@AiService
public interface ConversationalAssistant {
    @SystemMessage("You are a helpful assistant with memory.")
    String chat(@MemoryId String userId, String message);
}
```

## RAG Implementation

**Embedding Stores:** Configure embedding stores for RAG pipelines with Spring Data:

```java
@Configuration
public class RagConfig {

    @Bean
    public EmbeddingStore<TextSegment> embeddingStore() {
        return PgVectorEmbeddingStore.builder()
            .host("localhost")
            .port(5432)
            .database("vectordb")
            .table("embeddings")
            .dimension(1536)
            .build();
    }

    @Bean
    public EmbeddingModel embeddingModel() {
        return OpenAiEmbeddingModel.withApiKey(System.getenv("OPENAI_API_KEY"));
    }
}

@AiService
public interface RagAssistant {
    String answer(@UserMessage("Question: {{question}}") String question);
}
```

**Document Ingestion:** Use `ContentInjector` and `DocumentSplitter` for processing documents.
**Content Retrieval:** Configure `EmbeddingStoreContentRetriever` for knowledge augmentation.

## Tool Integration

**Spring Component Tools:** Define tools as Spring components:

```java
@Component
public class Calculator {
    @Tool("Calculate the sum of two numbers")
    public double add(double a, double b) {
        return a + b;
    }
}

@AiService
public interface MathAssistant {
    String solve(String problem);
}
```

## Examples

### Basic AI Service

```java
@AiService
public interface ChatAssistant {
    @SystemMessage("You are a helpful assistant.")
    String chat(String message);
}
```

### AI Service with Memory

```java
@AiService
public interface ConversationalAssistant {
    @SystemMessage("You are a helpful assistant with memory of conversations.")
    String chat(@MemoryId String userId, String message);
}
```

### AI Service with Tools

```java
@Component
public class WeatherService {
    @Tool("Get weather for a city")
    public String getWeather(String city) {
        return "Sunny, 22°C in " + city;
    }
}

@AiService
public interface WeatherAssistant {
    String getWeatherForCity(String city);
}
```

For more examples (including RAG configurations, streaming assistants, and multi-provider setups), refer to [references/examples.md](references/examples.md).

## Best Practices

- **Use Property-Based Configuration:** External configuration over hardcoded values
- **Use Profiles:** Separate configurations for development, testing, and production
- **Add Proper Logging:** Debug AI service calls and monitor performance
- **Implement Retry Mechanisms:** Handle transient failures with backoff strategies
- **Monitor Token Usage:** Track token consumption and implement limits

## References

For detailed API references and advanced configurations:
- [API Reference](references/references.md) - Complete API documentation
- [Examples](references/examples.md) - Comprehensive implementation examples
- [Configuration Guide](references/configuration.md) - Deep dive into configuration options

## Constraints and Warnings

- Store API keys securely using environment variables or secret management systems
- AI model responses are non-deterministic; tests should account for variability
- Rate limits may apply to AI providers; implement proper retry and backoff strategies
- Memory providers store conversation history; implement cleanup for multi-user scenarios
- Token costs accumulate quickly; monitor usage and implement token limits
- Streaming responses require proper error handling for partial failures
- Check provider-specific documentation for supported features
- Use explicit wiring mode when multiple chat models are configured
- Validate AI-generated outputs before use in production systems
