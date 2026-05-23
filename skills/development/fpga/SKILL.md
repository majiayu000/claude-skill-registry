---
name: fpga
description: FPGA development guidelines covering Vivado, SystemVerilog, timing closure, AXI interfaces, and hardware optimization.
---

# FPGA Development

You are an expert in FPGA development with Vivado, SystemVerilog, and hardware design optimization.

## Modular Design & Code Organization

- Structure designs into small, reusable modules to enhance readability and testability
- Start with a top-level design module and gradually break it down into sub-modules
- Use SystemVerilog interface blocks for clear interfaces
- Maintain consistent naming conventions across modules

## Synchronous Design Principles

- Prioritize single clock domains to simplify timing analysis
- Favor synchronous reset over asynchronous reset to ensure predictable behavior
- Avoid timing hazards during synthesis
- Use proper clock domain crossing (CDC) techniques when multiple clocks are required

## Timing Closure & Constraints

- Establish timing constraints early using XDC files
- Review Static Timing Analysis reports regularly
- Identify critical timing paths using Vivado's timing reports
- Address violations by adding pipeline stages or optimizing logic
- Use multi-cycle path constraints where appropriate

## Resource Utilization & Optimization

- Optimize LUTs, flip-flops, and block RAM through efficient SystemVerilog
- Leverage Vivado's built-in IP cores (AXI interfaces, DSP blocks, memory controllers)
- Select appropriate synthesis strategies based on design priorities
- Use `reg []` for RAM inference and minimize register usage
- Balance area vs. speed optimization based on requirements

## Power Optimization

- Implement clock gating to reduce dynamic power consumption
- Use Vivado's power-aware synthesis
- Set power constraints for low-power applications
- Minimize switching activity in non-critical paths

## Debugging & Simulation

- Write detailed, self-checking testbenches covering typical use cases and edge cases
- Use SystemVerilog assertions for verification
- Run behavioral and post-synthesis simulations
- Use Integrated Logic Analyzer (ILA) for real-time signal debugging
- Implement assertion-based verification to catch protocol violations

## Advanced Techniques

### Clock Domain Crossing
- Use synchronizers or FIFOs to handle CDC safely
- Implement proper handshaking protocols

### AXI Protocol Compliance
- Ensure proper read/write channel management and handshakes
- Optimize for high-throughput with proper burst sizing

### DMA Integration
- Configure burst transfers for maximum throughput
- Handle buffer management efficiently

### Latency Reduction
- Implement fine-tuned pipeline stages strategically
- Balance latency vs. throughput requirements
