---
name: using-workflows
description: Create and run durable workflows with steps, streaming, and agent execution. Covers starting, resuming, and persisting workflow results.
---

# Working with Workflows

Create and run durable workflows with steps, streaming, and agent execution. Covers starting, resuming, and persisting workflow results.

## Working with Workflows

Create and run durable workflows with steps, streaming, and agent execution. Covers starting, resuming, and persisting workflow results.

**See:**

- Resource: `using-workflows` in Fullstack Recipes
- URL: https://fullstackrecipes.com/recipes/using-workflows

---

### Workflow Folder Structure

Each workflow has its own subfolder in `src/workflows/`:

```
src/workflows/
  steps/           # Shared step functions
    stream.ts      # UI message stream helpers
  chat/
    index.ts       # Workflow orchestration function ("use workflow")
    steps/         # Workflow-specific steps ("use step")
      history.ts
      logger.ts
      name-chat.ts
    types.ts       # Workflow-specific types
```

- **`workflows/steps/`** - Shared step functions reusable across workflows (e.g., stream helpers).
- **`index.ts`** - Contains the main workflow function with the `"use workflow"` directive. Orchestrates the workflow by calling step functions.
- **`steps/`** - Contains individual step functions with the `"use step"` directive. Each step is a durable checkpoint.
- **`types.ts`** - Type definitions for the workflow's UI messages.

---

### Creating a Workflow

Define workflows with the `"use workflow"` directive:

```typescript
// src/workflows/chat/index.ts
import { getWorkflowMetadata, getWritable } from "workflow";
import { startStream, finishStream } from "../steps/stream";
import { chatAgent } from "@/lib/ai/chat-agent";

export async function chatWorkflow({ chatId, userMessage }) {
  "use workflow";

  const { workflowRunId } = getWorkflowMetadata();

  // Persist user message
  await persistUserMessage({ chatId, message: userMessage });

  // Create assistant placeholder with runId for resumption
  const messageId = await createAssistantMessage({
    chatId,
    runId: workflowRunId,
  });

  // Get message history
  const history = await getMessageHistory(chatId);

  // Start the UI message stream
  await startStream(messageId);

  // Run agent with streaming
  const { parts } = await chatAgent.run(history, {
    maxSteps: 10,
    writable: getWritable(),
  });

  // Persist and finalize
  await persistMessageParts({ chatId, messageId, parts });

  // Finish the UI message stream
  await finishStream();

  await removeRunId(messageId);
}
```

### Starting a Workflow

Use the `start` function from `workflow/api`:

```typescript
import { start } from "workflow/api";
import { chatWorkflow } from "@/workflows/chat";

const run = await start(chatWorkflow, [{ chatId, userMessage }]);

// run.runId - unique identifier for this run
// run.readable - stream of UI message chunks
```

### Resuming a Workflow Stream

Use `getRun` to reconnect to an in-progress or completed workflow:

```typescript
import { getRun } from "workflow/api";

const run = await getRun(runId);
const readable = await run.getReadable({ startIndex });
```

### Using Steps

Steps are durable checkpoints that persist their results:

```typescript
async function getMessageHistory(chatId: string) {
  "use step";

  const dbMessages = await getChatMessages(chatId);
  return convertDbMessagesToUIMessages(dbMessages);
}
```

---

### Streaming UIMessageChunks

When streaming `UIMessageChunk` responses to clients (e.g., chat messages), you must signal the start and end of the stream. This is required for proper stream framing with `WorkflowChatTransport`.

**Always call `startStream()` before `agent.run()` and `finishStream()` after:**

```typescript
import { getWritable } from "workflow";
import { startStream, finishStream } from "../steps/stream";
import { chatAgent } from "@/lib/ai/chat-agent";

export async function chatWorkflow({ chatId, messageId }) {
  "use workflow";

  const history = await getMessageHistory(chatId);

  // Signal stream start with the message ID
  await startStream(messageId);

  // Run agent - streams UIMessageChunks to the client
  const { parts } = await chatAgent.run(history, {
    maxSteps: 10,
    writable: getWritable(),
  });

  await persistMessageParts({ chatId, messageId, parts });

  // Signal stream end and close the writable
  await finishStream();
}
```

The stream step functions write `UIMessageChunk` messages:

- `startStream(messageId)` - Writes `{ type: "start", messageId }` to signal a new message
- `finishStream()` - Writes `{ type: "finish", finishReason: "stop" }` and closes the stream

Without these signals, the client's `WorkflowChatTransport` cannot properly parse the streamed response.

---

### Getting Workflow Metadata

Access the current run's metadata:

```typescript
import { getWorkflowMetadata } from "workflow";

export async function chatWorkflow({ chatId }) {
  "use workflow";

  const { workflowRunId } = getWorkflowMetadata();

  // Store runId for resumption
  await createAssistantMessage({ chatId, runId: workflowRunId });
}
```

### Workflow-Safe Logging

The workflow runtime doesn't support Node.js modules. Wrap logger calls in steps:

```typescript
// src/workflows/chat/steps/logger.ts
import { logger } from "@/lib/logging/logger";

export async function log(
  level: "info" | "warn" | "error" | "debug",
  message: string,
  data?: Record<string, unknown>,
): Promise<void> {
  "use step";

  if (data) {
    logger[level](data, message);
  } else {
    logger[level](message);
  }
}
```

### Running Agents in Workflows

Use the custom `Agent` class for full streaming control:

```typescript
import { getWritable } from "workflow";
import { startStream, finishStream } from "../steps/stream";
import { chatAgent } from "@/lib/ai/chat-agent";

export async function chatWorkflow({ chatId, userMessage }) {
  "use workflow";

  const messageId = await createAssistantMessage({ chatId, runId });
  const history = await getMessageHistory(chatId);

  await startStream(messageId);

  const { parts } = await chatAgent.run(history, {
    maxSteps: 10,
    writable: getWritable(),
  });

  await persistMessageParts({ chatId, messageId, parts });
  await finishStream();
}
```

### Persisting Workflow Results

Save agent output using step functions. The `assertChatAgentParts` function validates that generic `UIMessage["parts"]` (returned by agents) match your application's specific tool and data types:

```typescript
// src/workflows/chat/steps/history.ts
import type { UIMessage } from "ai";
import { insertMessageParts } from "@/lib/chat/queries";
import { assertChatAgentParts, type ChatAgentUIMessage } from "../types";

export async function persistMessageParts({
  chatId,
  messageId,
  parts,
}: {
  chatId: string;
  messageId: string;
  parts: UIMessage["parts"];
}): Promise<void> {
  "use step";

  assertChatAgentParts(parts);

  await insertMessageParts(chatId, messageId, parts);

  // Update chat timestamp
  await db
    .update(chats)
    .set({ updatedAt: new Date() })
    .where(eq(chats.id, chatId));
}
```

---

## References

- [Workflow Development Kit](https://useworkflow.dev/docs)
- [Workflow API Reference](https://useworkflow.dev/docs/api-reference)
