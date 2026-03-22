---
name: memory-audit
description: Audit embedded code for stack overflow risks, heap fragmentation, static allocation patterns, and memory leaks. Use when investigating OOM crashes, optimizing memory usage, or reviewing memory-critical code on constrained devices.
argument-hint: <file, directory, or component to audit>
context: fork
agent: memory-audit-agent
---

Audit code for memory safety issues specific to resource-constrained embedded systems.

$ARGUMENTS

## What This Skill Analyzes

### Stack Usage
- Functions with large local arrays or structs (risk of stack overflow)
- Deep call chains and recursion (stack depth estimation)
- Task/thread stack size adequacy (FreeRTOS `xTaskCreate` stack parameter)
- Alloca/VLA usage (variable-length arrays on stack)

### Heap Fragmentation
- Frequent small allocations and deallocations in hot paths
- Mixed allocation sizes causing fragmentation over time
- Missing deallocation (memory leaks)
- Allocation in ISRs or time-critical code (heap locks can cause priority inversion)

### Static Allocation Patterns
- Global/static buffer sizing (too large wastes RAM, too small causes overflow)
- Compile-time vs runtime allocation trade-offs
- `.bss` and `.data` section usage
- PSRAM vs internal SRAM placement decisions

### Platform-Specific Concerns
- ESP32: DRAM/IRAM split, PSRAM cache line alignment, DMA-capable memory
- ARM Cortex-M: Stack/heap collision, MPU configuration, scatter file layout
- AVR: 2KB SRAM constraint, PROGMEM usage for constants

## How To Use

```
/memory-audit src/platforms/esp/32/drivers/
/memory-audit src/fl/channels/
/memory-audit Check if LED buffer allocation is safe for 1000+ LEDs on ESP32
```

## What You'll Get

- Memory usage breakdown by category (stack, heap, static)
- Risk assessment for each finding (Critical/High/Medium/Low)
- Specific recommendations with code examples
- Platform-aware advice (e.g., "move to PSRAM" vs "reduce buffer size")
