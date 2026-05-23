---
name: effect-collections-datastructs
description: Value-based data structures (Data.struct, tuple, array) and high-performance collections (Chunk, HashSet). Use for safe comparisons and pipelines.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Data Structures & Collections

## Structural Equality
```ts
import { Data, Equal } from "effect"
const a = Data.struct({ id: 1, name: "A" })
const b = Data.struct({ id: 1, name: "A" })
Equal.equals(a, b) // true
```

## Tuples & Arrays
```ts
const t = Data.tuple(1, "x")
const arr = Data.array([1,2,3])
```

## Chunk
```ts
import { Chunk } from "effect"
const items = Chunk.fromIterable([1,2,3])
```

## HashSet
```ts
import { HashSet } from "effect"
const set = HashSet.fromIterable([1,2,3])
```

## Local Source Reference

**CRITICAL: Search local Effect source before implementing**

The full Effect source code is available at `docs/effect-source/`. Always search the actual implementation before writing Effect code.

### Key Source Files
- Data: `docs/effect-source/effect/src/Data.ts`
- Chunk: `docs/effect-source/effect/src/Chunk.ts`
- HashSet: `docs/effect-source/effect/src/HashSet.ts`
- Equal: `docs/effect-source/effect/src/Equal.ts`

### Example Searches
```bash
# Find Data.struct and equality patterns
grep -F "Data.struct" docs/effect-source/effect/src/Data.ts
grep -F "Data.tuple" docs/effect-source/effect/src/Data.ts

# Find Chunk operations
grep -F "export" docs/effect-source/effect/src/Chunk.ts | grep -F "function"

# Study HashSet API
grep -F "export" docs/effect-source/effect/src/HashSet.ts | grep -F "function"

# Find Equal implementation
grep -F "equals" docs/effect-source/effect/src/Equal.ts
```

### Workflow
1. Identify the collection API you need (e.g., Chunk, HashSet)
2. Search `docs/effect-source/effect/src/` for the implementation
3. Study the types and available operations
4. Look at test files for usage examples
5. Write your code based on real implementations

**Real source code > documentation > assumptions**

## References
- Agent Skills overview: https://www.anthropic.com/news/skills
- Skills guide: https://docs.claude.com/en/docs/claude-code/skills

