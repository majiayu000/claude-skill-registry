---
name: textmate-grammar
# prettier-ignore
description: Use when authoring TextMate grammars for syntax highlighting - covers scopes, patterns, and language injection
---

# TextMate Grammar Authoring

## Quick Start

```json
{
  "scopeName": "source.lea",
  "patterns": [
    { "include": "#comments" },
    { "include": "#keywords" },
    { "include": "#strings" }
  ],
  "repository": {
    "comments": {
      "name": "comment.line.double-dash.lea",
      "match": "--.*$"
    }
  }
}
```

## Core Concepts

### Scope Naming Convention

```
comment.line          - Line comments
comment.block         - Block comments
keyword.control       - if, else, match, return
keyword.operator      - +, -, *, /, />
storage.type          - let, maybe, context
entity.name.function  - Function names
variable.other        - Variables
string.quoted.double  - "strings"
constant.numeric      - Numbers
constant.language     - true, false
```

### Pattern Types

#### Match Pattern

```json
{
  "name": "keyword.control.lea",
  "match": "\\b(if|else|match|return)\\b"
}
```

#### Begin/End Pattern

```json
{
  "name": "string.quoted.double.lea",
  "begin": "\"",
  "end": "\"",
  "patterns": [
    {
      "name": "constant.character.escape.lea",
      "match": "\\\\."
    }
  ]
}
```

#### Captures

```json
{
  "match": "\\b(let)\\s+([a-zA-Z_][a-zA-Z0-9_]*)\\s*=",
  "captures": {
    "1": { "name": "storage.type.lea" },
    "2": { "name": "entity.name.function.lea" }
  }
}
```

## Lea-Specific Patterns

### Pipe Operators

```json
{
  "name": "keyword.operator.pipe.lea",
  "match": "/>|/>>>|\\\\>|</"
}
```

### Decorators

```json
{
  "name": "entity.name.decorator.lea",
  "match": "#[a-zA-Z_][a-zA-Z0-9_]*"
}
```

### Type Annotations

```json
{
  "match": "(::)\\s*([A-Z][a-zA-Z0-9]*)\\s*(:>)\\s*([A-Z][a-zA-Z0-9]*)",
  "captures": {
    "1": { "name": "keyword.operator.type.lea" },
    "2": { "name": "entity.name.type.lea" },
    "3": { "name": "keyword.operator.return-type.lea" },
    "4": { "name": "entity.name.type.lea" }
  }
}
```

### Functions

```json
{
  "begin": "\\(",
  "end": "\\)\\s*(->)",
  "endCaptures": {
    "1": { "name": "storage.type.function.arrow.lea" }
  },
  "patterns": [
    { "include": "#parameters" }
  ]
}
```

## Testing

Use VSCode's "Developer: Inspect Editor Tokens and Scopes" command to verify tokenization.

## Reference Files

- [references/scopes.md](references/scopes.md) - Complete scope naming guide
- [references/regex.md](references/regex.md) - Oniguruma regex reference
