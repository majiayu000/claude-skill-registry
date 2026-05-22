---
name: core-development
description: Work on the core package (types, validation, normalization, diff). Use when modifying DSL processing logic or data flow.
---

# Core Package Development

The core package (`packages/core/`) is dependency-free and handles all DSL processing.

## Data Flow

```
DSL (YAML input) → validate() → normalize() → IR → diff() → Patch
```

## Key Files

| File | Purpose | Exports |
|------|---------|---------|
| `types.ts` | Type definitions | DSL*, IR*, Patch, WebSocket protocol |
| `validate.ts` | YAML validation | `validate(dsl): ValidationResult` |
| `normalize.ts` | DSL → IR conversion | `normalize(dsl): IRDocument` |
| `diff.ts` | IR diff calculation | `diff(prev, next): Patch` |

## Type Hierarchy

```
DSL Types (user input)      IR Types (normalized)
─────────────────────       ────────────────────
DSLDocument                 IRDocument
  ├─ version: number          ├─ version: number
  ├─ docId: string            ├─ docId: string
  ├─ title?: string           ├─ title: string
  ├─ nodes: DSLNode[]         ├─ nodes: Record<string, IRNode>
  └─ edges?: DSLEdge[]        └─ edges: Record<string, IREdge>

DSLNode                     IRNode
  ├─ id: string               ├─ id: string
  ├─ provider: string         ├─ provider: string
  ├─ kind: string             ├─ kind: string
  ├─ label?: string           ├─ label: string (default: id)
  ├─ parent?: string          ├─ parent: string | null
  └─ layout: DSLLayout        └─ layout: { x, y, w, h }

DSLEdge                     IREdge
  ├─ id: string               ├─ id: string
  ├─ from: string             ├─ from: string
  ├─ to: string               ├─ to: string
  └─ label?: string           └─ label: string (default: "")
```

## Patch Operations

```typescript
type PatchOp =
  | { op: "upsertNode"; node: IRNode }
  | { op: "removeNode"; id: string }
  | { op: "upsertEdge"; edge: IREdge }
  | { op: "removeEdge"; id: string };

interface Patch {
  baseRev: number;
  nextRev: number;
  ops: PatchOp[];
}
```

## WebSocket Protocol Types

```typescript
// Plugin → CLI
interface HelloMessage {
  type: "hello";
  docId: string;
  secret?: string;
}

interface RequestFullMessage {
  type: "requestFull";
  docId: string;
}

// CLI → Plugin
interface FullMessage {
  type: "full";
  rev: number;
  ir: IRDocument;
}

interface PatchMessage {
  type: "patch";
  baseRev: number;
  nextRev: number;
  ops: PatchOp[];
}

interface ErrorMessage {
  type: "error";
  message: string;
}
```

## Development Workflow

1. **Modify types** → Update `types.ts`
2. **Update validation** → Ensure `validate.ts` catches invalid input
3. **Update normalization** → Handle new fields/defaults in `normalize.ts`
4. **Update diff** → Handle new patch scenarios in `diff.ts`
5. **Add tests** → Co-located `*.test.ts` files
6. **Run tests** → `bun test packages/core/`

## Testing

```bash
# All core tests
bun test packages/core/

# Specific test file
bun test packages/core/src/diff.test.ts
bun test packages/core/src/validate.test.ts
bun test packages/core/src/normalize.test.ts

# Watch mode
bun test --watch packages/core/
```

## Common Patterns

### Adding a new node property

1. Add to `DSLNode` and `IRNode` in `types.ts`
2. Add validation in `validate.ts`
3. Add default value handling in `normalize.ts`
4. Update diff logic if property affects equality
5. Add test cases for validation, normalization, and diff

### Adding a new edge property

1. Add to `DSLEdge` and `IREdge` in `types.ts`
2. Add validation in `validate.ts`
3. Add default value handling in `normalize.ts`
4. Update diff logic for edge equality check
5. Add test cases
