---
name: railway-api
description: Railway.com GraphQL API automation for projects, services, deployments, and environment variables. Use when automating Railway operations, querying project data, managing deployments, setting variables via API, or integrating Railway into workflows.
---

# Railway API

Comprehensive reference for Railway.com GraphQL API v2 automation including authentication, queries, mutations, and workflow automation.

## Overview

The Railway GraphQL API enables programmatic access to all Railway platform features:
- Project and service management
- Environment variable configuration
- Deployment triggering and monitoring
- Team and resource management
- Usage and billing queries

**API Endpoint**: `https://backboard.railway.com/graphql/v2`

## Quick Start

### 1. Authentication Setup

Railway supports three token types with different scopes:

| Token Type | Header | Scope | Use Case |
|------------|--------|-------|----------|
| Account | `Authorization: Bearer <token>` | All user resources | Personal automation |
| Team | `Team-Access-Token: <token>` | Team-specific resources | Team workflows |
| Project | `Project-Access-Token: <token>` | Single project only | CI/CD, project automation |

**Get tokens**: Use the railway-auth skill or Railway dashboard → Account Settings → Tokens

### 2. Basic Query Example

```bash
curl https://backboard.railway.com/graphql/v2 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { me { name email } }"}'
```

### 3. Basic Mutation Example

```bash
curl https://backboard.railway.com/graphql/v2 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation($input: VariableUpsertInput!) { variableUpsert(input: $input) }",
    "variables": {
      "input": {
        "projectId": "project-id",
        "environmentId": "env-id",
        "name": "API_KEY",
        "value": "secret-value"
      }
    }
  }'
```

## Common Operations

### User & Account Information

```graphql
query {
  me {
    id
    name
    email
    avatar
    isAdmin
  }
}
```

### List Projects

```graphql
query {
  projects {
    edges {
      node {
        id
        name
        description
        createdAt
        updatedAt
      }
    }
  }
}
```

### Get Project Details with Services

```graphql
query GetProject($projectId: String!) {
  project(id: $projectId) {
    id
    name
    description
    services {
      edges {
        node {
          id
          name
          serviceInstances {
            edges {
              node {
                id
                environmentId
                serviceId
              }
            }
          }
        }
      }
    }
    environments {
      edges {
        node {
          id
          name
        }
      }
    }
  }
}
```

### Get Environment Variables

```graphql
query GetVariables($projectId: String!, $environmentId: String!) {
  variables(projectId: $projectId, environmentId: $environmentId) {
    edges {
      node {
        name
        value
      }
    }
  }
}
```

### Set/Update Variable

```graphql
mutation SetVariable($input: VariableUpsertInput!) {
  variableUpsert(input: $input)
}

# Variables:
{
  "input": {
    "projectId": "your-project-id",
    "environmentId": "your-env-id",
    "name": "DATABASE_URL",
    "value": "postgresql://..."
  }
}
```

### Trigger Deployment

```graphql
mutation TriggerDeployment($serviceId: String!, $environmentId: String!) {
  deploymentTrigger(serviceId: $serviceId, environmentId: $environmentId) {
    id
    status
    createdAt
  }
}
```

## Architecture

### Progressive Disclosure Structure

1. **SKILL.md** (this file): Quick reference and common operations
2. **references/**: Detailed documentation
   - `graphql-endpoint.md` - Complete API endpoint documentation
   - `authentication.md` - Comprehensive authentication guide
   - `common-queries.md` - 15+ query examples with responses
   - `common-mutations.md` - 15+ mutation examples with patterns
3. **scripts/**: Automation tools
   - `query-project.py` - Python script for querying Railway API
   - `set-variables.ts` - TypeScript script for variable management

## Error Handling

Railway API returns errors in this format:

```json
{
  "errors": [
    {
      "message": "Error message",
      "extensions": {
        "code": "ERROR_CODE"
      }
    }
  ]
}
```

**Common errors**:
- `UNAUTHORIZED` - Invalid or expired token
- `FORBIDDEN` - Insufficient permissions for resource
- `NOT_FOUND` - Resource doesn't exist
- `VALIDATION_ERROR` - Invalid input data

**Best practices**:
1. Always check for `errors` field in response
2. Use appropriate token type for operation scope
3. Handle rate limiting (429 responses)
4. Validate input before mutations
5. Use variables for parameterized queries

## Integration Patterns

### CI/CD Pipeline

```bash
# Get project token from railway-auth
# Set deployment variables
# Trigger deployment
# Monitor deployment status
```

See `scripts/` for complete automation examples.

### Infrastructure as Code

```typescript
// Define Railway resources in code
// Apply changes via GraphQL mutations
// Track state and changes
```

### Monitoring & Alerts

```python
# Query deployment status
# Check resource usage
# Alert on failures
```

## Cross-References

- **railway-auth**: Token generation and management
- **railway-deployment**: High-level deployment workflows
- **railway-troubleshooting**: API error debugging

## Learning Path

1. **Start**: Read `references/graphql-endpoint.md` for endpoint details
2. **Authentication**: Study `references/authentication.md` for token setup
3. **Queries**: Explore `references/common-queries.md` for data retrieval
4. **Mutations**: Review `references/common-mutations.md` for operations
5. **Automation**: Use scripts in `scripts/` for workflow examples
6. **Advanced**: Combine patterns for complex automation

## Quick Reference

### Essential Queries
- Get user info: `query { me { name email } }`
- List projects: `query { projects { edges { node { id name } } } }`
- Get variables: Use `variables` query with projectId and environmentId
- Deployment status: Query `deployments` with filters

### Essential Mutations
- Set variable: `variableUpsert` mutation
- Trigger deploy: `deploymentTrigger` mutation
- Create service: `serviceCreate` mutation
- Delete variable: `variableDelete` mutation

### Rate Limits
- Account tokens: 100 requests/minute
- Team tokens: 500 requests/minute
- Project tokens: 1000 requests/minute

## Notes

- All timestamps are in ISO 8601 format (UTC)
- IDs are opaque strings, don't parse or construct them
- Pagination uses cursor-based edges/nodes pattern
- Use GraphQL variables for all dynamic values
- Production mutations should use Project tokens for security

## Known API Limitations

Some GraphQL queries return "Problem processing request" even with valid tokens. This is a Railway API limitation, not a token issue.

**Affected queries**: `deployment(id:)`, `deploymentLogs`, `buildLogs`, `me.teams`, `teams`

**Workaround**: Use Railway CLI for these operations:
```bash
railway list --json     # Projects/teams
railway logs            # Deployment/build logs
```

See [api-limitations.md](references/api-limitations.md) for full details.

---

## References

- [common-queries.md](references/common-queries.md) - 31 query examples
- [common-mutations.md](references/common-mutations.md) - 37 mutation examples
- [api-limitations.md](references/api-limitations.md) - Known limitations and workarounds
- [authentication.md](references/authentication.md) - Token types and headers
- [graphql-endpoint.md](references/graphql-endpoint.md) - Endpoint details

---

## Resources

- Railway API Documentation: https://docs.railway.com/reference/public-api
- GraphQL Explorer: https://backboard.railway.com/graphql/v2 (with GraphiQL)
- Token Management: Use railway-auth skill
