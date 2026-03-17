---
name: dojo-indexer
description: Set up and configure Torii indexer for GraphQL queries, gRPC subscriptions, and SQL access. Use when indexing your deployed world for client queries or real-time updates.
allowed-tools: Read, Write, Bash, Grep
---

# Dojo Indexer (Torii)

Set up and use Torii, the Dojo indexer, for efficient querying and real-time subscriptions to your world state.

## When to Use This Skill

- "Set up Torii indexer"
- "Configure GraphQL for my world"
- "Create subscriptions for entity updates"
- "Query world state efficiently"

## What This Skill Does

Manages Torii indexer:
- Start and configure Torii
- Create GraphQL queries
- Set up real-time subscriptions
- Access SQL database directly

## Quick Start

**Start Torii:**
```bash
torii --world <WORLD_ADDRESS>
```

This starts Torii with default settings:
- GraphQL API at `http://localhost:8080/graphql`
- gRPC API at `http://localhost:8080`
- In-memory database (for development)

**With Controller indexing (recommended):**
```bash
torii --world <WORLD_ADDRESS> --indexing.controllers
```

**Production configuration:**
```bash
torii --world <WORLD_ADDRESS> --db-dir ./torii-db --indexing.controllers
```

## What is Torii?

Torii is the Dojo indexer that:
- Watches blockchain for world events
- Indexes model state changes
- Provides GraphQL API for queries
- Provides gRPC API for subscriptions
- Offers SQL access for complex queries

**Why use Torii:**
- Faster than direct RPC queries
- Complex queries (filters, pagination)
- Real-time subscriptions
- Type-safe GraphQL schema

## GraphQL API

Torii provides GraphQL endpoint at `http://localhost:8080/graphql`

Use the GraphiQL IDE in your browser to explore the schema and test queries.

### Schema Structure

Torii generates two types of queries:

**Generic Queries:**
- `entities` - Access all entities with filtering
- `models` - Retrieve model definitions
- `transactions` - Query indexed transactions

**Model-Specific Queries:**
- `{modelName}Models` - Custom queries for each model
- Example: `positionModels`, `movesModels`

### Basic Queries

**Get all entities of a model:**
```graphql
query {
    movesModels {
        edges {
            node {
                player
                remaining
                last_direction
            }
        }
    }
}
```

**Get model metadata:**
```graphql
query {
    models {
        edges {
            node {
                id
                name
                classHash
                contractAddress
            }
        }
        totalCount
    }
}
```

### Pagination

**Cursor-based pagination:**
```graphql
query {
    entities(first: 10) {
        edges {
            cursor
            node {
                id
            }
        }
        pageInfo {
            hasNextPage
            endCursor
        }
    }
}
```

**Get next page:**
```graphql
query {
    entities(first: 10, after: "cursor_value") {
        edges {
            cursor
            node { id }
        }
    }
}
```

**Offset/limit pagination:**
```graphql
query {
    entities(offset: 20, limit: 10) {
        edges {
            node { id }
        }
        totalCount
    }
}
```

## Real-time Subscriptions

Subscribe to world state changes via WebSocket.

### Entity Updates

```graphql
subscription {
    entityUpdated(id: "0x54f58...") {
        id
        updatedAt
        models {
            __typename
            ... on Position {
                vec {
                    x
                    y
                }
            }
            ... on Moves {
                remaining
            }
        }
    }
}
```

### Event Stream

Monitor all world events:

```graphql
subscription {
    eventEmitted {
        id
        keys
        data
        transactionHash
    }
}
```

### Model Registration

Listen for new model registrations:

```graphql
subscription {
    modelRegistered {
        id
        name
        namespace
    }
}
```

## SQL Access

Torii stores data in SQLite, accessible for complex queries.

**Connect to database:**
```bash
sqlite3 torii.db
```

**Example queries:**
```sql
-- Count entities
SELECT COUNT(*) FROM entities;

-- Custom aggregations
SELECT AVG(value) FROM model_data WHERE model_name = 'Health';
```

## Client Integration

### JavaScript/TypeScript

```typescript
import { createClient } from '@dojoengine/torii-client';

const client = await createClient({
    rpcUrl: "http://localhost:5050",
    toriiUrl: "http://localhost:8080",
    worldAddress: WORLD_ADDRESS,
});

// Query entities
const positions = await client.getEntities({
    model: "Position",
    limit: 10
});

// Subscribe to updates
await client.onEntityUpdated(
    [{ model: "Position", keys: [playerId] }],
    (entity) => console.log("Position updated:", entity)
);
```

### Apollo Client (GraphQL)

```typescript
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

const client = new ApolloClient({
    uri: 'http://localhost:8080/graphql',
    cache: new InMemoryCache(),
});

const { data } = await client.query({
    query: gql`
        query GetMoves {
            movesModels {
                edges {
                    node {
                        player
                        remaining
                    }
                }
            }
        }
    `
});
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--world` | World contract address | Optional (since Torii 1.6.0) |
| `--rpc` | RPC endpoint URL | `http://localhost:5050` |
| `--db-dir` | Database directory | In-memory |
| `--config` | Path to TOML configuration file | None |
| `--http.cors_origins` | CORS origins | `*` |

## Slot Deployment (Remote)

[Slot](https://docs.cartridge.gg/slot) provides hosted Torii instances. Slot requires a TOML configuration file.

### Create Configuration

```toml
# torii.toml
world_address = "<WORLD_ADDRESS>"
rpc = "<RPC_URL>"

[indexing]
controllers = true
```

See the [Torii configuration guide](/toolchain/torii/configuration) for all TOML options (indexing, polling, namespaces, etc.).

### Deploy

```bash
slot auth login

slot deployments create <PROJECT_NAME> torii --config torii.toml --version <DOJO_VERSION>
```

### Manage

```bash
# Stream logs
slot deployments logs <PROJECT_NAME> torii -f

# Delete and recreate (safe — all data is on-chain)
slot deployments delete <PROJECT_NAME> torii
```

## Development Workflow

**Terminal 1: Start Katana**
```bash
katana --dev --dev.no-fee
```

**Terminal 2: Deploy world**
```bash
sozo build && sozo migrate
```

**Terminal 3: Start Torii**
```bash
torii --world <WORLD_ADDRESS> --http.cors_origins "*"
```

## Troubleshooting

### "Connection refused"
- Check Torii is running
- Verify port (default 8080)
- Check firewall rules

### "World not found"
- Verify world address is correct
- Check RPC URL is accessible
- Ensure world is deployed

### "Slow queries"
- Use model-specific queries instead of generic `entities`
- Use pagination
- Request only needed fields

## Next Steps

After Torii setup:
1. Integrate with client (`dojo-client` skill)
2. Create optimized queries
3. Set up subscriptions
4. Monitor performance

## Related Skills

- **dojo-deploy**: Deploy world first
- **dojo-client**: Use Torii in clients
- **dojo-world**: Configure what Torii indexes
- **dojo-migrate**: Restart Torii after migrations
