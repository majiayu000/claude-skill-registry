---
name: connector
description: Use when working with connector components - headers, sockets, wire-to-board, board-to-board connectors. Includes adding patterns, parsing connector MPNs, extracting pin count, pitch, and series information.
---

# Connector Component Skill

Guidance for working with connector components in the lib-electronic-components library.

## Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| Wurth | `WurthHandler` | `61########`, `62########` | `6130xx14021` |
| Molex | `MolexHandler` | `43###-####`, `39###-####`, `53###-####` | `43045-0212` |
| TE Connectivity | `TEHandler` | `1-######`, `2-######`, `282###-#` | `282836-3` |
| JST | `JSTHandler` | `PH#`, `EH#`, `XH#`, `ZH#` | `PHR-2` |
| Hirose | `HiroseHandler` | `DF#`, `FH#`, `BM#`, `ZX#` | `DF13-2P-1.25DSA` |
| Amphenol | `AmphenolHandler` | `10####`, `20####` | `10127716-001 |

## ComponentTypes

```java
// Base type
ComponentType.CONNECTOR

// Manufacturer-specific types
ComponentType.CONNECTOR_WURTH
ComponentType.CONNECTOR_MOLEX
ComponentType.CONNECTOR_TE
ComponentType.CONNECTOR_JST
ComponentType.CONNECTOR_HIROSE
ComponentType.CONNECTOR_AMPHENOL
ComponentType.CONNECTOR_HARWIN
```

## Wurth Connectors

### MPN Structure
```
61 300 14 021 1
│  │   │  │   │
│  │   │  │   └── Variant (plating, orientation)
│  │   │  └────── Pitch code (021=2.00mm, 254=2.54mm)
│  │   └───────── Pin count (14 pins)
│  └───────────── Series (300=WR-PHD)
└──────────────── Product family (61=Headers)
```

### Series Codes

| Prefix | Series | Description |
|--------|--------|-------------|
| 61 | Pin Headers | Male headers |
| 62 | Socket Headers | Female headers |
| 613 | WR-PHD | Pin Header Double Row |
| 614 | WR-BHD | Box Header |
| 615 | WR-TBL | Terminal Blocks |

## Molex Connectors

### Series & Families

| Series | Family | Pitch | Current |
|--------|--------|-------|---------|
| 43045 | Micro-Fit 3.0 | 3.00mm | 5A |
| 39281 | Mini-Fit Jr. | 4.20mm | 9A |
| 53261 | PicoBlade | 1.25mm | 1A |
| 22057 | KK 254 | 2.54mm | 3A |
| 51021 | PicoClasp | 1.00mm | 1A |
| 51047 | Nano-Fit | 2.50mm | 3.5A |

### MPN Structure
```
43045 - 0212
│       │
│       └── Position/variant (02=2 circuits, 12=vertical)
└────────── Series (Micro-Fit 3.0)
```

## JST Connectors

### Series

| Series | Pitch | Description |
|--------|-------|-------------|
| PH | 2.00mm | Wire-to-board |
| XH | 2.50mm | Wire-to-board |
| EH | 2.50mm | Wire-to-board |
| ZH | 1.50mm | Wire-to-board |
| SM | 2.50mm | Wire-to-wire |
| PA | 2.00mm | High density |

### MPN Pattern
```
PHR-2
│  │
│  └── Pin count
└───── Series (PH = 2.0mm pitch)
       R = Receptacle housing
```

## TE Connectivity Connectors

### MPN Patterns

| Pattern | Description |
|---------|-------------|
| `1-######` | Legacy part numbers |
| `2-######` | Current part numbers |
| `282###-#` | Terminal blocks |

## Adding New Connector Patterns

1. In the manufacturer handler's `initializePatterns()`:
```java
registry.addPattern(ComponentType.CONNECTOR, "^NEWCON[0-9].*");
registry.addPattern(ComponentType.CONNECTOR_MANUFACTURER, "^NEWCON[0-9].*");
```

2. Add to `getSupportedTypes()`:
```java
types.add(ComponentType.CONNECTOR);
types.add(ComponentType.CONNECTOR_MANUFACTURER);
```

## Similarity Calculation

`ConnectorSimilarityCalculator` compares:
- Pin count
- Pitch
- Connector type (header, socket, wire-to-board)
- Current rating
- Series family

## Key Handler Methods

### Extract Series
```java
// Returns "61300" from Wurth header
handler.extractSeries("6130014021");

// Returns "43045" from Molex
handler.extractSeries("43045-0212");
```

### Extract Pin Count
Most handlers can extract pin count from MPN for matching purposes.

## Connector Handler Registry

There's also a specialized connector handler system in `connectors/` package:
- `ConnectorHandler` - Interface for connector-specific parsing
- `ConnectorHandlerRegistry` - Registry of connector handlers
- `TEConnectorHandler` - TE-specific parsing
- `WurthHeaderHandler` - Wurth header parsing

---

## Learnings & Quirks

<!-- Record component-specific discoveries, edge cases, and quirks here -->
