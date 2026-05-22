---
name: data-engineer
description: Expert in data pipelines, ETL processes, and data infrastructure
version: 1.0.0
tags: [data-engineering, etl, pipelines, databases, analytics]
---

# Data Engineer Skill

I help you build robust data pipelines, ETL processes, and data infrastructure.

## What I Do

**Data Pipelines:**

- Extract, Transform, Load (ETL) processes
- Data ingestion from multiple sources
- Batch and real-time processing
- Data quality validation

**Data Infrastructure:**

- Database schema design
- Data warehousing
- Caching strategies
- Data replication

**Analytics:**

- Data aggregation
- Metrics calculation
- Report generation
- Data export

## ETL Patterns

### Pattern 1: Simple ETL Pipeline

**Use case:** Daily sync from external API to database

```typescript
// lib/etl/daily-sync.ts

interface RawCustomer {
  id: string
  full_name: string
  email_address: string
  signup_date: string
}

interface Customer {
  id: string
  name: string
  email: string
  signupDate: Date
}

export async function syncCustomers() {
  console.log('Starting customer sync...')

  // EXTRACT: Fetch data from external API
  const response = await fetch('https://api.example.com/customers', {
    headers: {
      Authorization: `Bearer ${process.env.API_KEY}`
    }
  })

  const rawCustomers: RawCustomer[] = await response.json()
  console.log(`Extracted ${rawCustomers.length} customers`)

  // TRANSFORM: Clean and normalize data
  const transformedCustomers: Customer[] = rawCustomers.map(raw => ({
    id: raw.id,
    name: raw.full_name.trim(),
    email: raw.email_address.toLowerCase(),
    signupDate: new Date(raw.signup_date)
  }))

  // LOAD: Insert into database
  let inserted = 0
  let updated = 0

  for (const customer of transformedCustomers) {
    const existing = await db.customers.findUnique({
      where: { id: customer.id }
    })

    if (existing) {
      await db.customers.update({
        where: { id: customer.id },
        data: customer
      })
      updated++
    } else {
      await db.customers.create({
        data: customer
      })
      inserted++
    }
  }

  console.log(`Sync complete: ${inserted} inserted, ${updated} updated`)

  return { inserted, updated, total: transformedCustomers.length }
}
```

**Schedule with Vercel Cron:**

```json
// vercel.json
{
  "crons": [
    {
      "path": "/api/cron/sync-customers",
      "schedule": "0 2 * * *"
    }
  ]
}
```

```typescript
// app/api/cron/sync-customers/route.ts
import { syncCustomers } from '@/lib/etl/daily-sync'

export async function GET(req: Request) {
  const authHeader = req.headers.get('authorization')
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  try {
    const result = await syncCustomers()
    return Response.json(result)
  } catch (error) {
    console.error('Sync failed:', error)
    return Response.json({ error: 'Sync failed' }, { status: 500 })
  }
}
```

---

### Pattern 2: Incremental ETL (Delta Sync)

**Use case:** Only process new/changed records

```typescript
// lib/etl/incremental-sync.ts

export async function incrementalSync() {
  // Get last sync timestamp
  const lastSync = await db.syncLog.findFirst({
    where: { source: 'customers' },
    orderBy: { syncedAt: 'desc' }
  })

  const since = lastSync?.syncedAt || new Date('2020-01-01')

  // EXTRACT: Only fetch records modified since last sync
  const response = await fetch(
    `https://api.example.com/customers?modified_since=${since.toISOString()}`,
    {
      headers: { Authorization: `Bearer ${process.env.API_KEY}` }
    }
  )

  const newOrModified = await response.json()
  console.log(`Found ${newOrModified.length} new/modified records`)

  // TRANSFORM & LOAD
  for (const record of newOrModified) {
    await db.customers.upsert({
      where: { id: record.id },
      create: transformCustomer(record),
      update: transformCustomer(record)
    })
  }

  // Log sync
  await db.syncLog.create({
    data: {
      source: 'customers',
      recordsProcessed: newOrModified.length,
      syncedAt: new Date()
    }
  })

  return { processed: newOrModified.length }
}
```

**Benefits:**

- Faster (only process changes)
- Lower API costs
- Reduced database load

---

### Pattern 3: Real-Time Data Pipeline

**Use case:** Process events as they happen

```typescript
// lib/pipelines/events-processor.ts

import { Kafka } from 'kafkajs'

const kafka = new Kafka({
  clientId: 'myapp',
  brokers: [process.env.KAFKA_BROKER!]
})

const consumer = kafka.consumer({ groupId: 'analytics-group' })

export async function startEventProcessor() {
  await consumer.connect()
  await consumer.subscribe({ topic: 'user-events', fromBeginning: false })

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const event = JSON.parse(message.value!.toString())

      // TRANSFORM: Enrich event data
      const enrichedEvent = {
        ...event,
        processedAt: new Date(),
        userId: event.user_id,
        eventType: event.type.toLowerCase()
      }

      // LOAD: Write to analytics database
      await analyticsDb.events.create({
        data: enrichedEvent
      })

      // Also update real-time metrics
      await updateRealtimeMetrics(enrichedEvent)
    }
  })
}

async function updateRealtimeMetrics(event: any) {
  if (event.eventType === 'purchase') {
    await redis.hincrby('metrics:today', 'purchases', 1)
    await redis.hincrbyfloat('metrics:today', 'revenue', event.amount)
  }
}
```

---

## Data Transformation Patterns

### Transformation 1: Data Cleaning

```typescript
// lib/transformers/cleaners.ts

export function cleanEmail(email: string): string {
  return email.trim().toLowerCase()
}

export function cleanPhone(phone: string): string {
  // Remove all non-numeric characters
  return phone.replace(/\D/g, '')
}

export function cleanName(name: string): string {
  return name
    .trim()
    .replace(/\s+/g, ' ') // Multiple spaces → single space
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

export function parseDate(dateStr: string): Date | null {
  try {
    const date = new Date(dateStr)
    return isNaN(date.getTime()) ? null : date
  } catch {
    return null
  }
}
```

### Transformation 2: Data Enrichment

```typescript
// lib/transformers/enrichers.ts

export async function enrichCustomer(customer: RawCustomer) {
  // Add geolocation data
  const geo = await geocode(customer.address)

  // Add lifecycle stage
  const daysSinceSignup = differenceInDays(new Date(), customer.signupDate)
  const lifecycleStage =
    daysSinceSignup < 7
      ? 'new'
      : daysSinceSignup < 30
        ? 'active'
        : daysSinceSignup < 90
          ? 'engaged'
          : 'dormant'

  // Add lifetime value
  const orders = await db.orders.findMany({
    where: { customerId: customer.id }
  })
  const lifetimeValue = orders.reduce((sum, order) => sum + order.total, 0)

  return {
    ...customer,
    latitude: geo.lat,
    longitude: geo.lng,
    lifecycleStage,
    lifetimeValue,
    totalOrders: orders.length
  }
}
```

### Transformation 3: Data Aggregation

```typescript
// lib/transformers/aggregators.ts

export async function aggregateDailySales() {
  const sales = await db.$queryRaw`
    SELECT
      DATE(created_at) as date,
      COUNT(*) as order_count,
      SUM(total) as total_revenue,
      AVG(total) as average_order_value,
      COUNT(DISTINCT user_id) as unique_customers
    FROM orders
    WHERE created_at >= NOW() - INTERVAL '30 days'
    GROUP BY DATE(created_at)
    ORDER BY date DESC
  `

  return sales
}

export async function aggregateByRegion() {
  const regions = await db.$queryRaw`
    SELECT
      country,
      COUNT(*) as customer_count,
      SUM(lifetime_value) as total_revenue
    FROM customers
    GROUP BY country
    ORDER BY total_revenue DESC
  `

  return regions
}
```

---

## Data Validation

### Schema Validation with Zod

```typescript
// lib/validators/customer.ts
import { z } from 'zod'

export const customerSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150).optional(),
  signupDate: z.coerce.date(),
  tags: z.array(z.string()).default([])
})

export type ValidatedCustomer = z.infer<typeof customerSchema>

export function validateCustomer(data: unknown): ValidatedCustomer {
  return customerSchema.parse(data)
}

// In ETL pipeline
const rawData = await fetchFromAPI()
const validatedData = rawData
  .map(record => {
    try {
      return validateCustomer(record)
    } catch (error) {
      console.error(`Validation failed for record ${record.id}:`, error)
      return null
    }
  })
  .filter(Boolean)
```

### Data Quality Checks

```typescript
// lib/quality/checks.ts

export async function dataQualityChecks() {
  const checks = []

  // Check 1: No duplicate emails
  const duplicates = await db.$queryRaw`
    SELECT email, COUNT(*) as count
    FROM customers
    GROUP BY email
    HAVING COUNT(*) > 1
  `

  checks.push({
    name: 'No duplicate emails',
    passed: duplicates.length === 0,
    issues: duplicates
  })

  // Check 2: All customers have valid emails
  const invalidEmails = await db.customers.count({
    where: {
      email: {
        not: {
          contains: '@'
        }
      }
    }
  })

  checks.push({
    name: 'Valid email format',
    passed: invalidEmails === 0,
    issues: invalidEmails
  })

  // Check 3: No orphaned orders
  const orphanedOrders = await db.$queryRaw`
    SELECT COUNT(*) as count
    FROM orders
    WHERE user_id NOT IN (SELECT id FROM customers)
  `

  checks.push({
    name: 'No orphaned orders',
    passed: orphanedOrders[0].count === 0,
    issues: orphanedOrders[0].count
  })

  return checks
}
```

---

## Data Warehousing

### Star Schema Design

```prisma
// prisma/schema.prisma

// Fact table (metrics/events)
model FactSales {
  id             String   @id @default(cuid())

  // Foreign keys to dimensions
  dateId         String
  customerId     String
  productId      String
  locationId     String

  // Metrics
  quantity       Int
  unitPrice      Decimal
  totalAmount    Decimal
  discountAmount Decimal
  netAmount      Decimal

  // Relations
  date           DimDate     @relation(fields: [dateId], references: [id])
  customer       DimCustomer @relation(fields: [customerId], references: [id])
  product        DimProduct  @relation(fields: [productId], references: [id])
  location       DimLocation @relation(fields: [locationId], references: [id])
}

// Dimension tables
model DimDate {
  id         String   @id
  date       DateTime
  year       Int
  quarter    Int
  month      Int
  dayOfWeek  Int
  isWeekend  Boolean
  isHoliday  Boolean

  sales      FactSales[]
}

model DimCustomer {
  id             String   @id
  name           String
  email          String
  segment        String  // 'enterprise', 'smb', 'consumer'
  lifecycleStage String

  sales          FactSales[]
}

model DimProduct {
  id       String   @id
  name     String
  category String
  brand    String
  sku      String

  sales    FactSales[]
}

model DimLocation {
  id      String   @id
  country String
  state   String
  city    String
  zipCode String

  sales   FactSales[]
}
```

### Populate Data Warehouse

```typescript
// lib/warehouse/populate.ts

export async function populateWarehouse() {
  // Extract from operational database
  const orders = await db.orders.findMany({
    include: {
      customer: true,
      items: {
        include: { product: true }
      }
    },
    where: {
      createdAt: {
        gte: new Date(Date.now() - 24 * 60 * 60 * 1000) // Last 24 hours
      }
    }
  })

  for (const order of orders) {
    // Transform into fact table format
    for (const item of order.items) {
      await warehouseDb.factSales.create({
        data: {
          dateId: formatDateId(order.createdAt),
          customerId: order.customer.id,
          productId: item.product.id,
          locationId: order.customer.locationId,
          quantity: item.quantity,
          unitPrice: item.price,
          totalAmount: item.quantity * item.price,
          discountAmount: item.discount || 0,
          netAmount: item.quantity * item.price - (item.discount || 0)
        }
      })
    }
  }
}

function formatDateId(date: Date): string {
  return date.toISOString().split('T')[0] // "2025-10-22"
}
```

---

## Performance Optimization

### Batch Processing

```typescript
// lib/etl/batch-processor.ts

export async function processBatch<T>(
  items: T[],
  processor: (item: T) => Promise<void>,
  batchSize = 100
) {
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize)

    // Process batch in parallel
    await Promise.all(batch.map(processor))

    console.log(`Processed ${Math.min(i + batchSize, items.length)}/${items.length}`)

    // Small delay to avoid overwhelming database
    await new Promise(resolve => setTimeout(resolve, 100))
  }
}

// Usage
await processBatch(
  customers,
  async customer => {
    await db.customers.upsert({
      where: { id: customer.id },
      create: customer,
      update: customer
    })
  },
  100 // Process 100 at a time
)
```

### Database Optimization

```typescript
// lib/db/optimizations.ts

// Use raw SQL for complex aggregations
export async function efficientAggregation() {
  // Instead of multiple queries
  const result = await db.$queryRaw`
    SELECT
      c.segment,
      COUNT(DISTINCT c.id) as customer_count,
      COUNT(o.id) as order_count,
      SUM(o.total) as total_revenue,
      AVG(o.total) as avg_order_value
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id
    GROUP BY c.segment
  `

  return result
}

// Use indexes for faster queries
// In migration file:
await db.$executeRaw`
  CREATE INDEX idx_orders_created_at ON orders(created_at);
  CREATE INDEX idx_orders_customer_id ON orders(customer_id);
  CREATE INDEX idx_customers_email ON customers(email);
`
```

---

## Caching Strategies

### Redis for Aggregated Data

```typescript
// lib/cache/metrics.ts
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL!)

export async function getCachedMetrics(key: string) {
  const cached = await redis.get(key)

  if (cached) {
    return JSON.parse(cached)
  }

  // Calculate metrics
  const metrics = await calculateMetrics()

  // Cache for 1 hour
  await redis.setex(key, 3600, JSON.stringify(metrics))

  return metrics
}

async function calculateMetrics() {
  const [revenue, orders, customers] = await Promise.all([
    db.orders.aggregate({ _sum: { total: true } }),
    db.orders.count(),
    db.customers.count()
  ])

  return {
    totalRevenue: revenue._sum.total || 0,
    totalOrders: orders,
    totalCustomers: customers,
    avgOrderValue: (revenue._sum.total || 0) / orders
  }
}
```

---

## Monitoring and Logging

### Pipeline Monitoring

```typescript
// lib/monitoring/pipeline.ts

interface PipelineRun {
  pipelineName: string
  startTime: Date
  endTime?: Date
  status: 'running' | 'success' | 'failed'
  recordsProcessed: number
  errorMessage?: string
}

export async function trackPipeline<T>(name: string, pipeline: () => Promise<T>): Promise<T> {
  const run: PipelineRun = {
    pipelineName: name,
    startTime: new Date(),
    status: 'running',
    recordsProcessed: 0
  }

  // Log start
  await db.pipelineRuns.create({ data: run })

  try {
    const result = await pipeline()

    // Log success
    run.endTime = new Date()
    run.status = 'success'
    await db.pipelineRuns.update({
      where: { id: run.id },
      data: run
    })

    return result
  } catch (error) {
    // Log failure
    run.endTime = new Date()
    run.status = 'failed'
    run.errorMessage = error.message

    await db.pipelineRuns.update({
      where: { id: run.id },
      data: run
    })

    // Alert team
    await sendAlert({
      channel: '#data-engineering',
      message: `Pipeline ${name} failed: ${error.message}`
    })

    throw error
  }
}

// Usage
await trackPipeline('daily-customer-sync', async () => {
  return await syncCustomers()
})
```

---

## Common Patterns

### Pattern: Upsert with Conflict Resolution

```typescript
export async function upsertWithConflict(record: any) {
  const existing = await db.customers.findUnique({
    where: { id: record.id }
  })

  if (existing) {
    // Conflict resolution: Use most recent data
    if (record.updatedAt > existing.updatedAt) {
      await db.customers.update({
        where: { id: record.id },
        data: record
      })
      return { action: 'updated' }
    } else {
      return { action: 'skipped', reason: 'stale data' }
    }
  } else {
    await db.customers.create({ data: record })
    return { action: 'created' }
  }
}
```

### Pattern: Dead Letter Queue

```typescript
// lib/queue/dead-letter.ts

export async function processWithRetry<T>(
  item: T,
  processor: (item: T) => Promise<void>,
  maxRetries = 3
) {
  let attempt = 0

  while (attempt < maxRetries) {
    try {
      await processor(item)
      return { success: true }
    } catch (error) {
      attempt++
      console.error(`Attempt ${attempt} failed:`, error)

      if (attempt >= maxRetries) {
        // Move to dead letter queue
        await db.deadLetterQueue.create({
          data: {
            item: JSON.stringify(item),
            error: error.message,
            attempts: attempt,
            queuedAt: new Date()
          }
        })

        return { success: false, deadLettered: true }
      }

      // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, attempt)))
    }
  }
}
```

---

## When to Use Me

**Perfect for:**

- Building ETL pipelines
- Data migration projects
- Analytics infrastructure
- Data quality improvement
- Real-time data processing

**I'll help you:**

- Design data pipelines
- Transform and clean data
- Build data warehouses
- Optimize database queries
- Monitor data quality

## What I'll Create

```
🔄 ETL Pipelines
📊 Data Transformations
🏛️ Data Warehouses
✅ Data Quality Checks
⚡ Real-Time Processors
📈 Analytics Infrastructure
```

Let's build robust, scalable data infrastructure!
