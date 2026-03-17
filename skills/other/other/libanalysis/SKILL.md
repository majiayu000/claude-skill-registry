---
name: libanalysis
description: >
  libanalysis - Code analysis and formatting utilities. formatForAnalysis
  function prepares markdown documents with Prettier formatting and line numbers
  for LLM code review tasks. Use for document preparation, code analysis, and
  creating numbered reference documents for AI processing.
---

# libanalysis Skill

## When to Use

- Preparing documents for LLM-based code review
- Formatting markdown with line numbers for reference
- Creating numbered documents for analysis tasks
- Pre-processing content before sending to AI

## Key Concepts

**formatForAnalysis**: Formats markdown content using Prettier and prepends line
numbers, making it easy for LLMs to reference specific lines in their responses.

## Usage Patterns

### Pattern 1: Format document for analysis

```javascript
import { formatForAnalysis } from "@copilot-ld/libanalysis";

const document = `# README
This is a code sample.`;

const formatted = await formatForAnalysis(document);
// Returns:
// 1: # README
// 2: This is a code sample.
```

## Integration

Standalone utility used in analysis scripts and evaluation pipelines.
