---
name: azure-functions
description: Build serverless applications with Azure Functions. Create HTTP triggers, queue processors, timer functions, and durable orchestrations. Use for event-driven computing, API backends, and serverless microservices on Azure.
---

# Azure Functions

Expert guidance for serverless computing with Azure Functions.

## Project Setup

```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Create new project
func init MyFunctionApp --worker-runtime python
func init MyFunctionApp --worker-runtime node
func init MyFunctionApp --worker-runtime dotnet

# Create function
func new --name HttpTrigger --template "HTTP trigger"

# Run locally
func start
```

## Python Functions

### HTTP Trigger

```python
# function_app.py
import azure.functions as func
import json

app = func.FunctionApp()

@app.route(route="hello", methods=["GET", "POST"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            name = req_body.get('name')
        except ValueError:
            pass

    if name:
        return func.HttpResponse(f"Hello, {name}!")
    return func.HttpResponse(
        "Pass a name in the query string or request body",
        status_code=400
    )

@app.route(route="users/{id}", methods=["GET"])
def get_user(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get('id')
    return func.HttpResponse(json.dumps({"id": user_id}))
```

### Queue Trigger

```python
@app.queue_trigger(arg_name="msg", queue_name="tasks", connection="AzureWebJobsStorage")
def process_queue(msg: func.QueueMessage) -> None:
    logging.info(f'Processing message: {msg.get_body().decode()}')
    # Process the message

@app.queue_output(arg_name="outputQueue", queue_name="results", connection="AzureWebJobsStorage")
def queue_with_output(req: func.HttpRequest, outputQueue: func.Out[str]) -> func.HttpResponse:
    outputQueue.set("Message to queue")
    return func.HttpResponse("Message queued")
```

### Timer Trigger

```python
@app.timer_trigger(schedule="0 */5 * * * *", arg_name="timer")
def scheduled_task(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.info('Timer is past due!')
    logging.info('Timer trigger executed')
```

### Blob Trigger

```python
@app.blob_trigger(arg_name="blob", path="uploads/{name}", connection="AzureWebJobsStorage")
def process_blob(blob: func.InputStream) -> None:
    logging.info(f"Processing blob: {blob.name}, Size: {blob.length} bytes")
    content = blob.read()

@app.blob_output(arg_name="outputBlob", path="processed/{name}", connection="AzureWebJobsStorage")
def blob_processor(req: func.HttpRequest, outputBlob: func.Out[str]) -> func.HttpResponse:
    outputBlob.set("Processed content")
    return func.HttpResponse("Blob created")
```

### Cosmos DB Trigger

```python
@app.cosmos_db_trigger(
    arg_name="documents",
    database_name="mydb",
    container_name="items",
    connection="CosmosDBConnection",
    lease_container_name="leases"
)
def cosmos_trigger(documents: func.DocumentList) -> None:
    for doc in documents:
        logging.info(f"Document: {doc.to_dict()}")
```

### Event Hub Trigger

```python
@app.event_hub_message_trigger(
    arg_name="event",
    event_hub_name="myeventhub",
    connection="EventHubConnection"
)
def eventhub_trigger(event: func.EventHubEvent) -> None:
    logging.info(f"Event: {event.get_body().decode()}")
```

## Durable Functions

### Orchestrator

```python
import azure.durable_functions as df

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.orchestration_trigger(context_name="context")
def orchestrator(context: df.DurableOrchestrationContext):
    # Call activity functions
    result1 = yield context.call_activity("Activity1", "input1")
    result2 = yield context.call_activity("Activity2", result1)

    # Fan-out/fan-in pattern
    tasks = []
    for item in ["a", "b", "c"]:
        tasks.append(context.call_activity("ProcessItem", item))
    results = yield context.task_all(tasks)

    return results

@app.activity_trigger(input_name="input")
def Activity1(input: str) -> str:
    return f"Processed: {input}"

@app.route(route="start")
@app.durable_client_input(client_name="client")
async def start_orchestration(req: func.HttpRequest, client) -> func.HttpResponse:
    instance_id = await client.start_new("orchestrator", None, None)
    return client.create_check_status_response(req, instance_id)
```

### Human Interaction Pattern

```python
@app.orchestration_trigger(context_name="context")
def approval_workflow(context: df.DurableOrchestrationContext):
    # Request approval
    yield context.call_activity("SendApprovalRequest", context.instance_id)

    # Wait for external event with timeout
    approval_event = context.wait_for_external_event("ApprovalResponse")
    timeout = context.create_timer(context.current_utc_datetime + timedelta(hours=24))

    winner = yield context.task_any([approval_event, timeout])

    if winner == approval_event:
        approved = approval_event.result
        if approved:
            yield context.call_activity("ProcessApproval", None)
        else:
            yield context.call_activity("RejectRequest", None)
    else:
        yield context.call_activity("Escalate", None)
```

## TypeScript/JavaScript Functions

```typescript
// src/functions/httpTrigger.ts
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";

export async function httpTrigger(request: HttpRequest, context: InvocationContext): Promise<HttpResponseInit> {
    context.log(`Http function processed request for url "${request.url}"`);

    const name = request.query.get('name') || await request.text() || 'World';

    return { body: `Hello, ${name}!` };
}

app.http('httpTrigger', {
    methods: ['GET', 'POST'],
    authLevel: 'anonymous',
    handler: httpTrigger
});
```

## Configuration

### host.json

```json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  },
  "extensions": {
    "http": {
      "routePrefix": "api",
      "maxOutstandingRequests": 200,
      "maxConcurrentRequests": 100
    },
    "queues": {
      "batchSize": 16,
      "maxPollingInterval": "00:00:02"
    }
  }
}
```

### local.settings.json

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "CosmosDBConnection": "AccountEndpoint=...",
    "EventHubConnection": "Endpoint=..."
  }
}
```

## Deployment

```bash
# Deploy to Azure
func azure functionapp publish <FunctionAppName>

# Deploy with slots
func azure functionapp publish <FunctionAppName> --slot staging

# Create Function App
az functionapp create \
  --resource-group myResourceGroup \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name myFunctionApp \
  --storage-account mystorageaccount
```

## Bicep Deployment

```bicep
resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
      ]
    }
  }
}
```

## Resources

- [Azure Functions Documentation](https://learn.microsoft.com/azure/azure-functions/)
- [Durable Functions](https://learn.microsoft.com/azure/azure-functions/durable/)
- [Azure Functions Python Guide](https://learn.microsoft.com/azure/azure-functions/functions-reference-python)
