---
name: docs-nguyenquocviet2005-examples
description: The Text Analyzer skill is a comprehensive example of how to build agent
  skills in AnythingLLM. It demonstrates all key patterns and best practices for skill
  development.
---

# Example Agent Skill: Text Analyzer

## Overview

The **Text Analyzer** skill is a comprehensive example of how to build agent skills in AnythingLLM. It demonstrates all key patterns and best practices for skill development.

## What It Does

The Text Analyzer skill performs four types of text analysis:

1. **Keywords** - Extracts the top 10 most common meaningful words
2. **Sentiment** - Determines if text is positive, negative, or neutral
3. **Statistics** - Calculates word count, sentence count, character count, and averages
4. **Readability** - Computes Flesch-Kincaid grade level for text difficulty

## File Locations

- **Backend Implementation**: `server/utils/agents/aibitat/plugins/text-analyzer.js`
- **Plugin Registration**: `server/utils/agents/aibitat/plugins/index.js`
- **Frontend UI**: `frontend/src/pages/Admin/Agents/skills.js`

## How to Use

### In a Chat with @agent

Users can invoke the skill by asking the agent to analyze text:

```
@agent: Analyze the sentiment of this paragraph: "I love this product! It's amazing and works perfectly."
```

Or:

```
@agent: What are the most common keywords in this article? [article text]
```

### Skill Parameters

The skill accepts two parameters:

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `text` | string | Any text | The content to analyze |
| `analysis_type` | string | `keywords`, `sentiment`, `statistics`, `readability` | Type of analysis to perform |

## Architecture Breakdown

### 1. Skill Definition Object

```javascript
const textAnalyzer = {
  name: "text-analyzer",              // Unique identifier
  startupConfig: { params: {} },      // Optional config
  plugin: function() { ... }          // Plugin factory function
}
```

### 2. Plugin Setup

```javascript
setup(aibitat) {
  aibitat.function({
    // Function metadata and schema
    name: this.name,
    description: "What this skill does",

    // JSON Schema for input validation
    parameters: { ... },

    // Examples for LLM few-shot learning
    examples: [ ... ],

    // Main execution handler
    handler: async function({ text, analysis_type }) { ... }
  });
}
```

### 3. Handler Function Flow

```
handler() called
    ↓
Check for duplicates (prevent redundant calls)
    ↓
Route to appropriate analysis function
    ↓
Execute analysis logic
    ↓
Log action via introspect()
    ↓
Track execution
    ↓
Return result to LLM
```

## Key Patterns Demonstrated

### 1. Deduplication
```javascript
const { Deduplicator } = require("../utils/dedupe");
tracker: new Deduplicator(),

if (this.tracker.isDuplicate(this.name, { text, analysis_type })) {
  return "Already analyzed.";
}
this.tracker.trackRun(this.name, { text, analysis_type });
```

**Why**: Prevents the agent from calling the same skill twice with identical parameters.

### 2. Function Metadata

```javascript
parameters: {
  $schema: "http://json-schema.org/draft-07/schema#",
  type: "object",
  properties: {
    text: { type: "string" },
    analysis_type: { type: "string", enum: [...] }
  }
}
```

**Why**: Validates inputs and helps the LLM understand what parameters to provide.

### 3. Examples for LLM

```javascript
examples: [
  {
    prompt: "What are the most common words in this text?",
    call: JSON.stringify({ text: "...", analysis_type: "keywords" })
  }
]
```

**Why**: Few-shot learning helps the LLM learn how to properly invoke the function.

### 4. Logging & Introspection

```javascript
this.super.introspect(
  `${this.caller}: Analyzing text for ${analysis_type}.`
);
this.super.handlerProps.log(`Error message`);
```

**Why**: Helps with debugging and provides visibility into skill execution.

### 5. Helper Methods

```javascript
analyzeKeywords: async function(text) { ... }
analyzeSentiment: async function(text) { ... }
analyzeStatistics: async function(text) { ... }
analyzeReadability: async function(text) { ... }
```

**Why**: Organizing logic into separate methods keeps code clean and maintainable.

## Extending the Example

### Adding a New Analysis Type

1. **Add to enum** in parameters:
```javascript
analysis_type: {
  enum: ["keywords", "sentiment", "statistics", "readability", "ngrams"]
}
```

2. **Add to switch statement** in handler:
```javascript
case "ngrams":
  result = await this.analyzeNgrams(text);
  break;
```

3. **Implement analysis method**:
```javascript
analyzeNgrams: async function(text) {
  // Implementation here
  return "Results";
}
```

### Adding Socket Communication

For skills that need to send data to the frontend in real-time:

```javascript
this.super.socket.send("eventName", {
  key: "value",
  data: "payload"
});
```

**Examples in codebase**:
- `rechart.js`: Sends `rechartVisualize` event for chart rendering
- `save-file-browser.js`: Sends `fileDownload` event for file downloads

### Adding Complex Return Values

For skills that return structured data:

```javascript
this.super._replySpecialAttributes = {
  saveAsType: "customType",
  storedResponse: (additionalText = "") =>
    JSON.stringify({ data, additionalText }),
  postSave: () => { /* cleanup */ }
};
```

## Testing the Skill

Once enabled, the skill will be available to the agent. Test with:

```
@agent: Analyze the sentiment of "This is fantastic! I love it!"
```

Expected response:
```
Sentiment: Positive (Positive: 2, Negative: 0)
```

## Available Context in Handler

Inside the handler, you have access to:

```javascript
this.super              // AIbitat framework instance
this.super.socket       // WebSocket for real-time communication
this.super.introspect() // Log visible to frontend
this.super.handlerProps // Configuration and utilities
this.caller             // Name of the agent calling this
this.tracker            // Deduplication tracker
```

## Common Skill Patterns

### 1. Search Skill (Like web-browsing)
```
Takes query string → performs search → returns results
```

### 2. Generation Skill (Like create-chart)
```
Takes data/parameters → generates content → sends via socket
```

### 3. Storage Skill (Like save-file-to-browser)
```
Takes content → prepares for storage → sends download signal
```

### 4. Analysis Skill (Text Analyzer - this example)
```
Takes content → performs calculation → returns formatted results
```

## Skill Lifecycle

1. **Startup** - Skill plugin `setup()` called when AIbitat initializes
2. **Function Registration** - `aibitat.function()` registers the skill
3. **LLM Decision** - Agent decides to call the skill
4. **Validation** - Parameters validated against JSON Schema
5. **Execution** - Handler function runs async logic
6. **Response** - Result returned to LLM for processing
7. **Completion** - Deduplication tracked for future calls

## Best Practices

1. ✅ **Use JSON Schema** for clear parameter validation
2. ✅ **Provide Examples** for few-shot learning
3. ✅ **Handle Errors** gracefully with try-catch
4. ✅ **Deduplicate** to prevent redundant execution
5. ✅ **Log Actions** via introspect() for debugging
6. ✅ **Document** parameters and behavior
7. ✅ **Keep Handlers Async** for I/O operations
8. ✅ **Return Clear Messages** for user feedback

## Anti-Patterns to Avoid

1. ❌ **Long-running Sync Operations** - Use async/await
2. ❌ **Ignoring Deduplication** - Always check for duplicates
3. ❌ **Unclear Parameter Names** - Use descriptive names
4. ❌ **No Error Handling** - Wrap in try-catch
5. ❌ **Complex Nested Callbacks** - Use async/await
6. ❌ **Silent Failures** - Always log errors
7. ❌ **No Examples** - Provide few-shot examples

## Related Skills in Codebase

- `memory.js` - Search and store in RAG system
- `web-browsing.js` - Search using multiple engines
- `save-file-browser.js` - Download files to client
- `summarize.js` - Summarize documents
- `sql-agent/index.js` - Query SQL databases
- `rechart.js` - Render interactive charts

## References

- [Skill Definition Pattern](../../../utils/agents/defaults.js)
- [AIbitat Framework](./index.js)
- [Deduplicator Utility](../utils/dedupe.js)
- [Web Browsing Skill Example](./web-browsing.js)
- [Save File Skill Example](./save-file-browser.js)
