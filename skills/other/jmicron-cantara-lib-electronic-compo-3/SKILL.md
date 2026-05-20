---
name: jmicron
description: JMicron Technology MPN encoding patterns, series identification, and handler guidance. Use when working with storage controller ICs or JMicronHandler.
---

# JMicron Technology Manufacturer Skill

## MPN Structure

JMicron MPNs follow these general structures:

```
JMS[SERIES][VARIANT][PACKAGE]    (USB-SATA bridges)
JMB[SERIES][VARIANT][PACKAGE]    (PCIe/SATA controllers)
JMF[SERIES][VARIANT][PACKAGE]    (Flash controllers)
JM20[SERIES][VARIANT][PACKAGE]   (Legacy IDE/SATA)
 |     |       |        |
 |     |       |        └── Package code (QFN, LQFP, BGA, etc.)
 |     |       └── Variant letter (optional)
 |     └── 3-digit series number
 └── JMS/JMB/JMF/JM20 prefix
```

### Example Decoding

```
JMS583-QFN
│  │  │
│  │  └── QFN package
│  └── 583 = USB 3.1 Gen2 to SATA/NVMe bridge
└── JMS = JMicron USB-SATA prefix

JMB585-LQFP
│  │  │
│  │  └── LQFP package
│  └── 585 = 5-port PCIe Gen3 SATA controller
└── JMB = JMicron board controller prefix
```

---

## Product Series

### JMS5xx Series - USB to SATA Bridges

| Series | Interface | Description |
|--------|-----------|-------------|
| JMS539 | USB 3.0 | USB 3.0 to SATA III bridge |
| JMS567 | USB 3.0 | USB 3.0 to SATA III with UASP |
| JMS578 | USB 3.1 Gen1 | USB 3.1 Gen1 to SATA III |
| JMS583 | USB 3.1 Gen2 | USB 3.1 Gen2 to SATA III/NVMe |

### JMB5xx Series - PCIe SATA Controllers

| Series | Interface | Description |
|--------|-----------|-------------|
| JMB575 | PCIe | 5-port SATA 6Gb/s controller |
| JMB585 | PCIe Gen3 | 5-port SATA 6Gb/s PCIe Gen3 controller |

### JMB3xx Series - SATA/PATA Controllers

| Series | Interface | Description |
|--------|-----------|-------------|
| JMB363 | PCIe | SATA/PATA combo controller |
| JMB368 | PCIe | PATA controller |

### JMF Series - Flash Controllers

| Series | Type | Description |
|--------|------|-------------|
| JMF60x | Flash | SSD controller (early gen) |
| JMF61x | Flash | SSD controller |
| JMF66x | Flash | SSD controller (newer gen) |

### JM20xxx Series - Legacy Controllers

| Series | Interface | Description |
|--------|-----------|-------------|
| JM20330 | IDE/SATA | SATA to PATA bridge |
| JM20337 | IDE/SATA | IDE to SATA bridge |

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| QFN | QFN | Quad Flat No-Lead |
| Q | QFN | Short form |
| LQFP | LQFP | Low-profile Quad Flat Package |
| L | LQFP | Short form |
| BGA | BGA | Ball Grid Array |
| B | BGA | Short form |
| T | TQFP | Thin Quad Flat Package |

---

## USB Generation by Series

| Series | USB Generation | Notes |
|--------|----------------|-------|
| JMS539 | USB 3.0 | 5Gbps |
| JMS567 | USB 3.0 | 5Gbps, UASP support |
| JMS578 | USB 3.1 Gen1 | 5Gbps |
| JMS583 | USB 3.1 Gen2 | 10Gbps |

---

## Feature Support Matrix

| Series | UASP | NVMe | Port Count |
|--------|------|------|------------|
| JMS539 | No | No | 1 |
| JMS567 | Yes | No | 1 |
| JMS578 | Yes | No | 1 |
| JMS583 | Yes | Yes | 1 |
| JMB575 | N/A | No | 5 |
| JMB585 | N/A | No | 5 |
| JMB363 | N/A | No | 2 |
| JMB368 | N/A | No | 2 |

---

## Handler Implementation Notes

### Pattern Matching

```java
// JMS5xx series - USB to SATA bridge controllers
"^JMS5[0-9]{2}[A-Z]*.*"

// JMB5xx series - PCIe SATA/NVMe controllers
"^JMB5[0-9]{2}[A-Z]*.*"

// JMB3xx series - SATA port multiplier/host controllers
"^JMB3[0-9]{2}[A-Z]*.*"

// JMF series - Flash memory controllers
"^JMF[0-9]+[A-Z]*.*"

// JMB4xx series - USB bridge controllers (legacy)
"^JMB4[0-9]{2}[A-Z]*.*"

// JM20xxx series - IDE/SATA controllers (legacy)
"^JM20[0-9]{3}[A-Z]*.*"
```

### Series Extraction

```java
// JMS/JMB series: prefix + 3 digits = 6 characters
// JMS583 -> JMS583
// JMB585 -> JMB585

if (upperMpn.matches("^JMS5[0-9]{2}.*")) {
    return upperMpn.substring(0, 6);
}

// JMF series: variable length digits
// JMF612 -> JMF612
// JMF667 -> JMF667

// JM20xxx series: 7 characters
// JM20330 -> JM20330
```

### Package Code Extraction

```java
// Check hyphenated package codes first
// JMS583-QFN -> QFN

// Then check trailing letters after digits
// JMS583Q -> QFN (Q maps to QFN)
```

---

## Replacement Compatibility

### USB-SATA Bridge Upgrade Path

Higher generation can replace lower:
- JMS567 can replace JMS539 (adds UASP)
- JMS578 can replace JMS567 (USB 3.1 Gen1)
- JMS583 can replace JMS578 (USB 3.1 Gen2, adds NVMe)

**Level hierarchy:**
```
JMS539 (Level 1) < JMS567 (Level 2) < JMS578 (Level 3) < JMS583 (Level 4)
```

### PCIe SATA Controllers

- JMB585 can replace JMB575 (newer, PCIe Gen3)

### Non-Interchangeable

- JMS5xx (USB bridges) NOT compatible with JMB5xx (PCIe controllers)
- Different interface types cannot be swapped

---

## Common Applications

| Series | Application |
|--------|-------------|
| JMS539/567/578/583 | External USB hard drive enclosures |
| JMB575/585 | Multi-drive SATA expansion cards |
| JMB363 | Motherboard SATA+PATA combo |
| JMF series | SSD/Flash drive controllers |

---

## Related Files

- Handler: `manufacturers/JMicronHandler.java`
- Component types: `ComponentType.IC`

---

## Learnings & Edge Cases

- **JMS583 is unique for NVMe support**: Only USB-SATA bridge that supports NVMe
- **UASP support important for performance**: JMS567+ support UASP for better performance
- **Prefix indicates interface type**: JMS = USB, JMB = PCIe board controller, JMF = Flash
- **5-port controllers**: JMB575/585 are specifically 5-port SATA controllers
- **Legacy JM20xxx series**: Still found in older devices, uses 7-character part numbers
- **Variable digit length in JMF**: JMF series uses variable-length numeric suffixes

<!-- Add new learnings above this line -->
