---
name: anoma-intents
description: Anoma intent-centric architecture for cross-chain obstruction passing with Geb semantics and Juvix compilation
version: 1.0.0
---


# Anoma Intents (0)

> Intent-centric cross-chain messaging with categorical semantics

**Trit**: 0 (ERGODIC - coordination)
**Role**: Cross-chain obstruction routing

## Core Concept

Anoma's intent-centric architecture enables **cross-chain obstruction passing**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ANOMA INTENT ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  APTOS                    ANOMA                      TARGET CHAIN          │
│  ┌────────────────┐      ┌────────────────┐        ┌────────────────┐      │
│  │ Obstruction    │      │ Intent Machine │        │ Obstruction    │      │
│  │ Hot Potato     │─────►│                │───────►│ Receiver       │      │
│  │                │      │ - Match        │        │                │      │
│  │ Intent:        │      │ - Route        │        │ Intent:        │      │
│  │   nullify(obs) │      │ - Verify GF(3) │        │   commit(obs)  │      │
│  └────────────────┘      └────────────────┘        └────────────────┘      │
│                                 │                                           │
│                                 ▼                                           │
│                          ┌────────────┐                                    │
│                          │   Solver   │                                    │
│                          │ VCG fee    │                                    │
│                          │ (-1 trit)  │                                    │
│                          └────────────┘                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Intent as Categorical Morphism

From Geb: intents are morphisms in a bicartesian closed category.

```lisp
;; Intent structure in Geb
(define intent-type
  (prod 
    (prod address address)         ; (owner, solver)
    (prod resource-type            ; nullify (give)
          resource-type)))         ; commit (receive)

;; Obstruction pass intent
(define (obstruction-pass-intent owner obs target-chain)
  (make-intent
    :owner owner
    :nullify (obstruction-resource obs)
    :commit (receipt-resource target-chain obs)
    :constraint (vcg-payment-constraint (h1-class obs))))
```

## Cross-Chain Obstruction Flow

### Step 1: Create Intent on Aptos

```move
// From obstruction_hot_potato.move
public entry fun create_pass_intent(
    player: &signer,
    obstruction_idx: u64,
    target_chain: vector<u8>,
    max_vcg_payment: u64,
) acquires Player {
    let player_data = borrow_global_mut<Player>(signer::address_of(player));
    let obs = vector::borrow(&player_data.obstructions, obstruction_idx);
    
    // Create intent: nullify obstruction, receive receipt
    let intent = Intent {
        owner: signer::address_of(player),
        nullify: obs,
        commit: CrossChainReceipt { chain: target_chain, obs_hash: hash(obs) },
        vcg_constraint: compute_externality(obs.h1_class),
    };
    
    emit_intent(intent);
}
```

### Step 2: Solver Matches on Anoma

```python
class AnomaObstructionSolver:
    """Match cross-chain obstruction pass intents."""
    
    def match_intents(self, 
                      aptos_nullify: Intent, 
                      target_commit: Intent) -> Optional[Transaction]:
        # Verify complementary structure
        if not self.complementary(aptos_nullify, target_commit):
            return None
        
        # Compute VCG payment
        h1_class = aptos_nullify.obstruction.h1_class
        vcg_payment = vcg_externality(h1_class)
        
        # Extract solver fee
        solver_fee = vcg_payment * self.extraction_rate
        
        # Build matched transaction
        return Transaction(
            nullifications=[aptos_nullify.nullify],
            commitments=[target_commit.commit],
            payments=[
                Payment(aptos_nullify.owner, vcg_payment),
                Payment(self.address, solver_fee)
            ],
            gf3_sum=aptos_nullify.trit + target_commit.trit + (-1)  # Must be 0 mod 3
        )
    
    def verify_gf3(self, tx: Transaction) -> bool:
        return tx.gf3_sum % 3 == 0
```

### Step 3: Execute on Target Chain

```juvix
-- Commit obstruction on target chain
commitObstruction : Obstruction -> ChainState -> ChainState
commitObstruction obs state :=
  let newState := addObstruction state obs
  in if gf3Conserved newState
     then newState
     else abort "GF(3) violation";

-- GF(3) check
gf3Conserved : ChainState -> Bool
gf3Conserved state := 
  let sum := foldr (+) 0 (map trit (obstructions state))
  in sum `mod` 3 == 0;
```

## Juvix Intent DSL

```juvix
-- Intent type
type Intent := mkIntent {
  owner : Address;
  nullify : Resource;
  commit : Resource;
  constraints : List Constraint
};

-- Obstruction as resource
type Obstruction := mkObstruction {
  sexp : ByteArray;
  trit : GF3;
  h1Class : Nat;
  color : Word64
};

-- Cross-chain pass intent
passObstructionIntent : Address -> Obstruction -> ChainId -> Intent
passObstructionIntent owner obs targetChain :=
  mkIntent {
    owner := owner;
    nullify := obstructionResource obs;
    commit := receiptResource targetChain obs;
    constraints := [vcgConstraint (h1Class obs)]
  };

-- Compile to Geb morphism
compileIntent : Intent -> Geb.Morphism
compileIntent intent :=
  Geb.pair
    (Geb.injectLeft (nullify intent) Geb.so0)
    (Geb.injectRight Geb.so0 (commit intent));
```

## Spectral Gap Preservation

Cross-chain obstruction passing must preserve spectral gap:

```julia
function cross_chain_spectral_check(
    source_game::OpenGame,
    target_game::OpenGame,
    obstruction::Obstruction
)
    # Source chain spectral gap
    gap_source = spectral_gap(strategy_graph(source_game))
    
    # Obstruction penalty to spectral gap
    penalty = obstruction.h1_class * PENALTY_COEFFICIENT
    
    # Target chain must absorb without breaking Ramanujan
    gap_target = spectral_gap(strategy_graph(target_game))
    gap_after = gap_target - penalty
    
    ramanujan_bound = 3 - 2√2  # For d=3 (GF(3))
    
    if gap_after < ramanujan_bound
        return :expansion_failure
    else
        return :ok
    end
end
```

## GF(3) Conservation Across Chains

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GF(3) CROSS-CHAIN CONSERVATION                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Chain A (Aptos)          Solver           Chain B (Target)                │
│  emit: +1 (nullify)   +   -1 (fee)    +    0 (commit)    =  0 ✓           │
│                                                                             │
│  OR with different trit assignment:                                         │
│  emit: 0 (nullify)    +   -1 (fee)    +    +1 (commit)   =  0 ✓           │
│                                                                             │
│  The solver's -1 trit balances cross-chain flow                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Integration with Other Skills

### Neighbor Skills (GF(3) Triads)

```
anoma-intents (0) ⊗ solver-fee (-1) ⊗ geb (+1) = 0 ✓
  └─ Coordinates        └─ Extracts        └─ Semantics

anoma-intents (0) ⊗ intent-sink (-1) ⊗ free-monad-gen (+1) = 0 ✓
  └─ Routes             └─ Nullifies       └─ Generates

anoma-intents (0) ⊗ ramanujan-expander (-1) ⊗ moebius-inversion (+1) = 0 ✓
  └─ Cross-chain        └─ Validates gap   └─ Extracts cycles
```

### Skill Neighborhood

| Skill | Trit | Role in Anoma |
|-------|------|---------------|
| geb | +1 | Categorical semantics for intent types |
| solver-fee | -1 | VCG fee extraction from matched intents |
| intent-sink | -1 | Resource nullification |
| open-games | 0 | Game-theoretic intent matching |
| juvix | +1 | Intent DSL compilation |

## Commands

```bash
# Create cross-chain intent
just anoma-intent create --from aptos --to anoma --obstruction obs.json

# Match intents (solver)
just anoma-solve --intents pool.json --extraction-rate 0.03

# Verify GF(3) conservation
just anoma-verify-gf3 --transaction tx.json

# Compile Juvix intent to Geb
just juvix-compile intent.juvix --target geb
```

## References

- **anoma/anoma** - Intent machine architecture
- **anoma/geb** - Categorical semantics
- **anoma/juvix** - Intent-centric language
- **Roughgarden CS364A** - VCG mechanism design
- **Bumpus arXiv:2402.00206** - Decomposition theory
- **open-games skill** - Spectral gap → monads

---

**Trit**: 0 (ERGODIC - coordination)
**Key Property**: Cross-chain intent routing with GF(3) conservation



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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