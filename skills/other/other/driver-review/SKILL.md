---
name: driver-review
description: Review hardware driver code for DMA safety, interrupt correctness, timing constraints, and peripheral register usage. Use when writing or modifying LED drivers, SPI/I2S/RMT/UART peripherals, or GPIO configuration code.
disable-model-invocation: true
---

# Hardware Driver Code Review

Review hardware driver code changes for embedded-specific safety and correctness issues that generic code review misses.

## Your Task

1. Run `git diff --cached` and `git diff` to see all changes
2. Identify files that are hardware driver code (see "What Counts as Driver Code" below)
3. Review ALL driver code changes against the rules below
4. Fix straightforward violations directly
5. Report summary of all findings

## What Counts as Driver Code

Files matching these patterns:
- `src/platforms/**` — Platform-specific implementations
- `src/fl/channels/**` — LED channel engine and DMA pipeline
- `**/drivers/**` — Hardware driver implementations
- Files containing: DMA buffers, SPI/I2S/RMT/UART/PARLIO peripheral access, GPIO configuration, interrupt handlers, timer configuration

## Review Rules

### 1. DMA Safety
- [ ] DMA buffers allocated with `MALLOC_CAP_INTERNAL | MALLOC_CAP_DMA`
- [ ] DMA buffers are 4-byte aligned (use `__attribute__((aligned(4)))` or aligned allocator)
- [ ] No stack-allocated DMA buffers (must be heap or static)
- [ ] DMA descriptors in internal SRAM (not PSRAM/SPIRAM)
- [ ] Cache coherence handled: `esp_cache_msync()` or non-cacheable memory for DMA
- [ ] DMA transfer size within hardware limits
- [ ] Buffer lifetime extends beyond DMA completion (no use-after-free)

### 2. Interrupt Safety
- [ ] ISR functions marked with `IRAM_ATTR` (ESP32) or proper section attributes
- [ ] No heap allocation (`malloc`, `new`, `fl::vector`) inside ISRs
- [ ] No mutex/semaphore take with blocking timeout in ISRs (use `portMAX_DELAY` = 0 only)
- [ ] No `printf`, `FL_DBG`, `FL_WARN`, or logging in ISRs
- [ ] No flash access from ISRs (all ISR code and data in IRAM/DRAM)
- [ ] ISR-safe queue operations only (`xQueueSendFromISR`, not `xQueueSend`)
- [ ] Critical sections use proper primitives (`portENTER_CRITICAL_ISR` not `portENTER_CRITICAL`)
- [ ] ISR handlers return correct value (`true` if higher-priority task woken)

### 3. Peripheral Register Access
- [ ] Registers accessed through volatile pointers or HAL functions
- [ ] No read-modify-write races on shared registers (use atomic or critical section)
- [ ] Peripheral clock enabled before register access
- [ ] Peripheral properly initialized before use and cleaned up on teardown
- [ ] GPIO matrix/IOMUX configured correctly for peripheral signals

### 4. Timing Constraints
- [ ] SPI/I2S/RMT clock calculations match LED protocol requirements
- [ ] Reset timing meets protocol minimums (WS2812: >280us, SK6812: >80us)
- [ ] No blocking waits in time-critical paths
- [ ] Watchdog fed in long-running operations
- [ ] `vTaskDelay(1)` or `yield()` in busy loops to prevent watchdog reset

### 5. Memory Safety
- [ ] Buffer sizes checked before DMA transfer setup
- [ ] No buffer overflows in encoding functions (bounds checking on output buffer)
- [ ] Encoding output size calculated correctly (e.g., wave8: 8 SPI bits per LED bit)
- [ ] Chunk sizes aligned to hardware requirements (SPI: 4-byte aligned)

### 6. Channel Engine Patterns (FastLED-specific)
- [ ] `show()` waits for `poll() == READY` before starting new frame
- [ ] No branching on intermediate states (DRAINING, STREAMING) in wait loops
- [ ] Channel released after transmission complete (frees peripheral for next channel)
- [ ] State machine handles all transitions (no stuck states)
- [ ] Error recovery path exists (timeout, reset to IDLE)

### 7. Power and Reset
- [ ] Brown-out detection configured if needed
- [ ] Peripheral reset on initialization (clean state)
- [ ] GPIO pins set to safe state on driver teardown
- [ ] Power domains managed correctly (light sleep compatibility)

### 8. Multi-Platform Considerations
- [ ] Platform guards (`#ifdef ESP32`, `#ifdef FL_IS_ARM`) correct and complete
- [ ] No platform-specific types leaking into shared headers
- [ ] Fallback/no-op implementations for unsupported platforms
- [ ] Integer types match platform expectations (see `src/platforms/*/int.h`)

## Output Format

```
## Hardware Driver Review Results

### File-by-file Analysis
- **src/platforms/esp/32/drivers/spi/channel_engine_spi.cpp.hpp**: [findings]
- **src/fl/channels/channel_engine.h**: [findings]

### Findings by Category
- **DMA Safety**: N issues
- **Interrupt Safety**: N issues
- **Timing Constraints**: N issues
- **Memory Safety**: N issues
- **Channel Engine Patterns**: N issues

### Summary
- Files reviewed: N
- Violations found: N
- Violations fixed: N
- User confirmations needed: N
```

## Instructions
- Focus on driver/platform code — skip application-level changes
- Be thorough on DMA and interrupt safety (these cause hard-to-debug crashes)
- Reference `agents/docs/cpp-standards.md` for general C++ rules
- Make corrections directly when safe
- Ask for user confirmation on significant changes
