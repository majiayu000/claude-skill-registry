---
name: uvm-verification
description: UVM testbench architecture and verification methodology for SystemVerilog. Use when creating UVM tests, agents, drivers, monitors, sequences, or scoreboards.
---

# UVM Verification Methodology

UVM testbench design patterns and best practices for the AXIUART_RV32I verification environment.

## When to Use This Skill

- Creating UVM testbench components (tests, environments, agents)
- Implementing drivers, monitors, sequences, or scoreboards
- Debugging UVM configuration or communication issues
- Resolving UVM naming convention questions
- Setting up factory patterns or objection management

## UVM Component Naming

### Component Hierarchy

| Component | Naming Pattern | Example |
|-----------|---------------|---------|
| **Test** | `<module>_<type>_test` | `axiuart_basic_test` |
| **Environment** | `<module>_env` | `axiuart_env` |
| **Agent** | `<protocol>_agent` | `uart_agent` |
| **Driver** | `<protocol>_driver` | `uart_driver` |
| **Monitor** | `<protocol>_monitor` | `uart_monitor` |
| **Sequencer** | `<protocol>_sequencer` | `uart_sequencer` |
| **Sequence** | `<protocol>_<action>_sequence` | `uart_write_sequence` |
| **Transaction** | `<protocol>_transaction` | `uart_transaction` |
| **Scoreboard** | `<module>_scoreboard` | `axiuart_scoreboard` |

### File Naming

| File Type | Pattern | Example |
|-----------|---------|---------|
| **Testbench** | `tb_<module>.sv` | `tb_axiuart_top.sv` |
| **UVM Test** | `<test_name>.sv` | `axiuart_basic_test.sv` |
| **UVM Package** | `<module>_pkg.sv` | `axiuart_uvm_pkg.sv` |

## UVM Component Templates

### Driver Template

```systemverilog
class uart_driver extends uvm_driver #(uart_transaction);
    `uvm_component_utils(uart_driver)
    
    virtual uart_if vif;
    
    function new(string name = "uart_driver", uvm_component parent = null);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db#(virtual uart_if)::get(this, "", "vif", vif)) begin
            `uvm_fatal(get_type_name(), "Virtual interface not found in config DB")
        endif
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        forever begin
            seq_item_port.get_next_item(req);
            drive_transaction(req);
            seq_item_port.item_done();
        end
    endtask
    
    virtual task drive_transaction(uart_transaction trans);
        // Implementation
        `uvm_info(get_type_name(), 
            $sformatf("Driving transaction: %s", trans.convert2string()), 
            UVM_HIGH)
    endtask
endclass
```

### Monitor Template

```systemverilog
class uart_monitor extends uvm_monitor;
    `uvm_component_utils(uart_monitor)
    
    virtual uart_if vif;
    uvm_analysis_port #(uart_transaction) analysis_port;
    
    function new(string name = "uart_monitor", uvm_component parent = null);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if (!uvm_config_db#(virtual uart_if)::get(this, "", "vif", vif)) begin
            `uvm_fatal(get_type_name(), "Virtual interface not found in config DB")
        endif
        analysis_port = new("analysis_port", this);
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        uart_transaction trans;
        forever begin
            trans = uart_transaction::type_id::create("trans");
            collect_transaction(trans);
            `uvm_info(get_type_name(), 
                $sformatf("Collected: %s", trans.convert2string()), 
                UVM_HIGH)
            analysis_port.write(trans);
        end
    endtask
    
    virtual task collect_transaction(uart_transaction trans);
        // Implementation
    endtask
endclass
```

### Agent Template

```systemverilog
class uart_agent extends uvm_agent;
    `uvm_component_utils(uart_agent)
    
    uart_driver    driver;
    uart_monitor   monitor;
    uart_sequencer sequencer;
    
    function new(string name = "uart_agent", uvm_component parent = null);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        
        monitor = uart_monitor::type_id::create("monitor", this);
        
        if (get_is_active() == UVM_ACTIVE) begin
            driver = uart_driver::type_id::create("driver", this);
            sequencer = uart_sequencer::type_id::create("sequencer", this);
        end
    endfunction
    
    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        if (get_is_active() == UVM_ACTIVE) begin
            driver.seq_item_port.connect(sequencer.seq_item_export);
        end
    endfunction
endclass
```

### Environment Template

```systemverilog
class axiuart_env extends uvm_env;
    `uvm_component_utils(axiuart_env)
    
    uart_agent      uart_agt;
    axi_agent       axi_agt;
    axiuart_scoreboard scoreboard;
    
    function new(string name = "axiuart_env", uvm_component parent = null);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        
        uart_agt = uart_agent::type_id::create("uart_agt", this);
        axi_agt = axi_agent::type_id::create("axi_agt", this);
        scoreboard = axiuart_scoreboard::type_id::create("scoreboard", this);
    endfunction
    
    virtual function void connect_phase(uvm_phase phase);
        super.connect_phase(phase);
        
        uart_agt.monitor.analysis_port.connect(scoreboard.uart_export);
        axi_agt.monitor.analysis_port.connect(scoreboard.axi_export);
    endfunction
endclass
```

### Test Template with Objections

```systemverilog
class axiuart_basic_test extends uvm_test;
    `uvm_component_utils(axiuart_basic_test)
    
    axiuart_env env;
    
    function new(string name = "axiuart_basic_test", uvm_component parent = null);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        env = axiuart_env::type_id::create("env", this);
    endfunction
    
    virtual task run_phase(uvm_phase phase);
        uart_write_sequence seq;
        
        phase.raise_objection(this, "Test starting");
        `uvm_info(get_type_name(), "========== Test Started ==========", UVM_LOW)
        
        // Test body
        seq = uart_write_sequence::type_id::create("seq");
        seq.start(env.uart_agt.sequencer);
        
        #1000ns;  // Wait for processing
        
        `uvm_info(get_type_name(), "========== Test Completed ==========", UVM_LOW)
        phase.drop_objection(this, "Test completed");
    endtask
endclass
```

## UVM Logging Standards

### Verbosity Levels

```systemverilog
// Informational (UVM_MEDIUM or UVM_HIGH)
`uvm_info(get_type_name(), 
    $sformatf("Transaction: addr=0x%08h, data=0x%08h", trans.addr, trans.data), 
    UVM_MEDIUM)

// Error (always displayed)
`uvm_error(get_type_name(), 
    $sformatf("CRC mismatch: expected=0x%04h, got=0x%04h", exp_crc, act_crc))

// Fatal error (stops simulation)
`uvm_fatal(get_type_name(), "Watchdog timeout - DUT not responding")
```

**Verbosity guidelines:**
- `UVM_LOW`: Test start/end, major phase transitions
- `UVM_MEDIUM`: Transaction-level events (default for regression)
- `UVM_HIGH`: Detailed signal-level activity (debug only)
- `UVM_FULL`: Exhaustive debug (rarely used)

### Message Formatting

Use `$sformatf` for structured messages:

```systemverilog
`uvm_info(get_type_name(),
    $sformatf("State transition: %s -> %s (cycle=%0d)", 
        state_to_string(prev_state), 
        state_to_string(new_state),
        cycle_count),
    UVM_MEDIUM)
```

## Configuration Database

### Setting Values

```systemverilog
// In testbench top
initial begin
    uvm_config_db#(virtual uart_if)::set(null, "uvm_test_top.env.uart_agt*", "vif", uart_if_inst);
    uvm_config_db#(int)::set(null, "uvm_test_top.env", "num_transactions", 100);
end
```

### Getting Values

```systemverilog
// In component build_phase
if (!uvm_config_db#(virtual uart_if)::get(this, "", "vif", vif)) begin
    `uvm_fatal(get_type_name(), "Virtual interface not found in config DB")
endif

// With default value
if (!uvm_config_db#(int)::get(this, "", "timeout", timeout)) begin
    timeout = 1000;  // Default
    `uvm_info(get_type_name(), $sformatf("Using default timeout: %0d", timeout), UVM_MEDIUM)
end
```

## Factory Pattern

### Registration

```systemverilog
class uart_transaction extends uvm_sequence_item;
    rand logic [7:0] data;
    rand logic parity;
    
    `uvm_object_utils_begin(uart_transaction)
        `uvm_field_int(data, UVM_ALL_ON)
        `uvm_field_int(parity, UVM_ALL_ON)
    `uvm_object_utils_end
    
    function new(string name = "uart_transaction");
        super.new(name);
    endfunction
endclass
```

### Creating Objects

```systemverilog
// Use factory instead of direct new()
uart_transaction trans = uart_transaction::type_id::create("trans");

// Enables runtime override
set_type_override_by_type(
    uart_transaction::get_type(),
    extended_uart_transaction::get_type()
);
```

## Sequence Patterns

### Basic Sequence

```systemverilog
class uart_write_sequence extends uvm_sequence #(uart_transaction);
    `uvm_object_utils(uart_write_sequence)
    
    rand int num_transactions;
    
    constraint c_num_trans {
        num_transactions inside {[10:50]};
    }
    
    function new(string name = "uart_write_sequence");
        super.new(name);
    endfunction
    
    virtual task body();
        `uvm_info(get_type_name(), 
            $sformatf("Starting sequence with %0d transactions", num_transactions), 
            UVM_MEDIUM)
        
        repeat (num_transactions) begin
            req = uart_transaction::type_id::create("req");
            start_item(req);
            if (!req.randomize()) begin
                `uvm_fatal(get_type_name(), "Randomization failed")
            endif
            finish_item(req);
        end
    endtask
endclass
```

## Scoreboard Pattern

```systemverilog
class axiuart_scoreboard extends uvm_scoreboard;
    `uvm_component_utils(axiuart_scoreboard)
    
    uvm_analysis_imp #(uart_transaction, axiuart_scoreboard) uart_export;
    uvm_analysis_imp #(axi_transaction, axiuart_scoreboard) axi_export;
    
    uart_transaction uart_queue[$];
    int pass_count, fail_count;
    
    function new(string name = "axiuart_scoreboard", uvm_component parent = null);
        super.new(name, parent);
    endfunction
    
    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        uart_export = new("uart_export", this);
        axi_export = new("axi_export", this);
    endfunction
    
    virtual function void write(uart_transaction trans);
        uart_queue.push_back(trans);
    endfunction
    
    virtual function void report_phase(uvm_phase phase);
        super.report_phase(phase);
        `uvm_info(get_type_name(), 
            $sformatf("Scoreboard results: PASS=%0d, FAIL=%0d", pass_count, fail_count),
            UVM_LOW)
    endfunction
endclass
```

## Verification Requirements

### DUT Integration

- Use actual RTL modules from [rtl/](../../rtl/) as DUTs; mocks are prohibited
- Never instantiate simplified or placeholder DUT models
- Verify module hierarchy matches actual synthesis structure

### Coverage

```systemverilog
class uart_transaction extends uvm_sequence_item;
    rand logic [7:0] data;
    rand logic parity;
    
    covergroup cg_uart;
        cp_data: coverpoint data {
            bins low = {[0:63]};
            bins mid = {[64:191]};
            bins high = {[192:255]};
        }
        cp_parity: coverpoint parity;
        cross cp_data, cp_parity;
    endgroup
    
    function new(string name = "uart_transaction");
        super.new(name);
        cg_uart = new();
    endfunction
endclass
```

## Project-Specific Patterns

### Test File Structure

All UVM tests located in [sim/tests/](../../sim/tests/):

```
sim/tests/
├── axiuart_basic_test.sv
├── axiuart_stress_test.sv
└── axiuart_error_injection_test.sv
```

### UVM Architecture

```
sim/uvm/
├── env/              # Environments
├── agents/           # Protocol agents
├── sequences/        # Stimulus sequences
├── tests/            # Top-level tests (also in sim/tests/)
└── tb/               # Testbench top modules
```

### Package Organization

```systemverilog
package axiuart_uvm_pkg;
    import uvm_pkg::*;
    `include "uvm_macros.svh"
    
    // Transactions
    `include "uart_transaction.sv"
    `include "axi_transaction.sv"
    
    // Sequences
    `include "uart_write_sequence.sv"
    
    // Components
    `include "uart_driver.sv"
    `include "uart_monitor.sv"
    `include "uart_agent.sv"
    
    // Environment
    `include "axiuart_env.sv"
    
    // Tests
    `include "axiuart_basic_test.sv"
endpackage
```

## Compilation and Execution

### Standard Test Workflow

See the `mcp-workflow` skill for detailed MCP command sequences. Brief overview:

```bash
# 1. Compile test
python mcp_server/mcp_client.py --workspace . --tool run_uvm_simulation \
    --test-name axiuart_basic_test --mode compile --verbosity UVM_LOW

# 2. Run with waves
python mcp_server/mcp_client.py --workspace . --tool run_uvm_simulation \
    --test-name axiuart_basic_test --mode run --verbosity UVM_MEDIUM --waves
```

## Additional Resources

- **UVM architecture**: [sim/uvm/README.md](../../sim/uvm/README.md)
- **MCP workflow**: Reference `mcp-workflow` skill for command sequences
- **Accellera UVM examples**: [reference/Accellera/uvm/distrib/examples/](../../reference/Accellera/uvm/distrib/examples/)

## Summary

Key UVM principles:
1. Use factory pattern for all component creation (`type_id::create()`)
2. Always check config DB retrieval with error handling
3. Raise/drop objections in test `run_phase`
4. Use `uvm_info`/`uvm_error`/`uvm_fatal` with appropriate verbosity
5. Connect analysis ports in `connect_phase`
6. Follow naming conventions: `<protocol>_driver`, `<module>_env`
7. Never use placeholder DUTs - always use actual RTL from [rtl/](../../rtl/)
