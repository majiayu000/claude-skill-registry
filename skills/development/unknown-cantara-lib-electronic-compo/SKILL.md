---
name: sullins
description: Sullins Connector Solutions MPN encoding patterns, series decoding, and handler guidance. Use when working with Sullins connectors or SullinsHandler.
---

# Sullins Connector Solutions Manufacturer Skill

## MPN Structure

Sullins uses letter-prefix series with encoded specifications:

### SBH/SFH Series (Box Headers, FFC/FPC)

```
SBH11-PBPC-D10-ST-BK
 |  |   |   |   |  |
 |  |   |   |   |  +-- Color (BK=Black, GY=Gray)
 |  |   |   |   +-- Mount (ST=Straight, RA=Right Angle)
 |  |   |   +-- Pin count (D10 = Dual 10 = 20 total pins)
 |  |   +-- Contact type (PBPC=Phosphor Bronze, Tin)
 |  +-- Series variant (11, 21, etc.)
 +-- Series prefix (SBH=Box Header, SFH=FFC/FPC)
```

### PPPC/PRPC/NPPN Series (Headers)

```
PRPC040SAAN-RC
 |   | ||| |  |
 |   | ||| |  +-- Mount suffix (RC=Through-Hole, SC=SMT)
 |   | ||| +-- Plating (N=Tin, etc.)
 |   | ||+-- Contact options
 |   | |+-- Contact type
 |   | +-- Row count (1=Single, 2=Dual)
 |   +-- Pin count (040 = 40 pins)
 +-- Series (PRPC=Male, PPPC=Female, NPPN=Pin)
```

---

## Series Reference

### SBH Series - Box Headers

| Feature | Value |
|---------|-------|
| Type | Shrouded male header |
| Pitch | 2.54mm |
| Rated Current | 3.0A |
| Row Config | Dual row |

Pattern: `^SBH[0-9]+-[A-Z]+-D[0-9]+.*`

### PPPC Series - Female Headers

| Feature | Value |
|---------|-------|
| Type | Female socket header |
| Pitch | 2.54mm |
| Rated Current | 3.0A |
| Row Config | Single or dual |

Pattern: `^PPPC[0-9]+.*`

### PRPC Series - Male Headers

| Feature | Value |
|---------|-------|
| Type | Male pin header |
| Pitch | 2.54mm |
| Rated Current | 3.0A |
| Row Config | Single or dual |

Pattern: `^PRPC[0-9]+.*`

### NPPN Series - Pin Headers

| Feature | Value |
|---------|-------|
| Type | Pin header |
| Pitch | 2.54mm |
| Rated Current | 3.0A |
| Row Config | Configurable |

Pattern: `^NPPN[0-9]+.*`

### SFH Series - FFC/FPC Connectors

| Feature | Value |
|---------|-------|
| Type | Flat flex cable connector |
| Pitch | 1.27mm |
| Rated Current | 1.0A |
| Row Config | Dual row |

Pattern: `^SFH[0-9]+-[A-Z]+-D[0-9]+.*`

---

## Pin Count Extraction

### SBH/SFH Series

Pin count follows "D" prefix and is doubled for dual row:

```java
// SBH11-PBPC-D10-ST-BK -> 10 * 2 = 20 pins
Matcher m = Pattern.compile("D([0-9]+)").matcher(mpn);
if (m.find()) {
    return Integer.parseInt(m.group(1)) * 2;  // Dual row
}
```

### PPPC/PRPC/NPPN Series

Pin count is first 2-3 digits after series prefix:

```java
// PRPC040SAAN-RC -> 40 pins
// PPPC081LFBN-RC -> 8 pins
Pattern.compile("(PPPC|PRPC|NPPN)([0-9]+)").matcher(mpn);
return Integer.parseInt(m.group(2));
```

---

## Mounting Type Codes

### Suffix Codes

| Code | Mounting Type |
|------|---------------|
| -RC | Through-Hole |
| -SC | SMT |
| ST | Straight (Through-Hole) |
| RA | Right Angle (Through-Hole) |
| SM | Surface Mount |

### Detection Example

```java
String upper = mpn.toUpperCase();
if (upper.contains("-RC")) return "Through-Hole";
if (upper.contains("-SC")) return "SMT";
if (upper.contains("-RA")) return "Through-Hole Right Angle";
if (upper.contains("-ST")) return "Through-Hole Straight";
```

---

## Gender Detection

| Series | Gender |
|--------|--------|
| PPPC | Female (Socket) |
| PRPC | Male (Pin) |
| NPPN | Male (Pin) |
| SBH | Male (Shrouded) |
| SFH | Male (Shrouded) |

---

## Row Count Detection

### SBH/SFH

Always dual row (indicated by "D" prefix before pin count).

### PPPC/PRPC/NPPN

Digit after pin count indicates rows:

```java
// PRPC040SAAN-RC
//        ^ Row digit (S=Single, but position encoding varies)
// Check the digit after the pin count digits

// More reliable: Parse with regex
Pattern.compile("(PPPC|PRPC|NPPN)([0-9]+)([0-9])").matcher(mpn);
int rows = Integer.parseInt(m.group(3));  // 1=single, 2=dual
```

---

## Contact Plating

| Code | Plating Type |
|------|--------------|
| GN, G/ | Gold |
| SN, T/ | Tin |
| LF | Lead-Free Tin |

---

## Handler Implementation Notes

### Series Extraction

```java
// Extract known series prefixes
if (upperMpn.startsWith("SBH")) return "SBH";
if (upperMpn.startsWith("PPPC")) return "PPPC";
if (upperMpn.startsWith("PRPC")) return "PRPC";
if (upperMpn.startsWith("NPPN")) return "NPPN";
if (upperMpn.startsWith("SFH")) return "SFH";

// Generic extraction (3-4 letter prefix before digits)
Pattern.compile("^([A-Z]{3,4})[0-9]").matcher(mpn);
```

### Package Code Extraction

```java
// SBH/SFH: Mount type is in dash-separated field
// Example: SBH11-PBPC-D10-ST-BK -> ST = Straight

// PPPC/PRPC/NPPN: Mount type is suffix
// Example: PRPC040SAAN-RC -> RC = Through-Hole

// Look for standard suffix codes
if (upper.contains("-RC")) return "Through-Hole";
if (upper.contains("-SC")) return "SMT";
```

### Replacement Compatibility

```java
// Compatible if:
// 1. Same series
// 2. Same pin count
// 3. Compatible mounting type (both THT or both SMT)

String series1 = extractSeries(mpn1);
String series2 = extractSeries(mpn2);
if (!series1.equals(series2)) return false;

int pins1 = extractPinCount(mpn1);
int pins2 = extractPinCount(mpn2);
if (pins1 != pins2) return false;

return areCompatibleMountingTypes(mpn1, mpn2);
```

---

## Common Part Numbers

| MPN | Description |
|-----|-------------|
| PRPC040SAAN-RC | 40-pin male header, single row, through-hole |
| PPPC081LFBN-RC | 8-pin female header, lead-free, through-hole |
| SBH11-PBPC-D10-ST-BK | 20-pin box header (10x2), straight, black |
| NPPN101BFCN-RC | 10-pin header, through-hole |

---

## Related Files

- Handler: `manufacturers/SullinsHandler.java`
- Supported types: `CONNECTOR`, `IC`
- No manufacturer-specific ComponentType enum entries

---

## Learnings & Edge Cases

- **Row count encoding**: For PPPC/PRPC/NPPN, the digit after the pin count indicates row count (1=single, 2=dual).
- **SBH/SFH always dual**: Box headers and FFC connectors are always dual row. Pin count in MPN is per-row, multiply by 2.
- **Pitch by series**: SBH/PPPC/PRPC/NPPN are 2.54mm pitch. SFH is 1.27mm pitch (fine pitch FFC).
- **Right angle detection**: Look for "RA" in package code OR in the dash-separated fields. Beware: "stRAight" contains "RA".
- **Color codes**: BK=Black, GY=Gray, WH=White, BL=Blue appear at the end of SBH/SFH MPNs.
- **Dual connector type**: Handler registers both CONNECTOR and IC types.

<!-- Add new learnings above this line -->
