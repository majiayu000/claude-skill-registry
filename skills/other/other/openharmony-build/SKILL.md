---
name: openharmony-build
description: This skill should be used when the user asks to "编译 OpenHarmony", "build OpenHarmony", "编译完整代码", "执行编译", "编译 OpenHarmony 代码", "快速编译", "跳过gn编译", "fast-build", "编译测试", "编译测试用例", "build ace_engine_test", "编译 sdk", "编译 SDK", "build sdk", "build SDK", "编译 ohos-sdk", "编译测试列表", "build test list", "按列表编译测试", "编译指定测试", "编译覆盖率版本", "build coverage version", "覆盖率编译", or mentions building the full OpenHarmony system, fast rebuild, test compilation, SDK compilation, building tests from a target list, or building tests with code coverage enabled. Handles complete build process including build execution, success verification, and failure log analysis with primary focus on out/{product}/build.log.
version: 0.6.0
---

# OpenHarmony Build Skill

This skill provides comprehensive support for building the complete OpenHarmony codebase, including build execution, result verification, and error log analysis.

## Build Environment

OpenHarmony uses the `build.sh` script located in the root directory for building. The build process requires:

- **Build script**: `./build.sh` in OpenHarmony root directory
- **Build tool**: hb (Harmony Build) system
- **Python environment**: Python 3 from prebuilts
- **Node.js**: Version 14.21.1
- **Output directory**: `out/` in OpenHarmony root

## Build Execution

### Navigate to Root Directory

Always execute builds from the OpenHarmony root directory. To find the root directory from any location in the tree:

```bash
# Method 1: Find directory containing .gn file
find_root() {
    local current_dir="$(pwd)"
    while [[ ! -f "$current_dir/.gn" ]]; do
        current_dir="$(dirname "$current_dir")"
        if [[ "$current_dir" == "/" ]]; then
            echo "Error: OpenHarmony root not found (no .gn file)"
            return 1
        fi
    done
    echo "$current_dir"
}

# Navigate to root
cd "$(find_root)"
```

### Standard Build Commands

**Full build for product** (recommended command with cache enabled):
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache
```

**Build specific component**:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache
```

**Build with specific target**:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name <product> --build-target <target> --ccache
```

Common product names: `rk3568`, `ohos-sdk`, `rk3588`

Common build targets: `ohos` (default if omitted), `ace_engine`, `ace_engine_test`, `unittest`

### SDK Build (Special Case)

**IMPORTANT**: SDK build has a special output directory structure.

Build OpenHarmony SDK:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name ohos-sdk --ccache
```

**SDK build characteristics**:
- **No `--build-target` option**: Do NOT specify a build target for SDK compilation
- **Output directory**: `out/sdk/` (NOT `out/ohos-sdk/`)
- **Special case**: Unlike other products where output is `out/<product>/`, SDK output is always in `out/sdk/`
- **Use case**: Building the OpenHarmony SDK for application development

**Trigger keywords for SDK build**:
- "编译 sdk" / "编译 SDK"
- "build sdk" / "build SDK"
- "编译 ohos-sdk"
- "make sdk"

**Example SDK build workflow**:
```bash
# Navigate to OpenHarmony root
cd "$(find_root)"

# Build SDK (no target specified)
./build.sh --export-para PYCACHE_ENABLE:true --product-name ohos-sdk --ccache

# Check SDK build log
cat "$OH_ROOT/out/sdk/build.log"
```

**Build command options**:
- `--export-para PYCACHE_ENABLE:true` - Enable Python cache for faster builds
- `--ccache` - Enable compiler cache for faster rebuilds
- `--product-name` - Target product to build
- `--build-target` - Specific component or target (optional, defaults to full system)
- `--fast-rebuild` - Skip GN generation if no GN files modified (significantly faster)

### Test Build Commands

**Build ACE Engine tests** (recommended for ACE Engine development):
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine_test --ccache
```

**Build all unit tests** (full test suite):
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target unittest --ccache
```

**Test target priorities** (recommended usage):
1. **`ace_engine_test`** - Build ACE Engine specific tests only (faster, recommended for ACE Engine development)
2. **`unittest`** - Build all unit tests across entire system (slower, comprehensive testing)

**When to use `ace_engine_test`**:
- Developing or testing ACE Engine components
- Quick validation of ACE Engine changes
- Focused testing on ACE Engine functionality
- Faster iteration during development

**When to use `unittest`**:
- Running complete test suite
- Validating cross-module interactions
- Pre-release comprehensive testing
- When specifically required to build all tests

### Build Tests with Code Coverage

**IMPORTANT**: Building test suites with code coverage requires special build parameters.

**Trigger keywords**:
- "编译覆盖率版本" / "build coverage version"
- "覆盖率编译" / "compile with coverage"
- "测试套覆盖率" / "test suite coverage"

**Scope of coverage parameter**:
- ✅ **Valid for**: `ace_engine_test` and specific test targets within ace_engine repository
- ⚠️ **Scope limited**: The parameter `--gn-args ace_engine_feature_enable_coverage=true` ONLY affects ace_engine repository targets
- ✅ **Safe to use**: Even when used with global `unittest` target, the parameter only applies to ace_engine tests; other repositories are unaffected
- 💡 **Usage**: You can safely add this parameter when building `unittest` to enable coverage for ace_engine tests only

**Recommended practice**: When building ace_engine_test or ace_engine test targets, ALWAYS include `--gn-args ace_engine_feature_enable_coverage=true` to enable code coverage instrumentation.

**Build ace_engine_test with coverage**:
```bash
# Navigate to OpenHarmony root first
cd "$(find_root)"

# Build ACE Engine test suite with coverage
./build.sh --product-name rk3568 --build-target ace_engine_test --gn-args ace_engine_feature_enable_coverage=true
```

**Build specific ace_engine test with coverage**:
```bash
# Build a specific test target in ace_engine with coverage
./build.sh --product-name rk3568 --build-target <test_target_name> --gn-args ace_engine_feature_enable_coverage=true
```

**Example: Build ui_content_stub_unittest with coverage**:
```bash
# Navigate to OpenHarmony root first
cd "$(find_root)"

# Build specific ace_engine test with coverage
./build.sh --product-name rk3568 --build-target ui_content_stub_unittest --gn-args ace_engine_feature_enable_coverage=true
```

**Build global unittest with coverage (ace_engine only)**:
```bash
# Build global unittest - coverage parameter ONLY applies to ace_engine tests
# Other repositories' tests are NOT affected by the coverage parameter
./build.sh --product-name rk3568 --build-target unittest --gn-args ace_engine_feature_enable_coverage=true
```

**Note**: When using `--gn-args ace_engine_feature_enable_coverage=true` with global `unittest` target:
- ✅ ace_engine tests will be built with coverage instrumentation
- ✅ Other repositories' tests will be built normally (without coverage)
- ✅ No errors or warnings will occur
- 💡 This is the recommended approach when you want coverage for ace_engine tests within a full test build

**Key parameters**:
- `--build-target <test_target_name>` - Specify the test target name (without GN path format like `//path:target`)
- `--gn-args ace_engine_feature_enable_coverage=true` - Enable code coverage instrumentation (ONLY for ace_engine targets)

**Important notes**:
- ✅ Use simple target name (e.g., `ui_content_stub_unittest`), NOT full GN path (`//foundation/arkui/...:target`)
- ✅ Coverage flag ONLY affects ace_engine repository targets
- ✅ Other repositories' tests are unaffected when coverage parameter is used
- ✅ Safe to use with `unittest` target - enables coverage for ace_engine tests only
- ✅ Coverage builds generate additional instrumentation data for code coverage analysis
- ✅ Test executable location: `out/<product>/tests/ace_engine/unittest/<path>/<test_target_name>`

**Common ace_engine test target examples**:
```bash
# UI content stub test (ace_engine repository)
./build.sh --product-name rk3568 --build-target ui_content_stub_unittest --gn-args ace_engine_feature_enable_coverage=true

# Text pattern test (ace_engine repository)
./build.sh --product-name rk3568 --build-target text_pattern_test --gn-args ace_engine_feature_enable_coverage=true

# Button pattern test (ace_engine repository)
./build.sh --product-name rk3568 --build-target button_pattern_test --gn-args ace_engine_feature_enable_coverage=true
```

**When to use coverage builds**:
- Measuring code coverage for ace_engine test suites
- Validating test completeness for ace_engine components
- Generating coverage reports for ace_engine code
- Quality assurance and metrics collection for ACE Engine

**Target compatibility**:
| Target | Coverage Effect | Command |
|--------|----------------|---------|
| `ace_engine_test` | ✅ ace_engine tests with coverage | `./build.sh --product-name rk3568 --build-target ace_engine_test --gn-args ace_engine_feature_enable_coverage=true` |
| `ui_content_stub_unittest` | ✅ ace_engine test with coverage | `./build.sh --product-name rk3568 --build-target ui_content_stub_unittest --gn-args ace_engine_feature_enable_coverage=true` |
| `<other_ace_engine_test>` | ✅ ace_engine test with coverage | `./build.sh --product-name rk3568 --build-target <test_name> --gn-args ace_engine_feature_enable_coverage=true` |
| `unittest` (global) | ✅ ace_engine with coverage, others normal | `./build.sh --product-name rk3568 --build-target unittest --gn-args ace_engine_feature_enable_coverage=true` |

**Note**: When using `--gn-args ace_engine_feature_enable_coverage=true` with `unittest`:
- ace_engine repository tests → built with coverage instrumentation
- Other repositories' tests → built normally (without coverage)
- No errors or conflicts occur

### Fast Rebuild (Skip GN Generation)

When no GN files (BUILD.gn, *.gni) have been modified, use `--fast-rebuild` to skip GN generation:

```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache --fast-rebuild
```

**When to use fast rebuild**:
- Only source code (.cpp, .h, .ts, .ets) has changed
- No build configuration files (BUILD.gn, *.gni) modified
- Incremental development iteration

**Fast rebuild benefits**:
- Skips GN parse and generation phase
- Directly uses existing ninja build files
- Significantly faster for code-only changes
- Typical speedup: 30-50% faster

**When NOT to use fast rebuild**:
- BUILD.gn files modified
- New dependencies added
- Build configuration changed
- First time building or after cleaning output

### Fast Build for Component

Combine fast rebuild with component build for maximum speed:

```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache --fast-rebuild
```

### Fast Build for Tests

Combine fast rebuild with test builds for rapid iteration:

**Build ACE Engine tests (fast with coverage)**:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine_test --gn-args ace_engine_feature_enable_coverage=true --ccache --fast-rebuild
```

**Build all unit tests (fast with ace_engine coverage)**:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target unittest --gn-args ace_engine_feature_enable_coverage=true --ccache --fast-rebuild
```

**Recommendation**: For ACE Engine development, prefer `ace_engine_test` with `--gn-args ace_engine_feature_enable_coverage=true` and `--fast-rebuild` for fastest iteration when only test code has changed. Coverage instrumentation is recommended for all ace_engine test builds.

### Build Test Target List

**Build specified test targets from a list file**:

This feature allows you to build a custom list of test targets sequentially. If any test target fails to build, the process stops and does not continue with remaining targets.

**Trigger keywords**:
- "编译测试列表" / "build test list"
- "按列表编译测试" / "compile tests from list"
- "编译指定测试" / "build specified tests"

**unittest_targets.txt file location**:
- Searched in current ace_engine directory first
- Fallback to OpenHarmony root if not found in ace_engine
- File name must be exactly: `unittest_targets.txt`

**File format** (one target per line):
```txt
# Comments start with #
ace_engine_test
# Build specific test module
adapter/ohos/osal/system_properties_unittest
```

**Workflow**:
```bash
# 1. Create unittest_targets.txt in ace_engine directory
cd foundation/arkui/ace_engine
cat > unittest_targets.txt << EOF
# ACE Engine tests
ace_engine_test

# Specific test module
adapter/ohos/osal/system_properties_unittest
EOF

# 2. Navigate to OpenHarmony root
cd /home/sunfei/workspace/openHarmony

# 3. Build tests from the list
# For each target in file, runs: --build-target=<target>
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target=ace_engine_test --ccache
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target=adapter/ohos/osal/system_properties_unittest --ccache
```

**Key features**:
- ✅ Sequential compilation: Tests are built in the order listed in file
- ✅ Stop on error: Compilation stops immediately if a test target fails
- ✅ Uses `--build-target=`: Each target compiled with explicit `--build-target=<name>` parameter
- ✅ Comment support: Lines starting with # are ignored
- ✅ Empty lines: Blank lines are ignored
- ✅ Auto file discovery: Searches ace_engine directory first, then root

**Example: Creating target list**:
```bash
# Create file in ace_engine directory
cd foundation/arkui/ace_engine
cat > unittest_targets.txt << EOF
# Priority 1: Core ACE Engine tests
ace_engine_test

# Priority 2: Adapter tests
adapter/ohos/osal/system_properties_unittest
adapter/ohos/capability/feature_config_unittest
EOF
```

**Example: Building from list**:
```bash
# From OpenHarmony root
cd /home/sunfei/workspace/openHarmony

# Execute build (skill will read unittest_targets.txt and build each target sequentially)
# Equivalent to manually running:
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target=ace_engine_test --ccache
# Then if successful:
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target=adapter/ohos/osal/system_properties_unittest --ccache
# Then if successful:
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target=adapter/ohos/capability/feature_config_unittest --ccache
```

**Supported target types**:
- Full test targets: `--build-target=ace_engine_test`, `--build-target=unittest`
- Component/group targets: `--build-target=adapter/ohos/osal/*_unittest`
- Specific test modules: Any valid build-target path

**File discovery priority**:
1. `foundation/arkui/ace_engine/unittest_targets.txt` (ace_engine directory)
2. `unittest_targets.txt` (OpenHarmony root - fallback)

**Error handling**:
- **File not found**: Warning message displayed, normal build proceeds without list
- **Build failure**: Stops immediately, error extracted from failed target's build log
- **Recovery**: Fix error and re-run same command to continue from next target

**Disk space management**:
- **Problem**: Test artifacts can be very large, causing disk space issues during compilation
- **Solution**: Delete previously compiled test binaries to free up space
- **Safe deletion location**: `out/<product>/exe.unstripped/tests/unittest/ace_engine/`
- **⚠️ WARNING**: ONLY delete files in this specific directory, DO NOT delete files elsewhere
- **Resume strategy**: Continue compilation from the failed target, skip already verified targets
- **Goal**: Ensure all test targets in the list are successfully compiled

**Workflow for disk space recovery**:
```bash
# When disk space error occurs during test list compilation:

# 1. Navigate to test artifacts directory
cd "$OH_ROOT/out/<product>/exe.unstripped/tests/unittest/ace_engine/"

# 2. List current test binaries
ls -lh

# 3. Remove successfully compiled test binaries to free space
# Example: remove adapter_unittest, base_unittest (already verified)
rm -f adapter_unittest base_unittest bridge_unittest

# 4. Verify deletion (ensure only test binaries are removed)
ls -lh

# 5. Return to OpenHarmony root
cd "$OH_ROOT"

# 6. Resume compilation from the failed target
# Skip targets that were already successfully compiled
./build.sh --export-para PYCACHE_ENABLE:true --product-name <product> --build-target=<failed_target> --ccache
```

**Best practices for disk space management**:
- ✅ Keep track of which targets have been successfully compiled
- ✅ Only delete test binaries from `exe.unstripped/tests/unittest/ace_engine/` directory
- ✅ Verify file paths before deletion to avoid removing critical build artifacts
- ✅ Resume compilation from the first failed target after cleanup
- ✅ Document compilation progress to track remaining targets
- ❌ NEVER delete files from `out/<product>/libs/`, `out/<product>/packages/`, or other directories
- ❌ NEVER delete intermediate build files or object files
- ❌ NEVER delete build configuration files

**Progress tracking example**:
```bash
# Track compilation progress
# ✅ adapter_unittest - COMPLETED
# ✅ base_unittest - COMPLETED
# ✅ bridge_unittest - COMPLETED
# ❌ frameworks_unittest - FAILED (disk space error)
# ⏸️ interfaces_unittest - SKIPPED (waiting for frameworks_unittest)

# After cleanup, resume from frameworks_unittest
./build.sh --export-para PYCACHE_ENABLE:true --product-name <product> --build-target=frameworks_unittest --ccache

# Then continue with remaining targets
./build.sh --export-para PYCACHE_ENABLE:true --product-name <product> --build-target=interfaces_unittest --ccache
```

**Use cases**:
- Incremental test validation after focused code changes
- Building specific test modules for isolated testing
- Verifying fixes for specific test failures
- Splitting large test builds into sequential steps
- **Recovering from disk space errors during test list compilation**

### Build Process

Execute the build command and monitor the output. The build process:
1. Checks environment (Python, Node.js versions)
2. Initializes ohpm and dependencies
3. Runs the hb build system
4. Generates output in `out/` directory

## Success Verification

### Check Build Exit Code

A successful build exits with code 0 and displays:
```
=====build successful=====
```

### Verify Output

Check that the expected build artifacts exist in `out/`:

```bash
# Get OpenHarmony root dynamically
OH_ROOT=$(find_root)

# Check for product-specific output
ls -la "$OH_ROOT/out/<product-name>/"

# Example for rk3568:
ls -la "$OH_ROOT/out/rk3568/"
```

Look for key directories:
- `packages/` - Built packages
- `libs/` - Compiled libraries
- `bin/` - Executables

### Build Success Indicators

- Exit code is 0
- Success message displayed
- Expected artifacts in output directory
- No error messages in final output

## Failure Analysis

When build fails (exit code non-zero), analyze the error systematically.

### Locate Build Logs

**IMPORTANT: Always check the primary build log first**

Build logs are located in the `out/` directory structure. The primary build log contains all build information and should be the first place to check for errors.

```bash
# Get OpenHarmony root dynamically
OH_ROOT=$(find_root)
```

**Primary build log (FIRST PRIORITY)**:
```bash
# Main build log - contains all errors and warnings
$OH_ROOT/out/<product-name>/build.log

# Example for rk3568:
$OH_ROOT/out/rk3568/build.log
```

**Component-specific logs (for detailed investigation)**:
```bash
# Check for component build failures
$OH_ROOT/out/<product-name>/logs/<component>/

# Example for ace_engine:
find "$OH_ROOT/out/rk3568/logs" -name "*ace_engine*" -type f
```

**Common log locations** (in order of priority):
1. **`$OH_ROOT/out/<product>/build.log`** - Main build log ⭐ **ALWAYS CHECK THIS FIRST**
2. `$OH_ROOT/out/<product>/logs/` - Detailed component logs
3. **`$OH_ROOT/out/sdk/build.log`** - SDK build log ⚠️ **SPECIAL CASE**: SDK output is in `out/sdk/`, NOT `out/ohos-sdk/`

**Output directory mapping**:
- Regular products: `out/<product>/build.log` (e.g., `out/rk3568/build.log`)
- SDK product: `out/sdk/build.log` ⚠️ Special case, different directory structure

### Analyze Build Errors

Use the error analysis script to extract and summarize errors:

```bash
# Get OpenHarmony root dynamically
OH_ROOT=$(find_root)

# Use the provided analysis script
"$OH_ROOT/foundation/arkui/ace_engine/.claude/skills/openharmony-build/scripts/analyze_build_error.sh" <product-name>
```

**Manual error search**:
```bash
# Get OpenHarmony root dynamically
OH_ROOT=$(find_root)

# Search for error patterns in build log
grep -i "error" "$OH_ROOT/out/<product>/build.log" | tail -50

# Find fatal errors
grep -i "fatal" "$OH_ROOT/out/<product>/build.log"

# Search for specific failure patterns
grep -A 10 "FAILED" "$OH_ROOT/out/<product>/build.log"
```

### Common Build Failure Patterns

**Compilation errors**:
```
error: undefined reference to 'symbol'
error: 'header_file' not found
```

**Link errors**:
```
ld: error: undefined symbol
ld: cannot find -l<library>
```

**Dependency errors**:
```
error: package 'package-name' not found
error: dependency 'dependency-name' not satisfied
```

**Configuration errors**:
```
error: invalid product name
error: build target not found
```

## Error Resolution Workflow

1. **Check primary build log**: Always start with `$OH_ROOT/out/<product>/build.log`
2. **Identify the error**: Use `analyze_build_error.sh` to extract errors from build.log
3. **Locate the source**: Find the file and line number causing the error
4. **Understand the cause**: Read surrounding context in the build.log
5. **Propose solution**: Based on error type and context
6. **Verify fix**: Rebuild to confirm resolution

**Key Principle**: The primary build log (`out/<product>/build.log`) contains all build information including GN generation, ninja compilation, linking, and packaging errors. Always check this file first before looking at component-specific logs.

## Additional Resources

### Scripts

- **`scripts/analyze_build_error.sh`** - Extract and summarize build errors
- **`scripts/find_recent_errors.sh`** - Find recent build failures

### Reference Files

- **`references/build-commands.md`** - Complete build command reference
- **`references/common-errors.md`** - Common build errors and solutions
- **`references/log-locations.md`** - Detailed log file locations

## Best Practices

- Always find OpenHarmony root dynamically using `.gn` file as marker
- Use cache options (`--export-para PYCACHE_ENABLE:true --ccache`) for faster builds
- Use `--fast-rebuild` when only code changed (no GN modifications)
- Search for errors from the end of log files (most recent first)
- Preserve full error context including line numbers
- Check both main build log and component-specific logs
- Verify environment setup (Python, Node.js versions) before building

### Build Strategy Guide

**First time build or major changes**:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache
```

**Code-only changes (fastest)**:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --ccache --fast-rebuild
```

**Component development**:
```bash
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine --ccache --fast-rebuild
```

**Test development (ace_engine tests with coverage)**:
```bash
# Recommended: Always include coverage parameter for ace_engine tests
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target ace_engine_test --gn-args ace_engine_feature_enable_coverage=true --ccache --fast-rebuild

# Specific ace_engine test with coverage
./build.sh --export-para PYCACHE_ENABLE:true --product-name rk3568 --build-target <test_name> --gn-args ace_engine_feature_enable_coverage=true --ccache
```

**⭐ Recommended practice**: When building ace_engine_test or ace_engine test targets, ALWAYS include `--gn-args ace_engine_feature_enable_coverage=true` to enable code coverage instrumentation for better quality assurance.

### Dynamic Path Finding Helper

Use this helper function in all scripts and commands:

```bash
# Define function to find OpenHarmony root
find_oh_root() {
    local dir="$(pwd)"
    while [[ ! -f "$dir/.gn" ]]; do
        dir="$(dirname "$dir")"
        if [[ "$dir" == "/" ]]; then
            echo "Error: OpenHarmony root not found" >&2
            return 1
        fi
    done
    echo "$dir"
}

# Usage in commands
OH_ROOT=$(find_oh_root)
cd "$OH_ROOT" || exit 1
```

## Version History

- **0.6.0** (2026-02-10): 新增测试套件覆盖率编译支持
  - ✨ 添加测试覆盖率编译专门命令和参数
  - 📝 明确覆盖率编译参数：`--gn-args ace_engine_feature_enable_coverage=true`
  - ⚠️ 强调使用简单目标名称，不带 GN 路径格式（如 `//path:target`）
  - 📚 添加具体示例：`ui_content_stub_unittest` 覆盖率编译
  - 🎯 新增触发关键词："编译覆盖率版本"、"build coverage version"、"覆盖率编译"
  - 🔧 提供常用测试目标的覆盖率编译示例

- **0.5.0** (2026-02-02): 新增测试列表编译磁盘空间管理策略
  - 💾 添加磁盘空间不足时的处理方案
  - 🗑️ 指定安全删除测试产物的目录：`out/<product>/exe.unstripped/tests/unittest/ace_engine/`
  - ⚠️ 强调仅删除指定目录的文件，避免误删其他构建产物
  - 🔄 支持从失败的测试目标恢复编译，跳过已验证通过的目标
  - 📝 提供完整的磁盘空间恢复工作流和最佳实践
  - 📋 添加编译进度跟踪示例
  - 🔧 使用通用 `<product>` 占位符以支持不同产品

- **0.4.0** (2026-02-02): 新增测试目标列表编译功能
  - ✨ 添加测试目标列表编译功能
  - 📝 支持从 `unittest_targets.txt` 文件读取目标列表
  - 🎯 依次编译列表中的每个目标，使用 `--build-target=<target>` 参数
  - ⚠️ 遇到错误立即停止，不再编译后续目标
  - 🔄 优先在 ace_engine 目录搜索文件，回退到 OpenHarmony 根目录
  - 📋 新增触发关键词："编译测试列表"、"build test list"、"按列表编译测试"、"编译指定测试"

- **0.3.0** (2025-02-02): 新增 SDK 编译支持（ohos-sdk 产品）
  - ✨ 添加 SDK 编译专门命令和触发关键词
  - ⚠️ 特别说明：SDK 输出目录为 `out/sdk/` 而非 `out/ohos-sdk/`
  - 📝 添加 SDK 编译专门命令和触发关键词
  - 📚 更新产品列表，标注 SDK 的特殊输出目录
  - 🎯 新增触发关键词："编译 sdk"、"编译 SDK"、"build sdk"、"build SDK"、"编译 ohos-sdk"
  - 🔧 优化日志位置说明，明确 SDK 特殊目录结构

- **0.2.0** (2025-01-23): 新增 `ace_engine_test` 编译目标支持
  - ✨ 新增 `ace_engine_test` 编译目标支持
  - 📝 明确测试编译优先级：`ace_engine_test` > `unittest`
  - ⭐ 推荐使用 `ace_engine_test` 进行 ACE Engine 测试编译（更快）
  - 📚 更新所有文档和示例，添加测试编译说明
  - 🔧 优化测试编译工作流，支持快速编译测试用例
  - 🎯 新增触发关键词："编译测试"、"编译测试用例"、"build ace_engine_test"

