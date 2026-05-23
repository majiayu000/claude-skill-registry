---
name: skill-model-checker
description: Research and develop semantic theories using ModelChecker with Z3 SMT solver. Define operators, adjust frame constraints, create examples, run tests, and report findings. Invoke with /mc or when working with model-checker, semantic theories, or Z3 constraints.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(PYTHONPATH=* pytest *), Bash(PYTHONPATH=* python *), Bash(cd Code && ./dev_cli.py *), Bash(model-checker *)
context: fork
---

# ModelChecker Research Skill

Comprehensive skill for developing and testing modular semantic theories using the ModelChecker framework with Z3 SMT solver.

## Trigger Conditions

This skill activates when:
- User invokes `/mc` command
- Working with semantic theories (logos, exclusion, imposition, bimodal)
- Defining or modifying operators
- Creating or adjusting frame constraints
- Writing model-checker examples
- Running theory tests
- Analyzing countermodels or theorem results

## Context Loading

Load these context files as needed during skill execution:

### Core ModelChecker Context (Always Load)
- @.claude/context/project/modelchecker/architecture.md - System architecture and package structure
- @.claude/context/project/modelchecker/theories.md - Theory library overview (logos, exclusion, imposition, bimodal)
- @.claude/context/project/modelchecker/z3-patterns.md - Z3 solver patterns and best practices

### Domain Context (Load When Relevant)
- @.claude/context/project/logic/domain/kripke-semantics-overview.md - Modal semantics background

### Installation Context (Load for Troubleshooting)
- @.claude/context/project/modelchecker/installation.md - Installation and CLI usage

## Sub-Commands

| Command | Purpose |
|---------|---------|
| `/mc operator <name>` | Create or modify an operator |
| `/mc frame` | Adjust frame constraints |
| `/mc example` | Create test examples |
| `/mc test [theory]` | Run tests |
| `/mc report` | Analyze and report results |

## Quick Start

### Running the Model Checker

```bash
# Development CLI (recommended)
cd Code && ./dev_cli.py examples/my_example.py

# Installed package
model-checker examples.py              # Basic run
model-checker examples.py --maximize   # Compare theories
model-checker examples.py --save       # Export results
```

### Running Tests

```bash
# All tests
PYTHONPATH=Code/src pytest Code/tests/ -v

# Specific theory
PYTHONPATH=Code/src pytest Code/src/model_checker/theory_lib/logos/tests/ -v

# With coverage
PYTHONPATH=Code/src pytest --cov=model_checker --cov-report=term-missing
```

---

## Operator Definition Workflow

### When to Use

Use `/mc operator` when:
- Adding a new logical operator
- Modifying existing operator semantics
- Implementing operator for a new subtheory

### Theory Structure

Each theory follows this pattern:
```
theory_lib/{theory}/
├── __init__.py          # Public API
├── semantic.py          # Core semantic framework
├── operators.py         # Operator registry
├── examples.py          # Test cases
└── tests/
    ├── unit/           # Unit tests
    └── integration/    # Integration tests
```

### Operator Class Template

```python
from model_checker.syntactic import Operator

class MyOperator(Operator):
    """
    Operator implementing {description}.

    Syntax: A \\myop B
    """
    name = "\\myop"      # LaTeX-style name
    arity = 2            # Number of arguments

    def true_at(self, left, right, eval_point):
        """
        Truth conditions: when is 'A \\myop B' true at eval_point?

        Args:
            left: Left argument sentence
            right: Right argument sentence
            eval_point: Dict with 'world' key containing Z3 BitVec

        Returns:
            Z3 constraint for truth condition
        """
        world = eval_point["world"]
        # Example: conjunction semantics
        return z3.And(
            self.semantics.true_at(left, eval_point),
            self.semantics.true_at(right, eval_point)
        )

    def false_at(self, left, right, eval_point):
        """
        Falsity conditions: when is 'A \\myop B' false at eval_point?
        """
        world = eval_point["world"]
        # Example: conjunction falsity (either false)
        return z3.Or(
            self.semantics.false_at(left, eval_point),
            self.semantics.false_at(right, eval_point)
        )

    def extended_verify(self, state, left, right, eval_point):
        """
        Hyperintensional verification: state verifies 'A \\myop B'.

        Args:
            state: Z3 BitVec representing a state
            left, right: Argument sentences
            eval_point: Evaluation point
        """
        # Example: fusion of verifiers
        x, y = z3.BitVecs("ver_x ver_y", self.semantics.N)
        return z3.Exists([x, y], z3.And(
            self.semantics.extended_verify(x, left, eval_point),
            self.semantics.extended_verify(y, right, eval_point),
            state == self.semantics.fusion(x, y)
        ))

    def extended_falsify(self, state, left, right, eval_point):
        """
        Hyperintensional falsification: state falsifies 'A \\myop B'.
        """
        # Example: either falsifier suffices
        return z3.Or(
            self.semantics.extended_falsify(state, left, eval_point),
            self.semantics.extended_falsify(state, right, eval_point)
        )

    def find_verifiers_and_falsifiers(self, left, right, eval_point):
        """
        Compute proposition as (verifier_set, falsifier_set).
        Used for output display.
        """
        left_prop = self.semantics.find_proposition(left, eval_point)
        right_prop = self.semantics.find_proposition(right, eval_point)

        # Combine based on operator semantics
        verifiers = set()
        for lv in left_prop[0]:
            for rv in right_prop[0]:
                verifiers.add(self.semantics.fusion(lv, rv))

        falsifiers = left_prop[1] | right_prop[1]
        return (verifiers, falsifiers)
```

### Operator Registration

Add to `operators.py`:

```python
from .my_operator import MyOperator

def load_operators(semantics):
    """Load all operators for this theory."""
    return [
        # ... existing operators ...
        MyOperator(semantics),
    ]
```

### TDD Workflow for Operators

**1. Write failing test first:**

```python
# tests/unit/test_my_operator.py
import pytest
from model_checker.builder import BuildExample

class TestMyOperator:

    def test_basic_truth(self):
        """Test basic truth conditions for \\myop."""
        example = BuildExample(
            premises=['A', 'B'],
            conclusions=['A \\myop B'],
            settings={'N': 3, 'expectation': False}  # Should be theorem
        )
        result = example.run()
        assert result.is_theorem(), "A, B should entail A \\myop B"

    def test_countermodel(self):
        """Test that invalid inference has countermodel."""
        example = BuildExample(
            premises=['A \\myop B'],
            conclusions=['A'],
            settings={'N': 3, 'expectation': True}  # Should find countermodel
        )
        result = example.run()
        assert result.has_countermodel()
```

**2. Run test - verify it fails (RED)**

```bash
PYTHONPATH=Code/src pytest Code/src/model_checker/theory_lib/{theory}/tests/unit/test_my_operator.py -v
```

**3. Implement operator (GREEN)**

**4. Refactor while tests pass**

---

## Frame Constraints Workflow

### When to Use

Use `/mc frame` when:
- Adding new semantic constraints
- Modifying world/state relationships
- Adjusting possibility conditions

### SemanticDefaults Extension Pattern

```python
from model_checker.semantic import SemanticDefaults
from model_checker.utils import ForAll, Exists
import z3

class MySemantics(SemanticDefaults):

    def __init__(self, combined_settings=None, **kwargs):
        super().__init__(combined_settings)

        # Z3 primitives
        self.verify = z3.Function(
            "verify",
            z3.BitVecSort(self.N),
            syntactic.AtomSort,
            z3.BoolSort()
        )
        self.falsify = z3.Function(
            "falsify",
            z3.BitVecSort(self.N),
            syntactic.AtomSort,
            z3.BoolSort()
        )
        self.possible = z3.Function(
            "possible",
            z3.BitVecSort(self.N),
            z3.BoolSort()
        )

        # Main evaluation point
        self.main_world = z3.BitVec("w", self.N)
        self.main_point = {"world": self.main_world}

        # Build frame constraints
        self._build_frame_constraints()

    def _build_frame_constraints(self):
        """Define the frame constraints for this semantic theory."""
        x, y = z3.BitVecs("frame_x frame_y", self.N)

        # Possibility is downward closed under parthood
        possibility_downward = ForAll([x, y], z3.Implies(
            z3.And(self.possible(y), self.is_part_of(x, y)),
            self.possible(x)
        ))

        # Main world is a world
        main_is_world = self.is_world(self.main_world)

        # Verifiers must be possible
        atom = z3.Const("frame_atom", syntactic.AtomSort)
        verifier_possible = ForAll([x, atom], z3.Implies(
            self.verify(x, atom),
            self.possible(x)
        ))

        self.frame_constraints = [
            possibility_downward,
            main_is_world,
            verifier_possible,
        ]

        # Validity conditions
        self.premise_behavior = lambda p: self.true_at(p, self.main_point)
        self.conclusion_behavior = lambda c: self.false_at(c, self.main_point)
```

### Common Constraint Patterns

| Constraint | Z3 Pattern |
|------------|------------|
| Universal | `ForAll([x], condition(x))` |
| Existential | `Exists([x], condition(x))` |
| Parthood | `self.is_part_of(x, y)` (x <= y in bitvec) |
| Fusion | `self.fusion(x, y)` (x \| y in bitvec) |
| Possibility | `self.possible(x)` |
| World | `self.is_world(x)` (maximal possible state) |

---

## Example Creation Workflow

### When to Use

Use `/mc example` when:
- Creating test cases for operators
- Validating logical relationships
- Building countermodel demonstrations

### Example Naming Convention

```
{SUBTHEORY}_{TYPE}_{NUMBER}

SUBTHEORY: EXT, MOD, CONST, CF, REL (or theory-specific)
TYPE: CM (countermodel expected), TH (theorem expected)
NUMBER: Sequential number
```

### Example Template

```python
# examples.py

# Countermodel example (expect to find model)
EXT_CM_1_premises = ['A']
EXT_CM_1_conclusions = ['B']
EXT_CM_1_settings = {
    'N': 3,                    # State space size (2^N states)
    'contingent': False,       # Force contingent propositions
    'non_null': True,          # Exclude null state verifiers
    'non_empty': True,         # Require non-empty verifier sets
    'disjoint': False,         # Allow verifier/falsifier overlap
    'max_time': 1,             # Solver timeout (seconds)
    'iterate': 1,              # Number of models to find
    'expectation': True,       # True = expect countermodel
}
EXT_CM_1_example = [
    EXT_CM_1_premises,
    EXT_CM_1_conclusions,
    EXT_CM_1_settings,
]

# Theorem example (expect no countermodel)
EXT_TH_1_premises = ['A', '(A \\rightarrow B)']
EXT_TH_1_conclusions = ['B']
EXT_TH_1_settings = {
    'N': 3,
    'max_time': 1,
    'expectation': False,      # False = expect theorem (no countermodel)
}
EXT_TH_1_example = [
    EXT_TH_1_premises,
    EXT_TH_1_conclusions,
    EXT_TH_1_settings,
]

# Organize into collections
countermodel_examples = {
    "EXT_CM_1": EXT_CM_1_example,
}

theorem_examples = {
    "EXT_TH_1": EXT_TH_1_example,
}

# Active examples for testing
example_range = {
    **countermodel_examples,
    **theorem_examples,
}
```

### Settings Reference

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `N` | int | 16 | State space size (2^N possible states) |
| `contingent` | bool | True | Force propositions to be contingent |
| `non_empty` | bool | True | Verifier/falsifier sets must be non-empty |
| `non_null` | bool | True | Exclude null state from verifiers |
| `disjoint` | bool | True | Verifiers and falsifiers must be disjoint |
| `max_time` | int | 10 | Solver timeout in seconds |
| `iterate` | int/bool | False | Number of models to find (False = 1) |
| `expectation` | bool/None | None | True=countermodel, False=theorem, None=unknown |

---

## Testing Workflow

### When to Use

Use `/mc test` when:
- Running theory tests
- Validating examples
- Checking test coverage

### Test Commands

```bash
# All tests
PYTHONPATH=Code/src pytest Code/tests/ -v

# Specific theory
PYTHONPATH=Code/src pytest Code/src/model_checker/theory_lib/logos/tests/ -v
PYTHONPATH=Code/src pytest Code/src/model_checker/theory_lib/exclusion/tests/ -v
PYTHONPATH=Code/src pytest Code/src/model_checker/theory_lib/imposition/tests/ -v
PYTHONPATH=Code/src pytest Code/src/model_checker/theory_lib/bimodal/tests/ -v

# Specific test file
PYTHONPATH=Code/src pytest Code/src/model_checker/theory_lib/logos/tests/unit/test_semantic.py -v

# With coverage
PYTHONPATH=Code/src pytest --cov=model_checker --cov-report=term-missing

# Run single test
PYTHONPATH=Code/src pytest -k "test_name" -v
```

### Test Fixture Pattern

```python
import pytest
from model_checker.theory_lib.logos import get_theory, get_examples

@pytest.fixture
def theory():
    """Get logos theory instance."""
    return get_theory()

@pytest.fixture
def examples():
    """Get example collection."""
    return get_examples()

class TestOperator:

    def test_truth_conditions(self, theory):
        """Test operator truth conditions."""
        # ... test code ...

    def test_with_examples(self, examples):
        """Test against standard examples."""
        for name, example in examples.items():
            result = example.run()
            # Validate based on expectation
```

### Common Test Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `ImportError` | PYTHONPATH not set | Add `PYTHONPATH=Code/src` |
| `z3.Z3Exception` | Constraint type mismatch | Check BitVec sizes match |
| Timeout | State space too large | Reduce N or add constraints |
| Wrong result | Semantic error | Check operator methods |

---

## Reporting Workflow

### When to Use

Use `/mc report` when:
- Analyzing countermodel structure
- Documenting logical results
- Comparing theories

### Model Output Interpretation

When a countermodel is found:

```
=== COUNTERMODEL FOUND ===

World (w): 0b1101 (state 13)

Atoms:
  A: verifiers={0b0001, 0b0101}, falsifiers={0b0010}
  B: verifiers={0b0100}, falsifiers={0b0001, 0b0011}

Premises satisfied:
  A is TRUE at w (verified by 0b0101 which is part of w)

Conclusion falsified:
  B is FALSE at w (falsified by 0b0001 which is part of w)
```

**Key interpretation:**
- **World**: The evaluation world as a bitvector (maximal possible state)
- **Verifiers**: States that make the proposition true
- **Falsifiers**: States that make the proposition false
- **Parthood**: x is part of y if (x & y) == x (bitvector AND)

### Report Template

```markdown
# Model-Checker Analysis: {Topic}

**Date**: {date}
**Theory**: {logos/exclusion/imposition/bimodal}

## Formula Under Test

Premises:
- {premise 1}
- {premise 2}

Conclusion:
- {conclusion}

## Result

{THEOREM / COUNTERMODEL FOUND}

## Analysis

{Explanation of the logical significance}

## Model Details (if countermodel)

{Countermodel structure and interpretation}

## Implications

{What this tells us about the logical system}
```

### Theory Comparison

Run same formula across theories:

```bash
# Compare all theories
model-checker examples.py --maximize

# This runs the example against all available theories
# and reports which theory finds the smallest countermodel
# (or which validates as theorem)
```

---

## Quick Reference

### Formula Syntax

| Operator | Syntax | Arity | Description |
|----------|--------|-------|-------------|
| Negation | `\\neg A` | 1 | Classical negation |
| Conjunction | `(A \\wedge B)` | 2 | And |
| Disjunction | `(A \\vee B)` | 2 | Or |
| Conditional | `(A \\rightarrow B)` | 2 | If-then |
| Biconditional | `(A \\leftrightarrow B)` | 2 | Iff |
| Necessity | `\\Box A` | 1 | Necessary |
| Possibility | `\\Diamond A` | 1 | Possible |
| Ground | `(A \\leq B)` | 2 | A grounds B |
| Essence | `(A \\sqsubseteq B)` | 2 | A is essential to B |

### Subtheory Dependencies (Logos)

```
modal → extensional, counterfactual
counterfactual → extensional
constitutive → (none)
relevance → constitutive
extensional → (none)
```

### Key Codebase Locations

| Component | Path |
|-----------|------|
| Theory library | `Code/src/model_checker/theory_lib/` |
| Logos theory | `Code/src/model_checker/theory_lib/logos/` |
| Semantic base | `Code/src/model_checker/semantic/` |
| Builder | `Code/src/model_checker/builder/` |
| Tests | `Code/tests/` |
| Examples | `Code/src/model_checker/theory_lib/*/examples.py` |

### Z3 Quick Patterns

```python
import z3
from model_checker.utils import ForAll, Exists

# BitVector state (N bits)
x = z3.BitVec("x", N)
state = z3.BitVecVal(5, N)  # Concrete state 0b101

# Parthood: x is part of y
is_part = (x & y) == x

# Fusion: combine states
fusion = x | y

# Quantified constraints
ForAll([x], z3.Implies(condition, result))
Exists([x], z3.And(condition1, condition2))

# Function declarations
verify = z3.Function("verify", z3.BitVecSort(N), AtomSort, z3.BoolSort())

# Solver usage
solver = z3.Solver()
solver.add(constraints)
if solver.check() == z3.sat:
    model = solver.model()
    value = model.evaluate(expression)
```

## Error Recovery

### Import Errors

```bash
# Verify PYTHONPATH
echo $PYTHONPATH
# Should include Code/src

# Test import
PYTHONPATH=Code/src python -c "from model_checker import BuildExample"
```

### Solver Timeout

Reduce state space:
```python
settings = {
    'N': 3,      # Smaller state space
    'max_time': 5,
}
```

### Z3 Type Errors

Check BitVec sizes match:
```python
# All states must use same N
x = z3.BitVec("x", self.N)  # Use self.N consistently
```

## Additional Resources

- **Architecture**: `Code/docs/core/ARCHITECTURE.md`
- **Testing Guide**: `Code/docs/core/TESTING_GUIDE.md`
- **API Docs**: `Code/src/model_checker/README.md`
- **Theory Docs**: `Code/src/model_checker/theory_lib/logos/README.md`
