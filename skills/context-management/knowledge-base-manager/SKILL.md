---
name: Knowledge Base Manager
description: Design, build, and maintain comprehensive knowledge bases. Bridges document-based (RAG) and entity-based (graph) knowledge systems. Use when building knowledge-intensive applications, managing organizational knowledge, or creating intelligent information systems.
version: 1.0.0
---

# Knowledge Base Manager

Build and maintain high-quality knowledge bases for AI systems and human consumption.

## Core Principle

**Knowledge Base = Structured Information + Quality Curation + Accessibility**

A knowledge base is not just a data dump—it's curated, validated, versioned information designed to answer questions and enable reasoning.

---

## When to Use Knowledge Bases

### Use Knowledge Bases When:

- ✅ Need to answer factual questions consistently
- ✅ Information changes frequently and needs version control
- ✅ Multiple sources need to be unified and reconciled
- ✅ Provenance and citation tracking is critical
- ✅ Building AI systems that need grounded, verifiable information
- ✅ Organizational knowledge needs to be preserved and searchable
- ✅ Complex domain with interconnected concepts

### Don't Use Knowledge Bases When:

- ❌ Static documentation is sufficient (use docs + search)
- ❌ No one will maintain/update it (knowledge rot guaranteed)
- ❌ Simple FAQ covers all questions (<50 items)
- ❌ Information doesn't change (static site faster/cheaper)
- ❌ Team lacks resources for curation

---

## Knowledge Base Types: Decision Framework

### 1. Document-Based Knowledge Base (RAG)

**What it is:** Collection of documents, chunked and embedded for semantic search

**Best for:**

- Technical documentation
- Support articles, FAQs
- Policy documents
- Research papers
- Blog content
- User manuals

**Strengths:**

- Easy to add new documents
- Preserves full context
- Natural for text-heavy content

**Weaknesses:**

- Hard to query relationships ("Who works where?")
- Duplicate information across documents
- Difficult to keep facts consistent

**Use:** `rag-implementer` skill + `vector-database-mcp`

---

### 2. Entity-Based Knowledge Base (Knowledge Graph)

**What it is:** Network of entities (people, places, things) connected by relationships

**Best for:**

- Organizational charts
- Product catalogs with relationships
- Social networks
- Recommendation systems
- Fraud detection
- Supply chain tracking

**Strengths:**

- Excellent for "how are X and Y related?" queries
- Consistent facts (one source of truth)
- Powerful traversal ("friends of friends")

**Weaknesses:**

- Upfront modeling required (ontology design)
- Harder to add unstructured information
- Learning curve for graph queries

**Use:** `knowledge-graph-builder` skill + `graph-database-mcp`

---

### 3. Hybrid Knowledge Base (RAG + Graph)

**What it is:** Documents for unstructured knowledge + Graph for structured entities/relationships

**Best for:**

- Enterprise knowledge management
- Research with citations and relationships
- Medical systems (documents + patient/drug relationships)
- Legal systems (cases + precedents + entities)
- E-commerce (products + specs + relationships)

**Strengths:**

- Best of both worlds
- Flexible for different knowledge types
- Rich querying capabilities

**Weaknesses:**

- Most complex to build and maintain
- Requires expertise in both RAG and graphs
- Higher infrastructure costs

**Use:** Both `rag-implementer` + `knowledge-graph-builder` skills

---

## Decision Tree: Which KB Type?

```
What kind of knowledge do you have?

├─ Mostly unstructured text (docs, articles, content)?
│  └─ Document-Based KB (RAG)
│     Use: rag-implementer skill
│
├─ Mostly structured entities with relationships?
│  └─ Entity-Based KB (Graph)
│     Use: knowledge-graph-builder skill
│
└─ Mix of both?
   └─ Hybrid KB (RAG + Graph)
      Use: Both skills + This skill for integration
```

---

## 6-Phase Knowledge Base Implementation

### Phase 1: Knowledge Audit & Architecture

**Goal**: Understand what knowledge exists and how to structure it

**Actions**:

1. **Inventory existing knowledge sources**
   - Internal: databases, documents, wikis, Slack, emails
   - External: public data, APIs, third-party sources
   - Tribal: SME interviews, recorded conversations

2. **Classify knowledge types**
   - **Factual**: Verifiable facts ("Product X costs $50")
   - **Procedural**: How-to knowledge ("How to deploy")
   - **Conceptual**: Definitions and explanations
   - **Relationship**: Connections between entities

3. **Choose KB architecture**
   - Document-based? Entity-based? Hybrid?
   - Decision: Use framework above

4. **Define knowledge schema**
   - For documents: metadata fields (source, date, author, category)
   - For entities: ontology (entity types, relationship types, properties)

**Validation**:

- [ ] All knowledge sources inventoried and prioritized
- [ ] KB architecture chosen and justified
- [ ] Schema defined and validated with users
- [ ] Success metrics established

---

### Phase 2: Knowledge Curation & Ingestion

**Goal**: Transform raw information into high-quality knowledge

**Actions**:

1. **Extract knowledge from sources**
   - Automated: scraping, API ingestion, file parsing
   - Manual: expert input, annotation, validation

2. **Clean and normalize**
   - Remove duplicates
   - Standardize formats
   - Fix inconsistencies
   - Enrich with metadata

3. **Structure knowledge**
   - For documents: chunk intelligently (semantic boundaries)
   - For entities: extract entities, relationships, properties

4. **Add provenance**
   - Source URL or reference
   - Last updated timestamp
   - Author/contributor
   - Confidence score (if applicable)

**Curation Best Practices**:

- **Single Source of Truth**: One canonical answer per question
- **Deduplication**: Merge similar knowledge entries
- **Conflict Resolution**: When sources disagree, establish priority rules
- **Metadata Richness**: More metadata = better filtering and search

**Validation**:

- [ ] Knowledge extracted and structured
- [ ] Quality metrics above threshold (accuracy >95%)
- [ ] Provenance tracked for all entries
- [ ] Sample queries return relevant results

---

### Phase 3: Storage & Retrieval Setup

**Goal**: Implement technical infrastructure for knowledge access

**Architecture Patterns**:

**For Document-Based KB:**

```typescript
// Vector database for semantic search
interface DocumentKB {
  store: 'Pinecone' | 'Weaviate' | 'pgvector'
  chunks: {
    content: string
    embedding: number[]
    metadata: {
      source: string
      title: string
      updated_at: string
      category: string
    }
  }[]
}
```

**For Entity-Based KB:**

```typescript
// Graph database for relationship queries
interface EntityKB {
  store: 'Neo4j' | 'ArangoDB'
  nodes: {
    id: string
    type: 'Person' | 'Organization' | 'Product' | 'Concept'
    properties: Record<string, any>
  }[]
  relationships: {
    from: string
    to: string
    type: string
    properties: Record<string, any>
  }[]
}
```

**For Hybrid KB:**

```typescript
// Both vector DB + graph DB
interface HybridKB {
  vectorDB: DocumentKB
  graphDB: EntityKB
  linker: {
    // Links documents to entities mentioned in them
    linkDocumentToEntities(docId: string): string[]
    // Links entities to documents that mention them
    linkEntityToDocuments(entityId: string): string[]
  }
}
```

**Actions**:

1. **Choose database(s)**
   - Document: Pinecone, Weaviate, pgvector
   - Entity: Neo4j, ArangoDB
   - Hybrid: Both + linking layer

2. **Implement search/query layer**
   - Vector similarity search (for documents)
   - Graph traversal (for entities)
   - Hybrid queries (combining both)

3. **Add caching and optimization**
   - Cache frequent queries
   - Optimize for common access patterns

**Validation**:

- [ ] Database deployed and accessible
- [ ] Search/query functionality working
- [ ] Performance meets requirements (<100ms for most queries)

---

### Phase 4: Quality Control & Validation

**Goal**: Ensure knowledge base accuracy and reliability

**Quality Metrics**:

1. **Accuracy**: % of correct answers to test questions
2. **Coverage**: % of user questions answerable
3. **Freshness**: Average age of knowledge
4. **Consistency**: % of conflicts/contradictions
5. **Source Quality**: % from authoritative sources

**Validation Strategies**:

**1. Test Question Sets**
Create 100+ test questions with known correct answers:

```typescript
interface TestQuestion {
  question: string
  expected_answer: string
  category: string
  difficulty: 'easy' | 'medium' | 'hard'
}
```

**2. Human Review**

- Sample random knowledge entries
- Subject matter expert validation
- User feedback loops

**3. Automated Checks**

- **Duplicate Detection**: Find near-identical entries
- **Conflict Detection**: Find contradictory facts
- **Staleness Detection**: Flag outdated information
- **Citation Validation**: Verify sources still exist

**4. Continuous Monitoring**

```typescript
interface KBHealthMetrics {
  accuracy_score: number // 0-100
  coverage_score: number // % questions answered
  freshness_score: number // avg days since update
  consistency_score: number // % no conflicts
  user_satisfaction: number // feedback rating
}
```

**Actions**:

1. Run test question validation (target: >90% accuracy)
2. Conduct human review (sample 10% of entries)
3. Fix detected issues (duplicates, conflicts, staleness)
4. Establish monitoring dashboards

**Validation**:

- [ ] Accuracy >90% on test questions
- [ ] Coverage >80% of user questions
- [ ] <5% conflicting information
- [ ] Monitoring dashboard operational

---

### Phase 5: Versioning & Evolution

**Goal**: Track knowledge changes over time and enable rollback

**Why Versioning Matters**:

- Knowledge changes (facts update, policies change)
- Need audit trail (who changed what when)
- Rollback capability (undo bad updates)
- Historical queries ("What was policy on X in 2023?")

**Versioning Strategies**:

**1. Snapshot Versioning**

```typescript
interface KnowledgeEntry {
  id: string
  content: string
  version: number
  created_at: string
  updated_at: string
  updated_by: string
  changelog: string
  previous_version?: string // ID of prior version
}
```

**2. Event Sourcing**

```typescript
interface KnowledgeEvent {
  event_id: string
  entity_id: string
  event_type: 'created' | 'updated' | 'deleted'
  timestamp: string
  changes: {
    field: string
    old_value: any
    new_value: any
  }[]
  author: string
}
```

**3. Git-Style Versioning**

- Treat knowledge like code
- Commit-based changes
- Branch for experimental knowledge
- Merge when validated

**Actions**:

1. Implement version tracking
2. Add changelog for all updates
3. Create rollback mechanism
4. Build version comparison tools

**Validation**:

- [ ] All changes tracked with versions
- [ ] Rollback tested and working
- [ ] Historical queries supported
- [ ] Audit trail complete

---

### Phase 6: Maintenance & Governance

**Goal**: Keep knowledge base healthy long-term

**Maintenance Tasks**:

**Daily:**

- Monitor for errors and failures
- Review user feedback
- Address urgent corrections

**Weekly:**

- Review new content submissions
- Update time-sensitive knowledge
- Run automated quality checks

**Monthly:**

- Audit knowledge freshness
- Review and resolve conflicts
- Analyze usage patterns
- Update stale content

**Quarterly:**

- Comprehensive quality audit
- Schema/ontology review
- Performance optimization
- User satisfaction survey

**Governance Framework**:

**1. Roles & Responsibilities**

- **Knowledge Owners**: Domain experts responsible for content
- **Curators**: Review and approve changes
- **Contributors**: Submit new knowledge
- **Consumers**: Use knowledge and provide feedback

**2. Change Process**

```
Submit → Review → Approve → Publish → Monitor
```

**3. Quality Standards**

- Minimum source quality requirements
- Citation requirements
- Update frequency requirements
- Conflict resolution process

**Actions**:

1. Establish maintenance schedule
2. Assign roles and responsibilities
3. Create governance documentation
4. Train team on processes

**Validation**:

- [ ] Maintenance schedule in place
- [ ] Governance documented and communicated
- [ ] Team trained on processes
- [ ] Quality trending upward

---

## Knowledge Base Anti-Patterns

### ❌ Anti-Pattern 1: Data Dump Without Curation

**Problem**: Ingesting everything without quality filtering

**Impact**: Low signal-to-noise ratio, poor search results, user frustration

**Solution**: Curate before ingesting. Quality > Quantity

---

### ❌ Anti-Pattern 2: No Version Control

**Problem**: Knowledge changes but no history tracked

**Impact**: Can't audit changes, can't rollback errors, no accountability

**Solution**: Implement versioning from Phase 5

---

### ❌ Anti-Pattern 3: Stale Knowledge

**Problem**: Knowledge base outdated but no one knows

**Impact**: AI systems hallucinate using old facts, users get wrong answers

**Solution**: Freshness monitoring + scheduled updates

---

### ❌ Anti-Pattern 4: Duplicate Information

**Problem**: Same fact in multiple places, becomes inconsistent

**Impact**: Conflicting answers, confused users

**Solution**: Deduplication + single source of truth

---

### ❌ Anti-Pattern 5: No Provenance

**Problem**: Knowledge without source citations

**Impact**: Can't verify accuracy, can't trace errors

**Solution**: Always track source + timestamp + author

---

## Integration with Other Skills

### With rag-implementer

- Use for document-based portion of hybrid KB
- Follow RAG implementation phases
- Integrate vector search with KB queries

### With knowledge-graph-builder

- Use for entity-based portion of hybrid KB
- Follow graph design patterns
- Integrate graph traversal with KB queries

### With data-engineer

- For ETL pipelines (extract, transform, load knowledge)
- For data quality monitoring
- For performance optimization

### With quality-auditor

- For automated quality checks
- For testing and validation
- For continuous monitoring

### With technical-writer

- For knowledge documentation
- For user guides on KB usage
- For governance documentation

---

## Tools & Technologies

### Document-Based KB Stack

- **Vector DB**: Pinecone, Weaviate, pgvector
- **Embeddings**: OpenAI, Cohere, custom
- **Search**: Semantic + keyword hybrid

### Entity-Based KB Stack

- **Graph DB**: Neo4j, ArangoDB
- **Query**: Cypher, AQL
- **Visualization**: Neo4j Bloom, Gephi

### Curation Tools

- **Deduplication**: Custom algorithms, fuzzy matching
- **Conflict Detection**: Rule-based, ML-based
- **Validation**: Test question sets, human review

### Monitoring

- **Metrics**: Custom dashboard (Grafana)
- **Logging**: Structured logging of queries/updates
- **Alerts**: Freshness, accuracy, error rate alerts

---

## Success Metrics

### Knowledge Quality

- **Accuracy**: >90% on test questions
- **Coverage**: >80% of user questions answered
- **Freshness**: <30 days average age
- **Consistency**: <5% conflicting information

### User Satisfaction

- **Relevance**: >85% query results rated relevant
- **Usefulness**: >80% users find KB valuable
- **Speed**: <100ms median query time

### Operational Health

- **Uptime**: >99.9%
- **Update frequency**: Weekly minimum
- **Team engagement**: Regular contributions

---

## Common Pitfalls & Solutions

### Pitfall 1: "Build it and they will come"

**Problem**: No user validation, KB doesn't meet needs

**Solution**: Start with user research, validate continuously

### Pitfall 2: Perfectionism

**Problem**: Waiting to launch until KB is "perfect"

**Solution**: Launch with 80% coverage, iterate based on usage

### Pitfall 3: Over-engineering

**Problem**: Building complex hybrid system when simple docs would work

**Solution**: Start simple, add complexity only when needed

### Pitfall 4: Maintenance neglect

**Problem**: Build once, never update

**Solution**: Establish maintenance schedule from day 1

---

## Quick Start Checklist

**Before you start:**

- [ ] Read this entire skill
- [ ] Review `rag-implementer` if using document KB
- [ ] Review `knowledge-graph-builder` if using entity KB
- [ ] Have clear use case and success metrics

**Phase 1 - Architecture (Week 1):**

- [ ] Inventory knowledge sources
- [ ] Choose KB type (document/entity/hybrid)
- [ ] Define schema/ontology
- [ ] Set up infrastructure

**Phase 2 - Initial Build (Week 2-3):**

- [ ] Ingest and curate initial knowledge
- [ ] Implement search/query functionality
- [ ] Create test question set
- [ ] Validate with users

**Phase 3 - Iterate (Ongoing):**

- [ ] Add more knowledge based on usage
- [ ] Monitor quality metrics
- [ ] Fix issues as discovered
- [ ] Establish maintenance cadence

---

## Related Resources

- **Skills**: `rag-implementer`, `knowledge-graph-builder`, `data-engineer`, `quality-auditor`
- **MCPs**: `vector-database-mcp`, `graph-database-mcp`, `knowledge-base-mcp`, `semantic-search-mcp`
- **Patterns**: `STANDARDS/architecture-patterns/rag-pattern.md`, `knowledge-base-pattern.md` (coming soon)
- **Integrations**: `INTEGRATIONS/pinecone/`, `INTEGRATIONS/graph-databases/neo4j/`

---

## Further Reading

- [The Knowledge Graph Cookbook](https://neo4j.com/knowledge-graph-book/)
- [Building Knowledge Bases with LLMs](https://www.anthropic.com/knowledge-bases)
- [RAG: Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Knowledge Management Best Practices](https://www.kmworld.com)

---

**Remember**: A knowledge base is only as good as its curation. Invest in quality from day 1, establish maintenance processes, and iterate based on user feedback. The goal is not to have all knowledge—it's to have the _right_ knowledge, well-organized, and easily accessible.
