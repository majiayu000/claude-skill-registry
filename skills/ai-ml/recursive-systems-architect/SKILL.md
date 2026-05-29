---
name: recursive-systems-architect
description: Designs self-referential and recursive systems that examine, modify, or generate themselves, including metacognitive architectures and strange loops.
license: MIT
---

# Recursive Systems Architect

This skill provides guidance for designing systems that operate on themselves—self-referential structures, metacognitive architectures, and recursive processes that create emergent properties through strange loops.

## Core Competencies

- **Self-Reference**: Systems that examine or modify themselves
- **Strange Loops**: Hierarchical tangles where levels fold back
- **Metacognition**: Systems that reason about their own reasoning
- **Fixed Points**: Stable states in recursive processes
- **Emergence**: Properties arising from recursive interaction

## Foundations of Recursive Systems

### What Makes a System Recursive

```
Traditional System:              Recursive System:
Input → Process → Output         Input → Process → Output
                                         ↑         │
                                         └─────────┘
                                    Process operates on
                                    itself or its outputs
```

### Types of Self-Reference

| Type | Description | Example |
|------|-------------|---------|
| Direct | System references itself explicitly | `function f() { return f; }` |
| Indirect | System references itself via another | A references B, B references A |
| Hierarchical | Higher level describes lower level | Metadata about data |
| Strange Loop | Levels fold back unexpectedly | Gödel sentences |

### The Strange Loop Pattern

Douglas Hofstadter's concept: moving through levels of a hierarchy, you unexpectedly find yourself back where you started.

```
Level 3: Meta-rules (rules about rules)
    ↑                    │
Level 2: Rules           │
    ↑                    │
Level 1: Objects         │
    ↑                    ↓
    └────────────────────┘
    Level 3 can modify Level 1,
    which affects what reaches Level 3
```

## Recursive Architecture Patterns

### Self-Modifying Code

```python
# System that modifies its own behavior
class SelfModifyingAgent:
    def __init__(self):
        self.rules = {
            'default': lambda x: x * 2
        }
        self.meta_rules = {
            'optimize': self._optimize_rules
        }

    def process(self, input):
        result = self.rules['default'](input)
        # System examines its own performance
        self._reflect_on_result(result)
        return result

    def _reflect_on_result(self, result):
        # Meta-level: decide whether to modify rules
        if self._should_modify():
            self.meta_rules['optimize']()

    def _optimize_rules(self):
        # Modify the rule that produced the result
        # This is the recursive fold-back
        self.rules['default'] = self._generate_better_rule()
```

### Metacognitive Loop

```
┌─────────────────────────────────────────────────────────┐
│                  Metacognitive Architecture              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────┐       │
│  │           Meta-Cognitive Layer               │       │
│  │  • Monitor cognitive processes               │       │
│  │  • Evaluate strategy effectiveness           │       │
│  │  • Modify cognitive strategies               │       │
│  └──────────────────┬──────────────────────────┘       │
│                     │ observes & modifies               │
│                     ▼                                   │
│  ┌─────────────────────────────────────────────┐       │
│  │           Cognitive Layer                    │       │
│  │  • Execute reasoning strategies              │       │
│  │  • Process information                       │       │
│  │  • Generate outputs                          │       │
│  └──────────────────┬──────────────────────────┘       │
│                     │ produces                          │
│                     ▼                                   │
│  ┌─────────────────────────────────────────────┐       │
│  │           Ground Layer                       │       │
│  │  • Raw inputs and outputs                    │       │
│  │  • Environmental interaction                 │       │
│  └─────────────────────────────────────────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Fixed Point Iteration

Many recursive systems seek fixed points—states where further iteration produces no change:

```python
def find_fixed_point(f, initial, tolerance=1e-6, max_iter=1000):
    """Find x where f(x) = x"""
    x = initial
    for i in range(max_iter):
        x_next = f(x)
        if abs(x_next - x) < tolerance:
            return x_next  # Fixed point found
        x = x_next
    return x  # May not have converged

# Self-consistent beliefs example
def belief_update(beliefs):
    """Update beliefs based on other beliefs"""
    new_beliefs = {}
    for key, value in beliefs.items():
        # Each belief influenced by related beliefs
        related = get_related_beliefs(beliefs, key)
        new_beliefs[key] = aggregate(value, related)
    return new_beliefs

# Find equilibrium beliefs
stable_beliefs = find_fixed_point(belief_update, initial_beliefs)
```

### Quine Pattern (Self-Reproduction)

A quine is a program that outputs its own source code:

```python
# Python quine
s = 's = %r\nprint(s %% s)'
print(s % s)
```

This pattern extends to systems that can describe or reconstruct themselves:

```python
class SelfDescribingSystem:
    """System that can generate its own specification"""

    def __init__(self, config):
        self.config = config
        self.state = {}

    def describe(self):
        """Generate a complete description of this system"""
        return {
            'type': self.__class__.__name__,
            'config': self.config,
            'state': self.state,
            'methods': self._describe_methods()
        }

    def reconstruct(self, description):
        """Create a new instance from description"""
        return self.__class__(description['config'])

    def clone(self):
        """Self-reproduction via self-description"""
        description = self.describe()
        return self.reconstruct(description)
```

## Recursive System Design Patterns

### Observer-Observed Duality

```python
class ReflectiveSystem:
    """System that is both observer and observed"""

    def __init__(self):
        self.observations = []
        self.self_model = {}

    def act(self, action):
        # Perform action
        result = self._execute(action)

        # Observe self performing action
        self._observe_self(action, result)

        # Update self-model based on observation
        self._update_self_model()

        return result

    def _observe_self(self, action, result):
        observation = {
            'action': action,
            'result': result,
            'predicted': self.self_model.get('predicted_result'),
            'surprise': self._compute_surprise()
        }
        self.observations.append(observation)

    def _update_self_model(self):
        # Self-model predicts own behavior
        # Discrepancies drive model updates
        recent = self.observations[-10:]
        self.self_model['patterns'] = self._find_patterns(recent)
        self.self_model['predicted_result'] = self._predict_next()
```

### Recursive Decomposition

Break problems into self-similar sub-problems:

```python
def recursive_solve(problem, depth=0, max_depth=10):
    """Solve by recursive decomposition"""

    # Base case: problem is atomic
    if is_atomic(problem) or depth >= max_depth:
        return solve_directly(problem)

    # Recursive case: decompose and solve
    subproblems = decompose(problem)
    subsolutions = [recursive_solve(sp, depth + 1) for sp in subproblems]

    # Combine subsolutions
    solution = combine(subsolutions)

    # Meta-level: evaluate solution quality
    if not satisfactory(solution, problem):
        # Try different decomposition
        alternative = alternative_decomposition(problem)
        return recursive_solve(alternative, depth)

    return solution
```

### Self-Referential Data Structures

```python
class RecursiveNode:
    """Node that can contain references to itself"""

    def __init__(self, value):
        self.value = value
        self.children = []
        self.references = []  # Can include self

    def add_self_reference(self):
        """Create a strange loop"""
        self.references.append(self)

    def traverse(self, visited=None):
        """Traverse handling cycles"""
        if visited is None:
            visited = set()

        if id(self) in visited:
            return ['(cycle detected)']

        visited.add(id(self))
        result = [self.value]

        for child in self.children:
            result.extend(child.traverse(visited))

        return result
```

## Emergence from Recursion

### Cellular Automata Pattern

Simple rules + self-application = complex behavior:

```python
def cellular_automaton(rule, initial_state, generations):
    """
    Rule: function mapping neighborhood to next state
    Self-reference: each cell depends on neighbors who depend on it
    """
    state = initial_state
    history = [state]

    for _ in range(generations):
        new_state = []
        for i in range(len(state)):
            # Each cell's next state depends on neighborhood
            # The rule is applied uniformly—the recursion creates complexity
            neighborhood = get_neighborhood(state, i)
            new_state.append(rule(neighborhood))
        state = new_state
        history.append(state)

    return history
```

### Self-Organizing Criticality

Systems that naturally evolve toward critical states:

```python
class SandpileModel:
    """System that self-organizes to critical state"""

    def __init__(self, size, threshold=4):
        self.grid = [[0] * size for _ in range(size)]
        self.threshold = threshold

    def add_grain(self, x, y):
        self.grid[x][y] += 1
        self._maybe_topple(x, y)

    def _maybe_topple(self, x, y):
        """Recursive toppling creates power-law distributions"""
        if self.grid[x][y] >= self.threshold:
            self.grid[x][y] -= self.threshold
            # Distribute to neighbors—may trigger their toppling
            for nx, ny in self._neighbors(x, y):
                self.grid[nx][ny] += 1
                self._maybe_topple(nx, ny)  # Recursive!
```

## Design Principles

### Termination Guarantees

Recursive systems must handle infinite loops:

1. **Depth limits**: Maximum recursion depth
2. **Change detection**: Stop when fixed point reached
3. **Energy/resource bounds**: Limited computation budget
4. **Cycle detection**: Track visited states

### Coherence Maintenance

Self-modifying systems risk incoherence:

1. **Invariant preservation**: Core properties never violated
2. **Gradual change**: Small modifications only
3. **Rollback capability**: Undo harmful changes
4. **Sandboxing**: Test modifications before applying

### Observability

Recursive systems are hard to debug:

1. **Level tagging**: Track which meta-level produced output
2. **Trace logging**: Record the recursion path
3. **State snapshots**: Capture intermediate states
4. **Visualization**: Render the strange loop structure

## References

- `references/strange-loops.md` - Hofstadter's strange loop theory
- `references/fixed-point-theory.md` - Mathematical foundations
- `references/metacognitive-patterns.md` - Metacognition implementation patterns
