---
name: program-correctness-prover
description: "Generate Isabelle or Coq proofs establishing partial or total correctness of imperative programs from code and formal specifications. Use when users need to: (1) Prove program correctness using Hoare logic, (2) Generate verification conditions from pre/postconditions, (3) Construct loop invariants and termination arguments, (4) Verify imperative programs with assignments, conditionals, and loops. Supports both partial correctness (if terminates, postcondition holds) and total correctness (terminates and postcondition holds) for both Isabelle/HOL and Coq."
---

# Program Correctness Prover

Generate formal proofs establishing correctness of imperative programs.

## Overview

This skill takes imperative program code with formal specifications (preconditions and postconditions) and generates complete correctness proofs in Isabelle or Coq using Hoare logic. It handles loop invariant generation, verification condition generation, and proof construction for both partial and total correctness.

## How to Use

Provide:
1. **Program code**: Imperative program (assignments, conditionals, loops)
2. **Specification**: Precondition and postcondition
3. **Target system**: Isabelle or Coq
4. **Correctness type**: Partial or total correctness

The skill will generate:
- Loop invariants (if needed)
- Verification conditions
- Complete formal proof
- Termination argument (for total correctness)

## Verification Workflow

### Step 1: Analyze Program Structure

Identify program components:
- **Assignments**: `x := E`
- **Sequences**: `C1; C2`
- **Conditionals**: `if B then C1 else C2`
- **Loops**: `while B do C`

### Step 2: Generate Loop Invariants

For each loop, construct an invariant that:

1. **Holds initially**: Precondition implies invariant
2. **Preserved by loop body**: `{I ∧ B} C {I}`
3. **Implies postcondition**: `I ∧ ¬B ⟹ Q`

**Strategies**:
- Generalize postcondition by replacing constants with loop variables
- Express partial computation at iteration i
- Maintain relationships between variables

### Step 3: Generate Verification Conditions

Apply Hoare logic rules to generate VCs:

**Assignment**: `{P[E/x]} x := E {P}`

**Sequence**: Chain intermediate conditions

**Conditional**: Prove both branches

**Loop**: Prove initialization, preservation, and termination

### Step 4: Construct Proof

Build formal proof in target system:
- Apply Hoare logic rules
- Prove each verification condition
- Use simplification and automation where possible

### Step 5: Add Termination Argument (Total Correctness)

Provide variant function V that:
- Is non-negative when loop condition holds
- Strictly decreases each iteration

## Example: Sum of Array

**Program**:
```
sum := 0;
i := 0;
while i < n do
  sum := sum + a[i];
  i := i + 1
done
```

**Specification**:
- Precondition: `n ≥ 0`
- Postcondition: `sum = Σ(a[0..n-1])`

**Analysis**:
- Loop accumulates sum of array elements
- Loop counter i ranges from 0 to n

**Loop Invariant**:
```
I: sum = Σ(a[0..i-1]) ∧ 0 ≤ i ≤ n
```

**Verification Conditions**:

1. **Initialization**: `n ≥ 0 ⟹ 0 = Σ(a[0..-1]) ∧ 0 ≤ 0 ≤ n`
   - Simplifies to: `n ≥ 0 ⟹ 0 = 0 ∧ 0 ≤ n` ✓

2. **Preservation**: `{I ∧ i < n} sum := sum + a[i]; i := i + 1 {I}`
   - WP: `sum + a[i] = Σ(a[0..i]) ∧ 0 ≤ i + 1 ≤ n`
   - Verify: From I and i < n, this holds ✓

3. **Postcondition**: `I ∧ ¬(i < n) ⟹ sum = Σ(a[0..n-1])`
   - From I and i ≥ n and i ≤ n, get i = n
   - So sum = Σ(a[0..n-1]) ✓

4. **Termination** (total correctness): `V = n - i`
   - Initially: V = n ≥ 0 ✓
   - Decreases: i := i + 1 makes V' = V - 1 < V ✓
   - Bounded: i ≤ n ⟹ V ≥ 0 ✓

**Isabelle Proof** (abbreviated):
```isabelle
lemma sum_array_partial:
  "⦃λs. s ''n'' ≥ 0⦄
   sum := 0;; i := 0;;
   While (λs. s ''i'' < s ''n'')
   Do (sum := (λs. s ''sum'' + s ''a'' (s ''i''));;
       i := (λs. s ''i'' + 1))
   ⦃λs. s ''sum'' = (∑j<s ''n''. s ''a'' j)⦄"
proof -
  define I where "I = (λs. s ''sum'' = (∑j<s ''i''. s ''a'' j) ∧
                            0 ≤ s ''i'' ∧ s ''i'' ≤ s ''n'')"

  (* Initialization *)
  have "⦃λs. s ''n'' ≥ 0⦄ sum := 0;; i := 0 ⦃I⦄"
    unfolding I_def by (auto intro: hoare_seq hoare_asgn)

  (* Loop body preserves invariant *)
  moreover have "⦃λs. I s ∧ s ''i'' < s ''n''⦄
                 sum := (λs. s ''sum'' + s ''a'' (s ''i''));;
                 i := (λs. s ''i'' + 1)
                 ⦃I⦄"
    unfolding I_def by (auto intro: hoare_seq hoare_asgn)

  (* Apply while rule *)
  ultimately have "⦃λs. s ''n'' ≥ 0⦄
                   sum := 0;; i := 0;;
                   While (λs. s ''i'' < s ''n'')
                   Do (sum := (λs. s ''sum'' + s ''a'' (s ''i''));;
                       i := (λs. s ''i'' + 1))
                   ⦃λs. I s ∧ ¬(s ''i'' < s ''n'')⦄"
    by (auto intro: hoare_seq hoare_while)

  (* Postcondition follows from invariant *)
  then show ?thesis
    unfolding I_def by (rule hoare_conseq) auto
qed
```

**Coq Proof** (abbreviated):
```coq
Theorem sum_array_partial : forall n a,
  n >= 0 ->
  {{ fun st => st N = n /\ n >= 0 }}
  sum ::= 0;;
  i ::= 0;;
  while i < N do
    sum ::= sum + a[i];;
    i ::= i + 1
  done
  {{ fun st => st sum = sum_array a n }}.
Proof.
  intros n a Hn.
  remember (fun st => st sum = sum_array a (st i) /\
                      0 <= st i /\ st i <= st N) as I.

  (* Initialization *)
  eapply hoare_seq. apply hoare_asgn.
  eapply hoare_seq. apply hoare_asgn.

  (* Loop *)
  eapply hoare_consequence_post.
  - apply hoare_while.
    (* Loop body *)
    eapply hoare_seq. apply hoare_asgn.
    eapply hoare_consequence_pre.
    + apply hoare_asgn.
    + intros st [HI Hcond]. subst I. simpl.
      destruct HI as [Hsum [Hi1 Hi2]].
      split; [|split]; try lia.
      rewrite Hsum. unfold sum_array. lia.
  - (* Postcondition *)
    intros st [HI Hcond]. subst I.
    destruct HI as [Hsum [Hi1 Hi2]].
    assert (st i = n) by lia.
    rewrite H. exact Hsum.
Qed.
```

## Example: Maximum of Two Numbers

**Program**:
```
if x >= y then
  max := x
else
  max := y
```

**Specification**:
- Precondition: `true`
- Postcondition: `max = max(x, y)`

**Analysis**:
- Conditional with two branches
- No loops, so no invariants needed

**Verification Conditions**:

1. **Then branch**: `{x ≥ y} max := x {max = max(x, y)}`
   - WP: `x = max(x, y)`
   - Verify: x ≥ y ⟹ x = max(x, y) ✓

2. **Else branch**: `{x < y} max := y {max = max(x, y)}`
   - WP: `y = max(x, y)`
   - Verify: x < y ⟹ y = max(x, y) ✓

**Isabelle Proof**:
```isabelle
lemma max_correct:
  "⦃λs. True⦄
   If (λs. s ''x'' ≥ s ''y'')
   Then max := (λs. s ''x'')
   Else max := (λs. s ''y'')
   ⦃λs. s ''max'' = max (s ''x'') (s ''y'')⦄"
proof (rule hoare_if)
  show "⦃λs. s ''x'' ≥ s ''y''⦄
        max := (λs. s ''x'')
        ⦃λs. s ''max'' = max (s ''x'') (s ''y'')⦄"
    by (rule hoare_conseq[OF hoare_asgn]) simp
next
  show "⦃λs. ¬(s ''x'' ≥ s ''y'')⦄
        max := (λs. s ''y'')
        ⦃λs. s ''max'' = max (s ''x'') (s ''y'')⦄"
    by (rule hoare_conseq[OF hoare_asgn]) simp
qed
```

**Coq Proof**:
```coq
Example max_correct :
  {{ fun st => True }}
  if x >= y then
    max ::= x
  else
    max ::= y
  {{ fun st => st max = max (st x) (st y) }}.
Proof.
  apply hoare_if.
  - eapply hoare_consequence_pre.
    + apply hoare_asgn.
    + intros st H. simpl. lia.
  - eapply hoare_consequence_pre.
    + apply hoare_asgn.
    + intros st H. simpl. lia.
Qed.
```

## Common Patterns

### Pattern: Sequential Assignments

**Program**: `x := E1; y := E2; z := E3`

**Strategy**: Work backwards with weakest precondition

### Pattern: Accumulation Loop

**Program**: `result := init; while i < n do result := f(result, a[i]); i := i + 1`

**Invariant**: `result = fold(f, init, a[0..i-1]) ∧ 0 ≤ i ≤ n`

### Pattern: Search Loop

**Program**: `found := false; while i < n && !found do if a[i] == target then found := true else i := i + 1`

**Invariant**: `(∀j. 0 ≤ j < i ⟹ a[j] ≠ target) ∧ 0 ≤ i ≤ n`

### Pattern: Nested Loops

**Program**: Outer loop with inner loop

**Invariants**: Outer invariant + inner invariant (may depend on outer variables)

## Correctness Types

### Partial Correctness

**Definition**: If precondition holds and program terminates, postcondition holds

**Hoare triple**: `{P} C {Q}`

**What to prove**:
- Initialization
- Preservation
- Postcondition follows from invariant

### Total Correctness

**Definition**: If precondition holds, program terminates AND postcondition holds

**Hoare triple**: `[P] C [Q]` (square brackets)

**What to prove**:
- Everything from partial correctness
- Termination via variant function

**Variant requirements**:
- Non-negative when loop condition holds
- Strictly decreases each iteration

## References

Detailed guides for program verification:

- **[hoare_logic.md](references/hoare_logic.md)**: Complete Hoare logic rules, weakest preconditions, and verification condition generation
- **[verification_patterns.md](references/verification_patterns.md)**: Common verification patterns with complete proofs in Isabelle and Coq

Load these references when:
- Need detailed Hoare logic rules
- Working with complex loop invariants
- Generating verification conditions
- Need example proofs for similar programs

## Tips

1. **Start simple**: Verify assignments and sequences before loops
2. **Generalize postcondition**: Often leads to good loop invariants
3. **State partial progress**: Invariant should express what's computed so far
4. **Include bounds**: Always include loop counter bounds in invariant
5. **Work backwards**: Use weakest precondition for simple programs
6. **Test invariant**: Check initialization, preservation, and postcondition
7. **Choose simple variants**: n - i is often sufficient for termination
8. **Use automation**: Let simp/auto handle arithmetic when possible
