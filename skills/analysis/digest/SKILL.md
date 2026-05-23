---
name: digest
description: Extract patterns, insights, and knowledge from text content. Use when asked to digest, extract, summarize, analyze patterns in code, conversations, documents, or decisions. Stores extracted knowledge for future retrieval.
user-invocable: true
---

# /digest - CYNIC Knowledge Extraction

*"Transform chaos into structured knowledge"*

## Quick Start

```
/digest <content to analyze>
```

## What It Does

Analyzes content and extracts:
- **Patterns**: Recurring structures and behaviors
- **Insights**: Key learnings and observations
- **Decisions**: Choices made and their rationale
- **Knowledge**: Facts and relationships

Extracted knowledge is stored in CYNIC's memory for future queries.

## Content Types

| Type | Best For |
|------|----------|
| `code` | Source code analysis |
| `conversation` | Chat/discussion extraction |
| `document` | Documentation, articles |
| `decision` | Decision records |

## Examples

### Digest Code
```
/digest this module for patterns
```

### Digest a Conversation
```
/digest our discussion about authentication
```

### Digest a Document
```
/digest the API documentation
```

## Implementation

Use the `brain_cynic_digest` MCP tool:

```javascript
brain_cynic_digest({
  content: "<text to digest>",
  type: "code|conversation|document|decision",
  source: "<origin identifier>"
})
```

## Output

Returns:
- **Patterns detected**: Recurring structures
- **Key insights**: Main takeaways
- **Knowledge stored**: What was saved
- **Connections**: Links to existing knowledge

## See Also

- `/search` - Find digested knowledge
- `/patterns` - View detected patterns
- `/judge` - Evaluate extracted patterns
