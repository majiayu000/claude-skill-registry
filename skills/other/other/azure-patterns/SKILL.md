---
name: azure-patterns
description: Azure Functions, Cosmos DB modeling, Service Bus patterns, Bicep templates
---

# Azure Patterns

## Azure Functions

### HTTP Trigger (Node.js v4)

```typescript
import { app, HttpRequest, HttpResponseInit, InvocationContext } from '@azure/functions';

app.http('getOrder', {
  methods: ['GET'],
  authLevel: 'function',
  route: 'orders/{orderId}',
  handler: async (request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> => {
    const orderId = request.params.orderId;
    context.log(`Processing order: ${orderId}`);

    try {
      const order = await orderService.getById(orderId);
      if (!order) {
        return { status: 404, jsonBody: { error: 'Order not found' } };
      }
      return { status: 200, jsonBody: order };
    } catch (error) {
      context.error('Failed to get order', error);
      return { status: 500, jsonBody: { error: 'Internal server error' } };
    }
  },
});

// Service Bus trigger with retry
app.serviceBusTopic('processOrderEvent', {
  topicName: 'order-events',
  subscriptionName: 'order-processor',
  connection: 'ServiceBusConnection',
  handler: async (message: unknown, context: InvocationContext) => {
    const event = message as OrderEvent;
    context.log(`Processing event: ${event.type} for order ${event.orderId}`);

    await processEvent(event);
  },
});
```

### Durable Functions (Orchestrator)

```typescript
import * as df from 'durable-functions';

df.app.orchestration('orderWorkflow', function* (context) {
  const orderId = context.df.getInput() as string;

  // Step 1: Validate order
  const order = yield context.df.callActivity('validateOrder', orderId);

  // Step 2: Reserve inventory (with retry)
  const retryOptions = new df.RetryOptions(5000, 3); // 5s interval, 3 attempts
  yield context.df.callActivityWithRetry('reserveInventory', retryOptions, order);

  // Step 3: Charge payment
  yield context.df.callActivity('chargePayment', order);

  // Step 4: Wait for shipping confirmation (with timeout)
  const deadline = new Date(context.df.currentUtcDateTime.getTime() + 24 * 60 * 60 * 1000);
  const shippingEvent = context.df.waitForExternalEvent('shippingConfirmed');
  const timeout = context.df.createTimer(deadline);

  const winner = yield context.df.Task.any([shippingEvent, timeout]);
  if (winner === timeout) {
    yield context.df.callActivity('escalateShipping', orderId);
  }

  return { orderId, status: 'completed' };
});
```

## Cosmos DB Modeling

```typescript
// Partition key design: use tenant/user ID for multi-tenant
interface OrderDocument {
  id: string;                    // Unique document ID
  partitionKey: string;          // = tenantId (good distribution)
  type: 'order';                 // Discriminator for polymorphic container
  customerId: string;
  items: OrderItem[];            // Embed frequently accessed together
  total: number;
  status: string;
  createdAt: string;
  _etag?: string;                // Optimistic concurrency
}

// Optimistic concurrency with ETags
async function updateOrder(order: OrderDocument): Promise<void> {
  const container = cosmosClient.database('shop').container('orders');
  try {
    await container.item(order.id, order.partitionKey).replace(order, {
      accessCondition: { type: 'IfMatch', condition: order._etag },
    });
  } catch (error) {
    if (error.code === 412) {
      throw new ConflictError('Order was modified by another process');
    }
    throw error;
  }
}

// Change feed processor for event-driven updates
const changeFeedProcessor = cosmosClient
  .database('shop')
  .container('orders')
  .getChangeFeedProcessorBuilder('orderProcessor')
  .setFeedProcessorOptions({ startFromBeginning: false, maxItemCount: 25 })
  .setLeaseContainer(leaseContainer)
  .setProcessChanges(async (changes, context) => {
    for (const doc of changes) {
      await publishEvent({ type: 'order.updated', data: doc });
    }
  })
  .build();
```

## Service Bus Patterns

```typescript
import { ServiceBusClient, ServiceBusMessage } from '@azure/service-bus';

const client = new ServiceBusClient(process.env.SERVICEBUS_CONNECTION!);

// Send with deduplication and scheduling
async function sendOrderEvent(event: OrderEvent): Promise<void> {
  const sender = client.createSender('order-events');
  const message: ServiceBusMessage = {
    body: event,
    messageId: `${event.orderId}-${event.type}-${Date.now()}`,  // Dedup key
    subject: event.type,
    applicationProperties: { priority: event.priority },
    timeToLive: 24 * 60 * 60 * 1000,  // 24h TTL
  };
  await sender.sendMessages(message);
  await sender.close();
}

// Receive with sessions (ordered processing per entity)
async function processWithSessions(): Promise<void> {
  const receiver = client.acceptSession('order-events', 'order-processor', 'session-1');
  const messages = await receiver.receiveMessages(10, { maxWaitTimeInMs: 5000 });

  for (const msg of messages) {
    try {
      await handleMessage(msg.body);
      await receiver.completeMessage(msg);
    } catch {
      await receiver.abandonMessage(msg);  // Retry via Service Bus
    }
  }
  await receiver.close();
}
```

## Bicep Templates

```bicep
@description('Azure Function App with Service Bus and Cosmos DB')
param location string = resourceGroup().location
param appName string

resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: '${appName}-cosmos'
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    consistencyPolicy: { defaultConsistencyLevel: 'Session' }
    locations: [{ locationName: location, failoverPriority: 0 }]
  }
}

resource serviceBus 'Microsoft.ServiceBus/namespaces@2022-10-01-preview' = {
  name: '${appName}-bus'
  location: location
  sku: { name: 'Standard', tier: 'Standard' }
}

resource functionApp 'Microsoft.Web/sites@2023-12-01' = {
  name: '${appName}-func'
  location: location
  kind: 'functionapp,linux'
  identity: { type: 'SystemAssigned' }
  properties: {
    siteConfig: {
      appSettings: [
        { name: 'CosmosDBConnection', value: cosmosAccount.listConnectionStrings().connectionStrings[0].connectionString }
        { name: 'ServiceBusConnection', value: listKeys('${serviceBus.id}/AuthorizationRules/RootManageSharedAccessKey', serviceBus.apiVersion).primaryConnectionString }
      ]
    }
  }
}
```

## Checklist

- [ ] Functions use managed identity, not connection strings where possible
- [ ] Cosmos DB partition key chosen for even distribution and query patterns
- [ ] Service Bus dead-letter queue monitored and processed
- [ ] Durable Functions used for multi-step workflows
- [ ] Bicep templates parameterized for multi-environment deployment
- [ ] Cosmos DB RU autoscale configured to handle traffic spikes
- [ ] Application Insights connected for distributed tracing
- [ ] Function timeout matches expected workload duration

## Anti-Patterns

- Cross-partition queries in Cosmos DB (expensive, slow)
- Storing large blobs in Cosmos DB (use Blob Storage + reference)
- Not using sessions for ordered message processing
- Shared Service Bus connection strings across services
- Function apps without Application Insights (blind to failures)
- Cosmos DB with fixed RU provisioning for variable workloads
- Not configuring dead-letter queues on Service Bus subscriptions
- Using host keys for Function auth (use managed identity + RBAC)
