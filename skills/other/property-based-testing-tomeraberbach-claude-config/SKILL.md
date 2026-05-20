---
name: property-based-testing
description: |
  Use when writing, reviewing, or modifying property-based tests, such as those
  using `fast-check`, or when asked to add test coverage.
user-invocable: false
---

Before starting, read: `../authoring-tests/SKILL.md`

Adhere to these principles when writing property-based tests:

- Write focused properties with focused arbitraries to properly explore slices
  of the input space.

- Prefer arbitraries that generate the desired input space directly instead of
  generating a larger input space and then filtering it down.

- Keep assertions focused only on what's straightforward to infer from the input
  arbitraries. It's often infeasible assert the full value. If no assertion
  seems feasible, then the input space is too broad.

- NEVER unnecessarily constrain an arbitrary. Only add constraints if it's
  necessary to satisfy the property or resolve performance problems.

# Common properties

- "Output is always/never X for all inputs". Example: for any number `n`,
  `Math.floor(n)` is an integer.

- "When input is X, then output is always/never Y". Example: for any array
  `data` with no duplicates, the result of removing duplicates from `data` is
  `data` itself.

- "Complex implementation X is equivalent to simpler implementation Y". Example:
  "`c` is contained inside sorted array `data` for binary search" is equivalent
  to "`c` is contained inside `data` for linear search".

- Totality: function returns (doesn't throw) for all valid inputs. Example:
  `JSON.parse(JSON.stringify(x))` never throws for serializable `x`.

- Deterministic: always returns the same output for the same input. Example: for
  any date `d`, `formatDate(d)` always returns the same string.

- Side-effect free: does not mutate the input or non-local state. Example: for
  any array `data`, `sorted(data)` leaves `data` unchanged.

- Bounded output: output is always within a known range. Example:
  `clamp(x, low, high)` always returns a value between `low` and `high`.

- Structural invariant: output always has a guaranteed shape/structure. Example:
  `partition(predicate, data)` always produces two arrays whose combined length
  equals `data.length`.

- Closure under operation: applying `f` to valid inputs always produces a valid
  output of the same type/domain. Example: `add(positiveInt, positiveInt)` is
  always a positive integer.

- Identity element: there exists an input that leaves output unchanged. Example:
  `concat(xs, [])` equals `xs`.

- Absorption/annihilation: certain inputs collapse the result regardless of the
  other. Example: `and(false, x)` is always `false`.

- Idempotent: running twice is the same as running once, either in its effect on
  non-local state or when passing its first output as its second input. Example:
  for any array `data`, `sort(sort(data))` equals `sort(data)`.

- Commutative: rearranging argument order doesn't affect output. Example: for
  any numbers `a` and `b`, `add(a, b)` equals `add(b, a)`.

- Associative: regrouping arguments for multiple calls doesn't affect output.
  Example: `concat(concat(a, b), c)` equals `concat(a, concat(b, c))`.

- Distributive: `f(a ∪ b) === f(a) ∪ f(b)`. Example: `map(f, [...xs, ...ys])`
  equals `[...map(f, xs), ...map(f, ys)]`.

- Inverse/symmetry/roundtrips: `f` and `g` are inverses of each other. Example:
  `decode(encode(x))` equals `x`.

- Transitivity: if `f(a, b)` and `f(b, c)`, then `f(a, c)`. Example: if
  `isAncestor(a, b)` and `isAncestor(b, c)`, then `isAncestor(a, c)`.

- Monotonic: if input increases (or decreases), output always changes in the
  same direction. Example: sorting more elements never produces fewer elements.

- Consistent ordering: if `a` comes before `b` in the input, the relative order
  is preserved in the output. Example: a stable sort never reorders equal
  elements relative to each other.

- Prefix/suffix closure: if `f(x)` holds, it holds for any sub-input, or
  conversely, for any superset. Example: if `isValid(data)` then
  `isValid(data.slice(0, n))` for all `n`.

These aren't exhaustive. Reason from first principles when none fits cleanly.

# `fast-check` tips

- Use `fc.clone(arb, count)` to produce multiple equal value instead of using
  `structuredClone` or `JSON.parse(JSON.stringify(...))`.

- Use `fc.uniqueArray(arb, { minLength, maxLength })` to produce unique values
  instead of using `fc.tuple(...arbs).filter(...)`.
