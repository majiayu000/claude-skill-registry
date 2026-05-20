---
name: dapr-microservices
description: Expert guidance for building distributed microservices with Dapr (Distributed Application Runtime) from hello-world prototypes to production-ready systems. Use when working with (1) Service-to-service invocation, (2) State management and persistence, (3) Pub/Sub messaging, (4) Resource bindings and triggers, (5) Virtual actors for stateful services, (6) Workflows and orchestration, (7) Secrets management, (8) Observability and monitoring, (9) Kubernetes deployment. Covers Python, Go, .NET, Java, Node.js implementations.
---

# Dapr Distributed Microservices

Build portable, resilient distributed applications with Dapr - from local development to Kubernetes production.

## Core Concepts

### What is Dapr?

Dapr (Distributed Application Runtime) provides APIs as **building blocks** to simplify microservice development. It runs as a **sidecar** process alongside your application, handling cross-cutting concerns.

**Key benefits:**
- **Language agnostic** - Use any language, any framework
- **Platform agnostic** - Run locally, on-premises, or any cloud
- **Incremental adoption** - Use only the building blocks you need
- **Production-ready** - Built-in retry, circuit breaking, observability

### Architecture

```
┌─────────────────────────────────────┐
│  Your Application                    │
│  (Python, Go, .NET, Java, Node.js)  │
└──────────────┬──────────────────────┘
               │ HTTP/gRPC
┌──────────────▼──────────────────────┐
│  Dapr Sidecar                        │
│  ├─ Service Invocation               │
│  ├─ State Management                 │
│  ├─ Pub/Sub                          │
│  ├─ Bindings                         │
│  ├─ Actors                           │
│  ├─ Workflows                        │
│  ├─ Secrets                          │
│  └─ Configuration                    │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
   Components     Infrastructure
   (Redis, Kafka, (Kubernetes,
    PostgreSQL,    Docker, etc.)
    Azure, AWS)
```

## Building Blocks

### 1. Service Invocation

Call services by name with built-in service discovery, retries, and distributed tracing.

**HTTP API:**

```bash
# Call order-processor service's /orders endpoint
curl http://localhost:3500/v1.0/invoke/order-processor/method/orders \
  -H "Content-Type: application/json" \
  -d '{"orderId": 123, "item": "laptop"}'
```

**Python:**

```python
import requests

dapr_url = "http://localhost:3500/v1.0/invoke/order-processor/method/orders"
order = {"orderId": 123, "item": "laptop"}

response = requests.post(dapr_url, json=order)
print(response.json())
```

See `scripts/service_invocation.py` for complete example.

### 2. State Management

Persist and query key/value data with pluggable state stores.

**HTTP API:**

```bash
# Save state
curl -X POST http://localhost:3500/v1.0/state/statestore \
  -H "Content-Type: application/json" \
  -d '[{"key": "order1", "value": {"orderId": 123, "item": "laptop"}}]'

# Get state
curl http://localhost:3500/v1.0/state/statestore/order1
```

**Python:**

```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Save state
    client.save_state(store_name="statestore", key="order1",
                     value={"orderId": 123, "item": "laptop"})

    # Get state
    state = client.get_state(store_name="statestore", key="order1")
    print(state.data)
```

**Features:**
- ETag-based optimistic concurrency
- Bulk operations
- State transactions
- Query API (with supported stores)

See [STATE_MANAGEMENT.md](references/STATE_MANAGEMENT.md) for advanced patterns.

### 3. Pub/Sub Messaging

Publish and subscribe to messages with at-least-once delivery guarantees.

**Publisher:**

```python
from dapr.clients import DaprClient

with DaprClient() as client:
    client.publish_event(
        pubsub_name='orderpubsub',
        topic_name='orders',
        data={'orderId': 123, "item": "laptop"}
    )
```

**Subscriber (Flask):**

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    return jsonify([{
        'pubsubname': 'orderpubsub',
        'topic': 'orders',
        'route': 'orders'
    }])

@app.route('/orders', methods=['POST'])
def handle_order():
    data = request.json['data']
    print(f"Received order: {data['orderId']}")
    return jsonify({'success': True}), 200
```

See `scripts/pubsub_publisher.py` and `scripts/pubsub_subscriber.py` for complete examples.

### 4. Bindings

Connect to external systems (Kafka, AWS SQS, Azure Event Hubs, Twilio, etc.) with unified API.

**Output binding (send):**

```python
from dapr.clients import DaprClient

with DaprClient() as client:
    client.invoke_binding(
        binding_name='kafka-binding',
        operation='create',
        data={'message': 'Hello from Dapr'},
        metadata={'topic': 'orders'}
    )
```

**Input binding (receive):** Configure via component YAML (see references).

See [BINDINGS_GUIDE.md](references/BINDINGS_GUIDE.md) for all supported bindings.

### 5. Actors

Build stateful services using the virtual actor pattern with single-threaded execution.

**Key features:**
- **State management** - Per-actor state persisted automatically
- **Timers** - Fire-and-forget scheduled callbacks
- **Reminders** - Persistent scheduled callbacks (survive restarts)
- **Concurrency** - Turn-based execution (one method at a time)

**Actor interface (.NET):**

```csharp
public interface IOrderActor : IActor
{
    Task<Order> GetOrderAsync();
    Task SetOrderAsync(Order order);
    Task ProcessOrderAsync();
}
```

**Actor implementation:**

```csharp
public class OrderActor : Actor, IOrderActor
{
    public OrderActor(ActorHost host) : base(host) { }

    public async Task SetOrderAsync(Order order)
    {
        await StateManager.SetStateAsync("order", order);
    }

    public async Task<Order> GetOrderAsync()
    {
        return await StateManager.GetStateAsync<Order>("order");
    }
}
```

See [ACTORS_GUIDE.md](references/ACTORS_GUIDE.md) for complete patterns.

### 6. Workflows

Orchestrate long-running, fault-tolerant business processes across services.

**Workflow definition (.NET):**

```csharp
public class OrderProcessingWorkflow : Workflow<OrderInput, OrderResult>
{
    public override async Task<OrderResult> RunAsync(
        WorkflowContext context, OrderInput input)
    {
        // Step 1: Reserve inventory
        await context.CallActivityAsync("ReserveInventory", input.OrderId);

        // Step 2: Process payment
        var paymentResult = await context.CallActivityAsync<bool>(
            "ProcessPayment", input.Amount);

        if (!paymentResult)
        {
            await context.CallActivityAsync("ReleaseInventory", input.OrderId);
            return new OrderResult { Success = false };
        }

        // Step 3: Ship order
        await context.CallActivityAsync("ShipOrder", input.OrderId);

        return new OrderResult { Success = true };
    }
}
```

**Features:**
- Automatic state persistence
- Retry and timeout handling
- Long-running (days/weeks)
- Human-in-the-loop patterns

See [WORKFLOWS_GUIDE.md](references/WORKFLOWS_GUIDE.md) for orchestration patterns.

### 7. Secrets Management

Securely retrieve secrets from any secret store (Kubernetes, Azure Key Vault, AWS Secrets Manager, HashiCorp Vault).

```python
from dapr.clients import DaprClient

with DaprClient() as client:
    secret = client.get_secret(
        store_name='localsecretstore',
        key='database-password'
    )
    db_password = secret.secret['database-password']
```

**Component configuration:**

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: localsecretstore
spec:
  type: secretstores.local.file
  metadata:
  - name: secretsFile
    value: ./secrets.json
```

### 8. Configuration

Retrieve application configuration from any config store with change notifications.

```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Get configuration
    config = client.get_configuration(
        store_name='configstore',
        keys=['appSettings']
    )

    # Subscribe to changes
    def config_change_handler(id, items):
        print(f"Configuration changed: {items}")

    client.subscribe_configuration(
        store_name='configstore',
        keys=['appSettings'],
        handler=config_change_handler
    )
```

## Quick Start

### Installation

```bash
# Install Dapr CLI
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Verify installation
dapr --version

# Initialize Dapr (installs runtime locally with Docker)
dapr init

# Verify components
docker ps  # Should see dapr_redis, dapr_placement, dapr_zipkin
```

### Hello World

**1. Create application (app.py):**

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Dapr!"}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

**2. Run with Dapr:**

```bash
dapr run --app-id myapp --app-port 5000 --dapr-http-port 3500 -- python app.py
```

**3. Invoke via Dapr:**

```bash
curl http://localhost:3500/v1.0/invoke/myapp/method/hello
```

See `scripts/hello_world.py` for complete example.

## Component Configuration

Components are resources that Dapr uses to provide building block capabilities (state stores, pub/sub, bindings, etc.).

**Component structure:**

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key: password
```

**Common components:**
- **State stores**: Redis, PostgreSQL, MongoDB, Cassandra, Azure Cosmos DB
- **Pub/Sub**: Redis Streams, Kafka, RabbitMQ, Azure Service Bus, AWS SNS/SQS
- **Bindings**: Kafka, Cron, HTTP, AWS S3, Azure Blob Storage, Twilio
- **Secret stores**: Kubernetes, Local file, Azure Key Vault, AWS Secrets Manager

See [COMPONENTS_GUIDE.md](references/COMPONENTS_GUIDE.md) for full reference.

## Production Deployment

### Kubernetes Deployment

**1. Install Dapr on Kubernetes:**

```bash
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

helm install dapr dapr/dapr \
  --version=1.12 \
  --namespace dapr-system \
  --create-namespace \
  --wait
```

**2. Deploy application with sidecar:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "myapp"
        dapr.io/app-port: "5000"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0
        ports:
        - containerPort: 5000
```

**Key annotations:**
- `dapr.io/enabled` - Enable Dapr sidecar injection
- `dapr.io/app-id` - Unique application identifier
- `dapr.io/app-port` - Port your app listens on
- `dapr.io/config` - Name of Dapr configuration
- `dapr.io/log-level` - Logging level (debug, info, warn, error)

### High Availability

```yaml
# Dapr HA configuration (values.yml for Helm)
global:
  ha:
    enabled: true
    replicaCount: 3

placement:
  replicaCount: 3

operator:
  replicaCount: 3
```

### Security

**mTLS (automatic between services):**

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: appconfig
spec:
  mtls:
    enabled: true
    workloadCertTTL: "24h"
    allowedClockSkew: "15m"
```

**Access Control:**

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: appconfig
spec:
  accessControl:
    defaultAction: deny
    trustDomain: "public"
    policies:
    - appId: checkout
      defaultAction: allow
      trustDomain: 'public'
      operations:
      - name: /orders
        httpVerb: ['POST']
        action: allow
```

See [PRODUCTION_GUIDE.md](references/PRODUCTION_GUIDE.md) for complete deployment patterns.

## Observability

Dapr automatically collects metrics, logs, and traces.

**Metrics:**
- HTTP request count/duration
- gRPC call count/duration
- Actor invocations
- Component operations

**Tracing:** Distributed tracing with W3C Trace Context

**Integration:** Prometheus, Grafana, Jaeger, Zipkin, Application Insights

See [OBSERVABILITY_GUIDE.md](references/OBSERVABILITY_GUIDE.md) for monitoring setup.

## Multi-Language Support

Dapr provides SDKs for all major languages, but you can also use HTTP/gRPC directly.

| Language | SDK Repository | Status |
|----------|---------------|--------|
| Python | dapr/python-sdk | Stable |
| Go | dapr/go-sdk | Stable |
| .NET | dapr/dotnet-sdk | Stable |
| Java | dapr/java-sdk | Stable |
| JavaScript | dapr/js-sdk | Stable |
| Rust | dapr/rust-sdk | Alpha |
| PHP | dapr/php-sdk | Alpha |

## Architecture Decision Guide

### When to Use Actors

**Use actors when:**
- Need single-threaded execution per entity (e.g., shopping cart, game player)
- Need distributed locking without distributed locks
- State is scoped to individual entity instances
- Operations are primarily entity-centric

**Avoid actors when:**
- Need high throughput for stateless operations (use service invocation)
- Need complex queries across entities (use state store directly)
- Operations span multiple actors frequently

### Service Invocation vs. Pub/Sub

**Service invocation:**
- Synchronous request-response
- Direct service-to-service communication
- Need immediate response
- Example: Get user profile, validate order

**Pub/Sub:**
- Asynchronous fire-and-forget
- Decoupled publishers and subscribers
- Multiple consumers per message
- Example: Order created event, notification triggers

### State Store Selection

| Store | Use Case | Strengths |
|-------|----------|-----------|
| Redis | Low latency, high throughput | In-memory, fast, good for caching |
| PostgreSQL | Strong consistency, transactions | ACID, complex queries, durability |
| Cosmos DB | Global distribution | Multi-region, low latency worldwide |
| MongoDB | Flexible schema | Document model, horizontal scaling |

## Best Practices

1. **Use app-id strategically** - Keep consistent across environments
2. **Enable mTLS in production** - Automatic encrypted communication
3. **Implement health checks** - `/healthz` endpoint for liveness
4. **Set resource limits** - CPU/memory for sidecar containers
5. **Use configuration for URLs** - No hardcoded endpoints
6. **Implement idempotency** - Handle duplicate deliveries in pub/sub
7. **Monitor metrics** - Track sidecar health and performance
8. **Version components** - Use specific component versions
9. **Test locally first** - Use `dapr run` before Kubernetes
10. **Follow naming conventions** - Clear app-ids and component names

## Common Patterns

### Event-Driven Architecture

```
┌─────────┐    publish    ┌─────────┐
│ Order   │─────event────>│ Pub/Sub │
│ Service │               └────┬────┘
└─────────┘                    │
                               │ subscribe
                    ┌──────────┴─────────┐
                    ▼                    ▼
            ┌──────────────┐    ┌──────────────┐
            │ Notification │    │   Shipping   │
            │   Service    │    │   Service    │
            └──────────────┘    └──────────────┘
```

### Saga Pattern (with Workflows)

Coordinate distributed transactions with compensation logic.

### CQRS (Command Query Responsibility Segregation)

Separate write and read models using state management and pub/sub.

## Troubleshooting

### Common Issues

**Sidecar not starting:**
```bash
# Check Dapr logs
kubectl logs <pod-name> -c daprd

# Verify component configuration
dapr components -k
```

**Service invocation fails:**
- Verify app-id matches target service
- Check network policies in Kubernetes
- Ensure both services have Dapr enabled

**State not persisting:**
- Verify state store component is configured
- Check component connection credentials
- Review Dapr sidecar logs for errors

See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for detailed diagnostics.

## Reference Files

- **[STATE_MANAGEMENT.md](references/STATE_MANAGEMENT.md)** - State patterns, transactions, queries
- **[ACTORS_GUIDE.md](references/ACTORS_GUIDE.md)** - Actor patterns, timers, reminders
- **[WORKFLOWS_GUIDE.md](references/WORKFLOWS_GUIDE.md)** - Workflow orchestration, activities
- **[BINDINGS_GUIDE.md](references/BINDINGS_GUIDE.md)** - All input/output bindings
- **[COMPONENTS_GUIDE.md](references/COMPONENTS_GUIDE.md)** - Component configuration reference
- **[PRODUCTION_GUIDE.md](references/PRODUCTION_GUIDE.md)** - Kubernetes, security, HA
- **[OBSERVABILITY_GUIDE.md](references/OBSERVABILITY_GUIDE.md)** - Metrics, logs, tracing

## Example Scripts

All scripts are tested and ready to use:

- `hello_world.py` - Basic Dapr application
- `service_invocation.py` - Service-to-service calls
- `pubsub_publisher.py` - Publish messages
- `pubsub_subscriber.py` - Subscribe to messages
- `state_management.py` - Save/get/delete state
- `bindings_output.py` - Invoke output binding
- `secrets_example.py` - Retrieve secrets
