---
name: libindex
description: >
  libindex - Base index class for storage-backed data. Index class provides
  JSONL storage operations and filtering logic. BufferedIndex adds high-volume
  write support with periodic flushing. Use for building custom indexes,
  implementing data stores, and managing persistent collections.
---

# libindex Skill

## When to Use

- Building custom storage-backed indexes
- Implementing JSONL-based data stores
- Creating searchable collections with filtering
- Managing high-volume write workloads

## Key Concepts

**Index**: Base class providing read/write/filter operations on JSONL files.
Subclass to create domain-specific indexes.

**BufferedIndex**: Extends Index with write buffering for high-throughput
scenarios, flushing periodically.

## Usage Patterns

### Pattern 1: Create custom index

```javascript
import { Index } from "@copilot-ld/libindex";

class UserIndex extends Index {
  constructor(storage) {
    super(storage, "users");
  }

  async findByEmail(email) {
    return this.filter((user) => user.email === email);
  }
}
```

### Pattern 2: High-volume writes

```javascript
import { BufferedIndex } from "@copilot-ld/libindex";

const index = new BufferedIndex(storage, "logs", { flushInterval: 5000 });
await index.append(logEntry); // Buffered
await index.flush(); // Force flush
```

## Integration

Base class for VectorIndex, TraceIndex, ResourceIndex and other domain indexes.
