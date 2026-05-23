---
name: graphql
description: |
  Provides GraphQL API schema design and implementation expertise. Ensures proper type definitions, query/mutation patterns, pagination strategies, and error handling standards. Specializes in schema-first design, resolver implementation, DataLoader for N+1 prevention, subscription patterns, and federation architecture. Implements Relay cursor connections and Apollo best practices.
  Use when: designing GraphQL schemas, defining types and interfaces, implementing queries and mutations, creating resolvers, designing pagination with connections and edges, solving N+1 query problems with DataLoader, implementing subscriptions for real-time updates, handling errors and nullability, setting up GraphQL federation, or integrating with Apollo Server/Client or other GraphQL libraries.
---

# GraphQL API Standards

## Naming Conventions

### Field Naming

- Boolean: Require `is/has/can` prefix
- Date: Require `~At` suffix
- Use consistent terminology throughout the project (unify on either "create" or "add")

## Date Format

- ISO 8601 UTC
- Use DateTime type

## Pagination

### Relay Connection Specification

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

- Parameters: `first`, `after`

## Sorting

- `orderBy: [{ field: "createdAt", order: DESC }]`

## Type Naming

- Input: `{Verb}{Type}Input`
- Connection: `{Type}Connection`
- Edge: `{Type}Edge`

## Input

- Separate creation and modification (required for creation, optional for modification)
- Avoid nesting - IDs only

## Errors

### extensions (default)

- `code`, `field` in `errors[].extensions`

### Union (type safety)

- `User | ValidationError`

## N+1

- DataLoader is mandatory

## Documentation

- `"""description"""` is required
- Explicitly state Input constraints

## Deprecation

- `@deprecated(reason: "...")`
- Never delete types
