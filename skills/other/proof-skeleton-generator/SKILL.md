---
name: proof-skeleton-generator
description: "Generate structured proof skeletons with tactics, strategies, and intermediate lemmas for theorems in Isabelle/HOL or Coq. Use when users need to: (1) Create proof outlines for theorem statements, (2) Generate proof structure with tactic placeholders, (3) Identify key lemmas needed for a proof, (4) Plan proof strategies (induction, case analysis, forward/backward reasoning), (5) Scaffold proofs with intermediate steps and subgoals, or (6) Convert theorem statements into detailed proof templates. Supports both Isabelle/HOL and Coq equally."
---

# Proof Skeleton Generator

Generate structured proof skeletons with tactics, proof strategies, and key lemmas for theorems in Isabelle/HOL or Coq.

## Workflow

### 1. Analyze the Theorem Statement

Examine the theorem to understand:
- **Quantifiers**: Universal (∀/forall) or existential (∃/exists)
- **Logical structure**: Implications, conjunctions, disjunctions
- **Data types involved**: Lists, natural numbers, custom types
- **Complexity**: Simple equality vs. complex property

### 2. Choose Target System

Ask the user which proof assistant to target:
- **Isabelle/HOL**: Uses Isar structured proofs, automatic tactics
- **Coq**: Uses Ltac tactics, more explicit proof terms
- **Both**: Generate skeletons for both systems

If not specified, default to generating both versions.

### 3. Determine Proof Strategy

Based on the theorem structure, identify the appropriate proof technique:

**Induction** - When theorem involves recursive types:
- List induction for list properties
- Natural number induction for arithmetic
- Structural induction for custom datatypes
- Strong induction when needed

**Case Analysis** - When theorem involves:
- Boolean conditions
- Option types (None/Some)
- Sum types or custom constructors
- Conditional expressions

**Direct Proof** - When theorem is:
- Simple equality that simplifies
- Follows directly from definitions
- Provable by automatic tactics

**Forward Reasoning** - Build up facts:
- Establish intermediate lemmas
- Chain implications
- Construct witnesses for existentials

**Backward Reasoning** - Work from goal:
- Apply rules to reduce goal
- Split conjunctions
- Introduce implications

### 4. Identify Required Lemmas

Determine helper lemmas that may be needed:
- **Standard library lemmas**: Check if already available
- **Custom lemmas**: Properties that need separate proof
- **Induction hypotheses**: How they'll be used
- **Intermediate facts**: Steps in the main proof

### 5. Generate Proof Skeleton

Use the reference files for tactics and patterns:
- **Isabelle tactics**: See [isabelle_tactics.md](references/isabelle_tactics.md)
- **Coq tactics**: See [coq_tactics.md](references/coq_tactics.md)
- **Complete examples**: See [examples.md](references/examples.md)

Create a skeleton that includes:
1. **Proof structure** with appropriate method (induction, cases, etc.)
2. **Case labels** for each subgoal
3. **Strategy comments** explaining the approach
4. **Tactic placeholders** (sorry/admit) for incomplete steps
5. **Intermediate assertions** (have/assert) for key facts
6. **Helper lemmas** with their own skeletons

### 6. Structure the Output

Organize the proof skeleton clearly:

**For Isabelle/HOL:**
```isabelle
(* Helper lemmas if needed *)
lemma helper_name:
  "statement"
  sorry

(* Main theorem *)
theorem theorem_name:
  assumes "assumptions"
  shows "conclusion"
proof (method)
  case case_name
  (* Goal: ... *)
  (* Strategy: ... *)
  (* Key steps:
     1. ...
     2. ...
  *)
  show ?case sorry
next
  (* Additional cases *)
qed
```

**For Coq:**
```coq
(* Helper lemmas if needed *)
Lemma helper_name :
  statement.
Proof.
  (* proof *)
  admit.
Admitted.

(* Main theorem *)
Theorem theorem_name :
  statement.
Proof.
  intros.
  induction ... as [| ...].
  - (* Case: ... *)
    (* Strategy: ... *)
    admit.
  - (* Case: ... *)
    (* IH: ... *)
    (* Strategy: ... *)
    admit.
Admitted.
```

## Key Principles

### Clarity
- Add comments explaining the proof strategy
- Label each case clearly
- Document what the induction hypothesis provides
- Explain non-obvious steps

### Completeness
- Include all necessary cases
- Identify all required helper lemmas
- Show the structure of nested proofs
- Indicate where automation might work

### Practicality
- Use `sorry` (Isabelle) or `admit` (Coq) for incomplete steps
- Suggest automatic tactics where applicable
- Note when `sledgehammer` (Isabelle) might help
- Indicate which steps are trivial vs. challenging

### Correctness
- Ensure case analysis is exhaustive
- Verify induction is on the right variable
- Check that the proof structure matches the goal
- Validate that lemmas are actually needed

## Proof Strategy Selection Guide

### When to Use Induction

**List properties**: `forall xs, P xs`
- Induction on `xs`
- Base case: empty list
- Inductive case: `x :: xs` with IH `P xs`

**Natural number properties**: `forall n, P n`
- Induction on `n`
- Base case: `0` or `Suc 0`
- Inductive case: `Suc n` with IH `P n`

**Recursive function properties**: When function is defined recursively
- Induct on the recursive argument
- IH mirrors the recursive call

### When to Use Case Analysis

**Conditional expressions**: `if b then ... else ...`
- Split on `b` (true/false cases)

**Option types**: `match opt with None => ... | Some x => ...`
- Case on `None` and `Some x`

**Sum types**: `match x with Left a => ... | Right b => ...`
- Case on each constructor

### When to Use Direct Proof

**Definitional equalities**: `f x = g x` where definitions unfold
- Unfold definitions and simplify

**Trivial goals**: Provable by `auto`, `simp`, `reflexivity`
- Try automatic tactics first

### When to Use Lemmas

**Repeated subgoals**: Same property needed multiple times
- Extract as separate lemma

**Complex intermediate facts**: Multi-step derivations
- Prove as helper lemma

**Standard properties**: Check standard library first
- Import and use existing lemmas

## Common Patterns

### Induction with Simplification
```
proof (induction xs)
  case Nil
  show ?case by simp
next
  case (Cons x xs)
  show ?case using Cons.IH by simp
qed
```

### Case Analysis with Subproofs
```
proof (cases x)
  case Constructor1
  show ?thesis
  proof -
    (* detailed steps *)
  qed
next
  case Constructor2
  (* ... *)
qed
```

### Forward Reasoning Chain
```
proof -
  have step1: "fact1" by simp
  have step2: "fact2" using step1 by simp
  show ?thesis using step2 by simp
qed
```

### Backward Reasoning with Rules
```
proof (rule some_rule)
  show "premise1" sorry
  show "premise2" sorry
qed
```

## Tips

- **Start with structure**: Get the proof skeleton right before filling details
- **Use comments liberally**: Explain strategy and key steps
- **Identify IH usage**: Note where induction hypothesis is applied
- **Check standard library**: Many lemmas already exist
- **Suggest automation**: Note where `auto`, `simp`, `blast` might work
- **Be realistic**: Mark challenging steps as `sorry`/`admit`
- **Both systems**: Ensure semantic equivalence when generating both
- **Nested induction**: Handle carefully with clear variable names
- **Termination**: Note when termination proofs are needed
