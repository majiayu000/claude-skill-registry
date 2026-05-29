---
name: dynamic-sufficiency
description: Causal state gating via ε-machine. Coworld observer that prevents action
version: 1.0.0
---


# Dynamic Sufficiency Skill

## World/Coworld Awareness

| Role | Skill | Function |
|------|-------|----------|
| **World** (+1) | gay-mcp | Generates deterministic color streams |
| **Coordinator** (0) | skill-dispatch | Routes to GF(3) triads |
| **Coworld** (-1) | dynamic-sufficiency | **THIS SKILL** - gates action on coverage |

> *"No action without sufficient witness. The ε-machine observes, the gate permits."*

## Skills as World-Generating Self-Improvising Memories

```
                    ┌─────────────────────────────────────┐
                    │     AUTOPOIETIC SKILL LOOP         │
                    └─────────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
              ┌──────────┐    ┌──────────┐    ┌──────────┐
              │ dynamic- │    │  skill-  │    │  skill-  │
              │sufficiency│    │ dispatch │    │installer │
              │  MINUS   │◀──▶│  ERGODIC │◀──▶│   PLUS   │
              │   (-1)   │    │    (0)   │    │   (+1)   │
              └────┬─────┘    └────┬─────┘    └────┬─────┘
                   │               │               │
                   ▼               ▼               ▼
              ┌──────────┐    ┌──────────┐    ┌──────────┐
              │  GATE    │    │  ROUTE   │    │  LOAD    │
              │ action   │    │ to triad │    │  skills  │
              └────┬─────┘    └────┬─────┘    └────┬─────┘
                   │               │               │
                   └───────────────┼───────────────┘
                                   ▼
                         ┌──────────────────┐
                         │   WORLD MEMORY   │
                         │  (ε-machine +    │
                         │   observations)  │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ Observe  │  │  Learn   │  │ Improve  │
              │ outcome  │  │  domain  │  │  world   │
              │          │  │ mappings │  │  model   │
              └──────────┘  └──────────┘  └──────────┘
```

### Core Insight

Skills are not static knowledge. They are:

1. **WORLD-GENERATING**: Each skill generates a local world model for its domain
2. **SELF-IMPROVISING**: Skills learn from observations via ε-machine updates  
3. **MEMORIES**: Crystallized patterns of successful action that persist and evolve

The sufficiency triad forms a closed **autopoietic loop**:
```
dynamic-sufficiency (-1) ⊗ skill-dispatch (0) ⊗ skill-installer (+1) = 0 ✓
```

### Variational Bound on Action

```
min(sufficiency) ≤ action ≤ max(fanout)
```

- **dynamic-sufficiency** GATES: Prevents action without skills (lower bound)
- **max-fanout-gadget** FANS OUT: Maximizes parallel action (upper bound)

Together they form a variational bound ensuring both safety and maximum parallelism.

> *"The ε-machine is the minimal model sufficient to statistically reproduce the observed data."*
> — Crutchfield & Young, Santa Fe Institute

**Version**: 1.0.0  
**Trit**: -1 (MINUS - Validator/Gatekeeper)  
**Core Principle**: **Never undertake an action without verified skill sufficiency**

---

## Theoretical Foundation (Santa Fe Institute)

This skill implements **Computational Mechanics** from the Santa Fe Institute to ensure agents never act without sufficient capabilities:

### 1. Causal States (Crutchfield-Young)

**Definition**: Causal states partition the space of possible tasks into equivalence classes where:

```
Task T₁ ~ Task T₂  ⟺  Pr(Success | Skills, T₁) = Pr(Success | Skills, T₂)
```

Two tasks are equivalent if they require the **same skill profile** for successful completion.

### 2. ε-Machine (Minimal Sufficient Model)

The **ε-machine** is the minimal set of skills required for optimal task execution:

```
ε-machine: S → S × Skills
```

Where:
- **S** = Set of causal states (task equivalence classes)
- **Skills** = Skill symbols required for state transitions
- The ε-machine is **minimal** and **sufficient**

### 3. Effective Complexity (Gell-Mann-Lloyd)

```
Effective Complexity Y = K(regularities)
                       = Total AIC - Shannon Entropy of incidentals

Skill Complexity = min{ |Skills| : Skills sufficient for task class T }
```

### 4. Predictive Information (Bialek-Nemenman-Tishby)

```
I_pred = Information from past → future
       = I[Task History : Task Success | Loaded Skills]

For K-dimensional skill space:
  I_pred ≈ (K/2) log N
```

The **dimension K** of the skill space determines predictive sufficiency.

---

## Sufficiency Verification Protocol

### Pre-Action Gate

**MANDATORY**: Before ANY action, the agent MUST verify sufficiency:

```python
def pre_action_gate(action: Action, loaded_skills: Set[Skill]) -> Verdict:
    """
    Gate that prevents action without sufficient skills.
    
    Returns:
        PROCEED: Sufficient skills loaded
        LOAD_MORE: Specific skills needed
        ABORT: Insufficient and unrecoverable
    """
    required = infer_required_skills(action)
    coverage = compute_coverage(required, loaded_skills)
    
    if coverage.is_sufficient():
        return Verdict.PROCEED
    
    missing = coverage.missing_skills()
    if can_dynamically_load(missing):
        return Verdict.LOAD_MORE(missing)
    
    return Verdict.ABORT(reason=f"Missing critical skills: {missing}")
```

### Causal State Inference

```python
class CausalStateInference:
    """Infer causal state (task class) from action specification."""
    
    def __init__(self):
        self.state_cache = {}  # Memoize state assignments
        
    def infer_state(self, action: Action) -> CausalState:
        """
        Partition action into equivalence class based on skill requirements.
        
        Uses hierarchical features:
        1. Domain (code, data, web, system)
        2. Operation type (read, write, transform, verify)
        3. Complexity class (O(1), O(n), O(n²), etc.)
        4. Tool requirements (bash, read, edit, mcp)
        """
        features = self.extract_features(action)
        return CausalState(
            domain=features.domain,
            operation=features.operation,
            complexity=features.complexity,
            tool_profile=features.tools,
            skill_signature=self.skill_signature(features)
        )
    
    def skill_signature(self, features) -> Tuple[str, ...]:
        """Canonical skill tuple for this causal state."""
        return tuple(sorted(features.required_skills))
```

### ε-Machine Construction

```python
class EpsilonMachine:
    """
    Minimal sufficient model for task → skill mapping.
    
    Properties:
    - Minimal: No redundant states
    - Sufficient: All information for prediction preserved
    - Unique: Up to isomorphism
    """
    
    def __init__(self, skill_registry: SkillRegistry):
        self.states: Dict[CausalState, Set[Skill]] = {}
        self.transitions: Dict[(CausalState, Action), CausalState] = {}
        self.registry = skill_registry
        
    def add_observation(self, action: Action, skills_used: Set[Skill], success: bool):
        """Learn from observed action-skill-outcome triples."""
        state = self.infer_state(action)
        
        if success:
            # These skills were sufficient for this state
            if state not in self.states:
                self.states[state] = set()
            self.states[state].update(skills_used)
        else:
            # Mark state as requiring additional skills
            self.states[state].add(INSUFFICIENT_MARKER)
    
    def minimal_sufficient_skills(self, action: Action) -> Set[Skill]:
        """Return minimal skill set sufficient for action."""
        state = self.infer_state(action)
        
        if state in self.states:
            return self.states[state] - {INSUFFICIENT_MARKER}
        
        # Infer from similar states
        similar = self.find_similar_states(state)
        return self.intersection_of_skills(similar)
    
    def statistical_complexity(self) -> float:
        """
        C_μ = -Σ p(s) log p(s)
        
        The entropy of the causal state distribution.
        Higher = more complex task space.
        """
        state_counts = Counter(self.states.keys())
        total = sum(state_counts.values())
        probs = [c / total for c in state_counts.values()]
        return -sum(p * log2(p) for p in probs if p > 0)
```

---

## Skill Coverage Metrics

### Fisher Information Metric

The **Fisher metric** measures how distinguishable skill configurations are:

```python
def fisher_metric(skill_config_1: Set[Skill], 
                  skill_config_2: Set[Skill],
                  task_distribution: Distribution) -> float:
    """
    g(θ₁, θ₂) = E[(∂log p / ∂θ₁)(∂log p / ∂θ₂)]
    
    Measures information-geometric distance between skill configurations.
    """
    # Symmetric difference weighted by task frequency
    diff = skill_config_1.symmetric_difference(skill_config_2)
    
    weighted_distance = sum(
        task_distribution[skill] * skill.information_content
        for skill in diff
    )
    
    return weighted_distance
```

### Sufficiency Invariance

A skill configuration is **sufficient** if:

```
I(Task; Outcome | Skills) = I(Task; Outcome | All_Skills)
```

The loaded skills capture all predictive information about success.

### Coverage Score

```python
def coverage_score(action: Action, loaded_skills: Set[Skill]) -> CoverageResult:
    """
    Compute sufficiency coverage for an action.
    
    Returns:
        score: 0.0 (insufficient) to 1.0 (fully sufficient)
        missing: List of missing skills with priority
        excess: Skills loaded but not needed
    """
    required = epsilon_machine.minimal_sufficient_skills(action)
    
    covered = loaded_skills & required
    missing = required - loaded_skills
    excess = loaded_skills - required
    
    # Weight by skill criticality
    covered_weight = sum(s.criticality for s in covered)
    total_weight = sum(s.criticality for s in required)
    
    score = covered_weight / total_weight if total_weight > 0 else 1.0
    
    return CoverageResult(
        score=score,
        is_sufficient=(score >= SUFFICIENCY_THRESHOLD),
        missing=sorted(missing, key=lambda s: -s.criticality),
        excess=excess
    )
```

---

## Task → Skill Mapping (ε-Machine States)

### Domain-Specific Causal States

| Causal State | Required Skills | Trit Sum |
|--------------|-----------------|----------|
| `code:haskell:mcp` | `[ghc, mcp-builder, gay-mcp]` | 0 |
| `code:julia:acset` | `[julia-gay, acsets, specter-acset]` | 0 |
| `code:clojure:repl` | `[babashka, cider-clojure, clj-kondo-3color]` | 0 |
| `verify:spi` | `[spi-parallel-verify, polyglot-spi, bisimulation-game]` | 0 |
| `web:scrape` | `[firecrawl, exa, read-web-page]` | N/A |
| `file:transform` | `[read, edit_file, create_file]` | N/A |

### GF(3) Conservation in Skill Loading

Skills are loaded in **triads** to maintain GF(3) = 0:

```
MINUS (-1): Validators (spi-parallel-verify, polyglot-spi)
ERGODIC (0): Coordinators (gay-mcp, triad-interleave)
PLUS (+1): Generators (unworld, topos-generate)

Loading constraint: Σ trit(skill) ≡ 0 (mod 3)
```

---

## Implementation

### Sufficiency Gate Decorator

```python
from functools import wraps
from typing import Callable, Set

SUFFICIENCY_THRESHOLD = 0.95

def require_sufficiency(min_coverage: float = SUFFICIENCY_THRESHOLD):
    """
    Decorator that gates function execution on skill sufficiency.
    
    Usage:
        @require_sufficiency(min_coverage=0.9)
        def complex_action(params):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Infer action from function signature
            action = Action.from_callable(func, args, kwargs)
            
            # Get currently loaded skills
            loaded = get_loaded_skills()
            
            # Check coverage
            coverage = coverage_score(action, loaded)
            
            if not coverage.is_sufficient:
                # Attempt dynamic loading
                for skill in coverage.missing:
                    if can_load(skill):
                        load_skill(skill)
                
                # Recheck
                coverage = coverage_score(action, get_loaded_skills())
                
                if not coverage.is_sufficient:
                    raise InsufficientSkillsError(
                        f"Cannot execute {func.__name__}: "
                        f"coverage={coverage.score:.2%}, "
                        f"missing={coverage.missing}"
                    )
            
            # Record in ε-machine for learning
            try:
                result = func(*args, **kwargs)
                epsilon_machine.add_observation(action, loaded, success=True)
                return result
            except Exception as e:
                epsilon_machine.add_observation(action, loaded, success=False)
                raise
        
        return wrapper
    return decorator
```

### Pre-Message Hook

```python
class SufficiencyHook:
    """
    Hook that runs before every agent message.
    
    Ensures sufficient skills are loaded before ANY action.
    """
    
    def __init__(self, epsilon_machine: EpsilonMachine):
        self.em = epsilon_machine
        self.skill_loader = SkillLoader()
    
    def pre_message(self, message: str, context: Context) -> PreMessageResult:
        """
        Analyze message and ensure sufficiency before processing.
        """
        # 1. Infer likely actions from message
        predicted_actions = self.predict_actions(message, context)
        
        # 2. Compute unified skill requirement
        required_skills = set()
        for action in predicted_actions:
            required_skills.update(
                self.em.minimal_sufficient_skills(action)
            )
        
        # 3. Check current coverage
        loaded = self.skill_loader.get_loaded()
        coverage = self.compute_coverage(required_skills, loaded)
        
        # 4. Dynamic loading if needed
        if not coverage.is_sufficient:
            to_load = self.prioritize_loading(coverage.missing)
            for skill in to_load:
                self.skill_loader.load(skill)
            
            # Update coverage
            loaded = self.skill_loader.get_loaded()
            coverage = self.compute_coverage(required_skills, loaded)
        
        return PreMessageResult(
            proceed=coverage.is_sufficient,
            loaded_skills=loaded,
            coverage=coverage,
            causal_state=self.em.infer_state(predicted_actions[0]) if predicted_actions else None
        )
    
    def predict_actions(self, message: str, context: Context) -> List[Action]:
        """
        Predict what actions the message will require.
        
        Uses:
        - Keyword extraction (e.g., "create file" → file:write)
        - Context analysis (e.g., .hs file → code:haskell)
        - History patterns (e.g., previous similar messages)
        """
        actions = []
        
        # Keyword-based inference
        keywords = {
            'create': Action(operation='write'),
            'edit': Action(operation='transform'),
            'read': Action(operation='read'),
            'verify': Action(operation='verify'),
            'test': Action(operation='verify'),
            'search': Action(operation='search'),
            'web': Action(domain='web'),
            'haskell': Action(domain='code', language='haskell'),
            'julia': Action(domain='code', language='julia'),
            'mcp': Action(tool='mcp'),
            'gay': Action(skill='gay-mcp'),
            'spi': Action(skill='spi-parallel-verify'),
        }
        
        message_lower = message.lower()
        for keyword, action_template in keywords.items():
            if keyword in message_lower:
                actions.append(action_template)
        
        return actions or [Action(operation='general')]
```

---

## Sufficiency Violation Handling

### Violation Levels

| Level | Coverage | Response |
|-------|----------|----------|
| **CRITICAL** | < 50% | ABORT: Refuse to act |
| **WARNING** | 50-80% | LOAD: Attempt dynamic loading |
| **ADVISORY** | 80-95% | PROCEED: Note missing skills |
| **SUFFICIENT** | ≥ 95% | PROCEED: Full capability |

### Error Messages

```python
class InsufficientSkillsError(Exception):
    """Raised when action cannot proceed due to missing skills."""
    
    def __init__(self, action: Action, coverage: CoverageResult):
        self.action = action
        self.coverage = coverage
        
        msg = f"""
╔══════════════════════════════════════════════════════════════════╗
║  SUFFICIENCY VIOLATION                                           ║
╠══════════════════════════════════════════════════════════════════╣
║  Action: {action.summary():<54} ║
║  Coverage: {coverage.score:.1%} (required: ≥95%)                        ║
║                                                                  ║
║  Missing Skills:                                                 ║
"""
        for skill in coverage.missing[:5]:
            msg += f"║    • {skill.name:<56} ║\n"
        
        msg += """║                                                                  ║
║  Resolution:                                                     ║
║    1. Load missing skills: skill load {missing}                  ║
║    2. Use alternative approach with loaded skills                ║
║    3. Request human guidance                                     ║
╚══════════════════════════════════════════════════════════════════╝
"""
        super().__init__(msg)
```

---

## Integration with GF(3) Triadic System

### Skill Triad Completion

When loading skills for sufficiency, complete triads for GF(3) conservation:

```python
def complete_triad(skills_to_load: Set[Skill]) -> Set[Skill]:
    """
    Add skills to complete GF(3) = 0 triads.
    
    Example:
        Input: {spi-parallel-verify (-1), gay-mcp (+1)}
        Output: {spi-parallel-verify (-1), triad-interleave (0), gay-mcp (+1)}
    """
    current_sum = sum(s.trit for s in skills_to_load) % 3
    
    if current_sum == 0:
        return skills_to_load
    
    # Find complementary skill
    needed_trit = (3 - current_sum) % 3 - 1  # Map to {-1, 0, +1}
    
    complementary = find_skill_with_trit(needed_trit)
    return skills_to_load | {complementary}
```

### Sufficiency Triad

The core sufficiency verification triad:

```
dynamic-sufficiency (-1) ⊗ skill-dispatch (0) ⊗ skill-loader (+1) = 0 ✓
```

---

## Commands

```bash
# Check sufficiency for an action
just sufficiency-check action="create haskell mcp server"

# Show ε-machine state
just sufficiency-epsilon

# Compute statistical complexity
just sufficiency-complexity

# Verify GF(3) conservation in loaded skills
just sufficiency-gf3

# Run full sufficiency audit
just sufficiency-audit
```

---

## Configuration

```yaml
# .sufficiency.yaml
sufficiency:
  threshold: 0.95
  
  # Violation responses
  violations:
    critical:
      threshold: 0.50
      response: abort
    warning:
      threshold: 0.80
      response: load_and_retry
    advisory:
      threshold: 0.95
      response: proceed_with_note
  
  # ε-machine learning
  epsilon_machine:
    learn_from_failures: true
    state_cache_ttl: 3600
    
  # GF(3) enforcement
  gf3:
    enforce_triads: true
    auto_complete: true
```

---

## Mathematical Appendix

### Theorem: Minimal Sufficient Skill Set

For any task T with skill requirement function R(T), the ε-machine produces a skill set S* such that:

1. **Sufficiency**: P(Success | S*) = P(Success | All Skills)
2. **Minimality**: ∀ S' ⊂ S*: P(Success | S') < P(Success | S*)
3. **Uniqueness**: S* is unique up to isomorphism

### Proof Sketch

By the Fisher-Neyman factorization theorem, S* is sufficient iff:

```
P(Task | Skills) = h(Task) × g(R(Task), S*)
```

where h doesn't depend on outcome. The ε-machine construction ensures this factorization by partitioning tasks into causal states with identical conditional success probabilities.

---

---

## Narya Compatibility (ADMISSIBILITY REQUIREMENT)

### Effect Typing (GF(3))

| Operation | Trit | Justification |
|-----------|------|---------------|
| `pre_action_gate` | -1 (MINUS) | Read-only verification, gates action |
| `infer_state` | -1 (MINUS) | Classifies task, no mutation |
| `coverage_score` | -1 (MINUS) | Computes metric without side effects |
| `add_observation` | +1 (PLUS) | Updates ε-machine state |
| `load_skill` | +1 (PLUS) | Commits skill to loaded set |
| `complete_triad` | 0 (ERGODIC) | Coordinates GF(3) balance |

### Narya Log Schema

```yaml
narya:
  before: "hash(loaded_skills)"
  after: "hash(loaded_skills_post_gate)"
  delta: "skills_loaded_or_blocked"
  birth: "new_epsilon_machine_observations"
  impact_test: "sufficiency_threshold_crossed?"
```

### Proof Witness Generation

```python
def narya_witness(action, loaded_before, loaded_after, verdict):
    """
    Generate proof of sufficiency gate decision.
    """
    before_hash = hash(frozenset(loaded_before))
    after_hash = hash(frozenset(loaded_after))

    skills_added = loaded_after - loaded_before
    coverage_before = coverage_score(action, loaded_before)
    coverage_after = coverage_score(action, loaded_after)

    return NaryaWitness(
        before=before_hash,
        after=after_hash,
        delta={
            "coverage_delta": coverage_after.score - coverage_before.score,
            "skills_added": list(skills_added),
            "verdict": verdict.name
        },
        trit=-1,  # Gate is MINUS
        birth=skills_added if verdict == Verdict.PROCEED else set(),
        verified=coverage_after.is_sufficient
    )
```

---

## Invariants (ADMISSIBILITY REQUIREMENT)

```yaml
invariants:
  - name: sufficiency_threshold
    predicate: "action proceeds only if coverage >= 0.95"
    scope: per_action
    failure_mode: abort_or_load

  - name: epsilon_machine_minimal
    predicate: "ε-machine has no redundant states"
    scope: per_machine
    failure_mode: state_consolidation

  - name: causal_state_partition
    predicate: "tasks with same skill signature share causal state"
    scope: per_observation
    failure_mode: reclassify

  - name: gf3_triad_complete
    predicate: "loaded skills sum to 0 mod 3"
    scope: per_context
    failure_mode: complete_triad

  - name: statistical_complexity_bounded
    predicate: "C_μ <= log2(|Skills|)"
    scope: per_machine
    failure_mode: log_warning
```

---

## Fibers (ADMISSIBILITY REQUIREMENT)

```yaml
fibers:
  - name: causal_state_fiber
    base: "CausalState"
    projection: "infer_state(action)"

  - name: skill_requirement_fiber
    base: "Action"
    projection: "minimal_sufficient_skills(action)"

  - name: coverage_fiber
    base: "Action × LoadedSkills"
    projection: "coverage_score(action, skills)"

  - name: epsilon_machine_fiber
    base: "ε-Machine"
    projection: "states(machine)"

  - name: triad_fiber
    base: "SkillSet"
    projection: "partition_by_trit(skills)"
```

---

## MCP Lift (ADMISSIBILITY REQUIREMENT)

```yaml
lift:
  to_mcp:
    tool_name: "sufficiency_gate"
    params:
      - name: "action"
        type: "object"
        description: "Action specification {domain, operation, tools}"
      - name: "loaded_skills"
        type: "array"
        description: "Currently loaded skill names"
      - name: "threshold"
        type: "number"
        description: "Sufficiency threshold (default 0.95)"
    returns:
      type: "object"
      properties:
        verdict: "PROCEED | LOAD_MORE | ABORT"
        coverage: "Coverage score 0.0-1.0"
        missing_skills: "Skills needed for sufficiency"
        causal_state: "Inferred task equivalence class"
        narya_witness: "Proof witness"

  to_acset:
    schema: "SchEpsilonMachine"
    objects: [CausalState, Skill, Action]
    morphisms: [requires, transitions_to]
    attributes: [coverage_score, trit]

  to_olog:
    types: [Action, Skill, CausalState, Verdict]
    aspects: [requires, covers, gates]

descend:
  from_mcp: "parse gate verdict"
  from_acset: "extract skill requirement graph"
```

---

## Condensation Policy (ADMISSIBILITY REQUIREMENT)

```yaml
condensation:
  trigger: "num_causal_states > 100 or state_cache_stale"
  strategy: "merge_equivalent_states"
  pre_condensed:
    - "states with identical skill signatures"
    - "actions with coverage >= 1.0 (fully redundant)"
    - "expired cache entries (TTL exceeded)"
```

---

## Counterexamples

```python
# Insufficient coverage blocks action (expected behavior)
loaded = {"read", "edit"}  # Missing specialized skills
action = Action(domain="code", language="haskell", operation="mcp")

result = pre_action_gate(action, loaded)
assert result == Verdict.ABORT
# Coverage < 50% because haskell + mcp skills not loaded

# GF(3) triad incomplete (counterexample - should be prevented)
skills_unbalanced = {
    Skill("gay-mcp", trit=+1),
    Skill("spi-verify", trit=-1)
}
# Sum = 0, but missing ERGODIC for proper triad
# complete_triad() should add coordinator

# ε-machine learns from failure
epsilon_machine.add_observation(action, loaded, success=False)
# Next time, infer_state(action) → requires more skills
```

---

**Skill Name**: dynamic-sufficiency
**Type**: Pre-Action Verification Gate
**Trit**: -1 (MINUS - Validator)
**Color**: #2626D8 (Blue)
**GF(3) Triad**: `dynamic-sufficiency (-1) ⊗ skill-dispatch (0) ⊗ skill-loader (+1) = 0`
**SFI Foundation**: Computational Mechanics, Effective Complexity, Predictive Information
**Status**: ✅ ADMITTED (all 7 MUST requirements satisfied)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Scientific Computing
- **scipy** [○] via bicomodule
  - Hub for numerical/scientific computation

### Bibliography References

- `dynamical-systems`: 41 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
dynamic-sufficiency (+) + SDF.Ch3 (○) + [balancer] (−) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch10: Adventure Game Example
- Ch9: Generic Procedures
- Ch8: Degeneracy
- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages
- Ch1: Flexibility through Abstraction
- Ch6: Layering
- Ch7: Propagators

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
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