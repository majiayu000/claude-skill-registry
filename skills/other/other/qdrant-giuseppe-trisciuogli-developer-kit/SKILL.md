---
name: qdrant
description: Provides Qdrant vector database integration patterns with LangChain4j. Handles embedding storage, similarity search, and vector management for Java applications. Use when implementing vector-based retrieval for RAG systems, semantic search, or recommendation engines.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Qdrant Vector Database Integration

## Overview

Qdrant is an AI-native vector database for semantic search and similarity retrieval. This skill provides patterns for integrating Qdrant with Java applications, focusing on Spring Boot and LangChain4j integration.

## When to Use

- Semantic search or recommendation systems in Spring Boot applications
- RAG pipelines with Java and LangChain4j
- Vector database integration for AI/ML applications
- High-performance similarity search with filtered queries

## Instructions

### 1. Deploy Qdrant with Docker

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

Access: REST API at `http://localhost:6333`, gRPC at `http://localhost:6334`.

### 2. Add Dependencies

**Maven:**
```xml
<dependency>
    <groupId>io.qdrant</groupId>
    <artifactId>client</artifactId>
    <version>1.15.0</version>
</dependency>
```

**Gradle:**
```gradle
implementation 'io.qdrant:client:1.15.0'
```

### 3. Initialize Client

```java
QdrantClient client = new QdrantClient(
    QdrantGrpcClient.newBuilder("localhost").build());
```

For production with API key:
```java
QdrantClient client = new QdrantClient(
    QdrantGrpcClient.newBuilder("localhost", 6334, false)
        .withApiKey("YOUR_API_KEY")
        .build());
```

### 4. Create Collection

```java
client.createCollectionAsync("search-collection",
    VectorParams.newBuilder()
        .setDistance(Distance.Cosine)
        .setSize(384)
        .build()
).get();
```

**Validation:** Verify the collection was created by checking `client.getCollectionAsync("search-collection").get()`.

### 5. Upsert Vectors

```java
List<PointStruct> points = List.of(
    PointStruct.newBuilder()
        .setId(id(1))
        .setVectors(vectors(0.05f, 0.61f, 0.76f, 0.74f))
        .putAllPayload(Map.of("title", value("Spring Boot Documentation")))
        .build()
);
client.upsertAsync("search-collection", points).get();
```

**Validation:** Check that `client.upsertAsync(...).get()` completes without throwing.

### 6. Search Vectors

```java
List<ScoredPoint> results = client.queryAsync(
    QueryPoints.newBuilder()
        .setCollectionName("search-collection")
        .setLimit(5)
        .setQuery(nearest(0.2f, 0.1f, 0.9f, 0.7f))
        .build()
).get();
```

Filtered search:
```java
List<ScoredPoint> results = client.searchAsync(
    SearchPoints.newBuilder()
        .setCollectionName("search-collection")
        .addAllVector(List.of(0.62f, 0.12f, 0.53f, 0.12f))
        .setFilter(Filter.newBuilder()
            .addMust(range("category", Range.newBuilder().setEq("docs").build()))
            .build())
        .setLimit(5)
        .build()).get();
```

## LangChain4j Integration

For RAG pipelines, use LangChain4j's high-level abstractions:

```java
EmbeddingStore<TextSegment> embeddingStore = QdrantEmbeddingStore.builder()
    .collectionName("rag-collection")
    .host("localhost")
    .port(6334)
    .apiKey("YOUR_API_KEY")
    .build();
```

Spring Boot configuration with LangChain4j:
```java
@Bean
public EmbeddingStore<TextSegment> embeddingStore() {
    return QdrantEmbeddingStore.builder()
        .collectionName("rag-collection")
        .host(host)
        .port(port)
        .build();
}

@Bean
public EmbeddingModel embeddingModel() {
    return new AllMiniLmL6V2EmbeddingModel();
}
```

## Spring Boot Integration

Inject the client via configuration:

```java
@Configuration
public class QdrantConfig {
    @Value("${qdrant.host:localhost}")
    private String host;

    @Value("${qdrant.port:6334}")
    private int port;

    @Bean
    public QdrantClient qdrantClient() {
        return new QdrantClient(
            QdrantGrpcClient.newBuilder(host, port, false).build());
    }
}
```

## Examples

### REST Search Endpoint

```java
@RestController
@RequestMapping("/api/search")
public class SearchController {
    private final VectorSearchService searchService;

    public SearchController(VectorSearchService searchService) {
        this.searchService = searchService;
    }

    @GetMapping
    public List<ScoredPoint> search(@RequestParam String query) {
        List<Float> queryVector = embeddingModel.embed(query).content().vectorAsList();
        return searchService.search("documents", queryVector);
    }
}
```

## Best Practices

- **Distance metric**: Cosine for normalized text embeddings, Euclidean for non-normalized.
- **Batch upserts**: Use batch operations over individual point insertions.
- **Connection pooling**: Configure connection pooling for high-throughput production workloads.
- **Error handling**: Wrap async operations in try/catch for ExecutionException/InterruptedException.
- **API keys**: Store in environment variables or Spring config, never hardcode.

## Advanced Patterns

### Multi-tenant Storage

```java
public void upsertForTenant(String tenantId, List<PointStruct> points) {
    String collectionName = "tenant_" + tenantId + "_documents";
    client.upsertAsync(collectionName, points).get();
}
```

### Docker Compose for Production

```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.7.0
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage
```

## References

- [Qdrant API Reference](references/references.md) — Complete client API documentation
- [Complete Spring Boot Examples](references/examples.md) — Full application implementations
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [LangChain4j Documentation](https://langchain4j.dev/)

## Constraints and Warnings

- Vector dimensions must match the embedding model exactly; mismatched dimensions cause upsert errors.
- **Input validation**: Sanitize all document content before ingestion; untrusted payloads may contain prompt injection attacks.
- **Content filtering**: Apply content filtering on retrieved documents before passing them to the LLM.
- Large collections require proper indexing for acceptable search performance.
- Use gRPC API (port 6334) for production; REST API (port 6333) for debugging only.
- Collection recreation deletes all data; implement backup strategies for production environments.
