---
name: rtl-equivalence-checker
description: "Hardware verification tool for checking functional equivalence between two RTL designs (Verilog). Use when users need to: (1) Verify if two RTL versions are functionally equivalent, (2) Compare original vs. refactored RTL code, (3) Validate design changes or optimizations, (4) Identify semantic vs. cosmetic differences, (5) Generate counterexamples for non-equivalent designs. Analyzes interface alignment, state variables, logic differences, and produces detailed equivalence verdicts with plain language explanations. Particularly effective for design verification, code reviews, and regression testing of RTL modifications."
---

# RTL Equivalence Checker

Verify functional equivalence between two RTL designs with detailed analysis and counterexample generation.

## Overview

This skill compares two Verilog RTL designs to determine if they are functionally equivalent. It aligns interfaces and state variables, distinguishes semantic differences from cosmetic refactoring, and generates minimal counterexample traces when designs differ.

## Workflow

### 1. Basic Equivalence Check

Compare two RTL designs:

```bash
python3 scripts/check_equivalence.py design_a.v design_b.v
```

Output includes:
- Equivalence verdict (EQUIVALENT or NOT EQUIVALENT)
- Explanation of differences
- Counterexample trace (if not equivalent)

### 2. With Assumptions

Specify clock and reset behavior:

```bash
python3 scripts/check_equivalence.py design_a.v design_b.v \
  --clock clk \
  --reset rst_n \
  --reset-active low
```

### 3. Save Results

Write results to file:

```bash
python3 scripts/check_equivalence.py design_a.v design_b.v -o results.txt
```

### 4. Ignore Signal Names

Focus on functional behavior, ignore naming differences:

```bash
python3 scripts/check_equivalence.py design_a.v design_b.v --ignore-names
```

## Analysis Process

The checker performs five steps:

**[1/5] Parsing RTL designs**
- Extracts module structure
- Identifies ports, signals, and state elements
- Parses always blocks and assignments

**[2/5] Aligning interfaces and state variables**
- Matches ports by name and type
- Aligns state elements (registers)
- Reports unmatched signals

**[3/5] Analyzing behavioral differences**
- Identifies cosmetic differences (naming, formatting)
- Identifies semantic differences (logic changes)
- Categorizes difference types

**[4/5] Determining equivalence**
- Verdict: EQUIVALENT or NOT EQUIVALENT
- Based on semantic differences only
- Cosmetic differences don't affect equivalence

**[5/5] Generating counterexample** (if not equivalent)
- Creates minimal test sequence
- Shows input values that expose difference
- Traces outputs from both designs

## Output Format

### Equivalent Designs

```
======================================================================
EQUIVALENCE CHECKING RESULTS
======================================================================

Verdict: EQUIVALENT

Explanation:
----------------------------------------------------------------------
The two RTL designs are functionally equivalent. All differences are
cosmetic (naming, formatting, or structurally equivalent refactoring).

Cosmetic Differences (non-functional):
----------------------------------------------------------------------
  - module_name: Module names differ: 'counter_v1' vs 'counter_v2'
  - signal_name: Signal 'cnt' renamed to 'count_value'

======================================================================
```

### Non-Equivalent Designs

```
======================================================================
EQUIVALENCE CHECKING RESULTS
======================================================================

Verdict: NOT EQUIVALENT

Explanation:
----------------------------------------------------------------------
The logic in always block 0 differs between the two designs, which
will result in different behavior. The sensitivity list for always
block 0 differs, which may cause the block to trigger at different
times.

Semantic Differences (functional):
----------------------------------------------------------------------
  - sensitivity_list: Block 0: Different sensitivity: 'posedge clk
    or posedge rst' vs 'posedge clk'
    Location: always block 0
  - logic_difference: Block 0: Logic differs
    Location: always block 0

Counterexample Trace:
----------------------------------------------------------------------
Length: 3 cycles

Cycle 0:
  Inputs: {'clk': 0, 'rst': 1, 'enable': 0}
  Output A: output_a_01
  Output B: output_b_02
  MISMATCH: Outputs differ: A=output_a_01, B=output_b_02

======================================================================
```

## Common Use Cases

### Design Refactoring

**Scenario:** Refactored RTL for readability, need to verify functionality unchanged.

**Approach:**
1. Run equivalence check on original vs. refactored
2. Review cosmetic differences (expected)
3. Verify no semantic differences
4. Confirm EQUIVALENT verdict

**Example:**
```bash
python3 scripts/check_equivalence.py original.v refactored.v
```

### Optimization Verification

**Scenario:** Optimized design for area/timing, need to verify correctness.

**Approach:**
1. Compare original vs. optimized design
2. Check for semantic differences
3. If not equivalent, review counterexample
4. Determine if difference is acceptable (e.g., latency change)

### Bug Fix Validation

**Scenario:** Fixed a bug, want to understand impact on behavior.

**Approach:**
1. Compare buggy vs. fixed version
2. Identify semantic differences
3. Review counterexample showing bug
4. Confirm fix addresses the issue

### Code Review

**Scenario:** Reviewing RTL changes in pull request.

**Approach:**
1. Run equivalence check on before/after
2. Distinguish intentional changes from unintended
3. Flag unexpected semantic differences
4. Approve if changes match intent

## Difference Types

### Cosmetic (Non-Functional)

These don't affect behavior:
- Module name changes
- Signal renaming
- Code formatting
- Comment changes
- Expression reordering (commutative operations)
- Structural refactoring (combining/splitting blocks)

### Semantic (Functional)

These change behavior:
- Different reset behavior (async vs. sync)
- Different logic expressions
- Different sensitivity lists
- Missing or extra logic
- Different state encodings
- Different pipeline depths
- Different bit widths

**See:** [equivalence_patterns.md](references/equivalence_patterns.md) for detailed examples

## Interpreting Results

### Verdict: EQUIVALENT

Designs are functionally equivalent. Safe to:
- Replace one with the other
- Merge refactoring changes
- Proceed with optimized version

### Verdict: NOT EQUIVALENT

Designs differ functionally. Actions:
1. **Review semantic differences** - Understand what changed
2. **Examine counterexample** - See concrete example of difference
3. **Determine if intentional** - Bug fix vs. unintended change
4. **Fix or accept** - Correct issue or document difference

### Understanding Counterexamples

Counterexample shows:
- **Input sequence** - Test vectors that expose difference
- **Cycle-by-cycle trace** - State progression
- **Output mismatch** - Where designs diverge
- **Plain language description** - What the difference means

## Advanced Options

### Custom Clock/Reset

Specify non-standard signal names:

```bash
python3 scripts/check_equivalence.py design_a.v design_b.v \
  --clock sys_clk \
  --reset async_rst \
  --reset-active high
```

### Counterexample Depth

Control trace length:

```bash
python3 scripts/check_equivalence.py design_a.v design_b.v \
  --max-depth 50
```

## Integration with Formal Tools

This skill provides pre-analysis before running formal verification tools.

**Workflow:**
1. Run this checker for quick analysis
2. Identify differences and assumptions needed
3. Run formal tool (Formality, Conformal) with appropriate constraints
4. Compare results

**See:** [formal_tools.md](references/formal_tools.md) for formal tool integration

## Limitations

This skill provides heuristic analysis. For rigorous proof:

1. **Use formal tools** - Synopsys Formality, Cadence Conformal
2. **Simulation** - Comprehensive testbench verification
3. **Manual review** - Expert analysis of complex cases

**Limitations:**
- Simplified parsing (not full Verilog parser)
- Heuristic difference detection
- Symbolic simulation (not actual execution)
- May miss subtle timing differences

**Best for:**
- Quick pre-analysis
- Identifying obvious differences
- Guiding formal verification
- Code review assistance

## Tips

- **Start with this checker** - Fast feedback on differences
- **Review cosmetic differences** - Ensure they're expected
- **Investigate semantic differences** - Understand each one
- **Use counterexamples** - Concrete examples aid understanding
- **Follow up with formal tools** - For rigorous proof
- **Document assumptions** - Clock, reset, state encoding
- **Test incrementally** - Verify small changes frequently

## Common Issues

**Interface mismatch:** Ports don't align between designs.
- Solution: Check port names, directions, widths match

**Too many differences:** Hard to understand results.
- Solution: Compare smaller modules, verify incrementally

**No counterexample:** Semantic difference found but no trace.
- Solution: Increase max-depth, or manually construct test case

**False positive:** Reports difference but designs seem equivalent.
- Solution: May be timing/encoding difference, use formal tools

## References

- **[equivalence_patterns.md](references/equivalence_patterns.md)**: Common equivalence patterns and examples
- **[formal_tools.md](references/formal_tools.md)**: Integration with formal verification tools

## Scripts

- **check_equivalence.py**: Main equivalence checking script
- **rtl_parser.py**: Verilog RTL parser
- **equivalence_analyzer.py**: Equivalence analysis engine
- **counterexample_generator.py**: Counterexample trace generator
