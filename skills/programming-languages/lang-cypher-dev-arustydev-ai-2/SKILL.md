---
name: lang-cypher-dev
description: Foundational Cypher (Neo4j) patterns covering graph pattern matching, MATCH/CREATE/MERGE/DELETE operations, relationships, path patterns, aggregation, filtering, and common graph query patterns. Use when writing Cypher queries, modeling graph data, or needing guidance on graph database operations. This is the entry point for Cypher development.
---

# Cypher Fundamentals

Foundational Cypher patterns and core query language features for Neo4j graph databases. This skill serves as both a reference for common patterns and an index to specialized graph database skills.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Cypher Skill Hierarchy                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                 ┌─────────────────────┐                         │
│                 │  lang-cypher-dev    │ ◄── You are here        │
│                 │    (foundation)     │                         │
│                 └──────────┬──────────┘                         │
│                            │                                    │
│            ┌───────────────┴───────────────┐                    │
│            │                               │                    │
│            ▼                               ▼                    │
│   ┌─────────────────┐            ┌─────────────────┐           │
│   │    patterns     │            │     admin       │           │
│   │      -dev       │            │      -ops       │           │
│   └─────────────────┘            └─────────────────┘           │
│         (future)                       (future)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Node and relationship pattern syntax
- MATCH, CREATE, MERGE, DELETE operations
- WHERE clauses and filtering
- Path patterns and traversals
- Aggregation functions
- Indexes and constraints
- Common graph query patterns
- Query optimization basics

**This skill does NOT cover (see specialized skills):**
- Advanced graph algorithms → `lang-cypher-patterns-dev` (future)
- Performance tuning and profiling → `lang-cypher-patterns-dev` (future)
- Database administration → `lang-cypher-admin-ops` (future)
- APOC procedures → `lang-cypher-patterns-dev` (future)

---

## Quick Reference

| Task | Syntax |
|------|--------|
| Match node | `MATCH (n:Label)` |
| Match relationship | `MATCH (a)-[r:TYPE]->(b)` |
| Create node | `CREATE (n:Label {prop: value})` |
| Create relationship | `CREATE (a)-[r:TYPE]->(b)` |
| Merge (upsert) | `MERGE (n:Label {id: 1})` |
| Delete node | `MATCH (n) DELETE n` |
| Detach delete | `MATCH (n) DETACH DELETE n` |
| Filter | `WHERE n.age > 18` |
| Return | `RETURN n.name AS name` |
| Order/limit | `ORDER BY n.name LIMIT 10` |
| Count | `RETURN count(n)` |
| Variable path | `MATCH p=(a)-[*1..5]->(b)` |

---

## Skill Routing

Use this table to find the right specialized skill:

| When you need to... | Use this skill |
|---------------------|----------------|
| Advanced graph algorithms (PageRank, community detection) | `lang-cypher-patterns-dev` (future) |
| Performance tuning, query profiling | `lang-cypher-patterns-dev` (future) |
| Database administration, backup/restore | `lang-cypher-admin-ops` (future) |
| APOC procedures and custom extensions | `lang-cypher-patterns-dev` (future) |

---

## Node Patterns

### Basic Node Matching

```cypher
// Match all nodes
MATCH (n)
RETURN n

// Match nodes with specific label
MATCH (p:Person)
RETURN p

// Match nodes with multiple labels
MATCH (u:User:Admin)
RETURN u

// Match node with properties
MATCH (p:Person {name: 'Alice'})
RETURN p

// Match node with WHERE clause
MATCH (p:Person)
WHERE p.age > 30
RETURN p
```

### Creating Nodes

```cypher
// Create single node
CREATE (p:Person {name: 'Alice', age: 30})
RETURN p

// Create multiple nodes
CREATE
  (p1:Person {name: 'Alice'}),
  (p2:Person {name: 'Bob'})
RETURN p1, p2

// Create node with multiple labels
CREATE (u:User:Admin {name: 'Alice', role: 'admin'})
RETURN u

// Create and set properties
CREATE (p:Person)
SET p.name = 'Alice', p.age = 30
RETURN p
```

### Merging Nodes (Upsert)

```cypher
// MERGE: Create if not exists, match if exists
MERGE (p:Person {email: 'alice@example.com'})
ON CREATE SET p.name = 'Alice', p.created = timestamp()
ON MATCH SET p.lastSeen = timestamp()
RETURN p

// MERGE with complex logic
MERGE (u:User {id: 123})
ON CREATE SET
  u.name = 'Alice',
  u.created = timestamp(),
  u.status = 'new'
ON MATCH SET
  u.updated = timestamp(),
  u.loginCount = u.loginCount + 1
RETURN u
```

---

## Relationship Patterns

### Basic Relationship Matching

```cypher
// Match any relationship
MATCH (a)-[r]->(b)
RETURN a, r, b

// Match specific relationship type
MATCH (a:Person)-[r:KNOWS]->(b:Person)
RETURN a, r, b

// Match undirected relationship
MATCH (a:Person)-[r:KNOWS]-(b:Person)
RETURN a, r, b

// Match relationship with properties
MATCH (a:Person)-[r:KNOWS {since: 2020}]->(b:Person)
RETURN a, r, b

// Match multiple relationship types
MATCH (a)-[r:KNOWS|FOLLOWS]->(b)
RETURN a, type(r), b
```

### Creating Relationships

```cypher
// Create relationship between existing nodes
MATCH (a:Person {name: 'Alice'})
MATCH (b:Person {name: 'Bob'})
CREATE (a)-[r:KNOWS {since: 2020}]->(b)
RETURN a, r, b

// Create nodes and relationships in one query
CREATE (a:Person {name: 'Alice'})
CREATE (b:Person {name: 'Bob'})
CREATE (a)-[r:KNOWS]->(b)
RETURN a, r, b

// Compact syntax
CREATE (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'})
RETURN a, r, b
```

### Merging Relationships

```cypher
// MERGE relationship (with nodes)
MATCH (a:Person {name: 'Alice'})
MATCH (b:Person {name: 'Bob'})
MERGE (a)-[r:KNOWS]->(b)
ON CREATE SET r.since = timestamp()
RETURN a, r, b

// MERGE entire pattern
MERGE (a:Person {email: 'alice@example.com'})-[r:KNOWS]->(b:Person {email: 'bob@example.com'})
ON CREATE SET
  a.name = 'Alice',
  b.name = 'Bob',
  r.created = timestamp()
RETURN a, r, b
```

---

## Path Patterns

### Fixed-Length Paths

```cypher
// 2-hop path
MATCH (a:Person)-[:KNOWS]->(:Person)-[:KNOWS]->(b:Person)
WHERE a.name = 'Alice'
RETURN b

// Pattern with named intermediate nodes
MATCH (a:Person)-[:KNOWS]->(friend:Person)-[:KNOWS]->(fof:Person)
RETURN a.name, friend.name, fof.name
```

### Variable-Length Paths

```cypher
// Any path length (use with caution!)
MATCH p=(a:Person)-[:KNOWS*]->(b:Person)
WHERE a.name = 'Alice'
RETURN p

// Path with length bounds (1 to 3 hops)
MATCH p=(a:Person)-[:KNOWS*1..3]->(b:Person)
WHERE a.name = 'Alice'
RETURN b.name, length(p) AS hops

// Shortest path
MATCH p=shortestPath((a:Person)-[:KNOWS*]-(b:Person))
WHERE a.name = 'Alice' AND b.name = 'Charlie'
RETURN length(p) AS distance, nodes(p) AS path

// All shortest paths
MATCH p=allShortestPaths((a:Person)-[:KNOWS*]-(b:Person))
WHERE a.name = 'Alice' AND b.name = 'Charlie'
RETURN p
```

### Path Functions

```cypher
// Extract path components
MATCH p=(a:Person)-[:KNOWS*1..3]->(b:Person)
WHERE a.name = 'Alice'
RETURN
  length(p) AS pathLength,
  nodes(p) AS allNodes,
  relationships(p) AS allRels,
  [n in nodes(p) | n.name] AS names
```

---

## Filtering with WHERE

### Property Comparisons

```cypher
// Basic comparisons
MATCH (p:Person)
WHERE p.age > 30
RETURN p

// Multiple conditions (AND)
MATCH (p:Person)
WHERE p.age > 30 AND p.city = 'New York'
RETURN p

// OR conditions
MATCH (p:Person)
WHERE p.age < 20 OR p.age > 60
RETURN p

// NULL checks
MATCH (p:Person)
WHERE p.email IS NOT NULL
RETURN p

// Property exists
MATCH (p:Person)
WHERE exists(p.email)
RETURN p
```

### String Matching

```cypher
// Case-sensitive contains
MATCH (p:Person)
WHERE p.name CONTAINS 'ali'
RETURN p

// Case-insensitive (convert to lowercase)
MATCH (p:Person)
WHERE toLower(p.name) CONTAINS 'ali'
RETURN p

// Starts with
MATCH (p:Person)
WHERE p.name STARTS WITH 'A'
RETURN p

// Ends with
MATCH (p:Person)
WHERE p.email ENDS WITH '@example.com'
RETURN p

// Regex matching
MATCH (p:Person)
WHERE p.email =~ '.*@example\\.com'
RETURN p
```

### Collection Filtering

```cypher
// IN operator
MATCH (p:Person)
WHERE p.name IN ['Alice', 'Bob', 'Charlie']
RETURN p

// Check property in list
MATCH (p:Person)
WHERE 'admin' IN p.roles
RETURN p

// ANY predicate
MATCH (p:Person)
WHERE ANY(role IN p.roles WHERE role STARTS WITH 'dev')
RETURN p

// ALL predicate
MATCH (p:Person)
WHERE ALL(x IN p.scores WHERE x > 50)
RETURN p

// NONE predicate
MATCH (p:Person)
WHERE NONE(x IN p.tags WHERE x = 'blocked')
RETURN p

// SINGLE predicate (exactly one match)
MATCH (p:Person)
WHERE SINGLE(x IN p.roles WHERE x = 'admin')
RETURN p
```

### Relationship Filtering

```cypher
// Filter on relationship properties
MATCH (a:Person)-[r:KNOWS]->(b:Person)
WHERE r.since > 2020
RETURN a, b

// Filter on relationship existence
MATCH (p:Person)
WHERE NOT (p)-[:KNOWS]->()
RETURN p  // People who don't know anyone

// Filter on degree
MATCH (p:Person)
WHERE size((p)-[:KNOWS]->()) > 5
RETURN p  // People who know more than 5 others
```

---

## Aggregation

### Basic Aggregations

```cypher
// Count
MATCH (p:Person)
RETURN count(p) AS totalPeople

// Count distinct
MATCH (p:Person)
RETURN count(DISTINCT p.city) AS uniqueCities

// Sum
MATCH (p:Person)
RETURN sum(p.age) AS totalAge

// Average
MATCH (p:Person)
RETURN avg(p.age) AS averageAge

// Min/Max
MATCH (p:Person)
RETURN min(p.age) AS youngest, max(p.age) AS oldest

// Collect into list
MATCH (p:Person)
RETURN collect(p.name) AS allNames

// Collect distinct
MATCH (p:Person)
RETURN collect(DISTINCT p.city) AS cities
```

### Grouping

```cypher
// GROUP BY (implicit via non-aggregated fields)
MATCH (p:Person)
RETURN p.city, count(p) AS population
ORDER BY population DESC

// Multiple grouping fields
MATCH (p:Person)
RETURN p.city, p.age, count(p) AS count

// Aggregation with relationships
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN c.name, count(p) AS employees
ORDER BY employees DESC
```

### WITH Clause (Pipeline Queries)

```cypher
// Use WITH to chain query parts
MATCH (p:Person)
WITH p.city AS city, count(p) AS population
WHERE population > 100
RETURN city, population
ORDER BY population DESC

// Aggregate then filter
MATCH (p:Person)-[:KNOWS]->(friend:Person)
WITH p, count(friend) AS friendCount
WHERE friendCount > 10
RETURN p.name, friendCount

// Multiple WITH clauses
MATCH (p:Person)
WITH p.city AS city, count(p) AS pop
WHERE pop > 50
WITH city, pop
ORDER BY pop DESC
LIMIT 5
RETURN city, pop
```

---

## Modifying Data

### Updating Properties

```cypher
// SET property
MATCH (p:Person {name: 'Alice'})
SET p.age = 31
RETURN p

// SET multiple properties
MATCH (p:Person {name: 'Alice'})
SET p.age = 31, p.city = 'Boston', p.updated = timestamp()
RETURN p

// SET from map
MATCH (p:Person {name: 'Alice'})
SET p += {age: 31, city: 'Boston'}
RETURN p

// REMOVE property
MATCH (p:Person {name: 'Alice'})
REMOVE p.age
RETURN p
```

### Adding and Removing Labels

```cypher
// Add label
MATCH (p:Person {name: 'Alice'})
SET p:Admin
RETURN p

// Remove label
MATCH (p:Person {name: 'Alice'})
REMOVE p:Admin
RETURN p

// Add multiple labels
MATCH (p:Person {name: 'Alice'})
SET p:Admin:Moderator
RETURN p
```

### Deleting Data

```cypher
// Delete node (must have no relationships)
MATCH (p:Person {name: 'Alice'})
DELETE p

// DETACH DELETE (removes relationships first)
MATCH (p:Person {name: 'Alice'})
DETACH DELETE p

// Delete relationship
MATCH (:Person {name: 'Alice'})-[r:KNOWS]->(:Person {name: 'Bob'})
DELETE r

// Delete all nodes and relationships (DANGEROUS!)
MATCH (n)
DETACH DELETE n

// Conditional delete
MATCH (p:Person)
WHERE p.inactive = true
DETACH DELETE p
```

---

## Indexes and Constraints

### Creating Indexes

```cypher
// Single-property index
CREATE INDEX person_name FOR (p:Person) ON (p.name)

// Composite index
CREATE INDEX person_name_age FOR (p:Person) ON (p.name, p.age)

// Full-text index
CREATE FULLTEXT INDEX person_search FOR (p:Person) ON EACH [p.name, p.bio]

// Index on relationship
CREATE INDEX knows_since FOR ()-[r:KNOWS]-() ON (r.since)
```

### Creating Constraints

```cypher
// Unique constraint (automatically creates index)
CREATE CONSTRAINT person_email_unique FOR (p:Person) REQUIRE p.email IS UNIQUE

// Node key (multiple properties must be unique together)
CREATE CONSTRAINT person_key FOR (p:Person) REQUIRE (p.firstName, p.lastName) IS NODE KEY

// Property existence (Enterprise only)
CREATE CONSTRAINT person_name_exists FOR (p:Person) REQUIRE p.name IS NOT NULL

// Relationship existence (Enterprise only)
CREATE CONSTRAINT knows_since_exists FOR ()-[r:KNOWS]-() REQUIRE r.since IS NOT NULL
```

### Managing Indexes and Constraints

```cypher
// List all indexes
SHOW INDEXES

// List all constraints
SHOW CONSTRAINTS

// Drop index
DROP INDEX person_name

// Drop constraint
DROP CONSTRAINT person_email_unique
```

---

## Common Graph Patterns

### Friend-of-Friend (Recommendation)

```cypher
// Find friends of friends (2nd degree)
MATCH (me:Person {name: 'Alice'})-[:KNOWS]->(friend)-[:KNOWS]->(fof)
WHERE NOT (me)-[:KNOWS]->(fof) AND me <> fof
RETURN DISTINCT fof.name, count(friend) AS mutualFriends
ORDER BY mutualFriends DESC
LIMIT 10
```

### Hierarchical Data (Tree Traversal)

```cypher
// Find all descendants
MATCH (root:Category {name: 'Electronics'})-[:PARENT_OF*]->(descendant)
RETURN descendant

// Find path from root to leaf
MATCH path = (root:Category {name: 'Electronics'})-[:PARENT_OF*]->(leaf:Category)
WHERE NOT (leaf)-[:PARENT_OF]->()
RETURN path

// Find depth of each node
MATCH (root:Category {name: 'Electronics'})-[:PARENT_OF*]->(node)
RETURN node.name, length(path) AS depth
```

### Finding Cycles

```cypher
// Find circular dependencies
MATCH (a:Task)-[:DEPENDS_ON*]->(b:Task)-[:DEPENDS_ON*]->(a)
RETURN DISTINCT a.name, b.name

// Find triangles (3-node cycles)
MATCH (a:Person)-[:KNOWS]->(b:Person)-[:KNOWS]->(c:Person)-[:KNOWS]->(a)
WHERE id(a) < id(b) AND id(b) < id(c)
RETURN a.name, b.name, c.name
```

### Social Network Patterns

```cypher
// Mutual followers
MATCH (me:Person {name: 'Alice'})-[:FOLLOWS]->(person:Person)
WHERE (person)-[:FOLLOWS]->(me)
RETURN person.name

// Most influential (most followers)
MATCH (p:Person)<-[:FOLLOWS]-(follower)
RETURN p.name, count(follower) AS followers
ORDER BY followers DESC
LIMIT 10

// Activity feed (posts from followed users)
MATCH (me:Person {name: 'Alice'})-[:FOLLOWS]->(user:Person)-[:POSTED]->(post:Post)
RETURN post.content, post.timestamp, user.name
ORDER BY post.timestamp DESC
LIMIT 20
```

### Collaborative Filtering

```cypher
// Users who liked similar items
MATCH (me:User {id: 123})-[:LIKED]->(item:Item)<-[:LIKED]-(other:User)
WITH other, count(item) AS commonItems
WHERE commonItems > 3
RETURN other.name, commonItems
ORDER BY commonItems DESC

// Recommend items liked by similar users
MATCH (me:User {id: 123})-[:LIKED]->(myItem:Item)<-[:LIKED]-(other:User)
MATCH (other)-[:LIKED]->(rec:Item)
WHERE NOT (me)-[:LIKED]->(rec)
RETURN rec.title, count(DISTINCT other) AS recommendations
ORDER BY recommendations DESC
LIMIT 10
```

---

## Query Optimization

### Using EXPLAIN and PROFILE

```cypher
// EXPLAIN: Shows query plan without executing
EXPLAIN
MATCH (p:Person {name: 'Alice'})
RETURN p

// PROFILE: Executes and shows actual performance metrics
PROFILE
MATCH (p:Person)
WHERE p.age > 30
RETURN p
```

### Optimization Tips

```cypher
// BAD: Cartesian product
MATCH (a:Person), (b:Company)
WHERE a.companyId = b.id
RETURN a, b

// GOOD: Use relationship
MATCH (a:Person)-[:WORKS_AT]->(b:Company)
RETURN a, b

// BAD: Property lookup without index
MATCH (p:Person)
WHERE p.email = 'alice@example.com'
RETURN p

// GOOD: Create index first
CREATE INDEX person_email FOR (p:Person) ON (p.email)
// Then query
MATCH (p:Person {email: 'alice@example.com'})
RETURN p

// BAD: Unbounded variable-length path
MATCH (a)-[*]->(b)
RETURN a, b

// GOOD: Add upper bound
MATCH (a)-[*..5]->(b)
RETURN a, b

// Use LIMIT for large result sets
MATCH (p:Person)
RETURN p
LIMIT 100
```

### Using Parameters

```cypher
// Use parameters for better performance and security
// Parameter syntax: $paramName

// In neo4j driver or browser
:param name => 'Alice'
:param age => 30

// Query using parameters
MATCH (p:Person {name: $name})
WHERE p.age > $age
RETURN p

// Useful for batch operations
UNWIND $batchData AS data
MERGE (p:Person {id: data.id})
SET p.name = data.name, p.age = data.age
```

---

## Troubleshooting

### "Node not found" or Empty Results

```cypher
// Check if nodes exist
MATCH (n:Person)
RETURN count(n)

// Check labels
CALL db.labels()

// Check for typos in property names
MATCH (n:Person)
RETURN keys(n)
LIMIT 1
```

### Performance Issues

```cypher
// Check for missing indexes
SHOW INDEXES

// Profile slow query
PROFILE
MATCH (p:Person)-[:KNOWS*1..3]->(friend)
WHERE p.name = 'Alice'
RETURN friend

// Look for:
// - DB Hits (lower is better)
// - Rows (indicates cardinality)
// - EstimatedRows vs Rows (large difference = poor stats)
```

### Accidental Cartesian Products

```cypher
// BAD: Creates cartesian product
MATCH (a:Person)
MATCH (b:Company)
RETURN a, b

// Warning: "This query builds a cartesian product between disconnected patterns"

// FIX: Add relationship or WHERE clause
MATCH (a:Person)
MATCH (b:Company)
WHERE a.companyId = b.id
RETURN a, b
```

### Memory Issues

```cypher
// BAD: Loads all nodes into memory
MATCH (n)
RETURN collect(n)

// GOOD: Process in batches
MATCH (n)
RETURN n
SKIP 0 LIMIT 1000

// Use WITH for intermediate aggregation
MATCH (p:Person)-[:KNOWS]->(friend)
WITH p, collect(friend)[0..10] AS topFriends
RETURN p.name, topFriends
```

---

## References

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Neo4j Cypher Refcard](https://neo4j.com/docs/cypher-refcard/current/)
- [Neo4j Graph Algorithms](https://neo4j.com/docs/graph-data-science/current/)
- Specialized skills: `lang-cypher-patterns-dev`, `lang-cypher-admin-ops` (future)
