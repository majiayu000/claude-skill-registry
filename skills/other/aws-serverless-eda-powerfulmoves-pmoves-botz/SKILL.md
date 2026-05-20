---
name: aws-serverless-eda
description: AWS serverless and event-driven architecture expert based on Well-Architected Framework. Use when building serverless APIs, Lambda functions, REST APIs, microservices, or async workflows. Covers Lambda with TypeScript/Python, API Gateway (REST/HTTP), DynamoDB, Step Functions, EventBridge, SQS, SNS, and serverless patterns. Essential when user mentions serverless, Lambda, API Gateway, event-driven, async processing, queues, pub/sub, or wants to build scalable serverless applications with AWS best practices.
---

# AWS Serverless & Event-Driven Architecture

This skill provides comprehensive guidance for building serverless applications and event-driven architectures on AWS based on Well-Architected Framework principles.

## AWS Documentation Requirement

**CRITICAL**: This skill requires AWS MCP tools for accurate, up-to-date AWS information.

### Before Answering AWS Questions

1. **Always verify** using AWS MCP tools (if available):
   - `mcp__aws-mcp__aws___search_documentation` or `mcp__*awsdocs*__aws___search_documentation` - Search AWS docs
   - `mcp__aws-mcp__aws___read_documentation` or `mcp__*awsdocs*__aws___read_documentation` - Read specific pages
   - `mcp__aws-mcp__aws___get_regional_availability` - Check service availability

2. **If AWS MCP tools are unavailable**:
   - Guide user to configure AWS MCP: See [AWS MCP Setup Guide](../../docs/aws-mcp-setup.md)
   - Help determine which option fits their environment:
     - Has uvx + AWS credentials → Full AWS MCP Server
     - No Python/credentials → AWS Documentation MCP (no auth)
   - If cannot determine → Ask user which option to use

## Serverless MCP Servers

This skill can leverage serverless-specific MCP servers for enhanced development workflows:

### AWS Serverless MCP Server
**Purpose**: Complete serverless application lifecycle with SAM CLI
- Initialize new serverless applications
- Deploy serverless applications
- Test Lambda functions locally
- Generate SAM templates
- Manage serverless application lifecycle

### AWS Lambda Tool MCP Server
**Purpose**: Execute Lambda functions as tools
- Invoke Lambda functions directly
- Test Lambda integrations
- Execute workflows requiring private resource access
- Run Lambda-based automation

### AWS Step Functions MCP Server
**Purpose**: Execute complex workflows and orchestration
- Create and manage state machines
- Execute workflow orchestrations
- Handle distributed transactions
- Implement saga patterns
- Coordinate microservices

### Amazon SNS/SQS MCP Server
**Purpose**: Event-driven messaging and queue management
- Publish messages to SNS topics
- Send/receive messages from SQS queues
- Manage event-driven communication
- Implement pub/sub patterns
- Handle asynchronous processing

## When to Use This Skill

Use this skill when:
- Building serverless applications with Lambda
- Designing event-driven architectures
- Implementing microservices patterns
- Creating asynchronous processing workflows
- Orchestrating multi-service transactions
- Building real-time data processing pipelines
- Implementing saga patterns for distributed transactions
- Designing for scale and resilience

## AWS Well-Architected Serverless Design Principles

### 1. Speedy, Simple, Singular

**Functions should be concise and single-purpose**

```typescript
// ✅ GOOD - Single purpose, focused function
export const processOrder = async (event: OrderEvent) => {
  // Only handles order processing
  const order = await validateOrder(event);
  await saveOrder(order);
  await publishOrderCreatedEvent(order);
  return { statusCode: 200, body: JSON.stringify({ orderId: order.id }) };
};

// ❌ BAD - Function does too much
export const handleEverything = async (event: any) => {
  // Handles orders, inventory, payments, shipping...
  // Too many responsibilities
};
```

**Keep functions environmentally efficient and cost-aware**:
- Minimize cold start times
- Optimize memory allocation
- Use provisioned concurrency only when needed
- Leverage connection reuse

### 2. Think Concurrent Requests, Not Total Requests

**Design for concurrency, not volume**

Lambda scales horizontally - design considerations should focus on:
- Concurrent execution limits
- Downstream service throttling
- Shared resource contention
- Connection pool sizing

```typescript
// Consider concurrent Lambda executions accessing DynamoDB
const table = new dynamodb.Table(this, 'Table', {
  billingMode: dynamodb.BillingMode.PAY_PER_REQUEST, // Auto-scales with load
});

// Or with provisioned capacity + auto-scaling
const table = new dynamodb.Table(this, 'Table', {
  billingMode: dynamodb.BillingMode.PROVISIONED,
  readCapacity: 5,
  writeCapacity: 5,
});

// Enable auto-scaling for concurrent load
table.autoScaleReadCapacity({ minCapacity: 5, maxCapacity: 100 });
table.autoScaleWriteCapacity({ minCapacity: 5, maxCapacity: 100 });
```

### 3. Share Nothing

**Function runtime environments are short-lived**

```typescript
// ❌ BAD - Relying on local file system
export const handler = async (event: any) => {
  fs.writeFileSync('/tmp/data.json', JSON.stringify(data)); // Lost after execution
};

// ✅ GOOD - Use persistent storage
export const handler = async (event: any) => {
  await s3.putObject({
    Bucket: process.env.BUCKET_NAME,
    Key: 'data.json',
    Body: JSON.stringify(data),
  });
};
```

**State management**:
- Use DynamoDB for persistent state
- Use Step Functions for workflow state
- Use ElastiCache for session state
- Use S3 for file storage

### 4. Assume No Hardware Affinity

**Applications must be hardware-agnostic**

Infrastructure can change without notice:
- Lambda functions can run on different hardware
- Container instances can be replaced
- No assumption about underlying infrastructure

**Design for portability**:
- Use environment variables for configuration
- Avoid hardware-specific optimizations
- Test across different environments

### 5. Orchestrate with State Machines, Not Function Chaining

**Use Step Functions for orchestration**

```typescript
// ❌ BAD - Lambda function chaining
export const handler1 = async (event: any) => {
  const result = await processStep1(event);
  await lambda.invoke({
    FunctionName: 'handler2',
    Payload: JSON.stringify(result),
  });
};

// ✅ GOOD - Step Functions orchestration
const stateMachine = new stepfunctions.StateMachine(this, 'OrderWorkflow', {
  definition: stepfunctions.Chain
    .start(validateOrder)
    .next(processPayment)
    .next(shipOrder)
    .next(sendConfirmation),
});
```

**Benefits of Step Functions**:
- Visual workflow representation
- Built-in error handling and retries
- Execution history and debugging
- Parallel and sequential execution
- Service integrations without code

### 6. Use Events to Trigger Transactions

**Event-driven over synchronous request/response**

```typescript
// Pattern: Event-driven processing
const bucket = new s3.Bucket(this, 'DataBucket');

bucket.addEventNotification(
  s3.EventType.OBJECT_CREATED,
  new s3n.LambdaDestination(processFunction),
  { prefix: 'uploads/' }
);

// Pattern: EventBridge integration
const rule = new events.Rule(this, 'OrderRule', {
  eventPattern: {
    source: ['orders'],
    detailType: ['OrderPlaced'],
  },
});

rule.addTarget(new targets.LambdaFunction(processOrderFunction));
```

**Benefits**:
- Loose coupling between services
- Asynchronous processing
- Better fault tolerance
- Independent scaling

### 7. Design for Failures and Duplicates

**Operations must be idempotent**

```typescript
// ✅ GOOD - Idempotent operation
export const handler = async (event: SQSEvent) => {
  for (const record of event.Records) {
    const orderId = JSON.parse(record.body).orderId;

    // Check if already processed (idempotency)
    const existing = await dynamodb.getItem({
      TableName: process.env.TABLE_NAME,
      Key: { orderId },
    });

    if (existing.Item) {
      console.log('Order already processed:', orderId);
      continue; // Skip duplicate
    }

    // Process order
    await processOrder(orderId);

    // Mark as processed
    await dynamodb.putItem({
      TableName: process.env.TABLE_NAME,
      Item: { orderId, processedAt: Date.now() },
    });
  }
};
```

**Implement retry logic with exponential backoff**:
```typescript
async function withRetry<T>(fn: () => Promise<T>, maxRetries = 3): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
    }
  }
  throw new Error('Max retries exceeded');
}
```

## Event-Driven Architecture Patterns

### Pattern 1: Event Router (EventBridge)

Use EventBridge for event routing and filtering:

```typescript
// Create custom event bus
const eventBus = new events.EventBus(this, 'AppEventBus', {
  eventBusName: 'application-events',
});

// Define event schema
const schema = new events.Schema(this, 'OrderSchema', {
  schemaName: 'OrderPlaced',
  definition: events.SchemaDefinition.fromInline({
    openapi: '3.0.0',
    info: { version: '1.0.0', title: 'Order Events' },
    paths: {},
    components: {
      schemas: {
        OrderPlaced: {
          type: 'object',
          properties: {
            orderId: { type: 'string' },
            customerId: { type: 'string' },
            amount: { type: 'number' },
          },
        },
      },
    },
  }),
});

// Create rules for different consumers
new events.Rule(this, 'ProcessOrderRule', {
  eventBus,
  eventPattern: {
    source: ['orders'],
    detailType: ['OrderPlaced'],
  },
  targets: [new targets.LambdaFunction(processOrderFunction)],
});

new events.Rule(this, 'NotifyCustomerRule', {
  eventBus,
  eventPattern: {
    source: ['orders'],
    detailType: ['OrderPlaced'],
  },
  targets: [new targets.LambdaFunction(notifyCustomerFunction)],
});
```

### Pattern 2: Queue-Based Processing (SQS)

Use SQS for reliable asynchronous processing:

```typescript
// Standard queue for at-least-once delivery
const queue = new sqs.Queue(this, 'ProcessingQueue', {
  visibilityTimeout: Duration.seconds(300),
  retentionPeriod: Duration.days(14),
  deadLetterQueue: {
    queue: dlq,
    maxReceiveCount: 3,
  },
});

// FIFO queue for ordered processing
const fifoQueue = new sqs.Queue(this, 'OrderedQueue', {
  fifo: true,
  contentBasedDeduplication: true,
  deduplicationScope: sqs.DeduplicationScope.MESSAGE_GROUP,
});

// Lambda consumer
new lambda.EventSourceMapping(this, 'QueueConsumer', {
  target: processingFunction,
  eventSourceArn: queue.queueArn,
  batchSize: 10,
  maxBatchingWindow: Duration.seconds(5),
});
```

### Pattern 3: Pub/Sub (SNS + SQS Fan-Out)

Implement fan-out pattern for multiple consumers:

```typescript
// Create SNS topic
const topic = new sns.Topic(this, 'OrderTopic', {
  displayName: 'Order Events',
});

// Multiple SQS queues subscribe to topic
const inventoryQueue = new sqs.Queue(this, 'InventoryQueue');
const shippingQueue = new sqs.Queue(this, 'ShippingQueue');
const analyticsQueue = new sqs.Queue(this, 'AnalyticsQueue');

topic.addSubscription(new subscriptions.SqsSubscription(inventoryQueue));
topic.addSubscription(new subscriptions.SqsSubscription(shippingQueue));
topic.addSubscription(new subscriptions.SqsSubscription(analyticsQueue));

// Each queue has its own Lambda consumer
new lambda.EventSourceMapping(this, 'InventoryConsumer', {
  target: inventoryFunction,
  eventSourceArn: inventoryQueue.queueArn,
});
```

### Pattern 4: Saga Pattern with Step Functions

Implement distributed transactions:

```typescript
const reserveFlight = new tasks.LambdaInvoke(this, 'ReserveFlight', {
  lambdaFunction: reserveFlightFunction,
  outputPath: '$.Payload',
});

const reserveHotel = new tasks.LambdaInvoke(this, 'ReserveHotel', {
  lambdaFunction: reserveHotelFunction,
  outputPath: '$.Payload',
});

const processPayment = new tasks.LambdaInvoke(this, 'ProcessPayment', {
  lambdaFunction: processPaymentFunction,
  outputPath: '$.Payload',
});

// Compensating transactions
const cancelFlight = new tasks.LambdaInvoke(this, 'CancelFlight', {
  lambdaFunction: cancelFlightFunction,
});

const cancelHotel = new tasks.LambdaInvoke(this, 'CancelHotel', {
  lambdaFunction: cancelHotelFunction,
});

// Define saga with compensation
const definition = reserveFlight
  .next(reserveHotel)
  .next(processPayment)
  .addCatch(cancelHotel.next(cancelFlight), {
    resultPath: '$.error',
  });

new stepfunctions.StateMachine(this, 'BookingStateMachine', {
  definition,
  timeout: Duration.minutes(5),
});
```

### Pattern 5: Event Sourcing

Store events as source of truth:

```typescript
// Event store with DynamoDB
const eventStore = new dynamodb.Table(this, 'EventStore', {
  partitionKey: { name: 'aggregateId', type: dynamodb.AttributeType.STRING },
  sortKey: { name: 'version', type: dynamodb.AttributeType.NUMBER },
  stream: dynamodb.StreamViewType.NEW_IMAGE,
});

// Lambda function stores events
export const handleCommand = async (event: any) => {
  const { aggregateId, eventType, eventData } = event;

  // Get current version
  const items = await dynamodb.query({
    TableName: process.env.EVENT_STORE,
    KeyConditionExpression: 'aggregateId = :id',
    ExpressionAttributeValues: { ':id': aggregateId },
    ScanIndexForward: false,
    Limit: 1,
  });

  const nextVersion = items.Items?.[0]?.version + 1 || 1;

  // Append new event
  await dynamodb.putItem({
    TableName: process.env.EVENT_STORE,
    Item: {
      aggregateId,
      version: nextVersion,
      eventType,
      eventData,
      timestamp: Date.now(),
    },
  });
};

// Projections read from event stream
eventStore.grantStreamRead(projectionFunction);
```

## Serverless Architecture Patterns

### Pattern 1: API-Driven Microservices

REST APIs with Lambda backend:

```typescript
const api = new apigateway.RestApi(this, 'Api', {
  restApiName: 'microservices-api',
  deployOptions: {
    throttlingRateLimit: 1000,
    throttlingBurstLimit: 2000,
    tracingEnabled: true,
  },
});

// User service
const users = api.root.addResource('users');
users.addMethod('GET', new apigateway.LambdaIntegration(getUsersFunction));
users.addMethod('POST', new apigateway.LambdaIntegration(createUserFunction));

// Order service
const orders = api.root.addResource('orders');
orders.addMethod('GET', new apigateway.LambdaIntegration(getOrdersFunction));
orders.addMethod('POST', new apigateway.LambdaIntegration(createOrderFunction));
```

### Pattern 2: Stream Processing

Real-time data processing with Kinesis:

```typescript
const stream = new kinesis.Stream(this, 'DataStream', {
  shardCount: 2,
  retentionPeriod: Duration.days(7),
});

// Lambda processes stream records
new lambda.EventSourceMapping(this, 'StreamProcessor', {
  target: processFunction,
  eventSourceArn: stream.streamArn,
  batchSize: 100,
  maxBatchingWindow: Duration.seconds(5),
  parallelizationFactor: 10,
  startingPosition: lambda.StartingPosition.LATEST,
  retryAttempts: 3,
  bisectBatchOnError: true,
  onFailure: new lambdaDestinations.SqsDestination(dlq),
});
```

### Pattern 3: Async Task Processing

Background job processing:

```typescript
// SQS queue for tasks
const taskQueue = new sqs.Queue(this, 'TaskQueue', {
  visibilityTimeout: Duration.minutes(5),
  receiveMessageWaitTime: Duration.seconds(20), // Long polling
  deadLetterQueue: {
    queue: dlq,
    maxReceiveCount: 3,
  },
});

// Lambda worker processes tasks
const worker = new lambda.Function(this, 'TaskWorker', {
  // ... configuration
  reservedConcurrentExecutions: 10, // Control concurrency
});

new lambda.EventSourceMapping(this, 'TaskConsumer', {
  target: worker,
  eventSourceArn: taskQueue.queueArn,
  batchSize: 10,
  reportBatchItemFailures: true, // Partial batch failure handling
});
```

### Pattern 4: Scheduled Jobs

Periodic processing with EventBridge:

```typescript
// Daily cleanup job
new events.Rule(this, 'DailyCleanup', {
  schedule: events.Schedule.cron({ hour: '2', minute: '0' }),
  targets: [new targets.LambdaFunction(cleanupFunction)],
});

// Process every 5 minutes
new events.Rule(this, 'FrequentProcessing', {
  schedule: events.Schedule.rate(Duration.minutes(5)),
  targets: [new targets.LambdaFunction(processFunction)],
});
```

### Pattern 5: Webhook Processing

Handle external webhooks:

```typescript
// API Gateway endpoint for webhooks
const webhookApi = new apigateway.RestApi(this, 'WebhookApi', {
  restApiName: 'webhooks',
});

const webhook = webhookApi.root.addResource('webhook');
webhook.addMethod('POST', new apigateway.LambdaIntegration(webhookFunction, {
  proxy: true,
  timeout: Duration.seconds(29), // API Gateway max
}));

// Lambda handler validates and queues webhook
export const handler = async (event: APIGatewayProxyEvent) => {
  // Validate webhook signature
  const isValid = validateSignature(event.headers, event.body);
  if (!isValid) {
    return { statusCode: 401, body: 'Invalid signature' };
  }

  // Queue for async processing
  await sqs.sendMessage({
    QueueUrl: process.env.QUEUE_URL,
    MessageBody: event.body,
  });

  // Return immediately
  return { statusCode: 202, body: 'Accepted' };
};
```

## Best Practices

### Error Handling

**Implement comprehensive error handling**:

```typescript
export const handler = async (event: SQSEvent) => {
  const failures: SQSBatchItemFailure[] = [];

  for (const record of event.Records) {
    try {
      await processRecord(record);
    } catch (error) {
      console.error('Failed to process record:', record.messageId, error);
      failures.push({ itemIdentifier: record.messageId });
    }
  }

  // Return partial batch failures for retry
  return { batchItemFailures: failures };
};
```

### Dead Letter Queues

**Always configure DLQs for error handling**:

```typescript
const dlq = new sqs.Queue(this, 'DLQ', {
  retentionPeriod: Duration.days(14),
});

const queue = new sqs.Queue(this, 'Queue', {
  deadLetterQueue: {
    queue: dlq,
    maxReceiveCount: 3,
  },
});

// Monitor DLQ depth
new cloudwatch.Alarm(this, 'DLQAlarm', {
  metric: dlq.metricApproximateNumberOfMessagesVisible(),
  threshold: 1,
  evaluationPeriods: 1,
  alarmDescription: 'Messages in DLQ require attention',
});
```

### Observability

**Enable tracing and monitoring**:

```typescript
new NodejsFunction(this, 'Function', {
  entry: 'src/handler.ts',
  tracing: lambda.Tracing.ACTIVE, // X-Ray tracing
  environment: {
    POWERTOOLS_SERVICE_NAME: 'order-service',
    POWERTOOLS_METRICS_NAMESPACE: 'MyApp',
    LOG_LEVEL: 'INFO',
  },
});
```

## Using MCP Servers Effectively

### AWS Serverless MCP Usage

**Lifecycle management**:
- Initialize new serverless projects
- Generate SAM templates
- Deploy applications
- Test locally before deployment

### Lambda Tool MCP Usage

**Function execution**:
- Test Lambda functions directly
- Execute automation workflows
- Access private resources
- Validate integrations

### Step Functions MCP Usage

**Workflow orchestration**:
- Create state machines for complex workflows
- Execute distributed transactions
- Implement saga patterns
- Coordinate microservices

### SNS/SQS MCP Usage

**Messaging operations**:
- Test pub/sub patterns
- Send test messages to queues
- Validate event routing
- Debug message processing

## Additional Resources

This skill includes comprehensive reference documentation based on AWS best practices:

- **Serverless Patterns**: `references/serverless-patterns.md`
  - Core serverless architectures and API patterns
  - Data processing and integration patterns
  - Orchestration with Step Functions
  - Anti-patterns to avoid

- **Event-Driven Architecture Patterns**: `references/eda-patterns.md`
  - Event routing and processing patterns
  - Event sourcing and saga patterns
  - Idempotency and error handling
  - Message ordering and deduplication

- **Security Best Practices**: `references/security-best-practices.md`
  - Shared responsibility model
  - IAM least privilege patterns
  - Data protection and encryption
  - Network security with VPC

- **Observability Best Practices**: `references/observability-best-practices.md`
  - Three pillars: metrics, logs, traces
  - Structured logging with Lambda Powertools
  - X-Ray distributed tracing
  - CloudWatch alarms and dashboards

- **Performance Optimization**: `references/performance-optimization.md`
  - Cold start optimization techniques
  - Memory and CPU optimization
  - Package size reduction
  - Provisioned concurrency patterns

- **Deployment Best Practices**: `references/deployment-best-practices.md`
  - CI/CD pipeline design
  - Testing strategies (unit, integration, load)
  - Deployment strategies (canary, blue/green)
  - Rollback and safety mechanisms

**External Resources**:
- **AWS Well-Architected Serverless Lens**: https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/
- **ServerlessLand.com**: Pre-built serverless patterns
- **AWS Serverless Workshops**: https://serverlessland.com/learn?type=Workshops

For detailed implementation patterns, anti-patterns, and code examples, refer to the comprehensive references in the skill directory.
