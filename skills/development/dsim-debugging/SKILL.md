---
name: dsim-debugging
description: DSIM simulator debugging and troubleshooting. Use when investigating compilation errors, runtime failures, waveform analysis, or DSIM environment issues.
---

# DSIM Debugging and Troubleshooting

Debugging methodology for Metrics DSIM simulator in the AXIUART_RV32I verification environment.

## When to Use This Skill

- Investigating compilation or simulation failures
- Analyzing waveform data
- Troubleshooting DSIM environment configuration
- Resolving timescale mismatches or structural errors
- Optimizing simulation performance

## DSIM Environment Variables

### Required Variables (MANDATORY)

```powershell
# Check current environment
$env:DSIM_HOME
$env:DSIM_ROOT
$env:DSIM_LIB_PATH
$env:DSIM_LICENSE
```

### Verification

```bash
python mcp_server/mcp_client.py --workspace . --tool check_dsim_environment
```

**Expected output:**
```json
{
  "valid": true,
  "DSIM_HOME": "C:\\Metrics\\dsim-20231215",
  "DSIM_ROOT": "C:\\Metrics\\dsim-20231215",
  "DSIM_LIB_PATH": "C:\\Metrics\\dsim-20231215\\lib",
  "DSIM_LICENSE": "27020@license-server.local",
  "executable": "C:\\Metrics\\dsim-20231215\\bin\\dsim.exe"
}
```

### Common Issues

**Missing DSIM_HOME:**
```powershell
$env:DSIM_HOME = "C:\Metrics\dsim-20231215"
$env:DSIM_ROOT = $env:DSIM_HOME
$env:DSIM_LIB_PATH = "$env:DSIM_HOME\lib"
```

**License errors:**
```powershell
$env:DSIM_LICENSE = "27020@license-server.local"
dsim -version  # Test license connectivity
```

## Waveform Strategy

### MXD vs VCD

**Default: MXD waveform format** (Metrics proprietary)

**MXD advantages:**
- Faster dump performance
- Smaller file size
- Better compression
- Native DSIM format

**Enable MXD in simulation:**
```systemverilog
initial begin
    $dumpfile("sim/logs/axiuart_basic_test.mxd");
    $dumpvars(0, tb_axiuart_top);
end
```

**VCD (compatibility mode):**
```systemverilog
initial begin
    $dumpfile("sim/logs/axiuart_basic_test.vcd");
    $dumpvars(0, tb_axiuart_top);
end
```

**Avoid VCD unless:**
- Sharing waveforms with non-DSIM tools
- Post-processing with standard VCD parsers

## Assertion-Driven Debugging

### Priority Workflow

**1. Assertions FIRST → 2. Waveforms SECOND**

Investigate assertion failures before opening waveform viewer:

```bash
# Check assertion summary in log
grep "Assertion" sim/logs/axiuart_basic_test.log

# Filter for failures
grep "Assertion.*failed" sim/logs/axiuart_basic_test.log
```

### Assertion Error Analysis

**Example failure:**
```
** Error: [1250 ns] Assertion a_frame_minimum_length failed
   Frame length violation: byte_count=2
   File: sim/assertions/functional/Frame_Parser_Assertions.sv:15
```

**Investigation steps:**
1. Read assertion property definition (line 15)
2. Understand violated specification requirement
3. Determine if DUT bug or assertion bug
4. Use timestamp (1250 ns) to locate failure in waveform

### Enabling Assertions

```bash
python mcp_server/mcp_client.py --workspace . --tool run_uvm_simulation \
    --test-name axiuart_basic_test --mode run --waves \
    --compile-args "+define+ENABLE_ASSERTIONS"
```

Assertions located in:
- [sim/assertions/spec/](../../sim/assertions/spec/) - Timing specifications
- [sim/assertions/functional/](../../sim/assertions/functional/) - Functional properties
- [sim/assertions/bind/](../../sim/assertions/bind/) - Bind statements

## Troubleshooting Checklist

### 1. Confirm DSIM Environment Variables

```bash
python mcp_server/mcp_client.py --workspace . --tool check_dsim_environment
```

Verify all 4 required variables set correctly.

### 2. Inspect dsim_config.f Path List

Location: [sim/exec/dsim_config.f](../../sim/exec/dsim_config.f) or similar

```bash
# View compilation file list
Get-Content sim/exec/dsim_config.f
```

**Check for:**
- Correct file paths (no typos)
- Proper ordering (packages before modules)
- No missing files
- Correct include directories (`+incdir+`)

### 3. Ensure Timescale Match

**Every file MUST have:**
```systemverilog
`timescale 1ns / 1ps
```

**Detect mismatches:**
```bash
# Find files without timescale
Select-String -Path rtl\*.sv, sim\*.sv -Pattern '^`timescale' -NotMatch
```

**Common error:**
```
Error: Timescale mismatch: module 'Frame_Parser' (1ns/1ps) vs 'Uart_Tx' (1ps/1fs)
```

### 4. Verify Interface/RTL Structural Alignment

**Check bit widths:**
```systemverilog
// Interface definition
interface uart_if;
    logic [7:0] data;  // 8 bits
endinterface

// Module must match
module Uart_Tx (
    uart_if.master uart  // Uses 8-bit data
);
```

**Check signal directions:**
```systemverilog
// Interface modport
modport master (
    output tx_data,
    input  rx_data
);

// Module usage must match directions
module Uart_Controller (
    uart_if.master uart
);
    assign uart.tx_data = internal_tx;  // ✅ Output
    // assign uart.rx_data = ...  ❌ Can't drive input
```

### 5. Analyze DSIM Log Output

**Parse compilation errors:**
```bash
# Compilation phase errors
grep "Error" sim/logs/axiuart_basic_test.log | Select-Object -First 10
```

**Parse simulation errors:**
```bash
# Runtime errors
grep "Error\|Fatal" sim/logs/axiuart_basic_test.log
```

**UVM messages:**
```bash
# UVM_ERROR and UVM_FATAL
grep "UVM_ERROR\|UVM_FATAL" sim/logs/axiuart_basic_test.log
```

## DSIM Telemetry Analysis

### Telemetry JSON

Location: [sim/logs/<test_name>_telemetry.json](../../sim/logs/)

```json
{
  "compilation_time_seconds": 12.3,
  "simulation_time_seconds": 45.7,
  "memory_usage_mb": 512,
  "peak_memory_mb": 768,
  "events_processed": 1250000
}
```

### Performance Metrics

**Slow compilation:**
- Check for redundant package imports
- Verify file list ordering (packages first)
- Consider incremental compilation (`-genimage`)

**High memory usage:**
- Reduce waveform dump scope
- Limit UVM verbosity to UVM_MEDIUM
- Check for memory leaks in testbench

## Waveform Analysis

### Opening MXD Files

```bash
# DSIM waveform viewer
dsim -waves sim/logs/axiuart_basic_test.mxd
```

### Debugging Strategies

**1. Find assertion failure timestamp**
```
grep "Assertion.*failed" sim/logs/axiuart_basic_test.log
# Example: [1250 ns] Assertion a_handshake failed
```

**2. Navigate to timestamp in waveform**
- Jump to 1250 ns
- Add relevant signals to waveform view
- Trace signal history 10-20 cycles before failure

**3. Verify signal values**
- Check handshake signals (valid, ready)
- Verify state machine states
- Inspect data payloads

## Common Error Patterns

### Compilation Errors

**Undeclared identifier:**
```
Error: Undeclared identifier 'uart_if' at Frame_Parser.sv:10
```
**Solution:** Add interface to compile list or import package.

**Parameter override mismatch:**
```
Error: Parameter 'WIDTH' expects integer, got logic
```
**Solution:** Use correct parameter type in instantiation.

### Simulation Errors

**X-propagation:**
```
Warning: Signal 'data_out' driven with X value at 1250 ns
```
**Solution:** Check reset sequencing and initialization.

**Assertion failure:**
```
Error: Assertion a_protocol_timing failed at 3450 ns
```
**Solution:** Review protocol specification and DUT timing.

## Coverage Analysis

### Generate Coverage

```bash
python mcp_server/mcp_client.py --workspace . --tool run_uvm_simulation \
    --test-name axiuart_basic_test --mode run --coverage
```

### Review Coverage Report

Location: [sim/reports/coverage/](../../sim/reports/coverage/)

```bash
# Open HTML report
Start-Process sim/reports/coverage/index.html
```

**Key metrics:**
- Line coverage: % of RTL lines executed
- Toggle coverage: % of signals toggled
- Branch coverage: % of branches taken
- FSM coverage: % of state transitions

## Log File Organization

### Standard Locations

| Log Type | Location |
|----------|----------|
| **Compilation log** | [sim/logs/<test_name>_compile.log](../../sim/logs/) |
| **Simulation log** | [sim/logs/<test_name>.log](../../sim/logs/) |
| **Telemetry JSON** | [sim/logs/<test_name>_telemetry.json](../../sim/logs/) |
| **Result JSON** | [sim/logs/<test_name>_result.json](../../sim/logs/) |
| **Waveforms** | [sim/logs/<test_name>.mxd](../../sim/logs/) |

### Log Analysis Tools

```powershell
# Count errors
(Select-String -Path sim/logs/axiuart_basic_test.log -Pattern "Error").Count

# Extract UVM summary
Select-String -Path sim/logs/axiuart_basic_test.log -Pattern "UVM_INFO.*Test.*completed"

# Find assertion failures
Select-String -Path sim/logs/axiuart_basic_test.log -Pattern "Assertion.*failed"
```

## Escalation Criteria

### When to Escalate

- DSIM crashes or hangs
- License server connectivity issues
- Persistent X-propagation despite reset
- Coverage data corruption
- Waveform dump failures

### Escalation Data

Collect before escalating:
1. Full compilation log
2. Simulation log with `+verbose` flag
3. Telemetry JSON
4. DSIM version: `dsim -version`
5. Environment variables snapshot
6. Minimal reproducible test case

## Additional Resources

- **MCP workflow**: Reference `mcp-workflow` skill for command sequences
- **Assertion design**: Reference `assertion-design` skill for property debugging
- **Project logs**: [sim/logs/README.md](../../sim/logs/) (if exists)
- **DSIM documentation**: Check `DSIM_HOME/docs/`

## Summary

DSIM debugging principles:
1. Verify environment variables FIRST (`check_dsim_environment`)
2. Investigate assertions BEFORE waveforms
3. Enable MXD waveforms (default) over VCD
4. Check timescale consistency across all files
5. Inspect [dsim_config.f](../../sim/exec/dsim_config.f) for path ordering
6. Analyze telemetry JSON for performance insights
7. Parse logs systematically: errors → warnings → UVM messages
8. Use [sim/logs/](../../sim/logs/) as single source of truth for debugging data
