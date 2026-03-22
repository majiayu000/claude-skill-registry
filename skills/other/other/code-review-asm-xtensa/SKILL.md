---
name: code-review-asm-xtensa
description: Review Xtensa assembly code for ESP32 platforms. Checks for critical errors in inline assembly, ABI compliance, and optimization opportunities. Use after modifying ESP32 assembly or inline asm code.
disable-model-invocation: true
context: fork
agent: code_review_asm_xtensa-agent
---

Perform comprehensive manual review of Xtensa assembly code in FastLED ESP32 platforms for correctness, ABI compliance, safety, and performance.

## What Gets Checked

### Critical Errors (Must Fix)
- **E001**: Invalid `movi` for 32-bit addresses
- **E002**: Wrong return instruction in interrupts
- **E003**: Missing `memw` memory barriers for MMIO writes
- **E004**: Windowed ABI used in interrupt handlers
- **E005**: Unaligned memory access
- **E006**: Missing `IRAM_ATTR` on interrupt handlers
- **E007**: Mixed ABI usage in same function

### Performance Warnings
- **W001-W005**: Load-use hazards, loop overhead, nesting depth, register pressure, dependency chains

### Optimization Opportunities
- **O001-O004**: Array indexing, conditional moves, loop unrolling, code density

Search for Xtensa assembly code in git changes (inline asm and .S files) and perform deep analysis.
