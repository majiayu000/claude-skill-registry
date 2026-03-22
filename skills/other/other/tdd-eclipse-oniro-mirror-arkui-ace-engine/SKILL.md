---
name: tdd
description: This skill should be used when writing unit tests, TDD test cases, test coverage analysis, or test-driven development for NG component Pattern methods (e.g., OnModifyDone, OnDirtyLayoutWrapperSwap). Covers test principles, templates, common pitfalls, branch coverage, API verification, state reset, and mandatory self-checklist for ace_engine testing.
version: 1.0.0
---

# TDD Writing Guidelines for NG Component Pattern Methods

When writing TDD tests for NG component Pattern methods (e.g., `OnModifyDone()`, `OnDirtyLayoutWrapperSwap()`), follow these guidelines to avoid common pitfalls.

## Core Principles

### 1. Direct Method Invocation

Call the target method directly, not through indirect triggers.

- ✅ `menuPattern->OnModifyDone()`
- ❌ `menuPattern->FireBuilder()` (doesn't trigger `OnModifyDone()`)

### 2. State Reset

Always reset potentially interfering state before calling target method.

```cpp
// Reset to clean state before testing
auto renderContext = menuNode->GetRenderContext();
renderContext->ResetOuterBorder();  // Reset entire property group

// Then call target method
menuPattern->OnModifyDone();
```

### 3. API Verification

Use Grep/Read tools to verify method names, never guess.

```bash
# Search for method definition
grep -rn "ResetOuterBorder\|Reset.*Outer" frameworks/core/components_ng/render/render_context.h

# Understand macro-generated methods
grep -A 5 "ACE_DEFINE_PROPERTY_GROUP" frameworks/core/components_ng/property/property.h
```

- `ACE_DEFINE_PROPERTY_GROUP(OuterBorder, OuterBorderProperty)` generates:
  - `GetOrCreateOuterBorder()`, `GetOuterBorder()`, `CloneOuterBorder()`, **`ResetOuterBorder()`**
  - NOT `ResetOuterBorderRadius()` (common mistake)

### 4. Branch Coverage

Write paired tests for if/else branches.

```cpp
// Branch 1: Condition is true
HWTEST_F(Xxx, Test_BranchTrue, TestSize.Level1) {
    borderRadiusVP.SetRadius(Dimension(10.0_vp));  // No PERCENT unit
    renderContext->ResetOuterBorder();
    pattern->OnModifyDone();
    EXPECT_TRUE(outerRadius.has_value());
}

// Branch 2: Condition is false
HWTEST_F(Xxx, Test_BranchFalse, TestSize.Level1) {
    borderRadiusPercent.SetRadius(Dimension(50.0f, DimensionUnit::PERCENT));
    renderContext->ResetOuterBorder();
    pattern->OnModifyDone();
    EXPECT_FALSE(outerRadius.has_value());
}
```

### 5. No Line Numbers in Comments

Avoid hardcoding line numbers in test comments.

- ❌ `OnModifyDone should skip UpdateBorderRadius at line 299`
- ✅ `OnModifyDone should skip UpdateBorderRadius when borderRadius has percent unit`
- **Reason**: Line numbers change as code evolves, making comments outdated
- **Alternative**: Describe the logical condition being tested rather than the physical line location

### 6. No Documentation-Only Tests

Every test case must have actual test logic.

- ❌ Documentation-only test with only comments and `EXPECT_TRUE(true)`
- ✅ Test with real assertions and verification logic
- **Reason**: Tests without executable logic don't verify behavior and waste maintenance resources
- **Alternative**: Put branch documentation in separate design documents or code comments, not in test cases
- **Example of what NOT to do**:
  ```cpp
  // ❌ BAD: Documentation-only test
  HWTEST_F(ComponentPatternTestNg, ComponentPattern_BranchDocumentation, TestSize.Level1) {
      /**
       * @tc.steps: step1. Document branches
       * Branch 1: condition is true
       * Branch 2: condition is false
       */
      EXPECT_TRUE(true);  // No actual testing!
  }
  ```
- **Correct approach**: Write separate test cases for each branch with real logic

### 7. No Magic Numbers

Use named constants instead of hardcoded numbers.

- ❌ Hardcoded numbers like `720`, `1280`, `0`, `3.0`, `-1`, `100000`
- ✅ Named constants with clear semantic meaning
- **Reason**: Magic numbers make code hard to understand and maintain. Constants provide context and make changes easier
- **Where to define**: Place constants in anonymous namespace at the top of the test file
- **Example**:
  ```cpp
  // ❌ BAD: Magic numbers
  HWTEST_F(ComponentPatternTestNg, ComponentPattern_TestBranch, TestSize.Level1) {
      SystemProperties::InitDeviceInfo(720, 1280, 0, 3.0, false);
      auto size = GetSubWindowSize(100000, 0);
      EXPECT_GT(size.Width(), 0);
  }

  // ✅ GOOD: Named constants
  namespace {
      const int32_t TEST_DEVICE_WIDTH = 720;
      const int32_t TEST_DEVICE_HEIGHT = 1280;
      const int32_t TEST_DEVICE_ORIENTATION = 0;
      const double TEST_DEVICE_RESOLUTION = 3.0;
      const bool TEST_DEVICE_IS_ROUND = false;
      const int32_t TEST_PARENT_CONTAINER_ID = 100000;
      const uint32_t DEFAULT_DISPLAY_ID = 0;
  }
  HWTEST_F(ComponentPatternTestNg, ComponentPattern_TestBranch, TestSize.Level1) {
      SystemProperties::InitDeviceInfo(
          TEST_DEVICE_WIDTH, TEST_DEVICE_HEIGHT, TEST_DEVICE_ORIENTATION,
          TEST_DEVICE_RESOLUTION, TEST_DEVICE_IS_ROUND);
      auto size = GetSubWindowSize(TEST_PARENT_CONTAINER_ID, DEFAULT_DISPLAY_ID);
      EXPECT_GT(size.Width(), 0);
  }
  ```

## Test Template

```cpp
/**
 * @tc.name: PatternMethod_TestBranchName
 * @tc.desc: Test Description covering specific behavior (e.g., "when X happens, Y should occur")
 * @tc.type: FUNC
 */
HWTEST_F(ComponentPatternTestNg, ComponentPattern_TestBranchName, TestSize.Level1)
{
    // 1. Environment setup
    MockPipelineContext::GetCurrent()->SetMinPlatformVersion(static_cast<int32_t>(PlatformVersion::VERSION_ELEVEN));
    ScreenSystemManager::GetInstance().dipScale_ = DIP_SCALE;

    // 2. Create nodes (using existing helper methods like GetPreviewMenuWrapper)
    auto menuWrapperNode = GetPreviewMenuWrapper();
    ASSERT_NE(menuWrapperNode, nullptr);
    auto menuNode = AceType::DynamicCast<FrameNode>(menuWrapperNode->GetChildAtIndex(0));
    ASSERT_NE(menuNode, nullptr);
    auto menuPattern = menuNode->GetPattern<MenuPattern>();
    ASSERT_NE(menuPattern, nullptr);
    auto menuLayoutProperty = menuNode->GetLayoutProperty<MenuLayoutProperty>();
    ASSERT_NE(menuLayoutProperty, nullptr);
    auto renderContext = menuNode->GetRenderContext();
    ASSERT_NE(renderContext, nullptr);

    // 3. Set test data to trigger target branch
    TestDataType testData;
    testData.SetValue(...);  // Configure to trigger branch
    menuLayoutProperty->UpdateProperty(testData);

    // 4. Reset interfering state (CRITICAL!)
    renderContext->ResetTargetProperty();

    // 5. Call target method directly
    menuPattern->TargetMethod();

    // 6. Verify results match branch expectation
    auto result = renderContext->GetTargetProperty();
    EXPECT_TRUE(result.has_value());  // Or false based on branch
}
```

## Common Pitfalls

| Pitfall | Symptom | Solution |
|:---|:---|:---|
| Indirect method call | Test doesn't trigger target code path | Call target method directly |
| No state reset | Test fails with unexpected values | Reset all potentially interfering properties before calling method |
| Guessed API name | Compilation error or method not found | Use Grep to verify exact method name from source |
| Unclean test data | Tests interfere with each other | Each test should be independent, reset all state |
| Missing branch coverage | Code coverage shows gaps | Write tests for both true and false branches |
| Line numbers in comments | Comments become outdated when code changes | Describe logical conditions instead of physical locations |
| Documentation-only tests | Test contains only comments with `EXPECT_TRUE(true)` | Every test must have real assertions and verification logic |
| Magic numbers | Hardcoded numbers like `720`, `1280`, `100000` without meaning | Use named constants with clear semantic meaning in anonymous namespace |

## Mandatory Self-Checklist

After generating test code, verify:

- [ ] All called methods exist (verified via Grep/Read)
- [ ] State is reset before calling target method
- [ ] Test data triggers the correct branch (HasPercentUnit returns expected value)
- [ ] Assertions match branch behavior
- [ ] All API signatures match source definitions
- [ ] Test follows existing test file structure and naming conventions
- [ ] Comments describe logical behavior, not line numbers (e.g., use "when X happens" instead of "at line 299")
- [ ] **Every test case has real test logic (not just documentation with `EXPECT_TRUE(true)`)**
- [ ] **No magic numbers - all numeric literals replaced with named constants**

## Reference Implementation

See working example at: `test/unittest/core/pattern/menu/menu_pattern_test_ng.cpp:1482-1574`

- `MenuPatternTest_OnModifyDone_UpdateBorderRadius` - Tests when border has no PERCENT unit
- `MenuPatternTest_OnModifyDone_PercentBorderRadius` - Tests when border has PERCENT unit
