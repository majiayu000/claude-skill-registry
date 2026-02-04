---
name: textmate-grammar
# prettier-ignore
description: Use when creating or editing TextMate grammar files for VS Code syntax highlighting - patterns, scopes, and language tokenization
---

# TextMate Grammar

## Quick Start

```json
{
  "scopeName": "source.omg",
  "patterns": [{ "include": "#main" }],
  "repository": {
    "main": {
      "patterns": [
        { "include": "#comments" },
        { "include": "#strings" },
        { "include": "#keywords" }
      ]
    },
    "keywords": {
      "match": "\\b(if|else|while|return)\\b",
      "name": "keyword.control.omg"
    },
    "strings": {
      "begin": "\"",
      "end": "\"",
      "name": "string.quoted.double.omg",
      "patterns": [{ "include": "#escapes" }]
    }
  }
}
```

## Core Concepts

- **scopeName**: Unique identifier like `source.js`, `text.html`
- **patterns**: Array of rules applied in order
- **repository**: Named rule groups for reuse via `#name`
- **match**: Single-line regex pattern
- **begin/end**: Multi-line patterns with nested content

## Scope Naming Conventions

| Prefix | Usage |
|--------|-------|
| `keyword.control` | if, else, for, return |
| `keyword.operator` | +, -, =, && |
| `storage.type` | class, function, var |
| `entity.name.function` | function names |
| `entity.name.type` | type/class names |
| `variable.parameter` | function parameters |
| `string.quoted` | quoted strings |
| `comment.line` | single-line comments |
| `constant.numeric` | numbers |
| `punctuation.definition` | brackets, braces |

## Key Patterns

- Use `captures` to assign scopes to regex groups: `"captures": { "1": { "name": "..." } }`
- Use `contentName` for scope of content between begin/end
- Escape backslashes in JSON: `\\b` for word boundary
- Order matters: first matching pattern wins
