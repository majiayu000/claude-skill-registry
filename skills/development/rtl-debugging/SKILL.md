---
name: rtl-debugging
description: RTL design debugging methodology and reasoning process. Use when investigating test failures, assertion violations, scoreboard mismatches, or analyzing verification results to identify RTL bugs.
---

# RTL Debugging Methodology

Systematic approach for debugging RTL from verification results and test scenarios.

## When to Use This Skill

- Analyzing UVM test failures to identify RTL bugs
- Investigating assertion violations in simulation
- Debugging scoreboard mismatches between expected and actual behavior
- Triaging multiple test failures to find common root causes
- Understanding why specific test scenarios fail while others pass
- Analyzing coverage holes related to bugs

## Debugging Workflow (推論プロセス)

### 1. Analyze Test Failure Pattern

**Objective**: Understand which tests fail and why

**Questions to answer**:
- Which tests pass and which fail? (Pattern analysis)
- Do failures occur in specific test scenarios only?
- Is the failure deterministic or random? (Check with different seeds)
- At what phase does the test fail? (Build, run, scoreboard check)

**Evidence sources**:
- Test execution logs (sim/logs/)
- Regression test results (sim/reports/)
- UVM report summary (UVM_ERROR, UVM_FATAL locations)
- DSIM Collect Verification Evidence

**Objective**: Gather all available evidence from verification components

**Verification evidence sources**:

**From Assertions**:
```
UVM_ERROR @ 1250ns: Assertion 'a_axi_wdata_stable' failed
  Location: sim/assertions/axi4_protocol_checker.sv:45
  Property: wdata must remain stable when wvalid=1 and wready=0
```
→ RTL violates AXI4 protocol specification

**From Scoreboard**:
```
UVM_ERROR: [SCOREBOARD] Data mismatch detected
  Expected: 0xDEADBEEF
  Actual:   0xDEADBEE0
  Address:  0x1000
  Time:     1250ns
```
→ LSB nibble corrupted, check datapath width or masking logic

**From Monitor**:
```
UVM_WARNING: [MONITOR] Unexpected transaction observed
  Type: WRITE
  Address: 0x1004 (expected: 0x1000)
  PossiMap Evidence to RTL Problem Domain

**Objective**: Translate verification failures to RTL problem categories

**Evidence-to-Problem mapping**:

| Verification Evidence | RTL Problem Domain | Investigation Focus |
|----------------------|-------------------|---------------------|
| **Assertion: Protocol violation** | Interface logic | Check handshake FSM, signal timing |
| **Scoreboard: Data mismatch** | Datapath logic | Check ALU, mux select, forwarding |
| **Scoreboard: Missing transaction** | Control logic | Check enable signals, FSM transitions |
| **Scoreboard: Extra transaction** | Control logic | Check termination conditions, counters |
| **Monitor: Wrong address** | Address generation | Check increment/decrement logic, offset calculation |
| **Monitor: Wrong timing** | Pipeline control | Check stall logic, valid/ready propagation |
| **Assertion: X-propagation** | Reset/initialization | Check reset assignments, case completeness |

**Test scenario analysis**:

```
Failing scenario: Back-to-back writes with no idle cycles
Passing scenario: Writes with 2-cycle gaps

Hypothesis generation:
1. Pipeline hazard when no bubble between transactions
2. Backpressure handling assumes idle cycles
3. State machine doesn't handle consecutive valid inputs
4. Register forwarding path missing for zero-latency case
```Targeted Test Experiments

**Objective**: Create minimal test to isolate root cause

**Experiment design strategies**:

**Modify existing failing test**:
```systemverilog
// Original failing test: Back-to-back writes
sequence.add_transaction(WRITE, addr=0x1000, data=0xAA);
sequence.add_transaction(WRITE, addr=0x1004, data=0xBB);  // ← FAILS

// Experiment 1: Add gap between transactions
sequence.add_transaction(WRITE, addr=0x1000, data=0xAA);
sequence.add_idle_cycles(2);
sequence.add_transaction(WRITE, addr=0x1004, data=0xBB);  // ← PASS?
// If passes: Confirms pipeline hazard hypothesis

// Experiment 2: Same address back-to-back
sequence.add_transaction(WRITE, addr=0x1000, data=0xAA);
sequence.add_transaction(WRITE, addr=0x1000, data=0xBB);  // ← PASS/FAIL?
// If passes: Problem is address-generation specific
```

**Create minimal directed test**:
```systemverilog
// Hypothesis: Burst counter overflows at length=16
class minimal_burst_test extends base_test;
    virtual task run_phase(uvm_phase phase);
        phase.raise_objection(this);
        
        // Test exactly at boundary
        send_burst(addr=0x0, length=15);  // Should work
        send_burst(addr=0x0, length=16);  // Should fail
        send_burst(addr=0x0, length=17);  // Should fail
        
        phase.drop_objection(this);
    endtask
endclass
```

**Add debug assertions**:
```systemverilog
// Insert temporary assertion at suspected problem point
bind axi_slave_fsm debug_assertions (
    .clk(clk),
    .state(current_state),
    .wvalid(wvalid),
    .wready(wready)
);
Trace from Verification to RTL Root Cause

**Objective**: Navigate from high-level test failure to specific RTL bug

**Top-down tracing workflow**:

```
1. Test Failure
   └─ axiuart_burst_test fails with scoreboard mismatch
   
2. Scoreboard Analysis
   └─ Expected data: 0xBB, Actual: 0xAA
   └─ Second write returned first write's data
   
3. Monitor Analysis (check transactions observed)
   └─ WRITE(addr=0x1000, data=0xAA) @ 1000ns - acknowledged
   └─ WRITE(addr=0x1004, data=0xBB) @ 1002ns - acknowledged
   └─ READ(addr=0x1004) @ 1010ns - returned 0xAA (wrong!)
   
4. Waveform Analysis at 1002ns (second write)
   └─ axi_wdata = 0xBB ✓
   └─ axi_waddr = 0x1004 ✓
   └─ write_enable = 1'b1 ✓
   └─ But: register_select still points to 0x1000 ✗
   
5. RTL Module Analwith Test Suite

**Objective**: Confirm fix resolves issue without breaking other tests

**Verification workflow**:

**Step 1: Re-run failing test**
```bash
# Run specific test that previously failed
run_uvm_simulation --test axiuart_burst_test --seed 12345
# Expected: PASS
```

**Step 2: Run related tests** (test suite partitioning)
```bash
# Run all tests that exercise same RTL module
run_uvm_simulation --regression smoke_suite
# Focus: Tests with write transactions, address decoding
```

**Step 3: Full regression**
```Test Failure Pattern Analysis (問題分類)

### By Test Failure Type

| Failure Type | Root Cause Category | Investigation Focus |
|-------------|---------------------|---------------------|
| **Scoreboard mismatch: wrong data** | Datapath error | Trace data from source to sink, check mux selects, forwarding |
| **Scoreboard mismatch: missing transaction** | Control flow error | Check FSM transitions, enable signals, counter termination |
| **Scoreboard mismatch: extra transaction** | Control flow error | Check counter overflow, FSM looping, duplicate strobes |
| **Assertion: Protocol violation** | Interface timing | Check handshake sequences, stability requirements, backpressure |
| **Assertion: Stability violation** | Combinational logic | Check for unintended signal changes, glitches, race conditions |
| **Assertion: X-propagation** | Initialization error | Check reset coverage, case statement completeness, undriven signals |
| **Timeout: No response** | Deadlock or FSM stuck | Check FSM for unreachable transitions, missing conditions |
| **UVM_FATAL: Null object** | Verification code bug | Not RTL issue - check testbench configuration |

### By Test Pass/Fail Pattern

**Pattern: Only random tests fail, directed tests pass**
- **Hypothesis**: Corner case not covered by directed tests
- **Action**: Analyze failing random test stimulus for common characteristics
- **Example**: Random test hits burst length=256, directed tests only ≤16

**Pattern: All tests with feature X fail, others pass**
- **Hypothesis**: Feature X has RTL bug
- **Action**: Focus debug on RTL module implementing feature X
- **Example**: All interrupt tests fail → debug interrupt controller

**Pattern: Intermittent failures with different seeds**
- **Hypothesis**: Race condition or initialization dependency
- *From Verification Evidence to RTL Root Cause

### Scoreboard-Driven Investigation

**Scoreboard reports data mismatch**:

```
Step 1: Identify transaction with mismatch
  Monitor: WRITE(addr=0x1000, data=0xDEADBEEF) @ 1000ns
  Scoreboard: Expected 0xDEADBEEF at 0x1000
  Monitor: READ(addr=0x1000) → 0xDEADBEE0 @ 1100ns
  Mismatch: LSB nibble changed 0xF → 0x0

Step 2: Hypothesize based on bit pattern
  - All bits except LSB nibble correct → byte masking issue
  - LSB nibble zeroed → possible width/alignment problem
  
Step 3: Check waveform at write cycle (1000ns)
  axi_wdata[31:0] = 0xDEADBEEF ✓
  write_strobe[3:0] = 4'b1111 ✓
  register_wdata[31:0] = 0xDEADBEE0 ✗ ← BUG IS HERE
  
Step 4: Trace write path
  axi_wdata → data_align_unit → register_wdata
  Check data_align_unit for LSB nibble handling
  
Step 5: Find root cause in RTL
  // Bug found in data_align_unit
  assign register_wdata = {axi_wdata[31:4], 4'b0000}; // ← Hardcoded zero!
```

### Assertion-Driven Investigation

**Assertion reports protocol violation**:

```
Assertion 'a_axi_wdata_stable' failed @ 1250ns
Property: (wvalid && !wready) |=> $stable(wdata)

Step 1: Understand assertion semantics
  - wdata must not change when wvalid=1 and wready=0
  - This is AXI4 protocol requirement
  
Step 2: Check waveform at violation timestamp
  @1249ns: wvalid=1, wready=0, wdata=0xAAAA
  @1250ns: wvalid=1, wready=0, wdata=0xBBBB ← Changed illegally
  
Step 3: Find source of wdata in RTL
  assign wdata = write_fifo_dout;
  
Step 4: Check FIFO read logic
  assign fifo_read_en = wvalid && wready; ✓ Correct condition
  
Step 5: Check for other paths affecting wdata
  // Found: Debug logic bypassing FIFO!
  assign wdata = debug_mode ? debug_data : write_fifo_dout;
  // debug_mode changed during backpressure → violation
```

### Test Suite Differential Analysis

**Multiple tests analysis**:

| Test Name | Scenario | Result | Common Attribute |
|-----------|----------|--------|------------------|
| basic_write | Single write | ✓ PASS | Burst length = 1 |
| burst4_write | 4-beat burst | ✓ PASS | Burst length = 4 |
| bDebugging Techniques from Test Results

### Regression Test Triage

**Analyze multiple test results to find common root cause**:

```
Regression suite: 42 tests total
- 38 PASS
- 4 FAIL: axiuart_burst16, axiuart_burst32, axiuart_wrap16, axiuart_wrap32

Pattern recognition:
- All failures involve burst length ≥ 16
- Both INCR and WRAP burst types affected
- Burst length ≤ 8 always passes

Common root cause hypothesis:
- Burst counter width insufficient for length ≥ 16
- Not specific to burst type (INCR vs WRAP)
- Not data-pattern dependent

Single fix expected to resolve all 4 failures.
```

### Minimal Reproducing Test

**Create simplest test that triggers bug**:

```systemverilog
// Original failing test: 200 lines, 10 minutes runtime
class axiuart_burst16_test extends base_test;
    // Complex randomization, multiple sequences, ...
endclass

// Minimal reproducer: 15 lines, 10 seconds runtime  
class minimal_burst16_test extends base_test;
    task run_phase(uvm_phase phase);
        axi_seq seq = axi_seq::type_id::create("seq");
        phase.raise_objection(this);
        
        // Single burst-16 transaction
        seq.addr = 32'h1000;
        seq.burst_length = 16;  // Minimal case that fails
        seq.start(env.agent.sequencer);
        
        phase.drop_objection(this);
    endtask
endclass

// Run: Still fails with same root cause
// Benefit: Faster debug iteration (10s vs 10min)
```

### Test Modification Experiments

**Systematically modify test to isolate variable**:
Debugging Pitfalls

### Don't Debug Without Test Evidence

❌ **Wrong**: "I think the problem is in module X, let me check the code"
✅ **Right**: "Test Y failed with scoreboard mismatch at time T, let me analyze the evidence"

### Don't Ignore Test Pass/Fail Patterns

❌ **Wrong**: Debug first failure in isolation, ignore other tests
✅ **Right**: Analyze which tests pass/fail to identify common characteristics

### Don't Trust Single Test Result

❌ **Wrong**: Test passed once → bug is fixed
✅ **Right**: Run regression suite (multiple seeds, scenarios) to confirm fix

### Don't Modify RTL Without Evidence

❌ **Wrong**: Change RTL based on intuition, hope test passes
✅ **Right**: Trace from test failure → scoreboard → monitor → waveform → RTL

### Don't Create Tests Without Purpose

❌ **Wrong**: Write random tests hoping to find bugs
✅ **Right**: Analyze coverage holes, create tests targeting untested scenarios

### Don't Skip Regression After Fix

❌ **Wrong**: Failing test now passes → Done
✅ **Right**: Run full regression to ensure fix doesn't break other tests
// Final conclusion: Pure burst length issue, check counter width
```

### Coverage-Guided Root Cause Analysis

**Use coverage to identify untested paths related to bug**:

```systemverilog
// Coverage report after test failures
covergroup cg_burst_length;
    cp_length: coverpoint burst_length {
        bins short[] = {[1:8]};     // 100% hit
        bins boundary = {15, 16};   // 16 causes failures
        bins long[] = {[17:256]};   // 0% hit ← Never tested!
    }
endgroup

// Analysis:
// - Tests never tried burst_length > 16
// - Bug might affect all values ≥ 16, not just 16
// - After fix, add test for burst_length=256 to verify
from Test Failures

### From Scoreboard Timestamp to Waveform

**Workflow**:

```
1. Test log shows scoreboard error at simulation time 1250ns
   UVM_ERROR: [SCOREBOARD] Data mismatch at addr=0x1000

2. Set waveform viewer to time 1250ns

3. Identify relevant signals from monitor transaction:
   - axi_awaddr (write address channel)
   - axi_wdata (write data channel)
   - Internal register_file signals
   
4. Check transaction timing:
   @1240ns: awvalid=1, awaddr=0x1000, awready=1 (address accepted)
   @1242ns: wvalid=1, wdata=0xBEEF, wready=1 (data accepted)
   @1250ns: register_file[0] = 0xBEE0 ← Should be 0xBEEF
   
5. Trace internal path:
   axi_wdata (0xBEEF) → write_data_reg (0xBEEF) → 
   data_align (0xBEE0) ← BUG HERE
```

### Backward Tracing from Assertion

**Assertion fires, trace backward to root cause**:

```
Assertion violation @ 1250ns:
  a_valid_stable: (valid && !ready) |=> $stable(data)

Waveform analysis:
  @1249ns: valid=1, ready=0, data=0xAAAA
  @1250ns: valid=1, ready=0, data=0xBBBB ← Violated $stable()

Trace data signal backward:
  data ← output_mux
  output_mux ← select between fifo_out and bypass_data
  mux_select changed at 1250ns ← WHY?

Trace mux_selefrom verification results is evidence-driven investigation:

1. **Analyze test failure patterns** - Which tests fail? What do they have in common?
2. **Collect verification evidence** - Scoreboard, assertions, monitors, logs
3. **Map evidence to RTL problem domain** - Translate test failure to RTL category
4. **Design targeted experiments** - Create minimal tests to isolate root cause
5. **Trace from verification to RTL** - Navigate from test → scoreboard → waveform → RTL
6. **Verify with test suite** - Confirm fix with regression, add prevention tests

Key principle: **Test results guide investigation**. Start from verification evidence (test failures, assertion violations, scoreboard mismatches), not RTL code reading
### By Affected Component

**Datapath issues**:
- Check operand widths, sign extension, overflow handling
- Verify bypass/forwarding conditions
- Trace data flow from source to destination

**Control logic issues**:
- Draw state transition diagram from code
- Verify all states are reachable
- Check for conflicting control signals

**Interface issues**:
- Review protocol timing diagrams
- Check handshake signal relationships (valid before ready, stable until accepted)
- Verify backpressure handling

## Hypothesis Generation Strategies

### Backwards Tracing

Start at the failure point and work backwards:

1. Identify the first wrong signal at failure timestamp
2. Find all signals that directly drive it (combinational or registered)
3. Check if those signals are correct one cycle earlier
4. Repeat until you find where correct values become incorrect

### Dependency Analysis

Map signal dependencies:

```
output_wrong [time=1250ns]
  ├─ driven by: alu_result (combinational)
  │    ├─ operand_a (registered at 1249ns) ✓ correct
  │    ├─ operand_b (registered at 1249ns) ✗ INCORRECT
  │    └─ operation (registered at 1249ns) ✓ correct
  └─ operand_b driven by: bypass_mux
       ├─ mem_result (registered at 1248ns) ✓ correct  
       ├─ ex_result (registered at 1249ns) ✗ INCORRECT
       └─ bypass_select ✗ WRONG MUX SELECT ← ROOT CAUSE
```

### Differential Diagnosis

Compare working vs failing cases:

| Aspect | Working Case | Failing Case | Insight |
|--------|-------------|--------------|---------|
| Input pattern | 0x00000001 | 0x80000000 | MSB triggers bug |
| Execution path | State A→B→C | State A→B→D | Transition B→D buggy |
| Timing | No stalls | Pipeline stall | Stall logic incorrect |

## Verification Techniques

### Assertion-Based Isolation

Insert temporary assertions to partition the design:

```systemverilog
// Check: Does problem occur before or after this pipeline stage?
property p_debug_stage2_input;
    @(posedge clk) stage2_valid |-> stage2_input inside {[0:1000]};
endproperty
assert property (p_debug_stage2_input) 
    else $error("Problem exists at stage2 input");
```

### Minimal Reproducer

Reduce test case to absolute minimum:

1. Start with failing test
2. Remove stimulus that doesn't affect failure
3. Shorten simulation time to just before failure
4. Remove unrelated RTL modules
5. Result: ~20 line testbench, ~50 line RTL

**Benefits**: Faster iteration, easier to share, clearer root cause

### Force/Release Experiments

Test hypotheses by overriding signals:

```systemverilog
// Hypothesis: Bug disappears if bypass is disabled
initial begin
    #100ns;
    force top.cpu.bypass_enable = 1'b0;
    // Observe if problem still occurs
end
```

**Caution**: Only for debugging, never in production code

### Coverage-Guided Debugging

Use coverage holes to identify untested scenarios:

```systemverilog
covergroup cg_state_transitions @(posedge clk);
    cp_current: coverpoint state;
    cp_next: coverpoint state_next;
    cross cp_current, cp_next;  // Are all transitions covered?
endgroup
```

**If bug occurs**: Check if failing scenario corresponds to coverage hole

## Common Pitfalls

### Don't Trust Assumptions

❌ **Wrong**: "Signal X is always stable, so I won't check it"
✅ **Right**: Add assertion to verify assumption, then proceed

### Don't Skip Symptom Observation

❌ **Wrong**: Jump straight to suspected module and start modifying
✅ **Right**: Observe exact failure in waveform, then form hypothesis

### Don't Fix Symptoms

❌ **Wrong**: Add logic to mask the symptom without understanding root cause
✅ **Right**: Trace to root cause, fix it, verify symptom disappears

### Don't Test Multiple Changes

❌ **Wrong**: Make 3 changes simultaneously, rerun simulation
✅ **Right**: Change one thing at a time, verify effect

## Waveform Analysis Patterns

### Cause → Effect Tracing

1. Find the symptom signal at failure timestamp
2. Look 1-2 cycles back for potential causes
3. Check if cause signals deviated from expected
4. Repeat backwards until finding the origin

### Critical Path Analysis

Identify longest combinational path:

```systemverilog
// Use $time in always_comb to detect long paths
always_comb begin
    logic [31:0] temp1, temp2, temp3;
    temp1 = input_a & input_b;      // 1 gate delay
    temp2 = temp1 | input_c;        // 1 gate delay  
    temp3 = temp2 ^ input_d;        // 1 gate delay
    output_z = temp3 + input_e;     // 1 gate delay
    // Total: 4 gate delays - may violate timing
end
```

### Clock Domain Crossing Detection

Look for signals crossing without proper synchronization:

```
Clock A domain: signal_a toggles at time 1250ns
Clock B domain: signal_b samples signal_a at 1251ns
                ↑ METASTABILITY RISK if clocks unrelated
```

## Integration with Other Skills

- **dsim-debugging**: Use when DSIM tool itself has issues (environment, waves, logs)
- **rtl-coding-standards**: Apply when fixing identified bugs to maintain code quality
- **assertion-design**: Create permanent assertions for bugs found during debugging
- **mcp-workflow**: Use MCP commands to compile/run debug experiments quickly

## Summary

RTL debugging is systematic reasoning:

1. **Reproduce** the problem reliably
2. **Observe** symptoms without assumptions  
3. **Generate** hypotheses based on evidence
4. **Test** each hypothesis independently
5. **Narrow** down to single root cause
6. **Verify** fix and prevent regression

Key principle: **Evidence over intuition**. Always trace from observed symptoms to root cause using waveforms and assertions.
