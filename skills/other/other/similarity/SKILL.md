---
name: similarity
description: Use when working with component similarity calculations - comparing MPNs, finding equivalent parts, implementing new similarity calculators, or understanding how component matching works.
---

# Component Similarity Calculator Skill

This skill provides guidance for working with component similarity calculators in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

Similarity calculators determine how similar two electronic components are based on their MPNs (Manufacturer Part Numbers). They return a value between 0.0 (completely different) and 1.0 (identical or equivalent).

## Core Interfaces

### SimilarityCalculator (Simple)
```java
public interface SimilarityCalculator {
    double calculateSimilarity(String normalizedMpn1, String normalizedMpn2);
}
```
Used for generic calculators that don't need component type context.

### ComponentSimilarityCalculator (Type-Aware)
```java
public interface ComponentSimilarityCalculator {
    boolean isApplicable(ComponentType type);
    double calculateSimilarity(String mpn1, String mpn2, PatternRegistry registry);
}
```
Used for component-specific calculators that need to check applicability.

## Standard Similarity Thresholds

```java
private static final double HIGH_SIMILARITY = 0.9;    // Equivalent/interchangeable
private static final double MEDIUM_SIMILARITY = 0.7;  // Similar, may work as substitute
private static final double LOW_SIMILARITY = 0.3;     // Same category but different specs
```

## Available Calculators

| Calculator | Interface | Component Types | Key Features |
|------------|-----------|-----------------|--------------|
| `ResistorSimilarityCalculator` | Component | RESISTOR, RESISTOR_* | Value, package, tolerance |
| `CapacitorSimilarityCalculator` | Component | CAPACITOR, CAPACITOR_* | Value, voltage, dielectric |
| `TransistorSimilarityCalculator` | Component | TRANSISTOR, TRANSISTOR_* | NPN/PNP polarity, equivalent groups |
| `DiodeSimilarityCalculator` | Component | DIODE, DIODE_* | Signal/rectifier/zener types |
| `MosfetSimilarityCalculator` | Component | MOSFET, MOSFET_* | N/P channel, equivalent groups |
| `OpAmpSimilarityCalculator` | Component | OPAMP, OPAMP_* | Single/dual/quad, equivalent families |
| `VoltageRegulatorSimilarityCalculator` | Component | VOLTAGE_REGULATOR* | Fixed (78xx) vs adjustable (LM317) |
| `LogicICSimilarityCalculator` | Component | LOGIC_IC, IC | 74xx/CD4000 series, function groups |
| `LEDSimilarityCalculator` | Component | LED, LED_* | Color, bins, families |
| `MemorySimilarityCalculator` | Component | MEMORY, MEMORY_* | I2C/SPI EEPROM, Flash equivalents |
| `SensorSimilarityCalculator` | Component | SENSOR, TEMPERATURE_SENSOR, ACCELEROMETER | Sensor families, package variants |
| `ConnectorSimilarityCalculator` | Component | CONNECTOR, CONNECTOR_* | Pin count, pitch, family |
| `MicrocontrollerSimilarityCalculator` | Component | MICROCONTROLLER* | Series, package, manufacturer |
| `MCUSimilarityCalculator` | Simple | (generic) | Family, series, features |
| `PassiveComponentCalculator` | Simple | (generic) | Value, size code, tolerance |
| `LevenshteinCalculator` | Simple | (generic) | String edit distance |
| `DefaultSimilarityCalculator` | Simple | (generic) | Prefix, numeric, suffix weights |

## Creating a New Similarity Calculator

### 1. Implement the Interface

```java
public class NewComponentSimilarityCalculator implements ComponentSimilarityCalculator {
    private static final double HIGH_SIMILARITY = 0.9;
    private static final double MEDIUM_SIMILARITY = 0.7;
    private static final double LOW_SIMILARITY = 0.3;

    @Override
    public boolean isApplicable(ComponentType type) {
        if (type == null) return false;
        return type == ComponentType.NEW_COMPONENT ||
               type.name().startsWith("NEW_COMPONENT_");
    }

    @Override
    public double calculateSimilarity(String mpn1, String mpn2, PatternRegistry registry) {
        if (mpn1 == null || mpn2 == null) return 0.0;

        // Check if both are the component type we handle
        if (!isComponentType(mpn1) || !isComponentType(mpn2)) {
            return 0.0;
        }

        // Compare components
        // ...
        return similarity;
    }
}
```

### 2. Key Design Principles

1. **Return 0.0 for null inputs** - Always check for null MPNs and registry
2. **Return 0.0 for non-matching types** - If the MPN isn't your component type
3. **Use equivalent groups** - Define known equivalent parts (e.g., 2N2222 ≈ PN2222)
4. **Consider package variants** - Same part in different package should be high similarity
5. **Ensure symmetry** - `sim(A,B) == sim(B,A)`
6. **Keep in [0.0, 1.0]** - Never return values outside this range

### 3. Common Patterns

#### Equivalent Groups
```java
private static final Map<String, Set<String>> EQUIVALENT_GROUPS = new HashMap<>();
static {
    EQUIVALENT_GROUPS.put("2N2222", Set.of("2N2222", "2N2222A", "PN2222", "PN2222A"));
}

private boolean areEquivalent(String mpn1, String mpn2) {
    for (Set<String> group : EQUIVALENT_GROUPS.values()) {
        if (group.contains(mpn1) && group.contains(mpn2)) {
            return true;
        }
    }
    return false;
}
```

#### Package Code Extraction
```java
private String extractBasePart(String mpn) {
    // Remove common package suffixes
    return mpn.replaceAll("(?:CT|T|N|P|DG|PW|DR)$", "");
}
```

#### Polarity/Type Checking
```java
private boolean areSamePolarity(String mpn1, String mpn2) {
    boolean isNPN1 = NPN_PATTERNS.stream().anyMatch(mpn1::matches);
    boolean isNPN2 = NPN_PATTERNS.stream().anyMatch(mpn2::matches);
    return isNPN1 == isNPN2;
}
```

## Testing

### Test Structure
```java
@Nested
@DisplayName("isApplicable tests")
class IsApplicableTests { /* ... */ }

@Nested
@DisplayName("Equivalent groups tests")
class EquivalentGroupTests { /* ... */ }

@Nested
@DisplayName("Edge cases and null handling")
class EdgeCaseTests { /* ... */ }

@Nested
@DisplayName("Symmetry and property tests")
class PropertyTests { /* ... */ }
```

### Run Tests
```bash
# All similarity calculator tests
mvn test -Dtest="*SimilarityCalculatorTest,PassiveComponentCalculatorTest"

# Specific calculator
mvn test -Dtest=TransistorSimilarityCalculatorTest
```

## Related Skills

- `/similarity-resistor` - Resistor similarity details
- `/similarity-transistor` - Transistor equivalent groups and polarity
- `/similarity-mosfet` - MOSFET N/P channel comparison
- `/similarity-opamp` - Op-amp families and equivalents
- `/similarity-memory` - Memory IC equivalents (I2C/SPI EEPROM, Flash)
- `/similarity-sensor` - Sensor family comparison
- `/similarity-led` - LED bins and color temperature
- `/similarity-regulator` - Voltage regulator comparison (78xx, LM317)
- `/similarity-logic` - Logic IC function groups (74xx, CD4000)

---

## Metadata-Driven Architecture (January 2026)

The similarity system now uses a **metadata-driven architecture** for configurable, type-specific similarity rules.

**Conversion Status**: 12 of 17 calculators converted (71% complete)

| Calculator | Status | PR | Conversion Date |
|-----------|--------|-----|-----------------|
| ResistorSimilarityCalculator | ✅ Converted | - | Jan 2026 |
| CapacitorSimilarityCalculator | ✅ Converted | - | Jan 2026 |
| TransistorSimilarityCalculator | ✅ Converted | - | Jan 2026 |
| DiodeSimilarityCalculator | ✅ Converted | - | Jan 2026 |
| MosfetSimilarityCalculator | ✅ Converted | - | Jan 2026 |
| VoltageRegulatorSimilarityCalculator | ✅ Converted | - | Jan 2026 |
| OpAmpSimilarityCalculator | ✅ Converted | #116 | Jan 2026 |
| MemorySimilarityCalculator | ✅ Converted | #117 | Jan 2026 |
| LEDSimilarityCalculator | ✅ Converted | #118 | Jan 2026 |
| ConnectorSimilarityCalculator | ✅ Converted | (pre-existing) | Jan 2026 |
| LogicICSimilarityCalculator | ✅ Converted | #119 | Jan 2026 |
| SensorSimilarityCalculator | ✅ Converted | #120 | Jan 2026 |
| MicrocontrollerSimilarityCalculator | ⏳ Legacy | - | - |
| MCUSimilarityCalculator | ⏳ Legacy | - | - |
| PassiveComponentCalculator | ⏳ Legacy | - | - |
| LevenshteinCalculator | ⏳ Legacy | - | - |
| DefaultSimilarityCalculator | ⏳ Legacy | - | - |

### Core Metadata Classes

| Class | Purpose |
|-------|---------|
| `ComponentTypeMetadata` | Defines specs, importance levels, tolerance rules per component type |
| `ComponentTypeMetadataRegistry` | Singleton registry mapping ComponentType → metadata |
| `SpecImportance` | Enum: CRITICAL (1.0), HIGH (0.7), MEDIUM (0.4), LOW (0.2), OPTIONAL (0.0) |
| `ToleranceRule` | Interface for comparing spec values (ExactMatch, Percentage, MinRequired, MaxAllowed, Range) |
| `SimilarityProfile` | Context-aware profiles (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, PERFORMANCE_UPGRADE, EMERGENCY_SOURCING) |

### Retrieving Metadata

```java
ComponentTypeMetadataRegistry registry = ComponentTypeMetadataRegistry.getInstance();

// Get metadata for a component type
Optional<ComponentTypeMetadata> metadata = registry.getMetadata(ComponentType.RESISTOR);

// Query specs
if (metadata.isPresent()) {
    ComponentTypeMetadata meta = metadata.get();

    // Check if spec is critical
    boolean critical = meta.isCritical("resistance"); // true

    // Get tolerance rule for a spec
    SpecConfig config = meta.getSpecConfig("resistance");
    if (config != null) {
        ToleranceRule rule = config.getToleranceRule();
        SpecImportance importance = config.getImportance();
    }

    // Get all configured specs
    Set<String> allSpecs = meta.getAllSpecs();
}
```

### Pre-Registered Types (10)

RESISTOR, CAPACITOR, MOSFET, TRANSISTOR, DIODE, OPAMP, MICROCONTROLLER, MEMORY, LED, CONNECTOR

Each type has:
- Critical specs (must match for similarity)
- High/Medium/Low importance specs (contribute to score)
- Tolerance rules (how to compare values)
- Default similarity profile

### Context-Aware Profiles

Adjust importance multipliers based on use case:

| Profile | Threshold | CRITICAL | HIGH | MEDIUM | LOW | Use Case |
|---------|-----------|----------|------|--------|-----|----------|
| DESIGN_PHASE | 0.85 | 1.0 | 0.9 | 0.7 | 0.4 | Exact match for new designs |
| REPLACEMENT | 0.75 | 1.0 | 0.7 | 0.4 | 0.2 | **Default**: Direct replacement |
| COST_OPTIMIZATION | 0.60 | 1.0 | 0.4 | 0.2 | 0.0 | Maintain critical specs only |
| EMERGENCY_SOURCING | 0.50 | 0.8 | 0.4 | 0.2 | 0.0 | Urgent, relaxed requirements |

```java
// Check if similarity meets threshold for a profile
SimilarityProfile profile = SimilarityProfile.REPLACEMENT;
double similarity = 0.78;
boolean passes = profile.meetsThreshold(similarity); // true

// Get effective weight for a spec
double effectiveWeight = profile.getEffectiveWeight(SpecImportance.HIGH); // 0.7 × 0.7 = 0.49
```

### Converted Calculator Implementation Pattern

Calculators converted to metadata-driven approach follow this pattern:

```java
@Override
public double calculateSimilarity(String mpn1, String mpn2, PatternRegistry registry) {
    if (mpn1 == null || mpn2 == null) return 0.0;

    // Try metadata-driven approach first
    Optional<ComponentTypeMetadata> metadataOpt = metadataRegistry.getMetadata(ComponentType.OPAMP);
    if (metadataOpt.isPresent()) {
        logger.trace("Using metadata-driven similarity calculation");
        return calculateMetadataDrivenSimilarity(mpn1, mpn2, metadataOpt.get());
    }

    // Fallback to legacy pattern-based approach
    logger.trace("No metadata found, using legacy approach");
    return calculateLegacySimilarity(mpn1, mpn2);
}

private double calculateMetadataDrivenSimilarity(String mpn1, String mpn2, ComponentTypeMetadata metadata) {
    SimilarityProfile profile = metadata.getDefaultProfile();

    // Extract specs from MPNs
    String config1 = extractConfiguration(mpn1);  // e.g., "dual", "quad"
    String config2 = extractConfiguration(mpn2);
    // ... extract other specs

    // Short-circuit check for CRITICAL incompatibility
    if (!config1.isEmpty() && !config2.isEmpty() && !config1.equals(config2)) {
        return LOW_SIMILARITY;
    }

    double totalScore = 0.0;
    double maxPossibleScore = 0.0;

    // Compare each spec with weighted scoring
    ComponentTypeMetadata.SpecConfig configSpec = metadata.getSpecConfig("configuration");
    if (configSpec != null && !config1.isEmpty() && !config2.isEmpty()) {
        ToleranceRule rule = configSpec.getToleranceRule();
        SpecValue<String> orig = new SpecValue<>(config1, SpecUnit.NONE);
        SpecValue<String> cand = new SpecValue<>(config2, SpecUnit.NONE);

        double specScore = rule.compare(orig, cand);
        double specWeight = profile.getEffectiveWeight(configSpec.getImportance());

        totalScore += specScore * specWeight;
        maxPossibleScore += specWeight;
    }

    // Repeat for other specs (family, package, etc.)
    // ...

    double similarity = maxPossibleScore > 0 ? totalScore / maxPossibleScore : 0.0;

    // Apply boosts for equivalent groups
    if (areEquivalentParts(mpn1, mpn2)) {
        similarity = Math.max(similarity, HIGH_SIMILARITY);
    }

    return similarity;
}
```

**Key Features of Converted Calculators:**
1. **Dual-path approach** - Try metadata first, fall back to legacy
2. **Short-circuit checks** - Early return for CRITICAL spec mismatches
3. **Weighted scoring** - `totalScore / maxPossibleScore` formula
4. **Spec extraction** - Component-specific methods to extract values from MPNs
5. **Equivalent boost** - Apply known equivalence rules after scoring
6. **Profile support** - Use `getEffectiveWeight()` for context-aware weights

### Converted Calculator Specs

| Calculator | Critical Specs | High Importance | Medium Importance | Low Importance |
|-----------|----------------|-----------------|-------------------|----------------|
| **OpAmp** | configuration | family | package | - |
| **Memory** | memoryType, capacity | interface | - | package |
| **LED** | color | family, brightness | - | package |
| **Connector** | pinCount, pitch | family | mountingType | - |
| **LogicIC** | function | series, technology | - | package |
| **Sensor** | sensorType | family | interface | package |

### Migration Path

**For converting existing calculators:**
1. Add imports: `SimilarityProfile`, `ToleranceRule`, `SpecUnit`, `SpecValue`
2. Modify `calculateSimilarity()` to check for metadata first
3. Implement `calculateMetadataDrivenSimilarity()` method
4. Add spec extraction helper methods
5. Update tests to use threshold assertions (`>= HIGH_SIMILARITY`)
6. Run full test suite to verify backward compatibility

**For new calculators:**
1. Start with metadata-driven approach from the beginning
2. Define specs in `ComponentTypeMetadataRegistry`
3. Implement spec extraction methods
4. Use `SpecValue` wrapper for type-safe comparison
5. Apply context-aware profiles with `SimilarityProfile`

See CLAUDE.md § "Metadata-Driven Similarity Framework" for complete architecture details.

---

## Learnings & Quirks

### General Patterns
- Always normalize MPNs to uppercase before comparison
- Package suffixes vary by manufacturer - don't assume consistency
- Some calculators return HIGH_SIMILARITY (0.9) for identical parts, not 1.0

### Edge Cases
- Parts starting with digits (e.g., "2N2222") need special regex handling - `^[A-Za-z]+` won't match
- Some MPNs have significant hyphens (Molex) vs decorative hyphens (TI)
- Reel/tape suffixes (-RL, -T, -TR) should generally be ignored

### Metadata System Gotchas (January 2026)

**SpecValue Instantiation**:
```java
// NO static factory - use constructor
SpecValue<Double> v = new SpecValue<>(100.0, SpecUnit.FARAD); // ✓
SpecValue<Double> v = SpecValue.of(100.0); // ✗ Does not exist
```

**API Return Types**:
```java
// Registry returns Optional, metadata methods return direct values
Optional<ComponentTypeMetadata> meta = registry.getMetadata(type); // Optional
SpecConfig config = metadata.getSpecConfig("resistance"); // Can be null
boolean critical = metadata.isCritical("resistance"); // false if not found
```

**Singleton Side Effects**:
- Registry is shared across all tests
- Custom registrations persist
- Use unregistered types (CRYSTAL, FUSE) for tests, not RESISTOR/CAPACITOR

**Profile Multiplier Values**:
- COST_OPTIMIZATION maintains CRITICAL=1.0 (safety specs never compromised)
- EMERGENCY_SOURCING relaxes CRITICAL to 0.8 (only for urgent scenarios)

**Builder Validation**:
```java
ComponentTypeMetadata.builder(null).build(); // IllegalArgumentException
ComponentTypeMetadata.builder(ComponentType.IC).build(); // IllegalStateException (no specs)
```

<!-- Add new learnings above this line -->

---

## See Also

### Advanced Skills
- `/similarity-calculator-architecture` - Calculator registration, ordering, and the OpAmp IC interception bug
- `/metadata-driven-similarity-conversion` - Converting calculators to metadata-driven approach
- `/component-spec-extraction` - How to extract specs from MPNs for comparison
- `/equivalent-group-identification` - Hardcoded equivalent groups across calculators
