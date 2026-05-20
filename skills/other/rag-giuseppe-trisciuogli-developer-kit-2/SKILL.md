---
name: rag
description: Provides patterns to build Retrieval-Augmented Generation (RAG) systems for AI applications with vector databases and semantic search. Use when implementing knowledge-grounded AI, building document Q&A systems, or integrating LLMs with external knowledge bases.
allowed-tools: Read, Write, Bash
---

# RAG Implementation

Build Retrieval-Augmented Generation systems that extend AI capabilities with external knowledge sources.

## Overview

RAG (Retrieval-Augmented Generation) enhances AI applications by retrieving relevant information from knowledge bases and incorporating it into AI responses, reducing hallucinations and providing accurate, grounded answers.

## When to Use

Use this skill when:

- Building Q&A systems over proprietary documents
- Creating chatbots with current, factual information
- Implementing semantic search with natural language queries
- Reducing hallucinations with grounded responses
- Enabling AI systems to access domain-specific knowledge
- Building documentation assistants
- Creating research tools with source citation
- Developing knowledge management systems

## Instructions

### Step 1: Choose Vector Database

Select an appropriate vector database based on your requirements:

1. **For production scalability**: Use Pinecone or Milvus
2. **For open-source requirements**: Use Weaviate or Qdrant
3. **For local development**: Use Chroma or FAISS
4. **For hybrid search needs**: Use Weaviate with BM25 support

### Step 2: Select Embedding Model

Choose an embedding model based on your use case:

1. **General purpose**: text-embedding-ada-002 (OpenAI)
2. **Fast and lightweight**: all-MiniLM-L6-v2
3. **Multilingual support**: e5-large-v2
4. **Best performance**: bge-large-en-v1.5

### Step 3: Implement Document Processing Pipeline

1. Load documents from your source (file system, database, API)
2. Clean and preprocess documents (remove formatting artifacts, normalize text)
3. Split documents into chunks using appropriate chunking strategy
4. Generate embeddings for each chunk
5. Store embeddings in your vector database with metadata

### Step 4: Configure Retrieval Strategy

1. **Dense Retrieval**: Use semantic similarity via embeddings for most use cases
2. **Hybrid Search**: Combine dense + sparse retrieval for better coverage
3. **Metadata Filtering**: Add filters based on document attributes
4. **Reranking**: Implement cross-encoder reranking for high-precision requirements

### Step 5: Build RAG Pipeline

1. Create content retriever with your embedding store
2. Configure AI service with retriever and chat memory
3. Implement prompt template with context injection
4. Add response validation and grounding checks

### Step 6: Evaluate and Optimize

1. Measure retrieval metrics (precision@k, recall@k, MRR)
2. Evaluate answer quality (faithfulness, relevance)
3. Monitor performance and user feedback
4. Iterate on chunking, retrieval, and prompt parameters

## Examples

### Example 1: Basic Document Q&A System

```java
// Simple RAG setup for document Q&A
List<Document> documents = FileSystemDocumentLoader.loadDocuments("/docs");

InMemoryEmbeddingStore<TextSegment> store = new InMemoryEmbeddingStore<>();
EmbeddingStoreIngestor.ingest(documents, store);

DocumentAssistant assistant = AiServices.builder(DocumentAssistant.class)
    .chatModel(chatModel)
    .contentRetriever(EmbeddingStoreContentRetriever.from(store))
    .build();

String answer = assistant.answer("What is the company policy on remote work?");
```

### Example 2: Metadata-Filtered Retrieval

```java
// RAG with metadata filtering for specific document categories
EmbeddingStoreContentRetriever retriever = EmbeddingStoreContentRetriever.builder()
    .embeddingStore(store)
    .embeddingModel(embeddingModel)
    .maxResults(5)
    .minScore(0.7)
    .filter(metadataKey("category").isEqualTo("technical"))
    .build();
```

### Example 3: Multi-Source RAG Pipeline

```java
// Combine multiple knowledge sources
ContentRetriever webRetriever = EmbeddingStoreContentRetriever.from(webStore);
ContentRetriever docRetriever = EmbeddingStoreContentRetriever.from(docStore);

List<Content> results = new ArrayList<>();
results.addAll(webRetriever.retrieve(query));
results.addAll(docRetriever.retrieve(query));

// Rerank and return top results
List<Content> topResults = reranker.reorder(query, results).subList(0, 5);
```

### Example 4: RAG with Chat Memory

```java
// Conversational RAG with context retention
Assistant assistant = AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
    .contentRetriever(retriever)
    .build();

// Multi-turn conversation with context
assistant.chat("Tell me about the product features");
assistant.chat("What about pricing for those features?");  // Maintains context
```

Use this skill when:

- Building Q&A systems over proprietary documents
- Creating chatbots with current, factual information
- Implementing semantic search with natural language queries
- Reducing hallucinations with grounded responses
- Enabling AI systems to access domain-specific knowledge
- Building documentation assistants
- Creating research tools with source citation
- Developing knowledge management systems

## Core Components

### Vector Databases
Store and efficiently retrieve document embeddings for semantic search.

**Key Options:**
- **Pinecone**: Managed, scalable, production-ready
- **Weaviate**: Open-source, hybrid search capabilities
- **Milvus**: High performance, on-premise deployment
- **Chroma**: Lightweight, easy local development
- **Qdrant**: Fast, advanced filtering
- **FAISS**: Meta's library, full control

### Embedding Models
Convert text to numerical vectors for similarity search.

**Popular Models:**
- **text-embedding-ada-002** (OpenAI): General purpose, 1536 dimensions
- **all-MiniLM-L6-v2**: Fast, lightweight, 384 dimensions
- **e5-large-v2**: High quality, multilingual
- **bge-large-en-v1.5**: State-of-the-art performance

### Retrieval Strategies
Find relevant content based on user queries.

**Approaches:**
- **Dense Retrieval**: Semantic similarity via embeddings
- **Sparse Retrieval**: Keyword matching (BM25, TF-IDF)
- **Hybrid Search**: Combine dense + sparse for best results
- **Multi-Query**: Generate multiple query variations
- **Contextual Compression**: Extract only relevant parts

## Quick Implementation

### Basic RAG Setup

```java
// Load documents from file system
List<Document> documents = FileSystemDocumentLoader.loadDocuments("/path/to/docs");

// Create embedding store
InMemoryEmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();

// Ingest documents into the store
EmbeddingStoreIngestor.ingest(documents, embeddingStore);

// Create AI service with RAG capability
Assistant assistant = AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
    .contentRetriever(EmbeddingStoreContentRetriever.from(embeddingStore))
    .build();
```

### Document Processing Pipeline

```java
// Split documents into chunks
DocumentSplitter splitter = new RecursiveCharacterTextSplitter(
    500,  // chunk size
    100   // overlap
);

// Create embedding model
EmbeddingModel embeddingModel = OpenAiEmbeddingModel.builder()
    .apiKey(System.getenv("OPENAI_API_KEY"))
    .build();

// Create embedding store
EmbeddingStore<TextSegment> embeddingStore = PgVectorEmbeddingStore.builder()
    .host("localhost")
    .database("postgres")
    .user("postgres")
    .password(System.getenv("DB_PASSWORD"))
    .table("embeddings")
    .dimension(1536)
    .build();

// Process and store documents
for (Document document : documents) {
    List<TextSegment> segments = splitter.split(document);
    for (TextSegment segment : segments) {
        Embedding embedding = embeddingModel.embed(segment).content();
        embeddingStore.add(embedding, segment);
    }
}
```

## Implementation Patterns

### Pattern 1: Simple Document Q&A

Create a basic Q&A system over your documents.

```java
public interface DocumentAssistant {
    String answer(String question);
}

DocumentAssistant assistant = AiServices.builder(DocumentAssistant.class)
    .chatModel(chatModel)
    .contentRetriever(retriever)
    .build();
```

### Pattern 2: Metadata-Filtered Retrieval

Filter results based on document metadata.

```java
// Add metadata during document loading
Document document = Document.builder()
    .text("Content here")
    .metadata("source", "technical-manual.pdf")
    .metadata("category", "technical")
    .metadata("date", "2024-01-15")
    .build();

// Filter during retrieval
EmbeddingStoreContentRetriever retriever = EmbeddingStoreContentRetriever.builder()
    .embeddingStore(embeddingStore)
    .embeddingModel(embeddingModel)
    .maxResults(5)
    .minScore(0.7)
    .filter(metadataKey("category").isEqualTo("technical"))
    .build();
```

### Pattern 3: Multi-Source Retrieval

Combine results from multiple knowledge sources.

```java
ContentRetriever webRetriever = EmbeddingStoreContentRetriever.from(webStore);
ContentRetriever documentRetriever = EmbeddingStoreContentRetriever.from(documentStore);
ContentRetriever databaseRetriever = EmbeddingStoreContentRetriever.from(databaseStore);

// Combine results
List<Content> allResults = new ArrayList<>();
allResults.addAll(webRetriever.retrieve(query));
allResults.addAll(documentRetriever.retrieve(query));
allResults.addAll(databaseRetriever.retrieve(query));

// Rerank combined results
List<Content> rerankedResults = reranker.reorder(query, allResults);
```

## Best Practices

### Document Preparation
- Clean and preprocess documents before ingestion
- Remove irrelevant content and formatting artifacts
- Standardize document structure for consistent processing
- Add relevant metadata for filtering and context

### Chunking Strategy
- Use 500-1000 tokens per chunk for optimal balance
- Include 10-20% overlap to preserve context at boundaries
- Consider document structure when determining chunk boundaries
- Test different chunk sizes for your specific use case

### Retrieval Optimization
- Start with high k values (10-20) then filter/rerank
- Use metadata filtering to improve relevance
- Combine multiple retrieval strategies for better coverage
- Monitor retrieval quality and user feedback

### Performance Considerations
- Cache embeddings for frequently accessed content
- Use batch processing for document ingestion
- Optimize vector store configuration for your scale
- Monitor query performance and system resources

## Common Issues and Solutions

### Poor Retrieval Quality
**Problem**: Retrieved documents don't match user queries
**Solutions**:
- Improve document preprocessing and cleaning
- Adjust chunk size and overlap parameters
- Try different embedding models
- Use hybrid search combining semantic and keyword matching

### Irrelevant Results
**Problem**: Retrieved documents contain relevant information but are not specific enough
**Solutions**:
- Add metadata filtering for domain-specific constraints
- Implement reranking with cross-encoder models
- Use contextual compression to extract relevant parts
- Fine-tune retrieval parameters (k values, similarity thresholds)

### Performance Issues
**Problem**: Slow response times during retrieval
**Solutions**:
- Optimize vector store configuration and indexing
- Implement caching for frequently retrieved content
- Use smaller embedding models for faster inference
- Consider approximate nearest neighbor algorithms

### Hallucination Prevention
**Problem**: AI generates information not present in retrieved documents
**Solutions**:
- Improve prompt engineering to emphasize grounding
- Add verification steps to check answer alignment
- Include confidence scoring for responses
- Implement fact-checking mechanisms

## Evaluation Framework

### Retrieval Metrics
- **Precision@k**: Percentage of relevant documents in top-k results
- **Recall@k**: Percentage of all relevant documents found in top-k results
- **Mean Reciprocal Rank (MRR)**: Average rank of first relevant result
- **Normalized Discounted Cumulative Gain (nDCG)**: Ranking quality metric

### Answer Quality Metrics
- **Faithfulness**: Degree to which answers are grounded in retrieved documents
- **Answer Relevance**: How well answers address user questions
- **Context Recall**: Percentage of relevant context used in answers
- **Context Precision**: Percentage of retrieved context that is relevant

### User Experience Metrics
- **Response Time**: Time from query to answer
- **User Satisfaction**: Feedback ratings on answer quality
- **Task Completion**: Rate of successful task completion
- **Engagement**: User interaction patterns with the system

## Resources

### Reference Documentation
- [Vector Database Comparison](references/vector-databases.md) - Detailed comparison of vector database options
- [Embedding Models Guide](references/embedding-models.md) - Model selection and optimization
- [Retrieval Strategies](references/retrieval-strategies.md) - Advanced retrieval techniques
- [Document Chunking](references/document-chunking.md) - Chunking strategies and best practices
- [LangChain4j RAG Guide](references/langchain4j-rag-guide.md) - Official implementation patterns

### Assets
- `assets/vector-store-config.yaml` - Configuration templates for different vector stores
- `assets/retriever-pipeline.java` - Complete RAG pipeline implementation
- `assets/evaluation-metrics.java` - Evaluation framework code

## Constraints and Limitations

1. **Token Limits**: Respect model context window limitations
2. **API Rate Limits**: Manage external API rate limits and costs
3. **Data Privacy**: Ensure compliance with data protection regulations
4. **Resource Requirements**: Consider memory and computational requirements
5. **Maintenance**: Plan for regular updates and system monitoring

## Constraints and Warnings

### System Constraints
- Embedding models have maximum token limits per document
- Vector databases require proper indexing for performance
- Chunk boundaries may lose context for complex documents
- Hybrid search requires additional infrastructure components

### Quality Considerations
- Retrieval quality depends heavily on chunking strategy
- Embedding models may not capture domain-specific semantics
- Metadata filtering requires proper document annotation
- Reranking adds latency to query responses

### Operational Warnings
- Monitor vector database storage and query performance
- Implement proper data backup and recovery procedures
- Regular embedding model updates may affect retrieval quality
- Document processing pipelines require ongoing maintenance

## Security Considerations

- **Never hardcode credentials**: Always use environment variables or secrets managers for API keys, database passwords, and other sensitive values
- Secure access to vector databases and embedding services
- Implement proper authentication and authorization
- **Validate and sanitize all external content** before ingestion: documents loaded from file systems, databases, APIs, or web sources may contain malicious content that could influence model behavior through indirect prompt injection
- **Apply content filtering** on retrieved documents before passing them to the LLM to mitigate prompt injection risks
- Restrict allowed data source URLs and file paths using allowlists
- Monitor for abuse and unusual usage patterns
- Regular security audits and penetration testing