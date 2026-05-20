---
name: tlaplus-model-reduction
description: Automatically simplify and minimize TLA+ specifications by reducing redundant state variables, merging equivalent actions, and minimizing invariants while preserving specified properties. Use when working with TLA+ specifications that need optimization, simplification, or reduction. Triggers when users ask to minimize, reduce, simplify, or optimize TLA+ specs, or when they want to remove redundancy from formal specifications while maintaining semantic equivalence.
---

# TLA+ Model Reduction (Spec Minimizer)

## Overview

This skill analyzes TLA+ specifications and produces minimized versions by eliminating redundancies while preserving all specified properties. The reduction process analyzes reachability, dependency relations, and property relevance to ensure semantic equivalence between the original and reduced specifications.

## Workflow

### Step 1: Input Analysis

Parse and understand the input TLA+ specification:

1. **Identify components**:
   - State variables (VARIABLES declaration)
   - Initial state predicate (Init)
   - Next-state relation (Next)
   - Invariants (INVARIANT declarations)
   - Temporal properties (PROPERTY declarations)
   - Type invariants and constraints

2. **Extract structure**:
   - List all actions (disjuncts in Next)
   - Identify action guards (enabling conditions)
   - Map variable dependencies
   - Note fairness constraints if present

3. **Understand properties**:
   - Safety properties to preserve
   - Liveness properties to maintain
   - User-specified invariants

### Step 2: Dependency Analysis

Build comprehensive dependency graphs:

1. **Variable dependency graph**:
   - For each variable, identify which actions read/write it
   - Determine which variables are used in property specifications
   - Find derived variables (computed from others)
   - Identify unused variables

2. **Action dependency graph**:
   - Map which actions enable/disable other actions
   - Identify independent vs. dependent action sequences
   - Find actions with identical effects

3. **Property dependency graph**:
   - Determine which variables each property depends on
   - Identify which actions affect property satisfaction

### Step 3: Identify Reduction Opportunities

Systematically find redundancies using the techniques in [reduction_techniques.md](references/reduction_techniques.md):

1. **Redundant state variables**:
   - Variables never referenced in actions or properties
   - Variables whose values are always derivable from others
   - Variables that remain constant after initialization

2. **Equivalent actions**:
   - Actions with identical guards and effects
   - Actions that differ only syntactically
   - Actions that can be merged without changing behavior

3. **Redundant invariants**:
   - Invariants implied by other invariants
   - Invariants that are always trivially true
   - Invariants not needed for property verification

### Step 4: Apply Reductions Incrementally

Perform reductions one at a time, verifying correctness after each:

1. **Remove redundant variables**:
   - Eliminate unused variables first (safest)
   - Remove derived variables and update references
   - Simplify expressions after variable removal

2. **Merge equivalent actions**:
   - Combine actions with identical effects
   - Simplify the Next-state relation
   - Preserve action names in comments for traceability

3. **Minimize invariants**:
   - Remove implied invariants
   - Keep minimal set that ensures all properties
   - Document which invariants were removed and why

4. **Simplify expressions**:
   - Reduce complex boolean expressions
   - Eliminate dead code in action definitions
   - Simplify guards when possible

### Step 5: Verify Semantic Equivalence

Ensure the reduced specification is equivalent to the original:

1. **Reachability preservation**:
   - Verify the reduced spec reaches the same states (modulo removed variables)
   - Check that no new behaviors are introduced
   - Confirm all original behaviors are preserved

2. **Property preservation**:
   - Verify all safety properties still hold
   - Confirm liveness properties are maintained
   - Check that fairness constraints are preserved

3. **Refinement relationship**:
   - Establish that reduced spec refines the original
   - Define refinement mapping if variables were removed
   - Explain the correspondence between states

### Step 6: Generate Output

Produce the minimized specification and justification:

1. **Minimized TLA+ specification**:
   - Write the complete reduced spec
   - Use clear formatting and structure
   - Add comments explaining major changes

2. **Reduction summary**:
   - List all reductions performed:
     - Variables removed (with reasons)
     - Actions merged (with justification)
     - Invariants eliminated (with explanation)
   - Quantify the reduction (e.g., "Reduced from 8 to 5 variables")

3. **Correctness justification**:
   - Explain why each reduction preserves semantics
   - Describe the refinement mapping if applicable
   - Reference dependency analysis results
   - Note any assumptions made

## Example Usage

**User request**: "Minimize this TLA+ spec while preserving the safety property"

**Process**:
1. Parse the spec and identify 3 state variables, 4 actions, 2 invariants
2. Build dependency graphs showing variable `temp` is only used internally
3. Identify that `Action1` and `Action2` have identical effects
4. Determine that `Inv2` is implied by `Inv1`
5. Remove `temp`, merge actions, eliminate `Inv2`
6. Output reduced spec with 2 variables, 3 actions, 1 invariant
7. Provide justification: "`temp` removed (derived from `x` and `y`), actions merged (identical guards and effects), `Inv2` removed (implied by `Inv1`)"

## Important Notes

- Always preserve the original specification's semantics
- Document all assumptions made during reduction
- If uncertain about a reduction's correctness, keep the original form
- Prioritize safety: when in doubt, don't reduce
- For complex specs, consider using TLC model checker to verify equivalence
- Maintain traceability between original and reduced specifications

## References

- [reduction_techniques.md](references/reduction_techniques.md) - Detailed reduction techniques and strategies
