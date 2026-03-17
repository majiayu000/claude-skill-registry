---
name: azure-event-grid
description: Event routing with Azure Event Grid. Configure topics, subscriptions, event handlers, and dead-lettering. Use for event-driven architectures, serverless triggers, and reactive systems on Azure.
---

# Azure Event Grid

Expert guidance for event routing and serverless event handling.

## Create Resources

```bash
# Create custom topic
az eventgrid topic create \
  --name myeventtopic \
  --resource-group myResourceGroup \
  --location eastus

# Create system topic (for Azure services)
az eventgrid system-topic create \
  --name mysystemtopic \
  --resource-group myResourceGroup \
  --source /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{account} \
  --topic-type Microsoft.Storage.StorageAccounts \
  --location eastus

# Create subscription
az eventgrid event-subscription create \
  --name mysubscription \
  --source-resource-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.EventGrid/topics/myeventtopic \
  --endpoint https://myfunction.azurewebsites.net/api/handler \
  --endpoint-type webhook
```

## Event Subscriptions

### Webhook Endpoint

```bash
az eventgrid event-subscription create \
  --name webhook-sub \
  --source-resource-id $TOPIC_ID \
  --endpoint https://myapi.com/events \
  --endpoint-type webhook \
  --event-delivery-schema eventgridschema
```

### Azure Function

```bash
az eventgrid event-subscription create \
  --name function-sub \
  --source-resource-id $TOPIC_ID \
  --endpoint /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Web/sites/{app}/functions/{function} \
  --endpoint-type azurefunction
```

### Service Bus Queue

```bash
az eventgrid event-subscription create \
  --name servicebus-sub \
  --source-resource-id $TOPIC_ID \
  --endpoint /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.ServiceBus/namespaces/{ns}/queues/{queue} \
  --endpoint-type servicebusqueue
```

### Storage Queue

```bash
az eventgrid event-subscription create \
  --name storage-sub \
  --source-resource-id $TOPIC_ID \
  --endpoint /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{account}/queueServices/default/queues/{queue} \
  --endpoint-type storagequeue
```

## Publish Events

### Python

```python
from azure.eventgrid import EventGridPublisherClient, EventGridEvent
from azure.core.credentials import AzureKeyCredential

client = EventGridPublisherClient(
    endpoint="https://myeventtopic.eastus-1.eventgrid.azure.net/api/events",
    credential=AzureKeyCredential(key)
)

events = [
    EventGridEvent(
        event_type="MyApp.Orders.Created",
        data={"orderId": "12345", "customer": "John"},
        subject="orders/12345",
        data_version="1.0"
    )
]

client.send(events)
```

### .NET

```csharp
using Azure;
using Azure.Messaging.EventGrid;

var client = new EventGridPublisherClient(
    new Uri(topicEndpoint),
    new AzureKeyCredential(topicKey)
);

var events = new List<EventGridEvent>
{
    new EventGridEvent(
        subject: "orders/12345",
        eventType: "MyApp.Orders.Created",
        data        data: new { OrderId = "12345", Customer = "John" }
    )
};

await client.SendEventsAsync(events);
```

### Cloud Events

```python
from azure.eventgrid import EventGridPublisherClient
from azure.core.messaging import CloudEvent

client = EventGridPublisherClient(endpoint, credential)

events = [
    CloudEvent(
        type="MyApp.Orders.Created",
        source="/myapp/orders",
        data={"orderId": "12345"},
    )
]

client.send(events)
```

## Event Filtering

### Subject Filtering

```bash
az eventgrid event-subscription create \
  --name filtered-sub \
  --source-resource-id $TOPIC_ID \
  --endpoint https://myapi.com/events \
  --subject-begins-with "orders/" \
  --subject-ends-with ".json"
```

### Advanced Filtering

```bash
az eventgrid event-subscription create \
  --name advanced-sub \
  --source-resource-id $TOPIC_ID \
  --endpoint https://myapi.com/events \
  --advanced-filter data.priority StringIn high critical \
  --advanced-filter data.amount NumberGreaterThan 1000
```

### Advanced Filter Examples

```json
{
  "filter": {
    "advancedFilters": [
      {
        "operatorType": "StringIn",
        "key": "data.category",
        "values": ["electronics", "clothing"]
      },
      {
        "operatorType": "NumberGreaterThan",
        "key": "data.price",
        "value": 100
      },
      {
        "operatorType": "IsNotNull",
        "key": "data.customerId"
      }
    ]
  }
}
```

## Dead Lettering

```bash
az eventgrid event-subscription create \
  --name sub-with-dlq \
  --source-resource-id $TOPIC_ID \
  --endpoint https://myapi.com/events \
  --deadletter-endpoint /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{account}/blobServices/default/containers/deadletters \
  --max-delivery-attempts 10 \
  --event-ttl 1440
```

## Azure Function Handler

```python
import azure.functions as func
import json

def main(event: func.EventGridEvent):
    event_data = event.get_json()

    print(f"Event ID: {event.id}")
    print(f"Event Type: {event.event_type}")
    print(f"Subject: {event.subject}")
    print(f"Data: {json.dumps(event_data)}")

    # Process event
    if event.event_type == "MyApp.Orders.Created":
        process_order(event_data)
```

## System Topics (Built-in Events)

```bash
# Storage events
az eventgrid system-topic event-subscription create \
  --name blob-created \
  --system-topic-name storage-topic \
  --resource-group myResourceGroup \
  --endpoint https://myfunction.azurewebsites.net/api/blobhandler \
  --included-event-types Microsoft.Storage.BlobCreated

# Resource events
az eventgrid event-subscription create \
  --name resource-changes \
  --source-resource-id /subscriptions/{sub} \
  --endpoint https://myapi.com/events \
  --included-event-types Microsoft.Resources.ResourceWriteSuccess
```

## Bicep Deployment

```bicep
resource eventGridTopic 'Microsoft.EventGrid/topics@2023-12-15-preview' = {
  name: topicName
  location: location
  properties: {
    inputSchema: 'EventGridSchema'
    publicNetworkAccess: 'Enabled'
  }
}

resource subscription 'Microsoft.EventGrid/eventSubscriptions@2023-12-15-preview' = {
  name: 'webhook-subscription'
  scope: eventGridTopic
  properties: {
    destination: {
      endpointType: 'WebHook'
      properties: {
        endpointUrl: webhookUrl
      }
    }
    filter: {
      includedEventTypes: [
        'MyApp.Orders.Created'
        'MyApp.Orders.Updated'
      ]
    }
    retryPolicy: {
      maxDeliveryAttempts: 10
      eventTimeToLiveInMinutes: 1440
    }
  }
}
```

## Resources

- [Event Grid Documentation](https://learn.microsoft.com/azure/event-grid/)
- [Event Schemas](https://learn.microsoft.com/azure/event-grid/event-schema)
- [Event Grid Python SDK](https://learn.microsoft.com/python/api/overview/azure/eventgrid)
