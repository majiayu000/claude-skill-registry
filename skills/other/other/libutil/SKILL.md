---
name: libutil
description: >
  libutil - General utilities. countTokens and estimateTokens for GPT-style
  token counting. generateHash creates SHA256 hashes. generateUuid creates
  unique IDs findProjectRoot locates repository root. updateEnvFile modifies
  environment files. exec runs child processes. createBundler downloads code
  bundles. Use for token counting, hashing, and project utilities.
---

# libutil Skill

## When to Use

- Counting tokens for LLM context management
- Generating hashes and UUIDs
- Finding project root directory
- Running child processes
- Managing generated code bundles

## Key Concepts

**Token counting**: GPT-compatible tokenization for context window management.

**Project root**: Finds repository root by looking for package.json markers.

**Bundle management**: Download and extract pre-generated code bundles.

## Usage Patterns

### Pattern 1: Count tokens

```javascript
import { countTokens, estimateTokens } from "@copilot-ld/libutil";

const exact = countTokens("Hello, world!"); // Accurate count
const fast = estimateTokens("Hello, world!"); // Quick estimate
```

### Pattern 2: Generate identifiers

```javascript
import { generateHash, generateUuid } from "@copilot-ld/libutil";

const hash = generateHash(content); // 16-char SHA256
const uuid = generateUuid(); // Standard UUID
```

### Pattern 3: Find project root

```javascript
import { findProjectRoot } from "@copilot-ld/libutil";

const root = await findProjectRoot(); // /path/to/copilot-ld
```

## Integration

Used across packages for common utilities. countTokens used by libmemory.
