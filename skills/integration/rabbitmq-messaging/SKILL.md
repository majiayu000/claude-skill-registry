---
name: rabbitmq-messaging
description: RabbitMQ Streams and AMQP messaging patterns for the crypto-scout ecosystem
license: MIT
compatibility: opencode
metadata:
  messaging: rabbitmq
  protocols: streams,amqp
  version: "4.1.4"
---

## What I Do

Provide guidance for RabbitMQ Streams and AMQP messaging patterns used in the crypto-scout ecosystem for real-time data flow.

## Messaging Architecture

### Topology Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    crypto-scout-exchange                     │
│                        (direct type)                         │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
      ┌────────┴────────┐            ┌────────┴────────┐
      │   bybit-stream  │            │crypto-scout-stream
      │    (Stream)     │            │    (Stream)     │
      └────────┬────────┘            └────────┬────────┘
               │                              │
               │  Payload<Map<String,Object>> │
               │                              │
      ┌────────┴────────┐            ┌────────┴────────┐
      │ crypto-scout    │            │ crypto-scout    │
      │   -client       │            │   -collector    │
      │  (Publisher)    │            │  (Consumer)     │
      └─────────────────┘            └─────────────────┘
```

### Queues
| Queue | Purpose | Arguments |
|-------|---------|-----------|
| `collector-queue` | Command/control messages | lazy mode, TTL 6h, max 2500 |
| `chatbot-queue` | Chatbot notifications | lazy mode, TTL 6h, max 2500 |
| `dlx-queue` | Dead letter handling | lazy mode, TTL 7d |

### Streams
| Stream | Purpose | Retention |
|--------|---------|-----------|
| `bybit-stream` | Bybit market data | 1 day, 2GB max |
| `crypto-scout-stream` | CMC/parser data | 1 day, 2GB max |

## Streams Protocol (Port 5552)

### Publisher Implementation
```java
public final class AmqpPublisher extends AbstractReactive implements ReactiveService {
    private volatile Environment environment;
    private volatile Producer bybitStream;
    private volatile Producer cryptoScoutStream;
    
    @Override
    public Promise<Void> start() {
        return Promise.ofBlocking(executor, () -> {
            environment = Environment.builder()
                .host("crypto-scout-mq")
                .port(5552)
                .username("crypto_scout_mq")
                .password("password")
                .build();
            
            bybitStream = environment.producerBuilder()
                .name("bybit-stream")
                .stream("bybit-stream")
                .build();
            
            cryptoScoutStream = environment.producerBuilder()
                .name("crypto-scout-stream")
                .stream("crypto-scout-stream")
                .build();
        });
    }
    
    public Promise<Void> publish(final Payload<Map<String, Object>> payload) {
        final var producer = getProducer(payload.getProvider());
        final var settablePromise = new SettablePromise<Void>();
        
        final var message = producer.messageBuilder()
            .addData(JsonUtils.object2Bytes(payload))
            .build();
        
        producer.send(message, status -> {
            if (status.isConfirmed()) {
                settablePromise.set(null);
            } else {
                settablePromise.setException(
                    new IllegalStateException("Publish not confirmed: " + status)
                );
            }
        });
        
        return settablePromise;
    }
}
```

### Consumer Implementation with Offset Management
```java
public final class StreamService extends AbstractReactive implements ReactiveService {
    private volatile Environment environment;
    private volatile Consumer consumer;
    
    @Override
    public Promise<Void> start() {
        return Promise.ofBlocking(executor, () -> {
            environment = AmqpConfig.getEnvironment();
            
            consumer = environment.consumerBuilder()
                .stream("bybit-stream")
                .noTrackingStrategy()
                .subscriptionListener(this::updateOffset)
                .messageHandler(this::handleMessage)
                .build();
        });
    }
    
    private void updateOffset(final SubscriptionContext context) {
        final var savedOffset = offsetRepository.getOffset("bybit-stream");
        if (savedOffset.isPresent()) {
            context.offsetSpecification(
                OffsetSpecification.offset(savedOffset.getAsLong() + 1)
            );
        } else {
            context.offsetSpecification(OffsetSpecification.first());
        }
    }
    
    private void handleMessage(final Context context, final Message message) {
        final var payload = JsonUtils.bytes2Object(
            message.getBodyAsBinary(), 
            Payload.class
        );
        // Process and save with offset
        service.save(payload, context.offset());
    }
}
```

## AMQP Protocol (Port 5672)

### Consumer Implementation
```java
public final class AmqpConsumer extends AbstractReactive implements ReactiveService {
    private volatile Connection connection;
    private volatile Channel channel;
    
    @Override
    public Promise<Void> start() {
        return Promise.ofBlocking(executor, () -> {
            final var factory = new ConnectionFactory();
            factory.setHost("crypto-scout-mq");
            factory.setPort(5672);
            factory.setUsername("crypto_scout_mq");
            factory.setPassword("password");
            
            connection = factory.newConnection();
            channel = connection.createChannel();
            
            channel.basicQos(1);  // Fair dispatch
            
            final var consumer = new DefaultConsumer(channel) {
                @Override
                public void handleDelivery(
                    String consumerTag, 
                    Envelope envelope,
                    AMQP.BasicProperties properties, 
                    byte[] body
                ) throws IOException {
                    try {
                        final var message = JsonUtils.bytes2Object(body, Map.class);
                        messageHandler.accept(message);
                        channel.basicAck(envelope.getDeliveryTag(), false);
                    } catch (Exception e) {
                        channel.basicNack(envelope.getDeliveryTag(), false, true);
                    }
                }
            };
            
            channel.basicConsume("collector-queue", false, consumer);
        });
    }
}
```

### Publisher Implementation
```java
public final class AmqpPublisher extends AbstractReactive implements ReactiveService {
    private volatile Connection connection;
    private volatile Channel channel;
    
    public Promise<Void> publish(final Map<String, Object> message, 
                                  final String routingKey) {
        return Promise.ofBlocking(executor, () -> {
            final var bytes = JsonUtils.object2Bytes(message);
            final var props = new AMQP.BasicProperties.Builder()
                .contentType("application/json")
                .deliveryMode(2)  // Persistent
                .build();
            
            channel.basicPublish(
                "crypto-scout-exchange",
                routingKey,
                props,
                bytes
            );
        });
    }
}
```

## Payload Structure

### Standard Payload Format
```java
public class Payload<T> {
    private final Provider provider;  // CMC, BYBIT
    private final Source source;      // PMST, PML, API
    private final Event event;        // TICKERS, KLINE, TRADE
    private final long timestamp;
    private final String symbol;      // BTCUSDT, ETHUSDT
    private final T data;
}

// Example JSON
{
    "provider": "BYBIT",
    "source": "PMST",
    "event": "TICKERS",
    "timestamp": 1704067200000,
    "symbol": "BTCUSDT",
    "data": {
        "lastPrice": "42000.50",
        "highPrice24h": "43500.00",
        "lowPrice24h": "41000.00"
    }
}
```

## Configuration

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `AMQP_RABBITMQ_HOST` | `localhost` | RabbitMQ host |
| `AMQP_RABBITMQ_PORT` | `5672` | AMQP port |
| `AMQP_STREAM_PORT` | `5552` | Streams port |
| `AMQP_RABBITMQ_USERNAME` | `crypto_scout_mq` | Username |
| `AMQP_RABBITMQ_PASSWORD` | - | Password |
| `AMQP_BYBIT_STREAM` | `bybit-stream` | Bybit stream name |
| `AMQP_CRYPTO_SCOUT_STREAM` | `crypto-scout-stream` | CMC stream name |

### Stream Retention Policy
```json
{
    "vhost": "/",
    "name": "stream-retention",
    "pattern": ".*-stream$",
    "definition": {
        "max-length-bytes": 2000000000,
        "max-age": "1D",
        "stream-max-segment-size-bytes": 100000000
    }
}
```

## Error Handling

### Connection Recovery
```java
private Promise<Void> startWithRetry() {
    return Promise.ofBlocking(executor, () -> {
        int attempts = 0;
        while (attempts < MAX_RETRIES) {
            try {
                connect();
                return;
            } catch (Exception e) {
                attempts++;
                if (attempts >= MAX_RETRIES) {
                    throw new IllegalStateException("Failed to connect after retries", e);
                }
                Thread.sleep(RETRY_DELAY_MS * attempts);
            }
        }
    });
}
```

### Publisher Confirm Timeout
```java
producer.send(message, status -> {
    reactor.scheduleAfter(Duration.ofSeconds(30), () -> {
        if (!settablePromise.isComplete()) {
            settablePromise.setException(
                new IllegalStateException("Publish confirmation timeout")
            );
        }
    });
    
    if (status.isConfirmed()) {
        settablePromise.set(null);
    } else {
        settablePromise.setException(
            new IllegalStateException("Publish not confirmed: " + status)
        );
    }
});
```

## Monitoring

### Health Checks
```java
public boolean isReady() {
    return environment != null && 
           bybitStream != null && 
           cryptoScoutStream != null;
}

// HTTP endpoint
curl http://localhost:8081/health
# Returns: ok (200) or not-ready (503)
```

### Management UI
- URL: http://localhost:15672
- Monitor streams, queues, connections
- View message rates and consumer counts

## When to Use Me

Use this skill when:
- Implementing RabbitMQ Streams publishers or consumers
- Configuring AMQP queues and exchanges
- Managing stream offsets for exactly-once processing
- Handling connection failures and retries
- Designing message payload structures
- Setting up stream retention policies
- Monitoring messaging health
