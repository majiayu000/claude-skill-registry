---
name: message-queues
description: Message queue patterns with RabbitMQ, Redis Streams, and Kafka. Use when implementing async communication, pub/sub systems, event-driven microservices, or reliable message delivery.
context: fork
agent: event-driven-architect
version: 2.0.0
tags: [message-queue, rabbitmq, redis-streams, kafka, faststream, pub-sub, async, event-driven, 2026]
allowed-tools: [Read, Write, Bash, Grep, Glob]
author: SkillForge
user-invocable: false
---

# Message Queue Patterns (2026)

Asynchronous communication patterns for distributed systems using RabbitMQ, Redis Streams, Kafka, and FastStream.

## Overview

- Decoupling services in microservices architecture
- Implementing pub/sub and work queue patterns
- Building event-driven systems with reliable delivery
- Load leveling and buffering between services
- Task distribution across multiple workers
- High-throughput event streaming (Kafka)

## Quick Reference

### FastStream: Unified API (2026 Recommended)

```python
# pip install faststream[kafka,rabbit,redis]
from faststream import FastStream
from faststream.kafka import KafkaBroker
from pydantic import BaseModel

broker = KafkaBroker("localhost:9092")
app = FastStream(broker)

class OrderCreated(BaseModel):
    order_id: str
    customer_id: str
    total: float

@broker.subscriber("orders.created")
async def handle_order(event: OrderCreated):
    """Automatic Pydantic validation and deserialization."""
    print(f"Processing order {event.order_id}")
    await process_order(event)

@broker.publisher("orders.processed")
async def publish_processed(order_id: str) -> dict:
    return {"order_id": order_id, "status": "processed"}

# Run with: faststream run app:app
```

### Kafka Producer (aiokafka)

```python
from aiokafka import AIOKafkaProducer
import json

class KafkaPublisher:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self._producer: AIOKafkaProducer | None = None

    async def start(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode(),
            acks="all",  # Wait for all replicas
            enable_idempotence=True,  # Exactly-once semantics
        )
        await self._producer.start()

    async def publish(
        self,
        topic: str,
        value: dict,
        key: str | None = None,
    ):
        await self._producer.send_and_wait(
            topic,
            value=value,
            key=key.encode() if key else None,
        )

    async def stop(self):
        await self._producer.stop()
```

### Kafka Consumer with Consumer Group

```python
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import OffsetOutOfRangeError

class KafkaConsumer:
    def __init__(
        self,
        topic: str,
        group_id: str,
        bootstrap_servers: str,
    ):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=False,  # Manual commit for reliability
            value_deserializer=lambda v: json.loads(v.decode()),
        )

    async def consume(self, handler):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                try:
                    await handler(msg.value, msg.key, msg.partition)
                    await self.consumer.commit()
                except Exception as e:
                    # Handle or send to DLQ
                    await self.send_to_dlq(msg, e)
        finally:
            await self.consumer.stop()
```

### RabbitMQ Publisher

```python
import aio_pika
from aio_pika import Message, DeliveryMode

class RabbitMQPublisher:
    def __init__(self, url: str):
        self.url = url
        self._connection = None
        self._channel = None

    async def connect(self):
        self._connection = await aio_pika.connect_robust(self.url)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=10)

    async def publish(self, exchange: str, routing_key: str, message: dict):
        exchange_obj = await self._channel.get_exchange(exchange)
        await exchange_obj.publish(
            Message(
                body=json.dumps(message).encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
                content_type="application/json"
            ),
            routing_key=routing_key
        )
```

### RabbitMQ Consumer with Retry

```python
class RabbitMQConsumer:
    async def consume(self, queue_name: str, handler, max_retries: int = 3):
        queue = await self._channel.get_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(requeue=False):
                    try:
                        body = json.loads(message.body.decode())
                        await handler(body)
                    except Exception as e:
                        retry_count = message.headers.get("x-retry-count", 0)
                        if retry_count < max_retries:
                            await self.publish(exchange, routing_key, body,
                                headers={"x-retry-count": retry_count + 1})
                        else:
                            await self.publish("dlx", "failed", body,
                                headers={"x-error": str(e)})
```

### Redis Streams Consumer Group

```python
import redis.asyncio as redis

class RedisStreamConsumer:
    def __init__(self, url: str, stream: str, group: str, consumer: str):
        self.redis = redis.from_url(url)
        self.stream, self.group, self.consumer = stream, group, consumer

    async def setup(self):
        try:
            await self.redis.xgroup_create(self.stream, self.group, "0", mkstream=True)
        except redis.ResponseError as e:
            if "BUSYGROUP" not in str(e): raise

    async def consume(self, handler):
        while True:
            messages = await self.redis.xreadgroup(
                groupname=self.group, consumername=self.consumer,
                streams={self.stream: ">"}, count=10, block=5000
            )
            for stream, stream_messages in messages:
                for message_id, data in stream_messages:
                    try:
                        await handler(message_id, data)
                        await self.redis.xack(self.stream, self.group, message_id)
                    except Exception:
                        pass  # Message redelivered on restart
```

### "Just Use Postgres" Pattern

```python
# For simpler use cases - Postgres LISTEN/NOTIFY + FOR UPDATE SKIP LOCKED
from sqlalchemy import text

class PostgresQueue:
    """Simple queue using Postgres - good for moderate throughput."""

    async def publish(self, db: AsyncSession, channel: str, payload: dict):
        await db.execute(
            text("SELECT pg_notify(:channel, :payload)"),
            {"channel": channel, "payload": json.dumps(payload)}
        )

    async def get_next_job(self, db: AsyncSession) -> dict | None:
        """Get next job with advisory lock."""
        result = await db.execute(text("""
            SELECT id, payload FROM job_queue
            WHERE status = 'pending'
            ORDER BY created_at
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        """))
        return result.first()
```

## Key Decisions

| Technology | Best For | Throughput | Ordering | Persistence |
|------------|----------|------------|----------|-------------|
| **Kafka** | Event streaming, logs, high-volume | 100K+ msg/s | Partition-level | Excellent |
| **RabbitMQ** | Task queues, RPC, routing | ~50K msg/s | Queue-level | Good |
| **Redis Streams** | Real-time, simple streaming | ~100K msg/s | Stream-level | Good (AOF) |
| **Postgres** | Moderate volume, simplicity | ~10K msg/s | Query-defined | Excellent |

### When to Choose Each

```
┌────────────────────────────────────────────────────────────────────────┐
│                     DECISION FLOWCHART                                  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Need > 50K msg/s?                                                     │
│      YES → Kafka (partitioned, replicated)                             │
│      NO ↓                                                              │
│                                                                         │
│  Need complex routing (topic, headers)?                                │
│      YES → RabbitMQ (exchanges, bindings)                              │
│      NO ↓                                                              │
│                                                                         │
│  Need real-time + simple?                                              │
│      YES → Redis Streams (XREAD, consumer groups)                      │
│      NO ↓                                                              │
│                                                                         │
│  Already using Postgres + < 10K msg/s?                                 │
│      YES → Postgres (LISTEN/NOTIFY + FOR UPDATE SKIP LOCKED)           │
│      NO → Re-evaluate requirements                                     │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

## Anti-Patterns (FORBIDDEN)

```python
# NEVER process without acknowledgment
async for msg in consumer:
    process(msg)  # Message lost on failure!

# NEVER use sync calls in handlers
def handle(msg):
    requests.post(url, data=msg)  # Blocks event loop!

# NEVER ignore ordering when required
await publish("orders", {"order_id": "123"})  # No partition key!

# NEVER store large payloads
await publish("files", {"content": large_bytes})  # Use URL reference!

# NEVER skip dead letter handling
except Exception:
    pass  # Failed messages vanish!

# NEVER choose Kafka for simple task queue
# RabbitMQ or Redis is simpler for work distribution

# NEVER use Redis Streams when strict delivery matters
# Use RabbitMQ or Kafka for guaranteed delivery
```

## Related Skills

- `outbox-pattern` - Transactional outbox for reliable publishing
- `background-jobs` - Celery/ARQ task processing
- `streaming-api-patterns` - SSE/WebSocket real-time
- `observability-monitoring` - Queue metrics and alerting
- `event-sourcing` - Event store and CQRS patterns

## Capability Details

### kafka-streaming
**Keywords:** kafka, aiokafka, partition, consumer group, exactly-once, offset
**Solves:**
- How do I set up Kafka producers/consumers?
- Partition key selection for ordering
- Exactly-once semantics with idempotence
- Consumer group rebalancing

### rabbitmq-messaging
**Keywords:** rabbitmq, amqp, aio-pika, exchange, queue, topic, fanout, routing
**Solves:**
- How do I set up RabbitMQ pub/sub?
- Exchange types and queue binding
- Dead letter queue configuration
- Message persistence and acknowledgment

### redis-streams
**Keywords:** redis streams, xadd, xread, xreadgroup, consumer group, xack
**Solves:**
- How do I use Redis Streams?
- Consumer group setup and message claiming
- Stream trimming and retention
- At-least-once delivery patterns

### faststream-framework
**Keywords:** faststream, unified api, pydantic, asyncapi, broker
**Solves:**
- Unified API for Kafka/RabbitMQ/Redis
- Automatic Pydantic serialization
- AsyncAPI documentation generation
- Dependency injection for handlers

### postgres-queue
**Keywords:** postgres queue, listen notify, skip locked, simple queue
**Solves:**
- When to use Postgres instead of dedicated queue
- LISTEN/NOTIFY for pub/sub
- FOR UPDATE SKIP LOCKED for job queue
