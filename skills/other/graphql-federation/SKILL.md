---
name: graphql-federation
description: |
  GraphQL Federation skill for creating correct federation subgraphs. Use when: (1) Creating new federation subgraphs, (2) Adding entities with @key directives, (3) Extending types across subgraphs, (4) Using federation directives (@shareable, @external, @override, @provides, @requires, @inaccessible, @interfaceObject, @authenticated, @requiresScopes), (5) Debugging composition errors, (6) Understanding federation rules and patterns.
  MANDATORY TRIGGERS: federation, subgraph, @key, entity, federated graph, supergraph, GraphQL composition, router schema
---

# GraphQL Federation Skill

Create correct GraphQL federation subgraphs following WunderGraph Cosmo composition rules.

## Core Concepts

**Subgraph**: A GraphQL microservice contributing to the federated graph.
**Federated Graph/Supergraph**: The composed GraphQL interface for clients.
**Router**: Plans operations, routes requests to subgraphs, joins data.
**Entity**: A type with `@key` directive resolvable across subgraphs.
**Router Schema vs Client Schema**: Router sees all fields; clients don't see `@inaccessible` items.

## Essential Directives

### @key - Define Entities

```graphql
# Basic entity
type User @key(fields: "id") {
  id: ID!
  name: String!
}

# Multiple keys
type Product @key(fields: "id") @key(fields: "sku") {
  id: ID!
  sku: String!
  name: String!
}

# Composite key
type Review @key(fields: "author { id } product { id }") {
  author: User!
  product: Product!
  rating: Int!
}

# Non-resolvable key (reference only, can't resolve this entity)
type User @key(fields: "id", resolvable: false) {
  id: ID!
}
```

**Key Rules:**
- Key fields cannot have arguments
- Key fields cannot be abstract types (interfaces/unions)
- Key fields must select leaf scalars or nested objects with selections
- Multiple keys provide alternative resolution paths

### @shareable - Allow Multiple Definitions

```graphql
# When same field exists in multiple subgraphs
type User @key(fields: "id") {
  id: ID!
  name: String! @shareable  # Can be defined in other subgraphs
}

# Object-level shareable applies to all fields
type User @key(fields: "id") @shareable {
  id: ID!
  name: String!
  email: String!
}
```

**Shareable Rules:**
- Fields defined in multiple subgraphs MUST be @shareable
- Key fields used in other subgraphs' keys must be @shareable
- Root type fields (Query, Mutation) are implicitly shareable

### @external - Reference External Fields

```graphql
# Mark fields resolved by another subgraph
extend type User @key(fields: "id") {
  id: ID! @external
  name: String! @external
  reviews: [Review!]!  # This subgraph resolves reviews
}
```

**External Rules:**
- Use on key fields when extending entities
- Use on fields referenced in @requires
- Use on fields referenced in @provides
- External fields are NOT resolved by this subgraph

### @requires - Depend on External Data

```graphql
type Product @key(fields: "id") {
  id: ID!
  price: Float! @external
  currency: String! @external
  formattedPrice: String! @requires(fields: "price currency")
}
```

**Requires Rules:**
- Referenced fields must be @external
- Can reference nested fields: `@requires(fields: "details { weight }")`
- Router fetches required fields before calling this resolver

### @provides - Declare Additional Fields

```graphql
type Query {
  topProducts: [Product!]! @provides(fields: "name description")
}

type Product @key(fields: "id") {
  id: ID!
  name: String! @external
  description: String! @external
}
```

**Provides Rules:**
- Declares that a resolver provides additional fields
- Referenced fields must be @external in this subgraph
- Optimizes router query planning

### @override - Transfer Field Ownership

```graphql
# In new subgraph, taking over from "old-service"
type User @key(fields: "id") {
  id: ID!
  name: String! @override(from: "old-service")
}
```

**Override Rules:**
- Cannot override from same subgraph
- Overridden field in source doesn't need @shareable
- Used for gradual migration between subgraphs

### @inaccessible - Hide from Client Schema

```graphql
type User @key(fields: "id") {
  id: ID!
  name: String!
  internalId: String! @inaccessible  # Hidden from clients
}

# Entire type can be inaccessible
type InternalMetrics @inaccessible {
  requestCount: Int!
}
```

**Inaccessible Rules:**
- Field exists in router schema but not client schema
- Still subject to @shareable rules
- All fields on a type cannot be @inaccessible (type becomes useless)
- Required arguments cannot be @inaccessible alone

### @interfaceObject - Treat Interface as Object

```graphql
# Subgraph A defines the interface
interface Media @key(fields: "id") {
  id: ID!
  title: String!
}

type Book implements Media @key(fields: "id") {
  id: ID!
  title: String!
  author: String!
}

# Subgraph B adds fields to ALL implementations
type Media @key(fields: "id") @interfaceObject {
  id: ID!
  reviews: [Review!]!  # Added to Book and all Media types
}
```

**InterfaceObject Rules:**
- Cannot define implementations alongside @interfaceObject
- Fields propagate to all concrete implementations
- Must have @key matching the interface's key

### Authorization Directives

```graphql
type Query {
  publicData: String!
  privateData: String! @authenticated
  adminData: String! @requiresScopes(scopes: [["admin"], ["superuser"]])
}

# Type-level auth
type SecretDocument @authenticated @requiresScopes(scopes: [["read:secrets"]]) {
  content: String!
}
```

## Common Patterns

### Entity Extension

```graphql
# Subgraph A - owns User
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

# Subgraph B - extends User with posts
extend type User @key(fields: "id") {
  id: ID! @external
  posts: [Post!]!
}

type Post @key(fields: "id") {
  id: ID!
  title: String!
  author: User!
}
```

### Federated Mutations

```graphql
type Mutation {
  createUser(input: CreateUserInput!): User!
}

# Entity returned from mutation allows field resolution from other subgraphs
type User @key(fields: "id") {
  id: ID!
  name: String!
}
```

### Interface Entities

```graphql
interface Node @key(fields: "id") {
  id: ID!
}

type User implements Node @key(fields: "id") {
  id: ID!
  name: String!
}

type Product implements Node @key(fields: "id") {
  id: ID!
  title: String!
}
```

## Error Prevention

### Shareability Errors

```graphql
# ERROR: Field defined in multiple subgraphs without @shareable
# Subgraph A
type User @key(fields: "id") {
  id: ID!
  name: String!  # Missing @shareable
}

# Subgraph B
type User @key(fields: "id") {
  id: ID!
  name: String!  # Conflict!
}

# FIX: Add @shareable to both
type User @key(fields: "id") {
  id: ID!
  name: String! @shareable
}
```

### Resolvability Errors

```graphql
# ERROR: Field cannot be resolved from Query entry point
# Subgraph A
type Query {
  user: User!  # Only in A
}

type User {
  id: ID!
  name: String!  # Only in A
}

# Subgraph B
type User {
  email: String!  # Only in B, but User has no @key!
}

# FIX: Add @key to make User an entity
type User @key(fields: "id") {
  id: ID!
  name: String!
}
```

### External Field Errors

```graphql
# ERROR: @requires on non-external field
type Product @key(fields: "id") {
  id: ID!
  price: Float!  # Missing @external
  formattedPrice: String! @requires(fields: "price")
}

# FIX: Mark as external
type Product @key(fields: "id") {
  id: ID!
  price: Float! @external
  formattedPrice: String! @requires(fields: "price")
}
```

## Reference Files

For detailed directive specifications, see:
- `references/directives.md` - Complete directive documentation
- `references/composition-rules.md` - Composition validation rules
- `references/patterns.md` - Advanced federation patterns
