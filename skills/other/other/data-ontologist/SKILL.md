---
name: data-ontologist
description: This skill should be used when the user mentions "database design", "schema design", "graph database", "document database", "polyglot persistence", "data modeling", "Neo4j", "Supabase", "PostgreSQL", "MongoDB", discusses database architecture, choosing databases, or integrating multiple databases. Addresses when to use relational vs graph vs document databases and integration patterns.
version: 1.0.0
---

# Polyglot Persistence Architecture

Architectural guidance for using multiple database technologies together, with emphasis on PostgreSQL/Supabase (relational), Neo4j (graph), and MongoDB (document). Demonstrates when to use each database type and how to integrate them effectively.

---

## When This Skill Applies

Use this skill when:
- Designing data architecture for new projects
- Choosing between relational, graph, and document databases
- Integrating multiple database types
- Schema design decisions
- Query optimization across databases
- Migration strategies
- Questions about when to use which database paradigm

---

## Core Principle

**Start with the graph. Optimise from there.**

Most real-world domains are fundamentally about relationships. The graph is the truest representation of how entities connect. Start by thinking in nodes and edges — then decide where to persist based on access patterns and consistency needs.

**Right database for right data concern**

Don't force all data into one database type. Use:
- **Relational (PostgreSQL/Supabase)** - Structured data, transactions, strong consistency
- **Graph (Neo4j)** - Relationships as primary concern, traversal queries
- **Document (MongoDB)** - Semi-structured data, flexible schemas, nested documents

### Graph-First Modelling Process

Before choosing databases, model the domain as a graph:

1. **Identify nodes** — What are the entities? (Users, Courses, Organisations, Products)
2. **Identify edges** — How do they connect? (ENROLLED_IN, REPORTS_TO, PURCHASED)
3. **Annotate edges** — Do relationships carry data? (role, since, quantity)
4. **Spot patterns** — Trees? DAGs? Social graphs? Bipartite structures?
5. **Then persist** — Given the graph, which parts need relational guarantees, which need traversal, which need flexible schemas?

```cypher
// Step 1-3: Model the domain as a graph first
(:User)-[:MEMBER_OF {role: 'admin', since: date}]->(:Organisation)
(:User)-[:ENROLLED_IN {status: 'active'}]->(:Course)
(:Course)-[:REQUIRES]->(:Course)
(:User)-[:COMPLETED {score: 0.85}]->(:Module)
(:Module)-[:BELONGS_TO]->(:Course)
```

Then decide:
- Users and Organisations → **PostgreSQL** (transactional, auth, billing)
- MEMBER_OF, ENROLLED_IN, REQUIRES → **Neo4j** (traversal, recommendations, paths)
- Course content, Module materials → **MongoDB** (flexible nested content)

---

## When to Use Relational (PostgreSQL/Supabase)

### Strong Fit

**Transactional Data**:
- User accounts and authentication
- Order processing
- Financial records
- Inventory management

**Structured Records**:
- Clear schema with defined fields
- Data fits naturally into tables
- ACID guarantees required
- Standard CRUD operations
- Strong data integrity constraints

**Examples**:
```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Orders table
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  total DECIMAL(10,2),
  status TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Weak Fit

**Highly Connected Data**:
- Social networks (many-to-many relationships)
- Recommendation engines
- Organizational hierarchies with flexible depth

**Reason**: Joins become expensive, recursive queries complex.

**Rapidly Evolving Schemas**:
- Frequently adding new fields
- Different record types need different fields
- Exploratory data modeling

**Reason**: Migrations expensive, rigid structure.

---

## When to Use Graph (Neo4j)

### Strong Fit

**Relationships as Primary Concern**:
- Social graphs (followers, friends, connections)
- Recommendation systems (collaborative filtering)
- Knowledge graphs
- Access control with inheritance
- Dependencies and prerequisites

**Variable-Depth Traversals**:
- "Find all users within 3 degrees"
- "Shortest path between entities"
- "All ancestors in org chart"
- "Courses needed before advanced topic"

**Examples**:
```cypher
// Social connections
(:User)-[:FOLLOWS]->(:User)
(:User)-[:BLOCKED]->(:User)

// Learning paths
(:Course)-[:REQUIRES]->(:Course)
(:User)-[:COMPLETED]->(:Course)

// Organizational structure
(:Person)-[:REPORTS_TO]->(:Person)
(:Person)-[:MEMBER_OF]->(:Team)
```

### Weak Fit

**Simple Lookups**:
- User by email
- Order by ID
- Product details

**Reason**: Relational databases excel at indexed lookups.

**Large Aggregations**:
- Sum all orders this month
- Count users by region
- Analytics dashboards

**Reason**: SQL aggregations and window functions more powerful.

---

## When to Use Document (MongoDB)

### Strong Fit

**Semi-Structured Data**:
- Content management systems (blog posts, articles)
- Product catalogs with varying attributes
- User-generated content
- Configuration data
- API responses that need storage

**Nested/Embedded Data**:
- Comments within posts
- Order items within orders
- Addresses within user profiles
- Metadata with varying fields

**Flexible Schemas**:
- Rapid prototyping
- Evolving data models
- Different document types in same collection
- Optional fields vary by record

**Examples**:
```javascript
// Blog post with embedded comments
{
  _id: ObjectId("..."),
  title: "Getting Started with SvelteKit",
  slug: "getting-started-sveltekit",
  author: {
    id: "user-123",
    name: "Alice"
  },
  content: "...",
  tags: ["svelte", "javascript", "tutorial"],
  comments: [
    {
      id: "comment-1",
      userId: "user-456",
      text: "Great article!",
      createdAt: ISODate("2024-01-15")
    }
  ],
  metadata: {
    views: 1250,
    readingTime: "5 min"
  },
  publishedAt: ISODate("2024-01-10")
}

// Product with varying attributes
{
  _id: ObjectId("..."),
  name: "Laptop",
  category: "electronics",
  price: 999.99,
  specs: {
    cpu: "Intel i7",
    ram: "16GB",
    storage: "512GB SSD",
    screen: "15.6 inch"
  }
}

// Different product type, different fields
{
  _id: ObjectId("..."),
  name: "T-Shirt",
  category: "clothing",
  price: 29.99,
  sizes: ["S", "M", "L", "XL"],
  colors: ["black", "white", "blue"],
  material: "100% cotton"
}
```

### Weak Fit

**Complex Transactions**:
- Multi-step financial operations
- Strong ACID guarantees across documents
- Complex foreign key relationships

**Reason**: Relational databases better at multi-document transactions.

**Relationship-Heavy Data**:
- Social networks
- Graph traversals
- "Friends of friends" queries

**Reason**: Graph databases handle this natively.

**Highly Normalized Data**:
- No duplication tolerance
- Frequent joins needed
- Strong referential integrity

**Reason**: Relational databases enforce this better.

---

## Decision Framework

### Question 1: What's the primary data concern?

**RELATIONSHIPS** → Neo4j (Graph)
- Social connections
- Recommendations
- Dependency trees
- Path finding

**STRUCTURED ENTITIES** → PostgreSQL (Relational)
- User accounts
- Financial transactions
- Inventory
- Orders

**DOCUMENTS/CONTENT** → MongoDB (Document)
- Blog posts
- Product catalogs
- CMS content
- API data storage

### Question 2: How stable is your schema?

**VERY STABLE** → PostgreSQL
- Well-defined entities
- Clear field types
- Rare schema changes
- Strong typing needed

**EVOLVING** → MongoDB
- Prototyping phase
- Frequently adding fields
- Different record structures
- Flexible modeling

**SCHEMA-OPTIONAL** → Neo4j
- Relationships more important than structure
- Dynamic properties
- Graph structure evolves

### Question 3: How is data accessed?

**BY KEY/ID** → PostgreSQL or MongoDB
- User by email
- Product by SKU
- Order by ID

**BY TRAVERSAL** → Neo4j
- Friends of friends
- Shortest path
- Recommendations

**BY CONTENT/QUERY** → MongoDB
- Full-text search
- Filtering nested documents
- Flexible queries on varying fields

### Question 4: Do you need strong consistency?

**ABSOLUTE** → PostgreSQL
- Financial transactions
- ACID guarantees
- Multi-step operations

**EVENTUAL OKAY** → MongoDB or Neo4j
- Content updates
- Social interactions
- Non-critical data

### Question 5: Is data naturally nested?

**YES** → MongoDB
- Posts with comments
- Orders with line items
- Documents with metadata

**NO** → PostgreSQL
- Flat entities
- Many-to-many relationships
- Normalized structure

---

## Real-World Examples

### Example 1: Social Application (WorkWise)

**Supabase (PostgreSQL)**:
- User authentication and profiles
- Organization/company records
- Subscription billing
- Audit logs

**Neo4j**:
- Social connections (followers, following)
- Content interactions (likes, shares)
- Recommendation engine
- Activity feed generation

**MongoDB**:
- User-generated posts/content
- Comments and nested discussions
- Rich media metadata
- Activity logs with flexible structure

**Why All Three?**:
- Auth needs ACID (Supabase)
- Social graph needs traversal (Neo4j)
- Posts need flexible schema (MongoDB)
- User lookups fast in PG
- "People you may know" fast in Neo4j
- Content queries flexible in MongoDB

### Example 2: Learning Platform (Rhea)

**Supabase (PostgreSQL)**:
- User accounts and enrollment
- Payment transactions
- Progress tracking (completion %)
- Subscriptions

**Neo4j**:
- Course prerequisites and dependencies
- Learning path recommendations
- Skill relationships
- "What should I learn next?" queries

**MongoDB**:
- Course content (lessons, modules)
- Rich lesson materials (videos, exercises, notes)
- Student submissions and feedback
- Curriculum templates

**Why All Three?**:
- Enrollment is transactional (Supabase)
- Prerequisites are graph traversal (Neo4j)
- Course content is nested documents (MongoDB)
- Payment requires ACID (PG)
- Learning paths require traversal (Neo4j)
- Lessons have varying structures (MongoDB)

### Example 3: E-commerce Platform

**Supabase (PostgreSQL)**:
- User accounts
- Order transactions
- Inventory counts
- Payment records

**Neo4j**:
- Product recommendations
- "Customers who bought X also bought Y"
- Similar products

**MongoDB**:
- Product catalog with varying attributes
- User reviews and ratings
- Shopping cart state
- Product images and metadata

**Why All Three?**:
- Orders need transactions (Supabase)
- Recommendations need graph (Neo4j)
- Products have varying specs (MongoDB)
- Inventory atomic updates (PG)
- "Similar items" fast in graph
- Product attributes flexible in documents

### Example 4: Content Platform (CMS)

**Supabase (PostgreSQL)**:
- User authentication
- User roles and permissions
- Subscription management

**MongoDB**:
- Articles, blog posts, pages
- Media library
- Draft versions
- Comments and nested discussions
- SEO metadata

**Neo4j** (Optional):
- Content relationships
- Tag networks
- Content recommendations

**Why This Mix?**:
- Users need auth (Supabase)
- Content varies by type (MongoDB)
- Articles have nested comments (MongoDB)
- Permissions are relational (PG)
- Tags can be graphed (Neo4j optional)

---

## Integration Patterns

### Pattern 1: Shared Primary Keys

Use same IDs across all databases:
```typescript
const userId = generateId();

// Supabase - Auth and profile
await supabase.from('users').insert({
  id: userId,
  email,
  name
});

// Neo4j - Social graph node
await neo4j.run(`
  CREATE (u:User {id: $userId, name: $name})
`, { userId, name });

// MongoDB - User preferences
await mongo.collection('user_preferences').insertOne({
  _id: userId,
  theme: 'dark',
  notifications: {
    email: true,
    push: false
  }
});
```

### Pattern 2: Reference by ID

Store references, fetch as needed:
```typescript
// MongoDB - Blog post
{
  _id: ObjectId("..."),
  title: "My Post",
  authorId: "user-123",  // Reference to PostgreSQL user
  content: "...",
  tags: ["javascript", "svelte"]
}

// Query pattern
const post = await mongo.collection('posts').findOne({ _id });
const author = await supabase
  .from('users')
  .select('*')
  .eq('id', post.authorId)
  .single();
```

### Pattern 3: Embed vs Reference Decision

**Embed when**:
- Data accessed together
- One-to-few relationship
- Child data not shared
```javascript
// Good: Embed comments in post
{
  title: "My Post",
  comments: [
    { text: "Great!", userId: "user-123" }
  ]
}
```

**Reference when**:
- Data accessed independently
- One-to-many or many-to-many
- Child data shared across parents
```javascript
// Good: Reference author
{
  title: "My Post",
  authorId: "user-123"  // Author data in PostgreSQL
}
```

### Pattern 4: Event-Driven Sync

Keep databases in sync via events:
```typescript
// User created in Supabase
supabase.on('INSERT', 'users', async (payload) => {
  const user = payload.record;
  
  // Create in Neo4j
  await createUserNode(user);
  
  // Create preferences in MongoDB
  await mongo.collection('user_preferences').insertOne({
    _id: user.id,
    theme: 'light',
    notifications: {}
  });
});
```

### Pattern 5: Aggregate from Multiple Sources
```typescript
async function getUserDashboard(userId) {
  // PostgreSQL - Account info
  const account = await supabase
    .from('users')
    .select('*')
    .eq('id', userId)
    .single();
  
  // Neo4j - Social metrics
  const social = await neo4j.run(`
    MATCH (u:User {id: $userId})
    OPTIONAL MATCH (u)-[:FOLLOWS]->(following)
    OPTIONAL MATCH (follower)-[:FOLLOWS]->(u)
    RETURN 
      count(DISTINCT following) as followingCount,
      count(DISTINCT follower) as followerCount
  `, { userId });
  
  // MongoDB - Recent content
  const posts = await mongo
    .collection('posts')
    .find({ authorId: userId })
    .sort({ createdAt: -1 })
    .limit(5)
    .toArray();
  
  return {
    account: account.data,
    social: social.records[0],
    recentPosts: posts
  };
}
```

---

## Schema Design Patterns

### Relational Schema (Supabase)

**Normalized Structure**:
```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Clear foreign keys
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  total DECIMAL(10,2)
);
```

### Graph Schema (Neo4j)

**Labels and Relationships**:
```cypher
// Node labels
(:User)
(:Organization)
(:Course)

// Typed relationships
(:User)-[:MEMBER_OF {role}]->(:Organization)
(:User)-[:FOLLOWS {since}]->(:User)
(:Course)-[:REQUIRES]->(:Course)
```

### Document Schema (MongoDB)

**Flexible Structure**:
```javascript
// Embedded approach (1-to-few)
{
  _id: ObjectId("..."),
  userId: "user-123",
  title: "My Blog Post",
  content: "...",
  comments: [  // Embedded
    {
      id: "comment-1",
      userId: "user-456",
      text: "Great post!",
      createdAt: ISODate("2024-01-15")
    }
  ],
  tags: ["tutorial", "javascript"],
  metadata: {
    views: 150,
    likes: 23
  }
}

// Reference approach (1-to-many)
{
  _id: ObjectId("..."),
  title: "E-commerce Order",
  userId: "user-123",  // Reference
  items: [
    { productId: "prod-789", quantity: 2 },  // Reference
    { productId: "prod-456", quantity: 1 }
  ],
  total: 149.99
}
```

---

## Query Optimization

### PostgreSQL Optimization

**Indexes**:
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);
```

### Neo4j Optimization

**Constraints and Indexes**:
```cypher
CREATE CONSTRAINT user_id_unique
FOR (u:User) REQUIRE u.id IS UNIQUE;

CREATE INDEX user_email
FOR (u:User) ON (u.email);
```

### MongoDB Optimization

**Indexes**:
```javascript
// Single field
db.posts.createIndex({ authorId: 1 });

// Compound index
db.posts.createIndex({ authorId: 1, createdAt: -1 });

// Text search
db.posts.createIndex({ title: "text", content: "text" });

// Embedded field
db.posts.createIndex({ "metadata.views": -1 });
```

**Query Patterns**:
```javascript
// Efficient: Uses index
db.posts.find({ authorId: userId }).sort({ createdAt: -1 });

// Inefficient: Full collection scan
db.posts.find({ "comments.text": /keyword/ });

// Better: Index comment text separately or use aggregation
```

---

## Anti-Patterns

### Don't: Use Document DB for Transactions
```javascript
// ✗ Bad: Complex multi-document transaction in MongoDB
session.startTransaction();
await orders.insertOne({ userId, total });
await inventory.updateOne({ productId }, { $inc: { stock: -1 } });
await session.commitTransaction();
```

**Why**: PostgreSQL designed for this, ACID guarantees stronger.

### Don't: Embed Everything
```javascript
// ✗ Bad: Embedding user data in every post
{
  title: "My Post",
  author: {
    id: "user-123",
    name: "Alice",
    email: "alice@example.com",
    bio: "...",
    avatar: "..."  // Duplicated everywhere!
  }
}
```

**Better**: Store author ID, fetch user data separately.

### Don't: Use Graph for Simple Lookups
```cypher
// ✗ Bad: Using Neo4j for key-value lookup
MATCH (u:User {email: $email})
RETURN u;
```

**Why**: PostgreSQL or MongoDB faster for indexed lookups.

### Don't: Force Relational Patterns into Documents
```javascript
// ✗ Bad: Normalized MongoDB (defeats the purpose)
// users collection
{ _id: "user-123", name: "Alice" }

// posts collection
{ _id: "post-456", authorId: "user-123", title: "..." }

// comments collection
{ _id: "comment-789", postId: "post-456", text: "..." }
```

**Why**: If normalizing this much, use PostgreSQL instead.

---

## Migration Strategies

### Starting Point

**Begin with PostgreSQL**:
- Authentication
- Core transactional data
- Well-understood entities

**Add MongoDB When**:
- Content becomes varied
- Schema evolution frequent
- Nested data structures emerge

**Add Neo4j When**:
- Relationships become complex
- Traversal queries needed
- Recommendations required

### Data Migration Examples

**PostgreSQL → MongoDB**:
```typescript
// Export from PG
const posts = await supabase.from('posts').select('*');

// Transform and insert to MongoDB
await mongo.collection('posts').insertMany(
  posts.map(post => ({
    _id: post.id,
    ...post,
    metadata: {
      views: post.view_count,
      likes: post.like_count
    }
  }))
);
```

**MongoDB → Neo4j** (relationships):
```typescript
// Get follows from MongoDB
const follows = await mongo.collection('follows').find().toArray();

// Create relationships in Neo4j
await neo4j.run(`
  UNWIND $follows AS follow
  MATCH (follower:User {id: follow.followerId})
  MATCH (followed:User {id: follow.followedId})
  CREATE (follower)-[:FOLLOWS {since: follow.createdAt}]->(followed)
`, { follows });
```

---

## Portfolio Evidence

**KSBs Demonstrated**:
- **K2**: All Stages of Software Development Lifecycle (architecture decisions)
- **K3**: Roles and Responsibilities (database selection justification)
- **S1**: Analyse Requirements (choosing right tool for problem)
- **S6**: Design and Implement Database Systems (polyglot approach)

**How to Document**:
- Architecture Decision Records (ADRs) explaining database choices
- Diagrams showing which data lives where
- Performance comparisons (before/after changes)
- Migration scripts and sync strategies
- Trade-off analysis documentation

---

## Success Criteria

Architecture is successful when:
- Each database handles what it does best
- Queries are fast (minimal cross-database operations)
- Data consistency maintained appropriately
- Clear reasoning for database placement
- Can scale databases independently
- Schema evolution manageable
- Team understands the architecture
