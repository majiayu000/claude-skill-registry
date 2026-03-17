---
name: kafka-expert
version: 1.0.0
description: Expert-level Apache Kafka, event streaming, Kafka Streams, and distributed messaging
category: data
tags: [kafka, streaming, messaging, event-driven, kafka-streams]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(kafka:*)
---

# Apache Kafka Expert

Expert guidance for Apache Kafka, event streaming, Kafka Streams, and building event-driven architectures.

## Core Concepts

- Topics, partitions, and offsets
- Producers and consumers
- Consumer groups
- Kafka Streams
- Kafka Connect
- Exactly-once semantics

## Producer

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',  # Wait for all replicas
    retries=3
)

# Send message
future = producer.send('user-events', {
    'user_id': '123',
    'event': 'login',
    'timestamp': '2024-01-01T00:00:00Z'
})

# Wait for acknowledgment
record_metadata = future.get(timeout=10)
print(f"Topic: {record_metadata.topic}, Partition: {record_metadata.partition}")

producer.flush()
producer.close()
```

## Consumer

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    group_id='my-group',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(f"Received: {message.value}")

    # Process message
    process_event(message.value)

    # Manual commit
    consumer.commit()
```

## Kafka Streams

```java
Properties props = new Properties();
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-app");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");

StreamsBuilder builder = new StreamsBuilder();

KStream<String, String> source = builder.stream("input-topic");

// Transform and filter
KStream<String, String> transformed = source
    .filter((key, value) -> value.length() > 10)
    .mapValues(value -> value.toUpperCase());

transformed.to("output-topic");

KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();
```

## Best Practices

- Use appropriate partition keys
- Monitor consumer lag
- Implement idempotent producers
- Use consumer groups for scaling
- Set proper retention policies
- Handle rebalancing gracefully
- Monitor cluster metrics

## Anti-Patterns

❌ Single partition topics
❌ No error handling
❌ Ignoring consumer lag
❌ Producing to wrong partitions
❌ Not using consumer groups
❌ Synchronous processing
❌ No monitoring

## Resources

- Apache Kafka: https://kafka.apache.org/
- Confluent Platform: https://www.confluent.io/
