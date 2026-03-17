---
name: smv-model-extractor
description: "Automatically extract abstract finite-state models in SMV/NuSMV format from source code (C/C++, Java, Python) for formal model checking. Use when users need to: (1) Generate SMV models from program code for verification, (2) Extract state-transition models from protocol implementations, (3) Analyze control flow and data flow to construct formal models, (4) Create models for checking safety and liveness properties, (5) Convert imperative code to declarative state machines. Particularly effective for protocol implementations, concurrent systems, and control logic with clear state transitions."
---

# SMV Model Extractor

Automatically extract abstract finite-state models from source code for formal verification with NuSMV model checker.

## Overview

This skill transforms imperative programs (C/C++, Java, Python) into declarative SMV models suitable for model checking. It analyzes control flow, data flow, and program variables to construct states and transitions, applying appropriate abstraction to make models tractable while preserving properties of interest.

## Workflow

### 1. Analyze Source Code

Read and understand the program structure:

```bash
# For single file
python3 scripts/extract_model.py program.c -o model.smv

# For multiple files
python3 scripts/extract_model.py file1.c file2.c file3.java -o model.smv

# For entire directory
python3 scripts/extract_model.py src/*.py -o model.smv
```

The extractor automatically:
- Detects programming language from file extensions
- Parses source code into AST
- Identifies functions, control structures, and variables
- Builds control flow graph (CFG)

### 2. Apply Abstraction

The skill uses **medium abstraction** by default (balanced approach):

**Data abstraction:**
- Booleans → preserved as boolean
- Integers → bounded to small ranges (0..3)
- Pointers → abstracted to null/valid
- Arrays → abstracted to size properties
- Enums → preserved as enumerated types

**Control abstraction:**
- Preserve branching (if/else, switch)
- Preserve loops (while, for)
- Merge sequential statements
- Keep function boundaries

**Abstraction levels:**
```bash
# Low abstraction (more detail, larger state space)
python3 scripts/extract_model.py program.c -o model.smv --abstraction low

# Medium abstraction (recommended, balanced)
python3 scripts/extract_model.py program.c -o model.smv --abstraction medium

# High abstraction (minimal states, protocol phases only)
python3 scripts/extract_model.py program.c -o model.smv --abstraction high
```

### 3. Generate SMV Model

The extractor produces:

1. **model.smv** - Complete NuSMV model with:
   - MODULE main declaration
   - VAR section (state variables)
   - ASSIGN section (initial values and transitions)
   - Comments explaining structure

2. **model_mapping.txt** - Human-readable explanation:
   - How program states map to SMV states
   - Which variables are tracked
   - Transition conditions
   - Functions analyzed

**Example output structure:**
```smv
-- SMV Model automatically extracted from source code
MODULE main

VAR
  pc : {s0, s1, s2, s3};  -- program counter
  flag : boolean;
  count : 0..3;

ASSIGN
  init(pc) := s0;
  init(flag) := FALSE;
  init(count) := 0;

  next(pc) := case
    pc = s0 & !flag : s1;
    pc = s1 : s2;
    pc = s2 & count < 3 : s3;
    pc = s3 : s0;
    TRUE : pc;
  esac;

  next(count) := case
    pc = s2 & count < 3 : count + 1;
    TRUE : count;
  esac;
```

### 4. Add Verification Properties

After model generation, add temporal logic specifications to verify:

**Safety properties (things that should never happen):**
```smv
-- No buffer overflow
SPEC AG (count <= 3)

-- Mutual exclusion
SPEC AG !(process1_critical & process2_critical)
```

**Liveness properties (things that should eventually happen):**
```smv
-- Eventually reach goal state
SPEC AF (pc = s3)

-- Request eventually granted
SPEC AG (request -> AF grant)
```

See [smv_syntax.md](references/smv_syntax.md) for complete SMV syntax reference.

### 5. Run Model Checker

Verify the model with NuSMV:

```bash
# Check all specifications
NuSMV model.smv

# Interactive mode
NuSMV -int model.smv

# Generate counterexample if property fails
NuSMV -dcx model.smv
```

## Common Use Cases

### Protocol Implementation

**Scenario:** User has implemented a network protocol and wants to verify correctness.

**Approach:**
1. Extract model from protocol implementation
2. Identify protocol states (handshake, data transfer, teardown)
3. Add properties: message ordering, no deadlock, eventual completion
4. Verify with NuSMV

**See:** [extraction_patterns.md](references/extraction_patterns.md#pattern-1-client-server-protocol) for detailed protocol patterns.

### Concurrent System

**Scenario:** Multi-threaded program with shared resources.

**Approach:**
1. Extract models for each thread
2. Model shared variables and locks
3. Add mutual exclusion properties
4. Verify no race conditions or deadlocks

**See:** [extraction_patterns.md](references/extraction_patterns.md#pattern-2-mutual-exclusion-protocol)

### State Machine

**Scenario:** Program with explicit state variable and transitions.

**Approach:**
1. Direct mapping of program states to SMV states
2. Extract transition conditions
3. Verify reachability and liveness properties

**See:** [extraction_patterns.md](references/extraction_patterns.md#pattern-4-state-machine-protocol)

## Advanced Options

### Focus on Specific Functions

When codebase is large, focus extraction on relevant functions:

```bash
python3 scripts/extract_model.py program.c -o model.smv \
  --focus-functions connect disconnect send_message
```

### Track Specific Variables

Explicitly specify which variables to include in state:

```bash
python3 scripts/extract_model.py program.c -o model.smv \
  --track-vars connection_state buffer_count retry_limit
```

## Tips

- **Start simple**: Extract model for single function first, then expand
- **Check mapping file**: Review model_mapping.txt to understand state correspondence
- **Iterate abstraction**: If model checking is too slow, increase abstraction
- **Add properties incrementally**: Start with simple safety properties, then add liveness
- **Use counterexamples**: When property fails, NuSMV provides trace to debug

## Common Issues

**State explosion**: Model has too many states, verification is slow or fails.
- Solution: Increase abstraction level, focus on specific functions, bound integer ranges tighter

**Over-abstraction**: Model is too abstract, properties are trivially true/false.
- Solution: Decrease abstraction level, track more variables, preserve more control flow

**Missing transitions**: Model has deadlocks not present in original program.
- Solution: Check transition conditions, ensure all cases are covered, model external events

## References

- **[smv_syntax.md](references/smv_syntax.md)**: Complete NuSMV syntax reference with examples
- **[extraction_patterns.md](references/extraction_patterns.md)**: Detailed patterns for protocols, concurrency, state machines

## Scripts

- **extract_model.py**: Main extraction script (orchestrates entire process)
- **cfg_analyzer.py**: Control flow graph analysis module
- **smv_generator.py**: SMV model generation module
- **language_parser.py**: Multi-language parser (C/C++, Java, Python)
