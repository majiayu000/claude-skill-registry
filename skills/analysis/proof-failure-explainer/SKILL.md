---
name: proof-failure-explainer
description: Analyze and explain why Isabelle or Coq proofs fail, identifying the root cause such as type mismatches, missing assumptions, incorrect goals, unification failures, or inapplicable tactics. Use when the user encounters proof failures, error messages in formal verification, stuck proof states, or asks why their Isabelle/Coq proof doesn't work.
---

# Proof Failure Explainer

## Overview

Diagnose and explain proof failures in Isabelle and Coq by analyzing proof states, error messages, and goal structures. This skill helps identify root causes and suggests fixes for common proof problems.

## Analysis Workflow

### Step 1: Gather Context

Collect information about the failure:

1. **Proof state:**
   - Current goal(s)
   - Available hypotheses/assumptions
   - Context (definitions, lemmas in scope)

2. **Error message:**
   - Exact error text
   - Which tactic failed
   - Line/position of failure

3. **Proof attempt:**
   - What tactics were tried
   - What was expected to happen
   - Where the proof got stuck

### Step 2: Identify Failure Category

Classify the type of failure:

**Type Errors:**
- Type mismatch in expressions
- Wrong function argument types
- Incompatible type unification

**Unification Failures:**
- Cannot unify terms
- Existential variables not instantiated
- Pattern matching failures

**Missing Assumptions:**
- Unprovable without additional hypotheses
- Missing preconditions
- Insufficient context

**Incorrect Goals:**
- Goal statement is false
- Goal too strong or too weak
- Wrong quantifier order

**Tactic Failures:**
- Tactic not applicable to goal
- Wrong tactic for goal structure
- Induction hypothesis too weak

**Scope Issues:**
- Variables not in scope
- Shadowed variables
- Context problems

### Step 3: Analyze Root Cause

Examine the specific failure:

**For Type Errors:**
```
Check each term's type:
- What type does the term have?
- What type is expected?
- Where does the mismatch occur?
```

**For Unification Failures:**
```
Compare terms that should unify:
- Are they syntactically equal?
- What substitution would make them equal?
- Is that substitution possible?
```

**For Missing Assumptions:**
```
Identify what's needed:
- What fact would make the goal provable?
- Is it missing from hypotheses?
- Should it be a precondition?
```

**For Incorrect Goals:**
```
Verify goal correctness:
- Is the statement actually true?
- Can you find a counterexample?
- Is it too strong/weak?
```

### Step 4: Explain the Failure

Provide clear explanation:

1. **State the problem:**
   - "The proof fails because..."
   - Point to specific issue

2. **Show the mismatch:**
   - Highlight conflicting terms/types
   - Show what was expected vs. actual

3. **Explain why it fails:**
   - Why the tactic doesn't work
   - Why terms don't unify
   - Why the goal is unprovable

### Step 5: Suggest Solutions

Offer concrete fixes:

1. **Immediate fixes:**
   - Correct the type annotation
   - Add missing assumption
   - Fix goal statement
   - Use different tactic

2. **Alternative approaches:**
   - Different proof strategy
   - Strengthen/weaken goal
   - Generalize before induction
   - Add helper lemmas

3. **Code examples:**
   - Show corrected version
   - Demonstrate working proof
   - Explain why it works

## Common Failure Patterns

For detailed patterns and examples, see [failure_patterns.md](references/failure_patterns.md).

### Quick Diagnosis Guide

| Symptom | Likely Cause | Quick Check |
|---------|--------------|-------------|
| "Type unification failed" | Type mismatch | Check types with `Check` (Coq) or `term` (Isabelle) |
| "Unable to unify X with Y" | Terms don't match | Compare X and Y - are they equal? |
| "Tactic failure" | Wrong tactic | Check goal structure - does tactic apply? |
| "Not found in environment" | Scope issue | Is variable quantified? |
| Proof gets stuck | Missing hypothesis | What fact would help? |
| Goal unprovable | Incorrect statement | Is the goal actually true? |

## Examples

### Example 1: Type Mismatch

**User's Failing Proof (Coq):**
```coq
Definition double (n : nat) : nat := n + n.

Lemma test : double true = 2.
```

**Error:**
```
The term "true" has type "bool" while it is expected to have type "nat".
```

**Explanation:**
The proof fails because of a type mismatch:
- `double` expects an argument of type `nat`
- You provided `true`, which has type `bool`
- Coq cannot apply a function expecting `nat` to a `bool` argument

**Solution:**
```coq
Lemma test : double 1 = 2.
Proof.
  unfold double. reflexivity.
Qed.
```

### Example 2: Unification Failure

**User's Failing Proof (Coq):**
```coq
Lemma comm_fail : forall x y z : nat, x + y = y + z.
Proof.
  intros. reflexivity.
Qed.
```

**Error:**
```
Unable to unify "x + y" with "y + z".
```

**Explanation:**
The proof fails because:
- `reflexivity` requires both sides to be syntactically equal
- `x + y` and `y + z` are not equal without knowing `x = z`
- You're trying to prove something that's not true in general

**Solution:**
Either fix the goal or add the necessary assumption:
```coq
(* Option 1: Fix the goal to something true *)
Lemma comm_correct : forall x y : nat, x + y = y + x.
Proof.
  intros. lia.
Qed.

(* Option 2: Add assumption *)
Lemma comm_with_assumption : forall x y z : nat, x = z -> x + y = y + z.
Proof.
  intros. rewrite H. reflexivity.
Qed.
```

### Example 3: Missing Assumption

**User's Failing Proof (Isabelle):**
```isabelle
lemma "x > 0 ⟹ x + y > y"
  by simp
```

**Error:**
```
Failed to apply initial proof method
```

**Explanation:**
The proof fails because:
- For integers, `x + y > y` requires `x > 0`
- The assumption is stated, but `simp` alone is insufficient
- Need arithmetic reasoning, not just simplification

**Solution:**
```isabelle
lemma "x > (0::int) ⟹ x + y > y"
  by arith
```

Or in Coq:
```coq
Lemma add_positive : forall x y : nat, x > 0 -> x + y > y.
Proof.
  intros. lia.
Qed.
```

### Example 4: Wrong Tactic

**User's Failing Proof (Coq):**
```coq
Lemma or_intro : forall P Q : Prop, P -> P \/ Q.
Proof.
  intros. split.
Qed.
```

**Error:**
```
Unable to unify "?P /\ ?Q" with "P \/ Q".
```

**Explanation:**
The proof fails because:
- `split` is for conjunction (`/\`), not disjunction (`\/`)
- The goal is `P \/ Q` (disjunction)
- You need `left` or `right` for disjunction

**Solution:**
```coq
Lemma or_intro : forall P Q : Prop, P -> P \/ Q.
Proof.
  intros. left. assumption.
Qed.
```

### Example 5: Incorrect Goal

**User's Failing Proof (Isabelle):**
```isabelle
lemma list_comm: "xs @ ys = ys @ xs"
```

**Error:**
```
Failed to apply initial proof method
```

**Explanation:**
The proof fails because:
- List append (`@`) is NOT commutative
- The goal is false in general
- Counterexample: `[1] @ [2] = [1,2]` but `[2] @ [1] = [2,1]`

**Solution:**
Fix the goal to something true:
```isabelle
(* Append is associative, not commutative *)
lemma list_assoc: "(xs @ ys) @ zs = xs @ (ys @ zs)"
  by simp
```

### Example 6: Wrong Induction Variable

**User's Failing Proof (Coq):**
```coq
Lemma app_length : forall (A : Type) (l1 l2 : list A),
  length (l1 ++ l2) = length l1 + length l2.
Proof.
  intros. induction l2.
  - reflexivity.
  - simpl. (* Gets stuck *)
```

**Explanation:**
The proof fails because:
- Inducting on `l2` (second list)
- But `++` (append) is defined recursively on the first argument
- Need to induct on `l1` instead

**Solution:**
```coq
Lemma app_length : forall (A : Type) (l1 l2 : list A),
  length (l1 ++ l2) = length l1 + length l2.
Proof.
  intros. induction l1.
  - reflexivity.
  - simpl. rewrite IHl1. reflexivity.
Qed.
```

## Diagnostic Questions

When analyzing a failure, ask:

1. **Type-related:**
   - What are the types of all terms?
   - Do the types match expectations?
   - Is there implicit type coercion?

2. **Unification-related:**
   - What terms need to be equal?
   - Are they syntactically equal?
   - What would make them equal?

3. **Assumption-related:**
   - What facts are available?
   - What facts are needed?
   - Are preconditions satisfied?

4. **Goal-related:**
   - Is the goal statement correct?
   - Is it actually true?
   - Is it too strong/weak?

5. **Tactic-related:**
   - What does this tactic do?
   - Does it apply to this goal?
   - What goal structure does it expect?

6. **Induction-related:**
   - Which variable to induct on?
   - Is the IH strong enough?
   - Need to generalize first?

## Best Practices

1. **Read error messages carefully:** They often pinpoint the exact issue
2. **Check types first:** Many failures are type-related
3. **Verify goal correctness:** Make sure the statement is actually true
4. **Test with simple cases:** Try the proof on a simple example
5. **Use automation cautiously:** Understand why tactics fail
6. **Consult documentation:** Check tactic requirements and behavior
7. **Search for similar proofs:** Look for patterns in standard library
8. **Break down complex goals:** Prove helper lemmas first

## Debugging Tools

### Isabelle

- `term "expr"` - Check type of expression
- `thm theorem_name` - Display theorem
- `find_theorems pattern` - Search for relevant theorems
- `sledgehammer` - Automated proof search
- `try` - Try multiple tactics

### Coq

- `Check term` - Display type
- `Print name` - Show definition
- `Search pattern` - Find lemmas
- `Show Proof` - Display proof term
- `Set Printing All` - Show implicit arguments
- `Locate symbol` - Find definition of notation

## Resources

- **Failure patterns:** See [failure_patterns.md](references/failure_patterns.md) for comprehensive catalog
- **Isabelle documentation:** https://isabelle.in.tum.de/documentation.html
- **Coq documentation:** https://coq.inria.fr/documentation
- **Isabelle tutorial:** https://isabelle.in.tum.de/dist/Isabelle/doc/tutorial.pdf
- **Software Foundations:** https://softwarefoundations.cis.upenn.edu/
