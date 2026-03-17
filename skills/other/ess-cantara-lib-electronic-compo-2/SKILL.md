# Cypress Manufacturer Handler Skill

## Overview
CypressHandler manages Cypress Semiconductor components including PSoC MCUs, memory, USB controllers, and wireless chips.

**Note**: Cypress was acquired by Infineon in 2020. Some products may transition to Infineon branding.

## Supported Component Types
- MICROCONTROLLER, MICROCONTROLLER_CYPRESS, MCU_CYPRESS
- MEMORY, MEMORY_CYPRESS
- PSOC_MCU, FM_SERIES_MCU, TRAVEO_MCU

## MPN Patterns

### PSoC MCUs
| Prefix | Description |
|--------|-------------|
| CY8C4xxx | PSoC 4 (ARM Cortex-M0) |
| CY8C5xxx | PSoC 5 (ARM Cortex-M3) |
| CY8C6xxx | PSoC 6 (ARM Cortex-M4/M0+) |

### Memory Products
| Prefix | Description |
|--------|-------------|
| CY14Bxxx | nvSRAM (non-volatile SRAM) |
| CY62xxx | Static RAM |

### USB Controllers
| Prefix | Description |
|--------|-------------|
| CY7Cxxx | USB 2.0 controllers |
| CYUSBxxx | USB 3.0 controllers |

### Wireless/Bluetooth
| Prefix | Description |
|--------|-------------|
| CYWxxx | Wireless combo chips (WiFi+BT) |
| CYBLxxx | Bluetooth Low Energy |

### Touch Sensing
| Prefix | Description |
|--------|-------------|
| CY8CMBRxxx | CapSense controllers |
| CY8CTECHxxx | TrueTouch controllers |

### Power Management
| Prefix | Description |
|--------|-------------|
| CCGx | USB-C controllers |
| CYPDxxx | USB-PD controllers |

## Package Code Extraction

### PSoC Package Suffixes
- LP = LQFP
- TM = TQFP
- BX = BGA
- QF = QFN

### Memory Packages
Extracted from suffix after last dash (e.g., CY14B101LA-SXI → SXI)

## Series Extraction
Returns series names:
- "PSoC 4", "PSoC 5", "PSoC 6", "PSoC"
- "nvSRAM", "SRAM"
- "USB Controller", "USB 3.0 Controller"
- "Wireless Combo", "Bluetooth LE"
- "CapSense", "TrueTouch"
- "USB-C Controller", "USB-PD Controller"

## Known Issues
- Touch controller MPNs (CY8CMBR, CY8CTECH) return "PSoC" for series due to prefix ordering
- Some wireless chips (CYW, CYBLE) may not match IC type correctly

## Replacement Logic
- Same PSoC family and package may be pin-compatible
- Compares base part number before dash

## Test Patterns
When testing CypressHandler:
1. Use documentation tests for `matches()` behavior
2. Use assertions for `extractPackageCode()`, `extractSeries()`, null handling
3. Instantiate directly: `new CypressHandler()`