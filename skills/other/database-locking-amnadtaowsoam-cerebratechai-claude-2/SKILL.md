---
name: Database Locking Strategies
description: Understanding and implementing database locking mechanisms for concurrency control.
---

# Database Locking Strategies

## Overview

Database locking is a mechanism used to manage concurrent access to shared data. It ensures data integrity by preventing multiple transactions from modifying the same data simultaneously in ways that could cause inconsistencies.

## Prerequisites

- Understanding of database transactions and ACID properties
- Knowledge of SQL and database operations
- Familiarity with concurrent programming concepts
- Basic understanding of isolation levels

## Key Concepts

### Why Locking is Needed (Concurrency Control)

#### The Problem

Without locking, concurrent transactions can cause:

1. **Lost Updates**: Two transactions read and update same value, one update is lost
2. **Dirty Reads**: Reading uncommitted changes from another transaction
3. **Non-Repeatable Reads**: Same query returns different results within same transaction
4. **Phantom Reads**: New rows appear in subsequent queries

#### Example: Lost Update

```sql
-- Transaction 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Reads $1000
-- ... processing ...
UPDATE accounts SET balance = 900 WHERE id = 1;  -- $1000 - $100

-- Transaction 2 (concurrent)
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Reads $1000
UPDATE accounts SET balance = 1100 WHERE id = 1;  -- $1000 + $100
COMMIT;

-- Transaction 1 continues
COMMIT;  -- Final balance is $1100, lost the -$100 update!
```

#### Solution: Locking

```sql
-- Transaction 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;  -- Locks row
-- ... processing ...
UPDATE accounts SET balance = 900 WHERE id = 1;
COMMIT;  -- Releases lock

-- Transaction 2 waits for lock
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;  -- Waits...
-- Transaction 1 commits, now can proceed
SELECT balance FROM accounts WHERE id = 1;  -- Reads $900
UPDATE accounts SET balance = 1000 WHERE id = 1;
COMMIT;  -- Final balance is $1000, correct!
```

### Lock Types

#### Shared Locks (Read Locks)

Allow multiple transactions to read data but prevent writes.

```sql
-- Transaction 1
BEGIN;
SELECT * FROM products WHERE id = 1 FOR SHARE;  -- Shared lock
-- Other transactions can also read with FOR SHARE
-- But cannot update until this transaction commits
COMMIT;
```

**Characteristics:**
- Multiple readers can hold shared locks
- Writers are blocked
- Used when reading data that might be updated later

#### Exclusive Locks (Write Locks)

Prevent any other transaction from reading or writing.

```sql
-- Transaction 1
BEGIN;
SELECT * FROM products WHERE id = 1 FOR UPDATE;  -- Exclusive lock
-- Other transactions cannot read or update this row
COMMIT;
```

**Characteristics:**
- Only one transaction can hold exclusive lock
- Blocks all other transactions
- Used when updating data

#### Intent Locks

Indicate intention to acquire locks at a finer granularity.

```sql
-- Transaction 1
BEGIN;
-- Intent to lock table
LOCK TABLE products IN SHARE MODE;

-- Then lock specific rows
SELECT * FROM products WHERE id = 1 FOR UPDATE;

COMMIT;
```

**Types:**
- **Intent Shared (IS)**: Intention to acquire shared locks on rows
- **Intent Exclusive (IX)**: Intention to acquire exclusive locks on rows
- **Shared (S)**: Shared lock on entire table
- **Exclusive (X)**: Exclusive lock on entire table

**Lock Compatibility Matrix:**

| Lock Type | IS | IX | S | X |
|-----------|-----|-----|---|---|
| IS | ✓ | ✓ | ✓ | ✗ |
| IX | ✓ | ✓ | ✗ | ✗ |
| S | ✓ | ✗ | ✓ | ✗ |
| X | ✗ | ✗ | ✗ | ✗ |

#### Update Locks

A special lock that allows other shared locks but converts to exclusive when updating.

```sql
-- PostgreSQL automatically uses update locks
BEGIN;
SELECT * FROM products WHERE id = 1 FOR UPDATE;

-- During read, allows other FOR SHARE
-- When updating, converts to exclusive
UPDATE products SET stock = stock - 1 WHERE id = 1;

COMMIT;
```

### Lock Granularity

#### Row-Level Locks

Lock individual rows, allowing concurrent access to other rows.

```sql
-- Transaction 1
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- Locks row 1 only
-- Other transactions can access other rows
SELECT * FROM accounts WHERE id = 2 FOR UPDATE;  -- This works
COMMIT;
```

**Pros:**
- High concurrency
- Fine-grained control
- Good for OLTP workloads

**Cons:**
- More lock management overhead
- Can cause deadlocks
- May not be efficient for bulk operations

#### Page-Level Locks

Lock database pages (typically 8KB-16KB).

```sql
-- Some databases use page-level locking automatically
-- When you lock a row, the entire page containing it is locked
-- This affects multiple rows on the same page
```

**Pros:**
- Less overhead than row-level
- Good for sequential access patterns

**Cons:**
- Lower concurrency than row-level
- Can lock unintended rows

#### Table-Level Locks

Lock entire table.

```sql
-- Transaction 1
BEGIN;
LOCK TABLE accounts IN EXCLUSIVE MODE;  -- Locks entire table
-- No other transaction can access this table
COMMIT;
```

**Pros:**
- Simple to understand
- Good for bulk operations
- Minimal lock management overhead

**Cons:**
- Very low concurrency
- Blocks all access to table

**Lock Modes:**
- `ACCESS SHARE`: SELECT
- `ROW SHARE`: SELECT FOR UPDATE
- `ROW EXCLUSIVE`: INSERT, UPDATE, DELETE
- `SHARE UPDATE EXCLUSIVE`: VACUUM, ANALYZE
- `SHARE`: CREATE INDEX CONCURRENTLY
- `SHARE ROW EXCLUSIVE`: LOCK TABLE
- `EXCLUSIVE`: REFRESH MATERIALIZED VIEW
- `ACCESS EXCLUSIVE`: DROP TABLE, TRUNCATE

#### Database-Level Locks

Lock entire database.

```sql
-- PostgreSQL
BEGIN;
LOCK DATABASE mydb IN ACCESS EXCLUSIVE MODE;
-- No other session can connect to this database
COMMIT;
```

**Use Cases:**
- Database maintenance
- Schema changes
- Backup operations

## Implementation Guide

### Pessimistic Locking

#### SELECT FOR UPDATE

Lock rows for update.

```javascript
// Node.js with PostgreSQL
async function transferMoney(fromId, toId, amount) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    // Lock both accounts
    const [fromAccount] = await client.query(
      'SELECT * FROM accounts WHERE id = $1 FOR UPDATE',
      [fromId]
    );

    const [toAccount] = await client.query(
      'SELECT * FROM accounts WHERE id = $1 FOR UPDATE',
      [toId]
    );

    // Check balance
    if (fromAccount.rows[0].balance < amount) {
      throw new Error('Insufficient balance');
    }

    // Perform transfer
    await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
      [amount, fromId]
    );

    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
      [amount, toId]
    );

    await client.query('COMMIT');
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

#### SELECT FOR SHARE

Allow multiple readers but block writers.

```javascript
async function getProductStock(productId) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    // Lock for share - multiple readers OK
    const result = await client.query(
      'SELECT * FROM products WHERE id = $1 FOR SHARE',
      [productId]
    );

    const product = result.rows[0];

    // Check stock
    if (product.stock < 1) {
      await client.query('ROLLBACK');
      throw new Error('Out of stock');
    }

    // Update stock
    await client.query(
      'UPDATE products SET stock = stock - 1 WHERE id = $1',
      [productId]
    );

    await client.query('COMMIT');
    return product;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

#### Lock Timeout

```javascript
async function transferWithTimeout(fromId, toId, amount) {
  const client = await pool.connect();
  try {
    // Set lock timeout to 5 seconds
    await client.query('SET lock_timeout = 5000');
    await client.query('BEGIN');

    try {
      const [fromAccount] = await client.query(
        'SELECT * FROM accounts WHERE id = $1 FOR UPDATE',
        [fromId]
      );

      const [toAccount] = await client.query(
        'SELECT * FROM accounts WHERE id = $1 FOR UPDATE',
        [toId]
      );

      // ... transfer logic ...

      await client.query('COMMIT');
    } catch (error) {
      if (error.code === '55P03') {  // Lock not available
        throw new Error('Could not acquire lock, please try again');
      }
      throw error;
    }
  } finally {
    client.release();
  }
}
```

### Optimistic Locking

#### Version Columns

Add a version column to track changes.

```sql
CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  balance DECIMAL(10,2),
  version INT DEFAULT 0
);
```

```javascript
async function updateAccount(accountId, newBalance) {
  let retries = 0;
  const maxRetries = 3;

  while (retries < maxRetries) {
    // Read current version
    const [result] = await pool.query(
      'SELECT * FROM accounts WHERE id = $1',
      [accountId]
    );
    const account = result.rows[0];

    // Try to update with version check
    const updateResult = await pool.query(
      'UPDATE accounts SET balance = $1, version = version + 1 WHERE id = $2 AND version = $3',
      [newBalance, accountId, account.version]
    );

    if (updateResult.rowCount > 0) {
      // Success
      return updateResult.rows[0];
    }

    // Version mismatch - retry
    retries++;
    await sleep(100 * retries);  // Exponential backoff
  }

  throw new Error('Max retries exceeded');
}
```

#### Timestamp Columns

Use timestamp for optimistic locking.

```sql
CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  balance DECIMAL(10,2),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```javascript
async function updateAccount(accountId, newBalance) {
  // Read current timestamp
  const [result] = await pool.query(
    'SELECT * FROM accounts WHERE id = $1',
    [accountId]
  );
  const account = result.rows[0];

  // Try to update with timestamp check
  const updateResult = await pool.query(
    'UPDATE accounts SET balance = $1, updated_at = NOW() WHERE id = $2 AND updated_at = $3',
    [newBalance, accountId, account.updated_at]
  );

  if (updateResult.rowCount === 0) {
    throw new Error('Account was modified by another transaction');
  }

  return updateResult.rows[0];
}
```

#### Conditional Updates

Use WHERE clause to check current state.

```javascript
async function decrementStock(productId, quantity) {
  const result = await pool.query(
    'UPDATE products SET stock = stock - $1 WHERE id = $2 AND stock >= $1',
    [quantity, productId]
  );

  if (result.rowCount === 0) {
    throw new Error('Insufficient stock');
  }

  return result.rows[0];
}
```

## Deadlock

### Detection

Databases automatically detect deadlocks and choose a victim to rollback.

```sql
-- Transaction 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Locks row 1
-- Waiting for row 2...
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Transaction 2 (concurrent)
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 2;  -- Locks row 2
-- Waiting for row 1...
UPDATE accounts SET balance = balance + 100 WHERE id = 1;

-- DEADLOCK! Database detects and rolls back one transaction
```

### Prevention

**Consistent Lock Ordering:**

```javascript
// Always lock rows in the same order (e.g., by ID)
async function transferMoney(fromId, toId, amount) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    // Always lock lower ID first
    const [firstId, secondId] = fromId < toId
      ? [fromId, toId]
      : [toId, fromId];

    await client.query(
      'SELECT * FROM accounts WHERE id = $1 FOR UPDATE',
      [firstId]
    );

    await client.query(
      'SELECT * FROM accounts WHERE id = $1 FOR UPDATE',
      [secondId]
    );

    // ... transfer logic ...

    await client.query('COMMIT');
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

**Short Transactions:**

```javascript
// Keep transactions short to reduce deadlock window
async function transferMoney(fromId, toId, amount) {
  // Validate before transaction
  const fromAccount = await pool.query(
    'SELECT * FROM accounts WHERE id = $1',
    [fromId]
  );

  if (fromAccount.rows[0].balance < amount) {
    throw new Error('Insufficient balance');
  }

  // Short transaction for actual transfer
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
      [amount, fromId]
    );

    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
      [amount, toId]
    );

    await client.query('COMMIT');
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

### Resolution Strategies

```javascript
async function executeWithRetry(fn, maxRetries = 3) {
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      return await fn();
    } catch (error) {
      if (error.code === '40P01') {  // Deadlock detected
        attempt++;
        const delay = 100 * Math.pow(2, attempt);  // Exponential backoff
        await sleep(delay);
      } else {
        throw error;
      }
    }
  }

  throw new Error('Max retries exceeded due to deadlock');
}

// Usage
await executeWithRetry(async () => {
  await transferMoney(1, 2, 100);
});
```

## Advisory Locks

### PostgreSQL Advisory Locks

Application-level locks not tied to specific rows.

```sql
-- Acquire advisory lock
SELECT pg_advisory_lock(12345);  -- Returns true if acquired

-- Check if lock is held
SELECT pg_advisory_lock_shared(12345);

-- Release lock
SELECT pg_advisory_unlock(12345);
```

```javascript
// Use advisory locks for distributed tasks
async function processTask(taskId) {
  const lockId = hashTaskId(taskId);

  // Try to acquire lock
  const [result] = await pool.query(
    'SELECT pg_try_advisory_lock($1) AS acquired',
    [lockId]
  );

  if (!result.rows[0].acquired) {
    throw new Error('Task is already being processed');
  }

  try {
    // Process task
    await processTaskLogic(taskId);
  } finally {
    // Release lock
    await pool.query('SELECT pg_advisory_unlock($1)', [lockId]);
  }
}
```

### MySQL GET_LOCK

```sql
-- Acquire named lock
SELECT GET_LOCK('my_lock', 10);  -- 10 second timeout

-- Check if lock is held
SELECT IS_FREE_LOCK('my_lock');

-- Release lock
SELECT RELEASE_LOCK('my_lock');
```

```javascript
// Use named locks for distributed coordination
async function processJob(jobId) {
  const lockName = `job_${jobId}`;

  // Try to acquire lock with 10 second timeout
  const [result] = await pool.query(
    'SELECT GET_LOCK(?, 10) AS acquired',
    [lockName]
  );

  if (result[0].acquired === 0) {
    throw new Error('Job is already being processed');
  }

  try {
    // Process job
    await processJobLogic(jobId);
  } finally {
    // Release lock
    await pool.query('SELECT RELEASE_LOCK(?)', [lockName]);
  }
}
```

## Distributed Locking

### Redis Distributed Lock

```javascript
const Redis = require('ioredis');
const crypto = require('crypto');

class DistributedLock {
  constructor(redis, key, options = {}) {
    this.redis = redis;
    this.key = `lock:${key}`;
    this.ttl = options.ttl || 30000;  // 30 seconds
    this.value = crypto.randomBytes(16).toString('hex');
  }

  async acquire() {
    // Try to acquire lock with SET NX (only if not exists)
    const acquired = await this.redis.set(
      this.key,
      this.value,
      'PX', this.ttl,  // Expire after TTL
      'NX'  // Only set if not exists
    );

    return acquired === 'OK';
  }

  async release() {
    // Only release if we own the lock
    const script = `
      if redis.call('GET', KEYS[1]) == ARGV[1] then
        return redis.call('DEL', KEYS[1])
      else
        return 0
      end
    `;

    await this.redis.eval(script, 1, this.key, this.value);
  }

  async extend(newTtl) {
    // Extend lock TTL
    const script = `
      if redis.call('GET', KEYS[1]) == ARGV[1] then
        return redis.call('PEXPIRE', KEYS[1], ARGV[2])
      else
        return 0
      end
    `;

    const result = await this.redis.eval(
      script,
      1,
      this.key,
      this.value,
      newTtl
    );

    return result === 1;
  }
}

// Usage
const redis = new Redis();
const lock = new DistributedLock(redis, 'resource_123', { ttl: 30000 });

if (await lock.acquire()) {
  try {
    // Critical section
    await processResource(123);
  } finally {
    await lock.release();
  }
} else {
  throw new Error('Could not acquire lock');
}
```

### ZooKeeper Distributed Lock

```javascript
const ZooKeeper = require('zookeeper');

class ZKLock {
  constructor(zk, path, options = {}) {
    this.zk = zk;
    this.path = `/locks/${path}`;
    this.timeout = options.timeout || 30000;
  }

  async acquire() {
    return new Promise((resolve, reject) => {
      // Create ephemeral node
      this.zk.create(
        this.path,
        Buffer.from(''),
        ZooKeeper.CreateMode.EPHEMERAL,
        (error, path) => {
          if (error) {
            reject(error);
          } else {
            this.lockPath = path;
            resolve(true);
          }
        }
      );

      // Timeout
      setTimeout(() => {
        reject(new Error('Lock timeout'));
      }, this.timeout);
    });
  }

  async release() {
    return new Promise((resolve, reject) => {
      this.zk.delete(
        this.lockPath,
        (error) => {
          if (error) {
            reject(error);
          } else {
            resolve();
          }
        }
      );
    });
  }
}
```

## MVCC (Multi-Version Concurrency Control)

### How MVCC Works

MVCC allows readers to not block writers and vice versa by maintaining multiple versions of each row.

```
Row 1 (id=1, name="John", version=1)
  ↓ Update by Transaction A
Row 1 (id=1, name="Jane", version=2)
  ↓ Update by Transaction B
Row 1 (id=1, name="Jane", version=3)

Transaction A sees version=1
Transaction B sees version=2
New transactions see version=3
```

### PostgreSQL MVCC

```sql
-- Transaction 1
BEGIN;
SELECT * FROM users WHERE id = 1;  -- Sees version at transaction start
-- Even if other transaction commits changes, this sees old version

-- Transaction 2 (concurrent)
BEGIN;
UPDATE users SET name = 'Jane' WHERE id = 1;
COMMIT;  -- Creates new version

-- Transaction 1 continues
SELECT * FROM users WHERE id = 1;  -- Still sees old version
COMMIT;
```

### MySQL MVCC (InnoDB)

```sql
-- Transaction 1
START TRANSACTION;
SELECT * FROM users WHERE id = 1 FOR UPDATE;  -- Locks row
-- Waits if row is locked by another transaction

-- Transaction 2 (concurrent)
START TRANSACTION;
UPDATE users SET name = 'Jane' WHERE id = 1;  -- Waits for lock
-- Transaction 1 commits, then this proceeds
COMMIT;
```

## PostgreSQL vs MySQL Locking Differences

### Lock Modes Comparison

| Feature | PostgreSQL | MySQL (InnoDB) |
|----------|--------------|-------------------|
| **Row Locking** | FOR UPDATE, FOR SHARE | FOR UPDATE |
| **Lock Timeout** | lock_timeout parameter | innodb_lock_wait_timeout |
| **Advisory Locks** | pg_advisory_lock | GET_LOCK |
| **Lock Escalation** | No | Yes (automatically) |
| **Deadlock Detection** | Automatic | Automatic |
| **MVCC** | Yes (snapshot isolation) | Yes (undo log) |

### PostgreSQL-Specific

```sql
-- SELECT FOR UPDATE SKIP LOCKED - Skip locked rows
SELECT * FROM jobs
WHERE status = 'pending'
FOR UPDATE SKIP LOCKED
LIMIT 10;

-- SELECT FOR UPDATE NOWAIT - Fail immediately if locked
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT;
```

### MySQL-Specific

```sql
-- SELECT ... LOCK IN SHARE MODE - Shared lock
SELECT * FROM products WHERE id = 1 LOCK IN SHARE MODE;

-- SELECT ... FOR UPDATE - Exclusive lock
SELECT * FROM products WHERE id = 1 FOR UPDATE;

-- Low priority updates
UPDATE LOW_PRIORITY accounts SET balance = balance - 100 WHERE id = 1;
```

## Monitoring Locks

### PostgreSQL

```sql
-- View current locks
SELECT
  pid,
  relation::regclass AS table,
  mode,
  granted,
  query
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE l.granted = false;  -- Waiting locks

-- View lock statistics
SELECT * FROM pg_stat_user_tables;
```

### MySQL

```sql
-- View current locks
SELECT * FROM information_schema.INNODB_LOCKS;

-- View lock waits
SELECT * FROM information_schema.INNODB_LOCK_WAITS;

-- View lock wait graph
SELECT
  r.trx_id AS waiting_trx,
  r.trx_mysql_thread_id AS waiting_thread,
  b.trx_id AS blocking_trx,
  b.trx_mysql_thread_id AS blocking_thread
FROM information_schema.INNODB_LOCK_WAITS w
JOIN information_schema.INNODB_TRX r ON w.requesting_trx_id = r.trx_id
JOIN information_schema.INNODB_TRX b ON w.blocking_trx_id = b.trx_id;
```

## Troubleshooting Lock Contention

### Identify Contention

```sql
-- PostgreSQL: Find most locked tables
SELECT
  relation::regclass AS table,
  COUNT(*) AS lock_count
FROM pg_locks
WHERE relation IS NOT NULL
GROUP BY relation
ORDER BY lock_count DESC
LIMIT 10;

-- MySQL: Find most locked tables
SELECT
  table_name,
  COUNT(*) AS lock_count
FROM information_schema.INNODB_LOCKS
GROUP BY table_name
ORDER BY lock_count DESC
LIMIT 10;
```

### Solutions

1. **Reduce Lock Duration**
   - Keep transactions short
   - Avoid long-running queries
   - Process in batches

2. **Reduce Lock Scope**
   - Use row-level locks instead of table-level
   - Lock only necessary rows
   - Use appropriate isolation levels

3. **Use Optimistic Locking**
   - For low-contention scenarios
   - Implement retry logic
   - Use version/timestamp columns

4. **Improve Indexing**
   - Proper indexes reduce lock scope
   - Avoid full table scans
   - Use covering indexes

## Best Practices

1. **Choose Right Locking Strategy**
   - Pessimistic locking for high contention
   - Optimistic locking for low contention
   - Use row-level locks when possible
   - Consider advisory locks for application coordination

2. **Handle Deadlocks**
   - Implement consistent lock ordering
   - Keep transactions short
   - Add retry logic
   - Log deadlocks for analysis

3. **Set Appropriate Timeouts**
   - Configure lock timeout
   - Handle timeout errors gracefully
   - Provide feedback to users

4. **Monitor Locking**
   - Track lock wait times
   - Monitor deadlock frequency
   - Identify contention hotspots
   - Set up alerts

5. **Test Thoroughly**
   - Test concurrent access
   - Simulate deadlock scenarios
   - Verify isolation levels
   - Test under load

## Related Skills

- [`04-database/database-transactions`](04-database/database-transactions/SKILL.md)
- [`04-database/database-optimization`](04-database/database-optimization/SKILL.md)
- [`04-database/connection-pooling`](04-database/connection-pooling/SKILL.md)
