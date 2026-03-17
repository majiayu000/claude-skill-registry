---
name: graphql-architect
description: GraphQL schema and federation expert specializing in resolver optimization, subscriptions, and API gateway patterns
---

# GraphQL Architect Skill

## Purpose

Provides expert GraphQL architecture expertise specializing in schema design, federation patterns, resolver optimization, and real-time subscriptions. Builds performant, type-safe GraphQL APIs with N+1 prevention, efficient caching, and scalable API gateway patterns across distributed systems.

## When to Use

- Designing GraphQL schema from scratch for new APIs
- Implementing GraphQL federation across multiple services
- Optimizing resolvers to prevent N+1 queries (DataLoader implementation)
- Building real-time features with GraphQL subscriptions
- Migrating from REST to GraphQL or designing hybrid REST+GraphQL APIs
- Implementing GraphQL API gateway patterns

## Quick Start

**Invoke this skill when:**
- Designing new GraphQL schemas or federation architecture
- Solving N+1 query performance issues
- Implementing real-time subscriptions
- Migrating REST APIs to GraphQL

**Do NOT invoke when:**
- Simple REST API is sufficient (use api-designer)
- Database schema design without API layer (use database-administrator)
- Frontend data fetching only (use frontend-developer)

## Core Capabilities

### Schema Design
- Creating type-safe GraphQL schemas with best practices
- Implementing pagination patterns (Relay, offset-based)
- Designing mutations with input validation and error handling
- Managing schema evolution and backward compatibility

### Federation Architecture
- Implementing Apollo Federation for microservices
- Configuring schema stitching for service composition
- Managing cross-service queries and mutations
- Setting up API gateways for schema composition

### Resolver Optimization
- Implementing DataLoader for N+1 prevention
- Caching strategies at resolver and field levels
- Query complexity analysis and depth limiting
- Persisted queries for production optimization

### Real-Time Subscriptions
- Implementing WebSocket-based subscriptions
- Managing subscription lifecycle and cleanup
- Integrating with event-driven backends
- Handling subscription authentication and authorization

## Decision Framework

### GraphQL vs REST Decision Matrix

| Factor | Use GraphQL | Use REST |
|--------|-------------|----------|
| **Client types** | Multiple clients with different needs | Single client with predictable needs |
| **Data relationships** | Highly nested, interconnected data | Flat resources with few relationships |
| **Over-fetching** | Clients need different subsets | Clients typically need all fields |
| **Under-fetching** | Avoid multiple round trips | Single endpoint provides enough |
| **Schema evolution** | Frequent changes, backward compat | Stable API, versioning acceptable |
| **Real-time** | Subscriptions needed | Polling or webhooks sufficient |

### Schema Design Decision Tree

```
Schema Design Requirements
│
├─ Single service (monolith)?
│  └─ Schema-first design with single schema
│
├─ Multiple microservices?
│  ├─ Services owned by different teams?
│  │  └─ Apollo Federation
│  └─ Services owned by same team?
│     └─ Schema stitching (simpler)
│
├─ Existing REST APIs to wrap?
│  └─ GraphQL wrapper layer
│
└─ Need backward compatibility?
   └─ Hybrid REST + GraphQL
```

### N+1 Prevention Strategy

```
Resolver Implementation
│
├─ Field resolves to single related entity?
│  └─ DataLoader with batching
│
├─ Field resolves to list of related entities?
│  ├─ List size always small (<10)?
│  │  └─ Direct query acceptable
│  └─ List size unbounded?
│     └─ DataLoader with batching + pagination
│
├─ Nested resolvers (users → posts → comments)?
│  └─ Multi-level DataLoaders
│
└─ Aggregations or counts?
   └─ Separate DataLoader for counts
```

## Core Workflow: DataLoader Implementation

**Problem**: N+1 queries killing performance

```typescript
// WITHOUT DataLoader - N+1 problem
const resolvers = {
  Post: {
    author: async (post, _, { db }) => {
      // Executed once per post (N+1 problem!)
      return db.User.findByPk(post.userId);
    }
  }
};
// Query for 100 posts triggers 101 DB queries
```

**Solution**: Batch with DataLoader

```typescript
import DataLoader from 'dataloader';

// Create loader per request (important!)
function createLoaders(db) {
  return {
    userLoader: new DataLoader(async (userIds) => {
      const users = await db.User.findAll({
        where: { id: userIds }
      });
      // Return in same order as requested IDs
      const userMap = new Map(users.map(u => [u.id, u]));
      return userIds.map(id => userMap.get(id));
    })
  };
}

// Resolver using DataLoader
const resolvers = {
  Post: {
    author: (post, _, { loaders }) => {
      return loaders.userLoader.load(post.userId);
    }
  }
};
// Same query now triggers 2 queries total!
```

## Quick Reference: Schema Best Practices

### Pagination Pattern (Relay-style)

```graphql
type Query {
  users(first: Int, after: String, last: Int, before: String): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### Error Handling Pattern

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type CreateUserPayload {
  user: User
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  NOT_FOUND
  UNAUTHORIZED
  CONFLICT
}
```

## Red Flags - When to Escalate

| Observation | Why Escalate |
|-------------|--------------|
| Query complexity explosion | Unbounded nested queries causing DoS |
| Federation circular dependencies | Schema design issue |
| 10K+ concurrent subscriptions | Infrastructure architecture |
| Schema versioning across 50+ fields | Breaking change management |
| Cross-service transaction needs | Distributed systems pattern |

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
  - Apollo Federation setup workflow
  - Field-level authorization directives
  - Query complexity limiting
  
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
  - Anti-patterns (N+1 queries, no complexity limits)
  - Integration patterns with other skills
  - Complete resolver implementations
