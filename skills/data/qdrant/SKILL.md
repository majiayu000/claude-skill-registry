---
name: qdrant-vector-database-integration
description: Qdrant vector database integration patterns with LangChain4j. Store embeddings, similarity search, and vector management for Java applications. Use when implementing vector-based retrieval for RAG systems, semantic search, or recommendation engines.
category: backend
tags: [qdrant, java, spring-boot, langchain4j, vector-search, ai, machine-learning]
version: 1.2.0
allowed-tools: Read, Write, Bash
---

# Qdrant Vector Database Integration

## Overview

Qdrant is an AI-native vector database for semantic search and similarity retrieval. This skill provides patterns for integrating Qdrant with Java applications, focusing on Spring Boot integration and LangChain4j framework support. Enable efficient vector search capabilities for RAG systems, recommendation engines, and semantic search applications.

## When to Use

Use this skill when implementing:
- Semantic search or recommendation systems in Spring Boot applications
- Retrieval-Augmented Generation (RAG) pipelines with Java and LangChain4j
- Vector database integration for AI and machine learning applications
- High-performance similarity search with filtered queries
- Embedding storage and retrieval for context-aware applications

## Getting Started: Qdrant Setup

To begin integration, first deploy a Qdrant instance.

### Local Development with Docker

```bash
# Pull the latest Qdrant image
docker pull qdrant/qdrant

# Run the Qdrant container
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

Access Qdrant via:
- **REST API**: `http://localhost:6333`
- **gRPC API**: `http://localhost:6334` (used by Java client)

## Core Java Client Integration

Add dependencies to your build configuration and initialize the client for programmatic access.

### Dependency Configuration

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

### Client Initialization

Create and configure the Qdrant client for application use:

```java
import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;

// Basic local connection
QdrantClient client = new QdrantClient(
    QdrantGrpcClient.newBuilder("localhost").build());

// Secure connection with API key
QdrantClient secureClient = new QdrantClient(
    QdrantGrpcClient.newBuilder("localhost", 6334, false)
        .withApiKey("YOUR_API_KEY")
        .build());

// Managed connection with TLS
QdrantClient tlsClient = new QdrantClient(
    QdrantGrpcClient.newBuilder(channel)
        .withApiKey("YOUR_API_KEY")
        .build());
```

## Collection Management

Create and configure vector collections with appropriate distance metrics and dimensions.

### Create Collections

```java
import io.qdrant.client.grpc.Collections.Distance;
import io.qdrant.client.grpc.Collections.VectorParams;
import java.util.concurrent.ExecutionException;

// Create a collection with cosine distance
client.createCollectionAsync("search-collection",
    VectorParams.newBuilder()
        .setDistance(Distance.Cosine)
        .setSize(384)
        .build()).get();

// Create collection with configuration
client.createCollectionAsync("recommendation-engine",
    VectorParams.newBuilder()
        .setDistance(Distance.Euclidean)
        .setSize(512)
        .build()).get();
```

## Vector Operations

Perform common vector operations including upsert, search, and filtering.

### Upsert Points

```java
import io.qdrant.client.grpc.Points.PointStruct;
import java.util.List;
import java.util.Map;
import static io.qdrant.client.PointIdFactory.id;
import static io.qdrant.client.ValueFactory.value;
import static io.qdrant.client.VectorsFactory.vectors;

// Batch upsert vector points
List<PointStruct> points = List.of(
    PointStruct.newBuilder()
        .setId(id(1))
        .setVectors(vectors(0.05f, 0.61f, 0.76f, 0.74f))
        .putAllPayload(Map.of(
            "title", value("Spring Boot Documentation"),
            "content", value("Spring Boot framework documentation")
        ))
        .build(),
    PointStruct.newBuilder()
        .setId(id(2))
        .setVectors(vectors(0.19f, 0.81f, 0.75f, 0.11f))
        .putAllPayload(Map.of(
            "title", value("Qdrant Vector Database"),
            "content", value("Vector database for AI applications")
        ))
        .build()
);

client.upsertAsync("search-collection", points).get();
```

### Vector Search

```java
import io.qdrant.client.grpc.Points.QueryPoints;
import io.qdrant.client.grpc.Points.ScoredPoint;
import static io.qdrant.client.QueryFactory.nearest;
import java.util.List;

// Basic similarity search
List<ScoredPoint> results = client.queryAsync(
    QueryPoints.newBuilder()
        .setCollectionName("search-collection")
        .setLimit(5)
        .setQuery(nearest(0.2f, 0.1f, 0.9f, 0.7f))
        .build()
).get();

// Search with filters
List<ScoredPoint> filteredResults = client.searchAsync(
    SearchPoints.newBuilder()
        .setCollectionName("search-collection")
        .addAllVector(List.of(0.6235f, 0.123f, 0.532f, 0.123f))
        .setFilter(Filter.newBuilder()
            .addMust(range("rand_number",
                Range.newBuilder().setGte(3).build()))
            .build())
        .setLimit(5)
        .build()).get();
```

## Spring Boot Integration

Integrate Qdrant with Spring Boot using dependency injection and proper configuration.

### Configuration Class

```java
import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class QdrantConfig {

    @Value("${qdrant.host:localhost}")
    private String host;

    @Value("${qdrant.port:6334}")
    private int port;

    @Value("${qdrant.api-key:}")
    private String apiKey;

    @Bean
    public QdrantClient qdrantClient() {
        QdrantGrpcClient grpcClient = QdrantGrpcClient.newBuilder(host, port, false)
            .withApiKey(apiKey)
            .build();

        return new QdrantClient(grpcClient);
    }
}
```

### Service Layer Implementation

```java
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.concurrent.ExecutionException;

@Service
public class VectorSearchService {

    private final QdrantClient qdrantClient;

    public VectorSearchService(QdrantClient qdrantClient) {
        this.qdrantClient = qdrantClient;
    }

    public List<ScoredPoint> search(String collectionName, List<Float> queryVector) {
        try {
            return qdrantClient.queryAsync(
                QueryPoints.newBuilder()
                    .setCollectionName(collectionName)
                    .setLimit(5)
                    .setQuery(nearest(queryVector))
                    .build()
            ).get();
        } catch (InterruptedException | ExecutionException e) {
            throw new RuntimeException("Qdrant search failed", e);
        }
    }

    public void upsertPoints(String collectionName, List<PointStruct> points) {
        try {
            qdrantClient.upsertAsync(collectionName, points).get();
        } catch (InterruptedException | ExecutionException e) {
            throw new RuntimeException("Qdrant upsert failed", e);
        }
    }
}
```

## LangChain4j Integration

Leverage LangChain4j for high-level vector store abstractions and RAG implementations.

### Dependency Setup

**Maven:**
```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-qdrant</artifactId>
    <version>1.7.0</version>
</dependency>
```

### QdrantEmbeddingStore Configuration

```java
import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.embedding.EmbeddingModel;
import dev.langchain4j.embedding.allminilml6v2.AllMiniLmL6V2EmbeddingModel;
import dev.langchain4j.store.embedding.EmbeddingStore;
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor;
import dev.langchain4j.store.embedding.qdrant.QdrantEmbeddingStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class Langchain4jConfig {

    @Bean
    public EmbeddingStore<TextSegment> embeddingStore() {
        return QdrantEmbeddingStore.builder()
            .collectionName("rag-collection")
            .host("localhost")
            .port(6334)
            .apiKey("YOUR_API_KEY")
            .build();
    }

    @Bean
    public EmbeddingModel embeddingModel() {
        return new AllMiniLmL6V2EmbeddingModel();
    }

    @Bean
    public EmbeddingStoreIngestor embeddingStoreIngestor(
            EmbeddingStore<TextSegment> embeddingStore,
            EmbeddingModel embeddingModel) {
        return EmbeddingStoreIngestor.builder()
            .embeddingStore(embeddingStore)
            .embeddingModel(embeddingModel)
            .build();
    }
}
```

### RAG Service Implementation

```java
import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.embedding.EmbeddingModel;
import dev.langchain4j.store.embedding.EmbeddingStore;
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class RagService {

    private final EmbeddingStoreIngestor ingestor;

    public RagService(EmbeddingStoreIngestor ingestor) {
        this.ingestor = ingestor;
    }

    public void ingestDocument(String text) {
        TextSegment segment = TextSegment.from(text);
        ingestor.ingest(segment);
    }

    public List<TextSegment> findRelevant(String query) {
        EmbeddingStore<TextSegment> embeddingStore = ingestor.getEmbeddingStore();
        return embeddingStore.findRelevant(
            ingestor.getEmbeddingModel().embed(query).content(),
            5,
            0.7
        ).stream()
            .map(match -> match.embedded())
            .toList();
    }
}
```

## Examples

### Basic Search Implementation

```java
// Create simple search endpoint
@RestController
@RequestMapping("/api/search")
public class SearchController {

    private final VectorSearchService searchService;

    public SearchController(VectorSearchService searchService) {
        this.searchService = searchService;
    }

    @GetMapping
    public List<ScoredPoint> search(@RequestParam String query) {
        // Convert query to embedding (requires embedding model)
        List<Float> queryVector = embeddingModel.embed(query).content().vectorAsList();
        return searchService.search("documents", queryVector);
    }
}
```

## Best Practices

### Vector Database Configuration
- Use appropriate distance metrics: Cosine for text, Euclidean for numerical data
- Optimize vector dimensions based on embedding model specifications
- Configure proper collection naming conventions
- Monitor performance and optimize search parameters

### Spring Boot Integration
- Always use constructor injection for dependency injection
- Handle async operations with proper exception handling
- Configure connection timeouts and retry policies
- Use proper bean configuration for production environments

### Security Considerations
- Never hardcode API keys in code
- Use environment variables or Spring configuration properties
- Implement proper authentication and authorization
- Use TLS for production connections

### Performance Optimization
- Batch operations for bulk upserts
- Use appropriate limits and filters
- Monitor memory usage and connection pooling
- Consider sharding for large datasets

## Advanced Patterns

### Multi-tenant Vector Storage
```java
// Implement collection-based multi-tenancy
public class MultiTenantVectorService {
    private final QdrantClient client;

    public void upsertForTenant(String tenantId, List<PointStruct> points) {
        String collectionName = "tenant_" + tenantId + "_documents";
        client.upsertAsync(collectionName, points).get();
    }
}
```

### Hybrid Search with Filters
```java
// Combine vector similarity with metadata filtering
public List<ScoredPoint> hybridSearch(String collectionName, List<Float> queryVector,
                                     String category, Date dateRange) {
    Filter filter = Filter.newBuilder()
        .addMust(range("created_at",
            Range.newBuilder().setGte(dateRange.getTime()).build()))
        .addMust(exactMatch("category", category))
        .build();

    return client.searchAsync(
        SearchPoints.newBuilder()
            .setCollectionName(collectionName)
            .addAllVector(queryVector)
            .setFilter(filter)
            .build()
    ).get();
}
```

## References

For comprehensive technical details and advanced patterns, see:
- [Qdrant API Reference](references/references.md) - Complete client API documentation
- [Complete Spring Boot Examples](references/examples.md) - Full application implementations
- [Official Qdrant Documentation](https://qdrant.tech/documentation/) - Core documentation
- [LangChain4j Documentation](https://langchain4j.dev/) - Framework-specific patterns