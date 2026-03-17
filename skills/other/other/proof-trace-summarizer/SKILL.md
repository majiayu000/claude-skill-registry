---
name: proof-trace-summarizer
description: "Summarize long Isabelle or Coq proof scripts into high-level logical steps and reasoning flow. Use when users need to: (1) Understand the structure of a complex proof, (2) Document proof strategies for others, (3) Extract the key reasoning steps from verbose proof scripts, (4) Create readable proof outlines from detailed tactical proofs. Produces hierarchical outlines with moderate detail showing proof structure, main cases, key lemmas, and reasoning flow for both Isabelle/Isar and Coq proofs."
---

# Proof Trace Summarizer

Summarize long proof scripts into high-level logical steps and reasoning flow.

## Overview

This skill transforms verbose Isabelle or Coq proof scripts into clear, hierarchical summaries that capture the essential reasoning structure. It identifies proof patterns (induction, case analysis, equational reasoning), extracts key steps, and presents them in a readable outline format.

## How to Use

Provide a proof script with:
1. **System**: Isabelle or Coq
2. **Proof script**: The complete proof to summarize
3. **Context** (optional): Theorem statement, definitions, or background

The skill will produce a hierarchical outline showing:
- Main proof strategy
- Case structure (if applicable)
- Key reasoning steps
- Important lemmas or facts used

## Summarization Workflow

### Step 1: Identify Proof Structure

Recognize the high-level proof pattern:

**Induction proof**: Look for `proof (induction ...)` (Isabelle) or `induction ... as [|...]` (Coq)

**Case analysis**: Look for `proof (cases ...)` (Isabelle) or `destruct ... as [...]` (Coq)

**Direct proof**: Sequential reasoning without major branching

**Equational reasoning**: Chain of rewrites or calculations

**Hybrid**: Combination of patterns

### Step 2: Extract Major Components

Identify the key structural elements:

- **Base cases**: Initial cases in induction or case analysis
- **Inductive cases**: Recursive cases with induction hypotheses
- **Subgoals**: Intermediate facts or lemmas
- **Key tactics**: Non-trivial reasoning steps
- **Automation**: Where automatic methods are used

### Step 3: Group Related Steps

Combine sequences of tactics into logical units:

- Multiple simplification steps → "Simplification proves..."
- Rewrite sequences → "Rewriting chain: ..."
- Automation → "Automatic proof handles..."

### Step 4: Create Hierarchical Outline

Structure the summary as a tree:

```
Main theorem: <statement>
├─ Proof strategy: <induction/cases/direct>
├─ Case 1: <description>
│  ├─ Subgoal 1.1: <description>
│  │  └─ <how proven>
│  └─ Subgoal 1.2: <description>
│     └─ <how proven>
└─ Case 2: <description>
   └─ <how proven>
```

### Step 5: Add Moderate Detail

For each step, include:
- What is being proven
- How it's proven (key tactic or method)
- Why it works (if non-obvious)

Omit:
- Routine simplification details
- Obvious arithmetic steps
- Repetitive patterns

## Example: Isabelle Induction Proof

**Input proof script**:
```isabelle
lemma rev_rev: "rev (rev xs) = xs"
proof (induction xs)
  case Nil
  show ?case by simp
next
  case (Cons x xs)
  have "rev (rev (x # xs)) = rev (rev xs @ [x])" by simp
  also have "... = rev [x] @ rev (rev xs)" by simp
  also have "... = [x] @ xs" using Cons.IH by simp
  also have "... = x # xs" by simp
  finally show ?case .
qed
```

**Output summary**:
```
Theorem: rev (rev xs) = xs
Proof by induction on xs

├─ Base case: xs = []
│  └─ Simplification: rev (rev []) = rev [] = []
│
└─ Inductive case: xs = x # xs'
   ├─ IH: rev (rev xs') = xs'
   └─ Equational reasoning:
      ├─ rev (rev (x # xs')) = rev (rev xs' @ [x])  (definition of rev)
      ├─ = rev [x] @ rev (rev xs')                   (rev distributes)
      ├─ = [x] @ xs'                                  (apply IH)
      └─ = x # xs'                                    (list notation)
```

## Example: Coq Case Analysis

**Input proof script**:
```coq
Theorem option_map_Some : forall (A B : Type) (f : A -> B) (x : option A) (y : B),
  option_map f x = Some y -> exists z, x = Some z /\ f z = y.
Proof.
  intros A B f x y H.
  destruct x as [z|].
  - simpl in H. injection H as H. exists z. split.
    + reflexivity.
    + exact H.
  - simpl in H. discriminate H.
Qed.
```

**Output summary**:
```
Theorem: option_map f x = Some y → ∃z. x = Some z ∧ f z = y
Proof by case analysis on x

├─ Case: x = Some z
│  ├─ Simplify: option_map f (Some z) = Some (f z)
│  ├─ Extract: f z = y from Some (f z) = Some y
│  └─ Witness: z satisfies x = Some z and f z = y
│
└─ Case: x = None
   └─ Contradiction: option_map f None = None ≠ Some y
```

## Example: Complex Nested Proof

**Input proof script**:
```isabelle
lemma sorted_append:
  assumes "sorted xs" "sorted ys" "∀x∈set xs. ∀y∈set ys. x ≤ y"
  shows "sorted (xs @ ys)"
using assms
proof (induction xs)
  case Nil
  then show ?case by simp
next
  case (Cons x xs)
  then have "sorted xs" and "sorted ys" by auto
  moreover have "∀z∈set xs. ∀y∈set ys. z ≤ y" using Cons.prems by auto
  ultimately have "sorted (xs @ ys)" using Cons.IH by simp
  moreover have "∀z∈set (xs @ ys). x ≤ z"
  proof -
    have "∀z∈set xs. x ≤ z" using Cons.prems by auto
    moreover have "∀z∈set ys. x ≤ z" using Cons.prems by auto
    ultimately show ?thesis by auto
  qed
  ultimately show ?case by (simp add: sorted_Cons)
qed
```

**Output summary**:
```
Theorem: sorted xs ∧ sorted ys ∧ (∀x∈xs. ∀y∈ys. x ≤ y) → sorted (xs @ ys)
Proof by induction on xs

├─ Base case: xs = []
│  └─ Simplification: sorted ([] @ ys) = sorted ys (given)
│
└─ Inductive case: xs = x # xs'
   ├─ IH: sorted xs' ∧ sorted ys ∧ (∀z∈xs'. ∀y∈ys. z ≤ y) → sorted (xs' @ ys)
   ├─ Apply IH: sorted (xs' @ ys)
   │  └─ Verified: xs' sorted, ys sorted, ordering holds
   ├─ Prove: x ≤ all elements in (xs' @ ys)
   │  ├─ x ≤ all in xs' (from sorted (x # xs'))
   │  └─ x ≤ all in ys (from assumption)
   └─ Conclusion: sorted (x # (xs' @ ys)) by sorted_Cons lemma
```

## Common Proof Patterns

### Pattern: Proof by Simplification

**Indicators**: `by simp`, `by auto`, `reflexivity.`, `auto.`

**Summary format**:
```
Direct proof by [method]
└─ [Brief description of what automation handles]
```

### Pattern: Proof by Induction

**Indicators**: `proof (induction ...)`, `induction ... as [|...]`

**Summary format**:
```
Proof by induction on <var>
├─ Base case: <var> = <base>
│  └─ <proof method>
└─ Inductive case: <var> = <constructor> <subterm>
   ├─ IH: <hypothesis>
   └─ <how IH is used>
```

### Pattern: Proof by Case Analysis

**Indicators**: `proof (cases ...)`, `destruct ... as [...]`

**Summary format**:
```
Proof by case analysis on <var>
├─ Case: <var> = <value1>
│  └─ <proof method>
└─ Case: <var> = <value2>
   └─ <proof method>
```

### Pattern: Equational Reasoning

**Indicators**: `also ... finally`, multiple `rewrite` steps

**Summary format**:
```
Equational reasoning
├─ Start: <expr1>
├─ = <expr2> (<justification>)
├─ = <expr3> (<justification>)
└─ = <goal>
```

### Pattern: Lemma Application

**Indicators**: `by (rule lemma)`, `apply lemma.`

**Summary format**:
```
Apply lemma <name>
├─ Lemma: <statement>
└─ Instantiation: <parameters>
```

## Handling Different Proof Lengths

### Short Proofs (< 10 lines)

Provide a brief summary:
```
Proof: <one-line description of method>
```

### Medium Proofs (10-50 lines)

Use hierarchical outline with 2-3 levels:
```
Main strategy
├─ Step 1
└─ Step 2
```

### Long Proofs (> 50 lines)

Use full hierarchical outline with:
- Main structure (top level)
- Major cases or subgoals (second level)
- Key reasoning steps (third level)
- Omit routine details

## Quality Guidelines

### Good Summary Characteristics

✓ **Clear structure**: Hierarchical outline shows proof organization
✓ **Appropriate detail**: Captures key steps, omits routine ones
✓ **Readable**: Uses natural language, not just tactic names
✓ **Accurate**: Faithfully represents the proof logic
✓ **Informative**: Highlights non-obvious reasoning

### What to Include

- Main proof strategy (induction, cases, direct, equational)
- Case structure and how each case is resolved
- Key lemmas or theorems applied
- Non-obvious reasoning steps
- Induction hypotheses and how they're used
- Important intermediate facts

### What to Omit

- Routine simplification (`by simp`, `reflexivity.`)
- Obvious arithmetic
- Trivial case analysis
- Repetitive patterns
- Low-level tactic details
- Proof management commands (`next`, `qed`, etc.)

## References

Detailed guides for proof analysis:

- **[summarization_patterns.md](references/summarization_patterns.md)**: Patterns for recognizing and summarizing common proof structures
- **[tactic_interpretation.md](references/tactic_interpretation.md)**: Guide for interpreting tactics into reasoning steps

Load these references when:
- Encountering unfamiliar proof patterns
- Need detailed tactic interpretation
- Working with complex nested proofs
- Unsure how to structure the summary

## Tips

1. **Start with structure**: Identify the main proof pattern first
2. **Group related steps**: Combine sequences into logical units
3. **Use hierarchy**: Indent to show proof structure clearly
4. **Be selective**: Include key steps, omit routine ones
5. **Natural language**: Describe reasoning, not just tactics
6. **Preserve logic**: Ensure summary accurately reflects proof flow
7. **Highlight insights**: Give more detail to non-obvious steps
