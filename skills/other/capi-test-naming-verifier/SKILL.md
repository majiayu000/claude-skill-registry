---
name: capi-test-naming-verifier
description: This skill should be used when the user asks to "verify C API test naming", "check test naming convention", "validate test names", "C API test naming compliance", "test naming verification", "ensure test naming consistency", "audit test names", "review test naming", or mentions verifying that C API unit test names follow the standardized naming convention methodNameTestScenario.
version: 1.0.0
---

# C API Test Naming Verifier Skill

This skill verifies that all C API unit test names follow the standardized naming convention `methodNameTestScenario`. It scans all C API test files (excluding generated tests) and validates compliance with the established naming pattern.

## Naming Convention

### Primary Pattern: `methodNameTestScenario`

- **methodName**: Method name being tested, preserving original casing and underscores
  - camelCase methods: `setEnableHapticFeedback`
  - Underscored methods: `set_onChangeEvent_selected` (preserve underscores!)
- **Test**: Literal "Test" with capital T
- **Scenario**: Descriptive scenario in PascalCase (e.g., `InvalidValues`, `DefaultValues`)

### Special Cases

1. **DISABLED tests**: `DISABLED_methodNameTestScenario`
2. **Utility tests**: Simple names with "Test" suffix (e.g., `SimpleTypesTest`, `ArrayTypesTest`)
3. **Conditional compilation**: Tests in `#ifdef` blocks should have differentiated names (e.g., `WithSupport`, `WithoutSupport`)
4. **Methods containing "Test"**: When method name contains "Test" (e.g., `setHitTestBehavior`, `setOnChildTouchTest`), the separator "Test" is still added, resulting in double "Test" - this is acceptable:
   - `setHitTestBehaviorTestValidInput` ✅ (double "Test" is OK)
   - `setOnChildTouchTestTestValidCallback` ✅ (triple "Test" is OK)
5. **Underscored method names**: Methods with underscores must preserve them:
   - `set_onChangeEvent_selectedTestValidCallback` ✅
   - `setOnChangeEventSelectedTestValidCallback` ❌ (don't convert underscores)

## Usage

### Basic Verification

```bash
claude-code skill capi-test-naming-verifier --verify
```

### Generate Detailed Report

```bash
claude-code skill capi-test-naming-verifier --report
```

### Scan Specific Directory

```bash
claude-code skill capi-test-naming-verifier --directory test/unittest/capi/modifiers
```

### Check Specific File

```bash
claude-code skill capi-test-naming-verifier --file test/unittest/capi/modifiers/common_method_modifier_test2.cpp
```

## Validation Rules

1. **Method Name Format**:
   - camelCase methods: lowercase start (e.g., `setWidth`)
   - Underscored methods: preserve underscores (e.g., `set_onChangeEvent_selected`)
   - **CRITICAL**: Never convert underscored method names to camelCase
2. **"Test" Placement**: Appears between method name and scenario
   - Usually once: `setWidthTestValidValue`
   - Multiple times OK if method contains "Test": `setHitTestBehaviorTestValidInput`
3. **Scenario Format**: PascalCase, descriptive, non-empty (e.g., `ValidInput`, `DefaultValues`)
4. **Length Constraints**: Warning if > 100 characters
5. **DISABLED Prefix**: Must be uppercase `DISABLED_`
6. **Method Name Verification**: Method name in test name must correspond to actual method calls in test body (e.g., `accessor_->methodName` or `modifier_->methodName`)
   - Preserving underscores is required for match: `set_onChangeEvent_selected` matches `accessor_->set_onChangeEvent_selected()`
7. **DefaultValues Exception**: Tests ending in `DefaultValues` don't require method calls (they verify default state)

## Excluded Directories

- `test/unittest/capi/modifiers/generated/` - Auto-generated tests
- Any other generated test directories

## Implementation

The skill performs automated verification through:

1. **File Discovery**: Recursively find all `.cpp` test files in C API directories
2. **Pattern Extraction**: Extract test names from `HWTEST_F` macros
3. **Validation**: Check each test name against naming rules
4. **Reporting**: Generate compliance report with violations and suggestions

## Integration with Existing Skills

- **capi-test-fixer**: Can be used to fix naming violations
- **tdd**: Provides test writing guidelines
- **openharmony-build**: Build verification after naming fixes

## Common Violations

- **Empty scenario**: Test name ends with "Test" (e.g., `setWidthTest` should be `setWidthTestDefaultValues`)
- **Missing "Test"**: No "Test" separator (e.g., `setWidthValidValues` should be `setWidthTestValidValues`)
- **Case violations**: Scenario starts with lowercase (e.g., `setWidthTestvalidValues` should be `setWidthTestValidValues`)
- **Name length**: Test names longer than 100 characters
- **@tc.name mismatch**: Documentation tag doesn't match test name
- **Method name mismatch**: Method name in test doesn't match methods called in test body
  - Wrong: `setOnChangeEventSelectedTestValidCallback` when test calls `set_onChangeEvent_selected()`
  - Right: `set_onChangeEvent_selectedTestValidCallback` matches `set_onChangeEvent_selected()`
- **Underscore conversion**: Converting underscored method names to camelCase
  - Wrong: `setOnChangeEventSelected` (converted from `set_onChangeEvent_selected`)
  - Right: `set_onChangeEvent_selected` (preserved original)
- **Variant type in method name**: Extra descriptors should be in scenario, not method name
  - Wrong: `setStyleCapsuleTestValidBorderRadiusValues` (treats "Capsule" as part of method name)
  - Right: `setStyleTestCapsuleValidBorderRadiusValues` ("Capsule" describes the variant being tested)
  - **Explanation**: When method accepts union types, the variant descriptor belongs in scenario

## Acceptable Patterns (NOT Violations)

- **Double/triple "Test"**: When method name contains "Test", multiple occurrences are OK
  - `setHitTestBehaviorTestValidInput` ✅
  - `setOnChildTouchTestTestValidCallback` ✅
- **Underscored method names**: Must be preserved exactly as in C API
  - `set_onChangeEvent_selectedTestValidCallback` ✅
- **DefaultValues tests without method calls**: Tests verifying default state don't need method invocations

## Output Examples

### Compliance Report
```
C API Test Naming Compliance Report
===================================
Scanned files: 317
Total tests: 934
Compliant tests: 934 (100%)
Violations: 0
```

### Violation Report
```
Violations found in test/unittest/capi/modifiers/common_method_modifier_test2.cpp:
  Line 123: setResponseRegionTest → Should be setResponseRegionTestDefaultValues
  Line 145: SetEnableHapticFeedbackTestInvalidValues → Should be setEnableHapticFeedbackTestInvalidValues

Violations found in test/unittest/capi/modifiers/progress_modifier_test.cpp:
  Line 620: ProgressModifierTest::setStyleCapsuleTestValidBorderRadiusValues
    ❌ Method name mismatch: Test name has 'setStyleCapsule' but test body calls 'setStyle'
    ❌   Suggested test name: 'setStyleTestCapsuleValidBorderRadiusValues'
```

## Best Practices

1. **Run verification after adding new tests**: Ensure new tests follow naming convention
2. **Use during code reviews**: Check naming compliance before merging
3. **Integrate with CI**: Add naming verification to continuous integration pipeline
4. **Regular audits**: Periodically verify existing test names

## Limitations

- Cannot automatically fix naming violations (use capi-test-fixer for fixes)
- Requires manual review for scenario appropriateness
- Does not verify test logic or implementation
- May flag valid tests with no method calls (e.g., default value checks)
- Cannot detect method calls that don't use `accessor_->` or `modifier_->` patterns