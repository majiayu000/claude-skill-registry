---
name: midnight-indexer:event-subscriptions
description: Use when subscribing to real-time blockchain events, setting up WebSocket connections, monitoring contract state changes, building live dashboards, or implementing push notifications from Midnight.
---

# Event Subscriptions

Subscribe to real-time blockchain events from the Midnight Network using WebSocket connections.

## When to Use

- Listening for new transactions affecting an address
- Monitoring contract state changes in real-time
- Building live dashboards with blockchain data
- Implementing push notifications for blockchain events
- Tracking confirmation status of submitted transactions
- Building event-driven backend services

## Key Concepts

### WebSocket Architecture

The Midnight indexer provides GraphQL subscriptions over WebSocket for real-time event delivery.

| Component | Purpose |
|-----------|---------|
| WebSocket Connection | Persistent bidirectional channel |
| GraphQL Subscriptions | Event-driven queries |
| Subscription Filters | Target specific events |

### Event Types

| Event | Description |
|-------|-------------|
| `newTransaction` | Transaction confirmed in a block |
| `newBlock` | New block added to chain |
| `contractStateChange` | Contract state updated |
| `utxoCreated` | New UTXO created for address |
| `utxoSpent` | UTXO spent by transaction |

### Connection Lifecycle

1. **Connect** - Establish WebSocket connection
2. **Subscribe** - Send subscription query
3. **Receive** - Handle incoming events
4. **Reconnect** - Handle disconnections gracefully
5. **Unsubscribe** - Clean up when done

### Backpressure Handling

When events arrive faster than your application can process them, implement backpressure strategies:

- **Buffering** - Queue events for processing
- **Dropping** - Skip events when overloaded
- **Sampling** - Process only every Nth event

## References

| Document | Description |
|----------|-------------|
| [websocket-setup.md](references/websocket-setup.md) | Connection configuration and protocols |
| [reconnection-patterns.md](references/reconnection-patterns.md) | Handling disconnections and replay |

## Examples

| Example | Description |
|---------|-------------|
| [contract-events/](examples/contract-events/) | Subscribe to contract state changes |
| [reconnect-handler/](examples/reconnect-handler/) | Robust reconnection with event replay |

## Quick Start

### 1. Create WebSocket Client

```typescript
import { createWebSocketClient } from '@midnight-ntwrk/midnight-js-indexer';

const wsClient = createWebSocketClient({
  uri: 'wss://indexer.testnet.midnight.network/api/v1/graphql',
});
```

### 2. Subscribe to Events

```typescript
const subscription = wsClient.subscribe({
  query: `
    subscription WatchTransactions($address: String!) {
      newTransaction(address: $address) {
        hash
        blockNumber
        timestamp
        inputs { address amount }
        outputs { address amount }
      }
    }
  `,
  variables: { address: 'addr_test1...' },
});

subscription.on('data', (event) => {
  console.log('New transaction:', event.data.newTransaction);
});
```

### 3. Handle Events

```typescript
subscription.on('data', handleTransaction);
subscription.on('error', handleError);
subscription.on('complete', handleComplete);
```

### 4. Clean Up

```typescript
// When done listening
subscription.unsubscribe();
wsClient.close();
```

## Common Patterns

### Event Handler Setup

```typescript
interface SubscriptionHandlers<T> {
  onData: (data: T) => void;
  onError: (error: Error) => void;
  onComplete?: () => void;
}

function createEventSubscription<T>(
  client: WebSocketClient,
  query: string,
  variables: Record<string, unknown>,
  handlers: SubscriptionHandlers<T>
): () => void {
  const subscription = client.subscribe({ query, variables });

  subscription.on('data', (result) => {
    if (result.errors) {
      handlers.onError(new Error(result.errors[0].message));
      return;
    }
    handlers.onData(result.data);
  });

  subscription.on('error', handlers.onError);

  if (handlers.onComplete) {
    subscription.on('complete', handlers.onComplete);
  }

  // Return unsubscribe function
  return () => subscription.unsubscribe();
}
```

### Contract Event Listener

```typescript
interface ContractEvent {
  contractAddress: string;
  key: string;
  oldValue: string | null;
  newValue: string;
  txHash: string;
  blockNumber: number;
}

function watchContractState(
  client: WebSocketClient,
  contractAddress: string,
  onEvent: (event: ContractEvent) => void
): () => void {
  return createEventSubscription(
    client,
    `
      subscription WatchContract($address: String!) {
        contractStateChange(address: $address) {
          contractAddress
          key
          oldValue
          newValue
          txHash
          blockNumber
        }
      }
    `,
    { address: contractAddress },
    {
      onData: (data) => onEvent(data.contractStateChange),
      onError: (error) => console.error('Subscription error:', error),
    }
  );
}
```

### Transaction Confirmation Tracker

```typescript
async function waitForConfirmation(
  client: WebSocketClient,
  txHash: string,
  confirmations = 1,
  timeout = 120000
): Promise<number> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      unsubscribe();
      reject(new Error('Confirmation timeout'));
    }, timeout);

    const unsubscribe = createEventSubscription(
      client,
      `
        subscription TrackTx($hash: String!) {
          transactionConfirmation(hash: $hash) {
            hash
            blockNumber
            confirmations
          }
        }
      `,
      { hash: txHash },
      {
        onData: (data) => {
          const { confirmations: current } = data.transactionConfirmation;
          if (current >= confirmations) {
            clearTimeout(timer);
            unsubscribe();
            resolve(data.transactionConfirmation.blockNumber);
          }
        },
        onError: (error) => {
          clearTimeout(timer);
          reject(error);
        },
      }
    );
  });
}
```

### Multiple Subscriptions Manager

```typescript
class SubscriptionManager {
  private subscriptions = new Map<string, () => void>();
  private client: WebSocketClient;

  constructor(wsUri: string) {
    this.client = createWebSocketClient({ uri: wsUri });
  }

  subscribe(
    id: string,
    query: string,
    variables: Record<string, unknown>,
    onData: (data: unknown) => void
  ): void {
    // Unsubscribe existing with same ID
    this.unsubscribe(id);

    const unsub = createEventSubscription(
      this.client,
      query,
      variables,
      {
        onData,
        onError: (err) => console.error(`Subscription ${id} error:`, err),
      }
    );

    this.subscriptions.set(id, unsub);
  }

  unsubscribe(id: string): void {
    const unsub = this.subscriptions.get(id);
    if (unsub) {
      unsub();
      this.subscriptions.delete(id);
    }
  }

  unsubscribeAll(): void {
    for (const [id] of this.subscriptions) {
      this.unsubscribe(id);
    }
  }

  close(): void {
    this.unsubscribeAll();
    this.client.close();
  }
}
```

### Event Buffering

```typescript
class EventBuffer<T> {
  private buffer: T[] = [];
  private processing = false;
  private intervalHandle: ReturnType<typeof setInterval>;

  constructor(
    private processor: (events: T[]) => Promise<void>,
    private maxSize = 100,
    private flushInterval = 1000
  ) {
    this.intervalHandle = setInterval(() => this.flush(), flushInterval);
  }

  destroy(): void {
    clearInterval(this.intervalHandle);
  }

  push(event: T): void {
    this.buffer.push(event);

    if (this.buffer.length >= this.maxSize) {
      this.flush();
    }
  }

  async flush(): Promise<void> {
    if (this.processing || this.buffer.length === 0) return;

    this.processing = true;
    const events = this.buffer.splice(0);

    try {
      await this.processor(events);
    } catch (error) {
      console.error('Buffer processing error:', error);
      // Re-queue failed events at front
      this.buffer.unshift(...events);
    } finally {
      this.processing = false;
    }
  }
}
```

## Related Skills

- `indexer-service` - Query historical blockchain data
- `midnight-dapp:state-management` - Sync frontend state with events
- `midnight-dapp:transaction-flows` - Submit transactions and track status

## Related Commands

- `/midnight-tooling:check` - Verify WebSocket connectivity
