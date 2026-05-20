---
name: rtl-property-inference
description: Automatically infer formal correctness properties from Verilog/SystemVerilog RTL code and generate SystemVerilog Assertions (SVA). Identifies control-flow invariants (mutual exclusion, valid-ready handshakes, pipeline ordering, safety properties), liveness expectations, and temporal properties. Use when working with RTL designs that need formal property generation, when adding assertions to existing RTL, or when users ask to infer properties, generate assertions, or create formal specifications from hardware designs.
---

# RTL Property Inference

## Overview

This skill analyzes Verilog/SystemVerilog RTL code and automatically infers implicit correctness properties, generating formal SystemVerilog Assertions (SVA). The skill identifies common hardware patterns and generates appropriate safety, liveness, and fairness properties with clear explanations.

## Workflow

### Step 1: Parse and Understand RTL Structure

Analyze the input RTL code to extract key components:

1. **Identify signals and their roles**:
   - Clock and reset signals
   - Control signals (valid, ready, enable, grant, request)
   - Data signals
   - State variables (FSM states, counters, flags)

2. **Recognize structural patterns**:
   - State machines (one-hot, binary encoded)
   - Handshake protocols (valid-ready, req-ack)
   - Pipelines (with/without stalls)
   - FIFOs and buffers
   - Arbiters and mutual exclusion logic
   - Counters (saturating, wraparound)
   - Memory interfaces

3. **Extract clock/reset conventions**:
   - Clock signal name and edge (posedge/negedge)
   - Reset signal name, polarity (active high/low), and type (sync/async)
   - Reset values for state variables

### Step 2: Identify Control-Flow Invariants

Systematically analyze the design for common invariant patterns:

1. **Mutual Exclusion**:
   - Grant signals from arbiters
   - Mutually exclusive enable signals
   - One-hot state encodings
   - Look for: Multiple signals that should never be active simultaneously

2. **Valid-Ready Handshakes**:
   - Data stability during valid-without-ready
   - Valid persistence until handshake completes
   - No data loss (eventual completion)
   - Look for: Pairs of valid/ready signals with associated data

3. **Pipeline Ordering**:
   - Valid bit propagation through stages
   - Data stability in pipeline stages
   - Stall behavior (freezing pipeline state)
   - Look for: Arrays of valid signals, stage indices, pipeline registers

4. **Safety Properties** (bad things never happen):
   - Buffer overflow/underflow prevention
   - Invalid state detection
   - Address conflict prevention
   - Counter bounds
   - Look for: Boundary conditions, error states, conflict scenarios

### Step 3: Identify Liveness Properties

Look for patterns indicating "good things eventually happen":

1. **Request-Response Patterns**:
   - Request eventually gets grant
   - Valid eventually gets ready
   - Transaction eventually completes
   - Look for: Request signals paired with acknowledgment/grant signals

2. **Progress Properties**:
   - FSM eventually leaves certain states
   - Counters eventually reach targets
   - Pipelines eventually drain
   - Look for: Temporary states, countdown logic, completion conditions

3. **Fairness Constraints**:
   - All requesters eventually get service
   - Round-robin behavior
   - Starvation freedom
   - Look for: Arbitration logic, scheduling mechanisms

**Note**: Liveness properties require careful analysis. Only infer when there's clear evidence of intended eventual behavior. Use bounded liveness (with timeouts) when unbounded liveness may not hold.

### Step 4: Map Patterns to Properties

Use the pattern library in [common_patterns.md](references/common_patterns.md) to generate appropriate assertions:

1. **Match identified patterns** to known property templates
2. **Instantiate properties** with actual signal names from the design
3. **Adjust timing parameters** based on design characteristics (e.g., pipeline depth, timeout values)
4. **Add appropriate disable conditions** (typically reset)

Refer to [sva_syntax.md](references/sva_syntax.md) for SVA syntax details.

### Step 5: Classify Properties

Separate properties into clear categories:

1. **Strong Invariants** (assert):
   - Properties that must always hold in correct design
   - Internal consistency checks
   - Safety properties derived from design structure
   - Example: Mutual exclusion, one-hot encoding, buffer bounds

2. **Assumed Environment Constraints** (assume):
   - Properties about external inputs
   - Interface protocol assumptions
   - Timing assumptions from environment
   - Example: Input valid-ready protocol compliance, reset behavior

3. **Coverage Properties** (cover):
   - Reachability checks for important scenarios
   - Corner case coverage
   - Example: All FSM states reachable, maximum buffer occupancy

### Step 6: Generate Output

For each inferred property, provide:

1. **SVA assertion code**:
   ```systemverilog
   property_name: assert property (
     @(posedge clk) disable iff (rst)
       antecedent |-> consequent
   ) else $error("Description of violation");
   ```

2. **Natural-language explanation**:
   - What the property checks
   - Why it should hold
   - What violation would indicate

3. **Signal list**:
   - All signals involved in the property
   - Their roles (control, data, state)

4. **Classification**:
   - Type: Safety / Liveness / Fairness
   - Directive: Assert / Assume / Cover
   - Confidence: High / Medium / Low (based on pattern clarity)

5. **Additional context**:
   - Related properties (if any)
   - Assumptions made during inference
   - Suggested verification approach

## Output Format

Structure the output as follows:

```
## Inferred Properties for [Module Name]

### Clock and Reset
- Clock: <signal_name> (<edge>)
- Reset: <signal_name> (<polarity>, <sync/async>)

### Strong Invariants (Assert)

#### Property 1: <Short Name>
**Type**: Safety | Liveness | Fairness
**Confidence**: High | Medium | Low

**Assertion**:
```systemverilog
<property_name>: assert property (
  @(posedge clk) disable iff (rst)
    <property_expression>
) else $error("<error_message>");
```

**Explanation**:
<Natural language description of what this property checks and why>

**Signals Involved**:
- `<signal1>`: <role/description>
- `<signal2>`: <role/description>

**Rationale**:
<Why this property was inferred from the RTL structure>

---

[Repeat for each property]

### Assumed Environment Constraints (Assume)

[Same format as above, but using `assume` directive]

### Coverage Properties (Cover)

[Same format as above, but using `cover` directive]

### Summary

- Total properties inferred: <count>
  - Strong invariants: <count>
  - Environment assumptions: <count>
  - Coverage properties: <count>
- Patterns identified: <list of patterns>
- Verification recommendations: <suggestions>
```

## Important Guidelines

1. **Be conservative**: Only infer properties with clear evidence in the RTL
2. **Explain reasoning**: Always justify why a property was inferred
3. **Mark confidence**: Indicate confidence level (High/Medium/Low) for each property
4. **Avoid false positives**: Better to miss a property than infer an incorrect one
5. **Consider timing**: Ensure delay values match design behavior
6. **Check vacuity**: Suggest cover properties for antecedents to avoid vacuous success
7. **Document assumptions**: Clearly state any assumptions made during inference
8. **Provide context**: Explain how properties relate to overall design correctness

## Example Usage

**User request**: "Infer properties from this FIFO module"

**Process**:
1. Parse RTL and identify: full, empty, wr_en, rd_en, count signals
2. Recognize FIFO pattern with full/empty flags
3. Infer safety properties:
   - No write when full
   - No read when empty
   - Count within bounds [0:DEPTH]
   - Full and empty mutually exclusive (unless DEPTH=1)
4. Infer liveness property:
   - Write eventually makes FIFO non-empty
5. Generate SVA assertions with explanations
6. Classify as strong invariants (assert)
7. Add coverage for full and empty conditions

## References

- [common_patterns.md](references/common_patterns.md) - Library of common RTL patterns and their properties
- [sva_syntax.md](references/sva_syntax.md) - SystemVerilog Assertions syntax reference

## Limitations

- Cannot infer properties requiring deep semantic understanding beyond structural patterns
- May miss complex cross-module properties
- Liveness properties may need manual refinement for unbounded cases
- Timing parameters (delays, timeouts) may need adjustment based on actual design constraints
- Does not replace manual formal specification for critical properties
