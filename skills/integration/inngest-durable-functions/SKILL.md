---
name: inngest-durable-functions
description: Create and configure Inngest durable functions. Covers triggers (events, cron, invoke), step execution and memoization, idempotency, cancellation, error handling, retries, logging, and observability.
---

# Inngest Durable Functions

Master Inngest's durable execution model for building fault-tolerant, long-running workflows. This skill covers the complete lifecycle from triggers to error handling.

> **These skills are focused on TypeScript.** For Python or Go, refer to the [Inngest documentation](https://www.inngest.com/llms.txt) for language-specific guidance. Core concepts apply across all languages.

## Core Concepts You Need to Know

### **Durable Execution Model**

- **Each step** should encapsulate side-effects and non-deterministic code
- **Memoization** prevents re-execution of completed steps
- **State persistence** survives infrastructure failures
- **Automatic retries** with configurable retry count

### **Step Execution Flow**

```typescript
// ❌ BAD: Non-deterministic logic outside steps
async ({ event, step }) => {
  const timestamp = Date.now(); // This runs multiple times!

  const result = await step.run("process-data", () => {
    return processData(event.data);
  });
};

// ✅ GOOD: All non-deterministic logic in steps
async ({ event, step }) => {
  const result = await step.run("process-with-timestamp", () => {
    const timestamp = Date.now(); // Only runs once
    return processData(event.data, timestamp);
  });
};
```

## Function Limits

**Every Inngest function has these hard limits:**

- **Maximum 1,000 steps** per function run
- **Maximum 4MB** returned data for each step
- **Maximum 32MB** combined function run state including, event data, step output, and function output
- Each step = separate HTTP request (~50-100ms overhead)

If you're hitting these limits, break your function into smaller functions connected via `step.invoke()` or `step.sendEvent()`.

## When to Use Steps

**Always wrap in `step.run()`:**

- API calls and network requests
- Database reads and writes
- File I/O operations
- Any non-deterministic operation
- Anything you want retried independently on failure

**Never wrap in `step.run()`:**

- Pure calculations and data transformations
- Simple validation logic
- Deterministic operations with no side effects
- Logging (use outside steps)

## Function Creation

### Basic Function Structure

```typescript
const processOrder = inngest.createFunction(
  {
    id: "process-order", // Unique, never change this
    retries: 4, // Default: 4 retries per step
    concurrency: 10 // Max concurrent executions
  },
  { event: "order/created" }, // Trigger
  async ({ event, step }) => {
    // Your durable workflow
  }
);
```

### **Step IDs and Memoization**

```typescript
// Step IDs can be reused - Inngest handles counters automatically
const data = await step.run("fetch-data", () => fetchUserData());
const more = await step.run("fetch-data", () => fetchOrderData()); // Different execution

// Use descriptive IDs for clarity
await step.run("validate-payment", () => validatePayment(event.data.paymentId));
await step.run("charge-customer", () => chargeCustomer(event.data));
await step.run("send-confirmation", () => sendEmail(event.data.email));
```

## Triggers and Events

### **Event Triggers**

```typescript
// Single event trigger
{ event: "user/signup" }

// Event with conditional filter
{
  event: "user/action",
  if: 'event.data.action == "purchase" && event.data.amount > 100'
}

// Multiple triggers (up to 10)
[
  { event: "user/signup" },
  { event: "user/login", if: 'event.data.firstLogin == true' },
  { cron: "0 9 * * *" } // Daily at 9 AM
]
```

### **Cron Triggers**

```typescript
// Basic cron
{
  cron: "0 */6 * * *";
} // Every 6 hours

// With timezone
{
  cron: "TZ=Europe/Paris 0 12 * * 5";
} // Fridays at noon Paris time

// Combine with events
[
  { event: "manual/report.requested" },
  { cron: "0 0 * * 0" } // Weekly on Sunday
];
```

### **Function Invocation**

```typescript
// Invoke another function as a step
const result = await step.invoke("generate-report", {
  function: generateReportFunction,
  data: { userId: event.data.userId }
});

// Use returned data
await step.run("process-report", () => {
  return processReport(result);
});
```

## Idempotency Strategies

### **Event-Level Idempotency (Producer Side)**

```typescript
// Prevent duplicate events with custom ID
await inngest.send({
  id: `checkout-completed-${cartId}`, // 24-hour deduplication
  name: "cart/checkout.completed",
  data: { cartId, email: "user@example.com" }
});
```

### **Function-Level Idempotency (Consumer Side)**

```typescript
const sendEmail = inngest.createFunction(
  {
    id: "send-checkout-email",
    // Only run once per cartId per 24 hours
    idempotency: "event.data.cartId"
  },
  { event: "cart/checkout.completed" },
  async ({ event, step }) => {
    // This function won't run twice for same cartId
  }
);

// Complex idempotency keys
const processUserAction = inngest.createFunction(
  {
    id: "process-user-action",
    // Unique per user + organization combination
    idempotency: 'event.data.userId + "-" + event.data.organizationId'
  },
  { event: "user/action.performed" },
  async ({ event, step }) => {
    /* ... */
  }
);
```

## Cancellation Patterns

### **Event-Based Cancellation**

In expressions, `event` = the **original** triggering event, `async` = the **new** event being matched. See [Expression Syntax Reference](../references/expressions.md) for full details.

```typescript
const processOrder = inngest.createFunction(
  {
    id: "process-order",
    cancelOn: [
      {
        event: "order/cancelled",
        if: "event.data.orderId == async.data.orderId"
      }
    ]
  },
  { event: "order/created" },
  async ({ event, step }) => {
    await step.sleepUntil("wait-for-payment", event.data.paymentDue);
    // Will be cancelled if order/cancelled event received
    await step.run("charge-payment", () => processPayment(event.data));
  }
);
```

### **Timeout Cancellation**

```typescript
const processWithTimeout = inngest.createFunction(
  {
    id: "process-with-timeout",
    timeouts: {
      start: "5m", // Cancel if not started within 5 minutes
      finish: "30m" // Cancel if not finished within 30 minutes
    }
  },
  { event: "long/process.requested" },
  async ({ event, step }) => {
    /* ... */
  }
);
```

### **Handling Cancellation Cleanup**

```typescript
// Listen for cancellation events
const cleanupCancelled = inngest.createFunction(
  { id: "cleanup-cancelled-process" },
  { event: "inngest/function.cancelled" },
  async ({ event, step }) => {
    if (event.data.function_id === "process-order") {
      await step.run("cleanup-resources", () => {
        return cleanupOrderResources(event.data.run_id);
      });
    }
  }
);
```

## Error Handling and Retries

### **Default Retry Behavior**

- **5 total attempts** (1 initial + 4 retries) per step
- **Exponential backoff** with jitter
- **Independent retry counters** per step

### **Custom Retry Configuration**

```typescript
const reliableFunction = inngest.createFunction(
  {
    id: "reliable-function",
    retries: 10 // Up to 10 retries per step
  },
  { event: "critical/task" },
  async ({ event, step, attempt }) => {
    // `attempt` is the function-level attempt counter (0-indexed)
    // It tracks retries for the currently executing step, not the overall function
    if (attempt > 5) {
      // Different logic for later attempts of the current step
    }
  }
);
```

### **Non-Retriable Errors**

Prevent retries for code that won't succeed upon retry.

```typescript
import { NonRetriableError } from "inngest";

const processUser = inngest.createFunction(
  { id: "process-user" },
  { event: "user/process.requested" },
  async ({ event, step }) => {
    const user = await step.run("fetch-user", async () => {
      const user = await db.users.findOne(event.data.userId);

      if (!user) {
        // Don't retry - user doesn't exist
        throw new NonRetriableError("User not found, stopping execution");
      }

      return user;
    });

    // Continue processing...
  }
);
```

### **Custom Retry Timing**

```typescript
import { RetryAfterError } from "inngest";

const respectRateLimit = inngest.createFunction(
  { id: "api-call" },
  { event: "api/call.requested" },
  async ({ event, step }) => {
    await step.run("call-api", async () => {
      const response = await externalAPI.call(event.data);

      if (response.status === 429) {
        // Retry after specific time from API
        const retryAfter = response.headers["retry-after"];
        throw new RetryAfterError("Rate limited", `${retryAfter}s`);
      }

      return response.data;
    });
  }
);
```

## Logging Best Practices

### **Proper Logging Setup**

```typescript
import winston from "winston";

// Configure logger
const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [new winston.transports.Console()]
});

const inngest = new Inngest({
  id: "my-app",
  logger // Pass logger to client
});
```

### **Function Logging Patterns**

```typescript
const processData = inngest.createFunction(
  { id: "process-data" },
  { event: "data/process.requested" },
  async ({ event, step, logger }) => {
    // ✅ GOOD: Log inside steps to avoid duplicates
    const result = await step.run("fetch-data", async () => {
      logger.info("Fetching data for user", { userId: event.data.userId });
      return await fetchUserData(event.data.userId);
    });

    // ❌ AVOID: Logging outside steps can duplicate
    // logger.info("Processing complete"); // This could run multiple times!

    await step.run("log-completion", async () => {
      logger.info("Processing complete", { resultCount: result.length });
    });
  }
);
```

## Performance Optimization

### **Checkpointing**

```typescript
// Enable checkpointing for lower latency
const realTimeFunction = inngest.createFunction(
  {
    id: "real-time-function",
    checkpointing: {
      maxRuntime: "5m", // Max continuous execution time
      bufferedSteps: 2, // Buffer 2 steps before checkpointing
      maxInterval: "10s" // Max wait before checkpoint
    }
  },
  { event: "realtime/process" },
  async ({ event, step }) => {
    // Steps execute immediately with periodic checkpointing
    const result1 = await step.run("step-1", () => process1(event.data));
    const result2 = await step.run("step-2", () => process2(result1));
    return { result2 };
  }
);
```

## Advanced Patterns

### **Conditional Step Execution**

```typescript
const conditionalProcess = inngest.createFunction(
  { id: "conditional-process" },
  { event: "process/conditional" },
  async ({ event, step }) => {
    const userData = await step.run("fetch-user", () => {
      return getUserData(event.data.userId);
    });

    // Conditional step execution
    if (userData.isPremium) {
      await step.run("premium-processing", () => {
        return processPremiumFeatures(userData);
      });
    }

    // Always runs
    await step.run("standard-processing", () => {
      return processStandardFeatures(userData);
    });
  }
);
```

### **Error Recovery Patterns**

```typescript
const robustProcess = inngest.createFunction(
  { id: "robust-process" },
  { event: "process/robust" },
  async ({ event, step }) => {
    let primaryResult;

    try {
      primaryResult = await step.run("primary-service", () => {
        return callPrimaryService(event.data);
      });
    } catch (error) {
      // Fallback to secondary service
      primaryResult = await step.run("fallback-service", () => {
        return callSecondaryService(event.data);
      });
    }

    return { result: primaryResult };
  }
);
```

## Common Mistakes to Avoid

1. **❌ Non-deterministic code outside steps**
2. **❌ Database calls outside steps**
3. **❌ Logging outside steps (causes duplicates)**
4. **❌ Changing step IDs after deployment**
5. **❌ Not handling NonRetriableError cases**
6. **❌ Ignoring idempotency for critical functions**

## Next Steps

- See **inngest-steps** for detailed step method reference
- See [references/step-execution.md](references/step-execution.md) for detailed step patterns
- See [references/error-handling.md](references/error-handling.md) for comprehensive error strategies
- See [references/observability.md](references/observability.md) for monitoring and tracing setup
- See [references/checkpointing.md](references/checkpointing.md) for performance optimization details

---

_This skill covers Inngest's durable function patterns. For event sending and webhook handling, see the `inngest-events` skill._
