---
name: graphql-inspector-validate
description: Use when validating GraphQL operations/documents against a schema, checking query depth, complexity, or fragment usage.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# GraphQL Inspector - Validate

Expert knowledge of GraphQL Inspector's validate command for checking operations and documents against a schema with configurable rules.

## Overview

The validate command checks GraphQL operations (queries, mutations, subscriptions) and fragments against a schema. It catches errors like undefined fields, wrong argument types, and invalid fragment spreads before runtime.

## Core Commands

### Basic Validation

```bash
# Validate operations against schema
npx @graphql-inspector/cli validate './src/**/*.graphql' './schema.graphql'

# Validate operations from TypeScript files
npx @graphql-inspector/cli validate './src/**/*.tsx' './schema.graphql'

# Validate with glob patterns
npx @graphql-inspector/cli validate './**/*.{graphql,gql}' './schema.graphql'
```

### Federation Support

```bash
# Apollo Federation V1
npx @graphql-inspector/cli validate './operations/**/*.graphql' './schema.graphql' \
  --federation

# Apollo Federation V2
npx @graphql-inspector/cli validate './operations/**/*.graphql' './schema.graphql' \
  --federationV2

# AWS AppSync directives
npx @graphql-inspector/cli validate './operations/**/*.graphql' './schema.graphql' \
  --aws
```

## Validation Rules

### Depth Limiting

Prevent deeply nested queries that could cause performance issues:

```bash
# Fail if query depth exceeds 10
npx @graphql-inspector/cli validate './src/**/*.graphql' './schema.graphql' \
  --maxDepth 10
```

Example violation:

```graphql
# Depth of 8 - might exceed limit
query DeepQuery {
  user {                     # 1
    posts {                  # 2
      author {               # 3
        followers {          # 4
          posts {            # 5
            comments {       # 6
              author {       # 7
                name         # 8
              }
            }
          }
        }
      }
    }
  }
}
```

### Alias Count

Limit alias usage to prevent response explosion:

```bash
# Max 5 aliases per operation
npx @graphql-inspector/cli validate './src/**/*.graphql' './schema.graphql' \
  --maxAliasCount 5
```

Example violation:

```graphql
# 6 aliases - exceeds limit of 5
query TooManyAliases {
  user1: user(id: "1") { name }
  user2: user(id: "2") { name }
  user3: user(id: "3") { name }
  user4: user(id: "4") { name }
  user5: user(id: "5") { name }
  user6: user(id: "6") { name }  # Exceeds limit
}
```

### Directive Count

Limit directives to prevent abuse:

```bash
# Max 10 directives per operation
npx @graphql-inspector/cli validate './src/**/*.graphql' './schema.graphql' \
  --maxDirectiveCount 10
```

### Token Count

Limit query complexity by token count:

```bash
# Max 1000 tokens per operation
npx @graphql-inspector/cli validate './src/**/*.graphql' './schema.graphql' \
  --maxTokenCount 1000
```

### Complexity Score

Calculate and limit query complexity:

```bash
# Max complexity score of 100
npx @graphql-inspector/cli validate './src/**/*.graphql' './schema.graphql' \
  --maxComplexityScore 100
```

## Configuration File

Create `.graphql-inspector.yaml`:

```yaml
validate:
  schema: './schema.graphql'
  documents: './src/**/*.graphql'

  # Validation limits
  maxDepth: 10
  maxAliasCount: 5
  maxDirectiveCount: 10
  maxTokenCount: 1000
  maxComplexityScore: 100

  # Federation support
  federation: false
  federationV2: false
  aws: false
```

## Common Validation Errors

### Unknown Field

```
Error: Cannot query field "unknownField" on type "User".
```

Fix: Check field name spelling or add field to schema.

### Wrong Argument Type

```
Error: Argument "id" has invalid value "123".
Expected type "ID!", found "123" (String).
```

Fix: Use correct type for argument.

### Missing Required Argument

```
Error: Field "user" argument "id" of type "ID!" is required.
```

Fix: Provide required argument.

### Invalid Fragment Spread

```
Error: Fragment "UserFields" cannot be spread here as objects of
type "Post" can never be of type "User".
```

Fix: Ensure fragment type matches spread location.

### Unused Fragment

```
Warning: Fragment "UnusedFragment" is never used.
```

Fix: Remove or use the fragment.

## CI/CD Integration

### GitHub Actions

```yaml
name: Validate Operations
on:
  pull_request:
    paths:
      - 'src/**/*.graphql'
      - 'src/**/*.tsx'
      - 'schema.graphql'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Inspector
        run: npm install -g @graphql-inspector/cli

      - name: Validate operations
        run: |
          graphql-inspector validate \
            'src/**/*.graphql' \
            schema.graphql \
            --maxDepth 10 \
            --maxAliasCount 5
```

### Pre-commit Hook

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "graphql-inspector validate 'src/**/*.graphql' schema.graphql"
    }
  }
}
```

## Extracting Operations from Code

GraphQL Inspector can extract operations from various file types:

### TypeScript/JavaScript

```typescript
// Operations in template literals are detected
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      name
      email
    }
  }
`;
```

### React with GraphQL

```tsx
// Tagged template literals in React files
import { gql } from '@apollo/client';

const USER_QUERY = gql`
  query UserQuery {
    currentUser {
      id
      name
    }
  }
`;
```

## Best Practices

1. **Validate in CI** - Run validation on every PR affecting GraphQL files
2. **Set reasonable limits** - Start with permissive limits, tighten over time
3. **Validate against production schema** - Ensure operations work in production
4. **Extract operations from code** - Validate all operations, not just `.graphql` files
5. **Use Federation flags** - Enable if using Apollo Federation
6. **Fail on warnings** - Treat unused fragments as errors in CI
7. **Version your schema** - Validate against specific schema versions
8. **Document limits** - Explain why limits exist to developers

## Common Patterns

### Multi-Schema Validation

For monorepos with multiple schemas:

```bash
# Validate against specific service schema
npx @graphql-inspector/cli validate \
  './packages/app/src/**/*.graphql' \
  './packages/api/schema.graphql'

# Validate against federated supergraph
npx @graphql-inspector/cli validate \
  './packages/web/src/**/*.graphql' \
  './supergraph.graphql' \
  --federationV2
```

### Incremental Adoption

Start permissive, add stricter rules over time:

```yaml
# Phase 1: Basic validation only
validate:
  schema: './schema.graphql'
  documents: './src/**/*.graphql'

# Phase 2: Add depth limiting
validate:
  schema: './schema.graphql'
  documents: './src/**/*.graphql'
  maxDepth: 15

# Phase 3: Add complexity limits
validate:
  schema: './schema.graphql'
  documents: './src/**/*.graphql'
  maxDepth: 10
  maxAliasCount: 10
  maxComplexityScore: 200
```

## Troubleshooting

### "Schema file not found"

- Verify schema path is correct
- Check glob pattern matches schema location
- Use absolute path if relative fails

### "No documents found"

- Check glob pattern matches operation files
- Verify file extensions are correct
- Ensure files contain GraphQL operations

### "Unknown directive"

- Add `--federation` or `--federationV2` for Federation directives
- Add `--aws` for AppSync directives
- Check custom directives are defined in schema

### Operations not detected in code

- Ensure using tagged template literal (`gql\`...\``)
- Check file extension is included in glob
- Verify GraphQL Inspector can parse the file type

## When to Use This Skill

- Setting up operation validation in CI/CD
- Enforcing query complexity limits
- Validating operations before deployment
- Catching schema-operation mismatches early
- Preventing deeply nested queries
- Auditing existing operations for compliance
