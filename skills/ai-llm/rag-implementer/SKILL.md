---
name: RAG Implementer
description: Implement retrieval-augmented generation systems. Use when building knowledge-intensive applications, document search, Q&A systems, or need to ground LLM responses in external data. Covers embedding strategy, vector stores, retrieval pipelines, and evaluation.
version: 1.0.0
---

# RAG Implementer

Build production-ready retrieval-augmented generation systems.

## Core Principle

**RAG = Retrieval + Context Assembly + Generation**

Use RAG when you need LLMs to access fresh, domain-specific, or proprietary knowledge that wasn't in their training data.

---

## ⚠️ Prerequisites & Cost Reality Check

### STOP: Have You Validated the Need for RAG?

**Before implementing RAG, confirm:**

- [ ] **Problem validated** - Completed `product-strategist` Phase 1 (problem discovery)
- [ ] **Users need AI search** - Tested with simpler alternatives (see below)
- [ ] **ROI justified** - Calculated cost vs benefit of RAG vs alternatives

### Try These FIRST (Before RAG)

RAG is powerful but expensive. Try cheaper alternatives first:

**1. FAQ Page / Documentation (1 day, $0)**

- Create well-organized FAQ or docs
- Add search with Cmd+F
- **Works for:** <50 common questions, static content
- **Test:** Do users find answers? If yes, stop here.

**2. Simple Keyword Search (2-3 days, $0-20/month)**

- Use Algolia, Typesense, or PostgreSQL full-text search
- Good enough for 80% of use cases
- **Works for:** <100k documents, keyword matching sufficient
- **Test:** Do users get relevant results? If yes, stop here.

**3. Manual Curation (Concierge MVP) (1 week, $0)**

- Manually answer user questions
- Build FAQ from common questions
- **Works for:** <100 users, validating if users want AI
- **Test:** Do users value your answers enough to pay? If yes, consider RAG.

**4. Simple Semantic Search (1 week, $30-50/month)**

- Use OpenAI embeddings + Postgres pgvector
- Skip complex retrieval, re-ranking, etc.
- **Works for:** <50k documents, basic semantic search
- **Test:** Are embeddings better than keyword search? If no, stop here.

### Cost Reality Check

**Naive RAG (Prototype):**

- **Time:** 1-2 weeks
- **Cost:** $50-150/month (vector DB + embeddings + API calls)
- **When:** Prototype, <10k documents, proof of concept

**Advanced RAG (Production):**

- **Time:** 3-4 weeks
- **Cost:** $200-500/month (hybrid search, re-ranking, monitoring)
- **When:** Production, 10k-1M documents, validated demand

**Modular RAG (Enterprise):**

- **Time:** 6-8 weeks
- **Cost:** $500-2000+/month (multiple KBs, specialized modules)
- **When:** Enterprise, 1M+ documents, mission-critical

### Decision Tree: Do You Really Need RAG?

```
Do users need to search your content?
│
├─ No → Don't build RAG ❌
│
└─ Yes
   ├─ <50 items? → FAQ page ✅ ($0)
   │
   └─ >50 items?
      ├─ Keyword search enough? → Use Algolia ✅ ($0-20/mo)
      │
      └─ Need semantic understanding?
         ├─ <50k docs? → Simple semantic (pgvector) ✅ ($30/mo)
         │
         └─ >50k docs?
            ├─ Validated with users? → Build RAG ✅
            └─ Not validated? → Test with Concierge MVP first ⚠️
```

### Validation Checklist

Only proceed with RAG implementation if:

- [ ] Tested simpler alternatives (FAQ, keyword search, manual curation)
- [ ] Users confirmed they need AI-powered search (not just you think they do)
- [ ] Calculated ROI: cost of RAG < value users get
- [ ] Have >50k documents OR complex semantic search requirements
- [ ] Budget: $200-500/month for infrastructure
- [ ] Time: 3-4 weeks for production implementation

**If any checkbox is unchecked:** Go back to `product-strategist` or `mvp-builder` skills to validate first.

**See also:** `PLAYBOOKS/validation-first-development.md` for step-by-step validation process.

---

## 8-Phase RAG Implementation

### Phase 1: Knowledge Base Design

**Goal**: Create well-structured knowledge foundation

**Actions**:

- Map data sources (internal: docs, databases, APIs / external: web, feeds)
- Filter noise, select authoritative content (prevent "data dump fallacy")
- Define chunking strategy: semantic chunking based on structure
- Add metadata: tags, timestamps, source identifiers, categories

**Validation**:

- [ ] All data sources catalogued and prioritized
- [ ] Data quality assessed (accuracy, completeness, freshness)
- [ ] Chunking strategy tested with sample documents
- [ ] Metadata schema validated for search effectiveness

**Common Chunking Strategies**:

- Fixed-size: 500-1000 tokens, 50-100 token overlap
- Semantic: By paragraph, section headers, or topic boundaries
- Recursive: Split by structure (markdown headers, code blocks)

---

### Phase 2: Embedding Strategy

**Goal**: Choose optimal embedding approach for semantic understanding

**Actions**:

- Select embedding model: `text-embedding-3-large` (1536 dim) for general, domain-specific for specialized
- Plan multi-modal needs (text, code, images, tables)
- Decide on fine-tuning: use domain data if general embeddings underperform
- Establish similarity benchmarks

**Validation**:

- [ ] Embedding model benchmarked on domain data
- [ ] Retrieval accuracy tested with known query-document pairs
- [ ] Storage and compute costs validated

**Model Selection**:

- General: OpenAI `text-embedding-3-large`, `text-embedding-3-small`
- Code: `code-search-babbage-code-001` or StarEncoder
- Multilingual: `multilingual-e5-large`

---

### Phase 3: Vector Store Architecture

**Goal**: Implement scalable vector database

**Actions**:

- Choose vector DB (Pinecone, Weaviate, Qdrant, Chroma, pgvector)
- Configure index: HNSW for speed, IVF for scale
- Plan scalability: data growth and query volume
- Implement backup, recovery, security

**Validation**:

- [ ] Vector store benchmarked under expected load
- [ ] Index optimized for retrieval speed and accuracy
- [ ] Backup and recovery tested
- [ ] Security controls implemented

**Vector DB Decision**:

- Managed cloud → Pinecone
- Self-hosted, feature-rich → Weaviate
- Lightweight, local → Chroma
- Cost-conscious → pgvector (Postgres extension)
- High-performance → Qdrant

---

### Phase 4: Retrieval Pipeline

**Goal**: Build sophisticated retrieval beyond simple similarity search

**Actions**:

- Implement hybrid retrieval: semantic search + keyword (BM25)
- Add query enhancement: expansion, reformulation, multi-query
- Apply contextual filtering: metadata, temporal constraints, relevance ranking
- Design for query types: factual (precision), analytical (breadth), creative (diversity)
- Handle edge cases: no relevant results found

**Advanced Techniques**:

- **Re-ranking**: Use cross-encoder after initial retrieval (e.g., `cross-encoder/ms-marco-MiniLM-L-12-v2`)
- **Query routing**: Route different query types to specialized strategies
- **Ensemble methods**: Combine multiple retrieval approaches
- **Adaptive retrieval**: Adjust top-k based on query complexity

**Validation**:

- [ ] Retrieval accuracy tested across diverse query types
- [ ] Hybrid retrieval outperforms single-method baselines
- [ ] Query latency meets requirements (<500ms ideal)
- [ ] Edge cases and fallbacks tested

---

### Phase 5: Context Assembly

**Goal**: Transform retrieved chunks into optimal LLM context

**Actions**:

- Rank and select: prioritize by relevance score, recency, source authority
- Synthesize: merge related chunks, avoid redundancy
- Compress: use LLMLingua or similar for token optimization
- Mitigate "lost in the middle": place critical info at start/end
- Adapt dynamically: adjust context based on conversation history

**Context Engineering Integration**:

- Blend RAG results with system instructions and user prompts
- Maintain conversation coherence across multi-turn interactions
- Implement context persistence for follow-up queries
- Balance context size vs. information density

**Validation**:

- [ ] Context relevance validated against human judgments
- [ ] Token optimization maintains accuracy
- [ ] Multi-turn conversations maintain coherence
- [ ] Assembly latency <200ms

---

### Phase 6: Evaluation & Metrics

**Goal**: Measure RAG system performance comprehensively

**Retrieval Quality**:

- **Precision@K**: Fraction of top-K results that are relevant
- **Recall@K**: Fraction of relevant docs in top-K
- **MRR (Mean Reciprocal Rank)**: Average rank of first relevant result
- **NDCG**: Ranking quality with graded relevance

**Generation Quality**:

- **Faithfulness**: Generated content accuracy vs. sources
- **Answer Relevance**: Response relevance to query
- **Context Utilization**: How effectively LLM uses retrieved info
- **Hallucination Rate**: Frequency of unsupported claims

**System Performance**:

- **End-to-End Latency**: Query to answer (<3 seconds target)
- **Retrieval Latency**: Time to retrieve and rank (<500ms)
- **Token Efficiency**: Information density per token
- **Cost Per Query**: Combined retrieval + generation costs

**Validation**:

- [ ] Baseline metrics established
- [ ] A/B testing framework for config comparisons
- [ ] Automated evaluation pipeline deployed
- [ ] Human evaluation protocols for ground truth

---

### Phase 7: Production Deployment

**Goal**: Deploy with enterprise-grade reliability and security

**Deployment**:

- Containerize with Docker/Kubernetes
- Implement load balancing across RAG instances
- Add caching for frequent queries
- Graceful degradation: fallback to base model on component failure

**Security**:

- Role-based access controls for knowledge base
- Data masking and PII protection
- Audit logging for compliance
- Prompt injection defense

**Monitoring**:

- Real-time metrics dashboard (latency, cost, accuracy)
- Query analysis for patterns and failure modes
- Cost tracking and optimization alerts
- Performance profiling for bottlenecks

**Validation**:

- [ ] Production handles expected traffic
- [ ] Security prevents unauthorized access
- [ ] Monitoring provides actionable insights
- [ ] Incident response procedures tested

---

### Phase 8: Continuous Improvement

**Goal**: Establish processes for ongoing enhancement

**Data Pipeline**:

- Automated knowledge base updates (real-time or scheduled)
- Quality monitoring: detect data drift and degradation
- Source diversification: add new data sources
- Feedback integration: user corrections and preferences

**Model Evolution**:

- Evaluate and migrate to improved embeddings
- Fine-tune on domain data regularly
- Upgrade architecture: Naive → Advanced → Modular RAG
- Expand multi-modal support (images, audio, video)

**Optimization**:

- Analyze query patterns, optimize for common needs
- Improve cache hit rates
- Tune vector indices regularly
- Balance performance vs. costs

**Validation**:

- [ ] Automated improvement pipelines functioning
- [ ] Performance trends show improvement
- [ ] User satisfaction increasing
- [ ] System adapts to changing needs

## Key RAG Principles

### 1. Relevance Over Volume

- Quality curation > massive datasets
- Remove outdated/low-quality content continuously
- Prioritize most relevant info to prevent "lost in the middle"

### 2. Semantic Understanding

- Use embeddings for true semantic matching, not just keywords
- Recognize query intent (factual, analytical, creative)
- Adapt retrieval strategy based on context

### 3. Multi-Modal Intelligence

- Handle text, images, code, tables, structured data
- Enable cross-modal retrieval (text query → image results)
- Preserve document structure and formatting

### 4. Temporal Awareness

- Prioritize recent info for time-sensitive topics
- Maintain historical access when relevant
- Integrate real-time data feeds for dynamic domains

### 5. Transparency & Trust

- Always provide source citations
- Indicate confidence levels
- Explain why specific information was selected

## Standard RAG Response Format

```json
{
  "answer": "Generated response incorporating retrieved information",
  "sources": [
    {
      "content": "Retrieved text chunk",
      "source": "Document/URL identifier",
      "relevance_score": 0.95,
      "chunk_id": "unique_identifier"
    }
  ],
  "confidence": 0.87,
  "retrieval_metadata": {
    "chunks_retrieved": 5,
    "retrieval_time_ms": 150,
    "generation_time_ms": 800
  }
}
```

## Critical Success Rules

**Non-Negotiable**:

1. ✅ Source attribution for every response
2. ✅ Validate generated content against sources (prevent hallucination)
3. ✅ Filter sensitive data before retrieval
4. ✅ Respond within latency thresholds (<3 seconds)
5. ✅ Monitor and optimize costs continuously
6. ✅ Comply with security policies
7. ✅ Graceful degradation on failures
8. ✅ Comprehensive testing before production

**Quality Gates**:

- Before Production: >85% accuracy on evaluation dataset
- Ongoing: User satisfaction >4.0/5.0
- Performance: 95th percentile <5 seconds
- Reliability: 99.5% uptime
- Cost: Within 10% of budget

## Advanced Patterns

### Modular RAG Architecture

- **Search Module**: Query understanding and reformulation
- **Memory Module**: Long-term conversation persistence
- **Routing Module**: Query routing to specialized knowledge bases
- **Predict Module**: Anticipatory pre-loading based on context

### Hybrid RAG + Fine-tuning

- RAG for dynamic, frequently changing knowledge
- Fine-tuning for domain-specific reasoning patterns
- Combine strengths for maximum effectiveness

## Related Resources

**Related Skills**:

- `multi-agent-architect` - For complex RAG orchestration
- `knowledge-graph-builder` - For structured knowledge integration
- `performance-optimizer` - For RAG system optimization

**Related Patterns**:

- `META/DECISION-FRAMEWORK.md` - Vector DB and embedding selection
- `STANDARDS/architecture-patterns/rag-pattern.md` - RAG architecture details (when created)

**Related Playbooks**:

- `PLAYBOOKS/deploy-rag-system.md` - RAG deployment procedure (when created)
