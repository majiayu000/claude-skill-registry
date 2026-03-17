---
name: azure-service-bus
description: Enterprise messaging with Azure Service Bus. Configure queues, topics, subscriptions, and message processing. Use for async communication, event-driven architectures, and reliable message delivery on Azure.
---

# Azure Service Bus

Expert guidance for enterprise messaging on Azure.

## Create Resources

```bash
# Create namespace
az servicebus namespace create \
  --name myservicebus \
  --resource-group myResourceGroup \
  --location eastus \
  --sku Standard

# Create queue
az servicebus queue create \
  --name orders \
  --namespace-name myservicebus \
  --resource-group myResourceGroup \
  --max-size 5120 \
  --default-message-time-to-live P14D

# Create topic
az servicebus topic create \
  --name events \
  --namespace-name myservicebus \
  --resource-group myResourceGroup

# Create subscription
az servicebus topic subscription create \
  --name processor \
  --topic-name events \
  --namespace-name myservicebus \
  --resource-group myResourceGroup
```

## Python SDK

### Connection

```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

# Connection string
client = ServiceBusClient.from_connection_string(conn_str)

# Managed Identity
credential = DefaultAzureCredential()
client = ServiceBusClient(
    fully_qualified_namespace="myservicebus.servicebus.windows.net",
    credential=credential
)
```

### Send Messages

```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage

with ServiceBusClient.from_connection_string(conn_str) as client:
    sender = client.get_queue_sender(queue_name="orders")

    with sender:
        # Single message
        message = ServiceBusMessage(
            body="Order data",
            application_properties={"order_id": "123"},
            subject="new-order"
        )
        sender.send_messages(message)

        # Batch messages
        batch = sender.create_message_batch()
        for i in range(10):
            batch.add_message(ServiceBusMessage(f"Message {i}"))
        sender.send_messages(batch)
```

### Receive Messages

```python
from azure.servicebus import ServiceBusClient, ServiceBusReceiveMode

with ServiceBusClient.from_connection_string(conn_str) as client:
    receiver = client.get_queue_receiver(
        queue_name="orders",
        receive_mode=ServiceBusReceiveMode.PEEK_LOCK
    )

    with receiver:
        # Receive batch
        messages = receiver.receive_messages(max_message_count=10, max_wait_time=5)

        for msg in messages:
            print(f"Received: {str(msg)}")
            print(f"Properties: {msg.application_properties}")

            # Complete message
            receiver.complete_message(msg)

            # Or dead-letter
            # receiver.dead_letter_message(msg, reason="Processing failed")
```

### Async Processing

```python
import asyncio
from azure.servicebus.aio import ServiceBusClient

async def process_messages():
    async with ServiceBusClient.from_connection_string(conn_str) as client:
        receiver = client.get_queue_receiver(queue_name="orders")

        async with receiver:
            async for msg in receiver:
                print(f"Received: {str(msg)}")
                await receiver.complete_message(msg)

asyncio.run(process_messages())
```

### Topics and Subscriptions

```python
# Send to topic
with ServiceBusClient.from_connection_string(conn_str) as client:
    sender = client.get_topic_sender(topic_name="events")

    with sender:
        message = ServiceBusMessage(
            body="Event data",
            subject="order.created"
        )
        sender.send_messages(message)

# Receive from subscription
with ServiceBusClient.from_connection_string(conn_str) as client:
    receiver = client.get_subscription_receiver(
        topic_name="events",
        subscription_name="processor"
    )

    with receiver:
        messages = receiver.receive_messages(max_message_count=10)
        for msg in messages:
            receiver.complete_message(msg)
```

## .NET SDK

```csharp
using Azure.Messaging.ServiceBus;

// Send
await using var client = new ServiceBusClient(connectionString);
ServiceBusSender sender = client.CreateSender("orders");

await sender.SendMessageAsync(new ServiceBusMessage("Order data"));

// Receive
ServiceBusReceiver receiver = client.CreateReceiver("orders");
ServiceBusReceivedMessage message = await receiver.ReceiveMessageAsync();
await receiver.CompleteMessageAsync(message);

// Processor
ServiceBusProcessor processor = client.CreateProcessor("orders");
processor.ProcessMessageAsync += async args =>
{
    Console.WriteLine($"Received: {args.Message.Body}");
    await args.CompleteMessageAsync(args.Message);
};
processor.ProcessErrorAsync += args =>
{
    Console.WriteLine($"Error: {args.Exception}");
    return Task.CompletedTask;
};

await processor.StartProcessingAsync();
```

## Subscription Filters

```bash
# SQL filter
az servicebus topic subscription rule create \
  --name high-priority \
  --subscription-name processor \
  --topic-name events \
  --namespace-name myservicebus \
  --resource-group myResourceGroup \
  --filter-sql-expression "priority = 'high'"

# Correlation filter
az servicebus topic subscription rule create \
  --name order-events \
  --subscription-name orders \
  --topic-name events \
  --namespace-name myservicebus \
  --resource-group myResourceGroup \
  --correlation-filter subject=order.created
```

## Sessions

```python
# Send session messages
message = ServiceBusMessage(
    body="Session message",
    session_id="session-123"
)
sender.send_messages(message)

# Receive session messages
session_receiver = client.get_queue_receiver(
    queue_name="session-queue",
    session_id="session-123"
)
```

## Dead Letter Queue

```python
# Receive from DLQ
dlq_receiver = client.get_queue_receiver(
    queue_name="orders",
    sub_queue=ServiceBusSubQueue.DEAD_LETTER
)

with dlq_receiver:
    messages = dlq_receiver.receive_messages(max_message_count=10)
    for msg in messages:
        print(f"Dead letter reason: {msg.dead_letter_reason}")
        print(f"Body: {str(msg)}")
```

## Bicep Deployment

```bicep
resource serviceBusNamespace 'Microsoft.ServiceBus/namespaces@2022-10-01-preview' = {
  name: namespaceName
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
}

resource queue 'Microsoft.ServiceBus/namespaces/queues@2022-10-01-preview' = {
  parent: serviceBusNamespace
  name: 'orders'
  properties: {
    maxSizeInMegabytes: 5120
    defaultMessageTimeToLive: 'P14D'
    deadLetteringOnMessageExpiration: true
    duplicateDetectionHistoryTimeWindow: 'PT10M'
    requiresSession: false
  }
}

resource topic 'Microsoft.ServiceBus/namespaces/topics@2022-10-01-preview' = {
  parent: serviceBusNamespace
  name: 'events'
  properties: {
    maxSizeInMegabytes: 5120
  }
}
```

## Resources

- [Azure Service Bus Documentation](https://learn.microsoft.com/azure/service-bus-messaging/)
- [Service Bus Python SDK](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-python-how-to-use-queues)
- [Best Practices](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-performance-improvements)
