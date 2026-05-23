---
name: assertion-design
description: SystemVerilog Assertions (SVA) as executable specifications. Use when defining timing requirements, protocol specifications, or formal properties for RTL verification.
---

# Assertion-Based Specification Design

SVA methodology treating assertions as executable specifications, not testbench utilities.

## Core Principle (MANDATORY)

**Specifications SHALL be written as SystemVerilog Assertions**

- Natural language explanations are secondary and optional
- RTL implementation details MUST NOT be referenced unless unavoidable
- Written assertions MUST be sufficient to understand intended behavior without reading RTL
- Assertions define **what** the design must do, not **how** it does it

## When to Use This Skill

- Defining timing specifications for RTL modules
- Specifying protocol requirements (AXI4, UART, custom interfaces)
- Creating formal properties for transaction sequences
- Reviewing assertion coverage completeness
- Debugging temporal property failures

## Directory and File Policy (MANDATORY)

### Assertion File Locations

```
sim/assertions/
├── spec/              # Timing-related specifications (REQUIRED location)
│   ├── uart_timing_spec.sva
│   ├── axi4_protocol_spec.sva
│   └── frame_parser_timing_spec.sva
├── functional/        # Functional correctness assertions
│   ├── Frame_Parser_Assertions.sv
│   └── Uart_Tx_Assertions.sv
└── bind/              # Bind statements
    ├── bind_Frame_Parser.sv
    └── bind_Uart_Tx.sv
```

**Critical Rules:**
- All timing-related specifications → [sim/assertions/spec/](../../sim/assertions/spec/)
- Functional module assertions → [sim/assertions/functional/](../../sim/assertions/functional/)
- Bind statements → [sim/assertions/bind/](../../sim/assertions/bind/)
- **NEVER** embed assertions inside DUT modules

## Assertion Separation (MANDATORY)

### ❌ Wrong: Assertions in DUT

```systemverilog
module Frame_Parser (/*...*/);
    // ❌ Never embed assertions in DUT
    assert property (@(posedge clk) frame_valid |-> byte_count >= 4);
endmodule
```

### ✅ Correct: Separate Assertion Module

```systemverilog
// File: sim/assertions/functional/Frame_Parser_Assertions.sv
module Frame_Parser_Assertions (
    input logic clk, 
    input logic rst, 
    input logic frame_valid,
    input logic [7:0] byte_count
);
    // Property definition
    property p_frame_minimum_length;
        @(posedge clk) disable iff (rst)
        frame_valid |-> byte_count >= 4;
    endproperty
    
    // Assertion
    a_frame_minimum_length: assert property (p_frame_minimum_length)
        else $error("Frame length violation: byte_count=%0d", byte_count);
    
    // Optional coverage
    c_frame_minimum_length: cover property (p_frame_minimum_length);
endmodule
```

### Bind Statement

```systemverilog
// File: sim/assertions/bind/bind_Frame_Parser.sv
`ifdef ENABLE_ASSERTIONS
bind Frame_Parser Frame_Parser_Assertions u_assertions (
    .clk(clk),
    .rst(rst),
    .frame_valid(frame_valid),
    .byte_count(byte_count)
);
`endif
```

**Enable at compile time:**
```bash
dsim +define+ENABLE_ASSERTIONS -f dsim_config.f
```

## Specification-First Design Pattern

### 1. Define Requirements as Properties

**Example: UART protocol timing spec**

```systemverilog
// File: sim/assertions/spec/uart_timing_spec.sva
module uart_timing_spec (
    input logic clk,
    input logic rst,
    input logic tx_start,
    input logic tx_done,
    input logic [15:0] baud_counter
);
    // Specification: TX duration must match baud rate
    property p_tx_duration;
        int start_time;
        @(posedge clk) disable iff (rst)
        (tx_start, start_time = $time) |-> 
        ##[1:$] (tx_done && ($time - start_time >= baud_counter * 10));
    endproperty
    
    a_tx_duration: assert property (p_tx_duration)
        else $error("TX duration too short");
    
    // Specification: No overlapping TX operations
    property p_no_tx_overlap;
        @(posedge clk) disable iff (rst)
        tx_start |-> !tx_start throughout ##[1:$] tx_done;
    endproperty
    
    a_no_tx_overlap: assert property (p_no_tx_overlap)
        else $error("TX overlap detected");
endmodule
```

### 2. Property Naming Convention

Use `p_` prefix for properties, `a_` for assertions, `c_` for coverage:

```systemverilog
property p_handshake_valid_before_ready;
    @(posedge clk) disable iff (rst)
    ready |-> valid;
endproperty

a_handshake: assert property (p_handshake_valid_before_ready)
    else $error("Ready asserted without valid");

c_handshake: cover property (p_handshake_valid_before_ready);
```

### 3. Formal Properties vs Implementation

**Good (specification-focused):**
```systemverilog
// Specifies: "Request must be followed by acknowledge within 10 cycles"
property p_request_ack_latency;
    @(posedge clk) disable iff (rst)
    request |-> ##[1:10] acknowledge;
endproperty
```

**Bad (implementation-focused):**
```systemverilog
// ❌ References internal state machine states
property p_state_machine_transition;
    @(posedge clk) disable iff (rst)
    (state == WAIT_ACK) |-> ##[1:10] (state == IDLE);
endproperty
```

## Temporal Operators

### Delay Operators

```systemverilog
// Fixed delay: exactly N cycles later
##N expr       // expr true N cycles after trigger

// Range delay: between M and N cycles
##[M:N] expr   // expr true M to N cycles after trigger

// Unbounded delay: eventually
##[1:$] expr   // expr true sometime in the future
```

### Implication Operators

```systemverilog
// Overlapping implication (same cycle)
antecedent |-> consequent

// Non-overlapping implication (next cycle)
antecedent |=> consequent

// Example: handshake protocol
property p_valid_ready_handshake;
    @(posedge clk) disable iff (rst)
    valid && ready |-> ##1 !valid;  // Valid drops after handshake
endproperty
```

### Repetition Operators

```systemverilog
// Consecutive repetition
signal[*N]             // signal true for exactly N cycles
signal[*M:N]           // signal true for M to N cycles

// Go-to repetition (allows gaps)
signal[->N]            // signal becomes true N times (eventually)

// Example: burst detection
property p_burst_transfer;
    @(posedge clk) disable iff (rst)
    burst_start |-> valid[*4];  // 4 consecutive valid cycles
endproperty
```

### Throughout Operator

```systemverilog
// Condition must hold throughout sequence
property p_hold_valid_until_ready;
    @(posedge clk) disable iff (rst)
    valid |-> valid throughout ##[1:$] ready;
endproperty
```

## AXI4-Lite Protocol Assertions

Example specification for AXI4-Lite write channel:

```systemverilog
// File: sim/assertions/spec/axi4_protocol_spec.sva
module axi4_protocol_spec (
    input logic clk,
    input logic rst,
    input logic awvalid, awready,
    input logic wvalid, wready,
    input logic bvalid, bready
);
    // AXI4 Rule: AWVALID stable until AWREADY
    property p_awvalid_stable;
        @(posedge clk) disable iff (rst)
        (awvalid && !awready) |=> $stable(awvalid);
    endproperty
    
    a_awvalid_stable: assert property (p_awvalid_stable)
        else $error("AXI4 violation: AWVALID changed before AWREADY");
    
    // AXI4 Rule: BVALID after both AW and W handshakes
    property p_bvalid_ordering;
        logic aw_done, w_done;
        @(posedge clk) disable iff (rst)
        (awvalid && awready, aw_done = 1) ##0
        (wvalid && wready, w_done = 1) ##0
        (aw_done && w_done) |-> ##[1:$] bvalid;
    endproperty
    
    a_bvalid_ordering: assert property (p_bvalid_ordering)
        else $error("AXI4 violation: BVALID ordering incorrect");
endmodule
```

## Debugging Assertion Failures

### 1. Enable Assertions with MCP

```bash
python mcp_server/mcp_client.py --workspace . --tool run_uvm_simulation \
    --test-name axiuart_basic_test --mode run --waves \
    --compile-args "+define+ENABLE_ASSERTIONS"
```

### 2. Assertion Failure Prioritization

**Investigate assertion failures BEFORE waveform inspection:**
1. Read assertion error message and property name
2. Identify violated specification requirement
3. Check if failure is DUT bug or assertion bug
4. Use waveform to understand failure context

### 3. Error Message Best Practices

```systemverilog
a_setup_time: assert property (p_setup_time_met)
    else $error("[%0t] Setup time violation: data=0x%h, required_stable=%0d cycles",
        $time, data_signal, SETUP_CYCLES);
```

## Assertion Coverage

### Measuring Specification Coverage

```systemverilog
// Cover all specified behaviors
c_normal_operation: cover property (p_normal_frame_processing);
c_error_recovery: cover property (p_error_frame_recovery);
c_back_to_back: cover property (p_back_to_back_frames);

// Cover corner cases
c_minimum_latency: cover property (
    @(posedge clk) disable iff (rst)
    request |-> ##1 acknowledge
);

c_maximum_latency: cover property (
    @(posedge clk) disable iff (rst)
    request |-> ##10 acknowledge
);
```

## Compilation Control

### Conditional Compilation

```systemverilog
`ifdef ENABLE_ASSERTIONS
module My_Module_Assertions (/*...*/);
    // Assertions here
endmodule

bind My_Module My_Module_Assertions u_assertions (.*);
`endif
```

### Severity Levels

```systemverilog
// Error (test fails)
assert property (p_critical) else $error("Critical failure");

// Warning (logged but test continues)
assert property (p_recommended) else $warning("Recommended practice violated");

// Info (just notification)
assert property (p_performance) else $info("Suboptimal performance detected");

// Fatal (simulation stops immediately)
assert property (p_safety_critical) else $fatal(1, "Safety violation - halting");
```

## Project-Specific Guidelines

### Reference Material

Follow detailed guidelines in:
- [sim/assertions/README.md](../../sim/assertions/README.md) - Assertion coding guidelines
- [docs/forCopilot-assertions.md](../../docs/) - Comprehensive assertion design rules (if exists)

### File Organization

```
sim/assertions/
├── spec/
│   └── <module>_timing_spec.sva          # Timing specifications
├── functional/
│   └── <Module>_Assertions.sv            # Functional properties
└── bind/
    └── bind_<Module>.sv                  # Bind statements
```

### Integration with MCP Workflow

MCP server can enable/disable assertions dynamically. See `mcp-workflow` skill for detailed command sequences.

## Additional Resources

- **Assertion guidelines**: [sim/assertions/README.md](../../sim/assertions/README.md)
- **DSIM assertion debugging**: Reference `dsim-debugging` skill
- **RTL coding standards**: Reference `rtl-coding-standards` skill for module structure

## Summary

Assertion design principles:
1. Assertions define specifications, not implementations
2. Never embed assertions in DUT modules - use separate assertion modules with `bind`
3. Timing specs → [sim/assertions/spec/](../../sim/assertions/spec/)
4. Use `p_` prefix for properties, `a_` for assertions, `c_` for coverage
5. Assertions drive debugging - investigate failures before waveforms
6. Enable with `+define+ENABLE_ASSERTIONS` at compile time
7. Properties should be RTL-agnostic (specify behavior, not structure)
