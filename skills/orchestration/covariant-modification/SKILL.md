---
name: covariant-modification
description: Unified skill modification with covariant transport, Darwin Gödel Machine evolution, and MCP Tasks self-rewriting. GF(3) conserved.
version: 1.0.0
---


# Covariant Modification Skill

**Trit**: 0 (ERGODIC - coordinator)
**Color**: Green (#26D826)

## Overview

**Covariant Modification** unifies three skill patterns for safe, structure-preserving self-modification:

| Component Skill | Trit | Role | Pattern |
|-----------------|------|------|---------|
| `codex-self-rewriting` | +1 | Generator | Lisp-machine self-modification via MCP Tasks |
| `self-evolving-agent` | 0 | Coordinator | Darwin Gödel Machine evolution loops |
| `covariant-fibrations` | -1 | Validator | Type families respect directed morphisms |

**GF(3)**: (+1) + (0) + (-1) = 0 ✓

## Core Concept: Covariant Transport

When skill `A` modifies itself, dependent skills `B` must transform **covariantly**:

```
                    modify_A
        Skill_A ─────────────→ Skill_A'
           │                      │
    uses   │    COVARIANT        │ uses'
           │    TRANSPORT        │
           ↓                      ↓
        Skill_B ─────────────→ Skill_B'
                  transport_f
```

### Agda Definition

```agda
-- Skill fibration over dependency base
skill-fibration : (Base : SkillGraph) → (Fiber : Base → SkillVersion) → Type

-- Covariant transport along modification morphisms
cov-transport : {A A' : Skill} {P : SkillDeps A → Type}
              → (f : Modification A A')
              → P (deps A) → P (deps A')

-- Functoriality
cov-comp : ∀ (f : Mod A A') (g : Mod A' A'') →
           cov-transport (g ∘ f) ≡ cov-transport g ∘ cov-transport f
```

## MCP Tasks State Machine

From `codex-self-rewriting`:

```
                    ┌─────────────┐
                    │   working   │ LIVE (+1)
                    │   (modify)  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  completed  │ │input_required│ │   failed    │
    │ BACKFILL(-1)│ │  VERIFY (0) │ │ BACKFILL(-1)│
    └─────────────┘ └─────────────┘ └─────────────┘
```

## Darwin Gödel Machine Integration

```python
class CovariantDGM(DarwinGodelMachine):
    """Darwin Gödel Machine with covariant skill transport."""
    
    def __init__(self, skill_fibration: SkillFibration, ...):
        super().__init__(...)
        self.fibration = skill_fibration
    
    def mutate(self, agent: Agent) -> Agent:
        """Mutate agent while preserving fibration structure."""
        new_code = self.mutator(agent)
        
        # Transport dependent skills covariantly
        modified_deps = {}
        for dep_skill in self.fibration.dependencies(agent):
            modified_deps[dep_skill] = self.fibration.transport(
                modification=Diff(agent.code, new_code),
                target=dep_skill
            )
        
        return Agent(
            code=new_code,
            dependencies=modified_deps,
            generation=self.generation
        )
```

## Multi-Agent Sheaf Gluing

```python
class CovariantModificationSheaf:
    """Sheaf ensuring consistent modifications across agents."""
    
    def glue(self, local_mods: Dict[Agent, Modification]) -> GlobalMod:
        """Glue compatible local modifications into global section."""
        for a1, a2 in combinations(local_mods.keys(), 2):
            overlap = self.overlap(a1, a2)
            if overlap:
                r1 = self.restrict(local_mods[a1], overlap)
                r2 = self.restrict(local_mods[a2], overlap)
                if not self.compatible(r1, r2):
                    raise CovarianceViolation(a1, a2, overlap)
        return self.colimit(local_mods)
```

## Triadic Modification Operators

| Trit | Effect | Operator | Example |
|------|--------|----------|---------|
| +1 | **Generative** | Create new structure | Add skill capability |
| 0 | **Neutral** | Refactor/reorganize | Rename function |
| -1 | **Destructive** | Remove/simplify | Delete unused code |

**Conservation Law**: 
```
Σ trit(modification_i) ≡ 0 (mod 3)
```

## GF(3) Triads

```
covariant-fibrations (-1) ⊗ covariant-modification (0) ⊗ codex-self-rewriting (+1) = 0 ✓
temporal-coalgebra (-1) ⊗ covariant-modification (0) ⊗ self-evolving-agent (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ covariant-modification (0) ⊗ gay-mcp (+1) = 0 ✓
```

## Commands

```bash
# Verify covariant modification
just covariant-verify skill=my-skill mod=v1.1

# Run DGM evolution with covariance check
just dgm-evolve --covariant --generations=50

# Check GF(3) conservation
just gf3-audit modified-skills/

# Apply modification with transport
just covariant-modify skill=target mod=change.diff
```

## Related Skills

- `covariant-fibrations` (-1): Type transport validation
- `self-evolving-agent` (0): DGM evolution patterns
- `codex-self-rewriting` (+1): MCP Tasks self-modification
- `bisimulation-game` (-1): Observational equivalence verification

## See Also

- [Covariant Fibrations in Directed Type Theory](https://arxiv.org/abs/2211.01602)
- [Darwin Gödel Machine](https://hf.co/papers/2505.22954)
- [MCP Tasks Specification](https://modelcontextprotocol.io/specification/draft/basic/utilities/tasks)



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