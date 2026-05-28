---
name: messaging
description: Message queues and event-driven backend architecture. RabbitMQ, Kafka, pub/sub patterns, and async communication.
sasmp_version: "2.0.0"
bonded_agent: 04-architecture-patterns
bond_type: SECONDARY_BOND

# === PRODUCTION-GRADE SKILL CONFIG (SASMP v2.0.0) ===

atomic_operations:
  - QUEUE_SETUP
  - EVENT_PUBLISHING
  - CONSUMER_CONFIGURATION
  - DLQ_HANDLING

parameter_validation:
  query:
    type: string
    required: true
    minLength: 5
    maxLength: 2000
  broker:
    type: string
    enum: [rabbitmq, kafka, redis, sqs]
    required: false

retry_logic:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 1000

logging_hooks:
  on_invoke: "skill.messaging.invoked"
  on_success: "skill.messaging.completed"
  on_error: "skill.messaging.failed"

exit_codes:
  SUCCESS: 0
  INVALID_INPUT: 1
  CONNECTION_ERROR: 2
---

# Messaging & Event-Driven Skill

**Bonded to:** `architecture-patterns-agent` (Secondary)

---

## Quick Start

```bash
# Invoke messaging skill
"Set up RabbitMQ for my microservices"
"Implement event-driven order processing"
"Configure Kafka for high-throughput messaging"
```

---

## Message Broker Comparison

| Broker | Best For | Throughput | Ordering |
|--------|----------|------------|----------|
| RabbitMQ | Task queues, RPC | Medium | Per queue |
| Kafka | Event streaming, logs | Very high | Per partition |
| Redis Pub/Sub | Real-time, simple | High | None |
| SQS | AWS serverless | Medium | FIFO optional |

---

## Examples

### RabbitMQ Producer/Consumer
```python
import pika
import json

# Producer
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='orders', durable=True)

def publish_order(order):
    channel.basic_publish(
        exchange='',
        routing_key='orders',
        body=json.dumps(order),
        properties=pika.BasicProperties(delivery_mode=2)  # persistent
    )

# Consumer
def process_order(ch, method, properties, body):
    order = json.loads(body)
    print(f"Processing order: {order['id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='orders', on_message_callback=process_order)
channel.start_consuming()
```

### Kafka Event Streaming
```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send('user-events', {'type': 'USER_CREATED', 'user_id': '123'})

# Consumer
consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    group_id='notification-service',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(f"Event: {message.value}")
```

---

## Patterns

### Dead Letter Queue (DLQ)
```python
def process_with_retry(message, max_retries=3):
    retry_count = message.headers.get('x-retry-count', 0)

    try:
        process(message)
    except Exception as e:
        if retry_count < max_retries:
            # Republish with incremented retry count
            republish_with_delay(message, retry_count + 1)
        else:
            # Send to DLQ
            publish_to_dlq(message, str(e))
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Message loss | No persistence | Enable durable queues |
| Consumer lag | Slow processing | Scale consumers, batch processing |
| Duplicate processing | No idempotency | Implement idempotent consumers |

---

## Resources

- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
