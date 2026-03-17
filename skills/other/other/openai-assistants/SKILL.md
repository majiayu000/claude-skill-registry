---
name: openai-assistants
description: |
  Build stateful chatbots with OpenAI Assistants API v2 - Code Interpreter, File Search (10k files), Function Calling. Prevents 10 documented errors including vector store upload bugs, temperature parameter conflicts, memory leaks. Deprecated (sunset August 2026); use openai-responses for new projects.

  Use when: maintaining legacy chatbots, implementing RAG with vector stores, or troubleshooting thread errors, vector store delays, uploadAndPoll issues.
user-invocable: true
---

# OpenAI Assistants API v2

**Status**: Production Ready (⚠️ Deprecated - Sunset August 26, 2026)
**Package**: openai@6.16.0
**Last Updated**: 2026-01-21
**v1 Deprecated**: December 18, 2024
**v2 Sunset**: August 26, 2026 (migrate to Responses API)

---

## ⚠️ Deprecation Notice

**OpenAI is deprecating Assistants API in favor of [Responses API](../openai-responses/SKILL.md).**

**Timeline**: v1 deprecated Dec 18, 2024 | v2 sunset August 26, 2026

**Use this skill if**: Maintaining legacy apps or migrating existing code (12-18 month window)
**Don't use if**: Starting new projects (use `openai-responses` skill instead)

**Migration**: See `references/migration-to-responses.md`

---

## Quick Start

```bash
npm install openai@6.16.0
```

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// 1. Create assistant
const assistant = await openai.beta.assistants.create({
  name: "Math Tutor",
  instructions: "You are a math tutor. Use code interpreter for calculations.",
  tools: [{ type: "code_interpreter" }],
  model: "gpt-5",
});

// 2. Create thread
const thread = await openai.beta.threads.create();

// 3. Add message
await openai.beta.threads.messages.create(thread.id, {
  role: "user",
  content: "Solve: 3x + 11 = 14",
});

// 4. Run assistant
const run = await openai.beta.threads.runs.create(thread.id, {
  assistant_id: assistant.id,
});

// 5. Poll for completion
let status = await openai.beta.threads.runs.retrieve(thread.id, run.id);
while (status.status !== 'completed') {
  await new Promise(r => setTimeout(r, 1000));
  status = await openai.beta.threads.runs.retrieve(thread.id, run.id);
}

// 6. Get response
const messages = await openai.beta.threads.messages.list(thread.id);
console.log(messages.data[0].content[0].text.value);
```

---

## Core Concepts

**Four Main Objects:**

1. **Assistants**: Configured AI with instructions (max 256k chars in v2, was 32k in v1), model, tools, metadata
2. **Threads**: Conversation containers with persistent message history (max 100k messages)
3. **Messages**: User/assistant messages with optional file attachments
4. **Runs**: Async execution with states (queued, in_progress, requires_action, completed, failed, expired)

---

## Key API Patterns

### Assistants

```typescript
const assistant = await openai.beta.assistants.create({
  model: "gpt-5",
  instructions: "System prompt (max 256k chars in v2)",
  tools: [{ type: "code_interpreter" }, { type: "file_search" }],
  tool_resources: { file_search: { vector_store_ids: ["vs_123"] } },
});
```

**Key Limits**: 256k instruction chars (v2), 128 tools max, 16 metadata pairs

### Threads & Messages

```typescript
// Create thread with messages
const thread = await openai.beta.threads.create({
  messages: [{ role: "user", content: "Hello" }],
});

// Add message with attachments
await openai.beta.threads.messages.create(thread.id, {
  role: "user",
  content: "Analyze this",
  attachments: [{ file_id: "file_123", tools: [{ type: "code_interpreter" }] }],
});

// List messages
const msgs = await openai.beta.threads.messages.list(thread.id);
```

**Key Limits**: 100k messages per thread

---

### Runs

```typescript
// Create run with optional overrides
const run = await openai.beta.threads.runs.create(thread.id, {
  assistant_id: "asst_123",
  additional_messages: [{ role: "user", content: "Question" }],
  max_prompt_tokens: 1000,
  max_completion_tokens: 500,
});

// Poll until complete
let status = await openai.beta.threads.runs.retrieve(thread.id, run.id);
while (['queued', 'in_progress'].includes(status.status)) {
  await new Promise(r => setTimeout(r, 1000));
  status = await openai.beta.threads.runs.retrieve(thread.id, run.id);
}
```

**Run States**: `queued` → `in_progress` → `requires_action` (function calling) / `completed` / `failed` / `cancelled` / `expired` (10 min max)

---

### Streaming

```typescript
const stream = await openai.beta.threads.runs.stream(thread.id, { assistant_id });

for await (const event of stream) {
  if (event.event === 'thread.message.delta') {
    process.stdout.write(event.data.delta.content?.[0]?.text?.value || '');
  }
}
```

**Key Events**: `thread.run.created`, `thread.message.delta` (streaming content), `thread.run.step.delta` (tool progress), `thread.run.completed`, `thread.run.requires_action` (function calling)

---

## Tools

### Code Interpreter

Runs Python code in sandbox. Generates charts, processes files (CSV, JSON, PDF, images). Max 512MB per file.

```typescript
// Attach file to message
attachments: [{ file_id: "file_123", tools: [{ type: "code_interpreter" }] }]

// Access generated files
for (const content of message.content) {
  if (content.type === 'image_file') {
    const fileContent = await openai.files.content(content.image_file.file_id);
  }
}
```

### File Search (RAG)

Semantic search with vector stores. **10,000 files max** (v2, was 20 in v1). **Pricing**: $0.10/GB/day (1GB free).

```typescript
// Create vector store
const vs = await openai.beta.vectorStores.create({ name: "Docs" });
await openai.beta.vectorStores.files.create(vs.id, { file_id: "file_123" });

// Wait for indexing
let store = await openai.beta.vectorStores.retrieve(vs.id);
while (store.status === 'in_progress') {
  await new Promise(r => setTimeout(r, 2000));
  store = await openai.beta.vectorStores.retrieve(vs.id);
}

// Use in assistant
tool_resources: { file_search: { vector_store_ids: [vs.id] } }
```

**⚠️ Wait for `status: 'completed'` before using**

### Function Calling

Submit tool outputs when run.status === 'requires_action':

```typescript
if (run.status === 'requires_action') {
  const toolCalls = run.required_action.submit_tool_outputs.tool_calls;
  const outputs = toolCalls.map(tc => ({
    tool_call_id: tc.id,
    output: JSON.stringify(yourFunction(JSON.parse(tc.function.arguments))),
  }));

  run = await openai.beta.threads.runs.submitToolOutputs(thread.id, run.id, {
    tool_outputs: outputs,
  });
}
```

## File Formats

**Code Interpreter**: .c, .cpp, .csv, .docx, .html, .java, .json, .md, .pdf, .php, .pptx, .py, .rb, .tex, .txt, .css, .jpeg, .jpg, .js, .gif, .png, .tar, .ts, .xlsx, .xml, .zip (512MB max)

**File Search**: .c, .cpp, .docx, .html, .java, .json, .md, .pdf, .php, .pptx, .py, .rb, .tex, .txt, .css, .js, .ts, .go (512MB max)

---

## Known Issues

**1. Thread Already Has Active Run**
```
Error: 400 Can't add messages to thread_xxx while a run run_xxx is active.
```
**Fix**: Cancel active run first: `await openai.beta.threads.runs.cancel(threadId, runId)`

**2. Run Polling Timeout / Incomplete Status**
```
Error: OpenAIError: Final run has not been received
```
**Why It Happens**: Long-running tasks may exceed polling windows or finish with `incomplete` status
**Prevention**: Handle incomplete runs gracefully
```typescript
try {
  const stream = await openai.beta.threads.runs.stream(thread.id, { assistant_id });
  for await (const event of stream) {
    if (event.event === 'thread.message.delta') {
      process.stdout.write(event.data.delta.content?.[0]?.text?.value || '');
    }
  }
} catch (error) {
  if (error.message?.includes('Final run has not been received')) {
    // Run ended with 'incomplete' status - thread can continue
    const run = await openai.beta.threads.runs.retrieve(thread.id, runId);
    if (run.status === 'incomplete') {
      // Handle: prompt user to continue, reduce max_completion_tokens, etc.
    }
  }
}
```
**Source**: [GitHub Issues #945](https://github.com/openai/openai-node/issues/945), [#1306](https://github.com/openai/openai-node/issues/1306), [#1439](https://github.com/openai/openai-node/issues/1439)

**3. Vector Store Not Ready**
Using vector store before indexing completes.
**Fix**: Poll `vectorStores.retrieve()` until `status === 'completed'` (see File Search section)

**4. File Upload Format Issues**
Unsupported file formats cause silent failures.
**Fix**: Validate file extensions before upload (see File Formats section)

**5. Vector Store Upload Documentation Incorrect**
```
Error: No 'files' provided to process
```
**Why It Happens**: Official documentation shows incorrect usage of `uploadAndPoll`
**Prevention**: Wrap file streams in `{ files: [...] }` object
```typescript
// ✅ Correct
await openai.beta.vectorStores.fileBatches.uploadAndPoll(vectorStoreId, {
  files: fileStreams
});

// ❌ Wrong (shown in official docs)
await openai.beta.vectorStores.fileBatches.uploadAndPoll(vectorStoreId, fileStreams);
```
**Source**: [GitHub Issue #1337](https://github.com/openai/openai-node/issues/1337)

**6. Reasoning Models Reject Temperature Parameter**
```
Error: Unsupported parameter: 'temperature' is not supported with this model
```
**Why It Happens**: When updating assistant to o3-mini/o1-preview/o1-mini, old temperature settings persist
**Prevention**: Explicitly set temperature to `null`
```typescript
await openai.beta.assistants.update(assistantId, {
  model: 'o3-mini',
  reasoning_effort: 'medium',
  temperature: null,  // ✅ Must explicitly clear
  top_p: null
});
```
**Source**: [GitHub Issue #1318](https://github.com/openai/openai-node/issues/1318)

**7. uploadAndPoll Returns Vector Store ID Instead of Batch ID**
```
Error: Invalid 'batch_id': 'vs_...'. Expected an ID that begins with 'vsfb_'.
```
**Why It Happens**: `uploadAndPoll` returns vector store object instead of batch object
**Prevention**: Use alternative methods to get batch ID
```typescript
// Option 1: Use createAndPoll after separate upload
const batch = await openai.vectorStores.fileBatches.createAndPoll(
  vectorStoreId,
  { file_ids: uploadedFileIds }
);

// Option 2: List batches to find correct ID
const batches = await openai.vectorStores.fileBatches.list(vectorStoreId);
const batchId = batches.data[0].id; // starts with 'vsfb_'
```
**Source**: [GitHub Issue #1700](https://github.com/openai/openai-node/issues/1700)

**8. Vector Store File Delete Affects All Stores**
**Warning**: Deleting a file from one vector store removes it from ALL vector stores
```typescript
// ❌ This deletes file from VS_A, VS_B, AND VS_C
await openai.vectorStores.files.delete('VS_A', 'file-xxx');
```
**Why It Happens**: SDK or API bug - delete operation has global effect
**Prevention**: Avoid sharing files across multiple vector stores if selective deletion is needed
**Source**: [GitHub Issue #1710](https://github.com/openai/openai-node/issues/1710)

**9. Memory Leak in Large File Uploads (Community-sourced)**
**Source**: [GitHub Issue #1052](https://github.com/openai/openai-node/issues/1052) | **Status**: OPEN
**Impact**: ~44MB leaked per 22MB file upload in long-running servers
**Why It Happens**: When uploading large files from streams (S3, etc.) using `vectorStores.fileBatches.uploadAndPoll`, memory may not be released after upload completes
**Verified**: Maintainer acknowledged, reduced in v4.58.1 but not eliminated
**Workaround**: Monitor memory usage in long-lived servers; restart periodically or use separate worker processes

**10. Thread Already Has Active Run - Race Condition (Community-sourced)**
**Enhancement to Issue #1**: When canceling an active run, race conditions may occur if the run completes before cancellation
```typescript
async function createRunSafely(threadId: string, assistantId: string) {
  // Check for active runs first
  const runs = await openai.beta.threads.runs.list(threadId, { limit: 1 });
  const activeRun = runs.data.find(r =>
    ['queued', 'in_progress', 'requires_action'].includes(r.status)
  );

  if (activeRun) {
    try {
      await openai.beta.threads.runs.cancel(threadId, activeRun.id);

      // Wait for cancellation to complete
      let run = await openai.beta.threads.runs.retrieve(threadId, activeRun.id);
      while (run.status === 'cancelling') {
        await new Promise(r => setTimeout(r, 500));
        run = await openai.beta.threads.runs.retrieve(threadId, activeRun.id);
      }
    } catch (error) {
      // Ignore "already completed" errors - run finished naturally
      if (!error.message?.includes('completed')) throw error;
    }
  }

  return openai.beta.threads.runs.create(threadId, { assistant_id: assistantId });
}
```
**Source**: [OpenAI Community Forum](https://community.openai.com/t/error-running-thread-already-has-an-active-run/782118)

See `references/top-errors.md` for complete catalog.

## Relationship to Other Skills

**openai-api** (Chat Completions): Stateless, manual history, direct responses. Use for simple generation.

**openai-responses** (Responses API): ✅ **Recommended for new projects**. Better reasoning, modern MCP integration, active development.

**openai-assistants**: ⚠️ **Deprecated H1 2026**. Use for legacy apps only. Migration: `references/migration-to-responses.md`

---

## v1 to v2 Migration

**v1 deprecated**: Dec 18, 2024

**Key Changes**: `retrieval` → `file_search`, vector stores (10k files vs 20), 256k instructions (vs 32k), message-level file attachments

See `references/migration-from-v1.md`

---

**Templates**: `templates/basic-assistant.ts`, `code-interpreter-assistant.ts`, `file-search-assistant.ts`, `function-calling-assistant.ts`, `streaming-assistant.ts`

**References**: `references/top-errors.md`, `thread-lifecycle.md`, `vector-stores.md`, `migration-to-responses.md`, `migration-from-v1.md`

**Related Skills**: `openai-responses` (recommended), `openai-api`

---

**Last Updated**: 2026-01-21
**Package**: openai@6.16.0
**Status**: Production Ready (⚠️ Deprecated - Sunset August 26, 2026)
**Changes**: Added 6 new known issues (vector store upload bugs, o3-mini temperature, memory leak), enhanced streaming error handling
