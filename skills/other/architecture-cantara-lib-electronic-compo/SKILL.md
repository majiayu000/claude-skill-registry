---
name: architecture
description: Use when refactoring, cleaning up, or enhancing the lib-electronic-components codebase. Provides guidance on architecture patterns, known issues, duplication hotspots, and recommended improvements.
---

# Software Architecture Skill

This skill provides architectural guidance for enhancing and cleaning up the lib-electronic-components library.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ComponentType (Enum)                         │
│                    ~200 component types                         │
│         Base types (RESISTOR) + Specific (RESISTOR_CHIP_VISHAY) │
└────────────────────────┬────────────────────────────────────────┘
                         │ matched by
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              ComponentManufacturer (Enum)                       │
│                    50+ manufacturers                            │
│         Each holds: regex pattern + ManufacturerHandler         │
└────────────────────────┬────────────────────────────────────────┘
                         │ delegates to
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              ManufacturerHandler (Interface)                    │
│                    50+ implementations                          │
│     initializePatterns(), extractPackageCode(), extractSeries() │
└────────────────────────┬────────────────────────────────────────┘
                         │ populates
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                PatternRegistry (Class)                          │
│     Map<ComponentType, Map<Class<?>, Set<Pattern>>>            │
│              Multi-handler pattern storage                      │
└────────────────────────┬────────────────────────────────────────┘
                         │ used by
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│          ComponentSimilarityCalculator (Interface)              │
│                    20+ implementations                          │
│     Per-component-type similarity strategies                    │
└─────────────────────────────────────────────────────────────────┘
```

## Design Patterns In Use

| Pattern | Implementation | Location |
|---------|---------------|----------|
| Registry | `PatternRegistry` | Stores patterns by type and handler |
| Factory | `ManufacturerHandlerFactory` | Dynamic handler discovery |
| Strategy | `ComponentSimilarityCalculator` | Different algorithms per type |
| Enum Dispatch | `ComponentManufacturer` | Enum + handler association |
| Template Method | `ManufacturerHandler.matches()` | Default with override |

---

## Critical Issues to Fix

### RESOLVED ISSUES (PR #74, #75)

The following issues have been fixed:

1. **TIHandler Pattern Duplication** - FIXED
   - Removed ~170 lines of duplicate COMPONENT_SERIES entries
   - Fixed LM35/LM358 pattern conflict (LM35 sensors use letter suffix A-D)

2. **No Base Handler Class** - FIXED
   - Created `AbstractManufacturerHandler` with shared helper methods
   - Methods: `extractSuffixAfterHyphen()`, `extractTrailingSuffix()`, `findFirstDigitIndex()`, `findLastDigitIndex()`

3. **Package Code Duplication** - FIXED
   - Created `PackageCodeRegistry` with centralized mappings
   - Includes standard codes (N→DIP, D→SOIC) and Atmel-specific (PU→PDIP, AU→TQFP)

4. **Flaky Tests** - FIXED
   - Changed `ManufacturerHandlerFactory` from `HashSet` to `TreeSet` with deterministic ordering
   - Handler iteration order is now consistent across all test runs

5. **ComponentType.getManufacturer() Fragile** - FIXED
   - Was using string matching on manufacturer names (fragile)
   - Fixed with explicit `MANUFACTURER_SUFFIX_MAP` for special cases (ON→ON_SEMI, AD→ANALOG_DEVICES)
   - Direct enum `valueOf()` lookup for standard cases

6. **TIHandlerPatterns.java Unused** - FIXED (deleted)
   - File existed but was never used after TIHandler consolidation
   - Safely deleted

---

## Package Code Registry (IMPLEMENTED)

The `PackageCodeRegistry` class has been created to centralize package code mappings:

```java
// Usage in handlers:
String resolvedCode = PackageCodeRegistry.resolve("PU");  // Returns "PDIP"
boolean isKnown = PackageCodeRegistry.isKnownCode("N");   // Returns true
boolean isPower = PackageCodeRegistry.isPowerPackage("TO-220"); // Returns true
```

**Supported codes include**:
- Standard: N→DIP, D→SOIC, PW→TSSOP, DGK→MSOP, DBV→SOT-23
- Power: T→TO-220, KC→TO-252, MP→SOT-223
- Atmel-specific: PU→PDIP, AU→TQFP, MU→QFN, SU→SOIC, XU→TSSOP

**Next step**: Migrate existing handlers to use the registry instead of inline maps.

---

## Test Coverage Status (January 2026)

| Area | Files | With Tests | Gap | Priority |
|------|-------|------------|-----|----------|
| Handlers | 56 | 40 (71.4%) | 16 handlers | HIGH |
| Similarity Calculators | 20 | 0 (0%) | All untested | HIGH |
| PatternRegistry | 1 | 0 | No tests | MEDIUM |
| ManufacturerHandlerFactory | 1 | 0 | No tests | LOW |

**Handlers WITHOUT Tests (16)**:
Abracon, AKM, Cree, DiodesInc, Epson, Fairchild, IQD, LG, LogicIC, Lumileds, NDK, Nexteria, OSRAM, Qualcomm, Spansion, Unknown

**Similarity Calculators (ALL untested)**:
CapacitorSimilarityCalculator, ConnectorSimilarityCalculator, DiodeSimilarityCalculator, LEDSimilarityCalculator, MCUSimilarityCalculator, MemorySimilarityCalculator, MosfetSimilarityCalculator, OpAmpSimilarityCalculator, ResistorSimilarityCalculator, SensorSimilarityCalculator, TransistorSimilarityCalculator, VoltageRegulatorSimilarityCalculator, MicrocontrollerSimilarityCalculator, DefaultSimilarityCalculator, PassiveComponentCalculator, LevenshteinCalculator

**Priority tests to add**:

1. **Handler tests** - For each handler:
   ```java
   @Test void shouldDetectComponentType()
   @Test void shouldExtractPackageCode()
   @Test void shouldExtractSeries()
   @Test void shouldIdentifyReplacements()
   ```

2. **Pattern conflict tests**:
   ```java
   @Test void noTwoHandlersShouldClaimSameMPN()
   ```

3. **Similarity calculator tests**:
   ```java
   @Test void resistorsSameValueShouldBeHighSimilarity()
   @Test void differentComponentTypesShouldBeLowSimilarity()
   ```

---

## Refactoring Priorities

### COMPLETED (PR #74, #75)

- ~~Deduplicate TIHandler COMPONENT_SERIES~~ - Done, removed ~170 lines
- ~~Create AbstractManufacturerHandler~~ - Done
- ~~Create PackageCodeRegistry~~ - Done
- ~~Fix flaky tests (handler ordering)~~ - Done, uses TreeSet now

### Priority 1: High (Structural Improvements)

1. **Migrate handlers to use AbstractManufacturerHandler**
   - Many handlers still use duplicate helper methods
   - Files: `*Handler.java` in `manufacturers/`

2. **Migrate handlers to use PackageCodeRegistry**
   - Replace inline PACKAGE_CODES maps with registry calls
   - Files: `*Handler.java` in `manufacturers/`

3. ~~**Delete TIHandlerPatterns.java**~~ - DONE
   - Deleted unused file

### Priority 2: Medium (Quality Improvements)

4. **Add Handler Unit Tests**
   - Test each handler's pattern matching
   - New files: `*HandlerTest.java`

5. ~~**Fix ComponentType.getManufacturer()**~~ - DONE
   - Fixed with explicit MANUFACTURER_SUFFIX_MAP

6. **Add Similarity Calculator Tests**
   - Test each calculator
   - New files: `*SimilarityCalculatorTest.java`

### Priority 3: Low (Enhancements)

7. **Standardize Pattern Approaches**
   - Consistent regex style across handlers
   - All handlers in `manufacturers/`

---

## Technical Debt Inventory (January 2026)

### Production Debug Statements (181 total - HIGH priority)

| File | Count | Notes |
|------|-------|-------|
| MPNUtils.java | 35 | Heaviest concentration |
| ManufacturerHandlerFactory.java | 17 | Also has 8 printStackTrace() |
| ComponentTypeDetector.java | 17 | |
| ConnectorSimilarityCalculator.java | 16 | |
| Similarity calculators (combined) | 97 | All 13 calculators affected |

**Action**: Replace with SLF4J logging framework.

### printStackTrace() Calls (9 total - HIGH priority)

| File | Lines |
|------|-------|
| ManufacturerHandlerFactory.java | 56, 66, 110, 123, 149, 155, 186, 191 |
| MPNUtils.java | 298 |

**Action**: Replace with `logger.error("message", exception)`.

### Inconsistent getSupportedTypes() Pattern

| Pattern | Count | Handlers |
|---------|-------|----------|
| **Set.of() (modern)** | 28 | AtmelHandler, STHandler, TIHandler, BoschHandler, HiroseHandler, JSTHandler, MolexHandler, EspressifHandler, LogicICHandler, MaximHandler, PanasonicHandler, VishayHandler, etc. |
| **new HashSet() (legacy)** | 29 | CreeHandler, AbraconHandler, LGHandler, NordicHandler, etc. |

**Action**: Standardize all to Set.of() for immutability and conciseness.
**Note**: 5 handlers fixed in PR #89: EspressifHandler, LogicICHandler, MaximHandler, PanasonicHandler, VishayHandler

### Type/Pattern Registration Mismatches (Critical bugs)

| Handler | Issue | Status |
|---------|-------|--------|
| MaximHandler | Declared INTERFACE_IC_MAXIM, RTC_MAXIM, BATTERY_MANAGEMENT_MAXIM without patterns | ✅ FIXED (PR #89) |
| EspressifHandler | Declared ESP8266_SOC, ESP32_SOC, all module types but only registered MICROCONTROLLER | ✅ FIXED (PR #89) |
| PanasonicHandler | Declared capacitor/inductor types but no patterns registered | ✅ FIXED (PR #89) |

**Impact**: `matches()` returns false for declared types because patterns aren't registered.

**Fix pattern**: When adding a type to `getSupportedTypes()`, MUST also add patterns in `initializePatterns()`.

### Code Quality Issues

| File | Issue | Line(s) | Status |
|------|-------|---------|--------|
| LogicICHandler.java | Debug System.out.println in production code | 70, 75, 84, 85 | ✅ FIXED (PR #89) |
| EspressifHandler.java | NPE risk - substring without indexOf check | 153-154 | ✅ FIXED (PR #89) |
| InfineonHandler.java | Commented-out code blocks | 44, 49, 51 | Open |

### Magic Numbers in Scoring (108+ instances)

All similarity calculators use hardcoded weights:
```java
// Varies by calculator - no consistent values!
HIGH_SIMILARITY = 0.9
MEDIUM_SIMILARITY = 0.5-0.7  // Inconsistent!
LOW_SIMILARITY = 0.3

// Scoring increments vary wildly
valueMatch = 0.3-0.5
packageMatch = 0.2-0.4
```

**Action**: Extract to configurable SimilarityWeights constants class.

---

## Code Smell Indicators

When reviewing code, watch for:

| Smell | Example | Fix |
|-------|---------|-----|
| Duplicate Map.put() | Same key added twice | Remove duplicate |
| Hardcoded package codes | `return "TO-220"` | Use PackageCodeRegistry |
| Copy-pasted regex | Same pattern in 3 handlers | Extract to constant |
| Giant switch statement | 50+ cases | Use Map lookup |
| Unused ComponentSeriesInfo | Defined but never queried | Remove or use |

---

## File Reference Quick Guide

| Task | Primary Files |
|------|---------------|
| Add manufacturer | `ComponentManufacturer.java`, new `*Handler.java` |
| Add component type | `ComponentType.java`, handler `initializePatterns()` |
| Fix pattern matching | Handler's `matches()` method |
| Add similarity logic | New `*SimilarityCalculator.java`, register in `MPNUtils` |
| Debug MPN detection | `ComponentManufacturer.fromMPN()`, handler patterns |

---

## Learnings & Quirks

### Architecture Decisions
- `ComponentManufacturer` enum tightly couples manufacturer identity with handler - this is intentional for performance (single lookup)
- `PatternRegistry` supports multi-handler per type but this feature is largely unused
- Similarity calculators are registered in `MPNUtils` static initializer (lines 34-48)

### Critical Implementation Details

**Handler Ordering (PR #75)**:
- `ManufacturerHandlerFactory` MUST use `TreeSet` with deterministic comparator
- `HashSet` caused flaky tests because iteration order varied between runs
- First matching handler wins in `getManufacturerHandler()` - order is critical!

**Type Detection Specificity (PR #74)**:
- `MPNUtils.getComponentType()` uses specificity scoring via `getTypeSpecificityScore()`
- Manufacturer-specific types (OPAMP_TI) score +150, generic types (IC) score -50
- Without scoring, iteration order could return IC instead of OPAMP_TI

**ComponentType.getBaseType() Completeness**:
- All manufacturer-specific types MUST be in the switch statement
- Missing types fall through to `default -> this` (returns self, not base type)
- Fixed in PR #74: Added TRANSISTOR_VISHAY, TRANSISTOR_NXP, OPAMP_ON, OPAMP_NXP, OPAMP_ROHM

**ComponentType.getManufacturer() Mapping (PR #76)**:
- Uses explicit `MANUFACTURER_SUFFIX_MAP` for special cases (ON→ON_SEMI, AD→ANALOG_DEVICES, SILABS→SILICON_LABS, DIODES→DIODES_INC)
- Falls back to direct `ComponentManufacturer.valueOf(suffix)` for standard cases
- Much more reliable than previous string-contains matching

**Cross-Handler Pattern Matching (PR #90 - CRITICAL FIX)**:
- Default `ManufacturerHandler.matches()` was using `PatternRegistry.getPattern(type)` which returned the first pattern from ANY handler
- This caused false matches when handlers were tested in alphabetical order (e.g., CypressHandler before STHandler)
- Fix: Added `matchesForCurrentHandler()` to PatternRegistry that only checks patterns for the current handler
- **IMPORTANT**: 7 handlers had custom `matches()` overrides with the same bug (using `patterns.getPattern(type)` as fallback):
  - NXPHandler, FairchildHandler, OnSemiHandler, MaximHandler, KemetHandler, WinbondHandler, TIHandler
  - All fixed by replacing fallback with `patterns.matchesForCurrentHandler()`
- Key insight: If tests pass locally but fail in CI, check for HashMap iteration order differences

### Known Gotchas
- Handler order in `ComponentManufacturer` affects detection priority for ambiguous MPNs
- Some MPNs legitimately match multiple manufacturers (second-source parts)
- **Handlers with custom matches() overrides**: Must use `patterns.matchesForCurrentHandler()` NOT `patterns.getPattern(type)` for fallback matching
- **CI vs Local differences**: Usually caused by HashMap/HashSet iteration order - always use deterministic collections

### Historical Context
- CI test failures (pre-PR #75) were caused by non-deterministic HashSet iteration
- Test stability now achieved via TreeSet with class name comparator
- PR #90: Fixed cross-handler pattern matching that caused STM32 MPNs to match CypressHandler
- Some handlers have commented-out patterns (e.g., `ComponentManufacturer.java` lines 45-53) - unclear if deprecated or WIP

---

## See Also

### Advanced Skills
- `/handler-pattern-design` - Handler patterns, anti-patterns, and cleanup checklists
- `/similarity-calculator-architecture` - Calculator ordering and architectural patterns
- `/component-type-detection-hierarchy` - Type system architecture and specificity
- `/manufacturer-detection-from-mpn` - Manufacturer detection patterns and ordering

### Documentation
- **HISTORY.md** - Technical debt history and completed work
- **.docs/history/** - Detailed analyses of architectural decisions

---

<!-- Add new learnings above this line -->
