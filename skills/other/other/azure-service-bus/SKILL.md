---
name: azure-service-bus
description: Enterprise messaging with Azure Service Bus. Configure queues, topics, subscriptions, and message processing. Use for async communication, event-driven architectures, and reliable message delivery on Azure.
---

# Azure Service Bus Skill

Build reliable messaging solutions with Azure Service Bus for enterprise integration.

## Triggers

Use this skill when you see:
- azure service bus, service bus, message queue
- service bus queue, service bus topic
- message subscription, dead letter queue
- message session, message broker

## Instructions

### Create Service Bus Resources

```bash
# Create namespace
az servicebus namespace create \
    --name myservicebus \
    --resource-group mygroup \
    --location eastus \
    --sku Premium

# Create queue
az servicebus queue create \
    --name myqueue \
    --namespace-name myservicebus \
    --resource-group mygroup \
    --max-size 5120 \
    --default-message-time-to-live P14D \
    --lock-duration PT1M \
    --enable-dead-lettering-on-message-expiration true

# Create topic
az servicebus topic create \
    --name mytopic \
    --namespace-name myservicebus \
    --resource-group mygroup \
    --max-size 5120 \
    --default-message-time-to-live P14D

# Create subscription
az servicebus topic subscription create \
    --name mysubscription \
    --topic-name mytopic \
    --namespace-name myservicebus \
    --resource-group mygroup \
    --max-delivery-count 10 \
    --default-message-time-to-live P7D

# Get connection string
az servicebus namespace authorization-rule keys list \
    --namespace-name myservicebus \
    --resource-group mygroup \
    --name RootManageSharedAccessKey
```

### Python SDK - Queue Operations

```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential
import json

# Using connection string
connection_string = "Endpoint=sb://..."
client = ServiceBusClient.from_connection_string(connection_string)

# Using managed identity
credential = DefaultAzureCredential()
client = ServiceBusClient(
    fully_qualified_namespace="myservicebus.servicebus.windows.net",
    credential=credential
)

# Send message
with client.get_queue_sender("myqueue") as sender:
    message = ServiceBusMessage(
        body=json.dumps({"orderId": "12345", "amount": 99.99}),
        content_type="application/json",
        subject="order-created",
        application_properties={"priority": "high"}
    )
    sender.send_messages(message)

# Send batch
with client.get_queue_sender("myqueue") as sender:
    batch = sender.create_message_batch()
    for i in range(10):
        try:
            batch.add_message(ServiceBusMessage(f"Message {i}"))
        except ValueError:
            # Batch is full
            sender.send_messages(batch)
            batch = sender.create_message_batch()
            batch.add_message(ServiceBusMessage(f"Message {i}"))
    sender.send_messages(batch)

# Receive messages
with client.get_queue_receiver("myqueue") as receiver:
    messages = receiver.receive_messages(max_message_count=10, max_wait_time=5)
    for message in messages:
        print(f"Received: {str(message)}")
        # Process message
        receiver.complete_message(message)

# Receive with peek lock (manual completion)
with client.get_queue_receiver("myqueue", receive_mode="peek_lock") as receiver:
    messages = receiver.receive_messages()
    for message in messages:
        try:
            process_message(message)
            receiver.complete_message(message)
        except Exception:
            receiver.abandon_message(message)  # Return to queue
            # or receiver.dead_letter_message(message)  # Move to DLQ
```

### TypeScript SDK - Queue Operations

```typescript
import { ServiceBusClient, ServiceBusMessage } from "@azure/service-bus";

const connectionString = "Endpoint=sb://...";
const client = new ServiceBusClient(connectionString);

// Send message
const sender = client.createSender("myqueue");
await sender.sendMessages({
  body: { orderId: "12345", amount: 99.99 },
  contentType: "application/json",
  subject: "order-created",
  applicationProperties: { priority: "high" }
});

// Send batch
const batch = await sender.createMessageBatch();
for (let i = 0; i < 100; i++) {
  if (!batch.tryAddMessage({ body: `Message ${i}` })) {
    await sender.sendMessages(batch);
    batch = await sender.createMessageBatch();
    batch.tryAddMessage({ body: `Message ${i}` });
  }
}
await sender.sendMessages(batch);
await sender.close();

// Receive messages
const receiver = client.createReceiver("myqueue");
const messages = await receiver.receiveMessages(10, { maxWaitTimeInMs: 5000 });
for (const message of messages) {
  console.log(`Received: ${message.body}`);
  await receiver.completeMessage(message);
}
await receiver.close();

// Subscribe to messages (continuous processing)
receiver.subscribe({
  processMessage: async (message) => {
    console.log(`Received: ${message.body}`);
    // No need to complete - done automatically
  },
  processError: async (err) => {
    console.error(`Error: ${err}`);
  }
});
```

### Topic/Subscription Operations

```python
# Send to topic
with client.get_topic_sender("mytopic") as sender:
    message = ServiceBusMessage(
        body=json.dumps({"event": "order.created"}),
        subject="orders",
        application_properties={"region": "us-east"}
    )
    sender.send_messages(message)

# Receive from subscription
with client.get_subscription_receiver(
    topic_name="mytopic",
    subscription_name="mysubscription"
) as receiver:
    messages = receiver.receive_messages(max_message_count=10)
    for message in messages:
        print(f"Received: {str(message)}")
        receiver.complete_message(message)
```

### Subscription Filters

```bash
# Create subscription with SQL filter
az servicebus topic subscription create \
    --name orders-us \
    --topic-name mytopic \
    --namespace-name myservicebus \
    --resource-group mygroup

az servicebus topic subscription rule create \
    --name us-filter \
    --subscription-name orders-us \
    --topic-name mytopic \
    --namespace-name myservicebus \
    --resource-group mygroup \
    --filter-sql-expression "region = 'us'"

# Correlation filter
az servicebus topic subscription rule create \
    --name priority-filter \
    --subscription-name priority-orders \
    --topic-name mytopic \
    --namespace-name myservicebus \
    --resource-group mygroup \
    --correlation-filter correlation-id=high-priority
```

### Sessions (Ordered Processing)

```python
# Send messages with session
with client.get_queue_sender("session-queue") as sender:
    for i in range(10):
        message = ServiceBusMessage(
            body=f"Message {i}",
            session_id="order-12345"  # Group messages by session
        )
        sender.send_messages(message)

# Receive from session
with client.get_queue_receiver(
    "session-queue",
    session_id="order-12345"
) as receiver:
    messages = receiver.receive_messages()
    for message in messages:
        # Messages arrive in order within session
        receiver.complete_message(message)

# Accept next available session
with client.get_queue_receiver(
    "session-queue",
    session_id=None  # Accept any session
) as receiver:
    # Process messages from the accepted session
    pass
```

### Dead Letter Queue

```python
# Receive from dead letter queue
dlq_receiver = client.get_queue_receiver(
    "myqueue",
    sub_queue="deadletter"
)

with dlq_receiver:
    messages = dlq_receiver.receive_messages(max_message_count=10)
    for message in messages:
        print(f"DLQ Message: {str(message)}")
        print(f"Dead letter reason: {message.dead_letter_reason}")
        print(f"Dead letter description: {message.dead_letter_error_description}")
        # Reprocess or log
        dlq_receiver.complete_message(message)
```

### Scheduled Messages

```python
from datetime import datetime, timedelta

# Schedule message for future delivery
with client.get_queue_sender("myqueue") as sender:
    scheduled_time = datetime.utcnow() + timedelta(hours=1)
    message = ServiceBusMessage("Scheduled message")
    sequence_number = sender.schedule_messages(message, scheduled_time)

    # Cancel scheduled message
    sender.cancel_scheduled_messages(sequence_number)
```

### Message Deferral

```python
# Defer message for later processing
with client.get_queue_receiver("myqueue") as receiver:
    messages = receiver.receive_messages()
    for message in messages:
        if not ready_to_process(message):
            # Defer the message
            sequence_number = message.sequence_number
            receiver.defer_message(message)
            # Store sequence_number for later retrieval

# Receive deferred message
with client.get_queue_receiver("myqueue") as receiver:
    deferred_message = receiver.receive_deferred_messages([sequence_number])
    receiver.complete_message(deferred_message[0])
```

## Best Practices

1. **Message Size**: Keep messages small; use claim-check pattern for large payloads
2. **Sessions**: Use sessions for ordered processing within groups
3. **Dead Letter**: Always monitor and handle dead letter messages
4. **Batching**: Use batch operations for throughput
5. **Retry**: Implement exponential backoff for transient failures

## Common Workflows

### Message Processing Pipeline
1. Create queue with dead-letter enabled
2. Send messages with correlation IDs
3. Process with peek-lock mode
4. Complete or abandon based on success
5. Monitor DLQ for failures

### Pub/Sub Pattern
1. Create topic for events
2. Create subscriptions with filters
3. Publishers send to topic
4. Subscribers receive from filtered subscriptions
5. Scale independently
