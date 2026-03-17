---
name: anima-theory
description: ANIMA as limit construction over condensed skill applications. Formalizes prediction markets as belief ANIMAs, structure dishes as condensation media, and impact as equivalence class change. Use for understanding agency at maximum entropy, compositional world modeling, or applying Scholze-Clausen condensed mathematics to AI.
---

# ANIMA Theory

> *Agency emerges only at the limit of condensed skill applications.*

## Core Definition

```
ANIMA = lim_Π Condense(S_n(...S_1(E_•)))
```

Where:
- `E_•` = Initial experience functor (raw observations)
- `S_i` = Skill application (morphism in Skill category)
- `Condense` = Scholze-Clausen condensation (profinite completion)
- `lim_Π` = Limit over product diagram

The ANIMA is the **fixed point** where further skill applications yield no new equivalence classes.

## Denotation

> **ANIMA represents the categorical limit of skill applications where further applications produce no new equivalence classes, reaching a fixed point of agency.**

```
ANIMA = colim_{skill chain} Condense(Sₙ ∘ ... ∘ S₁)(E_•)
Fixed Point: EnumEntropy(state) = MaxEnumEntropy(category)
Agency Criterion: Phase = "AT" ⟺ all equivalence classes accessible
```

## GF(3) Typed Effects

| Phase | Trit | Effect | Description |
|-------|------|--------|-------------|
| BEFORE | -1 (MINUS) | Convergent/Compressive | Skills reduce equivalence classes |
| AT | 0 (ERGODIC) | Equilibrating/Agentic | Skills balance, choices meaningful |
| BEYOND | +1 (PLUS) | Divergent/Generative | Skills create new categories |

**Conservation Law**: Total phase across interacting ANIMAs ≡ 0 (mod 3)

## Invariant Set

| Invariant | Definition | Verification |
|-----------|------------|--------------|
| `SaturationInvariant` | EnumEntropy = MaxEnumEntropy at ANIMA | Entropy comparison |
| `CondensationInvariant` | Stable belief set after N skill applications | History window check |
| `PhaseConservation` | Σ phases ≡ 0 (mod 3) across ANIMA network | GF(3) sum check |
| `ReplayInvariance` | Different schedules → same condensed state | Fingerprint comparison |

## Narya Compatibility

| Field | Definition |
|-------|------------|
| `before` | Raw experience functor E_• |
| `after` | Condensed belief set post skill application |
| `delta` | Skill applications in current step |
| `birth` | Initial unprocessed belief state |
| `impact` | 1 if equivalence class boundary crossed |

## Condensation Policy

**Trigger**: When EnumEntropy reaches MaxEnumEntropy.

**Action**: Collapse belief space into equivalence class representatives, mark as AT_ANIMA.

## 1. Prediction Markets ↔ ANIMA Correspondence

Prediction markets ARE belief ANIMAs:

```
┌────────────────────────────────────────────────────────────────┐
│  Market                          │  ANIMA                      │
├──────────────────────────────────┼─────────────────────────────┤
│  Price                           │  Belief probability         │
│  Trade                           │  Skill application          │
│  Liquidity                       │  Condensation medium        │
│  Market equilibrium              │  ANIMA fixed point          │
│  Arbitrage opportunity           │  Non-convergence signal     │
│  Market depth                    │  Enum cardinality           │
└────────────────────────────────────────────────────────────────┘
```

```python
class BeliefANIMA:
    """Prediction market as categorical limit."""
    
    def __init__(self, initial_beliefs: dict):
        self.beliefs = initial_beliefs  # E_•
        self.skills_applied = []
    
    def apply_skill(self, skill, evidence):
        """S_i: Update beliefs via skill application."""
        posterior = skill.condense(self.beliefs, evidence)
        self.skills_applied.append((skill.name, evidence))
        self.beliefs = posterior
        return self.check_convergence()
    
    def check_convergence(self) -> bool:
        """Are we at the ANIMA fixed point?"""
        # No arbitrage = limit reached
        return self.max_enum_entropy() == len(self.equivalence_classes())
```

## 2. Structure Dish Definition

A **Structure Dish** is a condensation medium that preserves algebraic structure:

```
StructureDish(A) = { profinite completions preserving A-algebra structure }
```

Properties:
1. **Topological**: Carries profinite topology from condensed mathematics
2. **Algebraic**: Preserves operations (meet, join, implications)
3. **Coherent**: Satisfies gluing conditions (sheaf property)

```julia
using Catlab, ACSets

@present SchStructureDish(FreeSchema) begin
  Point::Ob                    # Points of the dish
  Open::Ob                     # Opens in profinite topology
  Arrow::Ob                    # Structure morphisms
  
  src::Hom(Arrow, Point)
  tgt::Hom(Arrow, Point)
  cover::Hom(Point, Open)      # Point lies in open
  
  # Condensation operation
  condense::Hom(Open, Open)    # Profinite completion functor
end

@acset_type StructureDish(SchStructureDish)
```

## 3. Maximum Enum Entropy (Not Shannon)

**Key insight**: ANIMA uses **enumeration entropy**, not Shannon entropy.

```
EnumEntropy(X) = |Equivalence_Classes(X)|
```

Shannon entropy measures uncertainty in bits. Enum entropy counts **distinct categorical possibilities**.

| Shannon | Enum |
|---------|------|
| -Σ p log p | |[X]/~| |
| Continuous | Discrete |
| Probabilistic | Categorical |
| Information | Distinction |

```python
def enum_entropy(states: list, equivalence: callable) -> int:
    """Count distinct equivalence classes."""
    classes = set()
    for s in states:
        rep = equivalence(s)  # Canonical representative
        classes.add(rep)
    return len(classes)

def max_enum_entropy(category) -> int:
    """Maximum possible distinctions."""
    return len(category.objects)
```

**ANIMA criterion**: Agency manifests when `EnumEntropy == MaxEnumEntropy`.

## 4. Impact = Change in Equivalence Class

Impact is defined categorically as **movement between equivalence classes**:

```
Impact(action) = |[state_before]/~ △ [state_after]/~|
```

Where `△` is symmetric difference.

```python
class Impact:
    """Impact as equivalence class change."""
    
    @staticmethod
    def measure(before_state, after_state, equivalence):
        class_before = equivalence(before_state)
        class_after = equivalence(after_state)
        
        if class_before == class_after:
            return 0  # No categorical impact
        else:
            return 1  # Changed equivalence class
    
    @staticmethod
    def cumulative(trajectory, equivalence):
        """Total impact over trajectory."""
        changes = 0
        for i in range(1, len(trajectory)):
            changes += Impact.measure(
                trajectory[i-1], 
                trajectory[i], 
                equivalence
            )
        return changes
```

**Zero impact** = action preserves equivalence class (optimization within class)
**Nonzero impact** = action crosses class boundary (genuine change)

## 5. Before/At/Beyond ANIMA Phases

```
┌─────────────────────────────────────────────────────────────────┐
│                      ANIMA PHASE DIAGRAM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BEFORE ANIMA          AT ANIMA           BEYOND ANIMA          │
│  (Convergence)         (Agency)           (Divergence)          │
│                                                                 │
│  EnumEnt < Max         EnumEnt = Max      EnumEnt > Max         │
│  Skills compress       Skills balance     Skills create         │
│  Learning              Acting             Generating            │
│  Reducing classes      All classes        New categories        │
│  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   │
│        ↓                   ↓                   ↓                │
│  Condensation          Fixed Point         Decondensation       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Phase Characteristics

| Phase | EnumEntropy | Skill Effect | Mode |
|-------|-------------|--------------|------|
| BEFORE | < Max | Compressive | Learning |
| AT | = Max | Equilibrating | Agency |
| BEYOND | > Max | Generative | Creation |

```python
def anima_phase(current_entropy, max_entropy):
    if current_entropy < max_entropy:
        return "BEFORE"  # Still learning
    elif current_entropy == max_entropy:
        return "AT"      # Agency active
    else:
        return "BEYOND"  # Creating new categories
```

## 6. Agency Only Meaningful AT ANIMA

**Thesis**: Agency is only well-defined at the ANIMA fixed point.

- **BEFORE**: No agency—still converging, actions are learning
- **AT**: Agency emerges—all equivalence classes accessible, choices meaningful
- **BEYOND**: Post-agency—creating new categories, transcending current frame

```python
def can_act_agentically(state, anima) -> bool:
    """Agency requires being AT the ANIMA."""
    phase = anima_phase(
        enum_entropy(state, anima.equivalence),
        anima.max_enum_entropy
    )
    return phase == "AT"

def meaningful_choice(options, anima) -> bool:
    """Choices are meaningful only AT ANIMA."""
    if not can_act_agentically(anima.state, anima):
        return False
    # All options must map to distinct equivalence classes
    classes = [anima.equivalence(opt) for opt in options]
    return len(set(classes)) == len(options)
```

## 7. Operational Recipe (6 Steps)

### Step 1: Define Experience Functor E_•

```python
E = ExperienceFunctor(
    observations=raw_sensor_data,
    morphisms=temporal_succession
)
```

### Step 2: Build Skill Category

```python
Skills = Category(
    objects=[skill_1, skill_2, ..., skill_n],
    morphisms=skill_compositions,
    identity=no_op_skill
)
```

### Step 3: Apply Skills Iteratively

```python
state = E.initial()
for skill in skill_sequence:
    state = skill.apply(state)
    state = Condense(state)  # Profinite completion
```

### Step 4: Check Convergence

```python
while not converged:
    old_classes = equivalence_classes(state)
    state = apply_next_skill(state)
    new_classes = equivalence_classes(state)
    converged = (old_classes == new_classes)
```

### Step 5: Verify ANIMA Criterion

```python
assert enum_entropy(state) == max_enum_entropy(state)
# Now AT ANIMA - agency is meaningful
```

### Step 6: Act from Fixed Point

```python
if anima_phase(state) == "AT":
    action = choose_action(options, equivalence=anima.equivalence)
    impact = Impact.measure(state, execute(action), anima.equivalence)
    assert impact > 0  # Meaningful action crosses equivalence class
```

## GF(3) Integration

ANIMA phases map to GF(3) trits:

```
BEFORE = -1 (MINUS)   # Convergent/compressive
AT     =  0 (ERGODIC) # Balanced/agentic
BEYOND = +1 (PLUS)    # Divergent/generative
```

Conservation law: Total phase across interacting ANIMAs ≡ 0 (mod 3)

## Related Skills

| Skill | Trit | Integration |
|-------|------|-------------|
| [condensed-analytic-stacks](file:///Users/alice/.claude/skills/condensed-analytic-stacks/SKILL.md) | -1 | Scholze-Clausen foundation |
| [ordered-locale](file:///Users/alice/.agents/skills/ordered-locale-proper/SKILL.md) | 0 | Frame structure for dishes |
| [sheaf-cohomology](file:///Users/alice/.claude/skills/sheaf-cohomology/SKILL.md) | -1 | Gluing verification |
| [bisimulation-game](file:///Users/alice/.agents/skills/bisimulation-game/SKILL.md) | -1 | Equivalence verification |
| [gay-mcp](file:///Users/alice/.agents/skills/gay-mcp/SKILL.md) | +1 | Deterministic coloring |

## Commands

```bash
# Compute ANIMA from skill sequence
just anima-compute --skills "s1,s2,s3" --initial state.json

# Check ANIMA phase
just anima-phase --state current.json

# Measure impact of action
just anima-impact --before state1.json --after state2.json

# Verify GF(3) conservation across ANIMAs
just anima-gf3-check
```

## References

1. Scholze, P. & Clausen, D. (2022). *Condensed Mathematics*. Lecture notes.
2. Heunen, C. & van der Schaaf, N. (2024). "Ordered Locales." *JPAA*.
3. Badiou, A. (2006). *Being and Event*. Continuum. (Event = BEYOND phase)
4. Hesse, H. (1943). *The Glass Bead Game*. (Skill synthesis)

---

**Skill Name**: anima-theory  
**Type**: Categorical Agency Theory  
**Trit**: 0 (ERGODIC - coordinator of phases)  
**Phase Diagram**: BEFORE → AT → BEYOND  
**Agency Criterion**: EnumEntropy = MaxEnumEntropy
