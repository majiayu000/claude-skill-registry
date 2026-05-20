---
name: azure-functions
description: |
  Build serverless applications with Azure Functions. Create HTTP and event-driven
  functions with input/output bindings, configure triggers for queues, timers,
  and blob storage. Use Durable Functions for stateful orchestration workflows.
license: Apache-2.0
compatibility: 'azure-cli, func-cli, terraform'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
    - azure
    - functions
    - serverless
    - durable-functions
---

# Azure Functions

Azure Functions is a serverless compute service that runs event-driven code without managing infrastructure. Its unique binding system connects to Azure services declaratively, and Durable Functions enable complex stateful workflows.

## Core Concepts

- **Trigger** — what causes a function to run (HTTP, timer, queue, blob, etc.)
- **Input Binding** — declaratively read data from a service when function runs
- **Output Binding** — declaratively write data to a service after function runs
- **Function App** — a container for one or more functions sharing configuration
- **Hosting Plan** — Consumption (pay-per-execution), Premium, or Dedicated
- **Durable Functions** — extension for stateful orchestrations and workflows

## Project Setup

```bash
# Create a new function project
func init my-functions --worker-runtime node --language javascript
cd my-functions
```

```bash
# Create a new HTTP-triggered function
func new --name HandleWebhook --template "HTTP trigger" --authlevel anonymous
```

```bash
# Create Azure resources
az group create --name my-app-rg --location eastus

az storage account create \
  --name myappfuncstorage \
  --resource-group my-app-rg \
  --sku Standard_LRS

az functionapp create \
  --name my-app-functions \
  --resource-group my-app-rg \
  --storage-account myappfuncstorage \
  --consumption-plan-location eastus \
  --runtime node \
  --runtime-version 20 \
  --functions-version 4
```

## HTTP Functions

```javascript
// src/functions/handleWebhook.js — HTTP triggered function
const { app } = require('@azure/functions');

app.http('handleWebhook', {
    methods: ['POST'],
    authLevel: 'anonymous',
    route: 'webhooks/{source}',
    handler: async (request, context) => {
        const source = request.params.source;
        const body = await request.json();

        context.log(`Webhook from ${source}:`, body);

        // Process webhook
        const result = await processWebhook(source, body);

        return {
            status: 200,
            jsonBody: { received: true, id: result.id }
        };
    }
});
```

## Timer Functions

```javascript
// src/functions/dailyCleanup.js — runs on a CRON schedule
const { app } = require('@azure/functions');

app.timer('dailyCleanup', {
    schedule: '0 0 2 * * *', // 2:00 AM daily
    handler: async (myTimer, context) => {
        context.log('Running daily cleanup at', new Date().toISOString());

        const deleted = await cleanupExpiredSessions();
        context.log(`Deleted ${deleted} expired sessions`);
    }
});
```

## Queue Trigger with Output Binding

```javascript
// src/functions/processOrder.js — triggered by queue, writes to Cosmos DB
const { app, output } = require('@azure/functions');

const cosmosOutput = output.cosmosDB({
    databaseName: 'app-db',
    containerName: 'processed-orders',
    connection: 'CosmosDBConnection',
    createIfNotExists: true
});

app.storageQueue('processOrder', {
    queueName: 'order-queue',
    connection: 'AzureWebJobsStorage',
    return: cosmosOutput,
    handler: async (queueItem, context) => {
        context.log('Processing order:', queueItem.orderId);

        const processedOrder = {
            id: queueItem.orderId,
            ...queueItem,
            status: 'processed',
            processedAt: new Date().toISOString()
        };

        // Returned value goes to Cosmos DB via output binding
        return processedOrder;
    }
});
```

## Blob Trigger

```javascript
// src/functions/processImage.js — triggered when blob is uploaded
const { app } = require('@azure/functions');

app.storageBlob('processImage', {
    path: 'uploads/{name}',
    connection: 'AzureWebJobsStorage',
    handler: async (blob, context) => {
        const fileName = context.triggerMetadata.name;
        context.log(`Processing blob: ${fileName}, size: ${blob.length} bytes`);

        // Resize image, extract metadata, etc.
        await generateThumbnail(blob, fileName);
    }
});
```

## Durable Functions

```javascript
// src/functions/orderOrchestrator.js — orchestrate multi-step order processing
const { app } = require('@azure/functions');
const df = require('durable-functions');

// Orchestrator function
df.app.orchestration('orderOrchestrator', function* (context) {
    const order = context.df.getInput();

    // Step 1: Validate inventory
    const inventory = yield context.df.callActivity('checkInventory', order.items);
    if (!inventory.available) {
        yield context.df.callActivity('notifyCustomer', {
            orderId: order.id,
            message: 'Items out of stock'
        });
        return { status: 'cancelled', reason: 'out_of_stock' };
    }

    // Step 2: Process payment
    const payment = yield context.df.callActivity('processPayment', {
        amount: order.total,
        customerId: order.customerId
    });

    // Step 3: Ship order (with retry)
    const retryOptions = new df.RetryOptions(5000, 3); // 5s interval, 3 attempts
    const shipment = yield context.df.callActivityWithRetry(
        'shipOrder', retryOptions, order
    );

    // Step 4: Notify customer
    yield context.df.callActivity('notifyCustomer', {
        orderId: order.id,
        message: `Shipped! Tracking: ${shipment.trackingNumber}`
    });

    return { status: 'completed', tracking: shipment.trackingNumber };
});

// Activity functions
df.app.activity('checkInventory', { handler: async (items) => { /* ... */ } });
df.app.activity('processPayment', { handler: async (payment) => { /* ... */ } });
df.app.activity('shipOrder', { handler: async (order) => { /* ... */ } });
df.app.activity('notifyCustomer', { handler: async (notification) => { /* ... */ } });

// HTTP starter
app.http('startOrder', {
    route: 'orders/start',
    methods: ['POST'],
    extraInputs: [df.input.durableClient()],
    handler: async (req, context) => {
        const client = df.getClient(context);
        const order = await req.json();
        const instanceId = await client.startNew('orderOrchestrator', { input: order });
        return client.createCheckStatusResponse(req, instanceId);
    }
});
```

## Deployment

```bash
# Deploy to Azure
func azure functionapp publish my-app-functions
```

```bash
# Set application settings
az functionapp config appsettings set \
  --name my-app-functions \
  --resource-group my-app-rg \
  --settings "CosmosDBConnection=AccountEndpoint=..."
```

```bash
# View function logs
func azure functionapp logstream my-app-functions
```

## Best Practices

- Use bindings to avoid boilerplate for reading/writing Azure services
- Choose Consumption plan for sporadic workloads, Premium for consistent traffic
- Use Durable Functions for multi-step workflows instead of chaining queues
- Store connection strings in Application Settings, not code
- Set `FUNCTIONS_WORKER_PROCESS_COUNT` for CPU-bound workloads
- Use managed identities instead of connection strings where possible
- Enable Application Insights for monitoring and diagnostics
- Keep functions small and focused — one trigger, one purpose
