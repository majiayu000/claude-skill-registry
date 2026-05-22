---
name: langchain4j-vector-stores-configuration
description: Configure LangChain4J vector stores for RAG applications. Use when building semantic search, integrating vector databases (PostgreSQL/pgvector, Pinecone, MongoDB, Milvus, Neo4j), implementing embedding storage/retrieval, setting up hybrid search, or optimizing vector database performance for production AI applications.
allowed-tools: Read, Write, Bash, Edit
category: backend
tags: [langchain4j, vector-stores, embeddings, rag, semantic-search, ai, llm, java, databases]
version: 1.1.0
---

# LangChain4J Vector Stores Configuration

Configure vector stores for Retrieval-Augmented Generation applications with LangChain4J.

## When to Use

To configure vector stores when:

- Building RAG applications requiring embedding storage and retrieval
- Implementing semantic search in Java applications
- Integrating LLMs with vector databases for context-aware responses
- Configuring multi-modal embedding storage for text, images, or other data
- Setting up hybrid search combining vector similarity and full-text search
- Migrating between different vector store providers
- Optimizing vector database performance for production workloads
- Building AI-powered applications with memory and persistence
- Implementing document chunking and embedding pipelines
- Creating recommendation systems based on vector similarity

## Instructions

### Set Up Basic Vector Store

Configure an embedding store for vector operations:

```java
@Bean
public EmbeddingStore<TextSegment> embeddingStore() {
    return PgVectorEmbeddingStore.builder()
        .host("localhost")
        .port(5432)
        .database("vectordb")
        .user("username")
        .password("password")
        .table("embeddings")
        .dimension(1536) // OpenAI embedding dimension
        .createTable(true)
        .useIndex(true)
        .build();
}
```

### Configure Multiple Vector Stores

Use different stores for different use cases:

```java
@Configuration
public class MultiVectorStoreConfiguration {

    @Bean
    @Qualifier("documentsStore")
    public EmbeddingStore<TextSegment> documentsEmbeddingStore() {
        return PgVectorEmbeddingStore.builder()
            .table("document_embeddings")
            .dimension(1536)
            .build();
    }

    @Bean
    @Qualifier("chatHistoryStore")
    public EmbeddingStore<TextSegment> chatHistoryEmbeddingStore() {
        return MongoDbEmbeddingStore.builder()
            .collectionName("chat_embeddings")
            .build();
    }
}
```

### Implement Document Ingestion

Use EmbeddingStoreIngestor for automated document processing:

```java
@Bean
public EmbeddingStoreIngestor embeddingStoreIngestor(
        EmbeddingStore<TextSegment> embeddingStore,
        EmbeddingModel embeddingModel) {

    return EmbeddingStoreIngestor.builder()
        .documentSplitter(DocumentSplitters.recursive(
            300,  // maxSegmentSizeInTokens
            20,   // maxOverlapSizeInTokens
            new OpenAiTokenizer(GPT_3_5_TURBO)
        ))
        .embeddingModel(embeddingModel)
        .embeddingStore(embeddingStore)
        .build();
}
```

### Set Up Metadata Filtering

Configure metadata-based filtering capabilities:

```java
// MongoDB with metadata field mapping
IndexMapping indexMapping = IndexMapping.builder()
    .dimension(1536)
    .metadataFieldNames(Set.of("category", "source", "created_date", "author"))
    .build();

// Search with metadata filters
EmbeddingSearchRequest request = EmbeddingSearchRequest.builder()
    .queryEmbedding(queryEmbedding)
    .maxResults(10)
    .filter(and(
        metadataKey("category").isEqualTo("technical_docs"),
        metadataKey("created_date").isGreaterThan(LocalDate.now().minusMonths(6))
    ))
    .build();
```

### Configure Production Settings

Implement connection pooling and monitoring:

```java
@Bean
public EmbeddingStore<TextSegment> optimizedPgVectorStore() {
    HikariConfig hikariConfig = new HikariConfig();
    hikariConfig.setJdbcUrl("jdbc:postgresql://localhost:5432/vectordb");
    hikariConfig.setUsername("username");
    hikariConfig.setPassword("password");
    hikariConfig.setMaximumPoolSize(20);
    hikariConfig.setMinimumIdle(5);
    hikariConfig.setConnectionTimeout(30000);

    DataSource dataSource = new HikariDataSource(hikariConfig);

    return PgVectorEmbeddingStore.builder()
        .dataSource(dataSource)
        .table("embeddings")
        .dimension(1536)
        .useIndex(true)
        .build();
}
```

### Implement Health Checks

Monitor vector store connectivity:

```java
@Component
public class VectorStoreHealthIndicator implements HealthIndicator {

    private final EmbeddingStore<TextSegment> embeddingStore;

    @Override
    public Health health() {
        try {
            embeddingStore.search(EmbeddingSearchRequest.builder()
                .queryEmbedding(new Embedding(Collections.nCopies(1536, 0.0f)))
                .maxResults(1)
                .build());

            return Health.up()
                .withDetail("store", embeddingStore.getClass().getSimpleName())
                .build();
        } catch (Exception e) {
            return Health.down()
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

## Examples

### Basic RAG Application Setup

```java
@Configuration
public class SimpleRagConfig {

    @Bean
    public EmbeddingStore<TextSegment> embeddingStore() {
        return PgVectorEmbeddingStore.builder()
            .host("localhost")
            .database("rag_db")
            .table("documents")
            .dimension(1536)
            .build();
    }

    @Bean
    public ChatLanguageModel chatModel() {
        return OpenAiChatModel.withApiKey(System.getenv("OPENAI_API_KEY"));
    }
}
```

### Semantic Search Service

```java
@Service
public class SemanticSearchService {

    private final EmbeddingStore<TextSegment> store;
    private final EmbeddingModel embeddingModel;

    public List<String> search(String query, int maxResults) {
        Embedding queryEmbedding = embeddingModel.embed(query).content();

        EmbeddingSearchRequest request = EmbeddingSearchRequest.builder()
            .queryEmbedding(queryEmbedding)
            .maxResults(maxResults)
            .minScore(0.75)
            .build();

        return store.search(request).matches().stream()
            .map(match -> match.embedded().text())
            .toList();
    }
}
```

### Production Setup with Monitoring

```java
@Configuration
public class ProductionVectorStoreConfig {

    @Bean
    public EmbeddingStore<TextSegment> vectorStore(
            @Value("${vector.store.host}") String host,
            MeterRegistry meterRegistry) {

        EmbeddingStore<TextSegment> store = PgVectorEmbeddingStore.builder()
            .host(host)
            .database("production_vectors")
            .useIndex(true)
            .indexListSize(200)
            .build();

        return new MonitoredEmbeddingStore<>(store, meterRegistry);
    }
}
```

## Best Practices

### Choose the Right Vector Store

**For Development:**
- Use `InMemoryEmbeddingStore` for local development and testing
- Fast setup, no external dependencies
- Data lost on application restart

**For Production:**
- **PostgreSQL + pgvector**: Excellent for existing PostgreSQL environments
- **Pinecone**: Managed service, good for rapid prototyping
- **MongoDB Atlas**: Good integration with existing MongoDB applications
- **Milvus/Zilliz**: High performance for large-scale deployments

### Configure Appropriate Index Types

Choose index types based on performance requirements:

```java
// For high recall requirements
.indexType(IndexType.FLAT)  // Exact search, slower but accurate

// For balanced performance
.indexType(IndexType.IVF_FLAT)  // Good balance of speed and accuracy

// For high-speed approximate search
.indexType(IndexType.HNSW)  // Fastest, slightly less accurate
```

### Optimize Vector Dimensions

Match embedding dimensions to your model:

```java
// OpenAI text-embedding-3-small
.dimension(1536)

// OpenAI text-embedding-3-large
.dimension(3072)

// Sentence Transformers
.dimension(384)  // all-MiniLM-L6-v2
.dimension(768)  // all-mpnet-base-v2
```

### Implement Batch Operations

Use batch operations for better performance:

```java
@Service
public class BatchEmbeddingService {

    private static final int BATCH_SIZE = 100;

    public void addDocumentsBatch(List<Document> documents) {
        for (List<Document> batch : Lists.partition(documents, BATCH_SIZE)) {
            List<TextSegment> segments = batch.stream()
                .map(doc -> TextSegment.from(doc.text(), doc.metadata()))
                .collect(Collectors.toList());

            List<Embedding> embeddings = embeddingModel.embedAll(segments)
                .content();

            embeddingStore.addAll(embeddings, segments);
        }
    }
}
```

### Secure Configuration

Protect sensitive configuration:

```java
// Use environment variables
@Value("${vector.store.api.key:#{null}}")
private String apiKey;

// Validate configuration
@PostConstruct
public void validateConfiguration() {
    if (StringUtils.isBlank(apiKey)) {
        throw new IllegalStateException("Vector store API key must be configured");
    }
}
```

## References

For comprehensive documentation and advanced configurations, see:

- [API Reference](references/api-reference.md) - Complete API documentation
- [Examples](references/examples.md) - Production-ready examples
