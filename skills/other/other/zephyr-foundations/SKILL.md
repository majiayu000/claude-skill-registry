---
name: zephyr-foundations
description: Foundational skills for Zephyr RTOS development. Covers essential Embedded C patterns (BIT, CONTAINER_OF), real-time concurrency primitives (mutexes, semaphores, spinlocks), hardware literacy (datasheet-to-DTS mapping), and defensive programming. Trigger when writing core application logic, drivers, or troubleshooting foundational behavior.
---

# Zephyr Foundations

Mastering the bedrock of Zephyr is essential for writing efficient, robust, and idiomatic code.

## Core Workflows

### 1. Idiomatic C Patterns
Zephyr uses specific macros to manage memory and hardware-software mapping.
- **Reference**: **[zephyr_macros.md](references/zephyr_macros.md)**
- **Key Tools**: `CONTAINER_OF`, `BIT()`, `GENMASK()`, `ARRAY_SIZE`.

### 2. Real-Time Concurrency
Safe multi-threading and interrupt handling are critical for stability.
- **Reference**: **[concurrency.md](references/concurrency.md)**
- **Key Tools**: `k_mutex`, `k_sem`, `k_spinlock`, `atomic_t`, ISR safety rules.

### 3. Hardware Literacy (Devicetree)
Understanding how code interacts with the hardware description.
- **Reference**: **[devicetree_basics.md](references/devicetree_basics.md)**
- **Key Tools**: Nodes, properties, phandles, overlays, and advanced deletion.

### 4. Robust Error Handling
Preventing crashes through defensive programming.
- **Reference**: **[error_handling.md](references/error_handling.md)**
- **Key Tools**: `errno.h`, `BUILD_ASSERT`, validation patterns, return code checking.

## Examples & Templates

- **[template_driver.c](assets/foundation_examples/template_driver.c)**: A complete skeleton showing how to combine DT macros, mutexes, and config-data separation.

## Resources

- **[References](references/)**:
  - `zephyr_macros.md`: Essential macros (BIT, CONTAINER_OF, etc.).
  - `concurrency.md`: Mutexes, Semaphores, Spinlocks, and ISR safety.
  - `devicetree_basics.md`: Devicetree syntax and overlay patterns.
  - `error_handling.md`: Error codes and defensive programming.
- **[Assets](assets/)**:
  - `foundation_examples/`: Working code templates for drivers and logic.
