---
name: json-render-core
description: Core package for defining schemas, catalogs, and AI prompt generation for json-render. Use when working with @json-render/core, defining schemas, creating catalogs, or building JSON specs for UI/video generation.
---

# @json-render/core

Core package for schema definition, catalog creation, and spec streaming.

## Key Concepts

- **Schema**: Defines the structure of specs and catalogs (use `defineSchema`)
- **Catalog**: Maps component/action names to their definitions (use `defineCatalog`)
- **Spec**: JSON output from AI that conforms to the schema
- **SpecStream**: JSONL streaming format for progressive spec building

## Defining a Schema

```typescript
import { defineSchema } from "@json-render/core";

export const schema = defineSchema((s) => ({
  spec: s.object({
    // Define spec structure
  }),
  catalog: s.object({
    components: s.map({
      props: s.zod(),
      description: s.string(),
    }),
  }),
}), {
  promptTemplate: myPromptTemplate, // Optional custom AI prompt
});
```

## Creating a Catalog

```typescript
import { defineCatalog } from "@json-render/core";
import { schema } from "./schema";
import { z } from "zod";

export const catalog = defineCatalog(schema, {
  components: {
    Button: {
      props: z.object({
        label: z.string(),
        variant: z.enum(["primary", "secondary"]).nullable(),
      }),
      description: "Clickable button component",
    },
  },
});
```

## Generating AI Prompts

```typescript
const systemPrompt = catalog.prompt(); // Uses schema's promptTemplate
const systemPrompt = catalog.prompt({ customRules: ["Rule 1", "Rule 2"] });
```

## SpecStream Utilities

For streaming AI responses (JSONL patches):

```typescript
import { createSpecStreamCompiler } from "@json-render/core";

const compiler = createSpecStreamCompiler<MySpec>();

// Process streaming chunks
const { result, newPatches } = compiler.push(chunk);

// Get final result
const finalSpec = compiler.getResult();
```

## Dynamic Prop Expressions

Any prop value can be a dynamic expression resolved at render time:

- **`{ "$path": "/state/key" }`** - reads a value from the state model
- **`{ "$cond": <condition>, "$then": <value>, "$else": <value> }`** - evaluates a visibility condition and picks a branch

`$cond` uses the same syntax as visibility conditions (`eq`, `neq`, `path`, `and`, `or`, `not`). `$then` and `$else` can themselves be expressions (recursive).

```json
{
  "color": {
    "$cond": { "eq": [{ "path": "/activeTab" }, "home"] },
    "$then": "#007AFF",
    "$else": "#8E8E93"
  }
}
```

```typescript
import { resolvePropValue, resolveElementProps } from "@json-render/core";

const resolved = resolveElementProps(element.props, { stateModel: myState });
```

## User Prompt Builder

Build structured user prompts with optional spec refinement and state context:

```typescript
import { buildUserPrompt } from "@json-render/core";

// Fresh generation
buildUserPrompt({ prompt: "create a todo app" });

// Refinement (patch-only mode)
buildUserPrompt({ prompt: "add a toggle", currentSpec: spec });

// With runtime state
buildUserPrompt({ prompt: "show data", state: { todos: [] } });
```

## Spec Validation

Validate spec structure and auto-fix common issues:

```typescript
import { validateSpec, autoFixSpec } from "@json-render/core";

const { valid, issues } = validateSpec(spec, catalog);
const fixed = autoFixSpec(spec);
```

## Key Exports

| Export | Purpose |
|--------|---------|
| `defineSchema` | Create a new schema |
| `defineCatalog` | Create a catalog from schema |
| `resolvePropValue` | Resolve a single prop expression against data |
| `resolveElementProps` | Resolve all prop expressions in an element |
| `buildUserPrompt` | Build user prompts with refinement and state context |
| `validateSpec` | Validate spec structure |
| `autoFixSpec` | Auto-fix common spec issues |
| `createSpecStreamCompiler` | Stream JSONL patches into spec |
| `parseSpecStreamLine` | Parse single JSONL line |
| `applySpecStreamPatch` | Apply patch to object |
