---
name: lemma-discovery-assistant
description: Analyze failed or stuck proofs and propose auxiliary lemmas to help complete the proof in Isabelle/HOL or Coq. Use when encountering proof failures, stuck proof states, unprovable subgoals, or when needing to strengthen induction hypotheses. Identifies missing lemmas, suggests proof strategies, and generates helper lemmas with appropriate statements and proof sketches. Supports inductive proofs, case analysis, rewriting, and complex proof obligations.
---

# Lemma Discovery Assistant

Analyze stuck or failed proofs and propose auxiliary lemmas that can help complete the proof.

## Overview

When proofs fail or get stuck, the issue is often a missing auxiliary lemma. This skill helps identify what lemmas are needed by:

1. Analyzing the current proof state and goal
2. Identifying gaps in reasoning
3. Proposing auxiliary lemmas with precise statements
4. Suggesting proof strategies for the lemmas
5. Explaining how the lemmas help the main proof

## When Proofs Get Stuck

### Common Symptoms

**Unprovable subgoal:**
- Tactics fail to make progress
- Goal seems "obviously true" but won't prove
- Missing connection between hypotheses and goal

**Weak induction hypothesis:**
- Induction step fails
- Need stronger property to prove
- Generalization required

**Missing intermediate steps:**
- Large gap between current state and goal
- Need stepping stones
- Complex reasoning required

**Insufficient rewrite rules:**
- Simplification doesn't go far enough
- Need additional equations
- Definitions need unfolding lemmas

## Lemma Discovery Process

### Step 1: Analyze Proof State

Examine the current proof context:

**What to look for:**
- Current goal statement
- Available hypotheses/assumptions
- Failed tactic and error message
- Proof structure (induction, case analysis, etc.)
- Type information and constraints

**Questions to ask:**
- What is the proof trying to show?
- What information is available?
- What is missing?
- Why did the tactic fail?

### Step 2: Identify the Gap

Determine what's preventing progress:

**Gap types:**
- **Property gap**: Need to establish intermediate property
- **Generalization gap**: Current statement too specific
- **Rewrite gap**: Need equation to simplify
- **Structural gap**: Need lemma about data structure
- **Induction gap**: Induction hypothesis too weak

### Step 3: Propose Lemma Statement

Formulate precise lemma statement:

**Lemma characteristics:**
- **Precise**: Exact types and conditions
- **General**: Not overly specific to one case
- **Provable**: Can be proven independently
- **Useful**: Actually helps the main proof

**Example patterns:**
```
(* Isabelle *)
lemma helper_name: "⟦ assumptions ⟧ ⟹ conclusion"

(* Coq *)
Lemma helper_name : assumptions → conclusion.
```

### Step 4: Suggest Proof Strategy

Provide guidance on proving the lemma:

**Strategy types:**
- Induction (structural, well-founded, strong)
- Case analysis
- Rewriting and simplification
- Unfolding definitions
- Using existing lemmas

### Step 5: Explain Usage

Show how the lemma helps the main proof:

- Where to apply it
- What tactic to use
- How it closes the gap

## Lemma Patterns by Proof Type

### Inductive Proofs

**Problem:** Induction hypothesis too weak.

**Solution:** Strengthen the induction hypothesis.

**Example (Isabelle):**

**Stuck proof:**
```isabelle
lemma "length (reverse xs) = length xs"
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  (* Stuck: reverse (x # xs) = reverse xs @ [x]
     but we don't have a lemma about length of append *)
  then show ?case sorry
qed
```

**Proposed lemma:**
```isabelle
lemma length_append: "length (xs @ ys) = length xs + length ys"
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  then show ?case by simp
qed
```

**Usage:** Apply `length_append` in the induction step.

### Generalization Lemmas

**Problem:** Statement too specific to prove by induction.

**Solution:** Generalize with accumulator or additional parameter.

**Example (Coq):**

**Stuck proof:**
```coq
Fixpoint reverse {A} (l : list A) : list A :=
  match l with
  | [] => []
  | x :: xs => reverse xs ++ [x]
  end.

Lemma reverse_involutive : forall A (l : list A),
  reverse (reverse l) = l.
Proof.
  induction l.
  - reflexivity.
  - simpl. (* Stuck: need reverse (reverse l ++ [a]) = a :: l *)
Abort.
```

**Proposed lemma:**
```coq
Lemma reverse_append : forall A (l1 l2 : list A),
  reverse (l1 ++ l2) = reverse l2 ++ reverse l1.
Proof.
  induction l1; intros; simpl.
  - rewrite app_nil_r. reflexivity.
  - rewrite IHl1. rewrite app_assoc. reflexivity.
Qed.
```

**Usage:** Use `reverse_append` to handle the append in the goal.

### Rewrite Lemmas

**Problem:** Simplification doesn't reach desired form.

**Solution:** Add rewrite rules for specific patterns.

**Example (Isabelle):**

**Stuck proof:**
```isabelle
lemma "map f (map g xs) = map (f ∘ g) xs"
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  (* Need: (f ∘ g) x = f (g x) *)
  then show ?case sorry
qed
```

**Proposed lemma:**
```isabelle
lemma comp_apply: "(f ∘ g) x = f (g x)"
  by (simp add: comp_def)
```

**Usage:** Add to simplification set or apply explicitly.

### Structural Lemmas

**Problem:** Need properties about data structure operations.

**Solution:** Prove fundamental properties of the structure.

**Example (Coq):**

**Stuck proof:**
```coq
Fixpoint insert (x : nat) (t : tree) : tree := (* ... *)

Lemma insert_member : forall x t,
  member x (insert x t) = true.
Proof.
  induction t.
  - (* Stuck: need properties of member and insert *)
Abort.
```

**Proposed lemmas:**
```coq
Lemma member_insert_eq : forall x y t,
  x = y → member x (insert y t) = true.

Lemma member_insert_neq : forall x y t,
  x ≠ y → member x (insert y t) = member x t.

Lemma member_insert : forall x y t,
  member x (insert y t) = (x =? y) || member x t.
```

**Usage:** Case split on `x = y` and apply appropriate lemma.

## Framework-Specific Guidance

### Isabelle/HOL Lemma Discovery

For Isabelle-specific lemma patterns, tactics, and the sledgehammer tool, see [references/isabelle_lemmas.md](references/isabelle_lemmas.md).

Key features:
- Sledgehammer for automatic lemma discovery
- `try` and `try0` for tactic exploration
- Simplification set management
- Induction and case analysis patterns

### Coq Lemma Discovery

For Coq-specific lemma patterns, tactics, and proof search, see [references/coq_lemmas.md](references/coq_lemmas.md).

Key features:
- `Search` and `SearchAbout` for finding lemmas
- `auto`, `eauto` for proof search
- Proof automation with `Ltac`
- Inversion and case analysis

## Common Lemma Categories

For detailed lemma patterns organized by category, see [references/proof_patterns.md](references/proof_patterns.md).

Categories include:
- List lemmas (append, reverse, map, filter)
- Arithmetic lemmas (associativity, commutativity, distributivity)
- Set/Map lemmas (membership, union, intersection)
- Induction strengthening patterns
- Generalization patterns

## Example: Complete Lemma Discovery

**Scenario:** Proving correctness of insertion sort.

**Main theorem (Isabelle):**
```isabelle
lemma insertion_sort_correct:
  "sorted (insertion_sort xs) ∧ mset (insertion_sort xs) = mset xs"
```

**Stuck proof:**
```isabelle
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  (* Need to show:
     sorted (insert x (insertion_sort xs))
     mset (insert x (insertion_sort xs)) = mset (x # xs) *)
  then show ?case sorry
qed
```

**Analysis:**
1. Need properties of `insert` function
2. Need to show `insert` preserves sorting
3. Need to show `insert` preserves multiset

**Proposed lemmas:**

```isabelle
(* Lemma 1: insert preserves sorting *)
lemma insert_sorted:
  "sorted xs ⟹ sorted (insert x xs)"
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons y ys)
  then show ?case
    by (auto simp: sorted_Cons)
qed

(* Lemma 2: insert preserves multiset *)
lemma mset_insert:
  "mset (insert x xs) = {#x#} + mset xs"
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons y ys)
  then show ?case by (auto simp: ac_simps)
qed

(* Lemma 3: sorted definition for cons *)
lemma sorted_Cons:
  "sorted (x # xs) = (sorted xs ∧ (∀y ∈ set xs. x ≤ y))"
  by (auto simp: sorted_append)
```

**Revised main proof:**
```isabelle
lemma insertion_sort_correct:
  "sorted (insertion_sort xs) ∧ mset (insertion_sort xs) = mset xs"
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  have "sorted (insertion_sort xs)" using Cons by simp
  then have "sorted (insert x (insertion_sort xs))"
    by (rule insert_sorted)
  moreover have "mset (insert x (insertion_sort xs)) = {#x#} + mset (insertion_sort xs)"
    by (rule mset_insert)
  moreover have "mset (insertion_sort xs) = mset xs"
    using Cons by simp
  ultimately show ?case by (auto simp: ac_simps)
qed
```

## Lemma Discovery Strategies

### Bottom-Up Discovery

1. Start with failed proof
2. Identify immediate obstacle
3. Propose lemma for that obstacle
4. Recursively discover lemmas for the proposed lemma
5. Build up from base cases

### Top-Down Discovery

1. Analyze overall proof structure
2. Identify major proof steps
3. Propose high-level lemmas
4. Refine each lemma
5. Fill in details

### Pattern Matching

1. Recognize common proof patterns
2. Apply standard lemmas for that pattern
3. Adapt to specific context
4. Verify applicability

## Best Practices

1. **Start Simple**: Propose simplest lemma that could help
2. **Be Specific**: Precise types and conditions
3. **Check Provability**: Ensure lemma is actually provable
4. **Verify Usefulness**: Confirm lemma helps main proof
5. **Avoid Circularity**: Lemma shouldn't depend on main theorem
6. **Generalize Appropriately**: Not too specific, not too general
7. **Name Clearly**: Descriptive names aid understanding

## Troubleshooting

### Lemma Still Doesn't Help

**Possible issues:**
- Lemma statement incorrect
- Need additional lemmas
- Wrong proof strategy
- Main theorem statement flawed

**Solutions:**
- Revisit proof state analysis
- Try different generalization
- Consider alternative approach
- Check theorem statement

### Lemma Itself Won't Prove

**Possible issues:**
- Lemma too strong
- Missing preconditions
- Need intermediate lemmas
- Requires different proof technique

**Solutions:**
- Weaken conclusion
- Add necessary assumptions
- Discover sub-lemmas
- Try different proof method

## Additional Resources

For detailed guidance on specific aspects:
- [Isabelle Lemmas](references/isabelle_lemmas.md) - Isabelle/HOL lemma patterns and tactics
- [Coq Lemmas](references/coq_lemmas.md) - Coq lemma patterns and proof search
- [Proof Patterns](references/proof_patterns.md) - Common proof patterns and lemma categories
