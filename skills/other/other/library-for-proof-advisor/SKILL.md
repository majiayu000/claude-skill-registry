---
name: library-advisor
description: "Recommend relevant Isabelle/HOL or Coq standard library theories, lemmas, and tactics based on proof goals. Use when: (1) Users need library lemmas for their proof, (2) Proof goals match standard library patterns, (3) Users ask what libraries to import, (4) Specific lemmas are needed for list/set/arithmetic operations, (5) Users are stuck and need to know what library support exists, or (6) Guidance on find_theorems/Search commands is needed. Supports both Isabelle/HOL and Coq standard libraries."
---

# Library Usage Advisor

Recommend relevant libraries, lemmas, and theories from Isabelle/HOL or Coq standard libraries based on proof goals.

## Workflow

### 1. Analyze the Proof Goal

Examine the goal to identify:
- **Domain**: Lists, sets, arithmetic, logic, etc.
- **Operations**: Specific functions or operators involved
- **Pattern**: Commutativity, associativity, distributivity, etc.
- **Complexity**: Simple property vs. complex relationship

### 2. Determine Target System

Identify which proof assistant:
- **Isabelle/HOL**: Use Main library and extensions
- **Coq**: Use standard library (List, Arith, etc.)
- **Both**: Provide recommendations for both systems

### 3. Identify Relevant Libraries

Based on the domain, recommend appropriate libraries:

**For list operations**:
- Isabelle: Main (List theory included)
- Coq: `Require Import List. Import ListNotations.`

**For arithmetic**:
- Isabelle: Main (Nat theory included)
- Coq: `Require Import Arith Lia.`

**For sets**:
- Isabelle: Main (Set theory included)
- Coq: `Require Import MSets.`

**For logic**:
- Isabelle: HOL (automatically available)
- Coq: `Require Import Logic.`

### 4. Search for Specific Lemmas

Look for lemmas that directly match the goal:

**Exact matches**: Lemmas that prove the goal directly
**Component lemmas**: Lemmas for parts of the goal
**Related lemmas**: Similar properties that might help

Use the library reference files:
- **Isabelle library**: See [isabelle_library.md](references/isabelle_library.md)
- **Coq library**: See [coq_library.md](references/coq_library.md)

### 5. Recommend Usage

Provide concrete recommendations:

**Direct application**:
```isabelle
lemma "goal"
  by (simp add: relevant_lemma)
```

**With additional steps**:
```coq
Lemma goal : statement.
Proof.
  apply relevant_lemma.
  (* additional steps *)
Qed.
```

**Manual proof with lemmas**:
Show how to use lemmas in a structured proof

### 6. Suggest Search Commands

Teach users how to find lemmas themselves:

**Isabelle**:
```isabelle
find_theorems "pattern"
find_theorems name: "keyword"
sledgehammer
```

**Coq**:
```coq
Search pattern.
Search "keyword".
Locate "notation".
```

## Domain-Specific Recommendations

### Lists

**Common goals**:
- Length properties: `length_append`, `length_rev`, `length_map`
- Reverse properties: `rev_rev_ident`, `rev_append`
- Append properties: `append_assoc`, `append_Nil`
- Map properties: `map_append`, `map_map`
- Membership: `in_set_member`, `set_append`

**Libraries**:
- Isabelle: Main (automatic)
- Coq: `List` library

### Arithmetic

**Common goals**:
- Commutativity: `add_commute`, `mult_commute`
- Associativity: `add_assoc`, `mult_assoc`
- Distributivity: `add_mult_distrib`
- Inequalities: Use `arith`/`lia` tactics

**Libraries**:
- Isabelle: Main (Nat theory)
- Coq: `Arith`, `Lia`, `Nia`

### Sets

**Common goals**:
- Union/intersection: `Un_commute`, `Int_commute`
- Subset: `subset_refl`, `subset_trans`
- Membership: `Un_iff`, `Int_iff`

**Libraries**:
- Isabelle: Main (Set theory)
- Coq: `MSets` or custom definitions

### Logic

**Common goals**:
- Conjunction: `conjI`, `conjE`
- Disjunction: `disjI1`, `disjI2`
- Implication: `impI`, `mp`
- Quantifiers: `allI`, `exI`

**Libraries**:
- Isabelle: HOL (automatic)
- Coq: `Logic` (mostly automatic)

## Recommendation Patterns

### Pattern 1: Exact Lemma Match

When goal exactly matches a known lemma:

**Isabelle**:
```isabelle
lemma "rev (rev xs) = xs"
  by (simp add: rev_rev_ident)
```

**Coq**:
```coq
Lemma example : forall l, rev (rev l) = l.
Proof.
  apply rev_involutive.
Qed.
```

### Pattern 2: Combination of Lemmas

When goal needs multiple lemmas:

**Isabelle**:
```isabelle
lemma "length (rev (xs @ ys)) = length xs + length ys"
  by (simp add: length_rev length_append)
```

**Coq**:
```coq
Lemma example : forall l1 l2,
  length (rev (l1 ++ l2)) = length l1 + length l2.
Proof.
  intros.
  rewrite rev_length.
  rewrite app_length.
  reflexivity.
Qed.
```

### Pattern 3: Automation

When goal is provable by automation:

**Isabelle**:
```isabelle
lemma "n + m = m + n"
  by simp
(* Or: by auto, by arith *)
```

**Coq**:
```coq
Lemma example : forall n m, n + m = m + n.
Proof.
  intros. lia.
Qed.
```

### Pattern 4: Induction with Lemmas

When manual proof needed but lemmas help:

**Isabelle**:
```isabelle
lemma "property xs"
proof (induction xs)
  case Nil
  show ?case by simp
next
  case (Cons x xs)
  show ?case using Cons.IH by (simp add: helper_lemma)
qed
```

**Coq**:
```coq
Lemma example : forall l, property l.
Proof.
  induction l as [| x xs IHxs].
  - simpl. reflexivity.
  - simpl. rewrite IHxs. apply helper_lemma.
Qed.
```

## Search Strategies

### Strategy 1: Pattern-Based Search

**Isabelle**:
```isabelle
find_theorems "rev (rev _) = _"
find_theorems "length (_ @ _)"
find_theorems "_ + _ = _ + _"
```

**Coq**:
```coq
Search rev.
Search (_ ++ _).
Search (?x + ?y = ?y + ?x).
```

### Strategy 2: Name-Based Search

**Isabelle**:
```isabelle
find_theorems name: "append"
find_theorems name: "comm"
```

**Coq**:
```coq
Search "append".
Search "comm" (_ + _).
```

### Strategy 3: Type-Based Search

**Coq**:
```coq
Search (list _ -> nat).
Search (_ -> _ -> _ + _).
```

### Strategy 4: Sledgehammer/Auto

**Isabelle**:
```isabelle
lemma "goal"
  sledgehammer
  (* Suggests relevant lemmas and tactics *)
```

**Coq**:
```coq
Lemma goal : statement.
Proof.
  auto.  (* Try automatic tactics *)
Qed.
```

## Common Recommendations by Goal Type

### "rev (rev xs) = xs"
- Isabelle: `rev_rev_ident` or `by simp`
- Coq: `rev_involutive`

### "length (xs @ ys) = length xs + length ys"
- Isabelle: `length_append` or `by simp`
- Coq: `app_length`

### "n + m = m + n"
- Isabelle: `add_commute` or `by simp`
- Coq: `plus_comm` or `lia`

### "x ∈ set (xs @ ys) ⟷ x ∈ set xs ∨ x ∈ set ys"
- Isabelle: `set_append`
- Coq: `in_app_iff`

### "map f (xs @ ys) = map f xs @ map f ys"
- Isabelle: `map_append`
- Coq: `map_app`

## Examples

For complete examples with specific proof goals and library recommendations, see [examples.md](references/examples.md).

## Tips

- **Search first**: Use find_theorems/Search before proving manually
- **Check automation**: Try simp/auto/lia before complex proofs
- **Use sledgehammer**: In Isabelle, sledgehammer finds relevant lemmas
- **Import early**: Import all needed libraries at the start
- **Learn patterns**: Common properties (commutativity, etc.) have standard names
- **Read library docs**: Browse standard library documentation
- **Build intuition**: Learn which libraries contain which lemmas
- **Combine lemmas**: Complex goals often need multiple lemmas
- **Simplify first**: Use simp/simpl to reduce goals before searching
