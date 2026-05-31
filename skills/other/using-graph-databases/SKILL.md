---
name: using-graph-databases
description: Graph database implementation for relationship-heavy data models. Use when building social networks, recommendation engines, knowledge graphs, or fraud detection. Covers Neo4j (primary), ArangoDB, Amazon Neptune, Cypher query patterns, and graph data modeling.
---

# Graph Databases

## Purpose

This skill guides selection and implementation of graph databases for applications where relationships between entities are first-class citizens. Unlike relational databases that model relationships through foreign keys and joins, graph databases natively represent connections as properties, enabling efficient traversal-heavy queries.

## When to Use This Skill

Use graph databases when:
- **Deep relationship traversals** (4+ hops): "Friends of friends of friends"
- **Variable/evolving relationships**: Schema changes don't break existing queries
- **Path finding**: Shortest route, network analysis, dependency chains
- **Pattern matching**: Fraud detection, recommendation engines, access control

**Do NOT use graph databases when**:
- Fixed schema with shallow joins (2-3 tables) → Use PostgreSQL
- Primarily aggregations/analytics → Use columnar databases
- Key-value lookups only → Use Redis/DynamoDB

## Quick Decision Framework

```
DATA CHARACTERISTICS?
├── Fixed schema, shallow joins (≤3 hops)
│   └─ PostgreSQL (relational)
│
├── Already on PostgreSQL + simple graphs
│   └─ Apache AGE (PostgreSQL extension)
│
├── Deep traversals (4+ hops) + general purpose
│   └─ Neo4j (battle-tested, largest ecosystem)
│
├── Multi-model (documents + graph)
│   └─ ArangoDB
│
├── AWS-native, serverless
│   └─ Amazon Neptune
│
└── Real-time streaming, in-memory
    └─ Memgraph
```

## Core Concepts

### Property Graph Model

Graph databases store data as:
- **Nodes** (vertices): Entities with labels and properties
- **Relationships** (edges): Typed connections with properties
- **Properties**: Key-value pairs on nodes and relationships

```
(Person {name: "Alice", age: 28})-[:FRIEND {since: "2020-01-15"}]->(Person {name: "Bob"})
```

### Query Languages

| Language | Databases | Readability | Best For |
|----------|-----------|-------------|----------|
| **Cypher** | Neo4j, Memgraph, AGE | ⭐⭐⭐⭐⭐ SQL-like | General purpose |
| **Gremlin** | Neptune, JanusGraph | ⭐⭐⭐ Functional | Cross-database |
| **AQL** | ArangoDB | ⭐⭐⭐⭐ SQL-like | Multi-model |
| **SPARQL** | Neptune, RDF stores | ⭐⭐⭐ W3C standard | Semantic web |

## Common Cypher Patterns

Reference `references/cypher-patterns.md` for comprehensive examples.

### Pattern 1: Basic Matching
```cypher
// Find all users at a company
MATCH (u:User)-[:WORKS_AT]->(c:Company {name: 'Acme Corp'})
RETURN u.name, u.title
```

### Pattern 2: Variable-Length Paths
```cypher
// Find friends up to 3 degrees away
MATCH (u:User {name: 'Alice'})-[:FRIEND*1..3]->(friend)
WHERE u <> friend
RETURN DISTINCT friend.name
LIMIT 100
```

### Pattern 3: Shortest Path
```cypher
// Find shortest connection between two users
MATCH path = shortestPath(
  (a:User {name: 'Alice'})-[*]-(b:User {name: 'Bob'})
)
RETURN path, length(path) AS distance
```

### Pattern 4: Recommendations
```cypher
// Collaborative filtering: Products liked by similar users
MATCH (u:User {id: $userId})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(similar)
MATCH (similar)-[:PURCHASED]->(rec:Product)
WHERE NOT exists((u)-[:PURCHASED]->(rec))
RETURN rec.name, count(*) AS score
ORDER BY score DESC
LIMIT 10
```

### Pattern 5: Fraud Detection
```cypher
// Detect circular money flows
MATCH path = (a:Account)-[:SENT*3..6]->(a)
WHERE all(r IN relationships(path) WHERE r.amount > 1000)
RETURN path, [r IN relationships(path) | r.amount] AS amounts
```

## Database Selection Guide

### Neo4j (Primary Recommendation)

**Use for**: General-purpose graph applications

**Strengths**:
- Most mature (2007), largest community (2M+ developers)
- 65+ graph algorithms (GDS library): PageRank, Louvain, Dijkstra
- Best tooling: Neo4j Browser, Bloom visualization
- Comprehensive Cypher support

**Installation**:
```bash
# Python driver
pip install neo4j

# TypeScript driver
npm install neo4j-driver

# Rust driver
cargo add neo4rs
```

Reference: `references/neo4j.md`

### ArangoDB

**Use for**: Multi-model applications (documents + graph)

**Strengths**:
- Store documents AND graph in one database
- AQL combines document and graph queries
- Schema flexibility with relationships

Reference: `references/arangodb.md`

### Apache AGE

**Use for**: Adding graph capabilities to existing PostgreSQL

**Strengths**:
- Extend PostgreSQL with graph queries
- No new infrastructure needed
- Query both relational and graph data

Reference: Implementation details in examples/

### Amazon Neptune

**Use for**: AWS-native, serverless deployments

**Strengths**:
- Fully managed, auto-scaling
- Supports Gremlin AND SPARQL
- AWS ecosystem integration

## Graph Data Modeling Patterns

Reference `references/graph-modeling.md` for comprehensive patterns.

### Best Practice 1: Relationships as First-Class Citizens

**Anti-pattern** (storing relationships in node properties):
```cypher
// BAD
(:Person {name: 'Alice', friend_ids: ['b123', 'c456']})
```

**Pattern** (explicit relationships):
```cypher
// GOOD
(:Person {name: 'Alice'})-[:FRIEND]->(:Person {id: 'b123'})
(:Person {name: 'Alice'})-[:FRIEND]->(:Person {id: 'c456'})
```

### Best Practice 2: Relationship Properties for Metadata

```cypher
// Track interaction details on relationships
(:Person)-[:FRIEND {
  since: '2020-01-15',
  strength: 0.85,
  last_interaction: datetime()
}]->(:Person)
```

### Best Practice 3: Bounded Traversals for Performance

```cypher
// SLOW: Unbounded traversal
MATCH (a)-[:FRIEND*]->(distant)
RETURN distant

// FAST: Bounded depth with index
MATCH (a)-[:FRIEND*1..4]->(distant)
WHERE distant.active = true
RETURN distant
LIMIT 100
```

### Best Practice 4: Avoid Supernodes

**Problem**: Nodes with thousands of relationships slow traversals.

**Solution**: Intermediate aggregation nodes
```cypher
// Instead of: (:User)-[:POSTED]->(:Post) [1M relationships]

// Use time partitioning:
(:User)-[:POSTED_IN]->(:Year {year: 2025})
       -[:HAS_MONTH]->(:Month {month: 12})
       -[:HAS_POST]->(:Post)
```

## Use Case Examples

### Social Network

Schema and implementation in `examples/social-graph/`

**Key features**:
- Friend recommendations (friends-of-friends)
- Mutual connections
- News feed generation
- Influence metrics

### Knowledge Graph for AI/RAG

Integration example in `examples/knowledge-graph/`

**Key features**:
- Hybrid vector + graph search
- Entity relationship mapping
- Context expansion for LLM prompts
- Semantic relationship traversal

**Integration with Vector Databases**:
```python
# Step 1: Vector search in Qdrant/pgvector
vector_results = qdrant.search(collection="concepts", query_vector=embedding)

# Step 2: Expand with graph relationships
concept_ids = [r.id for r in vector_results]
graph_context = neo4j.run("""
  MATCH (c:Concept) WHERE c.id IN $ids
  MATCH (c)-[:RELATED_TO|IS_A*1..2]-(related)
  RETURN c, related, relationships(path)
""", ids=concept_ids)
```

### Recommendation Engine

Examples in `examples/social-graph/`

**Strategies**:
1. **Collaborative filtering**: "Users who bought X also bought Y"
2. **Content-based**: "Products similar to what you like"
3. **Session-based**: "Recently viewed items"

### Fraud Detection

Pattern detection in examples/

**Detection patterns**:
- Circular money flows
- Shared devices across accounts
- Rapid transaction chains
- Connection pattern anomalies

## Performance Optimization

Reference `references/cypher-patterns.md` for detailed optimization.

### Indexing
```cypher
// Single-property index
CREATE INDEX user_email FOR (u:User) ON (u.email)

// Composite index (Neo4j 5.x+)
CREATE INDEX user_name_location FOR (u:User) ON (u.name, u.location)

// Full-text search
CREATE FULLTEXT INDEX product_search FOR (p:Product) ON EACH [p.name, p.description]
```

### Caching Expensive Aggregations
```cypher
// Materialize friend count as property
MATCH (u:User)-[:FRIEND]->(f)
WITH u, count(f) AS friendCount
SET u.friend_count = friendCount

// Query becomes instant
MATCH (u:User) WHERE u.friend_count > 100
RETURN u.name, u.friend_count
```

### Scaling Strategies

| Scale | Strategy | Implementation |
|-------|----------|----------------|
| **Vertical** | Add RAM/CPU | In-memory caching, larger instances |
| **Horizontal (Read)** | Read replicas | Neo4j Cluster, ArangoDB Cluster |
| **Horizontal (Write)** | Sharding | ArangoDB SmartGraphs, JanusGraph |
| **Caching** | App-level cache | Redis for hot paths |

## Language Integration

### Python (Neo4j)

Complete example in `examples/social-graph/python-neo4j/`

```python
from neo4j import GraphDatabase

class GraphDB:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def find_friends_of_friends(self, user_id: str, max_depth: int = 2):
        query = """
        MATCH (u:User {id: $userId})-[:FRIEND*1..$maxDepth]->(fof)
        WHERE u <> fof
        RETURN DISTINCT fof.id, fof.name
        LIMIT 100
        """
        with self.driver.session() as session:
            result = session.run(query, userId=user_id, maxDepth=max_depth)
            return [dict(record) for record in result]

# Usage
db = GraphDB("bolt://localhost:7687", "neo4j", "password")
friends = db.find_friends_of_friends("u123", max_depth=3)
```

### TypeScript (Neo4j)

Complete example in `examples/social-graph/typescript-neo4j/`

```typescript
import neo4j, { Driver } from 'neo4j-driver'

class Neo4jService {
  private driver: Driver

  constructor(uri: string, username: string, password: string) {
    this.driver = neo4j.driver(uri, neo4j.auth.basic(username, password))
  }

  async findFriendsOfFriends(userId: string, maxDepth: number = 2) {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `MATCH (u:User {id: $userId})-[:FRIEND*1..$maxDepth]->(fof)
         WHERE u <> fof
         RETURN DISTINCT fof.id, fof.name
         LIMIT 100`,
        { userId, maxDepth }
      )
      return result.records.map(r => r.toObject())
    } finally {
      await session.close()
    }
  }
}
```

### Go (ArangoDB)

```go
import (
    "github.com/arangodb/go-driver"
    "github.com/arangodb/go-driver/http"
)

func findFriendsOfFriends(db driver.Database, userId string, maxDepth int) ([]User, error) {
    query := `
        FOR vertex, edge, path IN 1..@maxDepth OUTBOUND @startVertex GRAPH 'socialGraph'
            FILTER vertex._id != @startVertex
            RETURN DISTINCT vertex
            LIMIT 100
    `

    cursor, err := db.Query(ctx, query, map[string]interface{}{
        "startVertex": userId,
        "maxDepth": maxDepth,
    })

    // Handle results...
}
```

## Schema Validation

Use `scripts/validate_graph_schema.py` to check for:
- Unbounded traversals (missing depth limits)
- Missing indexes on frequently queried properties
- Supernodes (nodes with excessive relationships)
- Relationship property consistency

Run validation:
```bash
python scripts/validate_graph_schema.py --database neo4j://localhost:7687
```

## Integration with Other Skills

### With databases-vector (Hybrid Search)
Combine vector similarity with graph context for AI/RAG applications.
See `examples/knowledge-graph/`

### With search-filter
Implement relationship-based queries: "Find all users within 3 degrees of connection"

### With ai-chat
Use knowledge graphs to enrich LLM context with structured relationships.

### With auth-security (ReBAC)
Implement relationship-based access control: "Can user X access resource Y through relation Z?"

## Common Schema Patterns

### Star Schema (Hub and Spokes)
```cypher
(:User)-[:PURCHASED]->(:Product)
(:User)-[:VIEWED]->(:Product)
(:User)-[:RATED]->(:Product)
```

### Hierarchical Schema (Trees)
```cypher
(:CEO)-[:MANAGES]->(:VP)-[:MANAGES]->(:Director)
```

### Temporal Schema (Event Sequences)
```cypher
(:Event {timestamp})-[:NEXT]->(:Event {timestamp})
```

## Getting Started

1. **Choose database**: Use decision framework above
2. **Design schema**: Reference `references/graph-modeling.md`
3. **Implement queries**: Use patterns from `references/cypher-patterns.md`
4. **Validate**: Run `scripts/validate_graph_schema.py`
5. **Optimize**: Add indexes, bound traversals, cache aggregations

## Further Reading

- `references/neo4j.md` - Neo4j setup, drivers, GDS algorithms
- `references/arangodb.md` - ArangoDB multi-model patterns
- `references/cypher-patterns.md` - Comprehensive Cypher query library
- `references/graph-modeling.md` - Data modeling best practices
- `examples/social-graph/` - Complete social network implementation
- `examples/knowledge-graph/` - Hybrid vector + graph for AI/RAG
