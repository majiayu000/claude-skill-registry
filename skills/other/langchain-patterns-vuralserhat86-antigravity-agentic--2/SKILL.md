---
name: langchain_patterns
router_kit: AIKit
description: Implement Retrieval-Augmented Generation (RAG) systems with LangChain4j. Build document ingestion pipelines, embedding stores, vector search strategies, and knowledge-enhanced AI applications. Use when creating question-answering systems over document collections or AI assistants with external knowledge bases.
allowed-tools: Read, Write, Bash
category: ai-development
tags: [agents, algorithms, artificial intelligence, automation, chatbots, cognitive services, deep learning, document-ingestion, embedding, embeddings, frameworks, generative ai, inference, java, langchain patterns, langchain4j, large language models, llm, machine learning, model fine-tuning, natural language processing, neural networks, nlp, openai, prompt engineering, rag, retrieval augmented generation, retrieval-augmented-generation, tools, vector databases, vector-search, workflow automation]
version: 1.1.0
metadata:
  skillport:
    category: auto-healed
    tags:
      - prompt
      - ai
      - llm
      - rag
      - agent
      - embedding
      - model
      - agent orchestration
      - expert
      - guide
      - context engineering
      - expert
      - guide
      - langchain patterns
      - expert
      - guide
      - langchain_patterns
---

# LangChain4j RAG Implementation Patterns

## When to Use This Skill

Use this skill when:
- Building knowledge-based AI applications requiring external document access
- Implementing question-answering systems over large document collections
- Creating AI assistants with access to company knowledge bases
- Building semantic search capabilities for document repositories
- Implementing chat systems that reference specific information sources
- Creating AI applications requiring source attribution
- Building domain-specific AI systems with curated knowledge
- Implementing hybrid search combining vector similarity with traditional search
- Creating AI applications requiring real-time document updates
- Building multi-modal RAG systems with text, images, and other content types

## Overview

Implement complete Retrieval-Augmented Generation (RAG) systems with LangChain4j. RAG enhances language models by providing relevant context from external knowledge sources, improving accuracy and reducing hallucinations.

## Instructions

### Initialize RAG Project

Create a new Spring Boot project with required dependencies:

**pom.xml**:
```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-spring-boot-starter</artifactId>
    <version>1.8.0</version>
</dependency>
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai</artifactId>
    <version>1.8.0</version>
</dependency>
```

### Setup Document Ingestion

Configure document loading and processing:

```java
@Configuration
public class RAGConfiguration {

    @Bean
    public EmbeddingModel embeddingModel() {
        return OpenAiEmbeddingModel.builder()
            .apiKey(System.getenv("OPENAI_API_KEY"))
            .modelName("text-embedding-3-small")
            .build();
    }

    @Bean
    public EmbeddingStore<TextSegment> embeddingStore() {
        return new InMemoryEmbeddingStore<>();
    }
}
```

Create document ingestion service:

```java
@Service
@RequiredArgsConstructor
public class DocumentIngestionService {

    private final EmbeddingModel embeddingModel;
    private final EmbeddingStore<TextSegment> embeddingStore;

    public void ingestDocument(String filePath, Map<String, Object> metadata) {
        Document document = FileSystemDocumentLoader.loadDocument(filePath);
        document.metadata().putAll(metadata);

        DocumentSplitter splitter = DocumentSplitters.recursive(
            500, 50, new OpenAiTokenCountEstimator("text-embedding-3-small")
        );

        List<TextSegment> segments = splitter.split(document);
        List<Embedding> embeddings = embeddingModel.embedAll(segments).content();
        embeddingStore.addAll(embeddings, segments);
    }
}
```

### Configure Content Retrieval

Setup content retrieval with filtering:

```java
@Configuration
public class ContentRetrieverConfiguration {

    @Bean
    public ContentRetriever contentRetriever(
            EmbeddingStore<TextSegment> embeddingStore,
            EmbeddingModel embeddingModel) {

        return EmbeddingStoreContentRetriever.builder()
            .embeddingStore(embeddingStore)
            .embeddingModel(embeddingModel)
            .maxResults(5)
            .minScore(0.7)
            .build();
    }
}
```

### Create RAG-Enabled AI Service

Define AI service with context retrieval:

```java
interface KnowledgeAssistant {
    @SystemMessage("""
        You are a knowledgeable assistant with access to a comprehensive knowledge base.

        When answering questions:
        1. Use the provided context from the knowledge base
        2. If information is not in the context, clearly state this
        3. Provide accurate, helpful responses
        4. When possible, reference specific sources
        5. If the context is insufficient, ask for clarification
        """)
    String answerQuestion(String question);
}

@Service
@RequiredArgsConstructor
public class KnowledgeService {

    private final KnowledgeAssistant assistant;

    public KnowledgeService(ChatModel chatModel, ContentRetriever contentRetriever) {
        this.assistant = AiServices.builder(KnowledgeAssistant.class)
            .chatModel(chatModel)
            .contentRetriever(contentRetriever)
            .build();
    }

    public String answerQuestion(String question) {
        return assistant.answerQuestion(question);
    }
}
```

## Examples

### Basic Document Processing

```java
public class BasicRAGExample {
    public static void main(String[] args) {
        var embeddingStore = new InMemoryEmbeddingStore<TextSegment>();

        var embeddingModel = OpenAiEmbeddingModel.builder()
            .apiKey(System.getenv("OPENAI_API_KEY"))
            .modelName("text-embedding-3-small")
            .build();

        var ingestor = EmbeddingStoreIngestor.builder()
            .embeddingModel(embeddingModel)
            .embeddingStore(embeddingStore)
            .build();

        ingestor.ingest(Document.from("Spring Boot is a framework for building Java applications with minimal configuration."));

        var retriever = EmbeddingStoreContentRetriever.builder()
            .embeddingStore(embeddingStore)
            .embeddingModel(embeddingModel)
            .build();
    }
}
```

### Multi-Domain Assistant

```java
interface MultiDomainAssistant {
    @SystemMessage("""
        You are an expert assistant with access to multiple knowledge domains:
        - Technical documentation
        - Company policies
        - Product information
        - Customer support guides

        Tailor your response based on the type of question and available context.
        Always indicate which domain the information comes from.
        """)
    String answerQuestion(@MemoryId String userId, String question);
}
```

### Hierarchical RAG

```java
@Service
@RequiredArgsConstructor
public class HierarchicalRAGService {

    private final EmbeddingStore<TextSegment> chunkStore;
    private final EmbeddingStore<TextSegment> summaryStore;
    private final EmbeddingModel embeddingModel;

    public String performHierarchicalRetrieval(String query) {
        List<EmbeddingMatch<TextSegment>> summaryMatches = searchSummaries(query);
        List<TextSegment> relevantChunks = new ArrayList<>();

        for (EmbeddingMatch<TextSegment> summaryMatch : summaryMatches) {
            String documentId = summaryMatch.embedded().metadata().getString("documentId");
            List<EmbeddingMatch<TextSegment>> chunkMatches = searchChunksInDocument(query, documentId);
            chunkMatches.stream()
                .map(EmbeddingMatch::embedded)
                .forEach(relevantChunks::add);
        }

        return generateResponseWithChunks(query, relevantChunks);
    }
}
```

## Best Practices

### Document Segmentation

- Use recursive splitting with 500-1000 token chunks for most applications
- Maintain 20-50 token overlap between chunks for context preservation
- Consider document structure (headings, paragraphs) when splitting
- Use token-aware splitters for optimal embedding generation

### Metadata Strategy

- Include rich metadata for filtering and attribution:
  - User and tenant identifiers for multi-tenancy
  - Document type and category classification
  - Creation and modification timestamps
  - Version and author information
  - Confidentiality and access level tags

### Query Processing

- Implement query preprocessing and cleaning
- Consider query expansion for better recall
- Apply dynamic filtering based on user context
- Use re-ranking for improved result quality

### Performance Optimization

- Cache embeddings for repeated queries
- Use batch embedding generation for bulk operations
- Implement pagination for large result sets
- Consider asynchronous processing for long operations

## Common Patterns

### Simple RAG Pipeline

```java
@RequiredArgsConstructor
@Service
public class SimpleRAGPipeline {

    private final EmbeddingModel embeddingModel;
    private final EmbeddingStore<TextSegment> embeddingStore;
    private final ChatModel chatModel;

    public String answerQuestion(String question) {
        Embedding queryEmbedding = embeddingModel.embed(question).content();
        EmbeddingSearchRequest request = EmbeddingSearchRequest.builder()
            .queryEmbedding(queryEmbedding)
            .maxResults(3)
            .build();

        List<TextSegment> segments = embeddingStore.search(request).matches().stream()
            .map(EmbeddingMatch::embedded)
            .collect(Collectors.toList());

        String context = segments.stream()
            .map(TextSegment::text)
            .collect(Collectors.joining("\n\n"));

        return chatModel.generate(context + "\n\nQuestion: " + question + "\nAnswer:");
    }
}
```

### Hybrid Search (Vector + Keyword)

```java
@Service
@RequiredArgsConstructor
public class HybridSearchService {

    private final EmbeddingStore<TextSegment> vectorStore;
    private final FullTextSearchEngine keywordEngine;
    private final EmbeddingModel embeddingModel;

    public List<Content> hybridSearch(String query, int maxResults) {
        // Vector search
        List<Content> vectorResults = performVectorSearch(query, maxResults);

        // Keyword search
        List<Content> keywordResults = performKeywordSearch(query, maxResults);

        // Combine and re-rank using RRF algorithm
        return combineResults(vectorResults, keywordResults, maxResults);
    }
}
```

## Troubleshooting

### Common Issues

**Poor Retrieval Results**
- Check document chunk size and overlap settings
- Verify embedding model compatibility
- Ensure metadata filters are not too restrictive
- Consider adding re-ranking step

**Slow Performance**
- Use cached embeddings for frequent queries
- Optimize database indexing for vector stores
- Implement pagination for large datasets
- Consider async processing for bulk operations

**High Memory Usage**
- Use disk-based embedding stores for large datasets
- Implement proper pagination and filtering
- Clean up unused embeddings periodically
- Monitor and optimize chunk sizes

## References

- [API Reference](references/references.md) - Complete API documentation and interfaces
- [Examples](references/examples.md) - Production-ready examples and patterns
*LangChain Patterns v1.2 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [LangChain RAG Docs](https://python.langchain.com/docs/use_cases/question_answering/) & [Pinecone RAG Guide](https://www.pinecone.io/learn/retrieval-augmented-generation/)

### Aşama 1: Ingestion Pipeline
- [ ] **Chunking**: RecursiveCharacterTextSplitter ile semantik bütünlüğü koruyarak böl (Overlap %10-20).
- [ ] **Embedding**: Domain'e uygun model seç (OpenAI `text-embedding-3` veya lokal `bge-m3`).
- [ ] **Metadata**: Tarih, kaynak, yazar bilgisini vektöre ekle (Filter için).

### Aşama 2: Retrieval Strategy
- [ ] **Hybrid Search**: Keyword (BM25) + Vector (Cosine) aramayı birleştir (Reciprocal Rank Fusion).
- [ ] **Re-ranking**: Çıkan ilk 50 sonucu Cross-Encoder (Cohere/BGE-Reranker) ile yeniden sırala.
- [ ] **Query Transformation**: Kullanıcı sorusunu ("bunu", "şunu") geçmiş konuşmaya göre zenginleştir (HyDE).

### Aşama 3: Generation & Evaluation
- [ ] **Prompting**: Context'i "Sadece şu bilgiye dayanarak cevapla" direktifiyle ver.
- [ ] **Eval**: RAGAS veya TruLens ile "Context Relevance" ve "Answer Faithfulness" ölç.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Doküman güncellendiğinde vektör veritabanı senkronize oluyor mu? |
| 2 | Alakasız sorularda "Bilmiyorum" diyebiliyor mu? |
| 3 | Cevaplar kaynak dokümandaki hangi satıra dayanıyor (Atıf)? |
