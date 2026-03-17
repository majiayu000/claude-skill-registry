---
name: libstorage
description: >
  libstorage - Storage abstraction layer. createStorage factory returns backend
  based on environment (local, S3, Supabase). LocalStorage, S3Storage,
  SupabaseStorage implement storage interface. parseJsonl and serializeJsonl
  handle JSONL format. Use for file persistence, data storage, and multi-backend
  support.
---

# libstorage Skill

## When to Use

- Persisting data to filesystem or cloud storage
- Supporting multiple storage backends
- Reading/writing JSON and JSONL files
- Building storage-agnostic applications

## Key Concepts

**Storage interface**: Provides a common API (read, write, list, delete) for all
supported storage systems.

**createStorage**: Factory that returns appropriate backend based on environment
configuration.

**JSONL support**: Parse and serialize newline-delimited JSON for streaming
data.

## Usage Patterns

### Pattern 1: Create storage instance

```javascript
import { createStorage } from "@copilot-ld/libstorage";

const storage = createStorage(config);
await storage.write("data/file.json", { key: "value" });
const data = await storage.read("data/file.json");
```

### Pattern 2: JSONL operations

```javascript
import { parseJsonl, serializeJsonl } from "@copilot-ld/libstorage";

const items = parseJsonl(jsonlContent);
const output = serializeJsonl(items);
```

## Integration

Used by all indexes and services. Backend configured via STORAGE environment.
