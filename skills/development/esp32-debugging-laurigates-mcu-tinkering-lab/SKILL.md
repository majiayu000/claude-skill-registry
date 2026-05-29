---
name: esp32-debugging
description: Debug ESP32 firmware issues including compilation errors, runtime panics, memory issues, and communication failures
---

# ESP32 Firmware Debugging Guide

## When to Use This Skill

Apply this skill when the user:
- Encounters compilation errors in ESP-IDF projects
- Sees runtime panics or "Guru Meditation Error" messages
- Has memory-related crashes or stack overflows
- Experiences I2C/SPI/UART communication failures
- Needs help interpreting serial monitor output

## Debugging Techniques

### 1. Compilation Error Analysis

**Missing Includes**
```
fatal error: driver/gpio.h: No such file or directory
```
Fix: Check CMakeLists.txt and add the component to REQUIRES:
```cmake
idf_component_register(
    SRCS "main.c"
    REQUIRES driver
)
```

**Undefined References**
```
undefined reference to 'some_function'
```
Fix: Ensure the component containing the function is in REQUIRES or PRIV_REQUIRES.

**Type Errors**
Look for mismatched types between function declarations and implementations.

### 2. Runtime Panic Analysis

**Guru Meditation Error Patterns**

| Error | Cause | Fix |
|-------|-------|-----|
| `StoreProhibited` | Writing to invalid memory | Check pointer initialization |
| `LoadProhibited` | Reading from invalid memory | Check null pointers |
| `InstrFetchProhibited` | Corrupted function pointer | Check callback assignments |
| `IntegerDivideByZero` | Division by zero | Add zero checks |

**Stack Overflow**
```
Guru Meditation Error: Core 0 panic'ed (Stack overflow)
```
Fix: Increase stack size in task creation:
```c
xTaskCreatePinnedToCore(task_fn, "name", 4096, NULL, 5, NULL, 0);
//                                        ^^^^ increase this
```

**Stack Smashing**
```
Stack smashing detected
```
Fix: Local buffer overflow - check array bounds and string operations.

### 3. Memory Debugging

**Check Heap Usage**
```c
ESP_LOGI(TAG, "Free heap: %lu", esp_get_free_heap_size());
ESP_LOGI(TAG, "Min free heap: %lu", esp_get_minimum_free_heap_size());
```

**Common Memory Issues**
- Memory leak: Missing `free()` after `malloc()`
- Double free: Freeing same memory twice
- Use after free: Accessing freed memory

### 4. Communication Debugging

**I2C Issues**
```
E (1234) i2c: i2c_master_cmd_begin(xxx): I2C_NUM error
```
Checklist:
- Verify I2C address (7-bit vs 8-bit format)
- Check SDA/SCL GPIO pins
- Ensure pull-up resistors are present (4.7K typical)
- Verify clock frequency compatibility

**Serial/UART Issues**
- Baud rate mismatch
- TX/RX swapped
- Missing ground connection

### 5. Build Commands for Debugging

```bash
# Clean build to eliminate stale objects
make robocar-clean && make robocar-build-main

# Build with verbose output
cd packages/esp32-projects/robocar-main && idf.py build -v

# Start serial monitor
make robocar-monitor-main PORT=/dev/cu.usbserial-0001
```

### 6. Useful ESP-IDF Config Options

Enable in `sdkconfig` or via `idf.py menuconfig`:
- `CONFIG_ESP_SYSTEM_PANIC_PRINT_REBOOT` - Print panic info before reboot
- `CONFIG_FREERTOS_WATCHPOINT_END_OF_STACK` - Detect stack overflow earlier
- `CONFIG_HEAP_POISONING_COMPREHENSIVE` - Detect heap corruption

## Examples

### Example: Debugging a Stack Overflow

User reports: "My ESP32 keeps crashing on startup"

1. Ask for serial monitor output
2. Look for "Stack overflow" in panic message
3. Identify which task is overflowing
4. Suggest increasing stack size from 2048 to 4096
5. Explain FreeRTOS stack sizing considerations

### Example: I2C Communication Failure

User reports: "I2C device not responding"

1. Verify address with I2C scanner
2. Check GPIO configuration
3. Verify pull-up resistors
4. Check bus speed compatibility
5. Suggest adding delays between transactions if needed
