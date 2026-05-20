---
name: connectivity-usb-can
description: USB and CAN connectivity for Zephyr RTOS. Covers USB device stack configuration (CDC ACM, HID, MSC), CAN controller integration, and professional USB-to-CAN adapter patterns including buffering and protocol packetization. Trigger when adding USB interfaces, implementing CAN bus communication, or building hardware diagnostic tools.
---

# Zephyr Connectivity: USB & CAN

Build versatile hardware interfaces using Zephyr's modular USB device stack and robust CAN controller support.

## Core Workflows

### 1. USB Device Stack
Configure and enable standard USB classes for host communication.
- **Reference**: **[usb_device_stack.md](references/usb_device_stack.md)**
- **Key Tools**: `CONFIG_USB_DEVICE_STACK`, `usb_enable()`, CDC ACM, HID.

### 2. USB-to-CAN Integration
Implement high-performance bridge patterns for CAN bus diagnostics and adapters.
- **Reference**: **[usb_to_can.md](references/usb_to_can.md)**
- **Key Tools**: `can_send()`, `k_msgq`, binary packetization, CAN filtering.

## Quick Start (USB CDC ACM)
```kconfig
# prj.conf
CONFIG_USB_DEVICE_STACK=y
CONFIG_USB_CDC_ACM=y
```
```c
#include <zephyr/usb/usb_device.h>

void main(void) {
    usb_enable(NULL);
}
```

## Professional Patterns (Adapter Design)
- **Binary Protocols**: Use established protocols like `gs_usb` for robust data transfer over the USB-to-CAN bridge.
- **Hardware Filtering**: Rely on the CAN controller's hardware filters to minimize CPU overhead from irrelevant bus traffic.
- **Thread Safety**: Use Zephyr's kernel IPCs (`k_msgq`, `k_fifo`) to safely move data between high-priority CAN interrupts and the USB processing thread.

## Automation Tools
- **[can_filter_lint.py](scripts/can_filter_lint.py)**: Validate CAN filter ID/mask tables from CSV.

## Examples & Templates
- **[can_filters_template.csv](assets/can_filters_template.csv)**: Starter CAN filter table for adapter firmware.

## Validation Checklist
- [ ] USB enumeration succeeds and the host sees the expected class interface.
- [ ] CAN frames can be transmitted and received on a known-good test bus.
- [ ] Bridge buffering prevents frame loss under burst traffic conditions.
- [ ] Protocol framing between USB endpoint and CAN payload is decoded consistently on both sides.

## Resources

- **[References](references/)**:
  - `usb_device_stack.md`: Configuring USB classes and descriptors.
  - `usb_to_can.md`: Adapter patterns and buffering strategies.
- **[Scripts](scripts/)**:
  - `can_filter_lint.py`: CAN filter table consistency checker.
- **[Assets](assets/)**:
  - `can_filters_template.csv`: Sample filter definitions.
