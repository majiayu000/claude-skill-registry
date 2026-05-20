---
name: midnight-indexer:indexer-service
description: Use when querying the Midnight indexer for blockchain data, fetching account balances, listing transactions, reading contract state, or building data-driven DApp backends.
---

# Indexer Service

Connect to and query the Midnight Network indexer for blockchain data including balances, transactions, and contract state.

## When to Use

- Fetching account balances and UTXO data
- Listing transaction history for an address
- Reading contract state from the blockchain
- Querying shielded vs unshielded transaction data
- Building data-driven DApp backends
- Implementing pagination for large result sets

## Key Concepts

### Indexer Architecture

The Midnight indexer provides a GraphQL API for querying blockchain data. It indexes all on-chain activity and exposes it through structured queries.

| Component | Purpose |
|-----------|---------|
| GraphQL API | Query interface for blockchain data |
| WebSocket | Real-time subscriptions (see event-subscriptions skill) |
| REST Health | Service health checks |

### API Versions

The indexer API has evolved through several versions. Ensure your queries are compatible with your target version.

| Version | Key Features | Breaking Changes |
|---------|--------------|------------------|
| 2.0.0 | Base GraphQL schema | Initial release |
| 2.1.0 | Enhanced filters, pagination | Query parameter changes |
| 2.1.4 | Performance optimizations | None from 2.1.0 |

### UTXO Model

Midnight uses a UTXO (Unspent Transaction Output) model rather than an account model. Balance queries return the set of unspent outputs owned by an address.

### Shielded Transactions

Midnight supports both transparent and shielded transactions. The indexer provides different access patterns:

- **Transparent**: Full transaction details visible
- **Shielded**: Only commitment hashes visible, details encrypted

## References

| Document | Description |
|----------|-------------|
| [api-versions.md](references/api-versions.md) | Version differences and migration guide |
| [query-patterns.md](references/query-patterns.md) | Common query patterns and optimization |

## Examples

| Example | Description |
|---------|-------------|
| [balance-query/](examples/balance-query/) | Query account balance and UTXOs |
| [transaction-list/](examples/transaction-list/) | List transaction history with pagination |
| [contract-state/](examples/contract-state/) | Read deployed contract state |

## Quick Start

### 1. Configure Indexer Client

```typescript
import { createIndexerClient } from '@midnight-ntwrk/midnight-js-indexer';

const indexer = createIndexerClient({
  uri: 'https://indexer.testnet.midnight.network/api/v1/graphql',
  wsUri: 'wss://indexer.testnet.midnight.network/api/v1/graphql',
});
```

### 2. Query Balance

```typescript
const balance = await indexer.query({
  query: `
    query GetBalance($address: String!) {
      balance(address: $address) {
        total
        utxos {
          txHash
          outputIndex
          amount
        }
      }
    }
  `,
  variables: { address: 'addr_test1...' },
});

console.log('Total balance:', balance.data.balance.total);
```

### 3. List Transactions

```typescript
const transactions = await indexer.query({
  query: `
    query GetTransactions($address: String!, $limit: Int!) {
      transactions(address: $address, first: $limit) {
        edges {
          node {
            hash
            blockNumber
            timestamp
            inputs { address amount }
            outputs { address amount }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  `,
  variables: { address: 'addr_test1...', limit: 20 },
});
```

## Common Patterns

### Environment-Based Configuration

```typescript
interface IndexerConfig {
  uri: string;
  wsUri: string;
}

function getIndexerConfig(): IndexerConfig {
  const network = process.env.MIDNIGHT_NETWORK || 'testnet';

  const configs: Record<string, IndexerConfig> = {
    testnet: {
      uri: 'https://indexer.testnet.midnight.network/api/v1/graphql',
      wsUri: 'wss://indexer.testnet.midnight.network/api/v1/graphql',
    },
    mainnet: {
      uri: 'https://indexer.midnight.network/api/v1/graphql',
      wsUri: 'wss://indexer.midnight.network/api/v1/graphql',
    },
  };

  return configs[network] ?? configs.testnet;
}
```

### Pagination with Cursors

```typescript
async function fetchAllTransactions(
  indexer: IndexerClient,
  address: string
): Promise<Transaction[]> {
  const allTransactions: Transaction[] = [];
  let cursor: string | null = null;
  let hasMore = true;

  while (hasMore) {
    const result = await indexer.query({
      query: TRANSACTIONS_QUERY,
      variables: {
        address,
        first: 100,
        after: cursor,
      },
    });

    const { edges, pageInfo } = result.data.transactions;
    allTransactions.push(...edges.map(e => e.node));

    hasMore = pageInfo.hasNextPage;
    cursor = pageInfo.endCursor;
  }

  return allTransactions;
}
```

### Health Check

```typescript
async function checkIndexerHealth(baseUrl: string): Promise<boolean> {
  try {
    const response = await fetch(`${baseUrl}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
```

### Retry with Backoff

```typescript
async function queryWithRetry<T>(
  indexer: IndexerClient,
  query: string,
  variables: Record<string, unknown>,
  maxRetries = 3
): Promise<T> {
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await indexer.query({ query, variables });
    } catch (error) {
      lastError = error as Error;
      if (attempt < maxRetries) {
        await new Promise(r => setTimeout(r, 1000 * attempt));
      }
    }
  }

  throw lastError;
}
```

## Related Skills

- `event-subscriptions` - Real-time WebSocket event streams
- `midnight-tooling:contract-calling` - Invoking contracts that change state
- `midnight-dapp:state-management` - Frontend state synchronization with indexer

## Related Commands

- `/midnight-tooling:check` - Verify indexer connectivity
