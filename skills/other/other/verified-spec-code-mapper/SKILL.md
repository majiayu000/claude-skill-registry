---
name: verified-spec-code-mapper
description: Establish explicit traceability between formal specifications (preconditions, postconditions, invariants) and verified code components with their correctness proofs. Produce structured Markdown mapping reports showing verification coverage and proof evidence. Use when auditing formal verification, documenting verified systems, establishing traceability for certification, or when the user asks to map specifications to code, generate verification reports, or analyze verification coverage in Coq, Dafny, Isabelle, or other proof assistants.
---

# Verified Spec-Code Mapper

## Overview

Establish explicit, evidence-based traceability between formal specifications and verified code components. Generate structured reports that map each specification to its implementation and correctness proofs, supporting verification auditing, documentation, and reproducibility.

## Mapping Workflow

### Step 1: Identify Specifications

Locate all formal specifications in the codebase:

1. **Preconditions:**
   - Coq: `forall ... -> P -> ...` (hypothesis before conclusion)
   - Dafny: `requires` clauses
   - Isabelle: `assumes` clauses
   - Look for: Input constraints, safety conditions

2. **Postconditions:**
   - Coq: `... -> Q` (conclusion of theorem)
   - Dafny: `ensures` clauses
   - Isabelle: `shows` clauses
   - Look for: Output guarantees, correctness properties

3. **Loop Invariants:**
   - Dafny: `invariant` clauses in loops
   - Coq: Lemmas about recursive functions
   - Look for: Properties maintained across iterations

4. **Class/Type Invariants:**
   - Dafny: `predicate Valid()` methods
   - Coq: Well-formedness predicates
   - Look for: Structural constraints, consistency properties

5. **Functional Correctness:**
   - Theorems stating what function computes
   - Equivalence to specification
   - Look for: Correctness lemmas, specification theorems

### Step 2: Map to Code Components

For each specification, identify corresponding code:

1. **Direct mapping:**
   - Specification mentions function/method name
   - Theorem statement references definition
   - Example: `Lemma factorial_positive : forall n, factorial n >= 1`
     → Maps to `factorial` function

2. **Contextual mapping:**
   - Specification in same file/module
   - Comments linking spec to code
   - Naming conventions (e.g., `sort_correct` → `sort`)

3. **Structural mapping:**
   - Preconditions → Function parameters
   - Postconditions → Return values
   - Invariants → Loop bodies or class fields

4. **Record locations:**
   - File path
   - Line numbers
   - Function/method/class names

### Step 3: Identify Verification Evidence

For each specification-code mapping, find proof evidence:

1. **Complete proofs:**
   - Coq: Ends with `Qed`
   - Dafny: Verified by Dafny verifier (no errors)
   - Isabelle: Ends with `done` or `qed`
   - Status: ✓ Fully Verified

2. **Incomplete proofs:**
   - Coq: Ends with `Admitted`
   - Isabelle: Contains `sorry`
   - Status: ✗ Unverified

3. **Assumed axioms:**
   - Coq: `Axiom` declarations
   - Isabelle: `axiomatization`
   - Status: ⚠ Assumed (no proof)

4. **External verification:**
   - SMT solver verification
   - Automated tool checks
   - Status: ✓ Verified (by tool)

5. **Record evidence:**
   - Theorem/lemma name
   - Proof location
   - Proof method
   - Dependencies (lemmas, axioms used)

### Step 4: Analyze Coverage

Determine verification completeness:

1. **Specification coverage:**
   ```
   Coverage = (Verified Specs / Total Specs) × 100%
   ```

2. **Code coverage:**
   ```
   Coverage = (Verified Functions / Total Functions) × 100%
   ```

3. **Proof completeness:**
   ```
   Completeness = (Complete Proofs / Total Proofs) × 100%
   ```

4. **Categorize status:**
   - ✓ **Fully Verified:** All specs proved, no assumptions
   - ⚠ **Partially Verified:** Some specs proved, some assumed
   - ✗ **Unverified:** No formal verification

5. **Identify gaps:**
   - Unverified specifications
   - Incomplete proofs
   - Missing specifications
   - Assumed axioms

### Step 5: Generate Report

Produce structured Markdown report:

1. **Choose report type:**
   - Function-centric: One function per section
   - Specification-centric: One spec per section
   - Module-level: Overview of entire module

2. **Include required sections:**
   - Specification statements (formal)
   - Code component references (with locations)
   - Verification evidence (proofs, theorems)
   - Coverage summary
   - Assumptions and gaps

3. **Use clear status indicators:**
   - ✓ Fully Verified
   - ⚠ Partially Verified (with assumptions)
   - ✗ Unverified

4. **Provide traceability:**
   - Link specs to code
   - Link code to proofs
   - Show dependency chains

## Mapping Patterns

For detailed patterns and templates, see [mapping_patterns.md](references/mapping_patterns.md).

### Quick Reference

| Specification Type | Typical Location | Verification Evidence |
|-------------------|------------------|----------------------|
| Precondition | `requires`, hypothesis | Checked by verifier or proved |
| Postcondition | `ensures`, conclusion | Theorem proving property |
| Loop Invariant | `invariant`, lemma | Induction proof |
| Class Invariant | `predicate Valid()` | Maintained by all methods |
| Functional Correctness | Theorem statement | Complete proof |

## Examples

### Example 1: Simple Function Mapping (Coq)

**Input Code:**
```coq
Definition divide (n m : nat) : option nat :=
  if m =? 0 then None else Some (n / m).

Lemma divide_safe : forall n m : nat,
  m <> 0 -> exists q, divide n m = Some q.
Proof.
  intros n m Hm.
  unfold divide.
  destruct (m =? 0) eqn:E.
  - apply Nat.eqb_eq in E. contradiction.
  - exists (n / m). reflexivity.
Qed.
```

**Generated Report:**
```markdown
# Verification Report: divide

## Function Signature
```coq
Definition divide (n m : nat) : option nat
```

## Specifications

### Precondition: Non-zero Divisor
- **Specification:** `m <> 0`
- **Location:** divide.v:4 (lemma hypothesis)
- **Status:** ✓ Fully Verified

### Postcondition: Returns Quotient
- **Specification:** `exists q, divide n m = Some q`
- **Location:** divide.v:4 (lemma conclusion)
- **Status:** ✓ Fully Verified

## Verification Evidence

### Theorem: divide_safe
- **Statement:** `forall n m, m <> 0 -> exists q, divide n m = Some q`
- **Location:** divide.v:4-10
- **Proof Status:** ✓ Complete (ends with Qed)
- **Proof Method:** Case analysis on `m =? 0`
- **Dependencies:** None

## Coverage Summary
- Specifications: 2 total, 2 verified (100%)
- Status: ✓ Fully Verified
```

### Example 2: Class with Invariants (Dafny)

**Input Code:**
```dafny
class BankAccount {
  var balance: int

  predicate Valid()
    reads this
  {
    balance >= 0
  }

  constructor(initial: int)
    requires initial >= 0
    ensures Valid()
    ensures balance == initial
  {
    balance := initial;
  }

  method Deposit(amount: int)
    requires Valid()
    requires amount >= 0
    modifies this
    ensures Valid()
    ensures balance == old(balance) + amount
  {
    balance := balance + amount;
  }
}
```

**Generated Report:**
```markdown
# Verification Report: BankAccount

## Class Invariant

### Invariant: Non-negative Balance
- **Specification:** `balance >= 0`
- **Location:** BankAccount.dfy:5 (Valid predicate)
- **Status:** ✓ Fully Verified

## Method: constructor

### Specifications
1. **Precondition: Non-negative Initial**
   - Specification: `requires initial >= 0`
   - Location: BankAccount.dfy:10
   - Status: ✓ Verified by Dafny

2. **Postcondition: Establishes Invariant**
   - Specification: `ensures Valid()`
   - Location: BankAccount.dfy:11
   - Status: ✓ Verified by Dafny

3. **Postcondition: Correct Balance**
   - Specification: `ensures balance == initial`
   - Location: BankAccount.dfy:12
   - Status: ✓ Verified by Dafny

## Method: Deposit

### Specifications
1. **Precondition: Valid State**
   - Specification: `requires Valid()`
   - Location: BankAccount.dfy:18
   - Status: ✓ Verified by Dafny

2. **Precondition: Non-negative Amount**
   - Specification: `requires amount >= 0`
   - Location: BankAccount.dfy:19
   - Status: ✓ Verified by Dafny

3. **Postcondition: Maintains Invariant**
   - Specification: `ensures Valid()`
   - Location: BankAccount.dfy:21
   - Status: ✓ Verified by Dafny

4. **Postcondition: Correct Balance Update**
   - Specification: `ensures balance == old(balance) + amount`
   - Location: BankAccount.dfy:22
   - Status: ✓ Verified by Dafny

## Coverage Summary
- Total Specifications: 7
- Fully Verified: 7 (100%)
- Status: ✓ Fully Verified
- Verification Method: Dafny automatic verifier
```

### Example 3: Module with Assumptions (Coq)

**Input Code:**
```coq
Require Import FunctionalExtensionality.

Definition compose {A B C : Type} (g : B -> C) (f : A -> B) : A -> C :=
  fun x => g (f x).

Lemma compose_assoc : forall (A B C D : Type)
  (f : A -> B) (g : B -> C) (h : C -> D),
  compose h (compose g f) = compose (compose h g) f.
Proof.
  intros.
  apply functional_extensionality.
  intro x. reflexivity.
Qed.
```

**Generated Report:**
```markdown
# Verification Report: compose

## Function Signature
```coq
Definition compose {A B C : Type} (g : B -> C) (f : A -> B) : A -> C
```

## Specifications

### Functional Correctness: Associativity
- **Specification:** `compose h (compose g f) = compose (compose h g) f`
- **Location:** compose.v:6-8
- **Status:** ⚠ Verified with Assumptions

## Verification Evidence

### Theorem: compose_assoc
- **Statement:** Composition is associative
- **Location:** compose.v:6-13
- **Proof Status:** ✓ Complete (ends with Qed)
- **Proof Method:** Functional extensionality + reflexivity
- **Dependencies:**
  - ⚠ **Axiom:** `functional_extensionality` (assumed)

## Assumptions

### Axiom: functional_extensionality
- **Statement:** `forall (A B : Type) (f g : A -> B), (forall x, f x = g x) -> f = g`
- **Source:** Coq standard library
- **Justification:** Standard axiom for function equality
- **Used in:** compose_assoc
- **Impact:** Widely accepted axiom, consistent with Coq's logic

## Coverage Summary
- Specifications: 1 total, 1 verified (100%)
- Status: ⚠ Partially Verified (relies on standard axiom)
- Confidence: High (standard axiom)
```

### Example 4: Traceability Matrix

**Generated Report:**
```markdown
# Verification Traceability Matrix: Sorting Module

| Spec ID | Specification | Code Component | Proof/Theorem | Status |
|---------|---------------|----------------|---------------|--------|
| SORT-001 | Permutation preservation | `sort` (sort.v:15) | `sort_permutes` (sort.v:45) | ✓ |
| SORT-002 | Output is sorted | `sort` (sort.v:15) | `sort_sorted` (sort.v:62) | ✓ |
| SORT-003 | Combined correctness | `sort` (sort.v:15) | `sort_correct` (sort.v:78) | ✓ |
| SORT-004 | Stability (equal elements) | `sort` (sort.v:15) | - | ✗ |
| SORT-005 | Time complexity O(n log n) | `sort` (sort.v:15) | - | ✗ |

## Summary
- Total Specifications: 5
- Fully Verified: 3 (60%)
- Unverified: 2 (40%)

## Verification Gaps

### SORT-004: Stability
- **Status:** ✗ Unverified
- **Reason:** Stability not formally specified or proved
- **Impact:** Cannot guarantee order of equal elements
- **Priority:** Medium

### SORT-005: Time Complexity
- **Status:** ✗ Unverified
- **Reason:** Complexity analysis not formalized
- **Impact:** Performance guarantees not verified
- **Priority:** Low (functional correctness verified)
```

## Constraints and Requirements

### MUST Requirements

1. **Evidence-based mapping:**
   - Only map specifications with explicit proof evidence
   - Do not infer mappings without verification
   - Clearly mark assumptions and axioms

2. **Preserve specification integrity:**
   - Report complete specifications (don't drop preconditions)
   - Don't merge distinct specifications
   - Don't weaken specifications

3. **Honest status reporting:**
   - ✓ Only for fully verified (complete proofs, no assumptions)
   - ⚠ For verified with assumptions/axioms
   - ✗ For unverified or incomplete

4. **Clear distinction:**
   - Separate verified from assumed
   - Distinguish complete from incomplete proofs
   - Mark external verification (SMT, automated tools)

### MUST NOT Requirements

1. **Do not infer:**
   - Don't assume specifications are verified without proof
   - Don't guess at verification status
   - Don't create mappings without evidence

2. **Do not merge:**
   - Keep specifications separate
   - Don't combine preconditions and postconditions
   - Maintain granularity

3. **Do not weaken:**
   - Report full specifications
   - Include all preconditions
   - Don't simplify for convenience

## Best Practices

1. **Be explicit:** Include file paths, line numbers, exact statements
2. **Be honest:** Report verification status accurately
3. **Be complete:** Document all assumptions and dependencies
4. **Be structured:** Use consistent report format
5. **Be traceable:** Link specs → code → proofs clearly
6. **Be auditable:** Provide enough detail for independent verification

## Report Format Guidelines

### Required Sections

1. **Specification Statement:** Formal specification (exact syntax)
2. **Code Component:** Function/method name and location
3. **Verification Evidence:** Theorem/proof name and status
4. **Coverage Summary:** Statistics and overall status
5. **Assumptions:** Any axioms or assumptions used
6. **Gaps:** Unverified specifications or incomplete proofs

### Status Indicators

- ✓ **Fully Verified:** Complete proof, no assumptions
- ⚠ **Partially Verified:** Proof with assumptions/axioms
- ✗ **Unverified:** No proof or incomplete proof

### Location Format

- File: `filename.ext`
- Line: `filename.ext:line`
- Range: `filename.ext:start-end`

## Resources

- **Mapping patterns:** See [mapping_patterns.md](references/mapping_patterns.md) for comprehensive patterns and templates
- **Coq documentation:** https://coq.inria.fr/documentation
- **Dafny documentation:** https://dafny.org/
- **Isabelle documentation:** https://isabelle.in.tum.de/documentation.html
