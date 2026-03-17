---
name: aws-aurora
description: AWS Aurora Serverless v2, RDS Proxy, Data API, connection pooling
---

# AWS Aurora Skill

*Load with: base.md + [typescript.md | python.md]*

Amazon Aurora is a MySQL/PostgreSQL-compatible relational database with serverless scaling, high availability, and enterprise features.

**Sources:** [Aurora Docs](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/) | [Serverless v2](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html) | [RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-proxy.html)

---

## Core Principle

**Use RDS Proxy for serverless, Data API for simplicity, connection pooling always.**

Aurora excels at ACID-compliant workloads. For serverless architectures (Lambda), always use RDS Proxy or Data API to handle connection management. Never open raw connections from Lambda functions.

---

## Aurora Options

| Option | Best For |
|--------|----------|
| **Aurora Serverless v2** | Variable workloads, auto-scaling (0.5-128 ACUs) |
| **Aurora Provisioned** | Predictable workloads, maximum performance |
| **Aurora Global** | Multi-region, disaster recovery |
| **Data API** | Serverless without VPC, simple HTTP access |
| **RDS Proxy** | Connection pooling for Lambda, high concurrency |

---

## Connection Strategies

### Strategy 1: RDS Proxy (Recommended for Lambda)
```
Lambda → RDS Proxy → Aurora
         (pool)
```
- Connection pooling and reuse
- Automatic failover handling
- IAM authentication support
- Works with existing SQL clients

### Strategy 2: Data API (Simplest for Serverless)
```
Lambda → Data API (HTTP) → Aurora
```
- No VPC required
- No connection management
- Higher latency per query
- Limited to Aurora Serverless

### Strategy 3: Direct Connection (Not for Lambda)
```
App Server → Aurora
(persistent connection)
```
- Only for long-running servers (ECS, EC2)
- Manage connection pool yourself
- Not suitable for serverless

---

## RDS Proxy Setup

### Create Proxy (AWS Console/CDK)
```typescript
// CDK example
import * as rds from 'aws-cdk-lib/aws-rds';

const proxy = new rds.DatabaseProxy(this, 'Proxy', {
  proxyTarget: rds.ProxyTarget.fromCluster(cluster),
  secrets: [cluster.secret!],
  vpc,
  securityGroups: [proxySecurityGroup],
  requireTLS: true,
  idleClientTimeout: cdk.Duration.minutes(30),
  maxConnectionsPercent: 90,
  maxIdleConnectionsPercent: 10,
  borrowTimeout: cdk.Duration.seconds(30)
});
```

### Connect via Proxy (TypeScript/Node.js)
```typescript
// lib/db.ts
import { Pool } from 'pg';
import { Signer } from '@aws-sdk/rds-signer';

const signer = new Signer({
  hostname: process.env.RDS_PROXY_ENDPOINT!,
  port: 5432,
  username: process.env.DB_USER!,
  region: process.env.AWS_REGION!
});

// IAM authentication
async function getPool(): Promise<Pool> {
  const token = await signer.getAuthToken();

  return new Pool({
    host: process.env.RDS_PROXY_ENDPOINT,
    port: 5432,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: token,
    ssl: { rejectUnauthorized: true },
    max: 1,  // Single connection for Lambda
    idleTimeoutMillis: 120000,
    connectionTimeoutMillis: 10000
  });
}

// Usage in Lambda
let pool: Pool | null = null;

export async function handler(event: any) {
  if (!pool) {
    pool = await getPool();
  }

  const result = await pool.query('SELECT * FROM users WHERE id = $1', [event.userId]);
  return result.rows[0];
}
```

### Proxy Configuration Best Practices
```bash
# Key settings for Lambda workloads
MaxConnectionsPercent: 90        # Use most of DB connections
MaxIdleConnectionsPercent: 10    # Keep some idle for bursts
ConnectionBorrowTimeout: 30s     # Wait for available connection
IdleClientTimeout: 30min         # Close idle proxy connections

# Monitor these CloudWatch metrics:
# - DatabaseConnectionsCurrentlyBorrowed
# - DatabaseConnectionsCurrentlySessionPinned
# - QueryDatabaseResponseLatency
```

---

## Data API (HTTP-based)

### Enable Data API
```bash
# Must be Aurora Serverless
aws rds modify-db-cluster \
  --db-cluster-identifier my-cluster \
  --enable-http-endpoint
```

### TypeScript with Data API Client v2
```bash
npm install data-api-client
```

```typescript
// lib/db.ts
import DataAPIClient from 'data-api-client';

const db = DataAPIClient({
  secretArn: process.env.DB_SECRET_ARN!,
  resourceArn: process.env.DB_CLUSTER_ARN!,
  database: process.env.DB_NAME!,
  region: process.env.AWS_REGION!
});

// Simple query
const users = await db.query('SELECT * FROM users WHERE active = :active', {
  active: true
});

// Insert with returning
const result = await db.query(
  'INSERT INTO users (email, name) VALUES (:email, :name) RETURNING *',
  { email: 'user@test.com', name: 'Test User' }
);

// Transaction
const transaction = await db.transaction();
try {
  await transaction.query('UPDATE accounts SET balance = balance - :amount WHERE id = :from', {
    amount: 100, from: 1
  });
  await transaction.query('UPDATE accounts SET balance = balance + :amount WHERE id = :to', {
    amount: 100, to: 2
  });
  await transaction.commit();
} catch (error) {
  await transaction.rollback();
  throw error;
}
```

### Python with boto3
```python
# requirements.txt
boto3>=1.34.0

# db.py
import boto3
import os

rds_data = boto3.client('rds-data')

CLUSTER_ARN = os.environ['DB_CLUSTER_ARN']
SECRET_ARN = os.environ['DB_SECRET_ARN']
DATABASE = os.environ['DB_NAME']


def execute_sql(sql: str, parameters: list = None):
    """Execute SQL via Data API."""
    params = {
        'resourceArn': CLUSTER_ARN,
        'secretArn': SECRET_ARN,
        'database': DATABASE,
        'sql': sql
    }

    if parameters:
        params['parameters'] = parameters

    return rds_data.execute_statement(**params)


def get_user(user_id: int):
    result = execute_sql(
        'SELECT * FROM users WHERE id = :id',
        [{'name': 'id', 'value': {'longValue': user_id}}]
    )
    return result.get('records', [])


def create_user(email: str, name: str):
    result = execute_sql(
        'INSERT INTO users (email, name) VALUES (:email, :name) RETURNING *',
        [
            {'name': 'email', 'value': {'stringValue': email}},
            {'name': 'name', 'value': {'stringValue': name}}
        ]
    )
    return result.get('generatedFields')


# Transaction
def transfer_funds(from_id: int, to_id: int, amount: float):
    transaction = rds_data.begin_transaction(
        resourceArn=CLUSTER_ARN,
        secretArn=SECRET_ARN,
        database=DATABASE
    )
    transaction_id = transaction['transactionId']

    try:
        execute_sql(
            'UPDATE accounts SET balance = balance - :amount WHERE id = :id',
            [
                {'name': 'amount', 'value': {'doubleValue': amount}},
                {'name': 'id', 'value': {'longValue': from_id}}
            ]
        )

        execute_sql(
            'UPDATE accounts SET balance = balance + :amount WHERE id = :id',
            [
                {'name': 'amount', 'value': {'doubleValue': amount}},
                {'name': 'id', 'value': {'longValue': to_id}}
            ]
        )

        rds_data.commit_transaction(
            resourceArn=CLUSTER_ARN,
            secretArn=SECRET_ARN,
            transactionId=transaction_id
        )
    except Exception as e:
        rds_data.rollback_transaction(
            resourceArn=CLUSTER_ARN,
            secretArn=SECRET_ARN,
            transactionId=transaction_id
        )
        raise e
```

---

## Prisma with Aurora

### Setup (VPC Connection via RDS Proxy)
```bash
npm install prisma @prisma/client
npx prisma init
```

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())
}
```

### Environment
```bash
# Use RDS Proxy endpoint
DATABASE_URL="postgresql://user:password@proxy-endpoint.proxy-xxx.region.rds.amazonaws.com:5432/mydb?schema=public&connection_limit=1"
```

### Lambda Handler with Prisma
```typescript
// handlers/users.ts
import { PrismaClient } from '@prisma/client';

// Reuse client across invocations
let prisma: PrismaClient | null = null;

function getPrisma(): PrismaClient {
  if (!prisma) {
    prisma = new PrismaClient({
      datasources: {
        db: { url: process.env.DATABASE_URL }
      }
    });
  }
  return prisma;
}

export async function handler(event: any) {
  const db = getPrisma();

  const users = await db.user.findMany({
    include: { posts: true },
    take: 10
  });

  return {
    statusCode: 200,
    body: JSON.stringify(users)
  };
}
```

---

## Aurora Serverless v2

### Capacity Configuration
```typescript
// CDK
const cluster = new rds.DatabaseCluster(this, 'Cluster', {
  engine: rds.DatabaseClusterEngine.auroraPostgres({
    version: rds.AuroraPostgresEngineVersion.VER_15_4
  }),
  serverlessV2MinCapacity: 0.5,  // Minimum ACUs
  serverlessV2MaxCapacity: 16,   // Maximum ACUs
  writer: rds.ClusterInstance.serverlessV2('writer'),
  readers: [
    rds.ClusterInstance.serverlessV2('reader', { scaleWithWriter: true })
  ],
  vpc,
  vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }
});
```

### Capacity Guidelines

| Workload | Min ACUs | Max ACUs |
|----------|----------|----------|
| Dev/Test | 0.5 | 2 |
| Small Production | 2 | 8 |
| Medium Production | 4 | 32 |
| Large Production | 8 | 128 |

### Handle Scale-to-Zero Wake-up
```typescript
// Data API Client v2 handles this automatically
// For direct connections, implement retry logic:

import { Pool } from 'pg';

async function queryWithRetry(
  pool: Pool,
  sql: string,
  params: any[],
  maxRetries = 3
): Promise<any> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await pool.query(sql, params);
    } catch (error: any) {
      // Aurora Serverless waking up
      if (error.code === 'ETIMEDOUT' || error.message?.includes('Communications link failure')) {
        if (attempt === maxRetries) throw error;
        // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
        continue;
      }
      throw error;
    }
  }
}
```

---

## Migrations

### Using Prisma Migrate
```bash
# Development (creates migration)
npx prisma migrate dev --name add_users_table

# Production (apply migrations)
npx prisma migrate deploy

# Generate client
npx prisma generate
```

### CI/CD Migration Script
```yaml
# .github/workflows/deploy.yml
- name: Run migrations
  run: |
    # Connect via bastion or use a migration Lambda
    npx prisma migrate deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Migration Lambda
```typescript
// lambdas/migrate.ts
import { execSync } from 'child_process';

export async function handler() {
  try {
    execSync('npx prisma migrate deploy', {
      env: {
        ...process.env,
        DATABASE_URL: process.env.DATABASE_URL
      },
      stdio: 'inherit'
    });
    return { statusCode: 200, body: 'Migrations applied' };
  } catch (error) {
    console.error('Migration failed:', error);
    throw error;
  }
}
```

---

## Connection Pooling (Non-Lambda)

### PgBouncer Sidecar (ECS/EKS)
```yaml
# docker-compose.yml
services:
  app:
    build: .
    environment:
      DATABASE_URL: postgresql://user:pass@pgbouncer:6432/mydb

  pgbouncer:
    image: edoburu/pgbouncer
    environment:
      DATABASE_URL: postgresql://user:pass@aurora-endpoint:5432/mydb
      POOL_MODE: transaction
      MAX_CLIENT_CONN: 1000
      DEFAULT_POOL_SIZE: 20
```

### Application-Level Pooling
```typescript
// For long-running servers (not Lambda)
import { Pool } from 'pg';

const pool = new Pool({
  host: process.env.DB_HOST,
  port: 5432,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,                  // Max connections
  idleTimeoutMillis: 30000, // Close idle after 30s
  connectionTimeoutMillis: 10000
});

// Use pool for all queries
export async function query(sql: string, params?: any[]) {
  const client = await pool.connect();
  try {
    return await client.query(sql, params);
  } finally {
    client.release();
  }
}
```

---

## Monitoring

### Key CloudWatch Metrics
```
# Aurora
- CPUUtilization
- DatabaseConnections
- FreeableMemory
- ServerlessDatabaseCapacity (ACUs)
- AuroraReplicaLag

# RDS Proxy
- DatabaseConnectionsCurrentlyBorrowed
- DatabaseConnectionsCurrentlySessionPinned
- QueryDatabaseResponseLatency
- ClientConnectionsReceived
```

### Performance Insights
```bash
# Enable via console or CLI
aws rds modify-db-cluster \
  --db-cluster-identifier my-cluster \
  --enable-performance-insights \
  --performance-insights-retention-period 7
```

---

## Security

### IAM Database Authentication
```typescript
import { Signer } from '@aws-sdk/rds-signer';

const signer = new Signer({
  hostname: process.env.DB_HOST!,
  port: 5432,
  username: 'iam_user',
  region: 'us-east-1'
});

const token = await signer.getAuthToken();

// Use token as password (valid for 15 minutes)
const pool = new Pool({
  host: process.env.DB_HOST,
  user: 'iam_user',
  password: token,
  ssl: true
});
```

### Secrets Manager Rotation
```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getDbCredentials() {
  const response = await client.send(
    new GetSecretValueCommand({ SecretId: process.env.DB_SECRET_ARN })
  );
  return JSON.parse(response.SecretString!);
}
```

---

## CLI Quick Reference

```bash
# Cluster operations
aws rds describe-db-clusters
aws rds create-db-cluster --engine aurora-postgresql --db-cluster-identifier my-cluster
aws rds delete-db-cluster --db-cluster-identifier my-cluster --skip-final-snapshot

# Serverless v2
aws rds modify-db-cluster \
  --db-cluster-identifier my-cluster \
  --serverless-v2-scaling-configuration MinCapacity=0.5,MaxCapacity=16

# Data API
aws rds-data execute-statement \
  --resource-arn $CLUSTER_ARN \
  --secret-arn $SECRET_ARN \
  --database mydb \
  --sql "SELECT * FROM users"

# Proxy
aws rds describe-db-proxies
aws rds create-db-proxy --db-proxy-name my-proxy --engine-family POSTGRESQL ...

# Snapshots
aws rds create-db-cluster-snapshot --db-cluster-identifier my-cluster --db-cluster-snapshot-identifier backup-1
aws rds restore-db-cluster-from-snapshot --db-cluster-identifier restored --snapshot-identifier backup-1
```

---

## Anti-Patterns

- **Direct Lambda→Aurora connections** - Always use RDS Proxy or Data API
- **No connection limits** - Set `max: 1` for Lambda, use pooling for servers
- **Ignoring cold starts** - Serverless v2 needs time to scale; keep minimum ACUs for production
- **No read replicas** - Offload reads to replicas for heavy workloads
- **Missing IAM auth** - Use IAM over static passwords when possible
- **No retry logic** - Handle transient errors from scaling/failover
- **Over-provisioned capacity** - Use Serverless v2 for variable workloads
- **Skipping Secrets Manager** - Never hardcode credentials
