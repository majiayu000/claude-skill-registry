---
name: langchain4j-testing-strategies
description: Testing strategies for LangChain4j-powered applications. Mock LLM responses, test retrieval chains, and validate AI workflows. Use when testing AI-powered features reliably.
category: backend
tags: [langchain4j, testing, unit-tests, integration-tests, testcontainers, java, ai, llm, mock]
version: 1.1.0
allowed-tools: Read, Write, Bash
---

# LangChain4J Testing Strategies

## When to Use This Skill

Use this skill when:
- Building AI-powered applications with LangChain4J
- Writing unit tests for AI services and guardrails
- Setting up integration tests with real LLM models
- Creating mock-based tests for faster test execution
- Using Testcontainers for isolated testing environments
- Testing RAG (Retrieval-Augmented Generation) systems
- Validating tool execution and function calling
- Testing streaming responses and async operations
- Setting up end-to-end tests for AI workflows
- Implementing performance and load testing

## Instructions

To test LangChain4J applications effectively, follow these key strategies:

### 1. Start with Unit Testing

Use mock models for fast, isolated testing of business logic. See `references/unit-testing.md` for detailed examples.

```java
// Example: Mock ChatModel for unit tests
ChatModel mockModel = mock(ChatModel.class);
when(mockModel.generate(any(String.class)))
    .thenReturn(Response.from(AiMessage.from("Mocked response")));

var service = AiServices.builder(AiService.class)
        .chatModel(mockModel)
        .build();
```

### 2. Configure Testing Dependencies

Setup proper Maven/Gradle dependencies for testing. See `references/testing-dependencies.md` for complete configuration.

**Key dependencies**:
- `langchain4j-test` - Testing utilities and guardrail assertions
- `testcontainers` - Integration testing with containerized services
- `mockito` - Mock external dependencies
- `assertj` - Better assertions

### 3. Implement Integration Tests

Test with real services using Testcontainers. See `references/integration-testing.md` for container setup examples.

```java
@Testcontainers
class OllamaIntegrationTest {
    @Container
    static GenericContainer<?> ollama = new GenericContainer<>(
        DockerImageName.parse("ollama/ollama:latest")
    ).withExposedPorts(11434);

    @Test
    void shouldGenerateResponse() {
        ChatModel model = OllamaChatModel.builder()
                .baseUrl(ollama.getEndpoint())
                .build();
        String response = model.generate("Test query");
        assertNotNull(response);
    }
}
```

### 4. Test Advanced Features

For streaming responses, memory management, and complex workflows, refer to `references/advanced-testing.md`.

### 5. Apply Testing Workflows

Follow testing pyramid patterns and best practices from `references/workflow-patterns.md`.

- **70% Unit Tests**: Fast, isolated business logic testing
- **20% Integration Tests**: Real service interactions
- **10% End-to-End Tests**: Complete user workflows

## Examples

### Basic Unit Test

```java
@Test
void shouldProcessQueryWithMock() {
    ChatModel mockModel = mock(ChatModel.class);
    when(mockModel.generate(any(String.class)))
        .thenReturn(Response.from(AiMessage.from("Test response")));

    var service = AiServices.builder(AiService.class)
            .chatModel(mockModel)
            .build();

    String result = service.chat("What is Java?");
    assertEquals("Test response", result);
}
```

### Integration Test with Testcontainers

```java
@Testcontainers
class RAGIntegrationTest {
    @Container
    static GenericContainer<?> ollama = new GenericContainer<>(
        DockerImageName.parse("ollama/ollama:latest")
    );

    @Test
    void shouldCompleteRAGWorkflow() {
        // Setup models and stores
        var chatModel = OllamaChatModel.builder()
                .baseUrl(ollama.getEndpoint())
                .build();

        var embeddingModel = OllamaEmbeddingModel.builder()
                .baseUrl(ollama.getEndpoint())
                .build();

        var store = new InMemoryEmbeddingStore<>();
        var retriever = EmbeddingStoreContentRetriever.builder()
                .chatModel(chatModel)
                .embeddingStore(store)
                .embeddingModel(embeddingModel)
                .build();

        // Test complete workflow
        var assistant = AiServices.builder(RagAssistant.class)
                .chatLanguageModel(chatModel)
                .contentRetriever(retriever)
                .build();

        String response = assistant.chat("What is Spring Boot?");
        assertNotNull(response);
        assertTrue(response.contains("Spring"));
    }
}
```

## Best Practices

### Test Isolation
- Each test must be independent
- Use `@BeforeEach` and `@AfterEach` for setup/teardown
- Avoid sharing state between tests

### Mock External Dependencies
- Never call real APIs in unit tests
- Use mocks for ChatModel, EmbeddingModel, and external services
- Test error handling scenarios

### Performance Considerations
- Unit tests should run in < 50ms
- Integration tests should use container reuse
- Include timeout assertions for slow operations

### Quality Assertions
- Test both success and error scenarios
- Validate response coherence and relevance
- Include edge case testing (empty inputs, large payloads)

## Reference Documentation

For comprehensive testing guides and API references, see the included reference documents:

- **[Testing Dependencies](references/testing-dependencies.md)** - Maven/Gradle configuration and setup
- **[Unit Testing](references/unit-testing.md)** - Mock models, guardrails, and individual components
- **[Integration Testing](references/integration-testing.md)** - Testcontainers and real service testing
- **[Advanced Testing](references/advanced-testing.md)** - Streaming, memory, and error handling
- **[Workflow Patterns](references/workflow-patterns.md)** - Test pyramid and best practices

## Common Patterns

### Mock Strategy
```java
// For fast unit tests
ChatModel mockModel = mock(ChatModel.class);
when(mockModel.generate(anyString())).thenReturn(Response.from(AiMessage.from("Mocked")));

// For specific responses
when(mockModel.generate(eq("Hello"))).thenReturn(Response.from(AiMessage.from("Hi")));
when(mockModel.generate(contains("Java"))).thenReturn(Response.from(AiMessage.from("Java response")));
```

### Test Configuration
```java
// Use test-specific profiles
@TestPropertySource(properties = {
    "langchain4j.ollama.base-url=http://localhost:11434"
})
class TestConfig {
    // Test with isolated configuration
}
```

### Assertion Helpers
```java
// Custom assertions for AI responses
assertThat(response).isNotNull().isNotEmpty();
assertThat(response).containsAll(expectedKeywords);
assertThat(response).doesNotContain("error");
```

## Performance Requirements

- **Unit Tests**: < 50ms per test
- **Integration Tests**: Use container reuse for faster startup
- **Timeout Tests**: Include `@Timeout` for external service calls
- **Memory Management**: Test conversation window limits and cleanup

## Security Considerations

- Never use real API keys in tests
- Mock external API calls completely
- Test prompt injection detection
- Validate output sanitization

## Testing Pyramid Implementation

```
70% Unit Tests
  ├─ Business logic validation
  ├─ Guardrail testing
  ├─ Mock tool execution
  └─ Edge case handling

20% Integration Tests
  ├─ Testcontainers with Ollama
  ├─ Vector store testing
  ├─ RAG workflow validation
  └─ Performance benchmarking

10% End-to-End Tests
  ├─ Complete user journeys
  ├─ Real model interactions
  └─ Performance under load
```

## Related Skills

- `spring-boot-test-patterns`
- `unit-test-service-layer`
- `unit-test-boundary-conditions`

## References
- [Testing Dependencies](references/testing-dependencies.md)
- [Unit Testing](references/unit-testing.md)
- [Integration Testing](references/integration-testing.md)
- [Advanced Testing](references/advanced-testing.md)
- [Workflow Patterns](references/workflow-patterns.md)