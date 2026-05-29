---
sidebar_position: 6
---

# @jaypie/tildeskill

**Prerequisites:** `npm install @jaypie/tildeskill`

**Status:** Experimental - APIs may change

## Overview

`@jaypie/tildeskill` provides a storage abstraction for skill/vocabulary documents with markdown frontmatter support. It's used internally by `@jaypie/mcp` for serving skill documentation to AI assistants.

## Installation

```bash
npm install @jaypie/tildeskill
```

## Quick Reference

### Core Exports

| Export | Purpose |
|--------|---------|
| `createMarkdownStore` | File-based store (reads .md files) |
| `createMemoryStore` | In-memory store (for testing) |
| `expandIncludes` | Expand included skills into content |
| `isValidAlias` | Check if alias is valid |
| `validateAlias` | Validate and normalize alias (throws on invalid) |
| `normalizeAlias` | Normalize alias to lowercase |

### Types

| Type | Description |
|------|-------------|
| `SkillRecord` | Skill document with alias, content, description, includes, name, nicknames, related, tags |
| `SkillStore` | Store interface with get, getByNickname, list, put, search methods |
| `ListFilter` | Filter options for list (namespace, tag) |

## Store Factories

### Markdown Store

Reads skill documents from a directory of markdown files:

```typescript
import { createMarkdownStore } from "@jaypie/tildeskill";

const store = createMarkdownStore({ path: "./skills" });

// Get a specific skill
const skill = await store.get("aws");
if (skill) {
  console.log(skill.alias);       // "aws"
  console.log(skill.description); // From frontmatter
  console.log(skill.content);     // Markdown body
  console.log(skill.related);     // ["errors", "lambda"]
}

// List all skills
const skills = await store.list();
skills.forEach(s => console.log(`${s.alias}: ${s.description}`));
```

### Memory Store

In-memory store for testing:

```typescript
import { createMemoryStore } from "@jaypie/tildeskill";

const store = createMemoryStore([
  { alias: "test", content: "# Test\n\nContent", description: "Test skill" },
  { alias: "another", content: "# Another", related: ["test"] },
]);

// Supports all store operations
const skill = await store.get("test");
await store.put({ alias: "new", content: "# New Skill" });
```

## Include Expansion

Compose skills by including other skills' content:

```typescript
import { expandIncludes, createMemoryStore } from "@jaypie/tildeskill";

const store = createMemoryStore([
  { alias: "base", content: "Base content" },
  { alias: "main", content: "Main content", includes: ["base"] },
]);

const record = await store.get("main");
const expanded = await expandIncludes(store, record);
// expanded = "Base content\n\nMain content"
```

Features:
- Recursively expands nested includes
- Prevents circular references
- Skips missing includes silently

## Filtering and Search

```typescript
// Filter by namespace prefix
const kitSkills = await store.list({ namespace: "kit:" });

// Filter by tag
const cloudSkills = await store.list({ tag: "cloud" });

// Combined filters
const kitCloudSkills = await store.list({ namespace: "kit:", tag: "cloud" });

// Search across alias, name, description, content, and tags
const results = await store.search("lambda");

// Lookup by nickname (alternate alias)
const skill = await store.getByNickname("amazon");
```

## Skill File Format

Skill files use YAML frontmatter followed by markdown content:

```yaml
---
description: Brief description shown in skill listings
includes: base-skill, common-utils
name: Display Title
nicknames: alt-name, another-alias
related: alias1, alias2, alias3
tags: category1, category2
---

# Skill Title

Markdown content with documentation, code examples, etc.
```

### Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | `string` | Brief description for listings |
| `includes` | `string` | Comma-separated list of skills to auto-expand |
| `name` | `string` | Display title for the skill |
| `nicknames` | `string` | Comma-separated alternate lookup keys |
| `related` | `string` | Comma-separated list of related skill aliases |
| `tags` | `string` | Comma-separated categorization tags |

All frontmatter fields accept either comma-separated strings or YAML arrays.

## Validation Utilities

### isValidAlias

Check if an alias is valid without throwing:

```typescript
import { isValidAlias } from "@jaypie/tildeskill";

isValidAlias("my-skill");     // true
isValidAlias("my_skill");     // true
isValidAlias("skill123");     // true
isValidAlias("../../etc");    // false (path traversal)
isValidAlias("");             // false (empty)
isValidAlias("a".repeat(100)); // false (too long)
```

### validateAlias

Validate and normalize, throwing `BadRequestError` on invalid input:

```typescript
import { validateAlias } from "@jaypie/tildeskill";

validateAlias("Valid");       // returns "valid" (normalized)
validateAlias("MY-SKILL");    // returns "my-skill"
validateAlias("../bad");      // throws BadRequestError
```

### normalizeAlias

Normalize alias to lowercase (does not validate):

```typescript
import { normalizeAlias } from "@jaypie/tildeskill";

normalizeAlias("MY-Skill");   // "my-skill"
normalizeAlias("Test_123");   // "test_123"
```

## Testing

### With @jaypie/testkit

```typescript
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { mockTildeskill, restoreTildeskill } from "@jaypie/testkit";

describe("MyComponent", () => {
  beforeEach(() => {
    mockTildeskill();
  });

  afterEach(() => {
    restoreTildeskill();
  });

  it("works with mocked store", async () => {
    // Your tests here
  });
});
```

### Direct Memory Store

```typescript
import { createMemoryStore } from "@jaypie/tildeskill";

const testStore = createMemoryStore([
  { alias: "test", content: "# Test", description: "Test skill" },
]);

// Inject into your component/service
const service = createService({ store: testStore });
```

## Error Handling

```typescript
import { validateAlias } from "@jaypie/tildeskill";
import { BadRequestError } from "@jaypie/errors";

try {
  validateAlias("../malicious");
} catch (error) {
  if (error instanceof BadRequestError) {
    console.log("Invalid alias:", error.message);
  }
}
```

## Use Cases

### MCP Skill Server

The primary use case is serving skill documentation via MCP:

```typescript
import { createMarkdownStore } from "@jaypie/tildeskill";
import { fabricService } from "@jaypie/fabric";

const store = createMarkdownStore({ path: "./skills" });

const skillService = fabricService({
  alias: "skill",
  description: "Get skill documentation",
  input: {
    alias: { type: String, required: false },
  },
  service: async ({ alias }) => {
    if (!alias) {
      const skills = await store.list();
      return skills.map(s => `${s.alias}: ${s.description}`).join("\n");
    }
    const skill = await store.get(alias);
    return skill?.content ?? `Skill "${alias}" not found`;
  },
});
```

### Documentation System

Build a searchable documentation system:

```typescript
import { createMarkdownStore } from "@jaypie/tildeskill";

const store = createMarkdownStore({ path: "./docs" });

async function searchDocs(query: string) {
  const docs = await store.list();
  return docs.filter(d =>
    d.content.toLowerCase().includes(query.toLowerCase()) ||
    d.description?.toLowerCase().includes(query.toLowerCase())
  );
}
```

## Related

- [@jaypie/mcp](/docs/experimental/mcp) - MCP server using tildeskill
- [@jaypie/fabric](/docs/experimental/fabric) - Service patterns
- [@jaypie/testkit](/docs/packages/testkit) - Testing utilities
