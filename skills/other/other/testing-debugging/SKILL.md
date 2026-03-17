---
name: testing-debugging
description: Testing and debugging for Zephyr RTOS. Covers the Ztest framework for unit and integration tests, the Twister test runner for automated HIL/SIM validation, and advanced tracing/debugging techniques (SystemView, Thread Analyzer, Stack analysis). Trigger when writing unit tests, setting up CI/CD pipelines, or analyzing system performance and latency.
---

# Zephyr Testing & Debugging

Ensure code quality and system reliability using Zephyr's comprehensive testing framework and observability tools.

## Core Workflows

### 1. Ztest Framework
Write robust unit and integration tests for native simulation and real hardware.
- **Reference**: **[ztest_framework.md](references/ztest_framework.md)**
- **Key Tools**: `ZTEST_SUITE`, `ZTEST`, `zassert_equal`.

### 2. Twister Test Runner
Automate test execution across multiple platforms and generate professional reports.
- **Reference**: **[twister_testing.md](references/twister_testing.md)**
- **Key Tools**: `twister` script, `testcase.yaml`, hardware mapping.

### 3. Tracing & Debugging
Analyze system behavior, timing, and memory usage with advanced tracing tools.
- **Reference**: **[tracing_debugging.md](references/tracing_debugging.md)**
- **Key Tools**: `CONFIG_TRACING`, Segger SystemView, Thread Analyzer.

## Quick Start (Ztest)
```c
#include <zephyr/ztest.h>

ZTEST_SUITE(basic_test, NULL, NULL, NULL, NULL, NULL);

ZTEST(basic_test, test_pass) {
    zassert_true(true, "Boolean evaluation failed");
}
```

## Professional Patterns (Reliability)
- **Continuous Integration**: Integrate Twister reports (`twister.json`) into CI/CD pipelines for automated regression testing.
- **HIL Validation**: Use hardware maps to consistently run critical hardware tests on real devices during every release cycle.
- **Stack Safety**: Always enable `CONFIG_STACK_SENTINEL` and the Thread Analyzer during development to catch memory issues early.

## Resources

- **[References](references/)**:
  - `ztest_framework.md`: Writing tests with expectations and suites.
  - `twister_testing.md`: Using the test runner and metadata.
  - `tracing_debugging.md`: Tracing, stack analysis, and debugging backends.
