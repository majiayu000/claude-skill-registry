---
name: capi-test-fixer
description: This skill should be used when the user asks to "C API test failures", "C API unit test issues", "modifier tests failing", "undefined symbol in C API tests", "ARKUI_CAPI_UNITTEST compilation errors", "Converter API issues in tests", "test build configuration problems", "fix C API interface test failures", "capi test fix", "modifier test fix", or mentions fixing C API unit test failures in OpenHarmony ACE Engine. Automatically diagnoses and fixes common C API unit test failures including missing static modifiers, incorrect Converter API usage, and test build configuration issues.
version: 1.0.0
---

# C API Test Fixer Skill

This skill automatically diagnoses and fixes common C API unit test failures in OpenHarmony ACE Engine. It handles patterns like missing static modifiers in test builds, incorrect Converter API usage, and test build configuration issues.

## When to Use This Skill

Use this skill when encountering C API unit test failures, particularly:

- Linker errors: `undefined symbol: OHOS::Ace::NG::GeneratedModifier::Get*StaticModifier()`
- Test failures: `modifier_test_base.h:210: Expected: (modifier_) != (nullptr)`
- Compilation warnings about pointer/reference mismatches
- Build failures with "undefined reference" for static modifier functions
- Test build configuration issues with missing files

## Common Failure Patterns

### Pattern 1: Missing Static Modifier in Test Builds

**Symptoms**:
- Linker error: `undefined symbol: OHOS::Ace::NG::GeneratedModifier::Get*StaticModifier()`
- Test failure: `modifier_test_base.h:210: Expected: (modifier_) != (nullptr)`

**Root Cause**: Modifier function uses `DynamicModuleHelper` which returns `nullptr` in tests.

**Fix Pattern**:
1. Add ARKUI_CAPI_UNITTEST conditional compilation to modifier.cpp
2. Include static modifier implementation in test BUILD.gn

### Pattern 2: Incorrect Converter API Usage

**Symptoms**:
- Test failure comparing `nullopt` vs `nullptr`
- Compilation warnings about pointer/reference mismatches

**Root Cause**: Using `Converter::GetOptPtr(&local_var)` instead of `Converter::GetOpt(local_var)`

**Fix Pattern**: Replace `GetOptPtr(&var)` with `GetOpt(var)` for local variables.

### Pattern 3: Test Build Configuration Missing Files

**Symptoms**:
- Build fails with "undefined reference" for static modifier functions
- File not included in test build sources

**Root Cause**: Static modifier .cpp file not listed in test BUILD.gn sources

**Fix Pattern**: Add missing .cpp file to test BUILD.gn sources list.

### Pattern 4: Callback Invoke vs InvokeSync Mismatch

**Symptoms**:
- Test callback values remain at initial value (e.g., `g_indexValue = 0`)
- Event callbacks silently don't fire
- Test error: `Expected: g_indexValue == INDEX, Actual: 0 vs 10`

**Root Cause**: Implementation uses `CallbackHelper::InvokeSync()` but test callbacks
are created with `Converter::ArkCallback<T>(lambda)` where the lambda matches the `call`
signature (`Ark_Int32 nodeId, ...args`). `InvokeSync` uses `callSync` field which is
`nullptr`, so the callback silently does nothing.

The two `ArkCallback` overloads in `reverse_converter.h` select based on function signature:
- `call` type: `void (*)(Ark_Int32 resourceId, ...args)` → sets `.call`, `.callSync = nullptr`
- `callSync` type: `void (*)(Ark_VMContext vmContext, Ark_Int32 resourceId, ...args)` → sets `.callSync`, `.call = nullptr`

**Fix Pattern**: Add `Ark_VMContext vmContext` as the first parameter in test callback lambdas.

```cpp
// Before (matches call signature → InvokeSync finds callSync=nullptr → no-op)
auto callback = [](Ark_Int32 nodeId, const Ark_Int32 index) {
    g_indexValue = Converter::Convert<int32_t>(index);
};

// After (matches callSync signature → InvokeSync works correctly)
auto callback = [](Ark_VMContext vmContext, Ark_Int32 nodeId, const Ark_Int32 index) {
    g_indexValue = Converter::Convert<int32_t>(index);
};
```

**Common affected tests**: Any event callback test (onChange, onSelected, onWillShow, etc.)
where the implementation was changed from `Invoke()` to `InvokeSync()`.

### Pattern 5: Ark_String Dangling Pointer in Getters

**Symptoms**:
- Getter returns garbage/corrupted data (e.g., `"\0x\x1D"` instead of `"xor"`)
- Use-after-free in string return values
- Only affects getters that return `Ark_String`

**Root Cause**: Peer getter returns `std::string` by value. `Converter::ArkValue<Ark_String>()`
stores `chars` pointer to the temporary's data. When the temporary is destroyed, the pointer
dangles.

In `reverse_converter.h`, `AssignArkValue(Ark_String& dst, const std::string_view& src, ConvContext *ctx)`:
- When `ctx != nullptr`: copies data into persistent storage via `ctx->Store(src)`
- When `ctx == nullptr` (default): stores raw pointer `dst.chars = src.data()` — **dangles if source is temporary**

**Fix Pattern**: Change peer getter to return `const std::string&` instead of `std::string`
(since it returns a member variable), so the `Ark_String` points to stable memory.

```cpp
// Before (returns by value → Ark_String.chars dangles)
std::string GetGlobalCompositeOperation() const {
    return globalCompositeOperation_;
}

// After (returns by reference → Ark_String.chars points to member)
const std::string& GetGlobalCompositeOperation() const {
    return globalCompositeOperation_;
}
```

**Alternative fix**: Use `Converter::FC` (frame context) to store the string data persistently:
```cpp
auto result = peerImpl->GetGlobalCompositeOperation();
return Converter::ArkValue<Ark_String>(result, Converter::FC);
```

## Skill Implementation

The skill performs automated diagnosis through:

### 1. Error Analysis
- Parse build logs (`out/rk3568/build.log`)
- Extract linker errors and undefined symbols
- Analyze test failure messages

### 2. Pattern Matching
```python
# Example patterns from error_patterns.json
PATTERNS = {
    "static_modifier_missing": r"undefined symbol.*Get(\w+)StaticModifier",
    "converter_api_misuse": r"GetOptPtr\(&",
    "nullptr_modifier": r"modifier_test_base\.h.*modifier_.*!=.*nullptr",
}
```

### 3. Fix Generation
Based on detected patterns:

- **Static modifier missing**:
  - Check if modifier.cpp has ARKUI_CAPI_UNITTEST conditional
  - Verify test BUILD.gn includes static_modifier.cpp
  - Generate appropriate patches

- **Converter API misuse**:
  - Locate offending test file
  - Suggest GetOptPtr → GetOpt replacement

- **Build configuration**:
  - Check test BUILD.gn source lists
  - Add missing static modifier files

## Usage Examples

### Diagnose and Fix All Issues
```bash
claude-code skill capi-test-fixer --diagnose
```

### Fix Specific Test Failure
```bash
claude-code skill capi-test-fixer --test SymbolGlyphModifierTest
```

### Analyze Build Log
```bash
claude-code skill capi-test-fixer --build-log out/rk3568/build.log
```

## Integration with Existing Skills

This skill complements:

- **openharmony-build**: Uses build logs for diagnosis
- **build-error-analyzer**: Focuses specifically on C API test patterns
- **tdd**: Provides test-specific fixes

## File Structure

```
.claude/skills/capi-test-fixer/
├── SKILL.md                 # This file
├── README.md                # Detailed documentation
├── skill.json               # Skill configuration
├── test_skill.py            # Test script
├── scripts/
│   ├── diagnose.py          # Main diagnosis script
│   ├── fix_static_modifier.py
│   ├── fix_converter_api.py
│   └── fix_build_config.py
├── templates/
│   ├── static_modifier.patch
│   └── converter_fix.patch
└── patterns/
    └── error_patterns.json  # Error pattern definitions
```

## Error Resolution Workflow

1. **Collect Data**: Build logs, test outputs, source files
2. **Pattern Match**: Identify failure category using error_patterns.json
3. **Root Cause Analysis**: Determine exact issue location
4. **Fix Generation**: Create appropriate patches using templates
5. **Validation**: Verify fixes work by checking test compilation

## Common Fix Templates

### Static Modifier Fix
```cpp
// Before
const GENERATED_ArkUI*Modifier* Get*Modifier()
{
    auto* module = DynamicModuleHelper::GetInstance().GetDynamicModule("*");
    return reinterpret_cast<const GENERATED_ArkUI*Modifier*>(module->GetStaticModifier());
}

// After
#ifdef ARKUI_CAPI_UNITTEST
const GENERATED_ArkUI*Modifier* Get*StaticModifier();
#endif

const GENERATED_ArkUI*Modifier* Get*Modifier()
{
    static const GENERATED_ArkUI*Modifier* cachedModifier = nullptr;
    if (cachedModifier == nullptr) {
#ifdef ARKUI_CAPI_UNITTEST
        cachedModifier = GeneratedModifier::Get*StaticModifier();
#else
        auto* module = DynamicModuleHelper::GetInstance().GetDynamicModule("*");
        CHECK_NULL_RETURN(module, nullptr);
        cachedModifier = reinterpret_cast<const GENERATED_ArkUI*Modifier*>(module->GetStaticModifier());
#endif
    }
    return cachedModifier;
}
```

### Converter API Fix
```cpp
// Before
auto optValue = Converter::GetOptPtr(&ptr);

// After
auto optValue = Converter::GetOpt(ptr);
```

### BUILD.gn Fix
```gn
# Add to test/unittest/capi/BUILD.gn sources
sources += [
    "$ace_root/frameworks/core/components_ng/pattern/*/bridge/*_static_modifier.cpp",
]
```

### Callback InvokeSync Fix
```cpp
// Before (call signature — InvokeSync ignores this)
auto callback = [](Ark_Int32 nodeId, const Ark_Int32 index) { ... };

// After (callSync signature — InvokeSync uses this)
auto callback = [](Ark_VMContext vmContext, Ark_Int32 nodeId, const Ark_Int32 index) { ... };

// For VoidCallback:
// Before
auto cb = [](const Ark_Int32 resourceId) { ... };
// After
auto cb = [](Ark_VMContext vmContext, const Ark_Int32 resourceId) { ... };
```

### Ark_String Lifetime Fix
```cpp
// Before (dangling pointer — getter returns std::string by value)
std::string GetValue() const { return member_; }

// After (stable pointer — getter returns const reference)
const std::string& GetValue() const { return member_; }
```

## Best Practices

1. **Always check existing patterns**: Radio modifier already implements ARKUI_CAPI_UNITTEST pattern
2. **Verify test builds**: Ensure `ARKUI_CAPI_UNITTEST` is defined in test config
3. **Use proper Converter API**: `GetOpt` for values, `GetOptPtr` for pointers
4. **Maintain consistency**: Follow established patterns in codebase
5. **Test after fixes**: Always rebuild and run tests to verify fixes work

## Supported Patterns

The skill supports the following error patterns (defined in `patterns/error_patterns.json`):

1. **static_modifier_missing**: Detects undefined symbol errors for static modifiers
2. **converter_api_misuse**: Detects incorrect `GetOptPtr(&var)` usage
3. **nullptr_modifier_in_tests**: Detects modifier returning nullptr in tests
4. **test_build_config_missing_files**: Detects missing files in BUILD.gn
5. **arkui_capi_unittest_compilation_error**: Detects ARKUI_CAPI_UNITTEST compilation errors
6. **dynamic_module_helper_nullptr**: Detects DynamicModuleHelper returning nullptr
7. **callback_invoke_vs_invoke_sync**: Detects test callbacks using `call` signature when implementation uses `InvokeSync` (requires `callSync` signature)
8. **ark_string_dangling_pointer**: Detects Ark_String getters returning dangling pointers from temporary std::string

## Limitations

- Cannot fix complex test logic errors
- Requires clear error patterns
- May need manual review for edge cases
- Focuses on C API unit test failures only (not other test types)

## Contributing

Add new patterns to `patterns/error_patterns.json`:

```json
{
  "pattern_name": {
    "regex": "error pattern",
    "category": "static_modifier|converter_api|build_config",
    "fix_template": "template_name",
    "severity": "high|medium|low"
  }
}
```

Update fix templates in the `templates/` directory as needed for new patterns.