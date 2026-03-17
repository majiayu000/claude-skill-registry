---
name: prove-plus-comm
description: Guide for completing Coq proofs involving arithmetic properties like addition commutativity. This skill should be used when working on Coq proof files that require proving properties about natural number arithmetic using induction, particularly when lemmas like plus_n_O and plus_n_Sm are involved.
---

# Coq Arithmetic Proof Completion

This skill provides guidance for completing Coq proofs involving arithmetic properties on natural numbers, particularly addition commutativity and related lemmas.

## When to Use

- Completing incomplete Coq proofs about natural number arithmetic
- Proving commutativity, associativity, or other properties of addition
- Working with induction on natural numbers in Coq
- Debugging proofs that use standard library arithmetic lemmas

## Approach

### 1. Understand the Proof Structure

Before modifying any proof:

1. Read the entire proof file to understand what is being proven
2. Identify the theorem statement and its type signature
3. Note any auxiliary lemmas that are defined or imported
4. Locate the incomplete portions (often marked with `Admitted` or `(* TODO *)`)

### 2. Analyze the Proof State

For inductive proofs on natural numbers:

- **Base case (n = 0)**: After `simpl`, identify what remains to be proven
- **Inductive case (n = S n')**: Note the inductive hypothesis name (typically `IHn'`) and what goal remains after simplification

To understand goal states:

- Use `Show.` or inspect after `simpl.` to see current goals
- Recognize that `0 + m` simplifies to `m` by Coq's definition of addition
- Recognize that `S n + m` simplifies to `S (n + m)` by definition

### 3. Apply Standard Lemmas

Key lemmas for addition commutativity proofs:

| Lemma | Type | Use Case |
|-------|------|----------|
| `plus_n_O` | `forall n, n = n + 0` | Rewrite `n + 0` to `n` (use `rewrite <-`) |
| `plus_n_Sm` | `forall n m, S (n + m) = n + S m` | Rewrite `n + S m` to `S (n + m)` or vice versa |

### 4. Rewrite Direction Convention

In Coq, `rewrite` uses the lemma left-to-right by default:

- `rewrite plus_n_O` replaces `n` with `n + 0` (left-to-right)
- `rewrite <- plus_n_O` replaces `n + 0` with `n` (right-to-left)

Choose direction based on current goal:

- If goal contains `m + 0` and needs `m`, use `rewrite <- plus_n_O`
- If goal contains `m + S n` and needs `S (m + n)`, use `rewrite <- plus_n_Sm`

### 5. Standard Proof Pattern for Addition Commutativity

For proving `forall n m, n + m = m + n`:

```coq
Theorem plus_comm : forall n m : nat, n + m = m + n.
Proof.
  intros n m.
  induction n as [| n' IHn'].
  - (* Base case: 0 + m = m + 0 *)
    simpl.                    (* Simplifies to: m = m + 0 *)
    rewrite <- plus_n_O.      (* Rewrites m + 0 to m *)
    reflexivity.
  - (* Inductive case: S n' + m = m + S n' *)
    simpl.                    (* Simplifies to: S (n' + m) = m + S n' *)
    rewrite IHn'.             (* Uses IH: S (m + n') = m + S n' *)
    rewrite <- plus_n_Sm.     (* Rewrites to: m + S n' = m + S n' *)
    reflexivity.
Qed.
```

## Verification Strategy

1. **Compile the proof**: Run `coqc <filename>.v` to verify the proof compiles
2. **Check output files**: Successful compilation produces a `.vo` file
3. **Inspect error messages**: If compilation fails, Coq error messages indicate which goal cannot be proven

## Common Pitfalls

### Wrong Rewrite Direction

- **Symptom**: Goal doesn't change or proof gets stuck
- **Solution**: Try `rewrite <-` instead of `rewrite` or vice versa

### Missing Lemma Import

- **Symptom**: "Unknown reference" error for standard lemmas
- **Solution**: Ensure `Require Import Arith.` or appropriate module is loaded

### Incorrect Induction Variable

- **Symptom**: Inductive hypothesis doesn't match goal structure
- **Solution**: Check which variable induction is performed on; for commutativity, induction on first argument is typical

### Forgetting to Apply Inductive Hypothesis

- **Symptom**: Goal contains subexpression matching IH but proof is stuck
- **Solution**: Use `rewrite IHn'` to apply the inductive hypothesis before other lemmas

### Definition vs Lemma Confusion

- `0 + m = m` holds by definition (reflexivity after simpl)
- `m + 0 = m` requires `plus_n_O` lemma (not definitional)
- `S n + m = S (n + m)` holds by definition
- `m + S n = S (m + n)` requires `plus_n_Sm` lemma

## Debugging Tips

1. **Isolate the problematic step**: Comment out tactics after the failing point
2. **Check goal state**: Insert `Show.` to see current proof obligations
3. **Verify lemma types**: Use `Check plus_n_O.` to see lemma signatures
4. **Test lemmas in isolation**: Try `apply` or `rewrite` individually to understand behavior
