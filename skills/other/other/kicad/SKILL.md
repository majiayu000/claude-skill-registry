---
name: kicad
description: |
  Designs PCB schematics and circuit layouts for hardware projects.
  Use when: Creating or modifying KiCad schematic files (.kicad_sch), PCB layouts, symbol libraries, or footprint libraries for the VanDaemon hardware projects.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# KiCad Skill

Designs PCB schematics and layouts for VanDaemon hardware projects, primarily the ESP32-based 8-channel LED dimmer. KiCad 7+ uses S-expression format for all files. The project follows automotive-grade design practices for reliability in vehicle environments.

## Quick Start

### Find Hardware Project Files

```bash
# Locate KiCad project files
find hw/LEDDimmer -name "*.kicad_*" -type f

# Current project structure
hw/LEDDimmer/
├── led_dimmer_8ch.kicad_sch    # Main schematic
├── led_dimmer_8ch.kicad_pcb    # PCB layout (when created)
└── led_dimmer_8ch.kicad_pro    # Project settings
```

### Read Schematic Structure

```bash
# View schematic header and metadata
head -50 hw/LEDDimmer/led_dimmer_8ch.kicad_sch

# Find all component references
grep -E "^\s+\(property \"Reference\"" hw/LEDDimmer/led_dimmer_8ch.kicad_sch
```

## Key Concepts

| Concept | Format | Example |
|---------|--------|---------|
| Comments | `#` prefix only | `# Power section` |
| Component reference | `(property "Reference" "R1")` | Resistor R1 |
| Pin connection | `(wire (pts ...))` | Net connection |
| Symbol instance | `(symbol (lib_id "...")` | Component placement |
| Net label | `(label "VCC" ...)` | Named net |

## WARNING: Comment Syntax

**KiCad does NOT support semicolon comments.** Use `#` for comments in KiCad files.

```kicad
# GOOD - Hash comments work
# Power regulation section

; BAD - Semicolons are NOT comments, they become part of the data
```

## Common Patterns

### Adding a Component

```kicad
(symbol (lib_id "Device:R")
  (at 100 50 0)
  (unit 1)
  (property "Reference" "R1" (at 100 45 0))
  (property "Value" "10k" (at 100 55 0))
  (property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 100 50 0))
)
```

### Creating a Net Connection

```kicad
(wire (pts (xy 100 50) (xy 120 50)))
(label "PWM_CH0" (at 110 50 0))
```

## Design Guidelines

| Parameter | Requirement | Reason |
|-----------|-------------|--------|
| Trace width (power) | ≥0.5mm | Handle 2A per channel |
| Trace width (signal) | ≥0.25mm | Manufacturing tolerance |
| Via size | 0.8mm/0.4mm | Thermal dissipation |
| Clearance | ≥0.2mm | Automotive reliability |
| Copper weight | 2oz | Current handling |

## See Also

- [patterns](references/patterns.md) - Schematic and PCB patterns
- [workflows](references/workflows.md) - Design and export workflows

## Related Skills

- **platformio** skill - Firmware for ESP32 hardware
- **docker** skill - Build automation for production