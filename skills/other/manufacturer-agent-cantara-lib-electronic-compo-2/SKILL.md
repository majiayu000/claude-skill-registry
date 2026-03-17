---
name: manufacturer-agent
description: Web-augmented agent for creating manufacturer skills and comprehensive tests. Use when adding or improving support for a manufacturer handler.
---

# Manufacturer Agent

Automated agent for creating detailed manufacturer skills and comprehensive test coverage.

## Usage

```
/manufacturer-agent <manufacturer-name>
```

Examples:
- `/manufacturer-agent ST` - STMicroelectronics
- `/manufacturer-agent NXP` - NXP Semiconductors
- `/manufacturer-agent Infineon` - Infineon Technologies
- `/manufacturer-agent Microchip` - Microchip Technology

## Agent Workflow

Execute these phases in order:

### Phase 1: Analyze Existing Handler

1. Find the handler file:
   ```
   Glob: src/main/java/**/manufacturers/*Handler.java
   ```

2. Read the handler and extract:
   - All patterns registered in `initializePatterns()`
   - Supported ComponentTypes from `getSupportedTypes()`
   - Package code mappings in `extractPackageCode()`
   - Series extraction logic in `extractSeries()`
   - Any special matching logic in `matches()`

3. Identify issues:
   - Uses `HashSet` instead of `Set.of()`?
   - Uses default `matches()` with multi-pattern types?
   - Missing case-insensitive handling?

### Phase 2: Web Research

Search for manufacturer documentation using these queries:

```
WebSearch: "{manufacturer} part number naming convention"
WebSearch: "{manufacturer} ordering information guide"
WebSearch: "{manufacturer} package marking code"
WebSearch: "{manufacturer} product selector guide filetype:pdf"
```

For each relevant result, fetch and analyze:
```
WebFetch: <url>
Prompt: "Extract the MPN structure, package codes, temperature grades, and family prefixes from this page"
```

**Key information to gather:**
- MPN structure breakdown (prefix, series, variant, package, temp, qualifier)
- Package code table (e.g., N=DIP, D=SOIC, PW=TSSOP)
- Temperature grade suffixes (I=Industrial, Q=Automotive, M=Military)
- Family prefixes and what they indicate
- Common product series with examples
- Any naming quirks or conflicts (like TI's LM35 vs LM358)

### Phase 3: Gather Real MPN Examples

Search for real part numbers to use in tests:

```
WebSearch: "{manufacturer} {product-type} datasheet"
```

Product types to search based on handler's supported types:
- Microcontroller → "STM32 datasheet", "PIC microcontroller"
- MOSFET → "IRFZ44N datasheet", "STF5N52U"
- Op-amp → "LM358 datasheet", "TL072"
- Voltage regulator → "LM7805 datasheet"

Collect 5-10 real MPNs for each supported ComponentType.

### Phase 4: Generate Skill File

Create `.claude/skills/manufacturers/{manufacturer}/SKILL.md` following this template:

```markdown
---
name: {manufacturer-lowercase}
description: {Manufacturer} MPN encoding patterns, suffix decoding, and handler guidance.
---

# {Manufacturer} Manufacturer Skill

## MPN Structure

{Diagram showing MPN breakdown}

### Example Decoding

{2-3 annotated examples}

---

## Package Codes

### Through-Hole Packages
| Code | Package | Notes |
|------|---------|-------|

### Surface Mount Packages
| Code | Package | Notes |
|------|---------|-------|

---

## Family Prefixes

| Prefix | Category | Examples |
|--------|----------|----------|

---

## Temperature Grades

| Suffix | Range | Application |
|--------|-------|-------------|

---

## Common Series Reference

{Tables of common product series}

---

## Handler Implementation Notes

### Package Code Extraction
{Code examples and gotchas}

### Series Extraction
{Code examples}

### Known Issues
{Any bugs or limitations found}

---

## Related Files

- Handler: `manufacturers/{Handler}.java`
- Component types: {list types}
- Test: `handlers/{Handler}Test.java`

---

## Learnings & Edge Cases

{Bullet points of discoveries}

<!-- Add new learnings above this line -->
```

### Phase 5: Generate Test File

Create `src/test/java/no/cantara/electronic/component/lib/handlers/{Handler}Test.java`:

**CRITICAL: Test Design Principles**

1. **ALL TESTS MUST PASS** - Never commit failing tests
2. **Document bugs in SKILL.md and CLAUDE.md**, not via failing assertions
3. **Handler behavior can be non-deterministic** due to test execution order and shared PatternRegistry
4. **For flaky behavior**, use documentation tests (no assertions) instead of assertTrue/assertFalse

**Test Categories:**

| Category | Assertion Type | When to Use |
|----------|---------------|-------------|
| Stable behavior | `assertTrue`/`assertFalse` | Handler behavior is consistent |
| Flaky behavior | `System.out.println` only | Behavior varies by test order |
| Bug documentation | Comments + SKILL.md | Document in files, not tests |

**Structure:**

```java
package no.cantara.electronic.component.lib.handlers;

import no.cantara.electronic.component.lib.ComponentType;
import no.cantara.electronic.component.lib.PatternRegistry;
import no.cantara.electronic.component.lib.manufacturers.{Handler};
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import static org.junit.jupiter.api.Assertions.*;

class {Handler}Test {

    private static {Handler} handler;
    private static PatternRegistry registry;

    @BeforeAll
    static void setUp() {
        // Direct instantiation - avoids MPNUtils.getManufacturerHandler bug
        handler = new {Handler}();
        registry = new PatternRegistry();
        handler.initializePatterns(registry);
    }

    // === STABLE TESTS (use assertions) ===
    @Nested
    @DisplayName("{ProductType} Detection - Stable")
    class {ProductType}StableTests {
        @ParameterizedTest
        @ValueSource(strings = {"{real-mpn-1}", "{real-mpn-2}"})
        void shouldDetect{ProductType}(String mpn) {
            // Only assert if behavior is ALWAYS consistent
            assertTrue(handler.matches(mpn, ComponentType.{TYPE}, registry),
                    mpn + " should match {TYPE}");
        }
    }

    // === DOCUMENTATION TESTS (no assertions) ===
    @Nested
    @DisplayName("Behavior Documentation")
    class BehaviorDocumentation {
        @ParameterizedTest
        @ValueSource(strings = {"{potentially-flaky-mpn-1}", "{potentially-flaky-mpn-2}"})
        void documentDetectionBehavior(String mpn) {
            // Document actual behavior without assertions
            boolean matches = handler.matches(mpn, ComponentType.IC, registry);
            System.out.println(mpn + " matches IC = " + matches);
        }
    }

    // === EXTRACTION TESTS (usually stable) ===
    @Nested
    @DisplayName("Package Code Extraction")
    class PackageCodeTests {
        @ParameterizedTest
        @CsvSource({
            "{mpn1}, {expected-package1}",
            "{mpn2}, {expected-package2}"
        })
        void shouldExtractPackageCodes(String mpn, String expected) {
            assertEquals(expected, handler.extractPackageCode(mpn));
        }
    }

    // === EDGE CASES ===
    @Nested
    @DisplayName("Edge Cases")
    class EdgeCaseTests {
        @Test
        void shouldHandleNull() {
            assertFalse(handler.matches(null, ComponentType.IC, registry));
            assertEquals("", handler.extractPackageCode(null));
        }

        @Test
        void shouldBeCaseInsensitive() {
            // Test lowercase handling
        }
    }
}
```

### Phase 6: Run Tests and Report

1. Run the new tests:
   ```bash
   mvn test -Dtest={Handler}Test
   ```

2. If single-test fails with initialization error, run full suite:
   ```bash
   mvn test
   ```

3. Analyze failures:
   - Pattern not matching? → Fix pattern in handler
   - Package extraction wrong? → Check suffix ordering, speed grades
   - Multi-pattern type issue? → Use `registry.matches()` instead of default

4. Create summary report:
   - Tests created: X
   - Tests passing: Y
   - Handler bugs found: Z
   - Recommended fixes: [list]

### Phase 7: Update Documentation

1. Update CLAUDE.md with any new learnings
2. Add handler to "Known Technical Debt" if issues found
3. Note the new test as a template for similar manufacturers

---

## Common Handler Issues to Check

From previous work on TI, Atmel, and ST handlers:

1. **HashSet in getSupportedTypes()** → Change to `Set.of()`
2. **Multi-pattern types** → Override `matches()` to use `registry.matches()`
3. **Suffix ordering** → Check longer suffixes before shorter (DT before T)
4. **Speed grades** → Strip digits before package lookup
5. **Case sensitivity** → Ensure `toUpperCase()` is called
6. **Local package maps** → Migrate to `PackageCodeRegistry`
7. **Cross-handler pattern matching** → Don't fall through to `patterns.matches()` for base types (MICROCONTROLLER, MOSFET, etc.)
8. **Debug println statements** → Remove any `System.out.println` debug code
9. **Package location varies by component type** → MCUs often have suffix, MOSFETs have prefix, regulators have grade+suffix

---

## Learnings from ST Test Run (PR #81)

### Test Setup: Direct Instantiation Preferred

```java
// PROBLEM: MPNUtils.getManufacturerHandler can return wrong handler
// due to alphabetical ordering (AtmelHandler < STHandler)
ManufacturerHandler h = MPNUtils.getManufacturerHandler("STM32F103C8T6");
// Returns AtmelHandler instead of STHandler!

// SOLUTION: Use direct instantiation for handler tests
handler = new STHandler();
registry = new PatternRegistry();
handler.initializePatterns(registry);
```

### Cross-Handler Pattern Matching Bug

When a handler's `matches()` method falls through to `patterns.matches(mpn, type)`, it can accidentally match patterns registered by OTHER handlers because the PatternRegistry is shared.

**Example**: AtmelHandler checking STM32F103C8T6 for MICROCONTROLLER type:
1. Quick prefix check fails (not ATMEGA, ATTINY, etc.)
2. Falls through to `patterns.matches(mpn, MICROCONTROLLER)`
3. STHandler's STM32 pattern is in the registry for MICROCONTROLLER
4. Pattern matches → AtmelHandler incorrectly returns true!

**Fix**: For base types like MICROCONTROLLER, MOSFET, VOLTAGE_REGULATOR, handlers should:
- Return `true` only if their prefix check passes
- Return `false` if prefix check fails (don't fall through)
- Only use `patterns.matches()` for manufacturer-specific types

### Package Extraction by Component Type

Different component families encode package info differently:

| Component | Package Location | Example |
|-----------|-----------------|---------|
| STM32 MCU | Second-to-last char | STM32F103C8**T**6 → T=LQFP |
| ST MOSFET | Prefix | **STF**5N52U → STF=TO-220FP |
| L78xx Regulator | Grade + Suffix | L7805**CV** → CV=TO-220 |
| Atmel MCU | After hyphen | ATMEGA328P-**PU** → PU=PDIP |

### Test Expectations

When fixing package extraction, existing tests may expect the OLD (wrong) behavior:
- `MPNExtractionTest` expected "T6" for STM32F103C8T6
- After fix, it should expect "LQFP"
- Update ALL affected tests when fixing extraction logic

---

## Critical Lesson: Handler Behavior is Non-Deterministic

**Problem discovered**: Handler `matches()` behavior can vary based on:
1. Test execution order
2. Which other tests have initialized classes first
3. Shared PatternRegistry state

**Symptoms**:
- Test passes when run alone, fails in full suite (or vice versa)
- Same assertion passes/fails randomly between runs
- `assertTrue` and `assertFalse` for same MPN both fail

**Solution**:
1. **Stable tests**: Only assert on handler methods with deterministic output (extractPackageCode, extractSeries, null handling)
2. **Detection tests**: Use documentation approach (no assertions) for `matches()` calls that may vary
3. **Bug documentation**: Write bugs in SKILL.md "Known Handler Issues" section, NOT via failing test assertions

**Example - DO THIS:**
```java
// Document behavior without assertions
void documentDetectionBehavior(String mpn) {
    boolean matches = handler.matches(mpn, ComponentType.IC, registry);
    System.out.println(mpn + " matches IC = " + matches);
    // BUG documented in SKILL.md: MAX485 pattern missing
}
```

**Example - DON'T DO THIS:**
```java
// WRONG: Creates flaky tests
void bugMAX485NotDetected(String mpn) {
    assertFalse(handler.matches(mpn, ComponentType.IC, registry),
            "BUG: MAX485 should match but doesn't");  // May pass or fail randomly!
}
```

---

## Output Checklist

After running this agent, you should have:

- [ ] `.claude/skills/manufacturers/{manufacturer}/SKILL.md`
- [ ] `src/test/java/.../handlers/{Handler}Test.java`
- [ ] **ALL TESTS PASSING** (verify with `mvn test`)
- [ ] Bugs documented in SKILL.md, NOT via failing tests
- [ ] Updated CLAUDE.md with learnings
- [ ] PR ready for review
