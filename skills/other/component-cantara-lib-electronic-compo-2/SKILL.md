---
name: component
description: Base skill for working with electronic components in this library. Use when adding new component types, manufacturer handlers, or working with MPN (Manufacturer Part Number) operations, BOM entries, or component classification.
---

# Electronic Component Skill

This skill provides guidance for working with electronic components in the lib-electronic-components library.

## Core Concepts

### Component Type Hierarchy

Components are classified using `ComponentType` enum with two levels:
- **Base types**: `RESISTOR`, `CAPACITOR`, `MOSFET`, `OPAMP`, etc.
- **Manufacturer-specific types**: `MOSFET_INFINEON`, `CAPACITOR_CERAMIC_MURATA`, etc.

Use `getBaseType()` to map specific types to their base type.

### Key Classes

| Class | Purpose |
|-------|---------|
| `ComponentType` | Enum of ~200 component types with passive/semiconductor flags |
| `ComponentManufacturer` | Enum of manufacturers with regex patterns |
| `ManufacturerHandler` | Interface for manufacturer-specific MPN parsing |
| `MPNUtils` | Static utilities for MPN normalization, similarity, type detection |
| `BOMEntry` | Component entry in a bill of materials |

## Adding a New Manufacturer Handler

1. Create handler in `src/main/java/no/cantara/electronic/component/lib/manufacturers/`:

```java
public class NewMfrHandler implements ManufacturerHandler {
    @Override
    public void initializePatterns(PatternRegistry registry) {
        registry.registerPattern(ComponentType.RESISTOR,
            Pattern.compile("^NMF[0-9]{4}.*", Pattern.CASE_INSENSITIVE));
    }

    @Override
    public String extractPackageCode(String mpn) { /* ... */ }

    @Override
    public String extractSeries(String mpn) { /* ... */ }

    @Override
    public boolean isOfficialReplacement(String mpn1, String mpn2) { return false; }

    @Override
    public Set<ManufacturerComponentType> getManufacturerTypes() { return Set.of(); }

    @Override
    public Set<ComponentType> getSupportedTypes() {
        return Set.of(ComponentType.RESISTOR);
    }
}
```

2. Add entry to `ComponentManufacturer` enum:

```java
NEW_MFR("(?:NMF)[0-9]", "New Manufacturer", new NewMfrHandler()),
```

## Adding a New Component Type

1. Add to `ComponentType` enum with passive/semiconductor flags:
```java
NEW_TYPE(false, true),  // (isPassive, isSemiconductor)
NEW_TYPE_MANUFACTURER(false, true),
```

2. Update `getBaseType()` switch to map specific types to base:
```java
case NEW_TYPE_INFINEON, NEW_TYPE_ST -> NEW_TYPE;
```

3. Add patterns in relevant manufacturer handlers

## MPN Operations

```java
// Normalize MPN (removes special characters)
String normalized = MPNUtils.normalize("LM358-N"); // "LM358N"

// Strip package suffix to get base part number
String base = MPNUtils.stripPackageSuffix("MAX3483EESA+"); // "MAX3483EESA"
String base2 = MPNUtils.stripPackageSuffix("LTC2053HMS8#PBF"); // "LTC2053HMS8"

// Generate search variations (for datasheet/component searches)
List<String> vars = MPNUtils.getSearchVariations("TJA1050T/CM,118");
// ["TJA1050T/CM,118", "TJA1050T"]

// Check component equivalence (ignoring package suffixes)
boolean equiv = MPNUtils.isEquivalentMPN("LTC2053HMS8#PBF", "LTC2053HMS8#TR"); // true

// Extract package suffix
Optional<String> suffix = MPNUtils.getPackageSuffix("MAX3483EESA+"); // Optional.of("+")

// Detect manufacturer
ComponentManufacturer mfr = ComponentManufacturer.fromMPN("STM32F103C8T6");

// Detect component type
ComponentType type = ComponentType.fromMPN("IRF540N"); // MOSFET

// Calculate similarity
double sim = MPNUtils.calculateSimilarity("LM358", "MC1458"); // 0.9
```

### Package Suffix Support

MPNUtils now supports manufacturer-specific package suffixes:
- **Maxim/AD**: `+` (lead-free) - e.g., `MAX3483EESA+`
- **Linear Tech**: `#PBF`, `#TR` (RoHS, Tape & Reel) - e.g., `LTC2053HMS8#PBF`
- **NXP**: `/CM,118` (ordering codes) - e.g., `TJA1050T/CM,118`
- **Various**: `,315` (ordering codes) - e.g., `NC7WZ04,315`

**Use cases:**
- Datasheet searches: Try both original and base MPN
- Component deduplication: Same base = same component
- BOM validation: Match supplier MPNs to design MPNs
- Inventory matching: Ignore packaging differences

## Similarity Calculators

Each component type can have a dedicated similarity calculator in `componentsimilaritycalculators/`:
- `ResistorSimilarityCalculator` - compares resistance values, tolerances, packages
- `CapacitorSimilarityCalculator` - compares capacitance, voltage, dielectric
- `MosfetSimilarityCalculator` - compares Vds, Rds(on), package
- etc.

Implement `ComponentSimilarityCalculator` interface and add to list in `MPNUtils`.

## Testing

Run component-related tests:
```bash
mvn test -Dtest=MPNUtilsTest
mvn test -Dtest=ComponentTypeDetectorTest
mvn test -Dtest=MPNExtractionTest
```

## Related Skills

Use specialized skills for specific component types:
- `/resistor` - Resistor patterns and value extraction
- `/capacitor` - Capacitor patterns and specifications
- `/semiconductor` - Diodes, transistors, MOSFETs
- `/ic` - Microcontrollers, op-amps, voltage regulators
- `/connector` - Connector manufacturer patterns
- `/memory` - Flash, EEPROM, RAM components

## See Also

### Advanced Skills
- `/handler-pattern-design` - Handler patterns, anti-patterns, and testing strategies
- `/mpn-normalization` - MPN suffix handling and normalization patterns
- `/component-type-detection-hierarchy` - Type hierarchy, specificity levels, getBaseType() mapping
- `/component-spec-extraction` - Spec extraction patterns and naming conventions
- `/manufacturer-detection-from-mpn` - Manufacturer regex patterns and detection ordering

### Documentation
- **HISTORY.md** - Handler bug patterns and fixes (PR #89, handler cleanup PRs #73-88)
- **.docs/history/HANDLER_IMPLEMENTATION_PATTERNS.md** - Detailed handler development patterns
- **.docs/history/BUG_FIX_ANALYSIS.md** - Critical bugs and prevention strategies

## Recording Learnings

**Important**: When you discover quirks, edge cases, or important patterns while working on components:

1. **General/cross-cutting learnings** → Add to `CLAUDE.md` under "Learnings & Quirks"
2. **Component-specific learnings** → Add to the relevant skill file below

Examples of what to record:
- MPN patterns that don't follow expected conventions
- Manufacturer-specific quirks in part numbering
- Edge cases in similarity calculation
- Test failures that revealed unexpected behavior
- Regex patterns that needed adjustment

---

## Learnings & Quirks

### Handler Patterns
- Use `registry.addPattern()` not `registry.registerPattern()` - the latter requires a compiled Pattern object
- Handler order in `ComponentManufacturer` enum affects detection priority for ambiguous MPNs

### MPN Edge Cases
- Some MPNs contain hyphens that are significant (e.g., Molex `43045-0212`) vs decorative (e.g., `LM358-N`)
- Yageo resistors: `RC0603FR-0710KL` - the `-07` is TCR code, not a separator

<!-- Add new learnings above this line -->
