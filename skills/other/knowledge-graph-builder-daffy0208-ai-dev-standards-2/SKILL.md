---
name: Knowledge Graph Builder
description: Design and build knowledge graphs. Use when modeling complex relationships, building semantic search, or creating knowledge bases. Covers schema design, entity relationships, and graph database selection.
version: 1.0.0
---

# Knowledge Graph Builder

Build structured knowledge graphs for enhanced AI system performance through relational knowledge.

## Core Principle

**Knowledge graphs make implicit relationships explicit**, enabling AI systems to reason about connections, verify facts, and avoid hallucinations.

## When to Use Knowledge Graphs

### Use Knowledge Graphs When:

- ✅ Complex entity relationships are central to your domain
- ✅ Need to verify AI-generated facts against structured knowledge
- ✅ Semantic search and relationship traversal required
- ✅ Data has rich interconnections (people, organizations, products)
- ✅ Need to answer "how are X and Y related?" queries
- ✅ Building recommendation systems based on relationships
- ✅ Fraud detection or pattern recognition across connected data

### Don't Use Knowledge Graphs When:

- ❌ Simple tabular data (use relational DB)
- ❌ Purely document-based search (use RAG with vector DB)
- ❌ No significant relationships between entities
- ❌ Team lacks graph modeling expertise
- ❌ Read-heavy workload with no traversal (use traditional DB)

---

## 6-Phase Knowledge Graph Implementation

### Phase 1: Ontology Design

**Goal**: Define entities, relationships, and properties for your domain

**Entity Types** (Nodes):

- Person, Organization, Location, Product, Concept, Event, Document

**Relationship Types** (Edges):

- Hierarchical: IS_A, PART_OF, REPORTS_TO
- Associative: WORKS_FOR, LOCATED_IN, AUTHORED_BY, RELATED_TO
- Temporal: CREATED_ON, OCCURRED_BEFORE, OCCURRED_AFTER

**Properties** (Attributes):

- Node properties: id, name, type, created_at, metadata
- Edge properties: type, confidence, source, timestamp

**Example Ontology**:

```turtle
# RDF/Turtle format
@prefix : <http://example.org/ontology#> .

:Person a owl:Class ;
    rdfs:label "Person" .

:Organization a owl:Class ;
    rdfs:label "Organization" .

:worksFor a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Organization ;
    rdfs:label "works for" .
```

**Validation**:

- [ ] Entities cover all domain concepts
- [ ] Relationships capture key connections
- [ ] Ontology reviewed with domain experts
- [ ] Classification hierarchy defined (is-a relationships)

---

### Phase 2: Graph Database Selection

**Decision Matrix**:

**Neo4j** (Recommended for most):

- Pros: Mature, Cypher query language, graph algorithms, excellent visualization
- Cons: Licensing costs for enterprise, scaling complexity
- Use when: Complex queries, graph algorithms, team can learn Cypher

**Amazon Neptune**:

- Pros: Managed service, supports Gremlin and SPARQL, AWS integration
- Cons: Vendor lock-in, more expensive than self-hosted
- Use when: AWS infrastructure, need managed service, compliance requirements

**ArangoDB**:

- Pros: Multi-model (graph + document + key-value), JavaScript queries
- Cons: Smaller community, fewer graph-specific features
- Use when: Need document DB + graph in one system

**TigerGraph**:

- Pros: Best performance for deep traversals, parallel processing
- Cons: Complex setup, higher learning curve
- Use when: Massive graphs (billions of edges), real-time analytics

**Technology Stack**:

```yaml
graph_database: 'Neo4j Community' # or Enterprise for production
vector_integration: 'Pinecone' # For hybrid search
embeddings: 'text-embedding-3-large' # OpenAI
etl: 'Apache Airflow' # For data pipelines
```

**Neo4j Schema Setup**:

```cypher
// Create constraints for uniqueness
CREATE CONSTRAINT person_id IF NOT EXISTS
FOR (p:Person) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT org_name IF NOT EXISTS
FOR (o:Organization) REQUIRE o.name IS UNIQUE;

// Create indexes for performance
CREATE INDEX entity_search IF NOT EXISTS
FOR (e:Entity) ON (e.name, e.type);

CREATE INDEX relationship_type IF NOT EXISTS
FOR ()-[r:RELATED_TO]-() ON (r.type, r.confidence);
```

---

### Phase 3: Entity Extraction & Relationship Building

**Goal**: Extract entities and relationships from data sources

**Data Sources**:

- Structured: Databases, APIs, CSV files
- Unstructured: Documents, web content, text files
- Semi-structured: JSON, XML, knowledge bases

**Entity Extraction Pipeline**:

```python
class EntityExtractionPipeline:
    def __init__(self):
        self.ner_model = load_ner_model()  # spaCy, Hugging Face
        self.entity_linker = EntityLinker()
        self.deduplicator = EntityDeduplicator()

    def process_text(self, text: str) -> List[Entity]:
        # 1. Extract named entities
        entities = self.ner_model.extract(text)

        # 2. Link to existing entities (entity resolution)
        linked_entities = self.entity_linker.link(entities)

        # 3. Deduplicate and resolve conflicts
        resolved_entities = self.deduplicator.resolve(linked_entities)

        return resolved_entities
```

**Relationship Extraction**:

```python
class RelationshipExtractor:
    def extract_relationships(self, entities: List[Entity],
                            text: str) -> List[Relationship]:
        relationships = []

        # Use dependency parsing or LLM for extraction
        doc = self.nlp(text)
        for sent in doc.sents:
            rels = self.extract_from_sentence(sent, entities)
            relationships.extend(rels)

        # Validate against ontology
        valid_relationships = self.validate_relationships(relationships)
        return valid_relationships
```

**LLM-Based Extraction** (for complex relationships):

```python
def extract_with_llm(text: str) -> List[Relationship]:
    prompt = f"""
    Extract entities and relationships from this text:
    {text}

    Format: (Entity1, Relationship, Entity2, Confidence)
    Only extract factual relationships.
    """

    response = llm.generate(prompt)
    relationships = parse_llm_response(response)
    return relationships
```

**Validation**:

- [ ] Entity extraction accuracy >85%
- [ ] Entity deduplication working
- [ ] Relationships validated against ontology
- [ ] Confidence scores assigned

---

### Phase 4: Hybrid Knowledge-Vector Architecture

**Goal**: Combine structured graph with semantic vector search

**Architecture**:

```python
class HybridKnowledgeSystem:
    def __init__(self):
        self.graph_db = Neo4jConnection()
        self.vector_db = PineconeClient()
        self.embedding_model = OpenAIEmbeddings()

    def store_entity(self, entity: Entity):
        # Store structured data in graph
        self.graph_db.create_node(entity)

        # Store embeddings in vector database
        embedding = self.embedding_model.embed(entity.description)
        self.vector_db.upsert(
            id=entity.id,
            values=embedding,
            metadata=entity.metadata
        )

    def hybrid_search(self, query: str, top_k: int = 10) -> SearchResults:
        # 1. Vector similarity search
        query_embedding = self.embedding_model.embed(query)
        vector_results = self.vector_db.query(
            vector=query_embedding,
            top_k=100
        )

        # 2. Graph traversal from vector results
        entity_ids = [r.id for r in vector_results.matches]
        graph_results = self.graph_db.get_subgraph(entity_ids, max_hops=2)

        # 3. Merge and rank results
        merged = self.merge_results(vector_results, graph_results)
        return merged[:top_k]
```

**Benefits of Hybrid Approach**:

- Vector search: Semantic similarity, flexible queries
- Graph traversal: Relationship-based reasoning, context expansion
- Combined: Best of both worlds

---

### Phase 5: Query Patterns & API Design

**Common Query Patterns**:

**1. Find Entity**:

```cypher
MATCH (e:Entity {id: $entity_id})
RETURN e
```

**2. Find Relationships**:

```cypher
MATCH (source:Entity {id: $entity_id})-[r]-(target)
RETURN source, r, target
LIMIT 20
```

**3. Path Between Entities**:

```cypher
MATCH path = shortestPath(
  (source:Person {id: $source_id})-[*..5]-(target:Person {id: $target_id})
)
RETURN path
```

**4. Multi-Hop Traversal**:

```cypher
MATCH (p:Person {name: $name})-[:WORKS_FOR]->(o:Organization)-[:LOCATED_IN]->(l:Location)
RETURN p.name, o.name, l.city
```

**5. Recommendation Query**:

```cypher
// Find people similar to this person based on shared organizations
MATCH (p1:Person {id: $person_id})-[:WORKS_FOR]->(o:Organization)<-[:WORKS_FOR]-(p2:Person)
WHERE p1 <> p2
RETURN p2, COUNT(o) AS shared_orgs
ORDER BY shared_orgs DESC
LIMIT 10
```

**Knowledge Graph API**:

```python
class KnowledgeGraphAPI:
    def __init__(self, graph_db):
        self.graph = graph_db

    def find_entity(self, entity_name: str) -> Entity:
        """Find entity by name with fuzzy matching"""
        query = """
        MATCH (e:Entity)
        WHERE e.name CONTAINS $name
        RETURN e
        ORDER BY apoc.text.levenshtein(e.name, $name)
        LIMIT 1
        """
        return self.graph.run(query, name=entity_name).single()

    def find_relationships(self, entity_id: str,
                         relationship_type: str = None,
                         max_hops: int = 2) -> List[Relationship]:
        """Find relationships within specified hops"""
        query = f"""
        MATCH (source:Entity {{id: $entity_id}})
        MATCH path = (source)-[r*1..{max_hops}]-(target)
        RETURN path, relationships(path) AS rels
        LIMIT 100
        """
        return self.graph.run(query, entity_id=entity_id).data()

    def get_subgraph(self, entity_ids: List[str],
                    max_hops: int = 2) -> Subgraph:
        """Get connected subgraph for multiple entities"""
        query = f"""
        MATCH (e:Entity)
        WHERE e.id IN $entity_ids
        CALL apoc.path.subgraphAll(e, {{maxLevel: {max_hops}}})
        YIELD nodes, relationships
        RETURN nodes, relationships
        """
        return self.graph.run(query, entity_ids=entity_ids).data()
```

---

### Phase 6: AI Integration & Hallucination Prevention

**Goal**: Use knowledge graph to ground LLM responses and detect hallucinations

**Knowledge Graph RAG**:

```python
class KnowledgeGraphRAG:
    def __init__(self, kg_api, llm_client):
        self.kg = kg_api
        self.llm = llm_client

    def retrieve_context(self, query: str) -> str:
        # Extract entities from query
        entities = self.extract_entities_from_query(query)

        # Retrieve relevant subgraph
        subgraph = self.kg.get_subgraph(
            [e.id for e in entities],
            max_hops=2
        )

        # Format subgraph for LLM
        context = self.format_subgraph_for_llm(subgraph)
        return context

    def generate_with_grounding(self, query: str) -> GroundedResponse:
        context = self.retrieve_context(query)

        prompt = f"""
        Context from knowledge graph:
        {context}

        User query: {query}

        Answer based only on the provided context. Include source entities.
        """

        response = self.llm.generate(prompt)

        return GroundedResponse(
            response=response,
            sources=self.extract_sources(context),
            confidence=self.calculate_confidence(response, context)
        )
```

**Hallucination Detection**:

```python
class HallucinationDetector:
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph

    def verify_claim(self, claim: str) -> VerificationResult:
        # Parse claim into (subject, predicate, object)
        parsed_claim = self.parse_claim(claim)

        # Query knowledge graph for evidence
        evidence = self.kg.find_evidence(
            parsed_claim.subject,
            parsed_claim.predicate,
            parsed_claim.object
        )

        if evidence:
            return VerificationResult(
                is_supported=True,
                evidence=evidence,
                confidence=evidence.confidence
            )

        # Check for contradictory evidence
        contradiction = self.kg.find_contradiction(parsed_claim)

        return VerificationResult(
            is_supported=False,
            is_contradicted=bool(contradiction),
            contradiction=contradiction
        )
```

---

## Key Principles

### 1. Start with Ontology

Define your schema before ingesting data. Changing ontology later is expensive.

### 2. Entity Resolution is Critical

Deduplicate entities aggressively. "Apple Inc", "Apple", "Apple Computer" → same entity.

### 3. Confidence Scores on Everything

Every relationship should have a confidence score (0.0-1.0) and source.

### 4. Incremental Building

Don't try to model entire domain at once. Start with core entities and expand.

### 5. Hybrid Architecture Wins

Combine graph traversal (structured) with vector search (semantic) for best results.

---

## Common Use Cases

**1. Question Answering**:

- Extract entities from question
- Traverse graph to find answer
- Return path as explanation

**2. Recommendation**:

- Find similar entities via shared relationships
- Rank by relationship strength
- Return top-K recommendations

**3. Fraud Detection**:

- Model transactions as graph
- Find suspicious patterns (cycles, anomalies)
- Flag for review

**4. Knowledge Discovery**:

- Identify implicit relationships
- Suggest missing connections
- Validate with domain experts

**5. Semantic Search**:

- Hybrid vector + graph search
- Expand context via relationships
- Return rich connected results

---

## Technology Recommendations

**For MVPs (<10K entities)**:

- Neo4j Community Edition (free)
- SQLite for metadata
- OpenAI embeddings
- FastAPI for API layer

**For Production (10K-1M entities)**:

- Neo4j Enterprise or ArangoDB
- Pinecone for vector search
- Airflow for ETL
- GraphQL API

**For Enterprise (1M+ entities)**:

- Neo4j Enterprise or TigerGraph
- Distributed vector DB (Pinecone, Weaviate)
- Kafka for streaming
- Kubernetes deployment

---

## Validation Checklist

- [ ] Ontology designed and validated with domain experts
- [ ] Graph database selected and set up
- [ ] Entity extraction pipeline tested (>85% accuracy)
- [ ] Relationship extraction validated
- [ ] Hybrid search (graph + vector) implemented
- [ ] Query API created and documented
- [ ] AI integration tested (RAG or hallucination detection)
- [ ] Performance benchmarks met (query <100ms for common patterns)
- [ ] Data quality monitoring in place
- [ ] Backup and recovery tested

---

## Related Resources

**Related Skills**:

- `rag-implementer` - For hybrid KG+RAG systems
- `multi-agent-architect` - For knowledge-graph-powered agents
- `api-designer` - For KG API design

**Related Patterns**:

- `META/DECISION-FRAMEWORK.md` - Graph DB selection
- `STANDARDS/architecture-patterns/knowledge-graph-pattern.md` - KG architectures (when created)

**Related Playbooks**:

- `PLAYBOOKS/deploy-neo4j.md` - Neo4j deployment (when created)
- `PLAYBOOKS/build-kg-rag-system.md` - KG-RAG integration (when created)
