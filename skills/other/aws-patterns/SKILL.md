---
name: aws-patterns
description: Lambda best practices, S3 event patterns, SQS/SNS fanout, and DynamoDB access patterns for serverless AWS architectures.
---

# AWS Patterns

Serverless and managed service patterns for AWS production workloads.

## Lambda Best Practices

```typescript
// Cold start optimization: keep handler thin, initialize outside handler
import { DynamoDBClient } from '@aws-sdk/client-dynamodb'
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb'

// Initialized ONCE per container (reused across invocations)
const client = DynamoDBDocumentClient.from(new DynamoDBClient({}))

export const handler = async (event: APIGatewayProxyEvent) => {
  try {
    const userId = event.pathParameters?.id
    if (!userId) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Missing user ID' }) }
    }

    const result = await client.send(new GetCommand({
      TableName: process.env.USERS_TABLE!,
      Key: { pk: `USER#${userId}`, sk: `PROFILE` }
    }))

    if (!result.Item) {
      return { statusCode: 404, body: JSON.stringify({ error: 'User not found' }) }
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(result.Item)
    }
  } catch (err) {
    console.error('Handler error:', err)
    return { statusCode: 500, body: JSON.stringify({ error: 'Internal server error' }) }
  }
}
```

## S3 Event Processing

```typescript
// S3 → Lambda: process uploaded files
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3'

const s3 = new S3Client({})

export const handler = async (event: S3Event) => {
  for (const record of event.Records) {
    const bucket = record.s3.bucket.name
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, ' '))
    const size = record.s3.object.size

    // Guard: skip non-image files or oversized uploads
    if (size > 10_000_000) {
      console.warn(`Skipping oversized file: ${key} (${size} bytes)`)
      continue
    }

    const response = await s3.send(new GetObjectCommand({ Bucket: bucket, Key: key }))
    const body = await response.Body!.transformToByteArray()

    await processImage(body, key)

    console.log(`Processed ${key} (${size} bytes)`)
  }
}
```

## SQS/SNS Fanout Pattern

```typescript
// SNS → multiple SQS queues (fanout to parallel consumers)

// Publisher: send to SNS topic
import { SNSClient, PublishCommand } from '@aws-sdk/client-sns'

const sns = new SNSClient({})

async function publishOrderEvent(order: Order): Promise<void> {
  await sns.send(new PublishCommand({
    TopicArn: process.env.ORDER_EVENTS_TOPIC!,
    Message: JSON.stringify(order),
    MessageAttributes: {
      eventType: { DataType: 'String', StringValue: 'order.created' },
      region: { DataType: 'String', StringValue: order.region }
    }
  }))
}

// Consumer: SQS Lambda (one per subscriber: email, analytics, inventory)
export const emailHandler = async (event: SQSEvent) => {
  for (const record of event.Records) {
    const order = JSON.parse(record.body) as Order

    try {
      await sendOrderConfirmation(order)
    } catch (err) {
      console.error(`Failed to send email for order ${order.id}:`, err)
      throw err  // Message returns to queue for retry (DLQ after maxReceiveCount)
    }
  }
}
```

## DynamoDB Single-Table Design

```typescript
// Access patterns drive table design, not entity relationships

// Table: pk (partition key) + sk (sort key) + GSI1PK + GSI1SK
// Entities: User, Order, OrderItem - all in one table

const AccessPatterns = {
  // Get user profile
  getUserProfile: (userId: string) => ({
    pk: `USER#${userId}`,
    sk: `PROFILE`
  }),

  // Get user's orders (sorted by date)
  getUserOrders: (userId: string) => ({
    pk: `USER#${userId}`,
    sk: { begins_with: 'ORDER#' }     // sk: ORDER#2025-01-15#orderId
  }),

  // Get order with items
  getOrderWithItems: (orderId: string) => ({
    pk: `ORDER#${orderId}`,
    sk: { begins_with: '' }            // sk: METADATA, ITEM#productId
  }),

  // Get orders by status (GSI1)
  getOrdersByStatus: (status: string) => ({
    GSI1PK: `STATUS#${status}`,
    GSI1SK: { begins_with: '' }        // GSI1SK: date#orderId
  })
}

// Write: transactional multi-item write
import { TransactWriteCommand } from '@aws-sdk/lib-dynamodb'

async function createOrder(order: Order): Promise<void> {
  const items = [
    // Order metadata
    {
      Put: {
        TableName: process.env.TABLE!,
        Item: {
          pk: `ORDER#${order.id}`,
          sk: 'METADATA',
          GSI1PK: `STATUS#${order.status}`,
          GSI1SK: `${order.createdAt}#${order.id}`,
          ...order
        }
      }
    },
    // User's order reference
    {
      Put: {
        TableName: process.env.TABLE!,
        Item: {
          pk: `USER#${order.userId}`,
          sk: `ORDER#${order.createdAt}#${order.id}`,
          orderId: order.id,
          total: order.total,
          status: order.status
        }
      }
    }
  ]

  await client.send(new TransactWriteCommand({ TransactItems: items }))
}
```

## Checklist

- [ ] Lambda: initialize SDK clients outside handler (reuse across invocations)
- [ ] Lambda: set memory based on profiling (more memory = more CPU = faster)
- [ ] Lambda: set timeout to 2x expected duration (not max 900s)
- [ ] SQS: configure Dead Letter Queue with maxReceiveCount: 3
- [ ] DynamoDB: design table around access patterns, not entities
- [ ] DynamoDB: use TransactWrite for multi-item atomicity
- [ ] S3: enable versioning and lifecycle rules for cost optimization
- [ ] SNS: use message attributes for subscriber filtering

## Anti-Patterns

- Initializing SDK clients inside Lambda handler (cold start penalty every time)
- Synchronous Lambda chains: A calls B calls C (use Step Functions)
- DynamoDB scan operations in production (always query with pk/sk)
- S3 event without idempotency: Lambda can be invoked multiple times per event
- Oversized Lambda packages (>50MB): use layers or container images
- Missing DLQ on SQS: failed messages silently disappear after retention period
