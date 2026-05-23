---
name: n8n-ai-automation
description: World-class expert n8n workflow automation specialist with focus on AI integrations, webhooks, API connections, and building intelligent automation workflows at enterprise scale. Use when creating n8n workflows, integrating AI services, setting up webhooks, or building production-grade automation solutions with n8n.
---

# n8n AI Automation Expert - World-Class Edition

## Project Context: DriverConnect (eddication.io)

**IMPORTANT**: n8n is used for workflow automation and notification systems.

### Current n8n Integration

**Planned Use Cases**:
- Job assignment notifications to drivers
- Alert dispatch for exceptions (GPS offline, late check-in)
- Daily report generation and delivery
- Data sync between Supabase and Google Sheets
- Driver performance score calculation (scheduled)

### Example Workflow: Job Notification

```json
{
  "nodes": [
    {
      "name": "Supabase Trigger",
      "type": "n8n-nodes-base.supabaseTrigger",
      "parameters": {
        "table": "jobdata",
        "event": "INSERT",
        "condition": "status = 'PENDING'"
      }
    },
    {
      "name": "Filter by Driver",
      "type": "n8n-nodes-base.filter",
      "parameters": {
        "conditions": {
          "string": [{ "field1": "assigned_driver", "operation": "isNotEmpty" }]
        }
      }
    },
    {
      "name": "LINE Notify",
      "type": "n8n-nodes-base.lineNotify",
      "parameters": {
        "message": "=New job: {{ $json.reference }}\nCustomer: {{ $json.customer }}"
      }
    }
  ]
}
```

### Webhook Endpoints

**Edge Functions → n8n**:
- `supabase/functions/webhook/` - Relay events to n8n
- Handles: job_created, driver_checkin, exception_detected

---

## Overview

You are a world-class expert in n8n workflow automation with deep expertise in AI integrations, enterprise-grade architecture, and production-ready solutions. You design scalable, maintainable, and robust automation systems that leverage AI capabilities while following industry best practices for security, performance, and reliability.

---

# Philosophy & Principles

## Core Principles
1. **Idempotency First** - Workflows should be safe to retry
2. **Fail Gracefully** - Always handle errors appropriately
3. **Security by Design** - Never expose credentials or sensitive data
4. **Performance Matters** - Optimize for throughput and latency
5. **Observability** - Make workflows debuggable and monitorable
6. **Scalability** - Design for growth from day one

## Code of Conduct
- **Always validate inputs** from external sources
- **Never commit secrets** to version control
- **Use environment variables** for configuration
- **Implement proper error handling** with meaningful messages
- **Add comments** for complex logic
- **Test thoroughly** before production deployment

---

# Architecture Patterns

## Enterprise Workflow Architecture

### Layered Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Trigger Layer                         │
│  Webhooks | Schedules | Events | Webhooks | Polling    │
├─────────────────────────────────────────────────────────┤
│                  Validation Layer                        │
│  Input Validation | Schema Validation | Sanitization   │
├─────────────────────────────────────────────────────────┤
│                  Transformation Layer                    │
│  Data Mapping | Format Conversion | Enrichment         │
├─────────────────────────────────────────────────────────┤
│                   Business Logic Layer                   │
│  AI Processing | Decisions | Routing | Calculations    │
├─────────────────────────────────────────────────────────┤
│                  Integration Layer                       │
│  External APIs | Databases | Services | Queues         │
├─────────────────────────────────────────────────────────┤
│                   Output Layer                           │
│  Responses | Notifications | Storage | Logging         │
└─────────────────────────────────────────────────────────┘
```

### Micro-Workflow Pattern
Break complex workflows into smaller, reusable sub-workflows:

```javascript
// Main workflow
Trigger → Validate → Execute Sub-Workflow → Aggregate → Respond

// Sub-workflow (called via Execute Workflow node)
Input → Process → Return Result
```

### Event-Driven Architecture
```
Producer Workflow → Queue/Topic → Consumer Workflow(s)
                                    ↓
                          Consumer Workflow 2
                                    ↓
                          Consumer Workflow 3
```

---

# Node Types Deep Dive

## Trigger Nodes

### Webhook Trigger
```yaml
Production Best Practices:
  - Use HTTPS only
  - Verify authentication (API keys, JWT, OAuth)
  - Rate limit at the gateway level
  - Return immediately, process asynchronously
  - Validate request schema

Authentication Methods:
  - Header-based API Key: X-API-Key
  - JWT Bearer tokens
  - HMAC signature verification
  - OAuth 2.0
```

### Schedule Trigger (Cron)
```yaml
Cron Expressions:
  # Every 5 minutes
  */5 * * * *

  # Every day at 9 AM UTC
  0 9 * * *

  # Every Monday at 8 AM
  0 8 * * 1

  # First day of every month
  0 0 1 * *

Best Practices:
  - Use UTC for all schedules
  - Avoid overlapping executions with proper locking
  - Consider timezone for local business hours
  - Add jitter for distributed systems
```

### Event Triggers
```yaml
Available Event Triggers:
  - Email Trigger (IMAP/POP3)
  - MQTT Trigger
  - Redis Trigger
  - RabbitMQ Trigger
  - Kafka Trigger
  - S3 Trigger
```

## Action Nodes

### HTTP Request Node (Critical)
```yaml
Advanced Configuration:
  Authentication:
    - None
    - Generic Credential Type (Header-based)
    - HTTP Basic Auth
    - Digest Auth
    - OAuth1
    - OAuth2 (Implicit, Authorization Code, Client Credentials)
    - Custom Auth

  Request Options:
    - Follow Redirects: true/false
    - Proxy Configuration
    - Timeout: 30000ms (default)
    - Response Format: JSON, File, Text

  Retry Strategy:
    - Linear backoff
    - Exponential backoff with jitter
    - Max retries: 3-5
    - Retry on: 5xx errors, 429 (rate limit)

Rate Limiting Patterns:
  Split In Batches → Configure batch size
  Wait node with {{ $json.remaining }}
  Error workflow for 429 handling
```

### Code Node (JavaScript)
```javascript
// ============ ADVANCED PATTERNS ============

// 1. Error Handling in Code Nodes
try {
  const result = process($json);
  return { json: result };
} catch (error) {
  // Return error that can be caught by IF node
  return {
    json: {
      error: true,
      message: error.message,
      stack: error.stack
    }
  };
}

// 2. Data Validation
function validateUser(user) {
  const errors = [];

  if (!user.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(user.email)) {
    errors.push('Invalid email');
  }

  if (!user.name || user.name.length < 2) {
    errors.push('Name too short');
  }

  if (errors.length > 0) {
    throw new Error(`Validation failed: ${errors.join(', ')}`);
  }

  return user;
}

return { json: validateUser($json) };

// 3. External Library Import (Danger Mode OFF)
// Use native APIs and built-in modules
const crypto = require('crypto');

function generateSignature(secret, data) {
  return crypto
    .createHmac('sha256', secret)
    .update(JSON.stringify(data))
    .digest('hex');
}

return { json: { signature: generateSignature($env.WEBHOOK_SECRET, $json) } };

// 4. Complex Data Transformation
const items = $input.all();

// Group by key
const grouped = items.reduce((acc, item) => {
  const key = item.json.category;
  if (!acc[key]) acc[key] = [];
  acc[key].push(item.json);
  return acc;
}, {});

// Transform to array
return Object.entries(grouped).map(([category, items]) => ({
  json: { category, count: items.length, items }
}));

// 5. Async Operations (Promise.all)
const urls = $json.urls.map(url => fetch(url).then(r => r.json()));

const results = await Promise.allSettled(urls);

return {
  json: {
    successful: results.filter(r => r.status === 'fulfilled').map(r => r.value),
    failed: results.filter(r => r.status === 'rejected').map(r => r.reason)
  }
};

// 6. Environment-based configuration
const config = {
  apiUrl: $env.API_URL || 'https://api.example.com',
  timeout: parseInt($env.TIMEOUT) || 30000,
  retries: parseInt($env.RETRIES) || 3
};

// 7. Caching pattern using static variables
// Note: This persists within the same execution only
function getCachedData(key, ttl = 60000) {
  const now = Date.now();
  if (getCachedData.cache[key] && now - getCachedData.cache[key].timestamp < ttl) {
    return getCachedData.cache[key].data;
  }
  return null;
}
getCachedData.cache = {};

function setCachedData(key, data) {
  getCachedData.cache[key] = { data, timestamp: Date.now() };
}

// 8. Date/Time utilities
const now = new Date();
const timezone = $env.TIMEZONE || 'UTC';

function formatDate(date, format = 'ISO') {
  const pad = n => n.toString().padStart(2, '0');

  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());
  const seconds = pad(date.getSeconds());

  switch (format) {
    case 'ISO':
      return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}Z`;
    case 'date':
      return `${year}-${month}-${day}`;
    case 'time':
      return `${hours}:${minutes}:${seconds}`;
    case 'timestamp':
      return date.getTime();
    default:
      return date.toISOString();
  }
}

return { json: { timestamp: formatDate(now), date: formatDate(now, 'date') } };

// 9. Custom error responses
class WorkflowError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.code = code;
    this.details = details;
    this.name = 'WorkflowError';
  }
}

// Usage
if ($json.amount <= 0) {
  throw new WorkflowError('INVALID_AMOUNT', 'Amount must be positive', { amount: $json.amount });
}

// 10. Streaming data processing
function* processDataChunk(data, chunkSize) {
  for (let i = 0; i < data.length; i += chunkSize) {
    yield data.slice(i, i + chunkSize);
  }
}

const largeArray = $json.largeArray;
const chunks = [...processDataChunk(largeArray, 100)];

return chunks.map(chunk => ({ json: { chunk } }));
```

### Switch/IF Nodes
```javascript
// Condition Builder Patterns

// 1. Multi-condition routing (Switch Node)
// Route by status field
Routes:
  - Condition: {{ $json.status === "active" }}
    Label: Active Users
  - Condition: {{ $json.status === "pending" }}
    Label: Pending Users
  - Condition: {{ $json.status === "suspended" }}
    Label: Suspended Users
  - Default Route

// 2. Complex boolean logic
// Advanced expression syntax
{{ $json.age >= 18 && $json.country === "US" }}
{{ ($json.type === "premium" || $json.type === "vip") && $json.subscriptionActive }}
{{ $json.items.length > 0 && $json.items.every(i => i.available) }}

// 3. Type checking
{{ typeof $json.value === "string" && $json.value.length > 0 }}
{{ Array.isArray($json.items) }}
{{ $json.timestamp instanceof Date || !isNaN(new Date($json.timestamp)) }}

// 4. Null/undefined handling
{{ $json.field != null }}  // Checks for both null and undefined
{{ $json.field ?? "default" }}  // Nullish coalescing
{{ $json.field?.nested?.property }}  // Optional chaining
```

### Merge Node Strategies
```yaml
1. Append (Default):
   - Combines all items into one array
   - Preserves order from both inputs
   - Use for: Combining results from parallel branches

2. Merge by Index:
   - Combines items at the same index
   - Requires equal number of items in both inputs
   - Use for: Pairing related data from different sources

3. Merge by Key (Advanced):
   - Combines items based on a common field value
   - Like SQL JOIN operation
   - Use for: Enriching data with additional information

4. Wait Strategy (for async branches):
   - Waits for all branches to complete
   - Combines results when ready
   - Use for: Parallel independent operations
```

### Split In Batches Node
```yaml
Configuration:
  Batch Size: 100 (adjust based on API limits)
  Options:
    Reset: false (don't reset between workflow executions)

Best Practices:
  - Always use with APIs that have rate limits
  - Configure based on actual API documentation
  - Add Wait node after if needed for rate limiting
  - Handle partial failures gracefully

Pattern for Rate-Limited APIs:
  Trigger → Split In Batches → HTTP Request → Wait → Merge
                ↓
         Error Workflow (on 429)
```

---

# AI Integration Mastery

## OpenAI Advanced Patterns

### GPT-4 Turbo / GPT-4o Configuration
```javascript
{
  "model": "gpt-4o",
  "temperature": 0.7,        // 0 = deterministic, 1 = creative
  "maxTokens": 4096,         // Maximum response length
  "topP": 0.9,              // Nucleus sampling
  "frequencyPenalty": 0,     // -2 to 2
  "presencePenalty": 0,      // -2 to 2
  "seed": 42                 // For reproducible outputs
}
```

### Structured Outputs (Function Calling)
```javascript
// Define function schema
const functions = [
  {
    name: "extract_contact_info",
    description: "Extract contact information from text",
    parameters: {
      type: "object",
      properties: {
        name: { type: "string", description: "Full name" },
        email: { type: "string", format: "email" },
        phone: { type: "string" },
        company: { type: "string" }
      },
      required: ["name", "email"]
    }
  },
  {
    name: "analyze_sentiment",
    description: "Analyze the sentiment of text",
    parameters: {
      type: "object",
      properties: {
        sentiment: { type: "string", enum: ["positive", "negative", "neutral"] },
        confidence: { type: "number", minimum: 0, maximum: 1 },
        keyPoints: { type: "array", items: { type: "string" } }
      },
      required: ["sentiment", "confidence"]
    }
  }
];

// Handle function call response
// Response format: { function_call: { name, arguments } }
```

### JSON Mode
```javascript
{
  "model": "gpt-4o",
  "response_format": { "type": "json_object" },
  "messages": [
    {
      "role": "system",
      "content": "You must respond with valid JSON only. No markdown, no explanation."
    }
  ]
}
```

### Vision API (Image Analysis)
```javascript
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Describe this image in detail."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "{{ $json.imageUrl }}",
            "detail": "high"  // or "low" for faster processing
          }
        }
      ]
    }
  ]
}
```

### Streaming Responses
```javascript
// For real-time chat applications
{
  "model": "gpt-4o",
  "stream": true
}

// Handle streaming events
// SSE format: data: {"choices":[{"delta":{"content":"..."}}]}
```

### Token Optimization
```javascript
// Reduce token usage while maintaining quality

// 1. Use system messages efficiently
const systemMessage = `
You are a customer service assistant.
Rules:
- Be concise
- Use markdown
- Respond in {{ $json.language }}
`;

// 2. Truncate context while preserving meaning
function truncateContext(messages, maxTokens = 3000) {
  // Estimate tokens (roughly 4 chars per token)
  const maxChars = maxTokens * 4;
  let totalChars = 0;
  const result = [];

  for (const msg of messages.reverse()) {
    const msgChars = msg.content.length;
    if (totalChars + msgChars > maxChars) break;
    result.unshift(msg);
    totalChars += msgChars;
  }

  return result;
}

// 3. Use compression for repeated context
function compressContext(items) {
  // Instead of passing full items, pass summary
  return {
    count: items.length,
    categories: [...new Set(items.map(i => i.category))],
    totalValue: items.reduce((sum, i) => sum + i.value, 0),
    sample: items.slice(0, 3)
  };
}
```

## Anthropic Claude Advanced

### Claude 3.5 Sonnet (Recommended)
```javascript
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 8192,
  "temperature": 0.7,
  "messages": [
    {
      "role": "user",
      "content": "{{ $json.prompt }}"
    }
  ]
}
```

### Claude with Tools (Function Calling)
```javascript
{
  "model": "claude-3-5-sonnet-20241022",
  "tools": [
    {
      "name": "get_weather",
      "description": "Get weather information",
      "input_schema": {
        "type": "object",
        "properties": {
          "location": { "type": "string" },
          "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
        },
        "required": ["location"]
      }
    }
  ]
}
```

### Claude Vision
```javascript
{
  "model": "claude-3-5-sonnet-20241022",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": "{{ $json.base64Image }}"
          }
        },
        {
          "type": "text",
          "text": "Analyze this image"
        }
      ]
    }
  ]
}
```

### Extended Thinking (Claude 3.5 Sonnet)
```javascript
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 8192,
  "thinking": {
    "type": "enabled",
    "budget_tokens": 16000
  }
}
```

## LangChain Node Patterns

### Vector Store RAG
```javascript
// 1. Setup Vector Store
{
  "vectorStore": "pinecone", // or weaviate, pgvector, qdrant
  "embeddings": {
    "model": "text-embedding-3-small",
    "dimensions": 1536
  }
}

// 2. Ingest documents
Workflow:
  HTTP Request (fetch docs) → Split Text → Embed → Store

// 3. Query with RAG
Workflow:
  User Query → Embed → Semantic Search → AI Agent → Response
```

### AI Agent Node
```javascript
{
  "agentType": "openai-functions",
  "verbose": true,
  "returnValues": ["output"],
  "maxIterations": 5,
  "earlyStoppingMethod": "generate",
  "tools": [
    {
      "name": "search",
      "description": "Search the knowledge base",
      "func": "node:Search Tool"
    },
    {
      "name": "calculator",
      "description": "Perform calculations",
      "func": "node:Code"
    }
  ]
}
```

---

# Production Workflows

## Error Handling Strategies

### Multi-Layer Error Handling
```
┌────────────────────────────────────────────────────────┐
│ Layer 1: Node-level                                    │
│   - Continue On Fail                                   │
│   - Retry on Error                                     │
│   - Always Output Data                                 │
├────────────────────────────────────────────────────────┤
│ Layer 2: Workflow-level                                │
│   - Error Workflow Trigger                             │
│   - Execute on Error                                   │
├────────────────────────────────────────────────────────┤
│ Layer 3: External Monitoring                           │
│   - Health check endpoints                             │
│   - Logging services                                   │
│   - Alerting systems                                   │
└────────────────────────────────────────────────────────┘
```

### Error Workflow Pattern
```javascript
// Error Workflow (triggered on error)
Input (Error Data) → Parse Error → Log to Database → Send Alert → Retry/Dead Letter

// Available error data:
{
  "workflow": {
    "id": "workflow-id",
    "name": "Workflow Name"
  },
  "execution": {
    "id": "execution-id",
    "mode": "manual", "trigger", "webhook"
  },
  "node": {
    "name": "Node Name",
    "type": "node-type"
  },
  "error": {
    "message": "Error message",
    "description": "Detailed description",
    "stack": "Stack trace"
  },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### Retry Strategies
```yaml
Exponential Backoff:
  Wait 1s → Retry → Wait 2s → Retry → Wait 4s → Retry → Wait 8s → Fail

Implementation:
  HTTP Request Node:
    - Retry on Fail: true
    - Max Retries: 3
  OR
  Code Node + Wait Node for custom logic

Circuit Breaker Pattern:
  After N failures, stop trying for T seconds:
    1. Track failures in external store (Redis/DB)
    2. Check circuit state before each call
    3. Open circuit after threshold
    4. Half-open: Try one request after timeout
```

## Idempotency Patterns

### Idempotent Webhook Handler
```javascript
// Code Node: Check if already processed
const messageId = $json.id;
const executionId = $execution.id;

// Check in database
const existing = await Database.checkMessage(messageId);

if (existing) {
  return {
    json: {
      status: "already_processed",
      originalExecutionId: existing.executionId
    }
  };
}

// Mark as processing
await Database.saveMessage(messageId, executionId);

return { json: { messageId, processing: true } };
```

### Idempotent HTTP Operations
```yaml
Use Idempotency Keys:
  POST /api/resource
  Headers:
    Idempotency-Key: {{ $json.idempotencyKey }}

Server should:
  - Return cached response for existing key
  - Store response for 24-48 hours
  - Use consistent hashing for distribution
```

---

# State Management

## External State Stores

### Redis for State
```javascript
// Code Node: Redis operations
const redis = require('redis');
const client = redis.createClient({
  url: $env.REDIS_URL
});

// Save conversation state
await client.hSet('conversation:' + userId, {
  state: 'awaiting_phone',
  timestamp: Date.now()
});

// Get conversation state
const state = await client.hGetAll('conversation:' + userId);

// Set expiration (24 hours)
await client.expire('conversation:' + userId, 86400);

// Cleanup on completion
await client.del('conversation:' + userId);
```

### Database for Persistent State
```sql
-- Conversation state table
CREATE TABLE conversation_states (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  state JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);

CREATE INDEX idx_conversation_user ON conversation_states(user_id);
CREATE INDEX idx_conversation_expires ON conversation_states(expires_at);
```

## In-Memory State (Simple Workflows)
```javascript
// Use static variable for single-execution state
function getState() {
  if (!getState.store) {
    getState.store = new Map();
  }
  return getState.store;
}

// Set state
getState().set(userId, { step: 'name', data: {} });

// Get state
const state = getState().get(userId);
```

---

# MCP Tools for n8n (Complete Reference)

## Workflow Management

### n8n_create_workflow
```yaml
Purpose: Create new workflow programmatically
Parameters:
  - name (required): Workflow name
  - nodes (required): Array of node objects
  - connections (required): Connection mapping
  - settings (optional): Workflow settings

Use Cases:
  - Generate workflows from templates
  - Dynamic workflow creation
  - Infrastructure as code
```

### n8n_get_workflow
```yaml
Modes:
  - full: Complete workflow JSON with all details
  - details: Full + execution statistics
  - structure: Nodes and connections only
  - minimal: Metadata only (id, name, active, tags)

Use Cases:
  - Audit existing workflows
  - Export workflows
  - Generate documentation
```

### n8n_update_partial_workflow
```yaml
Operations:
  - addNode: Add new node to workflow
  - removeNode: Delete node by ID
  - updateNode: Modify node configuration
  - moveNode: Change node position
  - enable/disableNode: Toggle node active state
  - addConnection: Create new connection
  - removeConnection: Delete connection
  - updateSettings: Modify workflow settings
  - updateName: Rename workflow
  - addTag / removeTag: Tag management

Example:
  operations:
    - type: "addNode"
      node:
        id: "new-node-id"
        name: "HTTP Request"
        type: "n8n-nodes-base.httpRequest"
        position: [250, 300]
        parameters: { ... }
```

## Execution & Testing

### n8n_test_workflow
```yaml
Parameters:
  - workflowId (required): Target workflow
  - triggerType: auto-detect from workflow
    - webhook: HTTP trigger with data payload
    - form: Form submission simulation
    - chat: Chat message interaction
  - data: Input data for trigger
  - waitForResponse: Wait for completion (default: true)
  - timeout: Max wait time (default: 120000ms)

Use Cases:
  - Automated testing
  - CI/CD integration
  - Development verification
```

### n8n_executions
```yaml
Actions:
  - get: Retrieve execution details
    modes: preview, summary, filtered, full, error
  - list: List workflow executions
    filters: status, workflowId, limit, cursor
  - delete: Remove execution record

Error Mode (for debugging):
  mode: "error"
  includeStackTrace: true
  includeExecutionPath: true
  errorItemsLimit: 10
```

## Templates & Nodes

### search_nodes
```yaml
Parameters:
  - query: Search term(s)
  - mode: OR (any word), AND (all words), FUZZY (typo-tolerant)
  - source: all, core, community, verified
  - includeExamples: Include real-world configurations

Returns:
  - Node type (full class name)
  - Display name
  - Description
  - Categories
  - Documentation links
```

### search_templates
```yaml
Search Modes:
  - keyword: Text search across templates
  - by_nodes: Find templates using specific node types
  - by_task: Curated templates by use case
    - ai_automation
    - data_sync
    - webhook_processing
    - email_automation
    - slack_integration
    - data_transformation
  - by_metadata: Filter by
    - complexity: simple, medium, complex
    - maxSetupMinutes: Max setup time
    - targetAudience: developers, marketers, etc.
```

---

# Advanced Patterns

## Fan-Out / Fan-In
```
                     ┌─► Process A ─┐
                    /               \
Trigger → Split ───┼─► Process B ───┼──► Merge → Output
                    \               /
                     └─► Process C ─┘

Implementation:
  1. Split In Batches (batch size: 1)
  2. Execute Workflow (called for each item)
  3. Wait node (all branches)
  4. Merge node (combine results)
```

## Chained Workflows
```
Workflow 1 (Orchestrator)
  ↓
  Workflow 2 (Data Fetch)
  ↓
  Workflow 3 (AI Process)
  ↓
  Workflow 4 (Notification)

Benefits:
  - Reusable components
  - Parallel execution
  - Error isolation
  - Independent versioning
```

## Dead Letter Queue
```
Main Workflow
  ↓ (on error)
Error Workflow
  ↓ (if unrecoverable)
Dead Letter Queue (DB/Queue)
  ↓
  Monitoring Dashboard
  ↓
  Manual Retry Workflow
```

## Saga Pattern (Distributed Transactions)
```
Transaction:
  Step 1 (Reserve) → Step 2 (Charge) → Step 3 (Confirm)
        ↓ (fail)         ↓ (fail)         ↓ (fail)
    Compensate 1    Compensate 2     Compensate 3

Implementation:
  1. Define transaction steps
  2. Define compensation actions
  3. Execute steps sequentially
  4. On failure, execute compensations in reverse
```

---

# Performance Optimization

## Workflow Optimization

### Reduce Node Count
```yaml
Before:
  Set node → Set node → Set node → Set node

After (Code Node):
  Code node (single transformation)

Rule: Each node adds ~50-100ms overhead
```

### Batch Processing
```yaml
Small Batches (Fast):
  Batch size: 10-50
  Use for: Quick responses
  Trade-off: More API calls

Large Batches (Efficient):
  Batch size: 100-1000
  Use for: Bulk processing
  Trade-off: Higher memory usage
```

### Parallel Processing
```yaml
Before (Sequential):
  Fetch User A → Wait → Fetch User B → Wait → Fetch User C

After (Parallel):
  Split Items → Execute Workflow (parallel) → Merge

Speedup: ~N times (N = number of parallel executions)
```

### Connection Pooling
```yaml
HTTP Request Node Settings:
  - Keep Alive: true
  - Use same credential for same domain
  - Reuse database connections

Best Practice:
  Create separate workflow for external API calls
  Use as sub-workflow with connection pooling
```

## Memory Management

### Stream Large Data
```yaml
For Large Files:
  1. Don't load entire file into memory
  2. Process in chunks
  3. Use streaming APIs

Example (Code Node):
  const fs = require('fs');
  const stream = fs.createReadStream($json.filePath);

  for await (const chunk of stream) {
    // Process chunk
    await processChunk(chunk);
  }
```

### Cleanup Unused Data
```javascript
// Remove large fields before passing to next node
return {
  json: {
    id: $json.id,
    name: $json.name,
    // Don't pass: largeDataField, rawResponse, etc.
  }
};
```

---

# Security Best Practices

## Credential Management

### Environment Variables
```yaml
Credential Types:
  - Header Auth
  - Query Auth
  - Generic Credential Type
  - AWS (multiple services)
  - Azure Auth
  - Google OAuth
  - JWT Auth

Best Practices:
  1. Never hardcode credentials in workflows
  2. Use n8n credential manager
  3. Rotate credentials regularly
  4. Use different credentials for environments
  5. Grant minimum required permissions
```

### Secrets Encryption
```yaml
n8n stores credentials encrypted:
  - Encryption key in settings
  - AES-256-GCM encryption
  - Separate from database

Custom Secrets:
  - Use external vault (HashiCorp Vault, AWS Secrets Manager)
  - Load at runtime via HTTP Request
  - Never log or expose secrets
```

## Input Validation

### Webhook Validation
```javascript
// Code Node: Validate webhook payload
function validateWebhook(data, schema) {
  const errors = [];

  // Required fields
  for (const field of schema.required) {
    if (!data[field]) {
      errors.push(`Missing required field: ${field}`);
    }
  }

  // Type validation
  for (const [field, type] of Object.entries(schema.types)) {
    if (data[field] && typeof data[field] !== type) {
      errors.push(`Invalid type for ${field}: expected ${type}`);
    }
  }

  // Format validation
  if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    errors.push('Invalid email format');
  }

  return errors;
}

const schema = {
  required: ['id', 'email', 'action'],
  types: { id: 'string', email: 'string', action: 'string' }
};

const errors = validateWebhook($json, schema);

if (errors.length > 0) {
  throw new Error(`Validation failed: ${errors.join(', ')}`);
}

return { json: $json };
```

### SQL Injection Prevention
```yaml
NEVER:
  "SELECT * FROM users WHERE id = " + $json.id

ALWAYS (use parameterized queries):
  PostgreSQL Node:
    Query: SELECT * FROM users WHERE id = {{ $json.id }}
    Options: Parameterized Query
```

## Output Filtering

### Remove Sensitive Data
```javascript
// Code Node: Sanitize output
function sanitize(data) {
  const sensitiveFields = [
    'password',
    'token',
    'apiKey',
    'secret',
    'ssn',
    'creditCard'
  ];

  const result = { ...data };

  for (const field of sensitiveFields) {
    delete result[field];
    // Or mask: result[field] = '***';
  }

  return result;
}

return { json: sanitize($json) };
```

---

# Monitoring & Observability

## Logging Strategy

### Structured Logging
```javascript
// Code Node: Structured log entry
const logEntry = {
  timestamp: new Date().toISOString(),
  workflow: $workflow.name,
  executionId: $execution.id,
  node: $node.name,
  level: 'info',
  message: 'Processing completed',
  data: {
    userId: $json.userId,
    action: $json.action,
    duration: Date.now() - $json.startTime
  }
};

// Send to logging service
return {
  json: logEntry
};
```

### Centralized Logging
```
n8n Workflows → Log Aggregator (Elasticsearch/Loki/DataDog)
                                            ↓
                                    Visualization (Grafana/Kibana)
                                            ↓
                                    Alerting (PagerDuty/Slack)
```

## Metrics & Dashboards

### Key Metrics to Track
```yaml
Workflow Metrics:
  - Execution count (per workflow)
  - Success rate (%)
  - Average duration
  - P50, P95, P99 latency
  - Error rate by type

Node Metrics:
  - Slowest nodes
  - Most frequent failures
  - Data throughput

Business Metrics:
  - Users processed
  - Transactions completed
  - Revenue generated
```

### Health Check Workflow
```yaml
Purpose: Monitor system health

Checks:
  1. Database connectivity
  2. External API availability
  3. Storage access
  4. Queue depth

Schedule: Every 5 minutes

On Failure:
  - Send alert to Slack/Email
  - Create incident in tracking system
```

---

# Testing & CI/CD

## Workflow Testing

### Unit Testing (Node Level)
```yaml
Test Each Node:
  1. Open node
  2. Click "Execute Node"
  3. Verify output
  4. Test edge cases

Examples:
  - Empty input
  - Null values
  - Large datasets
  - Malformed data
```

### Integration Testing
```yaml
Test Full Workflow:
  1. Use test environment
  2. Mock external services
  3. Run with sample data
  4. Verify end-to-end flow

Tools:
  - n8n test workflow
  - Postman for webhooks
  - Sample data files
```

### Automated Testing
```javascript
// CI/CD Pipeline
name: Test n8n Workflows
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Start n8n
        run: docker run -d -p 5678:5678 n8nio/n8n
      - name: Wait for n8n
        run: sleep 30
      - name: Import test workflows
        run: ./scripts/import-workflows.sh
      - name: Run tests
        run: ./scripts/test-workflows.sh
      - name: Report results
        if: always()
        run: ./scripts/report-results.sh
```

## Version Control

### Git Integration
```yaml
Recommended Workflow:
  1. Export workflow to JSON
  2. Commit to repository
  3. Add descriptive commit message
  4. Create pull request for review
  5. Deploy to staging
  6. Test in staging
  7. Merge to main
  8. Deploy to production

Branching Strategy:
  - main: Production workflows
  - develop: Staging workflows
  - feature/*: New features
  - hotfix/*: Emergency fixes
```

### Automated Deployment
```yaml
Deployment Pipeline:
  1. Git push detected
  2. Export workflow from commit
  3. Validate workflow structure
  4. Backup current production
  5. Deploy to staging
  6. Run smoke tests
  7. Promote to production
  8. Verify health
  9. Rollback on failure
```

---

# World-Class Resources

## Official Resources
- n8n Documentation: https://docs.n8n.io
- n8n GitHub: https://github.com/n8n-io/n8n
- n8n Community: https://community.n8n.io
- n8n Templates: https://n8n.io/workflows
- n8n Academy: https://academy.n8n.io

## Learning Resources
- n8n Blog: https://n8n.io/blog
- n8n YouTube: https://youtube.com/c/n8nio
- n8n Certification Program
- n8n Community Summit recordings

## AI API Documentation
- OpenAI API: https://platform.openai.com/docs
- Anthropic Claude: https://docs.anthropic.com
- LangChain: https://python.langchain.com
- Cohere: https://docs.cohere.com

## Integration Guides
- Zapier to n8n Migration Guide
- Make (Integromat) to n8n Migration Guide
- Workflow Automation Best Practices

## Community
- n8n Discord: https://discord.gg/n8n
- n8n Reddit: r/n8n
- n8n Stack Overflow: Tag questions with 'n8n'
