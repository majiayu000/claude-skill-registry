---
name: Connection Pooling
description: Implementing and optimizing database connection pools for high-performance applications.
---

# Connection Pooling

## Overview

Connection pooling is a technique used to maintain a cache of database connections that can be reused instead of creating a new connection for each request. This significantly improves application performance by reducing the overhead of establishing new connections.

## What is Connection Pooling and Why It Matters

### The Problem Without Pooling

Without connection pooling, each database operation requires:

1. **TCP Connection Establishment** - Network handshake
2. **Authentication** - Verify credentials
3. **Session Initialization** - Set session parameters
4. **Query Execution** - Actual work
5. **Connection Teardown** - Close connection

This process can take 50-500ms, which is significant when multiplied across thousands of requests.

### The Solution With Pooling

With connection pooling:

1. **Borrow Connection** - Get from pool (~1ms)
2. **Query Execution** - Actual work
3. **Return Connection** - Back to pool (~1ms)

The pool maintains a set of established connections that are reused across requests.

### Benefits

- **Performance**: 10-100x faster connection acquisition
- **Resource Efficiency**: Fewer connections to the database
- **Scalability**: Handle more concurrent requests
- **Stability**: Prevents connection storms

## Connection Lifecycle

### Pool States

```
┌─────────────────────────────────────────────────────────────┐
│                    Connection Pool                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │    Idle      │    │    Active    │    │   Creating   │ │
│  │ Connections  │◄──►│ Connections  │◄──►│ Connections  │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         ▲                                      ▲           │
│         │                                      │           │
│         └──────────────────────────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Lifecycle Stages

```javascript
// 1. Create
const pool = new Pool({
  host: 'localhost',
  database: 'mydb',
  max: 20,  // Maximum pool size
});

// 2. Acquire (Borrow)
const connection = await pool.connect();
// Connection is now marked as active

// 3. Use
const result = await connection.query('SELECT * FROM users');

// 4. Release (Return)
connection.release();
// Connection is now marked as idle

// 5. Destroy (if needed)
// Pool may destroy connections that are:
// - Too old (maxLifetime)
// - Idle too long (idleTimeout)
// - Failed health check
```

### Detailed Lifecycle

```javascript
class Connection {
  constructor(pool) {
    this.pool = pool;
    this.state = 'idle';  // idle, active, creating, destroying
    this.createdAt = Date.now();
    this.lastUsed = Date.now();
    this.lastValidated = null;
  }
  
  async acquire() {
    if (this.state !== 'idle') {
      throw new Error('Connection not idle');
    }
    
    // Validate before returning
    await this.validate();
    
    this.state = 'active';
    this.lastUsed = Date.now();
    return this;
  }
  
  async release() {
    if (this.state !== 'active') {
      throw new Error('Connection not active');
    }
    
    // Reset connection state
    await this.reset();
    
    this.state = 'idle';
    this.lastUsed = Date.now();
    
    // Notify pool
    this.pool.onConnectionReleased(this);
  }
  
  async validate() {
    // Simple ping
    await this.query('SELECT 1');
    this.lastValidated = Date.now();
  }
  
  async reset() {
    // Reset session state
    await this.query('RESET ALL');
    await this.query('DISCARD ALL');
  }
  
  async destroy() {
    this.state = 'destroying';
    await this.end();
    this.state = 'destroyed';
  }
}
```

## Pool Sizing Strategies

### Basic Sizing Formula

A common starting point for pool sizing:

```
pool_size = (core_count * 2) + effective_spindle_count
```

For modern SSD-based databases:
```
pool_size = core_count * 2
```

### Connection Pool vs Database Limits

```javascript
// Database server configuration
max_connections = 100  // PostgreSQL default

// Application instances (4 instances)
connections_per_instance = 20  // 4 * 20 = 80 total
// Leave room for superuser connections, replication, etc.
```

### Dynamic Pool Sizing

```javascript
class DynamicPool {
  constructor(options) {
    this.min = options.min || 2;
    this.max = options.max || 20;
    this.connections = [];
    this.activeConnections = 0;
  }
  
  async getConnection() {
    // Try to get idle connection
    const idle = this.connections.find(c => c.state === 'idle');
    if (idle) {
      return idle.acquire();
    }
    
    // Create new connection if under max
    if (this.connections.length < this.max) {
      const conn = await this.createConnection();
      this.connections.push(conn);
      return conn.acquire();
    }
    
    // Wait for available connection
    return this.waitForAvailableConnection();
  }
  
  releaseConnection(conn) {
    conn.release();
    
    // Destroy excess idle connections
    this.pruneIdleConnections();
  }
  
  pruneIdleConnections() {
    const idle = this.connections.filter(c => c.state === 'idle');
    const excess = idle.length - this.min;
    
    if (excess > 0) {
      // Destroy oldest idle connections
      idle.slice(0, excess).forEach(c => c.destroy());
    }
  }
}
```

### Pool Sizing Calculator

```javascript
function calculatePoolSize(options) {
  const {
    cpuCores = 4,
    dbMaxConnections = 100,
    appInstances = 1,
    targetUtilization = 0.75,  // 75% utilization
  } = options;
  
  // Calculate connections per instance
  const totalAvailable = dbMaxConnections * targetUtilization;
  const connectionsPerInstance = Math.floor(totalAvailable / appInstances);
  
  // Use formula: cores * 2, but cap at available
  const formulaSize = cpuCores * 2;
  const poolSize = Math.min(formulaSize, connectionsPerInstance);
  
  return {
    poolSize,
    formulaSize,
    connectionsPerInstance,
    totalAvailable,
    maxConnections: dbMaxConnections,
  };
}

// Example
console.log(calculatePoolSize({
  cpuCores: 8,
  dbMaxConnections: 100,
  appInstances: 4,
}));
// Output: { poolSize: 16, formulaSize: 16, connectionsPerInstance: 18, ... }
```

## Connection Validation

### Test-on-Borrow

Validate connection before giving it to the application.

```javascript
class ValidatingPool {
  constructor(options) {
    this.testOnBorrow = options.testOnBorrow !== false;  // Default true
    this.validationQuery = options.validationQuery || 'SELECT 1';
  }
  
  async getConnection() {
    const conn = await this.acquireConnection();
    
    if (this.testOnBorrow) {
      try {
        await conn.query(this.validationQuery);
      } catch (error) {
        // Connection is bad, destroy and get another
        await conn.destroy();
        return this.getConnection();
      }
    }
    
    return conn;
  }
}
```

### Test-on-Return

Validate connection before returning to pool.

```javascript
class ValidatingPool {
  constructor(options) {
    this.testOnReturn = options.testOnReturn || false;
  }
  
  async releaseConnection(conn) {
    if (this.testOnReturn) {
      try {
        await conn.query('SELECT 1');
      } catch (error) {
        // Connection is bad, destroy it
        await conn.destroy();
        return;
      }
    }
    
    conn.release();
  }
}
```

### Test-While-Idle

Periodically validate idle connections.

```javascript
class IdleValidatingPool {
  constructor(options) {
    this.idleValidationInterval = options.idleValidationInterval || 60000;  // 1 minute
    this.startIdleValidation();
  }
  
  startIdleValidation() {
    setInterval(() => {
      this.validateIdleConnections();
    }, this.idleValidationInterval);
  }
  
  async validateIdleConnections() {
    const idleConnections = this.connections.filter(c => 
      c.state === 'idle' && 
      Date.now() - c.lastValidated > this.idleValidationInterval
    );
    
    for (const conn of idleConnections) {
      try {
        await conn.query('SELECT 1');
        conn.lastValidated = Date.now();
      } catch (error) {
        await conn.destroy();
      }
    }
  }
}
```

## Timeout Configurations

### Connection Timeout

Time to wait for a connection from the pool.

```javascript
const pool = new Pool({
  host: 'localhost',
  connectionTimeoutMillis: 5000,  // 5 seconds
});

try {
  const conn = await pool.connect();
  // ...
} catch (error) {
  if (error.code === 'CONNECTION_TIMEOUT') {
    console.error('Timeout waiting for connection');
  }
}
```

### Idle Timeout

Time after which idle connections are closed.

```javascript
const pool = new Pool({
  host: 'localhost',
  idleTimeoutMillis: 30000,  // 30 seconds
  // Connections idle for >30s will be closed
});
```

### Max Lifetime

Maximum time a connection can exist before being closed.

```javascript
const pool = new Pool({
  host: 'localhost',
  maxLifetimeMillis: 3600000,  // 1 hour
  // Connections older than 1 hour will be closed
});
```

### Query Timeout

Time limit for individual queries.

```javascript
const pool = new Pool({
  host: 'localhost',
  query_timeout: 30000,  // 30 seconds
});

try {
  await pool.query('SELECT * FROM large_table');
} catch (error) {
  if (error.code === 'QUERY_TIMEOUT') {
    console.error('Query timed out');
  }
}
```

### Complete Timeout Configuration

```javascript
const pool = new Pool({
  host: 'localhost',
  database: 'mydb',
  user: 'user',
  password: 'pass',
  
  // Pool timeouts
  connectionTimeoutMillis: 5000,      // Wait for connection
  idleTimeoutMillis: 30000,           // Close idle connections
  maxLifetimeMillis: 3600000,         // Close old connections
  
  // Query timeout
  query_timeout: 30000,
  
  // Statement timeout (PostgreSQL)
  statement_timeout: '30s',
});
```

## Connection Leaks Detection and Prevention

### What is a Connection Leak?

A connection leak occurs when a connection is acquired from the pool but never returned, causing the pool to eventually run out of available connections.

### Detection

```javascript
class LeakDetectingPool {
  constructor(options) {
    this.leakDetectionThreshold = options.leakDetectionThreshold || 30000;  // 30s
    this.borrowedConnections = new Map();
  }
  
  async getConnection() {
    const conn = await this.acquireConnection();
    const borrowId = generateId();
    
    this.borrowedConnections.set(borrowId, {
      connection: conn,
      borrowedAt: Date.now(),
      stackTrace: new Error().stack,
    });
    
    // Set timeout to detect leak
    setTimeout(() => {
      const borrowed = this.borrowedConnections.get(borrowId);
      if (borrowed) {
        console.error('Potential connection leak detected!');
        console.error('Connection borrowed at:', borrowed.borrowedAt);
        console.error('Stack trace:', borrowed.stackTrace);
      }
    }, this.leakDetectionThreshold);
    
    return {
      connection: conn,
      release: () => this.releaseConnection(borrowId),
    };
  }
  
  releaseConnection(borrowId) {
    const borrowed = this.borrowedConnections.get(borrowId);
    if (!borrowed) {
      console.warn('Connection already released or never borrowed');
      return;
    }
    
    borrowed.connection.release();
    this.borrowedConnections.delete(borrowId);
  }
}

// Usage
const { connection, release } = await pool.getConnection();
try {
  await connection.query('SELECT * FROM users');
} finally {
  release();  // Always release!
}
```

### Prevention with Automatic Cleanup

```javascript
class AutoCleaningPool {
  constructor(options) {
    this.autoCleanupInterval = options.autoCleanupInterval || 60000;
    this.borrowedConnections = new Map();
    this.startAutoCleanup();
  }
  
  startAutoCleanup() {
    setInterval(() => {
      this.cleanupStaleConnections();
    }, this.autoCleanupInterval);
  }
  
  cleanupStaleConnections() {
    const now = Date.now();
    
    for (const [borrowId, borrowed] of this.borrowedConnections) {
      const age = now - borrowed.borrowedAt;
      
      if (age > this.leakDetectionThreshold) {
        console.warn(`Force returning leaked connection (age: ${age}ms)`);
        borrowed.connection.release();
        this.borrowedConnections.delete(borrowId);
      }
    }
  }
}
```

### Using with try-finally Pattern

```javascript
// Always use try-finally to ensure release
async function getUsers() {
  const { connection, release } = await pool.getConnection();
  try {
    return await connection.query('SELECT * FROM users');
  } finally {
    release();
  }
}

// Or with async resource tracking
async function withConnection(fn) {
  const { connection, release } = await pool.getConnection();
  try {
    return await fn(connection);
  } finally {
    release();
  }
}

// Usage
const users = await withConnection(async (conn) => {
  return await conn.query('SELECT * FROM users');
});
```

## Pool Monitoring and Metrics

### Basic Metrics Collection

```javascript
class MonitoredPool {
  constructor(options) {
    this.metrics = {
      totalRequests: 0,
      totalWaitTime: 0,
      totalQueryTime: 0,
      errors: 0,
      timeouts: 0,
    };
  }
  
  async getConnection() {
    const startTime = Date.now();
    this.metrics.totalRequests++;
    
    try {
      const conn = await this.acquireConnection();
      const waitTime = Date.now() - startTime;
      this.metrics.totalWaitTime += waitTime;
      
      return {
        connection: conn,
        query: async (sql, params) => {
          const queryStart = Date.now();
          try {
            const result = await conn.query(sql, params);
            const queryTime = Date.now() - queryStart;
            this.metrics.totalQueryTime += queryTime;
            return result;
          } catch (error) {
            this.metrics.errors++;
            throw error;
          }
        },
        release: () => conn.release(),
      };
    } catch (error) {
      if (error.code === 'CONNECTION_TIMEOUT') {
        this.metrics.timeouts++;
      }
      this.metrics.errors++;
      throw error;
    }
  }
  
  getMetrics() {
    const avgWaitTime = this.metrics.totalRequests > 0
      ? this.metrics.totalWaitTime / this.metrics.totalRequests
      : 0;
    
    const avgQueryTime = this.metrics.totalRequests > 0
      ? this.metrics.totalQueryTime / this.metrics.totalRequests
      : 0;
    
    return {
      ...this.metrics,
      avgWaitTime,
      avgQueryTime,
      errorRate: this.metrics.totalRequests > 0
        ? this.metrics.errors / this.metrics.totalRequests
        : 0,
    };
  }
}
```

### Real-time Pool Status

```javascript
function getPoolStatus(pool) {
  return {
    totalCount: pool.totalCount,
    idleCount: pool.idleCount,
    waitingCount: pool.waitingCount,
    maxCount: pool.options.max,
    minCount: pool.options.min,
    utilization: pool.totalCount / pool.options.max,
  };
}

// Monitor periodically
setInterval(() => {
  const status = getPoolStatus(pool);
  console.log('Pool Status:', status);
  
  // Alert if pool is nearly exhausted
  if (status.utilization > 0.9) {
    console.warn('Pool utilization high:', status.utilization);
  }
}, 5000);
```

### Prometheus Metrics

```javascript
const promClient = require('prom-client');

// Create metrics
const poolSizeGauge = new promClient.Gauge({
  name: 'db_pool_size',
  help: 'Current pool size',
  labelNames: ['database'],
});

const poolIdleGauge = new promClient.Gauge({
  name: 'db_pool_idle',
  help: 'Number of idle connections',
  labelNames: ['database'],
});

const poolWaitingGauge = new promClient.Gauge({
  name: 'db_pool_waiting',
  help: 'Number of clients waiting for connection',
  labelNames: ['database'],
});

const poolQueryDuration = new promClient.Histogram({
  name: 'db_query_duration_seconds',
  help: 'Query execution time',
  labelNames: ['database', 'operation'],
  buckets: [0.001, 0.01, 0.1, 1, 10],
});

// Update metrics periodically
setInterval(() => {
  const status = getPoolStatus(pool);
  poolSizeGauge.set({ database: 'mydb' }, status.totalCount);
  poolIdleGauge.set({ database: 'mydb' }, status.idleCount);
  poolWaitingGauge.set({ database: 'mydb' }, status.waitingCount);
}, 5000);

// Track query duration
async function queryWithMetrics(sql) {
  const end = poolQueryDuration.startTimer({ database: 'mydb', operation: 'select' });
  try {
    return await pool.query(sql);
  } finally {
    end();
  }
}
```

## PostgreSQL Connection Poolers

### PgBouncer

PgBouncer is a lightweight connection pooler for PostgreSQL.

**Installation:**

```bash
# Ubuntu/Debian
sudo apt-get install pgbouncer

# macOS
brew install pgbouncer

# From source
wget https://pgbouncer.github.io/downloads/files/1.18.0/pgbouncer-1.18.0.tar.gz
tar xzf pgbouncer-1.18.0.tar.gz
cd pgbouncer-1.18.0
./configure && make && sudo make install
```

**Configuration (`pgbouncer.ini`):**

```ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
listen_addr = 127.0.0.1
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
max_client_conn = 1000
default_pool_size = 25
reserve_pool_size = 5
reserve_pool_timeout = 3
server_lifetime = 3600
server_idle_timeout = 600
```

**User list (`userlist.txt`):**

```
"username" "md5hash"
```

Generate MD5 hash:

```bash
echo -n "usernamepassword" | md5sum
```

**Pool Modes:**

1. **Session Pooling**: One server connection per client connection
2. **Transaction Pooling**: Server connection returned after each transaction (recommended)
3. **Statement Pooling**: Server connection returned after each statement

**Starting PgBouncer:**

```bash
pgbouncer -d /etc/pgbouncer/pgbouncer.ini
```

### Pgpool-II

Pgpool-II is a more feature-rich connection pooler with additional capabilities.

**Installation:**

```bash
# Ubuntu/Debian
sudo apt-get install pgpool2

# macOS
brew install pgpool2
```

**Configuration (`pgpool.conf`):**

```ini
# Connection settings
listen_addresses = '*'
port = 9999

# Pooling
connection_cache = on
num_init_children = 32
max_pool = 4
child_life_time = 300
connection_life_time = 0

# Load balancing
load_balance_mode = on
backend_hostname0 = 'db1.example.com'
backend_port0 = 5432
backend_weight0 = 1
backend_hostname1 = 'db2.example.com'
backend_port1 = 5432
backend_weight1 = 1
```

## MySQL Connection Pooling

### MySQL Server Configuration

```ini
[mysqld]
max_connections = 500
wait_timeout = 600
interactive_timeout = 600
```

### Node.js (mysql2)

```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'mydb',
  
  // Pool settings
  waitForConnections: true,
  connectionLimit: 20,
  queueLimit: 0,
  
  // Connection settings
  connectTimeout: 10000,
  acquireTimeout: 10000,
  timeout: 60000,
});

// Usage
async function query(sql, params) {
  const conn = await pool.getConnection();
  try {
    const [rows] = await conn.execute(sql, params);
    return rows;
  } finally {
    conn.release();
  }
}

// Close pool
await pool.end();
```

### Python (SQLAlchemy)

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'mysql://user:pass@localhost/mydb',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
)

# Usage
with engine.connect() as conn:
    result = conn.execute('SELECT * FROM users')
    print(result.fetchall())
```

## Node.js Pool Implementations

### pg (PostgreSQL)

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: 'localhost',
  database: 'mydb',
  user: 'user',
  password: 'pass',
  
  // Pool settings
  max: 20,                    // Maximum pool size
  min: 2,                     // Minimum pool size
  idleTimeoutMillis: 30000,    // Close idle connections after 30s
  connectionTimeoutMillis: 5000, // Wait 5s for connection
  
  // Connection settings
  application_name: 'myapp',
  statement_timeout: 30000,
});

// Simple query
const result = await pool.query('SELECT * FROM users');

// With connection
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('UPDATE users SET name = $1 WHERE id = $2', ['John', 1]);
  await client.query('COMMIT');
} catch (error) {
  await client.query('ROLLBACK');
  throw error;
} finally {
  client.release();
}

// Event listeners
pool.on('connect', (client) => {
  console.log('New client connected');
});

pool.on('error', (error) => {
  console.error('Pool error:', error);
});

// Graceful shutdown
await pool.end();
```

### mysql2 (MySQL)

```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'user',
  password: 'pass',
  database: 'mydb',
  
  // Pool settings
  waitForConnections: true,
  connectionLimit: 20,
  queueLimit: 0,
  
  // Connection settings
  connectTimeout: 10000,
  acquireTimeout: 10000,
  timeout: 60000,
});

// Simple query
const [rows] = await pool.query('SELECT * FROM users');

// With connection
const conn = await pool.getConnection();
try {
  await conn.beginTransaction();
  await conn.execute('UPDATE users SET name = ? WHERE id = ?', ['John', 1]);
  await conn.commit();
} catch (error) {
  await conn.rollback();
  throw error;
} finally {
  conn.release();
}

// Event listeners
pool.on('acquire', (connection) => {
  console.log('Connection %d acquired', connection.threadId);
});

pool.on('release', (connection) => {
  console.log('Connection %d released', connection.threadId);
});

pool.on('enqueue', () => {
  console.log('Waiting for available connection slot');
});

// Graceful shutdown
await pool.end();
```

## Python Pool Implementations

### SQLAlchemy

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool, NullPool

# Create engine with pooling
engine = create_engine(
    'postgresql://user:pass@localhost/mydb',
    poolclass=QueuePool,
    pool_size=20,           # Number of connections to maintain
    max_overflow=10,        # Additional connections beyond pool_size
    pool_timeout=30,         # Seconds to wait before giving up
    pool_recycle=3600,       # Recycle connections after 1 hour
    pool_pre_ping=True,      # Test connections before using
)

# Create session factory
Session = sessionmaker(bind=engine)

# Usage
def get_users():
    session = Session()
    try:
        users = session.query(User).all()
        return users
    finally:
        session.close()

# Context manager
from contextlib import contextmanager

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
with session_scope() as session:
    user = session.query(User).first()
    user.name = 'John'
```

### asyncpg (PostgreSQL - Async)

```python
import asyncpg

class ConnectionPool:
    def __init__(self, dsn, min_size=10, max_size=20):
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self.pool = None
    
    async def init(self):
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size,
            command_timeout=60,
        )
    
    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def close(self):
        await self.pool.close()

# Usage
pool = ConnectionPool('postgresql://user:pass@localhost/mydb')
await pool.init()

users = await pool.fetch('SELECT * FROM users')
await pool.close()
```

## Serverless Considerations

### Cold Start Impact

Serverless functions start cold and need to establish new connections each time.

```javascript
// Bad: New connection each invocation
exports.handler = async (event) => {
  const pool = new Pool({ /* ... */ });
  const result = await pool.query('SELECT * FROM users');
  return result;
};
```

### Connection Reuse

```javascript
// Better: Reuse connection across invocations
let pool;

async function getPool() {
  if (!pool) {
    pool = new Pool({
      host: process.env.DB_HOST,
      database: process.env.DB_NAME,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      max: 5,  // Lower max for serverless
      idleTimeoutMillis: 10000,  // Shorter idle timeout
    });
  }
  return pool;
}

exports.handler = async (event) => {
  const pool = await getPool();
  const result = await pool.query('SELECT * FROM users');
  return result;
};
```

### AWS Lambda RDS Proxy

Use AWS RDS Proxy for Lambda functions:

```javascript
// Connect through RDS Proxy
const pool = new Pool({
  host: process.env.RDS_PROXY_ENDPOINT,  // Proxy endpoint
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 5,
});
```

### Connection Limits

Serverless platforms have connection limits:

```javascript
// Calculate pool size based on concurrency
const maxConcurrentExecutions = 1000;  // Lambda limit
const avgDuration = 100;  // 100ms per request
const connectionsPerSecond = maxConcurrentExecutions / (avgDuration / 1000);
const poolSize = Math.min(connectionsPerSecond, 20);  // Cap at 20
```

## Pool Per Tenant in Multi-Tenant Apps

### Tenant-Specific Pools

```javascript
class TenantPoolManager {
  constructor() {
    this.pools = new Map();  // tenantId -> pool
  }
  
  async getPool(tenantId) {
    if (!this.pools.has(tenantId)) {
      const config = await this.getTenantConfig(tenantId);
      const pool = new Pool({
        host: config.host,
        database: config.database,
        user: config.user,
        password: config.password,
        max: 10,  // Smaller pools per tenant
      });
      this.pools.set(tenantId, pool);
    }
    return this.pools.get(tenantId);
  }
  
  async closePool(tenantId) {
    const pool = this.pools.get(tenantId);
    if (pool) {
      await pool.end();
      this.pools.delete(tenantId);
    }
  }
  
  async closeAll() {
    for (const [tenantId, pool] of this.pools) {
      await pool.end();
    }
    this.pools.clear();
  }
}

// Usage
const poolManager = new TenantPoolManager();

async function tenantQuery(tenantId, query) {
  const pool = await poolManager.getPool(tenantId);
  return await pool.query(query);
}
```

### Schema-Based Multi-Tenancy

```javascript
// Single pool, multiple schemas
const pool = new Pool({
  host: 'localhost',
  database: 'mydb',
  user: 'user',
  password: 'pass',
});

async function tenantQuery(tenantId, query) {
  const client = await pool.connect();
  try {
    // Set search path to tenant schema
    await client.query(`SET search_path TO tenant_${tenantId}`);
    return await client.query(query);
  } finally {
    client.release();
  }
}
```

## Troubleshooting Pool Exhaustion

### Symptoms

- Application hangs waiting for connections
- "Connection timeout" errors
- Slow response times

### Diagnosis

```javascript
// Check pool status
function diagnosePool(pool) {
  const status = {
    totalCount: pool.totalCount,
    idleCount: pool.idleCount,
    waitingCount: pool.waitingCount,
    maxCount: pool.options.max,
    utilization: pool.totalCount / pool.options.max,
  };
  
  console.log('Pool Status:', status);
  
  if (status.waitingCount > 10) {
    console.warn('Many clients waiting for connections');
  }
  
  if (status.utilization > 0.9) {
    console.warn('Pool nearly exhausted');
  }
  
  return status;
}
```

### Common Causes

1. **Connection Leaks**
   ```javascript
   // Bad: Connection not released
   const conn = await pool.connect();
   await conn.query('SELECT * FROM users');
   // Forgot: conn.release()
   
   // Good: Always release
   const conn = await pool.connect();
   try {
     await conn.query('SELECT * FROM users');
   } finally {
     conn.release();
   }
   ```

2. **Long-Running Queries**
   ```javascript
   // Bad: Long query holds connection
   const conn = await pool.connect();
   await conn.query('SELECT * FROM huge_table');  // Takes minutes
   
   // Good: Use cursor or pagination
   const conn = await pool.connect();
   const cursor = conn.query(new Cursor('SELECT * FROM huge_table'));
   while (true) {
     const rows = await cursor.read(1000);
     if (rows.length === 0) break;
     // Process rows
   }
   ```

3. **Pool Too Small**
   ```javascript
   // Increase pool size
   const pool = new Pool({
     max: 50,  // Increase from 20
   });
   ```

4. **Database Connection Limit Reached**
   ```sql
   -- Check current connections
   SELECT count(*) FROM pg_stat_activity;
   
   -- Check max connections
   SHOW max_connections;
   
   -- Increase if needed
   ALTER SYSTEM SET max_connections = 200;
   ```

## Best Practices and Common Mistakes

### Best Practices

1. **Pool Sizing**
   - Start with `cpu_cores * 2`
   - Monitor and adjust based on metrics
   - Consider database connection limits
   - Account for multiple application instances

2. **Timeout Configuration**
   - Set connection timeout (5-10s)
   - Set query timeout (30-60s)
   - Set idle timeout (30-60s)
   - Set max lifetime (1-8 hours)

3. **Connection Validation**
   - Enable test-on-borrow in development
   - Use test-while-idle in production
   - Set appropriate validation interval

4. **Error Handling**
   - Always release connections in finally blocks
   - Handle timeout errors gracefully
   - Log connection errors for debugging

5. **Monitoring**
   - Track pool utilization
   - Monitor wait times
   - Alert on pool exhaustion
   - Track connection errors

### Common Mistakes

1. **Not Releasing Connections**
   ```javascript
   // Bad
   const conn = await pool.connect();
   await conn.query('SELECT * FROM users');
   // Connection leaked!
   
   // Good
   const conn = await pool.connect();
   try {
     await conn.query('SELECT * FROM users');
   } finally {
     conn.release();
   }
   ```

2. **Pool Too Large**
   ```javascript
   // Bad: Too many connections
   const pool = new Pool({ max: 1000 });  // Overkill
   
   // Good: Appropriate size
   const pool = new Pool({ max: 20 });
   ```

3. **No Connection Validation**
   ```javascript
   // Bad: No validation
   const pool = new Pool({});
   
   // Good: Enable validation
   const pool = new Pool({
     idleTimeoutMillis: 30000,
     connectionTimeoutMillis: 5000,
   });
   ```

4. **Long Transactions**
   ```javascript
   // Bad: Long transaction holds connection
   const conn = await pool.connect();
   await conn.query('BEGIN');
   // ... lots of processing ...
   await conn.query('COMMIT');
   
   // Good: Keep transactions short
   const conn = await pool.connect();
   try {
     await conn.query('BEGIN');
     await conn.query('UPDATE users SET name = $1', ['John']);
     await conn.query('COMMIT');
   } catch (error) {
     await conn.query('ROLLBACK');
     throw error;
   } finally {
     conn.release();
   }
   ```

## Related Skills

- `04-database/database-optimization`
- `04-database/database-transactions`
- `14-monitoring-observability/prometheus-metrics`
