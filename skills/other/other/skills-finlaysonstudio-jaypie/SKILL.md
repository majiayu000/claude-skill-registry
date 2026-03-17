---
description: Skill/vocabulary storage with pluggable backends (pre-1.0)
related: fabric, mcp, tools
---

# @jaypie/tildeskill

Skill/vocabulary management with pluggable storage backends for AI assistants and documentation systems.

## Overview

This package provides a storage abstraction for skill/vocabulary documents with markdown frontmatter support. It enables:
- Loading skills from markdown files with YAML frontmatter
- In-memory storage for testing
- Consistent alias normalization and validation
- Filtering by namespace and tags
- Searching across alias, name, description, content, and tags
- Include expansion for composable skills

## Installation

```bash
npm install @jaypie/tildeskill
```

## Core Types

```typescript
interface SkillRecord {
  alias: string;              // Lookup key (normalized lowercase)
  content: string;            // Markdown body
  description?: string;       // Brief description from frontmatter
  includes?: string[];        // Auto-expand these skill aliases on lookup
  name?: string;              // Display title for the skill
  nicknames?: string[];       // Alternate lookup keys for getByNickname
  related?: string[];         // Related skill aliases
  tags?: string[];            // Categorization tags
}

interface ListFilter {
  namespace?: string;         // Namespace prefix matching (e.g., "kit:*")
  tag?: string;               // Filter by tag
}

interface SkillStore {
  get(alias: string): Promise<SkillRecord | null>;
  getByNickname(nickname: string): Promise<SkillRecord | null>;
  list(filter?: ListFilter): Promise<SkillRecord[]>;
  put(record: SkillRecord): Promise<SkillRecord>;
  search(term: string): Promise<SkillRecord[]>;
}
```

## Store Factories

### Markdown Store (File-based)

```typescript
import { createMarkdownStore } from "@jaypie/tildeskill";

const store = createMarkdownStore({ path: "./skills" });

// Get a specific skill
const skill = await store.get("aws");
if (skill) {
  console.log(skill.content);
}

// List all skills
const skills = await store.list();
skills.forEach(s => console.log(`${s.alias}: ${s.description}`));
```

### Memory Store (Testing)

```typescript
import { createMemoryStore } from "@jaypie/tildeskill";

const store = createMemoryStore([
  { alias: "test", content: "# Test\n\nContent", description: "Test skill" }
]);

const skill = await store.get("test");
```

## Include Expansion

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

## Filtering and Search

```typescript
// Filter by namespace prefix
const kitSkills = await store.list({ namespace: "kit:" });

// Filter by tag
const cloudSkills = await store.list({ tag: "cloud" });

// Search across alias, name, description, content, and tags
const results = await store.search("lambda");

// Lookup by nickname
const skill = await store.getByNickname("amazon");
```

## Validation Utilities

```typescript
import { isValidAlias, validateAlias, normalizeAlias } from "@jaypie/tildeskill";

// Check validity
isValidAlias("my-skill");     // true
isValidAlias("../../etc");    // false (path traversal)

// Normalize to lowercase
normalizeAlias("MY-Skill");   // "my-skill"

// Validate and normalize (throws on invalid)
validateAlias("valid");       // returns "valid"
validateAlias("../bad");      // throws BadRequestError
```

## Skill File Format

Skill files use YAML frontmatter:

```yaml
---
description: Brief description shown in listings
includes: base-skill, common-utils
name: Display Title
nicknames: alt-name, another-alias
related: alias1, alias2, alias3
tags: category1, category2
---

# Skill Title

Markdown content...
```

All frontmatter fields accept either comma-separated strings or YAML arrays.

## Testing with Mocks

```typescript
import { mockTildeskill, restoreTildeskill } from "@jaypie/testkit";

beforeEach(() => {
  mockTildeskill();
});

afterEach(() => {
  restoreTildeskill();
});
```

## See Also

- **`skill("fabric")`** - Service patterns that use tildeskill
- **`skill("mcp")`** - MCP server that uses tildeskill for skill storage
