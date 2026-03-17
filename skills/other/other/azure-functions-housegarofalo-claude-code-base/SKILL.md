---
name: azure-functions
description: Build serverless applications with Azure Functions. Create HTTP triggers, queue processors, timer functions, and durable orchestrations. Use for event-driven computing, API backends, and serverless microservices on Azure.
---

# Azure Functions Skill

Build serverless applications with Azure Functions for event-driven computing.

## Triggers

Use this skill when you see:
- azure functions, function app, serverless azure
- http trigger, timer trigger, queue trigger
- durable functions, orchestration
- function binding, function.json

## Instructions

### Create Function App

```bash
# Create storage account (required)
az storage account create \
    --name myfuncstorage \
    --resource-group mygroup \
    --location eastus \
    --sku Standard_LRS

# Create Function App
az functionapp create \
    --name myfuncapp \
    --resource-group mygroup \
    --storage-account myfuncstorage \
    --consumption-plan-location eastus \
    --runtime python \
    --runtime-version 3.11 \
    --functions-version 4

# Create with Premium plan
az functionapp plan create \
    --name mypremiumplan \
    --resource-group mygroup \
    --location eastus \
    --sku EP1

az functionapp create \
    --name myfuncapp \
    --resource-group mygroup \
    --storage-account myfuncstorage \
    --plan mypremiumplan \
    --runtime node \
    --runtime-version 20 \
    --functions-version 4
```

### Python Functions (v2 Programming Model)

#### HTTP Trigger

```python
import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="hello")
def hello_http(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            name = req_body.get('name')
        except ValueError:
            pass

    if name:
        return func.HttpResponse(f"Hello, {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )

@app.route(route="users/{id}", methods=["GET"])
def get_user(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get('id')
    # Fetch user from database
    return func.HttpResponse(
        json.dumps({"id": user_id, "name": "John"}),
        mimetype="application/json"
    )
```

#### Timer Trigger

```python
@app.timer_trigger(schedule="0 */5 * * * *", arg_name="timer")
def timer_function(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.info('The timer is past due!')

    logging.info('Timer trigger function executed.')
    # Run scheduled task
```

#### Queue Trigger

```python
@app.queue_trigger(arg_name="msg", queue_name="myqueue",
                   connection="AzureWebJobsStorage")
def queue_processor(msg: func.QueueMessage) -> None:
    logging.info(f'Queue trigger processed: {msg.get_body().decode()}')

    data = json.loads(msg.get_body().decode())
    process_message(data)

# Output binding to queue
@app.route(route="enqueue")
@app.queue_output(arg_name="msg", queue_name="myqueue",
                  connection="AzureWebJobsStorage")
def enqueue_message(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
    message = req.get_json()
    msg.set(json.dumps(message))
    return func.HttpResponse("Message enqueued", status_code=202)
```

#### Blob Trigger

```python
@app.blob_trigger(arg_name="blob", path="container/{name}",
                  connection="AzureWebJobsStorage")
def blob_processor(blob: func.InputStream) -> None:
    logging.info(f'Blob trigger: {blob.name}, Size: {blob.length} bytes')
    content = blob.read()
    process_blob(content)

# Output binding to blob
@app.route(route="upload")
@app.blob_output(arg_name="outputblob", path="container/{rand-guid}.txt",
                 connection="AzureWebJobsStorage")
def upload_blob(req: func.HttpRequest, outputblob: func.Out[str]) -> func.HttpResponse:
    content = req.get_body().decode()
    outputblob.set(content)
    return func.HttpResponse("Blob created", status_code=201)
```

#### Cosmos DB Trigger

```python
@app.cosmos_db_trigger(arg_name="documents",
                       container_name="items",
                       database_name="mydb",
                       connection="CosmosDBConnection",
                       lease_container_name="leases",
                       create_lease_container_if_not_exists=True)
def cosmos_trigger(documents: func.DocumentList) -> None:
    for doc in documents:
        logging.info(f'Document id: {doc["id"]}')
        process_document(doc)
```

### TypeScript Functions (v4 Programming Model)

```typescript
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";

// HTTP trigger
app.http("hello", {
  methods: ["GET", "POST"],
  authLevel: "function",
  handler: async (request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> => {
    context.log(`Http function processed request for url "${request.url}"`);

    const name = request.query.get("name") || (await request.text()) || "world";

    return {
      body: `Hello, ${name}!`,
    };
  },
});

// Timer trigger
app.timer("timerTrigger", {
  schedule: "0 */5 * * * *",
  handler: async (timer: Timer, context: InvocationContext): Promise<void> => {
    context.log("Timer trigger function executed");
  },
});

// Queue trigger with output binding
app.storageQueue("queueTrigger", {
  queueName: "myqueue",
  connection: "AzureWebJobsStorage",
  handler: async (message: unknown, context: InvocationContext): Promise<void> => {
    context.log(`Queue message: ${JSON.stringify(message)}`);
  },
});
```

### Durable Functions

```python
import azure.functions as func
import azure.durable_functions as df

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Orchestrator
@app.orchestration_trigger(context_name="context")
def orchestrator(context: df.DurableOrchestrationContext):
    # Fan-out/fan-in pattern
    tasks = []
    for i in range(5):
        tasks.append(context.call_activity("activity_function", i))

    results = yield context.task_all(tasks)

    # Process results
    total = sum(results)
    return total

# Activity
@app.activity_trigger(input_name="input")
def activity_function(input: int) -> int:
    return input * 2

# HTTP starter
@app.route(route="orchestrators/{functionName}")
@app.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client: df.DurableOrchestrationClient) -> func.HttpResponse:
    function_name = req.route_params.get('functionName')
    instance_id = await client.start_new(function_name)

    return client.create_check_status_response(req, instance_id)
```

### Application Settings

```bash
# Set application settings
az functionapp config appsettings set \
    --name myfuncapp \
    --resource-group mygroup \
    --settings "DatabaseConnection=connection-string" \
               "ApiKey=your-api-key"

# Get application settings
az functionapp config appsettings list \
    --name myfuncapp \
    --resource-group mygroup

# Reference Key Vault secrets
az functionapp config appsettings set \
    --name myfuncapp \
    --resource-group mygroup \
    --settings "Secret=@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/mysecret/)"
```

### Managed Identity

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Use managed identity
credential = DefaultAzureCredential()
secret_client = SecretClient(
    vault_url="https://myvault.vault.azure.net",
    credential=credential
)

secret = secret_client.get_secret("my-secret")
```

### Deployment

```bash
# Deploy from local
func azure functionapp publish myfuncapp

# Deploy with zip
az functionapp deployment source config-zip \
    --name myfuncapp \
    --resource-group mygroup \
    --src app.zip

# Continuous deployment from GitHub
az functionapp deployment source config \
    --name myfuncapp \
    --resource-group mygroup \
    --repo-url https://github.com/org/repo \
    --branch main \
    --manual-integration
```

## Best Practices

1. **Cold Starts**: Use Premium plan for latency-sensitive apps
2. **Bindings**: Use input/output bindings instead of SDK calls when possible
3. **Secrets**: Use Key Vault references for sensitive settings
4. **Logging**: Use structured logging with Application Insights
5. **Scaling**: Configure host.json for optimal scaling

## Common Workflows

### API Backend
1. Create Function App with HTTP triggers
2. Implement CRUD operations
3. Add authentication (Azure AD, API keys)
4. Configure CORS settings
5. Enable Application Insights

### Event Processing
1. Set up queue/blob/Cosmos DB triggers
2. Implement processing logic
3. Configure dead-letter queues
4. Add retry policies
5. Monitor with alerts
