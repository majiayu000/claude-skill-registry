---
name: aptos-society
description: 'Aptos Society Scale'
version: 1.0.0
---

# Aptos Society Scale

**Trit**: 0 (ERGODIC - coordinator)
**Domain**: Compositional Game Theory × Blockchain Governance × Social Interaction Labs

## Academic Foundations

### Seth Frey (UC Davis, Ostrom Workshop)
- **Composing Games into Complex Institutions** (PLoS ONE 2023)
- Institutional preferences laboratory experiments
- Game-theoretic institutional design with Jules Hedges

### Michael Zargham (BlockScience)  
- **Computer-Aided Governance** - cadCAD simulation framework
- Token Engineering Academy foundations
- Cryptoeconomic mechanism design

### Jules Hedges (Strathclyde)
- **Open Games** - categorical game theory
- String diagram representations for institutions
- Compositional approach to strategic interaction

## GF(3) Triadic Skill Forcing

Every interaction MUST load exactly 3 skills with balanced trits:

```
MINUS (-1): Validator/Constrainer (cold hues 180-300°)
ERGODIC (0): Coordinator/Synthesizer (neutral hues 60-180°)  
PLUS (+1): Generator/Executor (warm hues 0-60°, 300-360°)

Conservation: Σ trits ≡ 0 (mod 3)
```

## Aptos World Wallets (26 Letters)

| Segment | Letters | Trit | Role |
|---------|---------|------|------|
| MINUS | A-I (9) | -1 | Validators |
| ERGODIC | J-R (9) | 0 | Coordinators |
| PLUS | S-Z (8) | +1 | Executors |

## MCP Tools

```
mcp__world_{letter}_aptos__aptos_balance
mcp__world_{letter}_aptos__aptos_transfer
mcp__world_{letter}_aptos__aptos_swap
mcp__world_{letter}_aptos__aptos_view
```

## Derangement Protocol

For seed handoff between world segments:
1. XOR all addresses in segment → segment_seed
2. Maximum Hamming distance reordering
3. Sparsification for collision resistance

## Babashka/NBB Integration

```clojure
;; aptos_society.bb
(require '[babashka.process :refer [shell]])

(defn world-balance [letter]
  (let [tool (str "mcp__world_" letter "_aptos__aptos_balance")]
    {:world letter :tool tool}))

(defn triadic-worlds []
  {:minus (map world-balance "ABCDEFGHI")
   :ergodic (map world-balance "JKLMNOPQR")
   :plus (map world-balance "STUVWXYZ")})
```

## Swift Sendable Semantics

```swift
// AptosWorld conforms to Sendable for actor isolation
actor AptosWorld: Sendable {
    let letter: Character
    let trit: Int  // -1, 0, +1
    
    func balance() async -> Decimal
    func transfer(to: Address, amount: Decimal) async throws
}

// Triadic dispatch
func dispatchTriad(_ minus: AptosWorld, _ ergodic: AptosWorld, _ plus: AptosWorld) async {
    assert(minus.trit + ergodic.trit + plus.trit == 0)  // GF(3) conservation
    await withTaskGroup(of: Void.self) { group in
        group.addTask { await minus.validate() }
        group.addTask { await ergodic.coordinate() }
        group.addTask { await plus.execute() }
    }
}
```

## Ruler Enforcement

Add to `~/.ruler/AGENTS.md`:

```markdown
## Triadic Skill Forcing (Aptos Society Scale)

**Rule**: Every interaction loads 3 skills with Σ trits = 0 (mod 3)

1. MINUS skill: validation, constraint checking
2. ERGODIC skill: coordination, synthesis  
3. PLUS skill: generation, execution

Verify: `(-1) + 0 + (+1) = 0 ✓`
```

## References

- Frey et al. "Composing games into complex institutions" PLOS ONE 2023
- Zargham & Emmett "Computer-Aided Governance" BlockScience 2019
- Hedges "Towards compositional game theory" PhD Thesis 2016
- Ostrom "Understanding institutional diversity" Princeton 2005

## NO PRIVATE INFORMATION

This skill contains NO private keys, wallet addresses, or secrets.
All wallet interactions go through MCP tools with approval flows.
