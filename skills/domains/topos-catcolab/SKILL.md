---
name: topos-catcolab
description: Topos Institute's CatColab for collaborative category theory - community model building, double theories, stock and flow epidemiology, and real-time collaborative diagramming via Automerge CRDT.
version: 1.0.0
---


# CatColab: Collaborative Category Theory

**Trit**: 0 (ERGODIC - coordinator)
**Color**: Blue (#4A90D9)

## Overview

CatColab is Topos Institute's platform for **formal, interoperable, conceptual modeling** using applied category theory. It enables:

- **Community Model Building**: Groups collaboratively construct categorical models
- **Double Categories**: Theories as double categorical structures (DOTS)
- **Stock & Flow**: Epidemiological modeling with categorical semantics
- **Real-time Collaboration**: Automerge CRDT for conflict-free multi-user editing

## Core Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CatColab Platform                     │
├─────────────────────────────────────────────────────────┤
│  Frontend (SolidJS)                                      │
│  ├── ModelNotebookEditor   → Object/Morphism declarations│
│  ├── DiagramNotebookEditor → Visual diagram authoring    │
│  └── AnalysisNotebookEditor → ODE simulation, export     │
├─────────────────────────────────────────────────────────┤
│  Automerge CRDT Sync Layer                               │
│  ├── DocHandle (document state)                          │
│  ├── WebSocket sync to server                            │
│  └── Reconcile → SolidJS reactivity                      │
├─────────────────────────────────────────────────────────┤
│  catlog (Rust Engine via WASM)                           │
│  ├── Double theories (DiscreteDblTheory, ModalDblTheory) │
│  ├── Model elaboration & validation                      │
│  └── ODE integration for stock-flow                      │
├─────────────────────────────────────────────────────────┤
│  Backend (Axum + PostgreSQL)                             │
│  └── Document persistence, auth, Julia interop           │
└─────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Community Model Building Events

CatColab supports participatory modeling workshops:

```typescript
// Model Building Session Pattern
interface ModelBuildingEvent {
  theory: DblTheory;           // Double theory framework
  participants: User[];        // Concurrent editors
  liveDoc: LiveModelDoc;       // Automerge-backed document
  validationState: 'Valid' | 'Invalid' | 'Illformed';
}

// Each participant can add:
type CellType = 
  | 'ObDecl'           // Object declaration
  | 'MorDecl'          // Morphism declaration  
  | 'InstantiatedModel' // Compose from existing models
```

### 2. Double Theories (DOTS)

Diagrams Of Theories with double categorical semantics:

```rust
// From catlog: Double theory as VDC with structure
trait DblTheory: VDblCategory {
    type ObType;   // Object generators (stocks, states)
    type MorType;  // Morphism generators (flows, transitions)
    type ObOp;     // Object operations
    type MorOp;    // Morphism operations
}

// Example: Stock and Flow theory
pub fn th_stock_flow() -> DiscreteDblTheory {
    let mut cat = FpCategory::new();
    cat.add_ob_generator(name("Stock"));
    cat.add_mor_generator(name("Flow"), name("Stock"), name("Stock"));
    cat.add_mor_generator(name("Link"), name("Stock"), name("Stock"));
    cat.into()
}
```

### 3. Stock & Flow for Epidemiology

Categorical modeling for epidemic dynamics:

```julia
# SIR Model as Stock-Flow diagram
using Catlab

@present SchSIR(FreeSchema) begin
  Stock::Ob
  Flow::Hom(Stock, Stock)
  Link::Hom(Stock, Stock)
end

# Instantiate: S → I → R with infection/recovery flows
sir_model = @acset SIR begin
  Stock = [:S, :I, :R]
  Flow = [(:S, :I), (:I, :R)]  # infection, recovery
  Link = [(:I, :S)]            # I influences S→I rate
end

# CatColab generates mass-action ODEs:
# dS/dt = -β*S*I
# dI/dt = β*S*I - γ*I  
# dR/dt = γ*I
```

### 4. Collaborative Diagramming

Real-time multi-user diagram authoring:

```typescript
// Automerge change flow
function editDiagram(cell: DiagramCell, edit: Edit) {
  // 1. Local change via Automerge
  liveDoc.changeDoc((doc) => {
    applyEdit(doc.cells[cell.id], edit);
  });
  
  // 2. WebSocket broadcasts to server
  // 3. Server broadcasts to all clients
  // 4. reconcile() triggers SolidJS reactivity
  // → All participants see change in real-time
}
```

## Integration Points

### With world-t (CatColab Directory)

```bash
~/worlds/T/CatColab/
├── packages/catlog/           # Core Rust engine
├── packages/frontend/         # SolidJS UI
├── packages/backend/          # Axum server
└── packages/algjulia-interop/ # Julia bridge
```

### With acsets-relational-thinking

CatColab models are ACSets:

```julia
# Any CatColab model is a functor X: Theory → Set
# Schema = Theory, Instance = Model

# Export CatColab model to Catlab ACSet
function catcolab_to_acset(model_json::Dict)
    theory = parse_theory(model_json["theory"])
    schema = theory_to_schema(theory)
    acset = instantiate(schema, model_json["cells"])
    return acset
end
```

### With sheaf-laplacian-coordination

Multi-agent modeling coordination:

```python
# Coordinate multiple modelers via sheaf diffusion
from catcolab import LiveModelDoc
from sheaf_laplacian import SheafLaplacian

def coordinate_modelers(docs: list[LiveModelDoc], topology):
    """Harmonize beliefs across modeling participants."""
    sheaf = SheafLaplacian(
        num_nodes=len(docs),
        stalk_dim=embedding_dim,
        edge_index=topology
    )
    
    embeddings = [embed_model(doc) for doc in docs]
    consensus = sheaf.diffuse(torch.stack(embeddings))
    
    return suggest_reconciliation(docs, consensus)
```

## Practical Examples

### Example 1: Community Epidemiology Workshop

```typescript
// Host a model building event for local epidemiology
const workshop = await catcolab.createEvent({
  name: "Community Disease Modeling",
  theory: "primitive-stock-flow",
  participants: communityMembers,
});

// Facilitator seeds initial structure
await workshop.addCell({
  type: "ObDecl",
  name: "Population",
  theory_type: "Stock"
});

// Participants collaboratively add:
// - Disease states (Susceptible, Infected, Recovered)
// - Flows (infection, recovery, vaccination)
// - Links (contact rate influences)

// Run mass-action ODE simulation
const simulation = await workshop.analyze({
  type: "ode-simulation",
  parameters: { beta: 0.3, gamma: 0.1 },
  timespan: [0, 100]
});
```

### Example 2: Iterative Model Sharing

```bash
# Export model for review
catcolab export --format=json sir-model.catcolab > sir.json

# Import into Catlab for analysis
julia -e 'using CatColabInterop; analyze(load("sir.json"))'

# Fork and modify
catcolab fork sir-model.catcolab --name "sir-with-vaccination"

# Merge improvements back
catcolab merge --base=sir-model --feature=sir-with-vaccination
```

### Example 3: Double Theory for Custom Domain

```rust
// Define theory for supply chain modeling
pub fn th_supply_chain() -> DiscreteDblTheory {
    let mut cat = FpCategory::new();
    
    // Object types
    cat.add_ob_generator(name("Warehouse"));
    cat.add_ob_generator(name("Factory"));
    cat.add_ob_generator(name("Retailer"));
    
    // Morphism types (flows between locations)
    cat.add_mor_generator(name("Ship"), name("Factory"), name("Warehouse"));
    cat.add_mor_generator(name("Distribute"), name("Warehouse"), name("Retailer"));
    cat.add_mor_generator(name("Reorder"), name("Retailer"), name("Factory"));
    
    // Composition: Ship ; Distribute represents full supply chain
    cat.into()
}
```

## GF(3) Triads

```
acsets-relational-thinking (-1) ⊗ topos-catcolab (0) ⊗ gay-mcp (+1) = 0 ✓
sheaf-laplacian-coordination (-1) ⊗ topos-catcolab (0) ⊗ open-games (+1) = 0 ✓
world-t (-1) ⊗ topos-catcolab (0) ⊗ discopy (+1) = 0 ✓
```

## Commands

```bash
# Development
just catcolab-dev              # Start local CatColab
just catcolab-build            # Build frontend + WASM

# Model operations
just catcolab-new THEORY NAME  # Create new model
just catcolab-export MODEL     # Export to JSON
just catcolab-simulate MODEL   # Run ODE analysis

# Collaboration
just catcolab-share MODEL USERS # Share with collaborators
just catcolab-event THEORY      # Create model building event
just catcolab-sync              # Force sync all docs
```

## API Reference

### WASM Bindings

```typescript
import { init_catlog, th_stock_flow, elaborate_model } from '@catcolab/catlog-wasm';

await init_catlog();
const theory = th_stock_flow();
const result = elaborate_model(theory, modelJson);

if (result.status === 'Valid') {
  const odeSystem = result.equations;
}
```

### REST Endpoints

```http
GET  /api/documents           # List user documents
POST /api/documents           # Create document
GET  /api/documents/:id       # Get document metadata
GET  /api/documents/:id/sync  # WebSocket upgrade for Automerge

POST /api/analyses/:type      # Run analysis (ode, diagram-export)
```

## References

### Topos Institute
- [CatColab](https://catcolab.org) - Live platform
- [Topos Blog](https://topos.institute/blog) - Model building events
- [RelationalThinking](https://toposinstitute.github.io/RelationalThinking-Book/)

### Papers
- Patterson et al. "Categorical data structures for technical computing" (2022)
- Shapiro et al. "Conflict-free Replicated Data Types" (Automerge foundation)

### Related Skills
- `world-t` - CatColab directory structure and codebase
- `acsets-relational-thinking` - ACSets as categorical databases
- `sheaf-laplacian-coordination` - Multi-agent consensus
- `open-games` - Compositional game semantics
- `discopy` - String diagram computation
- `boneh-roughgarden-wev` - WEV mechanism design via double theories

## Boneh-Roughgarden Integration

CatColab double theories formalize the cognitive superposition of cryptographic (Boneh) and game-theoretic (Roughgarden) worlds:

```
┌─────────────────────────────────────────────────────────────────────┐
│  DOUBLE THEORY: CryptoGame                                          │
├─────────────────────────────────────────────────────────────────────┤
│  Horizontal Category (Crypto):                                      │
│    Objects: BLS, VDF, ZK-SNARK, Threshold                           │
│    Morphisms: commit, reveal, aggregate, verify                     │
│                                                                     │
│  Vertical Category (Games):                                         │
│    Objects: Nash, PoA, Mechanism, Auction                           │
│    Morphisms: equilibrate, price, extract, prevent                  │
│                                                                     │
│  Squares (World Extractable Value):                                 │
│    BLS ──commit──► Threshold                                        │
│     │               │                                               │
│  equilibrate     extract                                            │
│     ▼               ▼                                               │
│    Nash ──price──► Auction                                          │
└─────────────────────────────────────────────────────────────────────┘
```

### CatColab Model: WEV Prevention

```rust
// Double theory for Boneh-Roughgarden WEV
pub fn th_wev_mechanism() -> DiscreteDblTheory {
    let mut cat = FpCategory::new();
    
    // Crypto world (horizontal)
    cat.add_ob_generator(name("BLS"));
    cat.add_ob_generator(name("VDF")); 
    cat.add_ob_generator(name("ZK"));
    cat.add_mor_generator(name("commit"), name("BLS"), name("VDF"));
    cat.add_mor_generator(name("reveal"), name("VDF"), name("ZK"));
    
    // Game world (vertical via fibration)
    cat.add_ob_generator(name("Nash"));
    cat.add_ob_generator(name("Mechanism"));
    cat.add_mor_generator(name("equilibrate"), name("Nash"), name("Mechanism"));
    cat.add_mor_generator(name("price"), name("Mechanism"), name("Nash"));
    
    cat.into()
}
```

### 23-Subagent Spawning via CatColab

Each Boneh/Roughgarden/Wuollet subagent corresponds to a cell in the CatColab document:

| Cell Type | Persona | Colors Known | CatColab Element |
|-----------|---------|--------------|------------------|
| ObDecl | Boneh | 1 | `VDF` object |
| ObDecl | Roughgarden | 2 | `Nash` object |
| ObDecl | Wuollet | 3 | `MEV` object |
| MorDecl | Mixed | - | `extract: Nash → MEV` |

---

**Skill Name**: topos-catcolab
**Type**: Collaborative Applied Category Theory
**Trit**: 0 (ERGODIC)
**GF(3)**: Conserved via triadic composition



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb

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