---
name: kafka-patterns
description: Topic design, partition strategies, consumer group patterns, exactly-once processing, and dead letter queue handling.
---

# Kafka Patterns

Event streaming patterns for Apache Kafka in distributed systems.

## Topic Design

```yaml
# Topic naming convention: <domain>.<entity>.<event-type>
# Examples:
#   orders.order.created
#   payments.payment.completed
#   inventory.stock.updated

# Topic configuration
topics:
  orders.order.created:
    partitions: 12          # Match expected consumer parallelism
    replication-factor: 3   # Survive 2 broker failures
    retention.ms: 604800000 # 7 days
    cleanup.policy: delete

  orders.order.changelog:
    partitions: 12
    replication-factor: 3
    retention.ms: -1        # Infinite retention (compacted)
    cleanup.policy: compact # Keep latest value per key
    min.compaction.lag.ms: 3600000  # 1h before compacting
```

## Producer Patterns

```typescript
import { Kafka, Partitioners, CompressionTypes } from 'kafkajs'

const kafka = new Kafka({
  clientId: 'order-service',
  brokers: process.env.KAFKA_BROKERS!.split(','),
})

const producer = kafka.producer({
  idempotent: true,                                    // Exactly-once producer
  maxInFlightRequests: 5,                              // Max parallel requests
  createPartitioner: Partitioners.DefaultPartitioner,
})

await producer.connect()

// Key-based partitioning: same key always goes to same partition (ordering)
async function publishOrderEvent(order: Order, eventType: string): Promise<void> {
  await producer.send({
    topic: `orders.order.${eventType}`,
    compression: CompressionTypes.LZ4,
    messages: [{
      key: order.id,                    // Orders for same ID → same partition → ordered
      value: JSON.stringify({
        eventId: crypto.randomUUID(),   // Idempotency key
        eventType,
        timestamp: new Date().toISOString(),
        data: order,
      }),
      headers: {
        'content-type': 'application/json',
        'source': 'order-service',
        'correlation-id': order.correlationId,
      },
    }],
  })
}

// Batch publishing for throughput
async function publishBatch(events: OrderEvent[]): Promise<void> {
  await producer.sendBatch({
    topicMessages: [{
      topic: 'orders.order.created',
      messages: events.map(e => ({
        key: e.orderId,
        value: JSON.stringify(e),
      })),
    }],
  })
}
```

## Consumer Group Patterns

```typescript
const consumer = kafka.consumer({
  groupId: 'payment-processor',     // Consumer group: shared topic consumption
  sessionTimeout: 30000,
  heartbeatInterval: 3000,
  maxBytesPerPartition: 1048576,    // 1MB per partition per fetch
  retry: { retries: 5 },
})

await consumer.connect()
await consumer.subscribe({
  topics: ['orders.order.created'],
  fromBeginning: false,              // Start from latest offset
})

await consumer.run({
  autoCommit: false,                 // Manual commit for exactly-once
  eachBatchAutoResolve: false,

  eachBatch: async ({ batch, resolveOffset, commitOffsetsIfNecessary, heartbeat }) => {
    for (const message of batch.messages) {
      try {
        const event = JSON.parse(message.value!.toString())

        // Idempotency check: skip already processed events
        if (await isAlreadyProcessed(event.eventId)) {
          resolveOffset(message.offset)
          continue
        }

        await processOrderPayment(event.data)
        await markAsProcessed(event.eventId)

        resolveOffset(message.offset)
        await commitOffsetsIfNecessary()
        await heartbeat()
      } catch (err) {
        console.error(`Failed to process message at offset ${message.offset}:`, err)
        // Send to DLQ instead of blocking the partition
        await sendToDeadLetterQueue(message, err as Error)
        resolveOffset(message.offset)
      }
    }
  },
})
```

## Dead Letter Queue (DLQ)

```typescript
const DLQ_TOPIC = 'orders.order.created.dlq'

async function sendToDeadLetterQueue(
  originalMessage: KafkaMessage,
  error: Error
): Promise<void> {
  await producer.send({
    topic: DLQ_TOPIC,
    messages: [{
      key: originalMessage.key,
      value: originalMessage.value,
      headers: {
        ...originalMessage.headers,
        'dlq-reason': error.message,
        'dlq-timestamp': new Date().toISOString(),
        'dlq-original-topic': 'orders.order.created',
        'dlq-retry-count': '0',
      },
    }],
  })
}

// DLQ consumer: retry or alert
async function processDLQ(): Promise<void> {
  const dlqConsumer = kafka.consumer({ groupId: 'dlq-processor' })
  await dlqConsumer.subscribe({ topics: [DLQ_TOPIC] })

  await dlqConsumer.run({
    eachMessage: async ({ message }) => {
      const retryCount = parseInt(
        message.headers?.['dlq-retry-count']?.toString() ?? '0'
      )

      if (retryCount >= 3) {
        // Max retries exceeded: alert ops team
        await alertOps({
          topic: DLQ_TOPIC,
          key: message.key?.toString(),
          reason: message.headers?.['dlq-reason']?.toString(),
          retries: retryCount,
        })
        return
      }

      // Retry with incremented count
      try {
        const event = JSON.parse(message.value!.toString())
        await processOrderPayment(event.data)
      } catch (err) {
        // Re-enqueue with incremented retry count
        await producer.send({
          topic: DLQ_TOPIC,
          messages: [{
            key: message.key,
            value: message.value,
            headers: {
              ...message.headers,
              'dlq-retry-count': String(retryCount + 1),
            },
          }],
        })
      }
    },
  })
}
```

## Partition Strategy

```typescript
// Custom partitioner: route by region for data locality
const regionalPartitioner = () => ({
  partition: ({ topic, partitionMetadata, message }) => {
    const region = message.headers?.['region']?.toString() ?? 'default'
    const regionMap: Record<string, number> = {
      'us-east': 0, 'us-west': 1,
      'eu-west': 2, 'eu-east': 3,
      'ap-southeast': 4,
    }
    const partition = regionMap[region]
    if (partition !== undefined && partition < partitionMetadata.length) {
      return partition
    }
    // Fallback: hash the key
    const numPartitions = partitionMetadata.length
    const hash = murmurHash(message.key?.toString() ?? '')
    return Math.abs(hash) % numPartitions
  }
})
```

## Checklist

- [ ] Idempotent producer enabled (exactly-once semantics)
- [ ] Key-based partitioning for ordered processing per entity
- [ ] Manual offset commit (not auto-commit) for at-least-once guarantee
- [ ] Dead Letter Queue for failed messages (max 3 retries then alert)
- [ ] Consumer idempotency check before processing (eventId dedup)
- [ ] Heartbeat during long-running batch processing
- [ ] Replication factor >= 3 for production topics
- [ ] Monitoring: consumer lag, throughput, error rate per consumer group

## Anti-Patterns

- Auto-commit offsets: message loss if consumer crashes before processing
- Single partition topics: no parallelism, bottleneck
- Unbounded retry: infinite retry loop blocks partition processing
- Large messages (>1MB): use claim-check pattern (store in S3, send reference)
- Skipping idempotency: duplicate processing on consumer restart
- Global ordering requirement: use single partition only when truly needed
