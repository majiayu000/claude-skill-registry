---
name: rtl-coding-standards
description: SystemVerilog RTL coding standards for FPGA/ASIC design. Use when generating RTL modules, interfaces, state machines, or reviewing RTL code structure.
---

# RTL Coding Standards

SystemVerilog coding standards for production RTL design in the AXIUART_RV32I project.

## When to Use This Skill

- Generating new RTL modules, interfaces, or packages
- Creating state machines or combinational/sequential logic
- Reviewing or refactoring existing RTL code
- Resolving naming convention or structural questions
- Implementing design patterns (FSMs, FIFOs, counters)

## Critical Rules (Never Violate)

### 1. Timescale Directive (MANDATORY)
Every RTL and interface file MUST begin with:
```systemverilog
`timescale 1ns / 1ps
```

### 2. Variable Declaration Placement (MANDATORY)
All variable declarations MUST be at the beginning of module/block:

✅ **Correct:**
```systemverilog
module Example (/*...*/);
    // All declarations first
    typedef enum logic [1:0] {IDLE, RUN, DONE} state_t;
    state_t state, state_next;
    logic [7:0] counter;
    logic valid;
    
    // Logic follows declarations
    always_comb begin
        // ...
    end
endmodule
```

❌ **Wrong:**
```systemverilog
module Example (/*...*/);
    logic [7:0] counter;
    
    always_comb begin
        logic temp;  // ❌ Declaration inside block
        temp = counter + 1;
    end
endmodule
```

### 3. Reset Convention (MANDATORY)
Default: Synchronous, active-high reset

✅ **Standard:**
```systemverilog
always_ff @(posedge clk) begin
    if (rst) begin
        counter <= '0;
    end else begin
        counter <= counter + 1;
    end
end
```

For active-low reset, invert explicitly:
```systemverilog
module My_Module (input logic clk, input logic rst_n);
    logic rst;
    assign rst = ~rst_n;  // Explicit inversion
    
    always_ff @(posedge clk) begin
        if (rst) begin  // Use internal active-high
            // ...
        end
    end
endmodule
```

### 4. Always Block Types (MANDATORY)
- Use `always_ff` for sequential logic
- Use `always_comb` for combinational logic
- Never use `always @*` in new code

```systemverilog
// Combinational logic
always_comb begin
    data_next = data;
    if (increment) data_next = data + 1;
end

// Sequential logic
always_ff @(posedge clk) begin
    if (rst) begin
        data <= '0;
    end else begin
        data <= data_next;
    end
end
```

### 5. Production Quality (MANDATORY)
Never generate:
- Placeholder code or comments like `// TODO`
- Stopgap solutions
- Temporary modules
- Unverifiable logic

## Naming Conventions

### RTL Elements

| Element | Convention | Example |
|---------|-----------|---------|
| **Modules** | Capitalized_With_Underscores | `Frame_Parser`, `Uart_Tx` |
| **Signals** | lowercase_with_underscores | `rx_fifo_data`, `frame_valid` |
| **Parameters** | ALL_CAPS_WITH_UNDERSCORES | `FIFO_DEPTH`, `CLK_FREQ_HZ` |
| **Localparams** | ALL_CAPS_WITH_UNDERSCORES | `SOF_BYTE`, `STATE_WIDTH` |
| **Enums** | lowercase_t suffix | `parser_state_t`, `axi_state_t` |
| **Enum Values** | ALL_CAPS | `IDLE`, `PROCESSING`, `ERROR` |
| **Interfaces** | lowercase_if suffix | `axi4_lite_if`, `uart_if` |
| **Functions** | lowercase_with_underscores | `calculate_crc()`, `state_to_string()` |
| **Tasks** | lowercase_with_underscores | `send_byte()`, `wait_for_ack()` |

### File Naming

| File Type | Pattern | Example |
|-----------|---------|---------|
| **RTL Module** | `Module_Name.sv` | `Frame_Parser.sv` |
| **Interface** | `interface_name_if.sv` | `axi4_lite_if.sv` |
| **Package** | `package_name_pkg.sv` | `axiuart_reg_pkg.sv` |

**Critical**: Module name MUST match file name exactly (case-sensitive).

## Design Patterns

### State Machine Template

Use three-process state machine with typed enums:

```systemverilog
// 1. State type with encoding hint
(* fsm_encoding = "one_hot" *)
typedef enum logic [3:0] {
    IDLE        = 4'b0001,
    PROCESSING  = 4'b0010,
    WAITING     = 4'b0100,
    ERROR       = 4'b1000
} state_t;

state_t state, state_next;

// 2. Helper function for debug (recommended)
function automatic string state_to_string(state_t st);
    case (st)
        IDLE:       return "IDLE";
        PROCESSING: return "PROCESSING";
        WAITING:    return "WAITING";
        ERROR:      return "ERROR";
        default:    return "UNKNOWN";
    endcase
endfunction

// 3. Combinational next-state logic
always_comb begin
    state_next = state;  // Default: hold state
    
    case (state)
        IDLE: begin
            if (start) state_next = PROCESSING;
        end
        PROCESSING: begin
            if (done) state_next = IDLE;
            else if (error) state_next = ERROR;
        end
        // ... other states
    endcase
end

// 4. Sequential state register
always_ff @(posedge clk) begin
    if (rst) begin
        state <= IDLE;
    end else begin
        state <= state_next;
    end
end

// 5. Output logic
always_comb begin
    busy = (state == PROCESSING);
    error_flag = (state == ERROR);
end
```

### Parameter Width Calculations

Use `$clog2()` for width calculations:

```systemverilog
module Fifo #(
    parameter int DEPTH = 64,
    parameter int DATA_WIDTH = 8
)(/*...*/);
    // Address width: log2(DEPTH)
    localparam int ADDR_WIDTH = $clog2(DEPTH);  // 6 bits for 64 entries
    
    // Count width: log2(DEPTH) + 1 for full detection
    localparam int COUNT_WIDTH = $clog2(DEPTH) + 1;  // 7 bits
    
    logic [ADDR_WIDTH-1:0]  wr_ptr, rd_ptr;
    logic [COUNT_WIDTH-1:0] count;  // 0 to DEPTH (inclusive)
endmodule
```

**Critical**: 64-entry FIFO requires 6-bit addresses (0-63) and 7-bit counter (0-64).

### Module Header Format

```systemverilog
`timescale 1ns / 1ps

// Brief module description (1-2 lines)
// Key features or notes
module Module_Name #(
    // Parameters grouped by category
    parameter int WIDTH = 32,
    parameter int DEPTH = 64
)(
    // Clock and reset first
    input  logic                clk,
    input  logic                rst,
    
    // Input signals grouped logically
    input  logic [WIDTH-1:0]    data_in,
    input  logic                valid_in,
    
    // Output signals grouped logically
    output logic [WIDTH-1:0]    data_out,
    output logic                valid_out,
    
    // Debug signals last (if any)
    output logic [7:0]          debug_state
);
    // Module body
endmodule
```

### Interface Definition with Modports

```systemverilog
`timescale 1ns / 1ps

interface axi4_lite_if #(
    parameter int ADDR_WIDTH = 32,
    parameter int DATA_WIDTH = 32
)(
    input logic clk,
    input logic rst
);
    // Signal declarations
    logic [ADDR_WIDTH-1:0] awaddr;
    logic                  awvalid;
    logic                  awready;
    // ... other signals
    
    // Modport for master
    modport master (
        output awaddr, awvalid,
        input  awready
        // ... other directions
    );
    
    // Modport for slave
    modport slave (
        input  awaddr, awvalid,
        output awready
        // ... other directions
    );
endinterface
```

## Project-Specific Rules

### Register Management (JSON SSOT)

Register definitions come from [register_map/axiuart_registers.json](../../register_map/axiuart_registers.json). Never hardcode addresses.

```systemverilog
import axiuart_reg_pkg::*;

module Register_Block #(
    parameter logic [31:0] BASE_ADDR = 32'h4000_0000
)(/*...*/);
    // Compute relative offsets
    localparam logic [11:0] REG_CONTROL_OFFSET = 
        (axiuart_reg_pkg::REG_CONTROL - BASE_ADDR);
    
    always_comb begin
        case (addr_offset)
            REG_CONTROL_OFFSET: rdata = control_reg;
            REG_STATUS_OFFSET:  rdata = status_reg;
            default:            rdata = '0;
        endcase
    end
endmodule
```

### Debug Signal Instrumentation

Prefix debug signals with `debug_`:

```systemverilog
module Frame_Parser (
    // Functional ports
    input  logic clk, rst,
    output logic frame_valid,
    
    // Debug ports (at end)
    output logic [7:0] debug_rx_data,
    output logic [3:0] debug_state,
    output logic       debug_crc_error
);
    // Implementation
endmodule
```

## Pre-Commit Checklist

Before committing RTL code:

- [ ] `` `timescale 1ns / 1ps`` present in every file
- [ ] All variable declarations at beginning of module/block
- [ ] Naming conventions followed (modules, signals, parameters)
- [ ] Reset type is synchronous active-high (or explicitly inverted)
- [ ] FIFO/counter widths correct (use `$clog2()`)
- [ ] `always_ff` for sequential, `always_comb` for combinational
- [ ] Module name matches file name exactly
- [ ] No placeholder code or TODO comments
- [ ] State machines use typed enums
- [ ] Interface modports defined (if using interfaces)
- [ ] Comments in English, limited to non-obvious logic

## Compilation Requirements

All code must compile with 0 errors, 0 warnings:

```bash
dsim -genimage image.so -sv -timescale 1ns/1ps -f dsim_config.f
```

## Additional Resources

- **Full coding standards**: [docs/systemverilog_coding_standards.md](../../docs/systemverilog_coding_standards.md)
- **Quick naming reference**: [docs/sv_naming_quick_ref.md](../../docs/sv_naming_quick_ref.md)
- **Project architecture**: [rtl/README.md](../../rtl/README.md)

## Summary

Core RTL coding principles:
1. `` `timescale 1ns / 1ps`` at top of every file
2. Modules: `Capitalized_With_Underscores`, signals: `lowercase_with_underscores`
3. `always_ff` for sequential, `always_comb` for combinational
4. Synchronous active-high reset (default)
5. All declarations at beginning of module/block
6. No placeholder code - production quality only
7. Module name matches file name exactly
