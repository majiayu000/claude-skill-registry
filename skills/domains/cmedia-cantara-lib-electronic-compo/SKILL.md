---
name: cmedia
description: C-Media Electronics MPN encoding patterns, USB audio controller decoding, and handler guidance. Use when working with C-Media audio ICs or CMediaHandler.
---

# C-Media Electronics Manufacturer Skill

## MPN Structure

C-Media specializes in USB and HD audio controller ICs.

### CM Series (USB Audio)
```
CM[SERIES][VARIANT]-[PACKAGE][PINS]
   |   |      |        |       |
   |   |      |        |       +-- Pin count (optional)
   |   |      |        +-- Package code (QFP, LQFP, etc.)
   |   |      +-- Variant (A, AH, B)
   |   +-- Series (108, 109, 119, 6xxx)
   +-- CM = C-Media prefix
```

### CMI Series (HD/PCI Audio)
```
CMI[SERIES][VARIANT]
    |   |      |
    |   |      +-- Variant suffix
    |   +-- Series (8738, 8768, 8788)
    +-- CMI = C-Media Interface
```

### Example Decoding

```
CM108AH
|  | ||
|  | |+-- H = variant revision
|  | +-- A = first variant
|  +-- 108 = Basic USB stereo audio codec
+-- CM = C-Media prefix

CM6631A-S
|  |   ||
|  |   |+-- S = SSOP package
|  |   +-- A = variant
|  +-- 6631 = Professional USB 2.0 audio processor
+-- CM = C-Media prefix

CMI8788
|   |||
|   ||+-- 8 = series number
|   |+-- 8 = 8-channel HD audio
|   +-- 87 = HD audio codec series
+-- CMI = C-Media Interface
```

---

## Product Families

### CM108 Series - Basic USB Audio Codec

Entry-level USB stereo audio for PC peripherals.

| Part | Description | Features |
|------|-------------|----------|
| CM108 | USB stereo codec | Basic stereo |
| CM108AH | Enhanced version | Higher quality |
| CM108B | Cost-optimized | Lower cost |

### CM109 Series - USB Audio with HID

USB audio with keyboard/HID controller for headsets.

| Part | Description |
|------|-------------|
| CM109 | USB audio + HID keyboard |
| CM109A | Enhanced variant |

### CM119 Series - USB 7.1 Channel Audio

Multi-channel USB audio for gaming and surround sound.

| Part | Description | Channels |
|------|-------------|----------|
| CM119 | 7.1 USB audio | 8 |
| CM119A | Enhanced version | 8 |
| CM119B | Cost-optimized | 8 |

### CM6xxx Series - Professional USB Audio

Higher-end USB audio ICs for professional applications.

| Part | Description |
|------|-------------|
| CM6206 | USB 2.0 basic audio |
| CM6400 | USB audio controller |
| CM6631 | USB 2.0 audio processor |
| CM6631A | Enhanced CM6631 |
| CM6632 | USB audio DAC |

### CMI87xx Series - HD Audio Codec (PCI/PCIe)

HD audio codecs for motherboards and sound cards.

| Part | Description | Features |
|------|-------------|----------|
| CMI8738 | PCI audio codec | Legacy 7.1 |
| CMI8768 | PCI-E audio | 7.1 surround |
| CMI8788 | Oxygen HD Audio | High-end 8-ch |

### CMI83xx Series - Legacy PCI Audio

Older PCI audio codecs.

| Part | Description |
|------|-------------|
| CMI8330 | Legacy PCI audio |

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| QFP | QFP | Quad flat package |
| LQFP, LQ | LQFP | Low-profile QFP |
| QFN | QFN | Quad flat no-lead |
| SSOP, S | SSOP | Shrink small outline |
| TQFP | TQFP | Thin QFP |
| PLCC | PLCC | Plastic leadless |
| BGA | BGA | Ball grid array |

### Package Code Extraction

```java
// Handle hyphenated suffixes
// CM6631A-LQ -> LQFP
// CM6631A-S -> SSOP

// Handle embedded package codes
// After variant letters, look for package indicators
```

---

## Variant Suffixes

| Suffix | Meaning |
|--------|---------|
| A | First variant revision |
| AH | Enhanced variant |
| B | Second variant (often cost-optimized) |

---

## Handler Implementation Notes

### Series Extraction

```java
// CM108, CM109, CM119 - return 5 characters
if (upperMpn.matches("^CM108.*")) return "CM108";
if (upperMpn.matches("^CM109.*")) return "CM109";
if (upperMpn.matches("^CM119.*")) return "CM119";

// CM6xxx - return 6 characters (CM + 4 digits)
if (upperMpn.matches("^CM6[0-9]{3}.*")) {
    return upperMpn.substring(0, 6);  // CM6631
}

// CMI87xx - return 7 characters (CMI + 4 digits)
if (upperMpn.matches("^CMI87[0-9]{2}.*")) {
    return upperMpn.substring(0, 7);  // CMI8788
}
```

### Base Part Number Extraction

```java
// Include variant letters in base part
// CM108AH -> CM108AH
// CM6631A -> CM6631A

// Stop at package indicators
if (remaining.matches("^(QFP|LQFP|QFN|SSOP|TQFP).*")) {
    break;
}
```

### Matching Patterns

```java
// CM10x series
"^CM10[89][A-Z]*.*"

// CM119 series
"^CM119[A-Z]*.*"

// CM6xxx series
"^CM6[0-9]{3}[A-Z]*.*"

// CMI87xx series
"^CMI87[0-9]{2}[A-Z]*.*"

// CMI83xx series
"^CMI83[0-9]{2}[A-Z]*.*"
```

---

## Replacement Rules

### Same Series Variants

Parts in the same series with different variants (A, AH, B) are generally compatible:
- CM108 -> CM108A -> CM108AH (increasing quality)
- CM119 -> CM119A -> CM119B (same features, different optimization)

### Different Series

Different series are NOT compatible (different USB classes, channel counts):
- CM6206 != CM6631 (different USB audio implementations)
- CM108 != CM119 (stereo vs 7.1 channel)

---

## Related Files

- Handler: `manufacturers/CMediaHandler.java`
- Component types: `ComponentType.IC`

---

## Common MPNs

| MPN | Description | Application |
|-----|-------------|-------------|
| CM108AH | USB stereo codec | USB headsets |
| CM109 | USB audio + HID | Gaming headsets |
| CM119 | USB 7.1 audio | Gaming audio |
| CM6631A | USB 2.0 audio processor | USB DACs |
| CM6632 | USB audio DAC | External audio |
| CMI8788 | Oxygen HD Audio | Sound cards |

---

## USB Class Compliance

| Series | USB Class | Driver Required |
|--------|-----------|-----------------|
| CM108 | USB Audio Class 1.0 | No (driverless) |
| CM119 | USB Audio Class 1.0 | No (driverless) |
| CM6631 | USB Audio Class 2.0 | Yes (on Windows) |

---

## Applications

- USB headsets
- USB sound cards
- Gaming audio devices
- USB DACs
- Webcams with audio
- Conference devices
- PCI/PCIe sound cards
- Motherboard audio

---

## Learnings & Edge Cases

- **CM vs CMI prefix**: CM = USB audio controllers, CMI = PCI/PCIe HD audio codecs.
- **USB Class matters**: CM108/CM119 are class-compliant (driverless), CM6631 needs drivers on Windows.
- **7.1 channel support**: CM119 series is for 7.1 surround, CM108 is stereo only.
- **HID keyboard support**: CM109 has integrated HID controller for headset buttons/volume.
- **CMI8788 "Oxygen"**: High-end part used in audiophile sound cards (Asus Xonar, etc.).
- **Variant progression**: A < AH < B is not always quality progression - check datasheets.
- **Package suffix position**: Package code comes after variant letter(s) in hyphenated format.

<!-- Add new learnings above this line -->
