---
name: ic
description: Use when working with integrated circuits - microcontrollers, op-amps, voltage regulators, logic ICs. Includes adding patterns, parsing MPNs, extracting specifications like voltage, package, and series information.
---

# Integrated Circuit Skill

Guidance for working with ICs (microcontrollers, op-amps, voltage regulators, logic) in the lib-electronic-components library.

## Microcontrollers

### Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| Microchip | `MicrochipHandler` | `PIC#`, `dsPIC#`, `ATmega#`, `ATtiny#` | `PIC16F877A`, `ATmega328P` |
| ST | `STHandler` | `STM32#`, `STM8#` | `STM32F103C8T6` |
| TI | `TIHandler` | `MSP430#`, `CC####` | `MSP430G2553` |
| NXP | `NXPHandler` | `LPC#`, `MK#`, `IMX#`, `S32K#` | `LPC1768` |
| Espressif | `EspressifHandler` | `ESP32#`, `ESP8266` | `ESP32-WROOM-32` |
| Renesas | `RenesasHandler` | `RX#`, `RA#`, `R5F#` | `RX651` |
| Infineon | `InfineonHandler` | `XMC#` | `XMC4500` |
| Cypress | `CypressHandler` | `CY#`, `PSoC#` | `CY8C5888` |

### ComponentTypes

```java
// Base types
ComponentType.MICROCONTROLLER
ComponentType.IC

// Manufacturer-specific
ComponentType.MICROCONTROLLER_MICROCHIP
ComponentType.MICROCONTROLLER_ST
ComponentType.MICROCONTROLLER_TI
ComponentType.MICROCONTROLLER_NXP
ComponentType.MICROCONTROLLER_ESPRESSIF
ComponentType.MICROCONTROLLER_RENESAS
ComponentType.MICROCONTROLLER_INFINEON
ComponentType.MICROCONTROLLER_ATMEL

// Architecture-specific
ComponentType.PIC_MCU
ComponentType.AVR_MCU
ComponentType.MSP430_MCU
ComponentType.ESP32_SOC
ComponentType.ESP8266_SOC
ComponentType.KINETIS_MCU
ComponentType.LPC_MCU
```

### MPN Structure - STM32

```
STM32 F 103 C 8 T 6
│     │ │   │ │ │ │
│     │ │   │ │ │ └── Temperature (-40 to +85°C)
│     │ │   │ │ └──── Package (T=LQFP)
│     │ │   │ └────── Flash size (8=64KB)
│     │ │   └──────── Pin count (C=48 pins)
│     │ └──────────── Performance line (103)
│     └────────────── Family (F=Foundation)
└──────────────────── Series
```

## Op-Amps

### Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| TI | `TIHandler` | `LM###`, `TL0##`, `OPA###` | `LM358`, `TL072`, `OPA2134` |
| Analog Devices | `AnalogDevicesHandler` | `AD###`, `ADA###`, `OP##` | `AD8605`, `OP07` |
| ST | `STHandler` | `LM###`, `TS###` | `TS912` |
| ON Semi | `OnSemiHandler` | `LM###`, `MC####` | `MC1458` |

### ComponentTypes

```java
ComponentType.OPAMP
ComponentType.OPAMP_TI
ComponentType.OPAMP_AD
ComponentType.OPAMP_ST
ComponentType.OPAMP_ON
ComponentType.OPAMP_INFINEON
ComponentType.OPAMP_NXP
ComponentType.OPAMP_ROHM
```

### Common Op-Amp Series

| Series | Type | Key Specs |
|--------|------|-----------|
| LM358 | Dual | Low power, single supply |
| LM324 | Quad | Low power, single supply |
| TL072 | Dual | JFET input, low noise |
| OPA2134 | Dual | Audio, low distortion |
| AD8605 | Single | Rail-to-rail, CMOS |
| NE5532 | Dual | Audio, low noise |

## Voltage Regulators

### Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| TI | `TIHandler` | `LM78##`, `LM79##`, `LM317`, `TPS###` | `LM7805`, `LM317T`, `TPS65281` |
| ST | `STHandler` | `L78##`, `LD1117` | `L7805CV`, `LD1117V33` |
| ON Semi | `OnSemiHandler` | `MC78##`, `NCP###` | `MC7805CT` |
| Maxim | `MaximHandler` | `MAX###` | `MAX1555` |
| Analog Devices | `AnalogDevicesHandler` | `ADP###`, `LT####` | `ADP3338`, `LT1086` |

### ComponentTypes

```java
ComponentType.VOLTAGE_REGULATOR
ComponentType.VOLTAGE_REGULATOR_LINEAR_TI
ComponentType.VOLTAGE_REGULATOR_SWITCHING_TI
ComponentType.VOLTAGE_REGULATOR_LINEAR_ST
ComponentType.VOLTAGE_REGULATOR_SWITCHING_ST
ComponentType.VOLTAGE_REGULATOR_LINEAR_INFINEON
ComponentType.VOLTAGE_REGULATOR_SWITCHING_INFINEON
ComponentType.VOLTAGE_REGULATOR_LINEAR_ON
ComponentType.VOLTAGE_REGULATOR_SWITCHING_ON
ComponentType.VOLTAGE_REGULATOR_MAXIM
ComponentType.VOLTAGE_REGULATOR_DIODES
ComponentType.VOLTAGE_REGULATOR_ROHM
ComponentType.VOLTAGE_REGULATOR_TOSHIBA
```

### MPN Structure - LM78xx

```
LM 78 05 CT
│  │  │  │
│  │  │  └── Package (CT=TO-220)
│  │  └───── Output voltage (05=5V)
│  └──────── Series (78=positive, 79=negative)
└─────────── Family
```

## Logic ICs

### Handler

`LogicICHandler` handles the 74xx and CD4xxx series.

### Patterns

| Pattern | Family | Description |
|---------|--------|-------------|
| `74LS###` | 74LS | Low-power Schottky |
| `74HC###` | 74HC | High-speed CMOS |
| `74HCT###` | 74HCT | CMOS with TTL levels |
| `74AHC###` | 74AHC | Advanced HC |
| `74LVC###` | 74LVC | Low-voltage CMOS |
| `CD4###` | CD4000 | CMOS 4000 series |

### ComponentTypes

```java
ComponentType.LOGIC_IC
ComponentType.LOGIC_IC_NEXPERIA
ComponentType.LOGIC_IC_DIODES
ComponentType.DIGITAL_IC
```

## Adding New IC Patterns

1. In the manufacturer handler's `initializePatterns()`:
```java
registry.addPattern(ComponentType.OPAMP, "^NEWOPA[0-9].*");
registry.addPattern(ComponentType.OPAMP_MANUFACTURER, "^NEWOPA[0-9].*");
```

2. Add to `getSupportedTypes()`:
```java
types.add(ComponentType.OPAMP);
types.add(ComponentType.OPAMP_MANUFACTURER);
```

## Similarity Calculators

- `MicrocontrollerSimilarityCalculator` - Compares architecture, flash, RAM, peripherals
- `OpAmpSimilarityCalculator` - Compares GBW, slew rate, supply voltage
- `VoltageRegulatorSimilarityCalculator` - Compares output voltage, current, dropout
- `LogicICSimilarityCalculator` - Compares function, family, voltage levels

## Common Packages

| Package | Pins | Description |
|---------|------|-------------|
| DIP | 8-40 | Through-hole |
| SOIC | 8-28 | Surface mount |
| TSSOP | 8-56 | Thin small outline |
| QFP | 32-256 | Quad flat |
| LQFP | 32-256 | Low-profile QFP |
| QFN | 8-88 | Quad flat no-lead |
| BGA | Various | Ball grid array |

---

## Learnings & Quirks

<!-- Record component-specific discoveries, edge cases, and quirks here -->
