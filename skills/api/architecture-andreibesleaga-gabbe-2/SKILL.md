---
name: graphql-schema
description: Schema design, federation, and resolution strategies.
role: eng-api
triggers:
  - graphql
  - schema
  - resolver
  - federation
  - apollo
  - gql
---

# graphql-schema Skill

This skill prevents "Graph Spaghetti" and ensuring performant Graph APIs.

## 1. Schema Design
- **Consumption-First**: Design for the UI needs, not the DB schema.
- **Naming**: `User.posts` (Good), `User.getPosts` (Bad - it's a field, not a method).
- **Nullability**:
  - Default to **Nullable** for fields (resilience: if one field fails, partial data returns).
  - Use **Non-Null (!)** only for IDs and essential arguments.

## 2. N+1 Problem (The Graph Killer)
- **Scenario**: Querying `users { posts { comments } }`.
- **Solution**: **DataLoader** pattern.
  - Batches IDs from multiple resolvers.
  - Runs *one* DB query: `SELECT * FROM posts WHERE user_id IN (1, 2, 3)`.
  - Distributes results back to resolvers.

## 3. Pagination
- Avoid `offset`/`limit`.
- Use **Relay Connection Specification** (Cursor-based):
  ```graphql
  users(first: 10, after: "cursor") {
    edges {
      node { name }
      cursor
    }
    pageInfo { hasNextPage }
  }
  ```

## 4. Security
- **Depth Limiting**: Block queries deeper than 5 levels (prevent cyclic recursion DoS).
- **Cost Analysis**: Assign points to fields. Block query if Cost > 1000.
- **Introspection**: Disable in Production.

## 5. Federation (Apollo)
- Use when splitting Graph across microservices.
- **Entity**: A type shared across subgraphs (`@key(fields: "id")`).
- **Gateway**: Composes the Supergraph.
