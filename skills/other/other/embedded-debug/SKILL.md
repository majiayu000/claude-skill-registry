---
name: embedded-debug
description: Firmware crash analysis, stack trace decoder, and register dump interpreter for ESP32/ARM/AVR platforms. Use when debugging device crashes, panics, guru meditation errors, hard faults, or analyzing core dumps.
argument-hint: <crash output or description of the issue>
context: fork
agent: embedded-debug-agent
---

Analyze firmware crash output, decode stack traces, and diagnose embedded system failures.

$ARGUMENTS

## What This Skill Does

1. **Crash Analysis**: Parse panic handlers, guru meditation errors, hard faults, watchdog resets
2. **Stack Trace Decoding**: Decode raw addresses to function names using ELF binaries
3. **Register Dump Interpretation**: Analyze CPU register state at crash time
4. **Root Cause Identification**: Correlate crash data with source code to find the bug
5. **Fix Recommendations**: Suggest specific code changes to prevent the crash

## Supported Platforms

| Platform | Crash Types |
|----------|-------------|
| ESP32 (all variants) | Guru Meditation, LoadProhibited, StoreProhibited, InstrFetchProhibited, watchdog reset, brownout, cache errors |
| ARM Cortex-M (STM32, Teensy, nRF) | HardFault, MemManage, BusFault, UsageFault, watchdog reset |
| AVR (Arduino Uno/Mega) | Stack overflow (silent corruption), watchdog reset, undefined opcode |
| RISC-V (ESP32-C3/C6/H2) | Illegal instruction, load/store fault, breakpoint |

## How To Use

### With crash output
```
/embedded-debug
Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.
Core 0 register dump:
PC      : 0x400d1234  PS      : 0x00060030  A0      : 0x800d5678
...
```

### With a description
```
/embedded-debug Device reboots every 30 seconds, serial shows "rst:0x3 (SW_RESET)"
```

### With a core dump
```
/embedded-debug Analyze the core dump from the last crash
```

## What You'll Get

- Decoded stack trace with source file and line numbers
- Explanation of the crash type and what triggered it
- Identification of the faulty code path
- Specific fix recommendations with code examples
- Prevention strategies (stack size tuning, watchdog config, null checks)
