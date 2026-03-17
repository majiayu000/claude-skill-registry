---
name: event-sourcing
description: Implement event sourcing and CQRS patterns using event stores, aggregates, and projections. Use when building audit trails, temporal queries, or systems requiring full history.
---

# Event Sourcing

## Overview

Store state changes as a sequence of events rather than the current state, enabling temporal queries, audit trails, and event replay.

## When to Use

- Audit trail requirements
- Temporal queries (state at any point in time)
- Event-driven microservices
- CQRS implementations
- Financial systems
- Complex domain models
- Debugging and analysis
- Compliance and regulation

## Core Concepts

```
Event Store ─► Read Model (Projection)
     │
     └─► Aggregate (Domain Logic)
```

## Implementation Examples

### 1. **Event Store (TypeScript)**

```typescript
interface DomainEvent {
  id: string;
  aggregateId: string;
  aggregateType: string;
  eventType: string;
  data: any;
  metadata: {
    userId?: string;
    timestamp: number;
    version: number;
  };
}

interface Aggregate {
  id: string;
  version: number;
}

class EventStore {
  private events: DomainEvent[] = [];

  async appendEvents(
    aggregateId: string,
    expectedVersion: number,
    events: Omit<DomainEvent, 'id' | 'metadata'>[]
  ): Promise<void> {
    // Optimistic concurrency check
    const currentVersion = await this.getCurrentVersion(aggregateId);

    if (currentVersion !== expectedVersion) {
      throw new Error('Concurrency conflict');
    }

    const newEvents = events.map((event, index) => ({
      ...event,
      id: crypto.randomUUID(),
      metadata: {
        timestamp: Date.now(),
        version: expectedVersion + index + 1
      }
    }));

    this.events.push(...newEvents);
  }

  async getEvents(aggregateId: string): Promise<DomainEvent[]> {
    return this.events
      .filter(e => e.aggregateId === aggregateId)
      .sort((a, b) => a.metadata.version - b.metadata.version);
  }

  async getCurrentVersion(aggregateId: string): Promise<number> {
    const events = await this.getEvents(aggregateId);
    return events.length > 0 ? events[events.length - 1].metadata.version : 0;
  }
}

// Bank Account Aggregate
interface BankAccountState {
  id: string;
  balance: number;
  isOpen: boolean;
  version: number;
}

class BankAccount implements Aggregate {
  id: string;
  version: number;
  private balance: number = 0;
  private isOpen: boolean = false;
  private uncommittedEvents: DomainEvent[] = [];

  constructor(id: string) {
    this.id = id;
    this.version = 0;
  }

  // Commands
  open(initialDeposit: number): void {
    if (this.isOpen) {
      throw new Error('Account already open');
    }

    this.applyEvent({
      eventType: 'AccountOpened',
      data: { initialDeposit }
    });
  }

  deposit(amount: number): void {
    if (!this.isOpen) {
      throw new Error('Account not open');
    }

    if (amount <= 0) {
      throw new Error('Amount must be positive');
    }

    this.applyEvent({
      eventType: 'MoneyDeposited',
      data: { amount }
    });
  }

  withdraw(amount: number): void {
    if (!this.isOpen) {
      throw new Error('Account not open');
    }

    if (amount <= 0) {
      throw new Error('Amount must be positive');
    }

    if (this.balance < amount) {
      throw new Error('Insufficient funds');
    }

    this.applyEvent({
      eventType: 'MoneyWithdrawn',
      data: { amount }
    });
  }

  close(): void {
    if (!this.isOpen) {
      throw new Error('Account not open');
    }

    if (this.balance > 0) {
      throw new Error('Cannot close account with positive balance');
    }

    this.applyEvent({
      eventType: 'AccountClosed',
      data: {}
    });
  }

  // Event Application
  private applyEvent(event: Partial<DomainEvent>): void {
    const fullEvent: any = {
      aggregateId: this.id,
      aggregateType: 'BankAccount',
      ...event
    };

    this.apply(fullEvent);
    this.uncommittedEvents.push(fullEvent);
  }

  apply(event: DomainEvent): void {
    switch (event.eventType) {
      case 'AccountOpened':
        this.isOpen = true;
        this.balance = event.data.initialDeposit;
        break;

      case 'MoneyDeposited':
        this.balance += event.data.amount;
        break;

      case 'MoneyWithdrawn':
        this.balance -= event.data.amount;
        break;

      case 'AccountClosed':
        this.isOpen = false;
        break;
    }

    if (event.metadata) {
      this.version = event.metadata.version;
    }
  }

  getUncommittedEvents(): DomainEvent[] {
    return this.uncommittedEvents;
  }

  clearUncommittedEvents(): void {
    this.uncommittedEvents = [];
  }

  getState(): BankAccountState {
    return {
      id: this.id,
      balance: this.balance,
      isOpen: this.isOpen,
      version: this.version
    };
  }
}

// Repository
class BankAccountRepository {
  constructor(private eventStore: EventStore) {}

  async save(account: BankAccount): Promise<void> {
    const events = account.getUncommittedEvents();

    if (events.length === 0) return;

    await this.eventStore.appendEvents(
      account.id,
      account.version,
      events
    );

    account.clearUncommittedEvents();
  }

  async load(id: string): Promise<BankAccount> {
    const events = await this.eventStore.getEvents(id);
    const account = new BankAccount(id);

    events.forEach(event => account.apply(event));

    return account;
  }
}

// Usage
const eventStore = new EventStore();
const repository = new BankAccountRepository(eventStore);

// Create and use account
const account = new BankAccount('acc-123');
account.open(1000);
account.deposit(500);
account.withdraw(200);

await repository.save(account);

// Load account
const loadedAccount = await repository.load('acc-123');
console.log(loadedAccount.getState());
```

### 2. **Projections (Read Models)**

```typescript
interface AccountReadModel {
  id: string;
  balance: number;
  transactionCount: number;
  lastActivity: number;
}

class AccountProjection {
  private accounts = new Map<string, AccountReadModel>();

  async project(event: DomainEvent): Promise<void> {
    switch (event.eventType) {
      case 'AccountOpened':
        await this.handleAccountOpened(event);
        break;

      case 'MoneyDeposited':
        await this.handleMoneyDeposited(event);
        break;

      case 'MoneyWithdrawn':
        await this.handleMoneyWithdrawn(event);
        break;
    }
  }

  private async handleAccountOpened(event: DomainEvent): Promise<void> {
    this.accounts.set(event.aggregateId, {
      id: event.aggregateId,
      balance: event.data.initialDeposit,
      transactionCount: 1,
      lastActivity: event.metadata.timestamp
    });
  }

  private async handleMoneyDeposited(event: DomainEvent): Promise<void> {
    const account = this.accounts.get(event.aggregateId);
    if (!account) return;

    account.balance += event.data.amount;
    account.transactionCount++;
    account.lastActivity = event.metadata.timestamp;
  }

  private async handleMoneyWithdrawn(event: DomainEvent): Promise<void> {
    const account = this.accounts.get(event.aggregateId);
    if (!account) return;

    account.balance -= event.data.amount;
    account.transactionCount++;
    account.lastActivity = event.metadata.timestamp;
  }

  getAccount(id: string): AccountReadModel | undefined {
    return this.accounts.get(id);
  }

  getAllAccounts(): AccountReadModel[] {
    return Array.from(this.accounts.values());
  }
}
```

### 3. **Event Store with PostgreSQL**

```typescript
import { Pool } from 'pg';

class PostgresEventStore {
  constructor(private pool: Pool) {
    this.createTables();
  }

  private async createTables(): Promise<void> {
    await this.pool.query(`
      CREATE TABLE IF NOT EXISTS events (
        id UUID PRIMARY KEY,
        aggregate_id VARCHAR(255) NOT NULL,
        aggregate_type VARCHAR(100) NOT NULL,
        event_type VARCHAR(100) NOT NULL,
        data JSONB NOT NULL,
        metadata JSONB NOT NULL,
        version INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        UNIQUE(aggregate_id, version)
      );

      CREATE INDEX IF NOT EXISTS idx_events_aggregate
      ON events (aggregate_id, version);

      CREATE INDEX IF NOT EXISTS idx_events_type
      ON events (event_type);
    `);
  }

  async appendEvents(
    aggregateId: string,
    expectedVersion: number,
    events: Omit<DomainEvent, 'id' | 'metadata'>[]
  ): Promise<void> {
    const client = await this.pool.connect();

    try {
      await client.query('BEGIN');

      // Check version
      const result = await client.query(
        'SELECT MAX(version) as version FROM events WHERE aggregate_id = $1',
        [aggregateId]
      );

      const currentVersion = result.rows[0].version || 0;

      if (currentVersion !== expectedVersion) {
        throw new Error('Concurrency conflict');
      }

      // Insert events
      for (let i = 0; i < events.length; i++) {
        const event = events[i];
        const version = expectedVersion + i + 1;

        await client.query(`
          INSERT INTO events (
            id, aggregate_id, aggregate_type, event_type,
            data, metadata, version
          )
          VALUES ($1, $2, $3, $4, $5, $6, $7)
        `, [
          crypto.randomUUID(),
          aggregateId,
          event.aggregateType,
          event.eventType,
          JSON.stringify(event.data),
          JSON.stringify({ timestamp: Date.now(), version }),
          version
        ]);
      }

      await client.query('COMMIT');
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  async getEvents(
    aggregateId: string,
    fromVersion: number = 0
  ): Promise<DomainEvent[]> {
    const result = await this.pool.query(
      `SELECT * FROM events
       WHERE aggregate_id = $1 AND version > $2
       ORDER BY version ASC`,
      [aggregateId, fromVersion]
    );

    return result.rows.map(row => ({
      id: row.id,
      aggregateId: row.aggregate_id,
      aggregateType: row.aggregate_type,
      eventType: row.event_type,
      data: row.data,
      metadata: row.metadata
    }));
  }

  async getEventsByType(
    eventType: string,
    fromTimestamp: number = 0
  ): Promise<DomainEvent[]> {
    const result = await this.pool.query(
      `SELECT * FROM events
       WHERE event_type = $1
       AND (metadata->>'timestamp')::bigint > $2
       ORDER BY created_at ASC`,
      [eventType, fromTimestamp]
    );

    return result.rows.map(row => ({
      id: row.id,
      aggregateId: row.aggregate_id,
      aggregateType: row.aggregate_type,
      eventType: row.event_type,
      data: row.data,
      metadata: row.metadata
    }));
  }

  async getAllEvents(
    fromPosition: number = 0,
    limit: number = 100
  ): Promise<DomainEvent[]> {
    const result = await this.pool.query(
      `SELECT * FROM events
       WHERE id > $1
       ORDER BY created_at ASC
       LIMIT $2`,
      [fromPosition, limit]
    );

    return result.rows.map(row => ({
      id: row.id,
      aggregateId: row.aggregate_id,
      aggregateType: row.aggregate_type,
      eventType: row.event_type,
      data: row.data,
      metadata: row.metadata
    }));
  }
}
```

### 4. **Snapshots for Performance**

```typescript
interface Snapshot {
  aggregateId: string;
  version: number;
  state: any;
  createdAt: number;
}

class SnapshotStore {
  private snapshots = new Map<string, Snapshot>();

  async save(snapshot: Snapshot): Promise<void> {
    this.snapshots.set(snapshot.aggregateId, snapshot);
  }

  async get(aggregateId: string): Promise<Snapshot | null> {
    return this.snapshots.get(aggregateId) || null;
  }
}

class SnapshotRepository {
  constructor(
    private eventStore: EventStore,
    private snapshotStore: SnapshotStore,
    private snapshotInterval: number = 10
  ) {}

  async load(id: string): Promise<BankAccount> {
    // Try to load from snapshot
    const snapshot = await this.snapshotStore.get(id);
    const fromVersion = snapshot?.version || 0;

    // Load events since snapshot
    const events = await this.eventStore.getEvents(id);
    const recentEvents = events.filter(e => e.metadata.version > fromVersion);

    const account = new BankAccount(id);

    // Restore from snapshot
    if (snapshot) {
      Object.assign(account, snapshot.state);
    }

    // Apply recent events
    recentEvents.forEach(event => account.apply(event));

    return account;
  }

  async save(account: BankAccount): Promise<void> {
    const events = account.getUncommittedEvents();

    if (events.length === 0) return;

    await this.eventStore.appendEvents(
      account.id,
      account.version,
      events
    );

    // Create snapshot if needed
    if (account.version % this.snapshotInterval === 0) {
      await this.snapshotStore.save({
        aggregateId: account.id,
        version: account.version,
        state: account.getState(),
        createdAt: Date.now()
      });
    }

    account.clearUncommittedEvents();
  }
}
```

## Best Practices

### ✅ DO
- Store events immutably
- Version your events
- Use optimistic concurrency
- Create snapshots for performance
- Use projections for queries
- Keep events small and focused
- Include metadata (timestamp, user, etc.)
- Handle event versioning/migration

### ❌ DON'T
- Mutate past events
- Store current state only
- Skip concurrency checks
- Query event store for reads
- Make events too large
- Forget about event schema evolution

## Resources

- [Event Sourcing - Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)
- [EventStoreDB](https://www.eventstore.com/)
