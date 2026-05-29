---
name: time-travel-crdt
description: Time Travel CRDT Skill
version: 1.0.0
---

# Time Travel CRDT Skill

> *"Time is of the essence — but the essence is not time."*
> — Kleppmann & Gentle

CRDTs enable time travel: branch, merge, undo, redo without central coordination. GF(3) coloring for causal consistency.

## Overview

Time travel in collaborative systems means:
1. **Branching**: Diverge from any point in history
2. **Merging**: Automatically reconcile divergent branches
3. **Undo/Redo**: Navigate the causal graph
4. **Replay**: Reconstruct any historical state

This skill connects Diamond Types, Automerge, Eg-walker, and Janus reversible computing.

## Core Algorithms

### Eg-walker (Gentle & Kleppmann 2025) [ERGODIC: 0]

The **Event Graph Walker** combines the best of OT and CRDTs:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EG-WALKER ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Operation Log          Event Graph              Current State              │
│   ┌──────────┐          ┌───────────┐            ┌───────────┐              │
│   │ Insert A │──────────│  A ───┐   │            │           │              │
│   │ Insert B │          │       ▼   │            │  "ABCD"   │              │
│   │ Delete C │──────────│  B ◄── D  │────────────│           │              │
│   │ Insert D │          │       ▲   │            └───────────┘              │
│   └──────────┘          │  C ───┘   │                                       │
│                         └───────────┘                                       │
│                                                                              │
│   Time Complexity:                                                           │
│   - Insert/Delete: O(log n) amortized                                       │
│   - Merge: O(n) worst case, O(1) common case                                │
│   - Memory: O(n) steady state (vs O(n²) for YATA)                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key insight**: Walk the event graph to compute document state, caching intermediate results.

### Diamond Types [PLUS: +1]

bmorphism's `eg-walker-reference` is a TypeScript reimplementation of Diamond Types:

```typescript
// Simplified Eg-walker from bmorphism/eg-walker-reference
interface Op {
  id: OpId;           // (agent, seq) tuple
  origin: OpId | null; // causal parent
  content: string;    // inserted content
  deleted: boolean;   // tombstone flag
}

function merge(doc: Doc, remoteOps: Op[]): Doc {
  // Walk the event graph, applying ops in causal order
  for (const op of topoSort(remoteOps)) {
    if (op.deleted) {
      doc = deleteAt(doc, findPosition(doc, op.id));
    } else {
      doc = insertAt(doc, findPosition(doc, op.origin), op.content);
    }
  }
  return doc;
}
```

**Performance** (EuroSys 2025):
- 10x less memory than Automerge
- 100x faster document loading
- Competitive merge performance

### Automerge [MINUS: -1]

The original CRDT for JSON-like documents:

```javascript
import * as Automerge from '@automerge/automerge'

// Create and modify
let doc1 = Automerge.init()
doc1 = Automerge.change(doc1, 'Add title', doc => {
  doc.title = "Time Travel"
})

// Fork (branch)
let doc2 = Automerge.clone(doc1)
doc2 = Automerge.change(doc2, 'Edit on branch', doc => {
  doc.title = "Time Travel CRDTs"
})

// Merge (time travel reconciliation)
doc1 = Automerge.merge(doc1, doc2)
```

### Yjs [MINUS: -1]

Fast CRDT with YATA algorithm:

```javascript
import * as Y from 'yjs'

const ydoc = new Y.Doc()
const ytext = ydoc.getText('content')

// Observe changes
ytext.observe(event => {
  console.log('Delta:', event.delta)
})

// Time travel via undo manager
const undoManager = new Y.UndoManager(ytext)
undoManager.undo()
undoManager.redo()
```

## Janus Reversible Computing [ERGODIC: 0]

True time travel: run programs backwards.

```janus
// Janus: reversible Fibonacci
procedure fib(int n, int x1, int x2)
  if n = 0 then
    x1 += x2
    x1 <=> x2
    n += 1
  else
    n -= 1
    x1 <=> x2
    x1 -= x2
    call fib(n, x1, x2)
  fi x1 = x2

// Run forward: fib(10, 1, 0) → (1, 55)
// Run backward: fib(10, 1, 55) → (1, 0)
```

**Key insight**: Every operation has an inverse; no information is lost.

## GF(3) Causal Consistency

Color operations by their causal role:

| Trit | Color | Operation Type | Role |
|------|-------|----------------|------|
| +1 | Red | **Insert** | Creates content |
| 0 | Green | **Move/Retain** | Preserves structure |
| -1 | Blue | **Delete** | Removes content (tombstone) |

**Conservation Law**: A well-formed edit sequence maintains:
```
Σ(trits) ≡ 0 (mod 3)  ⟺  balanced edit
```

Example:
```
Insert "hello" (+1)
Insert "world" (+1)
Delete "world" (-1)
Retain structure (0)
───────────────────
Sum: +1 +1 -1 +0 = +1 ≢ 0 (mod 3) → unbalanced!

Fix: Add one more delete or two inserts to balance.
```

## Integration with Unworld

The `unworld` skill replaces time with derivation chains:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UNWORLD ↔ CRDT BRIDGE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   DerivationChain                    CRDT Event Graph                        │
│   ┌─────────────┐                   ┌─────────────────┐                     │
│   │ seed_0      │                   │ (agent_0, 0)    │                     │
│   │    ↓        │                   │      ↓          │                     │
│   │ seed_1 = f(seed_0, trit_0)      │ (agent_0, 1) ◄──│──┐                  │
│   │    ↓        │    ≅              │      ↓          │  │                  │
│   │ seed_2 = f(seed_1, trit_1)      │ (agent_1, 0) ───│──┘                  │
│   │    ↓        │                   │      ↓          │                     │
│   │ ...         │                   │ merge point     │                     │
│   └─────────────┘                   └─────────────────┘                     │
│                                                                              │
│   No time! Only derivation.         Causal order from vector clocks.        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Correspondence**:
- `seed` ↔ `OpId`
- `trit` ↔ operation type (insert/delete/retain)
- `derivation` ↔ causal dependency

## bmorphism Interactome

Relevant bmorphism repositories:

| Repo | Description | Role |
|------|-------------|------|
| `eg-walker-reference` | TypeScript Eg-walker | Reference implementation |
| `ewig` | Eternal text editor | Immutable data structures |
| `Gay.jl` | Splittable PRNG | Deterministic colors for ops |
| `duck` | DuckDB extensions | Time-travel queries |

**Cobordism**: bmorphism connects Diamond Types (josephg) with Gay.jl coloring for visual debugging of CRDT merge states.

## Time Travel Queries (DuckDB)

```sql
-- Create temporal versioning table
CREATE TABLE document_history (
    id UUID,
    content TEXT,
    op_type VARCHAR,  -- 'insert', 'delete', 'retain'
    trit INTEGER,     -- GF(3) color
    valid_from TIMESTAMP,
    valid_to TIMESTAMP,
    agent_id VARCHAR,
    seq INTEGER
);

-- Time travel query: document state at specific time
SELECT content
FROM document_history
WHERE valid_from <= '2025-01-01 12:00:00'
  AND (valid_to IS NULL OR valid_to > '2025-01-01 12:00:00')
ORDER BY seq;

-- GF(3) balance check
SELECT 
    SUM(trit) as trit_sum,
    SUM(trit) % 3 as mod3,
    CASE WHEN SUM(trit) % 3 = 0 THEN '✓ Balanced' ELSE '✗ Drift' END as status
FROM document_history
WHERE agent_id = 'agent_0';
```

## Commands

```bash
# Diamond Types (Rust)
cargo run --example edit

# Eg-walker reference (TypeScript)
cd eg-walker-reference && npm test

# Automerge
npx automerge-repo-demo

# Janus reversible interpreter
janus run program.jan --reverse

# DuckDB time travel
duckdb -c "SELECT * FROM document_history AS OF '2025-01-01';"
```

## Canonical Triads

```
# Time Travel Core
automerge (-1) ⊗ eg-walker (0) ⊗ diamond-types (+1) = 0 ✓

# Reversible Computing
janus (-1) ⊗ unworld (0) ⊗ gay-mcp (+1) = 0 ✓

# Temporal Versioning
temporal-coalgebra (-1) ⊗ time-travel-crdt (0) ⊗ koopman-generator (+1) = 0 ✓

# DuckDB Bridge
polyglot-spi (-1) ⊗ time-travel-crdt (0) ⊗ gay-mcp (+1) = 0 ✓
```

## References

- [Eg-walker Paper (EuroSys 2025)](https://arxiv.org/abs/2409.14252)
- [Diamond Types](https://github.com/josephg/diamond-types) - 1.7k★
- [Automerge](https://automerge.org/)
- [Yjs](https://yjs.dev/)
- [Janus Reversible Language](https://topps.diku.dk/pirc/janus-playground/)
- [Martin Kleppmann's Blog](https://martin.kleppmann.com/)
- [bmorphism/eg-walker-reference](https://github.com/bmorphism/eg-walker-reference)

## See Also

- `unworld` - Derivation chains replacing time
- `temporal-coalgebra` - Coalgebraic observation of streams
- `duckdb-temporal-versioning` - SQL time travel
- `reversible-computing` - Janus and time-symmetric computation



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `distributed-systems`: 3 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
time-travel-crdt (○) + SDF.Ch10 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch5: Evaluation
- Ch2: Domain-Specific Languages

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.