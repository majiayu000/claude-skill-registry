---
name: model-guided-code-repair
description: Automatically repair code violations of temporal properties using model-checking counterexamples as guidance. Use when working with formal verification results, temporal logic property violations (LTL, CTL), model checking counterexamples, or when asked to repair property violations, fix counterexamples, repair temporal properties, fix model checking violations, or repair code based on counterexamples. Applicable to concurrent systems, state machines, synchronization issues, safety/liveness properties, and resource management violations.
---

# Model-Guided Code Repair

## Overview

This skill enables automatic repair of code that violates temporal properties by analyzing model-checking counterexamples. It reasons about the root cause of violations at the model level, proposes minimal and semantically justified code modifications, and validates repairs through re-verification or test generation.

## Repair Workflow

Follow this sequential process when repairing temporal property violations:

### 1. Analyze Input

Gather and understand three required inputs:

- **Program source code**: The code containing the violation
- **Violated temporal property**: The formal specification (LTL, CTL, or natural language description)
- **Counterexample trace**: The execution path demonstrating the violation

Read all inputs carefully. If the temporal property is in natural language, formalize it first.

### 2. Understand the Counterexample

Trace through the counterexample step-by-step:

- Identify the sequence of states and transitions
- Map counterexample states to program locations (line numbers, function calls)
- Identify variable values at each step
- Pinpoint the exact moment the property is violated

**Output**: A clear narrative of the execution path leading to the violation.

### 3. Identify Root Cause

Analyze why the violation occurs:

- **Missing guards**: Are conditions missing that should prevent certain transitions?
- **Incorrect ordering**: Are operations executed in the wrong sequence?
- **Race conditions**: Are there synchronization issues in concurrent code?
- **Missing state updates**: Are variables not being updated correctly?
- **Incorrect logic**: Are conditional expressions wrong?

**Output**: A precise diagnosis of the model-level cause.

### 4. Propose Repair Strategy

Design a minimal repair that:

- Directly addresses the root cause
- Preserves intended program behavior
- Minimizes code changes
- Maintains code readability

Common repair strategies:

- **Add guards**: Insert conditional checks to prevent invalid transitions
- **Reorder operations**: Adjust execution sequence to satisfy temporal ordering
- **Add synchronization**: Insert locks, semaphores, or barriers for concurrent code
- **Update state management**: Fix variable assignments or state transitions
- **Strengthen preconditions**: Add assertions or input validation

**Output**: A clear repair plan with justification.

### 5. Generate Repaired Code

Implement the repair:

- Make minimal, targeted changes to the source code
- Clearly mark what was changed (comments or annotations)
- Ensure the repair is syntactically correct
- Preserve existing code style and conventions

**Output**: Modified source code with changes clearly indicated.

### 6. Validate the Repair

Verify that the repair resolves the violation:

**Option A: Re-run Model Checker**
- Execute the model checker on the repaired code
- Verify the temporal property now holds
- Check that no new violations were introduced

**Option B: Generate and Run Tests**
- Create test cases based on the counterexample
- Generate additional tests for edge cases
- Execute tests and verify they pass
- Ensure existing tests still pass (regression testing)

**Output**: Validation results showing the property is satisfied.

### 7. Document the Repair

Provide a comprehensive explanation:

- **Root cause**: What caused the violation
- **Repair strategy**: Why this approach was chosen
- **Minimality justification**: Why this is the smallest necessary change
- **Behavior preservation**: How intended functionality is maintained
- **Validation results**: Evidence that the repair works

## Output Format

Structure the final output as follows:

```
## Repaired Code

[Modified source code with changes clearly marked]

## Changes Made

- [Line X]: [Description of change]
- [Line Y]: [Description of change]

## Root Cause Analysis

[Explanation of what caused the violation]

## Repair Strategy

[Why this repair approach was chosen]
[Why it is minimal and semantically justified]

## Behavior Preservation

[How the repair maintains intended program behavior]

## Validation Results

[Model checking results OR test execution results]
[Confirmation that the property now holds]
```

## Common Scenarios

### Safety Property Violations

**Example**: "The system must never enter an error state"

- Look for missing error checks or exception handling
- Add guards to prevent invalid state transitions
- Validate with assertions or model checking

### Liveness Property Violations

**Example**: "Every request must eventually be processed"

- Look for deadlocks, infinite loops, or missing progress conditions
- Add fairness constraints or progress guarantees
- Validate with liveness checking or timeout tests

### Synchronization Issues

**Example**: "Shared resources must be accessed atomically"

- Look for race conditions or missing locks
- Add synchronization primitives (mutexes, semaphores)
- Validate with concurrency testing or model checking

### State Machine Violations

**Example**: "State transitions must follow the specified protocol"

- Look for missing state checks or incorrect transition logic
- Add state validation or fix transition conditions
- Validate with state machine verification

## Tips for Effective Repairs

- **Start simple**: Try the minimal fix first before complex refactoring
- **Preserve structure**: Maintain the original code architecture when possible
- **Consider side effects**: Ensure repairs don't break other properties
- **Document assumptions**: Note any assumptions made during repair
- **Test thoroughly**: Validate beyond just the violated property
- **Iterate if needed**: If the first repair doesn't work, analyze why and adjust

## Integration with Model Checkers

This skill works with various model checking tools:

- **SPIN**: For Promela models and LTL properties
- **NuSMV/nuXmv**: For SMV models and CTL/LTL properties
- **CBMC**: For C programs with assertions
- **Java PathFinder**: For Java programs
- **TLA+**: For TLA+ specifications

When counterexamples are provided in tool-specific formats, translate them into a clear execution trace before analysis.
