---
name: devicetree
description: Devicetree management for Zephyr RTOS. Covers syntax, bindings, overlays, Hardware Model v2 (HWMv2), and advanced node/property deletion patterns. Trigger when defining hardware topology, creating overlays, or mapping pins and peripherals.
---

# Zephyr Devicetree

The Devicetree (DT) is the source of truth for your hardware topology in Zephyr.

## Core Workflows

### 1. Understanding Syntax & Nodes
Nodes, properties, and phandles form the hierarchy.
- **Reference**: **[dt_syntax.md](references/dt_syntax.md)**
- **Key Tools**: Labels (`&label`), Properties (`reg`, `status`, `compatible`).

### 2. Working with Bindings
Mapping hardware descriptions to driver schemas.
- **Reference**: **[dt_bindings.md](references/dt_bindings.md)**
- **Key Tools**: YAML bindings, compatible strings, `pinctrl`.

### 3. Application Overlays & HWMv2
Modifying board behavior for specific application needs.
- **Reference**: **[dt_overlays.md](references/dt_overlays.md)**
- **Key Tools**: `.overlay` files, `zephyr,chosen`, variant-specific overlays.

### 4. Advanced Hardware Modification
Deleting and redefining nodes/properties for product variants.
- **Reference**: **[dt_overlays.md](references/dt_overlays.md#advanced-customization-from-golioth)**
- **Key Tools**: `/delete-node/`, `/delete-property/`.

## Quick Start (Overlay)
```dts
/* app.overlay */
&i2c1 {
  status = "okay";
};

&uart0 {
  status = "disabled";
};
```

## Tooling & Validation

- `west build -t rom_report`: See how devicetree definitions impact memory.
- `build/zephyr/zephyr.dts`: Inspect the FINAL resolved devicetree after all overlays are applied.
- `build/zephyr/include/generated/zephyr/devicetree_generated.h`: Inspect generated DT macros consumed by C code.

## Automation Tools
- **[overlay_include_check.py](scripts/overlay_include_check.py)**: Run basic sanity checks on `.overlay` files.

## Examples & Templates
- **[app_overlay_template.overlay](assets/app_overlay_template.overlay)**: Starter overlay with common node status changes.

## Validation Checklist
- [ ] Overlay compiles with no DTS syntax errors during `west build`.
- [ ] Expected node status/properties are present in `build/zephyr/zephyr.dts`.
- [ ] Expected DT macros exist in `build/zephyr/include/generated/zephyr/devicetree_generated.h`.
- [ ] Application runs with peripherals enabled/disabled exactly as described by the overlay.

## Resources

- **[References](references/)**:
  - `dt_syntax.md`: Core syntax and properties.
  - `dt_bindings.md`: Binding definitions and compatible mapping.
  - `dt_overlays.md`: Overlays, HWMv2, and deletion patterns.
- **[Scripts](scripts/)**:
  - `overlay_include_check.py`: Overlay sanity checker.
- **[Assets](assets/)**:
  - `app_overlay_template.overlay`: Baseline overlay template.
