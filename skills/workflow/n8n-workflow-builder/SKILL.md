---
name: n8n Workflow Builder
description: Design and build n8n workflows - triggers, nodes, flow logic, error handling, and best practices
allowed-tools: Read, Write, Edit, WebFetch, Bash
---

# n8n Workflow Builder

Expert guidance for designing and building n8n automation workflows.

## Core Concepts

### Workflow Structure
```
[Trigger] → [Process] → [Transform] → [Action] → [Output]
     ↓           ↓            ↓           ↓
  Webhook    HTTP Req     Code Node    Slack      Response
  Schedule   Database     Filter       Email      Webhook
  Manual     API Call     Merge        DB Write   File
```

## Trigger Nodes

### Webhook Trigger
```json
// Receives HTTP requests to start workflow
{
  "httpMethod": "POST",
  "path": "my-webhook",
  "authentication": "headerAuth",
  "responseMode": "onReceived"
}
```
- **Path**: Unique URL path for webhook
- **Authentication**: None, Basic, Header, JWT
- **Response Mode**:
  - `onReceived` - Immediate 200 response
  - `lastNode` - Wait for workflow completion

### Schedule Trigger
```json
// Cron-based execution
{
  "rule": {
    "interval": [{"field": "cronExpression", "expression": "0 9 * * *"}]
  }
}
```
- Cron expressions: `minute hour day month weekday`
- Examples: `0 */2 * * *` (every 2 hours), `0 9 * * 1-5` (9am weekdays)

### Manual Trigger
- For testing and on-demand execution
- Good for workflows triggered by other workflows

### Other Triggers
- **Email Trigger (IMAP)** - New email arrives
- **RSS Feed Trigger** - New feed item
- **Local File Trigger** - File system changes
- **Chat Trigger** - Chat message received
- **n8n Form Trigger** - Form submission

## Data Processing Nodes

### HTTP Request Node
```json
{
  "method": "POST",
  "url": "https://api.example.com/endpoint",
  "authentication": "genericCredentialType",
  "sendHeaders": true,
  "headerParameters": {
    "Content-Type": "application/json"
  },
  "sendBody": true,
  "bodyParameters": {
    "key": "={{ $json.value }}"
  }
}
```

### Code Node (JavaScript)
```javascript
// Process all items
const results = [];
for (const item of $input.all()) {
  results.push({
    json: {
      processed: item.json.data.toUpperCase(),
      timestamp: new Date().toISOString()
    }
  });
}
return results;
```

### Code Node (Python)
```python
# Process items with Python
results = []
for item in _input.all():
    results.append({
        "json": {
            "processed": item["json"]["data"].upper(),
            "count": len(item["json"]["data"])
        }
    })
return results
```

### Filter Node
```json
{
  "conditions": {
    "options": {
      "caseSensitive": true,
      "leftValue": "={{ $json.status }}",
      "operation": "equals",
      "rightValue": "active"
    }
  }
}
```
Operations: `equals`, `notEquals`, `contains`, `startsWith`, `endsWith`, `regex`, `exists`, `isNumeric`, `>=`, `<=`

### Merge Node
Combine data from multiple branches:
- **Append** - Combine all items into one list
- **Combine by Position** - Match items by index
- **Combine by Field** - Match items by key field
- **Multiplex** - Create all combinations
- **Choose Branch** - Select one branch's data

### Split Out Node
Convert array to individual items:
```json
{
  "fieldToSplitOut": "items",
  "include": "selectedOtherFields",
  "fieldsToInclude": "id,name"
}
```

### Aggregate Node
Group and summarize:
```json
{
  "aggregate": "aggregateAllItemData",
  "fieldsToAggregate": {
    "fieldToAggregate": "amount",
    "renameField": "total"
  },
  "aggregation": "sum"
}
```
Aggregations: `sum`, `average`, `count`, `min`, `max`, `concatenate`

## Flow Logic Nodes

### If Node (Conditional)
```json
{
  "conditions": {
    "boolean": [
      {
        "value1": "={{ $json.score }}",
        "operation": "largerEqual",
        "value2": 80
      }
    ]
  }
}
```
Creates two branches: `true` and `false`

### Switch Node (Multi-way)
```json
{
  "dataType": "string",
  "value1": "={{ $json.type }}",
  "rules": [
    {"value2": "email", "output": 0},
    {"value2": "sms", "output": 1},
    {"value2": "push", "output": 2}
  ],
  "fallbackOutput": 3
}
```

### Loop Over Items
Process items in batches:
```json
{
  "batchSize": 10,
  "options": {
    "reset": false
  }
}
```

### Wait Node
```json
{
  "resume": "timeInterval",
  "amount": 5,
  "unit": "minutes"
}
```
Or wait for webhook: `"resume": "webhook"`

### Stop And Error
```json
{
  "errorMessage": "Validation failed: {{ $json.error }}"
}
```

## Sub-Workflows

### Execute Sub-workflow
```json
{
  "source": "database",
  "workflowId": "workflow-id-here",
  "mode": "each",
  "options": {
    "waitForSubWorkflow": true
  }
}
```
- **Mode**: `once` (all items), `each` (per item)
- Pass data via workflow input

### Execute Sub-workflow Trigger
Define inputs for sub-workflow:
```json
{
  "inputFields": [
    {"fieldName": "userId", "fieldType": "string"},
    {"fieldName": "action", "fieldType": "string"}
  ]
}
```

## Error Handling

### Error Trigger Node
Catches workflow errors:
```javascript
// In Error Trigger workflow
const errorData = $json;
// errorData.execution.error - Error details
// errorData.workflow.name - Failed workflow name
// Send to Slack, email, or logging service
```

### Error Workflow Pattern
```
[Main Workflow]
     ↓ (on error)
[Error Trigger] → [Format Error] → [Slack Alert]
                                 → [Log to DB]
                                 → [Retry Logic]
```

### Retry Pattern
```javascript
// Code node for retry logic
const maxRetries = 3;
const currentRetry = $json.retryCount || 0;

if (currentRetry < maxRetries) {
  return [{
    json: {
      ...$json,
      retryCount: currentRetry + 1,
      shouldRetry: true
    }
  }];
}
return [{json: {...$json, shouldRetry: false, failed: true}}];
```

## Best Practices

### 1. Workflow Organization
- Use **Sticky Notes** for documentation
- **Tag workflows** by function (api, scheduled, webhook)
- Break complex workflows into **sub-workflows**
- Use descriptive node names

### 2. Data Handling
```javascript
// Always validate input data
if (!$json.email || !$json.email.includes('@')) {
  throw new Error('Invalid email format');
}

// Handle missing fields gracefully
const name = $json.name ?? 'Unknown';
const score = $json.score ?? 0;
```

### 3. Performance
- Use **batch processing** for large datasets
- Add **Wait nodes** to respect rate limits
- Use **parallel execution** when order doesn't matter
- **Limit** results from database queries

### 4. Security
- Store credentials in n8n's credential manager
- Use **environment variables** for sensitive config
- Validate and sanitize all webhook inputs
- Use HTTPS for all external requests

### 5. Testing
- Use **Pin Data** to test with fixed inputs
- Test error paths explicitly
- Use **Manual Trigger** for development
- Check execution history for debugging

## Common Patterns

### API Polling Pattern
```
[Schedule: Every 5 min] → [HTTP Request] → [Filter New Items]
                                                    ↓
                         [Store Last ID] ← [Process Items]
```

### Webhook → Process → Response
```
[Webhook Trigger] → [Validate] → [Process] → [Respond to Webhook]
                         ↓
                    [If Invalid] → [Error Response]
```

### Batch Processing
```
[Trigger] → [Get All Items] → [Loop (batch=100)]
                                      ↓
              [Process Batch] → [Wait 1 sec] → [Next Batch]
```

### Fan-out/Fan-in
```
[Trigger] → [Split to Items] → [Process Each] → [Merge Results]
                                                       ↓
                                               [Aggregate Stats]
```

## Debugging Tips

1. **Check Execution Log**: View input/output for each node
2. **Pin Data**: Freeze data at a node for testing
3. **Error Details**: Check `$execution.error` in error workflow
4. **Console Output**: Use Code node to log: `console.log(JSON.stringify($json))`
5. **Manual Execution**: Run workflow step-by-step

## Output Format
```
WORKFLOW DESIGN:
  Name: [Descriptive name]
  Trigger: [Type and config]
  Purpose: [What it automates]

NODES:
  1. [Node Type] - [Purpose]
  2. [Node Type] - [Purpose]
  ...

FLOW LOGIC:
  [ASCII diagram of workflow]

ERROR HANDLING:
  - [How errors are caught]
  - [Recovery strategy]

CONSIDERATIONS:
  - [Performance notes]
  - [Security notes]
  - [Rate limiting]
```
