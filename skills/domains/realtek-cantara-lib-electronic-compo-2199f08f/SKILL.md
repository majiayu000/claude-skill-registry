---
name: realtek
description: Realtek Semiconductor MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Realtek audio codecs, Ethernet controllers, WiFi ICs, or RealtekHandler.
---

# Realtek Semiconductor Manufacturer Skill

## Company Overview

Realtek Semiconductor Corporation is a fabless IC design house founded in 1987 in Taiwan. They are a leading supplier of:

- **Audio Codecs**: PC audio (ALC series) - dominant in motherboard audio
- **Ethernet Controllers**: PCIe/USB Ethernet (RTL81xx series) - #1 market share
- **Gigabit PHY**: Physical layer transceivers (RTL821x series)
- **WiFi Controllers**: 802.11n/ac/ax wireless (RTL88xx series)
- **Display Controllers**: LCD/monitor controllers (RTD2xxx series)
- **Card Readers**: SD/MMC controllers

## MPN Structure

Realtek MPNs follow this general structure:

```
[PREFIX][SERIES][VARIANT]-[PACKAGE]
   |       |        |        |
   |       |        |        +-- Package code (GR, VB, CG, etc.)
   |       |        +-- Variant letter (E, F, G, H for generations)
   |       +-- Series number (269, 1220, 8111, etc.)
   +-- Family prefix (ALC, RTL, RTD)
```

### Example Decoding

```
ALC892-GR
|  |   ||
|  |   |+-- GR = QFP package
|  |   +-- (no variant)
|  +-- 892 = High-end audio codec
+-- ALC = Audio codec family

RTL8111H-CG
|  |    |||
|  |    ||+-- CG = QFN package
|  |    |+-- H = Generation H (latest)
|  |    +-- 8111 = Gigabit Ethernet
+-- RTL = Realtek network IC

RTL8211E-VL-CG
|  |    |  | ||
|  |    |  | |+-- CG = QFN package
|  |    |  | +-- (second suffix)
|  |    |  +-- VL = QFN-VL variant
|  |    +-- E = Generation E
+-- RTL = Gigabit PHY
```

---

## Product Families

### Audio Codecs (ALC Series)

| Series | Category | Examples | Features |
|--------|----------|----------|----------|
| ALC2xx | Entry-level | ALC269, ALC272 | Basic PC audio, notebooks |
| ALC6xx | Mid-range | ALC662, ALC663 | Desktop motherboards |
| ALC8xx | High-end | ALC892, ALC898 | Enthusiast motherboards |
| ALC1xxx | HD Audio | ALC1150, ALC1200, ALC1220 | High-end gaming |
| ALC5xxx | Mobile | ALC5640, ALC5682 | Smartphones, tablets |

**Audio Codec Generations:**
- **Standard**: ALC2xx, ALC6xx, ALC8xx - PC audio applications
- **HD (High Definition)**: ALC1xxx - Premium PC audio with higher SNR
- **Mobile**: ALC5xxx - Low-power codecs for portable devices

### Ethernet Controllers (RTL81xx Series)

| Series | Category | Interface | Speed |
|--------|----------|-----------|-------|
| RTL810x | Fast Ethernet | PCIe | 10/100 Mbps |
| RTL811x | Gigabit PCIe | PCIe | 10/100/1000 Mbps |
| RTL816x | Gigabit PCIe | PCIe | 10/100/1000 Mbps |
| RTL821x | Gigabit PHY | RGMII/SGMII | 10/100/1000 Mbps |

**Notable Parts:**
- **RTL8101E**: Budget Fast Ethernet, PCIe
- **RTL8111H**: Most popular Gigabit Ethernet controller
- **RTL8168E**: Server/industrial Gigabit Ethernet
- **RTL8211E/F**: Integrated Gigabit PHY for SoCs

### WiFi Controllers (RTL88xx Series)

| Series | Standard | Band | Notes |
|--------|----------|------|-------|
| RTL8188 | 802.11n | 2.4GHz | Single-band, USB/PCIe |
| RTL8192 | 802.11n | 2.4GHz | Dual-stream, USB/PCIe |
| RTL8812 | 802.11ac | Dual-band | Wave 1, USB/PCIe |
| RTL8814 | 802.11ac | Dual-band | Wave 2, 4x4 MIMO |

**IMPORTANT**: RTL8188 and RTL8192 start with "RTL81" but are WiFi controllers, NOT Ethernet! The handler groups them with RTL88xx for series extraction.

### Display Controllers (RTD2xxx Series)

| Series | Category | Application |
|--------|----------|-------------|
| RTD2xxx | LCD Controllers | Monitors, TVs |

---

## Package Codes

### QFP (Quad Flat Package)

| Code | Package | Notes |
|------|---------|-------|
| GR | QFP | Standard quad flat package |
| G | QFP | QFP variant |

### QFN (Quad Flat No-lead)

| Code | Package | Notes |
|------|---------|-------|
| VB | QFN | Standard QFN |
| CG | QFN | Common for Ethernet ICs |
| VL | QFN-VL | QFN VL variant |
| VS | QFN-VS | QFN VS variant |
| VD | QFN-VD | QFN VD variant |
| VA | QFN-VA | QFN VA variant |
| VC | QFN-VC | QFN VC variant |
| VF | QFN-VF | QFN VF variant |
| LF | QFN-LF | Lead-free QFN |

### BGA (Ball Grid Array)

| Code | Package | Notes |
|------|---------|-------|
| BR | BGA | Ball grid array |
| BG | BGA | BGA variant |

### Qualifiers

| Code | Meaning | Notes |
|------|---------|-------|
| TR | Tape and Reel | Packaging for SMT |
| LF | Lead-free | RoHS compliant |

---

## Series Extraction Rules

The handler extracts series using these rules:

| MPN Prefix | Series | Product Category |
|------------|--------|------------------|
| ALC1xxx | ALC1 | HD Audio Codecs |
| ALC5xxx | ALC5 | Mobile Audio Codecs |
| ALC2xx | ALC2 | Entry-level Audio |
| ALC6xx | ALC6 | Mid-range Audio |
| ALC8xx | ALC8 | High-end Audio |
| RTL8188/8192 | RTL88 | WiFi Controllers (special case!) |
| RTL810x/811x/816x | RTL81 | Ethernet Controllers |
| RTL821x | RTL82 | Gigabit PHY |
| RTL88xx | RTL88 | WiFi Controllers |
| RTD2xxx | RTD2 | Display Controllers |

**CRITICAL**: RTL8188 and RTL8192 return "RTL88" (WiFi series), not "RTL81" (Ethernet), even though they start with "RTL81".

---

## Official Replacement Rules

The handler identifies compatible replacements within series:

### Audio Codec Compatibility

| Original | Replacement | Notes |
|----------|-------------|-------|
| ALC892 | ALC898 | Pin-compatible upgrade |
| ALC898 | ALC892 | Pin-compatible downgrade |
| ALC1150 | ALC1200 | Similar pinouts |
| ALC1200 | ALC1220 | Often compatible |

### Ethernet Controller Compatibility

| Original | Replacement | Notes |
|----------|-------------|-------|
| RTL8111E | RTL8111F/G/H | Backward compatible generations |
| RTL8168E | RTL8168F/G/H | Backward compatible generations |
| RTL8211E | RTL8211F | Backward compatible |

### WiFi Controller Compatibility

| Original | Replacement | Notes |
|----------|-------------|-------|
| RTL8188EU | RTL8188EUS | Same IC, different suffix |
| RTL8192EU | RTL8192EUS | Same IC, different suffix |

---

## Handler Helper Methods

The RealtekHandler provides these utility methods for product classification:

### `isAudioCodec(String mpn)`
Returns true if the MPN is an ALC audio codec.
```java
isAudioCodec("ALC892-GR")     // true
isAudioCodec("RTL8111H-CG")   // false
```

### `isNetworkController(String mpn)`
Returns true if the MPN is an Ethernet controller (excludes WiFi).
```java
isNetworkController("RTL8111H-CG")   // true
isNetworkController("RTL8188EU")     // false (WiFi, not Ethernet!)
```

### `isWiFiController(String mpn)`
Returns true if the MPN is a WiFi controller.
```java
isWiFiController("RTL8188EU")    // true
isWiFiController("RTL8812AU")    // true
isWiFiController("RTL8111H-CG")  // false
```

### `isDisplayController(String mpn)`
Returns true if the MPN is an RTD display controller.
```java
isDisplayController("RTD2660")   // true
isDisplayController("ALC892")    // false
```

### `getAudioCodecGeneration(String mpn)`
Returns the audio codec generation.
```java
getAudioCodecGeneration("ALC1220")  // "HD"
getAudioCodecGeneration("ALC5682")  // "Mobile"
getAudioCodecGeneration("ALC892")   // "Standard"
```

### `getNetworkInterfaceType(String mpn)`
Returns the network interface type.
```java
getNetworkInterfaceType("RTL8101E")   // "Fast Ethernet"
getNetworkInterfaceType("RTL8111H")   // "Gigabit Ethernet"
getNetworkInterfaceType("RTL8211F")   // "Gigabit PHY"
getNetworkInterfaceType("RTL8188EU")  // "WiFi"
```

---

## Example MPNs with Full Decoding

### Audio Codecs

| MPN | Series | Package | Generation | Notes |
|-----|--------|---------|------------|-------|
| ALC269-GR | ALC2 | QFP | Standard | Entry-level notebook audio |
| ALC662-GR | ALC6 | QFP | Standard | Mid-range desktop audio |
| ALC892-GR | ALC8 | QFP | Standard | High-end motherboard audio |
| ALC1150-VB | ALC1 | QFN | HD | Premium PC audio |
| ALC1220-VB | ALC1 | QFN | HD | Top-tier gaming audio |
| ALC5640-VB | ALC5 | QFN | Mobile | Smartphone/tablet audio |
| ALC5682-VF | ALC5 | QFN | Mobile | Current mobile audio |

### Ethernet Controllers

| MPN | Series | Package | Interface | Notes |
|-----|--------|---------|-----------|-------|
| RTL8101E-GR | RTL81 | QFP | Fast Ethernet | 10/100 Mbps PCIe |
| RTL8102E-GR | RTL81 | QFP | Fast Ethernet | 10/100 Mbps PCIe |
| RTL8111E-VL-CG | RTL81 | QFN | Gigabit | Gen E Gigabit PCIe |
| RTL8111H-CG | RTL81 | QFN | Gigabit | Latest Gigabit PCIe |
| RTL8168E-VL-CG | RTL81 | QFN | Gigabit | Server Gigabit |
| RTL8211E-VL-CG | RTL82 | QFN | Gigabit PHY | Integrated PHY |
| RTL8211F-CG | RTL82 | QFN | Gigabit PHY | Latest PHY |

### WiFi Controllers

| MPN | Series | Package | Standard | Notes |
|-----|--------|---------|----------|-------|
| RTL8188EU | RTL88 | - | 802.11n | USB 2.4GHz |
| RTL8188EUS | RTL88 | - | 802.11n | USB 2.4GHz |
| RTL8192EU | RTL88 | - | 802.11n | USB 2.4GHz dual-stream |
| RTL8812AU | RTL88 | - | 802.11ac | USB dual-band |
| RTL8814AU | RTL88 | - | 802.11ac | USB 4x4 MIMO |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// Realtek uses hyphen-separated suffixes
// Most MPNs: BASE-PACKAGE
// Multi-suffix: BASE-VARIANT-PACKAGE (take last segment)

int lastDashIndex = mpn.lastIndexOf('-');
String suffix = mpn.substring(lastDashIndex + 1);
return decodePackageCode(suffix);

// Package codes starting with 'V' are typically QFN variants
// Package codes starting with 'G' are typically QFP
// Package codes starting with 'B' are typically BGA
```

### Series Extraction - WiFi Special Case

```java
// CRITICAL: RTL8188 and RTL8192 must be checked BEFORE general RTL81xx
// They start with "RTL81" but are WiFi, not Ethernet!

if (upperMpn.startsWith("RTL8188") || upperMpn.startsWith("RTL8192")) {
    return "RTL88";  // Group with WiFi series
}
// Then check RTL81 for Ethernet
if (upperMpn.startsWith("RTL81")) {
    return "RTL81";
}
```

### Component Type

RealtekHandler only supports `ComponentType.IC`. All Realtek products (audio codecs, Ethernet, WiFi, display controllers) are registered under the base IC type.

---

## Related Files

- Handler: `manufacturers/RealtekHandler.java`
- Component types: `ComponentType.IC` (all Realtek products)
- Supported types: `Set.of(ComponentType.IC)` (immutable)

---

## Learnings & Quirks

- **WiFi vs Ethernet disambiguation**: RTL8188 and RTL8192 start with "RTL81" but are WiFi controllers, NOT Ethernet. The handler explicitly checks these before the general RTL81 Ethernet pattern.
- **Package code prefixes**: Most QFN variants start with 'V' (VB, VL, VS, VD, VA, VC, VF). The handler uses a switch statement with fallback to prefix matching.
- **Multi-suffix MPNs**: Some MPNs have multiple hyphens (e.g., RTL8211E-VL-CG). The handler extracts the LAST segment as the package code.
- **Audio codec tiers**: ALC1xxx is HD Audio (highest quality), ALC8xx is high-end, ALC6xx is mid-range, ALC2xx is entry-level, ALC5xxx is mobile.
- **Ethernet generation letters**: RTL8111 generations (E, F, G, H) are typically backward compatible. H is the latest generation.
- **getSupportedTypes() uses Set.of()**: Handler correctly uses immutable Set.of() instead of HashSet.
- **All products registered as IC**: Unlike some handlers, Realtek doesn't use manufacturer-specific ComponentTypes (no AUDIO_CODEC_REALTEK etc.). Everything is ComponentType.IC.
- **No manufacturer-specific types**: getManufacturerTypes() returns empty set.

<!-- Add new learnings above this line -->
