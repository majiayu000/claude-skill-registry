---
name: refinement-step-generator
description: Generate systematic refinement steps from high-level specifications to concrete implementations in Isabelle/HOL or Coq, preserving correctness obligations at each step. Use when working with formal verification, program refinement, proof development, or when translating abstract specifications into executable code while maintaining formal guarantees. Supports data refinement (abstract types → concrete structures), algorithmic refinement (specifications → algorithms), and stepwise refinement with proof obligations.
---

# Refinement Step Generator

Generate systematic refinement steps that transform high-level specifications into concrete, executable implementations while preserving correctness through formal proofs.

## Overview

Refinement is the process of transforming abstract specifications into concrete implementations through a series of correctness-preserving steps. Each refinement step:

1. Makes the specification more concrete (closer to executable code)
2. Preserves correctness through formal proof obligations
3. Maintains a clear abstraction relation between levels
4. Can be verified independently

This skill provides guidance for generating refinement steps in Isabelle/HOL and Coq.

## Refinement Workflow

```
Abstract Specification
    ↓ [Data Refinement]
Refined Data Structures
    ↓ [Algorithmic Refinement]
Concrete Algorithm
    ↓ [Implementation Refinement]
Executable Code
```

Each arrow represents a refinement step with proof obligations.

## Core Refinement Types

### 1. Data Refinement

Transform abstract data types into concrete data structures.

**Example: Set → List**

**Abstract (Isabelle):**
```isabelle
definition insert_set :: "'a ⇒ 'a set ⇒ 'a set" where
  "insert_set x S = S ∪ {x}"

definition member_set :: "'a ⇒ 'a set ⇒ bool" where
  "member_set x S = (x ∈ S)"
```

**Concrete (Isabelle):**
```isabelle
definition insert_list :: "'a ⇒ 'a list ⇒ 'a list" where
  "insert_list x xs = (if x ∈ set xs then xs else x # xs)"

definition member_list :: "'a ⇒ 'a list ⇒ bool" where
  "member_list x xs = (x ∈ set xs)"
```

**Abstraction Relation:**
```isabelle
definition abs_list :: "'a list ⇒ 'a set" where
  "abs_list xs = set xs"
```

**Proof Obligations:**
```isabelle
lemma insert_refines:
  "abs_list (insert_list x xs) = insert_set x (abs_list xs)"
  by (simp add: insert_list_def insert_set_def abs_list_def)

lemma member_refines:
  "member_list x xs = member_set x (abs_list xs)"
  by (simp add: member_list_def member_set_def abs_list_def)
```

### 2. Algorithmic Refinement

Transform specifications into algorithms.

**Example: Sorting Specification → Insertion Sort**

**Abstract (Coq):**
```coq
Definition is_sorted (l : list nat) : Prop :=
  forall i j, i < j < length l → nth i l 0 ≤ nth j l 0.

Definition sort_spec (input output : list nat) : Prop :=
  is_sorted output ∧ Permutation input output.
```

**Concrete (Coq):**
```coq
Fixpoint insert (x : nat) (l : list nat) : list nat :=
  match l with
  | [] => [x]
  | h :: t => if x <=? h then x :: l else h :: insert x t
  end.

Fixpoint insertion_sort (l : list nat) : list nat :=
  match l with
  | [] => []
  | h :: t => insert h (insertion_sort t)
  end.
```

**Proof Obligations:**
```coq
Theorem insertion_sort_correct : forall l,
  sort_spec l (insertion_sort l).
Proof.
  (* Prove is_sorted and Permutation properties *)
Qed.
```

### 3. Implementation Refinement

Transform algorithms into efficient implementations.

**Example: Naive → Optimized**

**Abstract:**
```isabelle
definition naive_reverse :: "'a list ⇒ 'a list" where
  "naive_reverse xs = rev xs"
```

**Concrete (tail-recursive):**
```isabelle
fun reverse_acc :: "'a list ⇒ 'a list ⇒ 'a list" where
  "reverse_acc [] acc = acc" |
  "reverse_acc (x # xs) acc = reverse_acc xs (x # acc)"

definition efficient_reverse :: "'a list ⇒ 'a list" where
  "efficient_reverse xs = reverse_acc xs []"
```

**Proof Obligation:**
```isabelle
lemma efficient_reverse_correct:
  "efficient_reverse xs = naive_reverse xs"
  by (simp add: efficient_reverse_def naive_reverse_def reverse_acc_correct)
```

## Refinement Process

### Step 1: Identify Abstraction Gap

Analyze the specification and identify what needs refinement:

- **Data structures**: Abstract types (sets, maps) → Concrete structures (lists, trees)
- **Operations**: Non-deterministic specs → Deterministic algorithms
- **Complexity**: Inefficient → Efficient implementations

### Step 2: Choose Refinement Strategy

Select appropriate refinement approach:

**Data Refinement:**
- Define concrete data type
- Define abstraction function
- Prove operations preserve abstraction

**Algorithmic Refinement:**
- Provide concrete algorithm
- Prove algorithm satisfies specification
- Maintain invariants

**Compositional Refinement:**
- Refine components independently
- Compose refinements
- Prove composition preserves correctness

### Step 3: Define Abstraction Relation

Establish connection between abstract and concrete levels:

**Isabelle:**
```isabelle
definition abs_rel :: "'concrete ⇒ 'abstract ⇒ bool" where
  "abs_rel c a = (abs_fun c = a)"
```

**Coq:**
```coq
Definition abs_rel (c : concrete) (a : abstract) : Prop :=
  abs_fun c = a.
```

### Step 4: Generate Proof Obligations

For each operation, prove refinement correctness:

**Forward Simulation:**
```
If: abs_rel c a
    op_concrete c = c'
Then: ∃a'. op_abstract a = a' ∧ abs_rel c' a'
```

**Backward Simulation:**
```
If: abs_rel c a
    op_abstract a = a'
Then: ∃c'. op_concrete c = c' ∧ abs_rel c' a'
```

### Step 5: Prove Obligations

Use proof tactics to discharge obligations:

**Isabelle:**
- `auto`, `simp`, `blast` for automation
- `induction` for recursive structures
- `case_tac` for case analysis

**Coq:**
- `auto`, `simpl`, `reflexivity` for automation
- `induction` for recursive proofs
- `destruct` for case analysis

## Framework-Specific Guidance

### Isabelle/HOL Refinement

For Isabelle-specific patterns and the Autoref framework, see [references/isabelle_refinement.md](references/isabelle_refinement.md).

Key features:
- Refinement framework with `⊑` relation
- Autoref for automatic refinement
- Sepref for imperative refinement
- Code generation support

### Coq Refinement

For Coq-specific patterns and refinement tactics, see [references/coq_refinement.md](references/coq_refinement.md).

Key features:
- Program for refinement with obligations
- Equations for well-founded recursion
- Refinement types
- Extraction to OCaml/Haskell

## Common Refinement Patterns

For detailed refinement patterns (data structures, algorithms, optimizations), see [references/refinement_patterns.md](references/refinement_patterns.md).

Common patterns include:
- Set → List/Tree refinement
- Map → Association list/Hash table
- Non-deterministic choice → Deterministic selection
- Specification → Divide-and-conquer algorithm
- Naive → Tail-recursive implementation

## Example: Complete Refinement

**Abstract Specification (Isabelle):**
```isabelle
definition find_spec :: "'a list ⇒ ('a ⇒ bool) ⇒ 'a option" where
  "find_spec xs P = (if ∃x ∈ set xs. P x
                     then Some (SOME x. x ∈ set xs ∧ P x)
                     else None)"
```

**Refinement Step 1: Deterministic Algorithm**
```isabelle
fun find_impl :: "'a list ⇒ ('a ⇒ bool) ⇒ 'a option" where
  "find_impl [] P = None" |
  "find_impl (x # xs) P = (if P x then Some x else find_impl xs P)"
```

**Proof Obligation:**
```isabelle
lemma find_impl_refines:
  "find_impl xs P = find_spec xs P"
proof (induction xs)
  case Nil
  then show ?case by (simp add: find_spec_def)
next
  case (Cons x xs)
  then show ?case
    by (auto simp add: find_spec_def split: if_splits)
qed
```

**Refinement Step 2: Tail-Recursive Implementation**
```isabelle
fun find_tail :: "'a list ⇒ ('a ⇒ bool) ⇒ 'a option" where
  "find_tail [] P = None" |
  "find_tail (x # xs) P = (if P x then Some x else find_tail xs P)"

lemma find_tail_correct:
  "find_tail xs P = find_impl xs P"
  by (induction xs) auto
```

## Best Practices

1. **Small Steps**: Make incremental refinements rather than large jumps
2. **Clear Abstractions**: Define explicit abstraction relations
3. **Modular Proofs**: Prove refinement for each operation separately
4. **Reuse Lemmas**: Build library of refinement lemmas
5. **Automation**: Use tactics and automation where possible
6. **Documentation**: Document refinement decisions and invariants

## Verification Checklist

Before finalizing refinement:

- [ ] Abstraction relation is well-defined
- [ ] All operations have refinement proofs
- [ ] Invariants are preserved
- [ ] Termination is proven (if applicable)
- [ ] Concrete implementation is executable
- [ ] Code can be extracted/generated
- [ ] Performance characteristics are acceptable

## Additional Resources

For detailed guidance on specific aspects:
- [Isabelle Refinement](references/isabelle_refinement.md) - Isabelle/HOL refinement framework
- [Coq Refinement](references/coq_refinement.md) - Coq refinement techniques
- [Refinement Patterns](references/refinement_patterns.md) - Common refinement patterns
