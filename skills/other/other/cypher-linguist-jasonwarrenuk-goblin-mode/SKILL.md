---
name: cypher-linguist
description: This skill should be used when the user mentions "Neo4j", "Cypher", "graph database", "graph query", discusses graph relationships, traversals, path finding, or needs help with Cypher syntax. Addresses Neo4j fundamentals, query patterns, performance optimization, and integration with relational databases.
version: 1.0.0
---

# Neo4j/Cypher Mastery

Comprehensive guide to Neo4j graph database and Cypher query language. Covers fundamental concepts, common patterns, performance optimization, schema design, and integration with PostgreSQL/Supabase.

---

## When This Skill Applies

Use this skill when:
- Writing Cypher queries
- Designing graph schemas
- Optimizing graph traversals
- Building recommendation systems
- Modeling hierarchies or networks
- Integrating Neo4j with relational databases
- Questions about graph database patterns

---

## Core Concepts

### Nodes, Relationships, Properties

**Nodes** - Entities (nouns):
```cypher
// Simple node
CREATE (u:User)

// Node with properties
CREATE (u:User {
  id: 'user-123',
  name: 'Alice',
  email: 'alice@example.com'
})

// Multiple labels
CREATE (p:Person:Developer {name: 'Bob'})
```

**Relationships** - Connections (verbs):
```cypher
// Simple relationship
CREATE (a)-[:FOLLOWS]->(b)

// Relationship with properties
CREATE (a)-[:FOLLOWS {since: date(), strength: 'strong'}]->(b)

// Relationship types are UPPERCASE by convention
CREATE (a)-[:MEMBER_OF {role: 'admin'}]->(org)
```

**Properties** - Attributes (key-value pairs):
```cypher
// Node properties
{
  id: 'user-123',
  name: 'Alice',
  age: 30,
  verified: true,
  createdAt: datetime()
}

// Relationship properties
{
  since: date(),
  weight: 0.85,
  type: 'professional'
}
```

### Graph Thinking

**Relational mindset**:
```sql
-- Joins and foreign keys
SELECT * FROM users u
JOIN follows f ON f.follower_id = u.id
JOIN users u2 ON f.followed_id = u2.id
WHERE u.id = '123';
```

**Graph mindset**:
```cypher
// Pattern matching
MATCH (u:User {id: '123'})-[:FOLLOWS]->(friend)
RETURN friend;
```

**Key difference**: Relationships are first-class citizens in graphs.

---

## Cypher Fundamentals

### MATCH - Finding Patterns

**Basic pattern**:
```cypher
// Find all users
MATCH (u:User)
RETURN u;

// Find users with specific property
MATCH (u:User {name: 'Alice'})
RETURN u;

// Find users matching condition
MATCH (u:User)
WHERE u.age > 25
RETURN u;
```

**Relationship patterns**:
```cypher
// Outgoing relationship
MATCH (a)-[:FOLLOWS]->(b)
RETURN a, b;

// Incoming relationship
MATCH (a)<-[:FOLLOWS]-(b)
RETURN a, b;

// Any direction
MATCH (a)-[:FOLLOWS]-(b)
RETURN a, b;

// Multiple relationships
MATCH (a)-[:FOLLOWS]->(b)-[:FOLLOWS]->(c)
RETURN a, b, c;

// Variable length
MATCH (a)-[:FOLLOWS*1..3]->(b)
RETURN a, b;
```

### CREATE - Adding Data

**Create nodes**:
```cypher
// Single node
CREATE (u:User {id: 'user-123', name: 'Alice'})
RETURN u;

// Multiple nodes
CREATE
  (a:User {name: 'Alice'}),
  (b:User {name: 'Bob'}),
  (c:User {name: 'Charlie'});
```

**Create relationships**:
```cypher
// Find existing nodes, create relationship
MATCH (a:User {name: 'Alice'})
MATCH (b:User {name: 'Bob'})
CREATE (a)-[:FOLLOWS]->(b);

// Create nodes and relationships together
CREATE (a:User {name: 'Alice'})-[:FOLLOWS]->(b:User {name: 'Bob'});
```

### MERGE - Create or Match

**Create if not exists**:
```cypher
// Create user only if doesn't exist
MERGE (u:User {id: 'user-123'})
ON CREATE SET u.name = 'Alice', u.createdAt = datetime()
ON MATCH SET u.lastSeen = datetime()
RETURN u;

// Create relationship only if doesn't exist
MATCH (a:User {id: 'user-123'})
MATCH (b:User {id: 'user-456'})
MERGE (a)-[r:FOLLOWS]->(b)
ON CREATE SET r.since = datetime()
RETURN r;
```

**Important**: MERGE matches on entire pattern:
```cypher
// This matches on ALL properties
MERGE (u:User {id: 'user-123', name: 'Alice'})

// Better: Match on unique constraint only
MERGE (u:User {id: 'user-123'})
SET u.name = 'Alice'
```

### SET - Updating Properties
```cypher
// Set single property
MATCH (u:User {id: 'user-123'})
SET u.name = 'Alicia'
RETURN u;

// Set multiple properties
MATCH (u:User {id: 'user-123'})
SET u.name = 'Alicia', u.verified = true
RETURN u;

// Set properties from map
MATCH (u:User {id: 'user-123'})
SET u += {name: 'Alicia', age: 31}
RETURN u;

// Add label
MATCH (u:User {id: 'user-123'})
SET u:Verified
RETURN u;
```

### DELETE - Removing Data
```cypher
// Delete node (only if no relationships)
MATCH (u:User {id: 'user-123'})
DELETE u;

// Delete node and all relationships
MATCH (u:User {id: 'user-123'})
DETACH DELETE u;

// Delete relationship only
MATCH (a:User)-[r:FOLLOWS]->(b:User)
WHERE a.id = 'user-123' AND b.id = 'user-456'
DELETE r;

// Delete properties
MATCH (u:User {id: 'user-123'})
REMOVE u.age, u.verified
RETURN u;
```

### RETURN - Formatting Results
```cypher
// Return nodes
MATCH (u:User)
RETURN u;

// Return specific properties
MATCH (u:User)
RETURN u.id, u.name;

// Alias properties
MATCH (u:User)
RETURN u.name AS userName, u.email AS userEmail;

// Return count
MATCH (u:User)
RETURN count(u) AS totalUsers;

// Return distinct
MATCH (u:User)-[:FOLLOWS]->(friend)
RETURN DISTINCT friend.name;
```

---

## Common Patterns

### Social Graph Patterns

**Followers/Following**:
```cypher
// Get user's followers
MATCH (follower:User)-[:FOLLOWS]->(u:User {id: $userId})
RETURN follower;

// Get who user follows
MATCH (u:User {id: $userId})-[:FOLLOWS]->(following)
RETURN following;

// Mutual follows (friends)
MATCH (a:User {id: $userId})-[:FOLLOWS]->(b:User)
MATCH (b)-[:FOLLOWS]->(a)
RETURN b AS friend;

// Follow suggestions (friends of friends, not already following)
MATCH (u:User {id: $userId})-[:FOLLOWS]->()-[:FOLLOWS]->(suggestion)
WHERE NOT (u)-[:FOLLOWS]->(suggestion)
  AND u <> suggestion
RETURN DISTINCT suggestion
LIMIT 10;
```

**Blocking**:
```cypher
// Create block relationship
MATCH (a:User {id: $userId})
MATCH (b:User {id: $blockUserId})
MERGE (a)-[:BLOCKED]->(b);

// Get all users except blocked
MATCH (u:User)
WHERE NOT (:User {id: $currentUserId})-[:BLOCKED]->(u)
  AND NOT (u)-[:BLOCKED]->(:User {id: $currentUserId})
RETURN u;
```

### Hierarchy Patterns

**Organizational structure**:
```cypher
// Find all reports (direct and indirect)
MATCH (manager:Person {id: $managerId})-[:MANAGES*]->(report:Person)
RETURN report;

// Find direct reports only
MATCH (manager:Person {id: $managerId})-[:MANAGES]->(report:Person)
RETURN report;

// Find manager chain up to CEO
MATCH path = (person:Person {id: $personId})-[:REPORTS_TO*]->(ceo:Person)
WHERE NOT (ceo)-[:REPORTS_TO]->()
RETURN nodes(path);

// Find all people in same department
MATCH (person:Person {id: $personId})-[:MEMBER_OF]->(dept:Department)
MATCH (colleague:Person)-[:MEMBER_OF]->(dept)
WHERE person <> colleague
RETURN colleague;
```

**Category hierarchies**:
```cypher
// Find all subcategories
MATCH (parent:Category {id: $categoryId})-[:PARENT_OF*]->(child:Category)
RETURN child;

// Find path to root category
MATCH path = (cat:Category {id: $categoryId})-[:CHILD_OF*]->(root:Category)
WHERE NOT (root)-[:CHILD_OF]->()
RETURN nodes(path);
```

### Recommendation Patterns

**Collaborative filtering**:
```cypher
// Users who liked similar items
MATCH (u:User {id: $userId})-[:LIKED]->(item:Item)
MATCH (item)<-[:LIKED]-(other:User)
MATCH (other)-[:LIKED]->(recommendation:Item)
WHERE NOT (u)-[:LIKED]->(recommendation)
RETURN recommendation, count(*) AS score
ORDER BY score DESC
LIMIT 10;

// Weighted recommendations
MATCH (u:User {id: $userId})-[r1:LIKED]->(item:Item)
MATCH (item)<-[r2:LIKED]-(other:User)
MATCH (other)-[r3:LIKED]->(recommendation:Item)
WHERE NOT (u)-[:LIKED]->(recommendation)
WITH recommendation,
     sum(r1.weight * r2.weight * r3.weight) AS score
RETURN recommendation
ORDER BY score DESC
LIMIT 10;
```

**Content-based filtering**:
```cypher
// Items similar to liked items
MATCH (u:User {id: $userId})-[:LIKED]->(item:Item)
MATCH (item)-[:HAS_TAG]->(tag:Tag)
MATCH (tag)<-[:HAS_TAG]-(similar:Item)
WHERE NOT (u)-[:LIKED]->(similar)
  AND item <> similar
RETURN similar, count(tag) AS commonTags
ORDER BY commonTags DESC
LIMIT 10;
```

### Path Finding

**Shortest path**:
```cypher
// Shortest path between two users
MATCH path = shortestPath(
  (a:User {id: $userId1})-[:FOLLOWS*]-(b:User {id: $userId2})
)
RETURN path, length(path);

// All shortest paths
MATCH path = allShortestPaths(
  (a:User {id: $userId1})-[:FOLLOWS*]-(b:User {id: $userId2})
)
RETURN path;
```

**Dijkstra's algorithm** (weighted paths):
```cypher
// Find cheapest route
CALL gds.shortestPath.dijkstra.stream('graph', {
  sourceNode: $startNodeId,
  targetNode: $endNodeId,
  relationshipWeightProperty: 'cost'
})
YIELD path, totalCost
RETURN path, totalCost;
```

### Access Control

**Permission hierarchies**:
```cypher
// Check if user has permission
MATCH (u:User {id: $userId})-[:HAS_ROLE]->(role:Role)
MATCH (role)-[:HAS_PERMISSION*0..]->(permission:Permission {name: $permissionName})
RETURN count(permission) > 0 AS hasPermission;

// Get all user permissions (including inherited)
MATCH (u:User {id: $userId})-[:HAS_ROLE]->(role:Role)
MATCH (role)-[:HAS_PERMISSION*0..]->(permission:Permission)
RETURN DISTINCT permission;
```

---

## Performance Optimization

### Indexes and Constraints

**Unique constraints** (automatically create index):
```cypher
// Unique user ID
CREATE CONSTRAINT user_id_unique
FOR (u:User) REQUIRE u.id IS UNIQUE;

// Unique email
CREATE CONSTRAINT user_email_unique
FOR (u:User) REQUIRE u.email IS UNIQUE;
```

**Regular indexes**:
```cypher
// Index on property
CREATE INDEX user_name_index
FOR (u:User) ON (u.name);

// Composite index
CREATE INDEX user_location_index
FOR (u:User) ON (u.city, u.country);

// Full-text search
CREATE FULLTEXT INDEX user_search_index
FOR (u:User) ON EACH [u.name, u.bio, u.email];
```

**Use indexes**:
```cypher
// Full-text search
CALL db.index.fulltext.queryNodes('user_search_index', 'Alice')
YIELD node, score
RETURN node, score;
```

### Query Optimization

**Use PROFILE to analyze**:
```cypher
PROFILE
MATCH (u:User {id: $userId})-[:FOLLOWS*1..3]->(friend)
RETURN friend;
```

**Optimization tips**:

**1. Start with most specific nodes**:
```cypher
// ✗ Bad: Starts with all users
MATCH (u:User)-[:FOLLOWS]->(friend:User {id: $friendId})
RETURN u;

// ✓ Good: Starts with specific user
MATCH (u:User)-[:FOLLOWS]->(friend:User)
WHERE friend.id = $friendId
RETURN u;
```

**2. Limit relationship depth**:
```cypher
// ✗ Bad: Unbounded traversal
MATCH (u:User {id: $userId})-[:FOLLOWS*]->(friend)
RETURN friend;

// ✓ Good: Bounded traversal
MATCH (u:User {id: $userId})-[:FOLLOWS*1..3]->(friend)
RETURN friend;
```

**3. Use LIMIT early**:
```cypher
// ✓ Good: Limit before expensive operations
MATCH (u:User)
RETURN u
ORDER BY u.createdAt DESC
LIMIT 10;
```

**4. Avoid Cartesian products**:
```cypher
// ✗ Bad: Creates cartesian product
MATCH (a:User), (b:User)
WHERE a.city = b.city
RETURN a, b;

// ✓ Good: Connect via relationship or property
MATCH (a:User)-[:LIVES_IN]->(city:City)<-[:LIVES_IN]-(b:User)
RETURN a, b;
```

### Batch Operations

**Bulk create**:
```cypher
// Create many nodes efficiently
UNWIND $users AS userData
MERGE (u:User {id: userData.id})
SET u.name = userData.name, u.email = userData.email;

// Create many relationships
UNWIND $follows AS follow
MATCH (a:User {id: follow.followerId})
MATCH (b:User {id: follow.followedId})
MERGE (a)-[:FOLLOWS {since: follow.since}]->(b);
```

**Use APOC for batching**:
```cypher
// Process in batches of 1000
CALL apoc.periodic.iterate(
  "MATCH (u:User) RETURN u",
  "SET u.processed = true",
  {batchSize: 1000}
);
```

---

## Schema Design

### Modeling Guidelines

**Nodes**: Represent entities
```cypher
(:User)
(:Post)
(:Comment)
(:Tag)
```

**Relationships**: Represent connections
```cypher
(:User)-[:POSTED]->(:Post)
(:User)-[:COMMENTED]->(:Comment)
(:Comment)-[:ON]->(:Post)
(:Post)-[:TAGGED]->(:Tag)
```

**Properties**: Store attributes
```cypher
// On nodes
User {id, name, email, createdAt}

// On relationships
FOLLOWS {since, strength}
LIKED {rating, timestamp}
```

### When to Use Relationships vs Properties

**Use relationship when**:
- Connection between entities
- Need to query traversals
- Connection has properties
- Many-to-many relationship
```cypher
// ✓ Good: Relationship
(user:User)-[:LIKED {rating: 5}]->(post:Post)
```

**Use property when**:
- Simple value
- Doesn't need traversal
- One-to-one relationship
- Rarely queried independently
```cypher
// ✓ Good: Property
(:User {email: 'alice@example.com'})
```

### Multiple Labels

**Use multiple labels for**:
- Shared behaviour
- Polymorphism
- Categorization
```cypher
// User can be both Person and Developer
CREATE (p:Person:Developer {name: 'Alice'})

// Query specific type
MATCH (d:Developer)
RETURN d;

// Query any person
MATCH (p:Person)
RETURN p;
```

---

## Integration with PostgreSQL/Supabase

### Shared Primary Keys

**Use same UUIDs**:
```typescript
// Create in PostgreSQL
const { data: user } = await supabase
  .from('users')
  .insert({
    id: userId,
    email: 'alice@example.com',
    name: 'Alice'
  });

// Create in Neo4j
await neo4j.run(`
  CREATE (u:User {
    id: $userId,
    name: $name
  })
`, { userId, name: user.name });
```

### Data Synchronization

**Event-driven sync**:
```typescript
// PostgreSQL trigger → Sync to Neo4j
supabase
  .from('users')
  .on('INSERT', async (payload) => {
    await neo4j.run(`
      MERGE (u:User {id: $id})
      SET u.name = $name, u.email = $email
    `, payload.record);
  })
  .subscribe();
```

**Batch sync**:
```typescript
// Bulk sync from PostgreSQL to Neo4j
const { data: users } = await supabase
  .from('users')
  .select('*');

await neo4j.run(`
  UNWIND $users AS userData
  MERGE (u:User {id: userData.id})
  SET u.name = userData.name,
      u.email = userData.email
`, { users });
```

### Query Patterns

**Hybrid queries**:
```typescript
// Get user from PostgreSQL
const { data: user } = await supabase
  .from('users')
  .select('*')
  .eq('id', userId)
  .single();

// Get social graph from Neo4j
const result = await neo4j.run(`
  MATCH (u:User {id: $userId})
  MATCH (u)-[:FOLLOWS]->(following:User)
  MATCH (follower:User)-[:FOLLOWS]->(u)
  RETURN
    count(DISTINCT following) as followingCount,
    count(DISTINCT follower) as followerCount
`, { userId });

// Combine results
return {
  ...user,
  social: {
    followingCount: result.records[0].get('followingCount'),
    followerCount: result.records[0].get('followerCount')
  }
};
```

---

## Portfolio Evidence

**KSBs Demonstrated**:
- **S6**: Design and Implement Database Systems (graph modeling)
- **S1**: Analyse Requirements (choosing graph for relationships)
- **S8**: Create Analysis Artefacts (query optimization)

**How to Document**:
- Schema diagrams showing graph structure
- Query examples with performance comparisons
- Explain why graph chosen over relational
- Document traversal patterns
- Show integration with other databases

---

## Success Criteria

Neo4j implementation is successful when:
- Queries leverage graph traversal strengths
- Indexes on frequently queried properties
- Bounded traversals (not unbounded `*`)
- Clear distinction between nodes/relationships/properties
- Integration with relational database clean
- Performance acceptable for use case
- Schema supports future requirements
