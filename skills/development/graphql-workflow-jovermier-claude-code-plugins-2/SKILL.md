---
name: graphql-workflow
description: Activate when creating, modifying, troubleshooting, or managing GraphQL operations with codegen. This includes scaffolding .graphql files, running code generation, validating naming conventions, fixing codegen errors, or updating GraphQL types and hooks.
updated: 2025-01-13
---

# GraphQL Workflow Skill

This skill provides a generic, project-agnostic workflow for GraphQL development with automatic code generation. The core pattern is **role-based file naming** which enables type-safe, permission-aware GraphQL operations.

## When This Skill Activates

Claude automatically uses this skill when you:

- Create a new GraphQL query, mutation, or subscription
- Modify existing GraphQL operations
- Troubleshoot GraphQL codegen errors
- Regenerate types after schema changes
- Validate GraphQL file naming conventions
- Need to understand role-based GraphQL structure

## The Core Pattern: Role-Based File Naming

The key insight is that **GraphQL operations should be organized by permission role**, not by feature or operation type.

```
operationName.role.graphql
```

### Example Role Hierarchy

```
public < user < employee < admin
```

**Your project's roles may differ.** Common patterns:

| Project Type | Typical Roles |
|--------------|---------------|
| SaaS App | `public`, `user`, `admin` |
| Marketplace | `public`, `buyer`, `seller`, `admin` |
| Social Platform | `public`, `member`, `moderator`, `admin` |
| E-commerce | `public`, `customer`, `staff`, `admin` |

## Critical Rules

**NEVER violate these rules when working with GraphQL:**

1. ❌ **NEVER edit files in `*/generated/` directories** - These are auto-generated
2. ✅ **ALWAYS follow `.{role}.graphql` naming convention** - One file per role
3. ✅ **ALWAYS run codegen after GraphQL changes** - Regenerate types
4. ✅ **ALWAYS verify GraphQL backend is running before codegen** - Services must be available
5. ✅ **ALWAYS place files in your project's GraphQL directory** - Configure your codegen

## Workflow Steps

### 1. Create GraphQL Operation

**Step 1: Determine Requirements**

- Operation name (camelCase, descriptive)
- User role (from your project's role hierarchy)
- Operation type (query, mutation, subscription)
- Required data fields

**Step 2: Create Properly Named File**

```bash
# File naming pattern: {operationName}.{role}.graphql
# Examples for a typical SaaS app:
src/graphql/getUserProfile.user.graphql
src/graphql/createAppointment.user.graphql
src/graphql/getAllUsers.admin.graphql
src/graphql/getPublicData.public.graphql
```

**Step 3: Write GraphQL Operation**

```graphql
# Query Example (getUserProfile.user.graphql)
query GetUserProfile($userId: ID!) {
  user(id: $userId) {
    id
    name
    email
    profilePicture
  }
}

# Mutation Example (createAppointment.user.graphql)
mutation CreateAppointment($input: AppointmentInput!) {
  createAppointment(input: $input) {
    id
    scheduledAt
    status
  }
}

# Subscription Example (onUserUpdate.user.graphql)
subscription OnUserUpdate($userId: ID!) {
  userUpdated(userId: $userId) {
    id
    name
    updatedAt
  }
}
```

**Step 4: Verify Backend Availability**

```bash
# Check your GraphQL endpoint is running
curl -f {YOUR_GRAPHQL_ENDPOINT} || echo "Backend not available"

# For Hasura: curl http://localhost:8080/healthz
# For Apollo: curl http://localhost:4000/.well-known/apollo/server-health
```

### 2. Run Code Generation

**Your project's codegen command will vary.** Common patterns:

```bash
# GraphQL Codegen (codegen-ts / graphql-codegen)
pnpm codegen

# With codegen-ts config files:
pnpm codegen:user      # User role only
pnpm codegen:admin     # Admin role only

# Or with npm scripts:
npm run generate-types
npm run codegen
```

**Expected Output:**

- ✅ TypeScript types generated in `src/generated/` (or your configured output)
- ✅ React hooks auto-generated for each operation
- ✅ Full type safety for variables and responses

### 3. Verify Generated Code

```typescript
// Import generated hook in your component
import { useGetUserProfileQuery } from '@/generated/user';

// Use with full type safety
const { data, loading, error } = useGetUserProfileQuery({
  variables: { userId: currentUser.id },
});

// data is fully typed with autocomplete
const user = data?.user; // Type: User | undefined
```

### 4. Handle Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Backend not available" | GraphQL server not running | Start your GraphQL backend service |
| "GraphQL file not found" | Wrong directory or naming | Check file location and `.role.graphql` suffix |
| "Codegen failed with syntax error" | Invalid GraphQL syntax | Validate operation syntax and field names |
| "Generated types not updated" | Stale build cache | Delete `generated/` folder and rerun codegen |
| "Type X does not exist" | Schema mismatch | Check your GraphQL schema matches backend |

## GraphQL Operation Templates

### Query Template

```graphql
# src/graphql/{operationName}.{role}.graphql
query {OperationName}($param: Type!) {
  tableName(where: { field: { _eq: $param } }) {
    id
    field1
    field2
    relatedTable {
      id
      name
    }
  }
}
```

### Mutation Template

```graphql
# src/graphql/{operationName}.{role}.graphql
mutation {OperationName}($input: table_insert_input!) {
  insert_table_one(object: $input) {
    id
    field1
    field2
    created_at
  }
}
```

### Subscription Template

```graphql
# src/graphql/{operationName}.{role}.graphql
subscription {OperationName}($userId: ID!) {
  tableName(where: { user_id: { _eq: $userId } }) {
    id
    field1
    updated_at
  }
}
```

## Integration with Components

**Step 1: Import Generated Hook**

```typescript
import { useGetUserProfileQuery } from '@/generated/user';
```

**Step 2: Use in Component**

```typescript
export function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error } = useGetUserProfileQuery({
    variables: { userId }
  });

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div>
      <h1>{data?.user?.name}</h1>
      <p>{data?.user?.email}</p>
    </div>
  );
}
```

## Configuring Codegen for Your Project

### Basic codegen.ts Configuration

```typescript
import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  schema: 'http://localhost:8080/v1/graphql', // Your GraphQL endpoint
  documents: ['src/graphql/**/*.graphql'],
  generateLocally: true,
  hooks: { afterAllFileWrite: ['prettier --write'] },
  generates: {
    'src/generated/types.ts': {
      plugins: ['typescript'],
      config: {
        scalars: {
          uuid: 'string',
          timestamptz: 'string',
        },
      },
    },
    'src/generated/': {
      preset: 'near-operation-file',
      presetConfig: {
        extension: '.generated.ts',
        baseTypesPath: 'types.ts',
      },
      plugins: ['typescript-operations', 'typescript-react-apollo'],
    },
  },
};

export default config;
```

### Role-Based Configuration (Multiple Output Files)

For role-based separation, use multiple config files:

```
codegen.ts              # Base types
codegen.user.ts         # User operations
codegen.admin.ts        # Admin operations
codegen.public.ts       # Public operations
```

**codegen.user.ts example:**

```typescript
import type { CodegenConfig } from '@graphql-codegen/cli';
import baseConfig from './codegen';

const config: CodegenConfig = {
  ...baseConfig,
  documents: ['src/graphql/**/*.user.graphql'],
  generates: {
    'src/generated/user.ts': {
      plugins: ['typescript', 'typescript-operations', 'typescript-react-apollo'],
    },
  },
};

export default config;
```

## Best Practices

1. **Descriptive Names**: Use clear operation names (e.g., `GetUserProfile`, not `GetUser`)
2. **Role Appropriate**: Only query data the role should access
3. **Field Selection**: Only request fields you need (avoid over-fetching)
4. **Pagination**: Use limit/offset or cursor-based pagination for large datasets
5. **Error Handling**: Always handle loading and error states
6. **Type Safety**: Leverage generated TypeScript types fully
7. **Fragments**: Reuse common field selections with GraphQL fragments

## Testing GraphQL Operations

1. **Test in GraphQL Playground/Console** - Your GraphQL endpoint's UI
2. **Test with Mock Data** - Use MSW or similar for unit tests
3. **Test Permissions** - Verify role-based access works correctly
4. **Test Error Cases** - Handle network failures, validation errors

## Performance Optimization

- **Fragments**: Reuse common field selections
- **Batching**: Combine related queries when possible
- **Caching**: Leverage your GraphQL client's cache (Apollo, urql, etc.)
- **Subscriptions**: Use sparingly; prefer queries with polling for most cases

## Quick Reference

| Task | Command |
|------|---------|
| Generate all types | `pnpm codegen` |
| Generate specific role | `pnpm codegen:{role}` |
| Check GraphQL endpoint | `curl {YOUR_GRAPHQL_ENDPOINT}` |
| Clean and rebuild | `rm -rf generated/ && pnpm codegen` |

---

**This skill is framework and backend agnostic.** Works with:
- **Backends**: Hasura, Apollo Server, GraphQL Yoga, PostGraphile, etc.
- **Frameworks**: React, Next.js, Vue, Svelte, Solid, etc.
- **Clients**: Apollo Client, urql, GraphQL Request, etc.
