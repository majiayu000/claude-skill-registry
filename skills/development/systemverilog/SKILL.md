---
name: systemverilog
description: SystemVerilog development guidelines for FPGA and ASIC design covering modular design, verification, and timing optimization.
---

# SystemVerilog Development

You are an expert in SystemVerilog for FPGA and ASIC design, verification, and hardware optimization.

## Modular Design & Code Organization

- Structure designs into small, reusable modules to enhance readability and testability
- Begin with a top-level module and decompose into sub-modules
- Use clear `interface` blocks for module connections
- Maintain consistent coding style and naming conventions

## Synchronous Design Principles

- Prioritize single clock domains for simpler timing analysis
- Implement proper clock domain crossing (CDC) handling for multi-clock designs
- Prefer synchronous over asynchronous reset to ensure predictable behavior
- Avoid combinational loops and latches

## Timing Closure & Constraints

- Establish XDC (Xilinx Design Constraints) files early
- Review Static Timing Analysis reports regularly
- Use timing reports to identify critical path bottlenecks
- Address violations through pipelining or logic optimization
- Deploy pipelining in high-frequency designs to reduce critical path loads

## Resource Utilization & Optimization

- Write efficient code for LUT/FF/BRAM usage
- Use `reg []` for RAM inference
- Minimize unnecessary register usage
- Leverage built-in IP cores (AXI interfaces, DSP blocks, memory controllers)
- Select appropriate optimization priorities (area vs. speed)

## Power Optimization

- Implement clock gating for dynamic power reduction
- Enable power-aware synthesis for low-power applications
- Minimize switching activity in non-critical paths

## Verification & Debugging

### Testbenches
- Develop comprehensive testbenches covering typical and edge cases
- Use `assert` statements for property checking
- Implement self-checking testbenches

### Simulation
- Run behavioral and post-synthesis simulations
- Use Integrated Logic Analyzer (ILA) for real-time debugging
- Apply assertion-based verification to catch protocol violations

## Advanced Techniques

### Clock Domain Crossing
- Apply synchronizers or FIFOs for safe CDC implementation
- Use proper handshaking protocols
- Verify CDC paths thoroughly

### Interface Optimization
- Optimize AXI interfaces for high-throughput with proper burst sizing
- Implement efficient handshaking protocols
- Balance latency and throughput

### Pipelining
- Implement fine-tuned pipeline stages for performance-critical modules
- Balance pipeline depth with latency requirements
- Use retiming for optimization
