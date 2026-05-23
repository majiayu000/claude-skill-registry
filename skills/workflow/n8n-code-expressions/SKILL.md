---
name: n8n Code & Expressions
description: Write code and expressions in n8n - JavaScript, Python, built-in variables, data transformation
allowed-tools: Read, Write, Edit, WebFetch
---

# n8n Code & Expressions

Master n8n's expression syntax and code capabilities.

## Expression Syntax

Expressions in n8n use `{{ }}` or `={{ }}` syntax to reference data dynamically.

### Core Variables

#### `$json` - Current Item Data
```javascript
// Access fields from current item
{{ $json.name }}                    // Direct field
{{ $json.user.email }}              // Nested field
{{ $json["field-name"] }}           // Fields with special chars
{{ $json.items[0].id }}             // Array access
```

#### `$input` - Input Operations
```javascript
// Get all input items
{{ $input.all() }}                  // Array of all items
{{ $input.first() }}                // First item
{{ $input.last() }}                 // Last item
{{ $input.item }}                   // Current item (in loop)

// Get specific item
{{ $input.item(0) }}                // Item at index
{{ $input.item(0).json.name }}      // Field from item
```

#### `$binary` - Binary Data
```javascript
// Access file/binary data
{{ $binary.data }}                  // Binary data object
{{ $binary.data.fileName }}         // Original filename
{{ $binary.data.mimeType }}         // MIME type
{{ $binary.data.fileSize }}         // Size in bytes
```

#### `$node` - Other Node Data
```javascript
// Reference output from specific node
{{ $node["HTTP Request"].json.response }}
{{ $node["Code"].json.result }}

// Get all items from node
{{ $node["Split"].json }}
```

### Metadata Variables

#### `$execution` - Execution Info
```javascript
{{ $execution.id }}                 // Execution ID
{{ $execution.mode }}               // "manual" or "trigger"
{{ $execution.resumeUrl }}          // URL to resume (Wait node)
{{ $execution.customData }}         // Custom execution data
```

#### `$workflow` - Workflow Info
```javascript
{{ $workflow.id }}                  // Workflow ID
{{ $workflow.name }}                // Workflow name
{{ $workflow.active }}              // Is active (boolean)
```

#### `$env` - Environment Variables
```javascript
{{ $env.MY_API_KEY }}               // Access env var
{{ $env["DATABASE_URL"] }}          // Env var with special chars
```

#### `$vars` - Workflow Variables
```javascript
{{ $vars.baseUrl }}                 // Workflow-level variable
{{ $vars.apiVersion }}              // Defined in workflow settings
```

#### `$now` and `$today`
```javascript
{{ $now }}                          // Current datetime (ISO)
{{ $today }}                        // Today's date (ISO)
{{ $now.toMillis() }}               // Unix timestamp (ms)
{{ $now.format('yyyy-MM-dd') }}     // Formatted date
```

### Item Context Variables

```javascript
{{ $itemIndex }}                    // Current item index (0-based)
{{ $runIndex }}                     // Current run index
{{ $prevNode }}                     // Previous node reference
{{ $position }}                     // Node position in workflow
```

## Built-in Methods

### String Methods
```javascript
{{ $json.text.toUpperCase() }}
{{ $json.text.toLowerCase() }}
{{ $json.text.trim() }}
{{ $json.text.split(',') }}
{{ $json.text.replace('old', 'new') }}
{{ $json.text.slice(0, 10) }}
{{ $json.text.includes('search') }}
{{ $json.text.startsWith('prefix') }}
{{ $json.text.length }}
```

### Number Methods
```javascript
{{ Math.round($json.price) }}
{{ Math.floor($json.value) }}
{{ Math.ceil($json.value) }}
{{ Math.abs($json.diff) }}
{{ Math.max($json.a, $json.b) }}
{{ Number.parseFloat($json.str) }}
{{ Number.parseInt($json.str, 10) }}
{{ $json.amount.toFixed(2) }}
```

### Array Methods
```javascript
{{ $json.items.length }}
{{ $json.items.map(i => i.name) }}
{{ $json.items.filter(i => i.active) }}
{{ $json.items.find(i => i.id === '123') }}
{{ $json.items.includes('value') }}
{{ $json.items.join(', ') }}
{{ $json.items.slice(0, 5) }}
{{ $json.items.sort((a,b) => a.name.localeCompare(b.name)) }}
{{ $json.items.reverse() }}
{{ [...new Set($json.items)] }}     // Unique values
```

### Object Methods
```javascript
{{ Object.keys($json.data) }}
{{ Object.values($json.data) }}
{{ Object.entries($json.data) }}
{{ JSON.stringify($json.data) }}
{{ JSON.parse($json.jsonString) }}
{{ {...$json.obj1, ...$json.obj2} }}  // Merge objects
```

### Date Methods
```javascript
// Luxon DateTime (built-in)
{{ DateTime.now().toISO() }}
{{ DateTime.fromISO($json.date).toFormat('MM/dd/yyyy') }}
{{ DateTime.now().plus({days: 7}).toISO() }}
{{ DateTime.now().minus({hours: 2}).toISO() }}
{{ DateTime.now().startOf('day').toISO() }}
{{ DateTime.now().endOf('month').toISO() }}

// Comparison
{{ DateTime.fromISO($json.date) > DateTime.now() }}
{{ DateTime.fromISO($json.date).diff(DateTime.now(), 'days').days }}
```

### Utility Methods
```javascript
// Conditionals
{{ $json.status === 'active' ? 'Yes' : 'No' }}
{{ $json.value ?? 'default' }}      // Nullish coalescing
{{ $json.name || 'Anonymous' }}     // Falsy fallback

// Type checking
{{ typeof $json.value }}
{{ Array.isArray($json.items) }}
{{ $json.value === null }}
{{ $json.value === undefined }}
```

## Code Node (JavaScript)

### Basic Structure
```javascript
// Process all items - must return array of {json: {...}} objects
const results = [];

for (const item of $input.all()) {
  // Process each item
  results.push({
    json: {
      original: item.json,
      processed: true,
      timestamp: new Date().toISOString()
    }
  });
}

return results;
```

### Single Item Return
```javascript
// Return single item
return [{
  json: {
    result: 'processed',
    data: $json.input
  }
}];
```

### Async Operations
```javascript
// HTTP request example
const response = await fetch('https://api.example.com/data', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({input: $json.data})
});

const data = await response.json();

return [{json: data}];
```

### Working with Binary Data
```javascript
// Access binary data
const binaryData = $input.first().binary;
const fileName = binaryData.data.fileName;

// Create binary output
const csvContent = 'name,email\nJohn,john@example.com';
const base64 = Buffer.from(csvContent).toString('base64');

return [{
  json: {exported: true},
  binary: {
    data: {
      data: base64,
      mimeType: 'text/csv',
      fileName: 'export.csv'
    }
  }
}];
```

### Error Handling
```javascript
try {
  const result = await riskyOperation($json.data);
  return [{json: {success: true, result}}];
} catch (error) {
  // Option 1: Return error info
  return [{json: {success: false, error: error.message}}];

  // Option 2: Throw to trigger error workflow
  throw new Error(`Processing failed: ${error.message}`);
}
```

### Using External Data
```javascript
// Get data from another node
const httpData = $node['HTTP Request'].json;

// Get all items from a node
const allItems = $items('Split Out');

// Get environment variable
const apiKey = $env.API_KEY;
```

## Code Node (Python)

### Basic Structure
```python
# Process all items
results = []

for item in _input.all():
    data = item["json"]
    results.append({
        "json": {
            "original": data,
            "processed": True,
            "uppercase": data.get("text", "").upper()
        }
    })

return results
```

### Data Transformation
```python
import json
from datetime import datetime

# Access current item
data = _json

# Transform data
result = {
    "json": {
        "id": data.get("id"),
        "name": data.get("name", "").strip(),
        "score": int(data.get("score", 0)) * 2,
        "processed_at": datetime.now().isoformat()
    }
}

return [result]
```

### Using Libraries
```python
# Available: json, datetime, re, math, urllib
import re
import math

text = _json.get("content", "")
emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)

return [{
    "json": {
        "emails": emails,
        "count": len(emails)
    }
}]
```

## Data Transformation Patterns

### Flatten Nested Data
```javascript
const item = $json;
return [{
  json: {
    id: item.id,
    userName: item.user.name,
    userEmail: item.user.email,
    addressCity: item.address?.city ?? 'Unknown'
  }
}];
```

### Group By Field
```javascript
const items = $input.all();
const grouped = {};

for (const item of items) {
  const key = item.json.category;
  if (!grouped[key]) grouped[key] = [];
  grouped[key].push(item.json);
}

return Object.entries(grouped).map(([category, items]) => ({
  json: {category, items, count: items.length}
}));
```

### Deduplicate
```javascript
const items = $input.all();
const seen = new Set();
const unique = [];

for (const item of items) {
  const key = item.json.id;
  if (!seen.has(key)) {
    seen.add(key);
    unique.push(item);
  }
}

return unique;
```

### Pivot Data
```javascript
// Convert rows to columns
const items = $input.all();
const pivoted = {};

for (const item of items) {
  const {key, value} = item.json;
  pivoted[key] = value;
}

return [{json: pivoted}];
```

### Batch Items
```javascript
const items = $input.all();
const batchSize = 10;
const batches = [];

for (let i = 0; i < items.length; i += batchSize) {
  batches.push({
    json: {
      batch: Math.floor(i / batchSize) + 1,
      items: items.slice(i, i + batchSize).map(item => item.json)
    }
  });
}

return batches;
```

## Common Recipes

### Validate Required Fields
```javascript
const required = ['email', 'name', 'amount'];
const missing = required.filter(f => !$json[f]);

if (missing.length > 0) {
  throw new Error(`Missing required fields: ${missing.join(', ')}`);
}

return [{json: {...$json, validated: true}}];
```

### Parse JSON String
```javascript
let parsed;
try {
  parsed = JSON.parse($json.jsonString);
} catch (e) {
  throw new Error('Invalid JSON input');
}
return [{json: parsed}];
```

### Format Currency
```javascript
const amount = $json.amount;
const formatted = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD'
}).format(amount);

return [{json: {...$json, formattedAmount: formatted}}];
```

### Generate UUID
```javascript
function uuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

return [{json: {...$json, id: uuid()}}];
```

### Rate Limit Helper
```javascript
// Track calls for rate limiting
const execId = $execution.id;
const callCount = $workflow.staticData?.callCount ?? 0;

$workflow.staticData = {
  callCount: callCount + 1,
  lastCall: Date.now()
};

return [{json: {...$json, callNumber: callCount + 1}}];
```

## Debugging

### Log Data
```javascript
console.log('Input:', JSON.stringify($json, null, 2));
console.log('Item count:', $input.all().length);
console.log('Execution:', $execution.id);
```

### Inspect Types
```javascript
return [{
  json: {
    inputType: typeof $json,
    keys: Object.keys($json),
    itemCount: $input.all().length,
    hasEmail: 'email' in $json,
    emailType: typeof $json.email
  }
}];
```

## Output Format
```
EXPRESSION:
  {{ [expression here] }}
  Returns: [expected output]

CODE PATTERN:
  Purpose: [what it does]
  ```javascript
  [code here]
  ```
  Input: [sample input]
  Output: [sample output]
```
