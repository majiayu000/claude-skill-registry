---
name: jinling
description: Jinling (JILN) connector MPN encoding, position-based part numbering for pin headers, female headers, and IDC connectors.
---

# Jinling (JILN) Manufacturer Skill

## Company Overview

**Full Name**: Shenzhen Jinling Electronics Co., Ltd.
**Brand**: JILN (Jiln)
**Founded**: 2004
**Website**: szjiln.en.made-in-china.com, jilnconnector.com
**Specialization**: Pin headers, female headers, board-to-board connectors, IDC, terminal blocks
**Patents**: 280+ independent innovation patents

## MPN Encoding Systems

Jinling uses **two different** MPN numbering systems:

### 1. Elprint Position-Based Encoding (15 characters)

```
27 31 0 2 02 A N G3 S U T
│  │  │ │ │  │ │ │  │ │ └─ [14] Packing
│  │  │ │ │  │ │ │  │ └─── [13] ContactType
│  │  │  │ │  │ │ │  └───── [12] ConnectorType
│  │  │ │ │  │ │ └─────── [10-11] ContactPlating
│  │  │ │ │  │ └────────── [9] Post
│  │  │ │ │  └─────────── [8] InsulatorMaterial
│  │  │ │ └──────────── [6-7] PinsPerRow (numeric)
│  │  │ └────────────── [5] Rows (1/2/3)
│  │  └──────────────── [4] HouseCount (usually 0)
│  └─────────────────── [2-3] PlasticsHeight × 10 (31 = 3.1mm)
└────────────────────── [0-1] Family (13/16/17/26/27)
```

**Total Length**: 15 characters (fixed)

### 2. JILN Distributor Format (15-18 characters)

Used on LCSC, JLCPCB, and other distributor platforms.

```
321010MG0CBK00A02
│││││││││││││││└┴─ Suffix codes (variant/packaging)
││││││││││││└┴──── Additional encoding
│││││││││││└────── K = Black color
││││││││││└─────── B = Material/housing
│││││││││└──────── C = Series/family code
││││││││└───────── 0 = Placeholder
│││││││└────────── G = Gold plating
││││││└─────────── M = SMT mounting
││││└┴──────────── 10 = Pin count (2x5=10)
│││└───────────── 1 = Rows
││└────────────── 2 = Pitch indicator (2.54mm)
└┴─────────────── 32 = Family/series (IDC)
```

---

## Elprint Format Reference Tables

### Family Codes (Positions 0-1)

| Code | Type | Pitch | Gender | Description |
|------|------|-------|--------|-------------|
| 13 | Pin Header | 1.27mm | Male | Fine pitch headers |
| 16 | Pin Header | 2.00mm | Male | Standard headers |
| 17 | Pin Header | 2.54mm | Male | Standard 0.1" headers |
| 26 | Female Header | 2.00mm | Female | Socket/receptacle |
| 27 | Female Header | 2.54mm | Female | Standard 0.1" sockets |

### Plastics Height (Positions 2-3)

Encoded as height in mm × 10:
- `31` = 3.1mm
- `35` = 3.5mm
- `85` = 8.5mm

Formula: `height_mm = parseInt(positions[2:4]) * 0.1`

### House Count (Position 4)

Always `0` for current Jinling products.

### Rows (Position 5)

- `1` = Single row
- `2` = Dual row
- `3` = Triple row

### Pins Per Row (Positions 6-7)

**MUST be numeric** (e.g., `02`, `10`, `20`, `40`).

Pin count calculation: `rows × pinsPerRow`

Examples:
- `1` row × `40` pins = 40 total
- `2` rows × `20` pins = 40 total
- `2` rows × `02` pins = 4 total

### Insulator Material (Position 8)

| Code | Material | Full Name |
|------|----------|-----------|
| A | PBT | Polybutylene Terephthalate |
| B | PA66 | Polyamide 66 (Nylon 66) |
| C | PA6T | Polyamide 6T |
| D | PA46 | Polyamide 46 |
| E | PA9T | Polyamide 9T |
| F | LCP | Liquid Crystal Polymer |

### Post (Position 9)

| Code | Meaning |
|------|---------|
| W | With post/standoff |
| N | Without post |

### Contact Plating (Positions 10-11)

| Code | Plating | Thickness |
|------|---------|-----------|
| SN | Tin | - |
| G0 | Gold Flash | < 1µin |
| G1 | Gold | 3µin |
| G2 | Gold | 5µin |
| G3 | Gold | 10µin |
| G4 | Gold | 15µin |
| G5 | Gold | 30µin |
| S0 | Gold Flash/Tin | Mixed |

### Connector Type (Position 12)

| Code | Type | Description |
|------|------|-------------|
| M | SMT | Surface Mount |
| S | Straight THT | 180° through-hole |
| R | Right Angle THT | 90° through-hole |
| W | Straddle THT | Straddle mount |
| Z | Right Angle SMT | 90° surface mount |

### Contact Type (Position 13)

| Code | Type |
|------|------|
| U | U-Type |
| S | Straight |
| R | Right Angle |

### Packing (Position 14)

| Code | Package Type |
|------|-------------|
| T | Tube |
| P | Tube + Cap |
| R | Reel |
| O | PE Bag |
| A | Tray |

---

## Example MPN Decoding

### Example 1: 27310202ANG3SUT

```
27 31 0 2 02 A N G3 S U T
│  │  │ │ │  │ │ │  │ │ └─ T = Tube packing
│  │  │ │ │  │ │ │  │ └─── U = U-Type contact
│  │  │ │ │  │ │ │  └───── S = Straight THT
│  │  │ │ │  │ │ └─────── G3 = 10µin Gold
│  │  │ │ │  │ └────────── N = No post
│  │  │ │ │  └─────────── A = PBT material
│  │  │ │ └──────────── 02 = 2 pins per row
│  │  │ └────────────── 2 = Dual row
│  │  └──────────────── 0 = No houses
│  └─────────────────── 31 = 3.1mm height
└────────────────────── 27 = Female Header (2.54mm pitch)
```

**Decoded**: 2.54mm female header, 2 rows × 2 pins = 4 total, 3.1mm height, PBT, no post, 10µin gold plating, straight THT, U-type contacts, tube packing

### Example 2: 17310140ANSNSUT

```
17 31 0 1 40 A N SN S U T
```

**Decoded**: 2.54mm pin header (male), 1 row × 40 pins = 40 total, 3.1mm height, PBT, no post, tin plating, straight THT, U-type contacts, tube packing

---

## Distributor Format Examples

Real Jinling part numbers from LCSC:

| MPN | Description | LCSC ID |
|-----|-------------|---------|
| 321010MG0CBK00A02 | IDC 2x5P (10 pins) 2.54mm SMT Gold | C601966 |
| 12251140CNG0S115001 | Pin Header 1x40P 2.54mm THT | C429959 |
| 12251220ANG0S115001 | Pin Header 2x20P 2.54mm THT | C429965 |
| 22850120ANG1SYA01 | Female Header 2.54mm | C429947 |
| 22850102ANG1SYA02 | Female Header 2.54mm | C429966 |
| 13201140CNG0S087004 | Pin Header 1.27mm 1x40P | C429955 |

---

## Handler Implementation Notes

### Pattern Matching

Elprint format requires:
- **Exactly 15 characters**
- Family code: `13`, `16`, `17`, `26`, or `27`
- Positions 2-7 must be numeric

```java
// Elprint pattern (15 chars)
^(?:13|16|17|26|27)[0-9]{4}[0-9]{2}[A-Z][A-Z]{2}[A-Z]{3}$

// Distributor patterns
^32[0-9]{4}[A-Z]{2}[0-9][A-Z]{3}[0-9]{2}[A-Z][0-9]{2}  // IDC
^1[0-9]{4}[0-9]{3,4}[A-Z]{3}[0-9][A-Z][0-9]{6,7}       // Pin headers (12xxx)
^22[0-9]{3}[0-9]{3,4}[A-Z]{3}[0-9][A-Z]{3}[A-Z][0-9]{2} // Female headers
```

### Position-Based Extraction

**CRITICAL**: Always validate MPN length before substring operations!

```java
private boolean isElprintFormat(String mpn) {
    if (mpn == null || mpn.length() < 15) return false;

    String family = mpn.substring(0, 2);
    boolean isKnownFamily = "13".equals(family) || "16".equals(family) ||
                           "17".equals(family) || "26".equals(family) ||
                           "27".equals(family);

    // Positions 2-7 must be numeric
    boolean hasNumericPrefix = mpn.substring(2, 6).matches("[0-9]+") &&
                              mpn.substring(6, 8).matches("[0-9]+");

    return isKnownFamily && hasNumericPrefix;
}
```

### Pin Count Calculation

```java
public int extractPinCount(String mpn) {
    if (!isElprintFormat(mpn)) return 0;

    try {
        int rows = Character.getNumericValue(mpn.charAt(5));
        int pinsPerRow = Integer.parseInt(mpn.substring(6, 8));
        return rows * pinsPerRow;
    } catch (NumberFormatException e) {
        return 0;
    }
}
```

### Package Code Extraction

```java
public String extractPackageCode(String mpn) {
    if (!isElprintFormat(mpn) || mpn.length() < 13) return "";

    String typeCode = mpn.substring(12, 13);
    return CONNECTOR_TYPES.getOrDefault(typeCode, typeCode);
}
```

### Official Replacement Logic

Components are interchangeable if:
1. Same family (e.g., both 27)
2. Same pin count
3. Compatible mounting types (both SMT or both THT)

Different plating, material, or packing are acceptable variations.

---

## Related Files

- **Handler**: `src/main/java/no/cantara/electronic/component/lib/manufacturers/JinlingHandler.java` (~560 lines)
- **Tests**: `src/test/java/no/cantara/electronic/component/lib/handlers/JinlingHandlerTest.java` (~550 lines, 131 tests)
- **Component Types**: `CONNECTOR`, `CONNECTOR_JINLING`
- **Manufacturer Enum**: `ComponentManufacturer.JINLING`

---

## Known Issues & Edge Cases

### Test MPN Format Issue (RESOLVED)

**Problem**: Initial test MPNs used 13-17 character format instead of required 15 characters.

**Example**:
- ❌ Wrong: `273102NSNSUXT` (13 chars with non-numeric positions)
- ❌ Wrong: `27310202ASNSUTT` (17 chars)
- ❌ Wrong: `17310110AG3SUT` (14 chars - missing post indicator)
- ✅ Correct: `27310202ANG3SUT` (15 chars, all numeric in positions 2-7)

**Resolution**: All 131 tests now use proper 15-character elprint format. Handler pattern enforces exact length validation with `length() != 15` check.

### Handler Pattern Conflicts

The handler registers patterns for **both** encoding systems:
- Elprint: Families 13/16/17/26/27
- Distributor: Families 12/22/32/35

Ensure ComponentManufacturer.JINLING pattern covers both:
```java
JINLING("(?:1[2367]|2[267]|3[25])[0-9]{4,}", "Shenzhen Jinling Electronics", new JinlingHandler())
```

### Position-Based Extraction Gotchas

1. **Always check MPN length** before substring - prevents IndexOutOfBoundsException
2. **Positions 6-7 MUST be numeric** - test MPNs with letters like "NS" will fail
3. **Position 14 is single character** for packing, not two
4. **Default to 0/empty** when extraction fails - graceful degradation

### Cross-Handler Pattern Matching

Jinling patterns (`^13...`, `^17...`) could conflict with other manufacturers using similar prefixes. The `matches()` method includes explicit family checks to prevent false positives.

---

## Test Examples

### Stable Pattern Matching Tests

```java
@Test
void shouldMatchElprintFormat() {
    assertTrue(handler.matches("27310202ANG3SUT", ComponentType.CONNECTOR, registry));
    assertTrue(handler.matches("17310140ANSNSUT", ComponentType.CONNECTOR, registry));
}

@Test
void shouldMatchDistributorFormat() {
    assertTrue(handler.matches("321010MG0CBK00A02", ComponentType.CONNECTOR, registry));
    assertTrue(handler.matches("12251140CNG0S115001", ComponentType.CONNECTOR, registry));
}
```

### Extraction Tests

```java
@Test
void shouldExtractPinCount() {
    assertEquals(4, handler.extractPinCount("27310202ANG3SUT"));   // 2×2=4
    assertEquals(40, handler.extractPinCount("17310140ANSNSUT"));  // 1×40=40
    assertEquals(80, handler.extractPinCount("27310240ANSNSUT"));  // 2×40=80
}

@Test
void shouldExtractPackageCode() {
    assertEquals("SMT", handler.extractPackageCode("27310202MNSNSUT"));
    assertEquals("Straight THT", handler.extractPackageCode("27310202ANSNSUT"));
    assertEquals("Right Angle THT", handler.extractPackageCode("27310202ARSNRUT"));
}
```

---

## Future Improvements

1. ~~**Test MPN Format**: Update all test MPNs to proper 15-character elprint format~~ ✓ COMPLETED
2. **Distributor MPN Decoding**: Implement full parsing for LCSC/JLCPCB format MPNs (partially done - pin count extraction works)
3. **Layout Variants**: Add support for optional [15-16] layout codes (TYPE 01, TYPE 02)
4. **IDC Connector Family (32)**: Expand handler to include full IDC connector support (basic pattern matching works)
5. **Validation**: Add MPN format validator to detect malformed part numbers

---

## Learnings & Quirks

- **Two Encodings**: Jinling uses both internal (elprint) and external (distributor) MPN formats
- **Fixed Length**: Elprint format is **exactly 15 characters**, not variable length
- **Numeric Pins**: Positions 6-7 must be numeric digits, not letters
- **Family Determines Type**: Family code determines gender (13/16/17=male, 26/27=female) and pitch
- **Position 12 Critical**: Connector type (M/S/R/W/Z) determines mounting style and orientation
- **Gold Plating Grades**: G0-G5 represent different gold thicknesses (flash to 30µin)
- **Real-World MPNs**: LCSC uses distributor format (18 chars), not elprint format (15 chars)
- **Position Misalignment**: Test failures often indicate wrong position encoding (e.g., connector type at pos 8 instead of 12)
- **Missing Characters**: 14-char MPNs usually missing post indicator 'N' at position 9
- **Pattern Validation**: Use `length() != 15` not `length() < 15` to catch both too short AND too long MPNs
- **Substring Safety**: Always validate length before `substring(6,8)` operations to prevent IndexOutOfBoundsException

<!-- Add new learnings above this line -->
