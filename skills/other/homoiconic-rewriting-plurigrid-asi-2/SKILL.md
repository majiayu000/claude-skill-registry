---
name: homoiconic-rewriting
description: Unified homoiconic graph rewriting - λ-calculus, interaction nets, ACSets, CUDA parallelism
version: 1.0.0
trit: 0
---

# Homoiconic Rewriting

> *Code = Data = Graph = Parallel Reduction*

**Trit**: 0 (ERGODIC - coordinates the stack)

## Core Synthesis

```
┌─────────────────────────────────────────────────────────────────┐
│              HOMOICONIC REWRITING PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   λ-term ──quote──→ S-exp ──parse──→ INet ──CUDA──→ Result     │
│     │                  │               │              │         │
│   typed              data            graph         parallel     │
│   code            (homoiconic)     rewriting      reduction     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## GF(3) Balanced Dependencies

| Trit | Skill | Role |
|------|-------|------|
| +1 | `lambda-calculus` | Term generation |
| +1 | `gay-mcp` | Color generation |
| 0 | `interaction-nets` | Parallel coordination |
| 0 | `lispsyntax-acset` | Data bridge |
| -1 | `algebraic-rewriting` | Rule validation |
| -1 | `slime-lisp` | Evaluation sink |

**Sum**: (+1+1) + (0+0) + (-1-1) = 0 ✓

## The Homoiconic Property

### Level 1: S-expressions (Lisp)

```clojure
;; Code
(+ 1 2)

;; Data (same representation!)
'(+ 1 2)

;; Transform code as data
(map inc '(+ 1 2))  ; → (1 2 3)
```

### Level 2: Interaction Nets (Graphs)

```
Code (λ-term):     Data (graph):         Rewrite (reduction):
  λx. x x          ┌───┐                 ┌───┐     ┌───┐
                   │ λ │──┬──┐           │ @ │─────│ @ │
                   └─┬─┘  │  │           └─┬─┘     └─┬─┘
                     │    │  │             │         │
                   ┌─┴─┐  │  │     →       └────┬────┘
                   │ @ │──┘  │                  │
                   └─┬─┘     │               result
                     └───────┘
```

### Level 3: ACSets (Algebraic Databases)

```julia
# Code: rewrite rule
rule = Rule(L, K, R)

# Data: same representation!
rule_data = @acset RuleSchema begin
    L = [...]; K = [...]; R = [...]
end

# Transform rules as data
composed_rule = compose_rules(rule1, rule2)
```

## Key Algorithms

### 1. λ → Interaction Net Compilation

```julia
function compile_lambda_to_inet(term::LambdaTerm)::InteractionNet
    match term
        Var(x)      => wire_to(x)
        Lam(x, body) => agent(:λ, [x], compile(body))
        App(f, arg)  => agent(:@, [compile(f), compile(arg)])
    end
end
```

### 2. Parallel Reduction (CUDA-ready)

```julia
function parallel_reduce!(net::InteractionNet)
    while has_active_pairs(net)
        # Find all independent redexes (no shared wires)
        active = find_active_pairs(net)
        
        # Reduce ALL in parallel - no dependencies!
        @cuda threads=length(active) reduce_kernel!(net, active)
    end
end
```

### 3. ACSet Rewriting (DPO)

```julia
using AlgebraicRewriting

# L ← K → R (span defines rule)
rule = Rule(
    L = @acset Graph begin V=2; E=1; src=[1]; tgt=[2] end,
    K = @acset Graph begin V=1 end,
    R = @acset Graph begin V=1; E=1; src=[1]; tgt=[1] end  # self-loop
)

# Apply via double pushout
result = rewrite(rule, graph, match)
```

## CUDA Integration (Groote et al.)

### GPU Kernel for Active Pair Reduction

```cuda
__global__ void reduce_active_pairs(
    Agent* agents,
    Wire* wires, 
    int* active_pairs,
    int n_active
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n_active) return;
    
    int pair_id = active_pairs[idx];
    Agent* a1 = &agents[wires[pair_id].from];
    Agent* a2 = &agents[wires[pair_id].to];
    
    // Dispatch by agent types
    if (a1->type == CONSTRUCTOR && a2->type == CONSTRUCTOR) {
        annihilate(a1, a2, wires);
    } else if (a1->type == CONSTRUCTOR && a2->type == DUPLICATOR) {
        commute(a1, a2, wires, agents);
    } else if (a1->type == ERASER) {
        erase(a1, a2, wires);
    }
}
```

### Performance (from Eindhoven team)

| Benchmark | CPU | GPU (RTX 3090) | Speedup |
|-----------|-----|----------------|---------|
| Fibonacci(30) | 2.4s | 0.08s | 30x |
| Tree reduction | 5.1s | 0.12s | 42x |
| λ-calculus eval | 1.2s | 0.05s | 24x |

## Typed Decomposition

### Simply Typed λ-Calculus → Linear Logic → Interaction Nets

```
Type System          Linear Logic         Interaction Net
────────────         ────────────         ───────────────
A → B                !A ⊸ B               λ-agent + !-box
A × B                A ⊗ B                Constructor pair
A + B                A ⊕ B                Case agent
```

### GF(3) Type Assignment

```julia
# Types carry trits
struct TypedTerm
    term::LambdaTerm
    type::SimpleType
    trit::Int  # -1, 0, +1
end

# Conservation: well-typed terms have balanced trits
function check_gf3(t::TypedTerm)::Bool
    sum_trits(t) % 3 == 0
end
```

## Practical Commands

```bash
# Parse λ-term to S-expression
echo "(lambda (x) (x x))" | bb -e '(read)'

# Compile to interaction net (Bend/HVM)
bend compile program.bend -o program.hvm

# Run with GPU parallelism
hvm run program.hvm --cuda

# Julia ACSet rewriting
julia -e 'using AlgebraicRewriting; include("rewrite_rules.jl")'
```

## Triadic Pipelines

### Pipeline 1: λ-Calculus Optimization

```
lambda-calculus (+1) → interaction-nets (0) → algebraic-rewriting (-1)
     source              parallel reduce          validate result
```

### Pipeline 2: Colored Term Rewriting

```
gay-mcp (+1) → lispsyntax-acset (0) → slime-lisp (-1)
  color nodes      serialize            evaluate
```

### Pipeline 3: Full Stack

```
λ-term → quote → sexp → parse → inet → reduce → result → eval
  +1      0       0      0       0      -1       -1      -1
                         (balanced across pipeline)
```

## Key Authors

| Author | Contribution | Affiliation |
|--------|--------------|-------------|
| **Yves Lafont** | Interaction nets (1990) | Marseille |
| **Jan Friso Groote** | GPU term rewriting | TU Eindhoven |
| **Anton Wijs** | CUDA rewriting | TU Eindhoven |
| **Thierry Boy de la Tour** | Parallel graph rewriting | CNRS Grenoble |
| **Nathan Marz** | Specter (bidirectional nav) | Red Planet Labs |

## Literature

1. Lafont (1990) - "Interaction Nets"
2. Groote et al. (2022) - "Innermost many-sorted term rewriting on GPUs"
3. Boy de la Tour & Echahed (2020) - "Parallel rewriting of attributed graphs"
4. Mazza (2007) - "Symmetric Interaction Combinators"

## Related Skills

- `lambda-calculus` (+1) - Term generation
- `interaction-nets` (0) - Parallel semantics
- `algebraic-rewriting` (-1) - DPO/SPO rules
- `lispsyntax-acset` (0) - Sexp ↔ data bridge
- `sexp-neighborhood` (0) - Sexp skill index
- `gay-mcp` (+1) - Deterministic coloring

---

**Trit**: 0 (ERGODIC - coordinates the homoiconic stack)
**GF(3)**: Balanced across all pipelines


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
homoiconic-rewriting (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch9: Generic Procedures
- Ch1: Flexibility through Abstraction
- Ch5: Evaluation
- Ch3: Variations on an Arithmetic Theme
- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages
- Ch7: Propagators

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
