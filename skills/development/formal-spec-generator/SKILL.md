---
name: formal-spec-generator
description: "Generate formal specifications (definitions, predicates, invariants, pre/post-conditions) in Isabelle/HOL or Coq from informal requirements, source code, pseudocode, or mathematical descriptions. Use when users need to: (1) Formalize algorithms or data structures, (2) Create function specifications with contracts, (3) Generate predicates and properties for verification, (4) Translate informal requirements into formal logic, (5) Specify invariants for loops or data structures, or (6) Create formal definitions for mathematical concepts. Supports both Isabelle/HOL and Coq equally."
---

# Formal Specification Generator

Generate formal specifications in Isabelle/HOL or Coq from informal descriptions, source code, or mathematical statements.

## Workflow

### 1. Understand the Input

Identify what type of input is provided:
- **Informal requirements**: Natural language descriptions (e.g., "a function that sorts a list")
- **Source code**: Existing implementations in Python, C, Java, or other languages
- **Pseudocode**: Algorithmic descriptions with semi-formal structure
- **Mathematical definitions**: Properties or theorems to formalize

### 2. Choose Target System

Ask the user which formal proof assistant to target:
- **Isabelle/HOL**: Preferred for higher-order logic, functional programming style
- **Coq**: Preferred for constructive logic, dependent types, proof automation
- **Both**: Generate specifications in both systems when requested

If not specified, default to generating both versions.

### 3. Identify Specification Components

Determine what needs to be formalized:
- **Function definitions**: Type signatures and implementations
- **Data types**: Algebraic data types, records, or inductive types
- **Predicates**: Properties and logical relationships
- **Pre/post-conditions**: Function contracts and correctness specifications
- **Invariants**: Loop invariants or data structure invariants

### 4. Generate Formal Specifications

Use the reference files for syntax and patterns:
- **Isabelle patterns**: See [isabelle_patterns.md](references/isabelle_patterns.md)
- **Coq patterns**: See [coq_patterns.md](references/coq_patterns.md)
- **Complete examples**: See [examples.md](references/examples.md)

Generate specifications that include:
1. **Type definitions** for data structures
2. **Function definitions** with proper types
3. **Predicates** describing properties
4. **Correctness specifications** relating inputs to outputs
5. **Theorem statements** (proofs can be left as `sorry` in Isabelle or `Admitted` in Coq)

### 5. Structure the Output

Organize the generated specifications clearly:

**For Isabelle/HOL:**
```isabelle
theory TheoryName
  imports Main
begin

(* Data type definitions *)
datatype ...

(* Function definitions *)
fun function_name :: "types" where
  ...

(* Predicates and properties *)
definition property_name :: "type" where
  ...

(* Correctness specifications *)
theorem theorem_name:
  "specification"
  sorry

end
```

**For Coq:**
```coq
Require Import List Arith.
Import ListNotations.

(* Data type definitions *)
Inductive ...

(* Function definitions *)
Fixpoint function_name ... :=
  ...

(* Predicates and properties *)
Definition property_name ... : Prop :=
  ...

(* Correctness theorems *)
Theorem theorem_name :
  specification.
Proof.
  Admitted.
```

## Key Principles

### Completeness
- Include all necessary type definitions
- Specify both preconditions and postconditions
- Define helper predicates when needed
- State correctness theorems even if proofs are omitted

### Clarity
- Use descriptive names for functions and predicates
- Add comments explaining non-obvious specifications
- Structure code logically (types, then functions, then properties)
- Keep specifications close to the informal description

### Correctness
- Ensure type signatures are accurate
- Match the semantics of the informal specification
- Use appropriate logical operators (∀, ∃, ⟶, ∧, ∨)
- Verify that pre/post-conditions capture the intended behavior

### Idiomatic Style
- Follow standard conventions for each system
- Use built-in libraries (List, Arith, etc.) when available
- Prefer simple definitions over complex ones
- Use pattern matching for recursive structures

## Common Patterns

### From Informal Requirements
When given natural language descriptions:
1. Extract the function signature (inputs, outputs, types)
2. Identify preconditions (assumptions about inputs)
3. Identify postconditions (guarantees about outputs)
4. Define helper predicates for complex properties
5. State the correctness theorem

Example: "A function that finds the maximum element in a non-empty list"
- Input: `list nat` (precondition: non-empty)
- Output: `nat`
- Postcondition: result is in the list AND result ≥ all elements

### From Source Code
When given existing implementations:
1. Translate the data structures to formal types
2. Translate the function logic to formal definitions
3. Infer the implicit preconditions and postconditions
4. Formalize the expected behavior as predicates
5. State correctness theorems

### From Mathematical Definitions
When given mathematical statements:
1. Choose appropriate formal types (nat, int, real, etc.)
2. Translate mathematical notation to formal syntax
3. Define predicates for mathematical properties
4. State theorems for mathematical facts

## Examples

For complete worked examples including insertion sort, binary search, and stack data structures, see [examples.md](references/examples.md).

## Tips

- **Start simple**: Begin with basic definitions, then add complexity
- **Use libraries**: Import standard libraries (List, Arith, etc.) for common operations
- **Leave proofs**: Focus on specifications; proofs can be `sorry`/`Admitted`
- **Test syntax**: Ensure generated code is syntactically valid
- **Explain choices**: Comment on design decisions in the specifications
- **Both systems**: When generating both Isabelle and Coq, ensure semantic equivalence
