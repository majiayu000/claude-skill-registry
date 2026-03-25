---
name: aws-sdk-java-v2-bedrock
description: Provides Amazon Bedrock patterns using AWS SDK for Java 2.x. Invokes foundation models (Claude, Llama, Titan), generates text and images, creates embeddings for RAG, streams real-time responses, and configures Spring Boot integration. Use when asking about Bedrock integration, Java SDK for AI models, AWS generative AI, Claude/Llama invocation, embeddings for RAG, or Spring Boot AI setup.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AWS SDK for Java 2.x - Amazon Bedrock

## Overview

Invokes foundation models through AWS SDK for Java 2.x. Configures clients, builds model-specific JSON payloads, handles streaming responses with error recovery, creates embeddings for RAG, integrates generative AI into Spring Boot applications, and implements exponential backoff for resilience.

## When to Use

- Invoke Claude, Llama, Titan, or Stable Diffusion for text/image generation
- Configure BedrockClient and BedrockRuntimeClient instances
- Build and parse model-specific payloads (Claude, Titan, Llama formats)
- Stream real-time AI responses with async handlers and error recovery
- Create embeddings for retrieval-augmented generation
- Integrate generative AI into Spring Boot microservices
- Handle throttling with exponential backoff retry logic

## Quick Start

### Dependencies

```xml
<!-- Bedrock (model management) -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>bedrock</artifactId>
</dependency>

<!-- Bedrock Runtime (model invocation) -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>bedrockruntime</artifactId>
</dependency>

<!-- For JSON processing -->
<dependency>
    <groupId>org.json</groupId>
    <artifactId>json</artifactId>
    <version>20231013</version>
</dependency>
```

### Client Setup

```java
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrock.BedrockClient;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;

// Model management client
BedrockClient bedrockClient = BedrockClient.builder()
    .region(Region.US_EAST_1)
    .build();

// Model invocation client
BedrockRuntimeClient bedrockRuntimeClient = BedrockRuntimeClient.builder()
    .region(Region.US_EAST_1)
    .build();
```

## Instructions

Follow these steps for production-ready Bedrock integration:

1. **Configure AWS Credentials** - Set up IAM roles with Bedrock permissions (avoid access keys)
2. **Enable Model Access** - Request access to specific foundation models in AWS Console
3. **Initialize Clients** - Create reusable `BedrockClient` and `BedrockRuntimeClient` instances
4. **Validate Model Availability** - Test with a simple invocation before production use
5. **Build Payloads** - Create model-specific JSON payloads with proper format
6. **Handle Responses** - Parse response structure and extract content
7. **Implement Streaming** - Use response stream handlers for real-time generation
8. **Add Error Handling** - Implement retry logic with exponential backoff

**Validation Checkpoint**: Always test with a simple prompt (e.g., "Hello") before production use to verify model access and response parsing.

## Examples

### Text Generation with Claude

```java
public String generateWithClaude(BedrockRuntimeClient client, String prompt) {
    JSONObject payload = new JSONObject()
        .put("anthropic_version", "bedrock-2023-05-31")
        .put("max_tokens", 1000)
        .put("messages", new JSONObject[]{
            new JSONObject().put("role", "user").put("content", prompt)
        });

    InvokeModelResponse response = client.invokeModel(InvokeModelRequest.builder()
        .modelId("anthropic.claude-sonnet-4-5-20250929-v1:0")
        .body(SdkBytes.fromUtf8String(payload.toString()))
        .build());

    JSONObject responseBody = new JSONObject(response.body().asUtf8String());
    return responseBody.getJSONArray("content")
        .getJSONObject(0)
        .getString("text");
}
```

### Model Discovery

```java
import software.amazon.awssdk.services.bedrock.model.*;

public List<FoundationModelSummary> listFoundationModels(BedrockClient bedrockClient) {
    return bedrockClient.listFoundationModels().modelSummaries();
}
```

### Multi-Model Invocation

```java
public String invokeModel(BedrockRuntimeClient client, String modelId, String prompt) {
    JSONObject payload = createPayload(modelId, prompt);

    InvokeModelResponse response = client.invokeModel(request -> request
        .modelId(modelId)
        .body(SdkBytes.fromUtf8String(payload.toString())));

    return extractTextFromResponse(modelId, response.body().asUtf8String());
}

private JSONObject createPayload(String modelId, String prompt) {
    if (modelId.startsWith("anthropic.claude")) {
        return new JSONObject()
            .put("anthropic_version", "bedrock-2023-05-31")
            .put("max_tokens", 1000)
            .put("messages", new JSONObject[]{
                new JSONObject().put("role", "user").put("content", prompt)
            });
    } else if (modelId.startsWith("amazon.titan")) {
        return new JSONObject()
            .put("inputText", prompt)
            .put("textGenerationConfig", new JSONObject()
                .put("maxTokenCount", 512)
                .put("temperature", 0.7));
    } else if (modelId.startsWith("meta.llama")) {
        return new JSONObject()
            .put("prompt", "[INST] " + prompt + " [/INST]")
            .put("max_gen_len", 512)
            .put("temperature", 0.7);
    }
    throw new IllegalArgumentException("Unsupported model: " + modelId);
}
```

### Streaming Response with Error Handling

```java
public String streamResponseWithRetry(BedrockRuntimeClient client, String modelId, String prompt, int maxRetries) {
    int attempt = 0;
    while (attempt < maxRetries) {
        try {
            JSONObject payload = createPayload(modelId, prompt);
            StringBuilder fullResponse = new StringBuilder();

            InvokeModelWithResponseStreamRequest request = InvokeModelWithResponseStreamRequest.builder()
                .modelId(modelId)
                .body(SdkBytes.fromUtf8String(payload.toString()))
                .build();

            client.invokeModelWithResponseStream(request,
                InvokeModelWithResponseStreamResponseHandler.builder()
                    .onEventStream(stream -> stream.forEach(event -> {
                        if (event instanceof PayloadPart) {
                            String chunk = ((PayloadPart) event).bytes().asUtf8String();
                            fullResponse.append(chunk);
                        }
                    }))
                    .onError(e -> System.err.println("Stream error: " + e.getMessage()))
                    .build());

            return fullResponse.toString();
        } catch (Exception e) {
            attempt++;
            if (attempt >= maxRetries) {
                throw new RuntimeException("Stream failed after " + maxRetries + " attempts", e);
            }
            try {
                Thread.sleep((long) Math.pow(2, attempt) * 1000); // Exponential backoff
            } catch (InterruptedException ie) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Interrupted during retry", ie);
            }
        }
    }
    throw new RuntimeException("Unexpected error in streaming");
}
```

### Exponential Backoff for Throttling

```java
import software.amazon.awssdk.awscore.exception.AwsServiceException;

public <T> T invokeWithRetry(Supplier<T> invocation, int maxRetries) {
    int attempt = 0;
    while (attempt < maxRetries) {
        try {
            return invocation.get();
        } catch (AwsServiceException e) {
            if (e.statusCode() == 429 || e.statusCode() >= 500) {
                attempt++;
                if (attempt >= maxRetries) throw e;
                long delayMs = Math.min(1000 * (1L << attempt) + (long) (Math.random() * 1000), 30000);
                Thread.sleep(delayMs);
            } else {
                throw e;
            }
        }
    }
    throw new IllegalStateException("Should not reach here");
}
```

### Text Embeddings

```java
public double[] createEmbeddings(BedrockRuntimeClient client, String text) {
    String modelId = "amazon.titan-embed-text-v1";

    JSONObject payload = new JSONObject().put("inputText", text);

    InvokeModelResponse response = client.invokeModel(request -> request
        .modelId(modelId)
        .body(SdkBytes.fromUtf8String(payload.toString())));

    JSONObject responseBody = new JSONObject(response.body().asUtf8String());
    JSONArray embeddingArray = responseBody.getJSONArray("embedding");

    double[] embeddings = new double[embeddingArray.length()];
    for (int i = 0; i < embeddingArray.length(); i++) {
        embeddings[i] = embeddingArray.getDouble(i);
    }
    return embeddings;
}
```

### Spring Boot Integration

```java
@Configuration
public class BedrockConfiguration {

    @Bean
    public BedrockClient bedrockClient() {
        return BedrockClient.builder()
            .region(Region.US_EAST_1)
            .build();
    }

    @Bean
    public BedrockRuntimeClient bedrockRuntimeClient() {
        return BedrockRuntimeClient.builder()
            .region(Region.US_EAST_1)
            .build();
    }
}

@Service
public class BedrockAIService {

    private final BedrockRuntimeClient bedrockRuntimeClient;
    private final ObjectMapper mapper;

    @Value("${bedrock.default-model-id:anthropic.claude-sonnet-4-5-20250929-v1:0}")
    private String defaultModelId;

    public BedrockAIService(BedrockRuntimeClient bedrockRuntimeClient, ObjectMapper mapper) {
        this.bedrockRuntimeClient = bedrockRuntimeClient;
        this.mapper = mapper;
    }

    public String generateText(String prompt) {
        Map<String, Object> payload = Map.of(
            "anthropic_version", "bedrock-2023-05-31",
            "max_tokens", 1000,
            "messages", List.of(Map.of("role", "user", "content", prompt))
        );

        InvokeModelResponse response = bedrockRuntimeClient.invokeModel(
            InvokeModelRequest.builder()
                .modelId(defaultModelId)
                .body(SdkBytes.fromUtf8String(mapper.writeValueAsString(payload)))
                .build());

        return extractText(response.body().asUtf8String());
    }
}
```

See [examples directory](references/aws-sdk-examples.md) for comprehensive usage patterns.

## Best Practices

### Model Selection
- **Claude 4.5 Sonnet**: Complex reasoning, analysis, and creative tasks
- **Claude 4.5 Haiku**: Fast and affordable for real-time applications
- **Llama 3.1**: Open-source alternative for general tasks
- **Titan**: AWS native, cost-effective for simple text generation

### Performance
- Reuse client instances (avoid creating new clients per request)
- Use async clients for I/O operations
- Implement streaming for long responses
- Cache foundation model lists

### Security
- Never log sensitive prompt data
- Use IAM roles for authentication
- Sanitize user inputs to prevent prompt injection
- Implement rate limiting for public applications

## Constraints and Warnings

- **Cost Management**: Bedrock API calls incur charges per token; implement usage monitoring and budget alerts.
- **Model Access**: Foundation models must be enabled in AWS Console; verify region availability.
- **Rate Limits**: Implement exponential backoff for throttling; check per-model limits.
- **Payload Size**: Maximum payload size varies by model; use chunking for large documents.
- **Streaming Complexity**: Handle partial content and error recovery carefully.
- **Data Privacy**: Prompts and responses may be logged by AWS; review data policies.
- **Credentials**: Never embed credentials in code; use IAM roles for EC2/Lambda.

## Common Model IDs

- Claude Sonnet 4.5: `anthropic.claude-sonnet-4-5-20250929-v1:0`
- Claude Haiku 4.5: `anthropic.claude-haiku-4-5-20251001-v1:0`
- Llama 3.1 70B: `meta.llama3-1-70b-instruct-v1:0`
- Titan Embeddings: `amazon.titan-embed-text-v1`

See [Model Reference](references/model-reference.md) for complete list.

## References

- [Advanced Topics](references/advanced-topics.md) - Multi-model patterns, advanced error handling
- [Model Reference](references/model-reference.md) - Detailed specifications, payload formats
- [Testing Strategies](references/testing-strategies.md) - Unit testing, LocalStack integration
- [AWS Bedrock User Guide](references/aws-bedrock-user-guide.md)
- [AWS SDK Examples](references/aws-sdk-examples.md)
- [Supported Models](references/bedrock-models-supported.md)

## Related Skills

- `aws-sdk-java-v2-core` - Core AWS SDK patterns
- `langchain4j-ai-services-patterns` - LangChain4j integration
- `spring-boot-dependency-injection` - Spring DI patterns
