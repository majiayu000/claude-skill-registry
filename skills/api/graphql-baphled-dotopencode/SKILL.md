---
name: graphql
description: GraphQL API design and implementation patterns
category: Database Persistence
---

# Skill: graphql

## What I do

I provide GraphQL API expertise: schema design, type hierarchies, resolvers, query/mutation patterns, real-time subscriptions, error handling, pagination, and performance optimisation. I focus on building flexible, type-safe APIs that avoid overfetching and the N+1 query problem through the DataLoader pattern.

## When to use me

- Designing GraphQL schemas (SDL) and type relationships
- Implementing resolvers for queries, mutations, and subscriptions
- Optimising data loading using DataLoaders to batch and cache queries
- Implementing cursor-based pagination (Relay spec) for large datasets
- Designing typed error payloads and schema-level validation
- Aggregating data from multiple microservices or database sources
- Implementing field-level authorisation and query complexity limiting

## Core principles

1. **Schema-First Design** - Define the contract between frontend and backend using a strongly-typed schema before implementation.
2. **Types Model the Domain** - Model types based on domain concepts and client needs, not internal database structures.
3. **Nullable by Default** - Embrace nullability; only use `!` when a field is guaranteed to be present even in error states.
4. **Efficient Data Loading** - Always use the DataLoader pattern to batch field resolution and prevent N+1 query performance issues.
5. **Contract Evolution** - Evolve the schema through deprecation and additive changes; avoid breaking existing clients.

## Patterns & examples

### Schema Design (SDL)
```graphql
type User {
  id: ID!
  name: String!
  orders(first: Int = 10, after: String): OrderConnection!
}

type Query {
  me: User
  user(id: ID!): User
}

type Mutation {
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
}
```

### Resolver with DataLoader (Go)
```go
// OrderResolver batches user lookups across all orders in a list
func (r *orderResolver) User(ctx context.Context, obj *model.Order) (*model.User, error) {
  return GetLoaders(ctx).UserLoader.Load(ctx, obj.UserID)
}
```

### Cursor Pagination (Relay)
```graphql
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
```

## Anti-patterns to avoid

- ❌ Exposing database schema directly as the GraphQL schema.
- ❌ Missing DataLoaders for list resolvers; causes N+1 query degradation.
- ❌ Generic error strings; use typed error payloads with `field` and `message`.
- ❌ Offset pagination for large/frequent datasets; use opaque cursors.
- ❌ Deeply nested queries without depth or complexity limiting (DoS risk).

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Languages/GraphQL.md`

## Related skills

- `api-design` - General API design principles
- `db-operations` - Database and repository patterns
- `sql` - Query optimisation and indexing
- `error-handling` - Typed error patterns
- `security` - Authentication and query depth limiting
- `architecture` - Layer separation with repository pattern
