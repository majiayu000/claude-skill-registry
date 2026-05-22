---
name: hughes-property-based-testing
description: Test software in the style of John Hughes, inventor of QuickCheck and property-based testing. Emphasizes specifying properties that should hold for all inputs, generating random test cases, and shrinking failures to minimal examples. Use when testing algorithms, data structures, parsers, serializers, or any code with clear invariants.
---

# John Hughes Property-Based Testing Style Guide

## Overview

John Hughes, along with Koen Claessen, invented QuickCheck in 1999—a revolutionary approach to testing that generates random inputs and checks that specified properties hold. Instead of writing individual test cases, you describe *properties* that should be true for all valid inputs. When a property fails, QuickCheck *shrinks* the failing input to the smallest example that still fails, making debugging dramatically easier.

## Core Philosophy

> "Don't write tests. Write specifications. Let the computer generate the tests."

> "One property can replace a hundred example-based tests."

> "Shrinking is not optional—the minimal failing case is often the key to understanding the bug."

Property-based testing inverts the traditional approach: instead of "here's an input and expected output," you say "for all valid inputs, this property should hold." The framework then tries to prove you wrong by finding counterexamples.

## Design Principles

1. **Properties Over Examples**: Describe what should always be true, not specific cases.

2. **Random Generation**: Let the computer explore the input space.

3. **Shrinking**: Automatically minimize failing cases for debugging.

4. **Reproducibility**: Seeds make random tests deterministic.

5. **Coverage Through Volume**: Run thousands of cases, not dozens.

## The Property-Based Testing Cycle

```
┌─────────────────────────────────────────────────────────────┐
│              PROPERTY-BASED TESTING CYCLE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. DEFINE PROPERTY                                          │
│     "For all lists xs: reverse(reverse(xs)) == xs"          │
│                                                              │
│                    │                                         │
│                    ▼                                         │
│                                                              │
│  2. GENERATE RANDOM INPUTS                                   │
│     xs = [], [1], [1,2], [42,-7,0,99], ...                  │
│     (hundreds or thousands of cases)                         │
│                                                              │
│                    │                                         │
│                    ▼                                         │
│                                                              │
│  3. CHECK PROPERTY                                           │
│     For each xs: assert reverse(reverse(xs)) == xs          │
│                                                              │
│                    │                                         │
│           ┌───────┴───────┐                                 │
│           ▼               ▼                                 │
│                                                              │
│     ALL PASS          FOUND FAILURE                         │
│     ────────          ─────────────                         │
│     Property          xs = [1, 2, 3, 4, 5]                  │
│     likely holds                │                           │
│                                 ▼                           │
│                                                              │
│                    4. SHRINK TO MINIMAL CASE                │
│                       Try smaller inputs:                    │
│                       [1,2,3,4] → [1,2,3] → [1,2] → [1,2]   │
│                       Minimal failing: [1, 2]                │
│                                                              │
│                                 │                           │
│                                 ▼                           │
│                                                              │
│                    5. REPORT MINIMAL COUNTEREXAMPLE         │
│                       "Property failed for input: [1, 2]"   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Types of Properties

### Roundtrip / Inverse Properties

```haskell
-- If you do something and undo it, you get back the original
prop_reverse_reverse :: [Int] -> Bool
prop_reverse_reverse xs = reverse (reverse xs) == xs

prop_encode_decode :: String -> Bool  
prop_encode_decode s = decode (encode s) == s

prop_serialize_deserialize :: Data -> Bool
prop_serialize_deserialize d = deserialize (serialize d) == d

prop_compress_decompress :: ByteString -> Bool
prop_compress_decompress bs = decompress (compress bs) == bs
```

### Invariant Properties

```haskell
-- A property that should always hold
prop_sort_length :: [Int] -> Bool
prop_sort_length xs = length (sort xs) == length xs

prop_sort_ordered :: [Int] -> Bool
prop_sort_ordered xs = isOrdered (sort xs)
  where isOrdered [] = True
        isOrdered [_] = True
        isOrdered (a:b:rest) = a <= b && isOrdered (b:rest)

prop_sort_permutation :: [Int] -> Bool
prop_sort_permutation xs = sort xs `isPermutationOf` xs
```

### Idempotence Properties

```haskell
-- Doing it twice is the same as doing it once
prop_sort_idempotent :: [Int] -> Bool
prop_sort_idempotent xs = sort (sort xs) == sort xs

prop_normalize_idempotent :: String -> Bool
prop_normalize_idempotent s = normalize (normalize s) == normalize s

prop_dedupe_idempotent :: [Int] -> Bool
prop_dedupe_idempotent xs = dedupe (dedupe xs) == dedupe xs
```

### Equivalence / Oracle Properties

```haskell
-- Two implementations should produce the same result
prop_optimized_equals_naive :: [Int] -> Bool
prop_optimized_equals_naive xs = 
    optimizedSort xs == naiveSort xs

prop_new_equals_old :: Input -> Bool
prop_new_equals_old input = 
    newImplementation input == oldImplementation input
```

### Algebraic Properties

```haskell
-- Mathematical laws
prop_monoid_associativity :: String -> String -> String -> Bool
prop_monoid_associativity a b c = 
    (a <> b) <> c == a <> (b <> c)

prop_monoid_identity :: String -> Bool
prop_monoid_identity a = 
    a <> mempty == a && mempty <> a == a

prop_functor_identity :: Maybe Int -> Bool
prop_functor_identity mx = fmap id mx == mx

prop_functor_composition :: Maybe Int -> Bool
prop_functor_composition mx = 
    fmap (f . g) mx == (fmap f . fmap g) mx
  where f = (+1)
        g = (*2)
```

## When Using Property-Based Testing

### Always

- Define properties for pure functions with clear invariants
- Test roundtrip properties (encode/decode, serialize/deserialize)
- Use shrinking to find minimal failing cases
- Set seeds for reproducibility in CI
- Run many iterations (100+ minimum, 1000+ preferred)
- Test algebraic laws for abstract data types

### Never

- Skip shrinking (the minimal case is crucial)
- Use properties for side-effectful code without isolation
- Ignore flaky properties (fix the generator or property)
- Write properties that are just examples in disguise
- Forget to test edge cases explicitly too
- Assume passing 100 tests means correctness

### Prefer

- Properties over example-based tests
- Custom generators over default ones
- Shrinking-aware generators
- Multiple complementary properties
- Testing invariants over specific outputs
- Algebraic properties for data structures

## Code Patterns

### Property-Based Testing Framework (Python-style)

```python
import random
from typing import TypeVar, Callable, List, Any, Optional
from dataclasses import dataclass

T = TypeVar('T')


@dataclass
class TestResult:
    success: bool
    num_tests: int
    counterexample: Optional[Any] = None
    shrunk_counterexample: Optional[Any] = None
    seed: int = None


class Generator:
    """Base class for random value generators."""
    
    def generate(self, rng: random.Random, size: int) -> Any:
        raise NotImplementedError
    
    def shrink(self, value: Any) -> List[Any]:
        """Return smaller versions of value for shrinking."""
        return []


class IntGenerator(Generator):
    """Generate random integers."""
    
    def __init__(self, min_val: int = -1000, max_val: int = 1000):
        self.min_val = min_val
        self.max_val = max_val
    
    def generate(self, rng: random.Random, size: int) -> int:
        # Size influences the range
        bound = min(size, self.max_val - self.min_val)
        return rng.randint(self.min_val, self.min_val + bound)
    
    def shrink(self, value: int) -> List[int]:
        """Shrink toward zero."""
        if value == 0:
            return []
        
        shrinks = [0]  # Try zero first
        
        # Try halving
        if abs(value) > 1:
            shrinks.append(value // 2)
        
        # Try decrementing
        if value > 0:
            shrinks.append(value - 1)
        else:
            shrinks.append(value + 1)
        
        return shrinks


class ListGenerator(Generator):
    """Generate random lists."""
    
    def __init__(self, element_gen: Generator):
        self.element_gen = element_gen
    
    def generate(self, rng: random.Random, size: int) -> List:
        length = rng.randint(0, size)
        return [self.element_gen.generate(rng, size) for _ in range(length)]
    
    def shrink(self, value: List) -> List[List]:
        """Shrink by removing elements and shrinking elements."""
        shrinks = []
        
        # Empty list
        if value:
            shrinks.append([])
        
        # Remove each element
        for i in range(len(value)):
            shrinks.append(value[:i] + value[i+1:])
        
        # Shrink each element
        for i, elem in enumerate(value):
            for shrunk_elem in self.element_gen.shrink(elem):
                shrinks.append(value[:i] + [shrunk_elem] + value[i+1:])
        
        return shrinks


class StringGenerator(Generator):
    """Generate random strings."""
    
    def __init__(self, alphabet: str = "abcdefghijklmnopqrstuvwxyz"):
        self.alphabet = alphabet
    
    def generate(self, rng: random.Random, size: int) -> str:
        length = rng.randint(0, size)
        return ''.join(rng.choice(self.alphabet) for _ in range(length))
    
    def shrink(self, value: str) -> List[str]:
        shrinks = []
        
        if value:
            shrinks.append("")
            shrinks.append(value[:-1])  # Remove last
            shrinks.append(value[1:])   # Remove first
            
            # Replace chars with 'a' (simplest)
            for i, c in enumerate(value):
                if c != 'a':
                    shrinks.append(value[:i] + 'a' + value[i+1:])
        
        return shrinks


class QuickCheck:
    """Property-based testing engine."""
    
    def __init__(self, 
                 num_tests: int = 100,
                 max_shrinks: int = 100,
                 seed: int = None):
        self.num_tests = num_tests
        self.max_shrinks = max_shrinks
        self.seed = seed or random.randint(0, 2**32)
    
    def for_all(self,
                generator: Generator,
                property_fn: Callable[[Any], bool]) -> TestResult:
        """
        Test that property holds for all generated values.
        """
        rng = random.Random(self.seed)
        
        for i in range(self.num_tests):
            # Increase size gradually
            size = i * 10 // self.num_tests + 1
            
            value = generator.generate(rng, size)
            
            try:
                if not property_fn(value):
                    # Property failed - shrink to minimal case
                    shrunk = self._shrink(generator, property_fn, value)
                    
                    return TestResult(
                        success=False,
                        num_tests=i + 1,
                        counterexample=value,
                        shrunk_counterexample=shrunk,
                        seed=self.seed,
                    )
            except Exception as e:
                # Exception counts as failure
                shrunk = self._shrink(generator, property_fn, value)
                
                return TestResult(
                    success=False,
                    num_tests=i + 1,
                    counterexample=value,
                    shrunk_counterexample=shrunk,
                    seed=self.seed,
                )
        
        return TestResult(
            success=True,
            num_tests=self.num_tests,
            seed=self.seed,
        )
    
    def _shrink(self,
                generator: Generator,
                property_fn: Callable,
                value: Any) -> Any:
        """
        Shrink a failing value to the smallest failing case.
        """
        smallest = value
        shrink_count = 0
        
        while shrink_count < self.max_shrinks:
            candidates = generator.shrink(smallest)
            
            found_smaller = False
            for candidate in candidates:
                try:
                    if not property_fn(candidate):
                        # Candidate also fails - use it
                        smallest = candidate
                        found_smaller = True
                        break
                except Exception:
                    smallest = candidate
                    found_smaller = True
                    break
            
            if not found_smaller:
                break
            
            shrink_count += 1
        
        return smallest


# Convenience decorators
def property_test(generator: Generator, 
                  num_tests: int = 100):
    """Decorator for property-based tests."""
    
    def decorator(prop_fn: Callable[[Any], bool]):
        def wrapper():
            qc = QuickCheck(num_tests=num_tests)
            result = qc.for_all(generator, prop_fn)
            
            if not result.success:
                raise AssertionError(
                    f"Property '{prop_fn.__name__}' failed!\n"
                    f"Counterexample: {result.counterexample}\n"
                    f"Shrunk to: {result.shrunk_counterexample}\n"
                    f"Seed: {result.seed}"
                )
            
            return result
        
        wrapper.__name__ = prop_fn.__name__
        return wrapper
    
    return decorator
```

### Example Properties

```python
# Roundtrip property
@property_test(ListGenerator(IntGenerator()))
def prop_reverse_reverse(xs: List[int]) -> bool:
    return list(reversed(list(reversed(xs)))) == xs


# Invariant property
@property_test(ListGenerator(IntGenerator()))
def prop_sort_preserves_length(xs: List[int]) -> bool:
    return len(sorted(xs)) == len(xs)


@property_test(ListGenerator(IntGenerator()))
def prop_sort_is_ordered(xs: List[int]) -> bool:
    result = sorted(xs)
    return all(result[i] <= result[i+1] for i in range(len(result)-1))


# Idempotence property
@property_test(ListGenerator(IntGenerator()))
def prop_sort_idempotent(xs: List[int]) -> bool:
    return sorted(sorted(xs)) == sorted(xs)


# Equivalence property
@property_test(ListGenerator(IntGenerator()))
def prop_sort_equals_builtin(xs: List[int]) -> bool:
    my_sort = quick_sort(xs.copy())
    builtin = sorted(xs)
    return my_sort == builtin


# Algebraic property
@property_test(StringGenerator())
def prop_string_concat_associative(s: str) -> bool:
    # Generate three strings by splitting
    a, b, c = s[:len(s)//3], s[len(s)//3:2*len(s)//3], s[2*len(s)//3:]
    return (a + b) + c == a + (b + c)
```

### Custom Generators

```python
class UserGenerator(Generator):
    """Generate random User objects."""
    
    def __init__(self):
        self.name_gen = StringGenerator("abcdefghijklmnopqrstuvwxyz")
        self.age_gen = IntGenerator(0, 150)
        self.email_gen = StringGenerator("abcdefghijklmnopqrstuvwxyz0123456789")
    
    def generate(self, rng: random.Random, size: int) -> 'User':
        return User(
            name=self.name_gen.generate(rng, size),
            age=self.age_gen.generate(rng, size),
            email=f"{self.email_gen.generate(rng, size)}@example.com"
        )
    
    def shrink(self, user: 'User') -> List['User']:
        shrinks = []
        
        # Shrink name
        for name in self.name_gen.shrink(user.name):
            shrinks.append(User(name=name, age=user.age, email=user.email))
        
        # Shrink age
        for age in self.age_gen.shrink(user.age):
            shrinks.append(User(name=user.name, age=age, email=user.email))
        
        return shrinks


class JsonGenerator(Generator):
    """Generate random JSON-compatible data."""
    
    def generate(self, rng: random.Random, size: int) -> Any:
        if size <= 0:
            return self._generate_leaf(rng)
        
        choice = rng.choice(['leaf', 'list', 'dict'])
        
        if choice == 'leaf':
            return self._generate_leaf(rng)
        elif choice == 'list':
            length = rng.randint(0, min(size, 5))
            return [self.generate(rng, size - 1) for _ in range(length)]
        else:  # dict
            length = rng.randint(0, min(size, 5))
            return {
                f"key{i}": self.generate(rng, size - 1)
                for i in range(length)
            }
    
    def _generate_leaf(self, rng: random.Random) -> Any:
        choice = rng.choice(['null', 'bool', 'int', 'float', 'string'])
        
        if choice == 'null':
            return None
        elif choice == 'bool':
            return rng.choice([True, False])
        elif choice == 'int':
            return rng.randint(-1000, 1000)
        elif choice == 'float':
            return rng.uniform(-1000, 1000)
        else:
            return ''.join(rng.choices('abcdefghijklmnopqrstuvwxyz', k=rng.randint(0, 10)))
    
    def shrink(self, value: Any) -> List[Any]:
        if value is None or isinstance(value, bool):
            return []
        elif isinstance(value, int):
            return IntGenerator().shrink(value)
        elif isinstance(value, str):
            return StringGenerator().shrink(value)
        elif isinstance(value, list):
            return ListGenerator(self).shrink(value)
        elif isinstance(value, dict):
            shrinks = [{}]  # Empty dict
            for key in value:
                shrinks.append({k: v for k, v in value.items() if k != key})
            return shrinks
        return []
```

### Stateful Testing

```python
class StatefulTest:
    """
    Test stateful systems by generating sequences of operations.
    Hughes' approach to testing state machines.
    """
    
    def __init__(self, model_class, system_class):
        self.model_class = model_class
        self.system_class = system_class
    
    def run(self, num_tests: int = 100, max_steps: int = 50):
        """
        Generate sequences of commands and check model matches system.
        """
        rng = random.Random()
        
        for test_num in range(num_tests):
            model = self.model_class()
            system = self.system_class()
            commands = []
            
            for step in range(max_steps):
                # Generate a valid command based on current state
                cmd = self.generate_command(rng, model)
                commands.append(cmd)
                
                # Apply to both model and system
                model_result = cmd.run_model(model)
                system_result = cmd.run_system(system)
                
                # Check they match
                if model_result != system_result:
                    shrunk = self.shrink_commands(commands, model_result, system_result)
                    raise AssertionError(
                        f"Model/system mismatch!\n"
                        f"Commands: {shrunk}\n"
                        f"Model result: {model_result}\n"
                        f"System result: {system_result}"
                    )


# Example: Testing a queue
class QueueModel:
    """Simple model of a queue."""
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
        return None
    
    def pop(self):
        if self.items:
            return self.items.pop(0)
        return None
    
    def size(self):
        return len(self.items)


class PushCommand:
    def __init__(self, item):
        self.item = item
    
    def run_model(self, model):
        return model.push(self.item)
    
    def run_system(self, system):
        return system.push(self.item)


class PopCommand:
    def run_model(self, model):
        return model.pop()
    
    def run_system(self, system):
        return system.pop()
```

## Mental Model

Hughes approaches testing by asking:

1. **What properties should always hold?** Think invariants, not examples
2. **Can I roundtrip it?** encode/decode, serialize/deserialize
3. **What are the algebraic laws?** Monoid, functor, monad laws
4. **What's the simplest failing case?** Shrinking is essential
5. **Am I testing enough cases?** Hundreds or thousands, not dozens

## The Property-Based Testing Checklist

```
□ Identify properties that should hold for all inputs
□ Build or use appropriate generators
□ Ensure generators produce edge cases (empty, large, etc.)
□ Implement shrinking for custom generators
□ Run sufficient iterations (100+)
□ Set seeds for reproducibility
□ Analyze shrunk counterexamples carefully
□ Complement with example-based tests for specific cases
```

## Signature Hughes Moves

- Properties over examples
- Random generation with size control
- Shrinking to minimal counterexamples
- Roundtrip testing (encode/decode)
- Algebraic properties (associativity, identity)
- Model-based stateful testing
- Custom generators with shrinking
- Seed-based reproducibility
