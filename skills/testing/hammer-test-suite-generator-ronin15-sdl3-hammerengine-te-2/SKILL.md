---
name: hammer-test-suite-generator
description: Generates complete test suite infrastructure (test scripts, functional tests, benchmark tests, output directories, CMake integration) for a new SDL3 HammerEngine system or manager following project conventions. Use when adding a new manager or system that needs testing infrastructure.
allowed-tools: [Read, Write, Bash, Edit, Grep]
---

# HammerEngine Test Suite Generator

This Skill automates the creation of standardized test infrastructure for new SDL3 HammerEngine systems. It generates all necessary files following the project's established patterns.

## What This Skill Generates

1. **Test Script** (`tests/test_scripts/run_<system>_tests.sh`)
2. **Functional Test Source** (`tests/<system>_tests.cpp`)
3. **Benchmark Test Source** (`tests/<system>_benchmark.cpp`) - Optional
4. **CMakeLists.txt Updates** - Add test executable targets
5. **Master Test Runner Update** - Add to `run_all_tests.sh`
6. **Output Directory Structure** - Create `test_results/<system>/`
7. **Documentation Stub** - Basic testing documentation

## User Input Collection

**Ask the user for:**

1. **System Name** (e.g., "AnimationManager", "SoundSystem")
   - Used for file naming and test suite naming
   - Must be PascalCase

2. **Manager Class Name** (e.g., "AnimationManager", "SoundManager")
   - The actual C++ class being tested
   - Must match existing class in codebase

3. **Test Categories** (checkboxes):
   - [ ] Functional Tests (always recommended)
   - [ ] Integration Tests (if integrates with other systems)
   - [ ] Benchmark Tests (if performance-critical)

4. **Integration Dependencies** (if applicable):
   - List of other systems this integrates with
   - Example: "AIManager, CollisionManager"

5. **Key Functionality** (brief description):
   - What does this system do?
   - Used for test case generation

## Generation Process

### Step 1: Read Template Pattern

**Reference Template:**
```bash
# Read existing test script to extract pattern
Read: $PROJECT_ROOT/tests/test_scripts/run_ai_optimization_tests.sh
```

**Common Pattern Elements:**
1. Shebang: `#!/bin/bash`
2. Color codes for output (RED, GREEN, YELLOW, RESET)
3. Project root discovery
4. Argument parsing (`--verbose`, `--help`, `--debug`, `--release`)
5. Test executable path resolution
6. Timeout protection (default 30s for functional, 120s for benchmarks)
7. Output redirection to `test_results/`
8. Success/failure status reporting
9. Cleanup instructions

### Step 2: Generate Test Script

**Template:**

```bash
#!/bin/bash

# Copyright (c) 2025 Hammer Forged Games
# All rights reserved.
# Licensed under the MIT License - see LICENSE file for details

# Test runner for <SystemName> tests
# Usage: ./run_<system>_tests.sh [--verbose] [--debug] [--release] [--help]

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

# Find project root (directory containing CMakeLists.txt)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Default values
BUILD_TYPE="debug"
VERBOSE=""
TIMEOUT_DURATION=30

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose)
            VERBOSE="--log_level=all"
            shift
            ;;
        --debug)
            BUILD_TYPE="debug"
            shift
            ;;
        --release)
            BUILD_TYPE="release"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --verbose    Enable verbose test output"
            echo "  --debug      Run debug build tests (default)"
            echo "  --release    Run release build tests"
            echo "  --help       Show this help message"
            echo ""
            echo "Description:"
            echo "  Runs <SystemName> functional tests"
            echo "  Tests: <brief-description>"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Test executable name
TEST_EXECUTABLE="<system>_tests"

# Determine test executable path
if [ "$BUILD_TYPE" = "release" ]; then
    TEST_PATH="$PROJECT_ROOT/bin/release/$TEST_EXECUTABLE"
else
    TEST_PATH="$PROJECT_ROOT/bin/debug/$TEST_EXECUTABLE"
fi

# Check if test executable exists
if [ ! -f "$TEST_PATH" ]; then
    echo -e "${RED}Error: Test executable not found at $TEST_PATH${RESET}"
    echo "Please build the project first:"
    echo "  cmake -B build/ -G Ninja -DCMAKE_BUILD_TYPE=Debug && ninja -C build"
    exit 1
fi

# Create output directory
OUTPUT_DIR="$PROJECT_ROOT/test_results/<system>"
mkdir -p "$OUTPUT_DIR"

# Output file
OUTPUT_FILE="$OUTPUT_DIR/<system>_test_results.txt"

# Run tests
echo -e "${BLUE}Running <SystemName> Tests...${RESET}"
echo "Executable: $TEST_PATH"
echo "Output: $OUTPUT_FILE"
echo ""

# Run with timeout protection
if command -v timeout &> /dev/null; then
    timeout ${TIMEOUT_DURATION}s "$TEST_PATH" $VERBOSE 2>&1 | tee "$OUTPUT_FILE"
    TEST_EXIT_CODE=${PIPESTATUS[0]}
elif command -v gtimeout &> /dev/null; then
    gtimeout ${TIMEOUT_DURATION}s "$TEST_PATH" $VERBOSE 2>&1 | tee "$OUTPUT_FILE"
    TEST_EXIT_CODE=${PIPESTATUS[0]}
else
    "$TEST_PATH" $VERBOSE 2>&1 | tee "$OUTPUT_FILE"
    TEST_EXIT_CODE=$?
fi

# Check results
echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ <SystemName> Tests PASSED${RESET}"
    exit 0
elif [ $TEST_EXIT_CODE -eq 124 ]; then
    echo -e "${RED}✗ <SystemName> Tests TIMEOUT (exceeded ${TIMEOUT_DURATION}s)${RESET}"
    echo "Possible infinite loop or performance issue"
    exit 3
else
    echo -e "${RED}✗ <SystemName> Tests FAILED (exit code: $TEST_EXIT_CODE)${RESET}"
    echo ""
    echo "To debug, run:"
    echo "  $TEST_PATH --verbose"
    echo ""
    exit 1
fi
```

**Substitutions:**
- `<SystemName>` → User-provided system name (e.g., "AnimationManager")
- `<system>` → Lowercase system name (e.g., "animation_manager")
- `<brief-description>` → User-provided key functionality
- `${TIMEOUT_DURATION}` → 30s for functional, 120s for benchmarks

**Save to:**
```
$PROJECT_ROOT/tests/test_scripts/run_<system>_tests.sh
```

**Make executable:**
```bash
chmod +x tests/test_scripts/run_<system>_tests.sh
```

### Step 3: Generate Functional Test Source

**Reference Template:**
```bash
# Read existing test file to extract pattern
Read: $PROJECT_ROOT/tests/ai_optimization_tests.cpp
```

**Template:**

```cpp
/* Copyright (c) 2025 Hammer Forged Games
 * All rights reserved.
 * Licensed under the MIT License - see LICENSE file for details
*/

#define BOOST_TEST_MODULE <SystemName>Tests
#include <boost/test/included/unit_test.hpp>

#include "<SystemName>.hpp"
// Include other dependencies as needed

/**
 * @file <system>_tests.cpp
 * @brief Functional tests for <SystemName>
 *
 * Test Categories:
 * - Construction/Destruction
 * - Basic Functionality
 * - Edge Cases
 * - Error Handling
 * - Thread Safety (if applicable)
 * - Integration (if applicable)
 */

// ============================================================================
// Test Fixtures
// ============================================================================

struct <SystemName>Fixture
{
    <SystemName>Fixture()
    {
        // Setup code
        BOOST_TEST_MESSAGE("Setting up <SystemName> test fixture");
    }

    ~<SystemName>Fixture()
    {
        // Cleanup code
        BOOST_TEST_MESSAGE("Tearing down <SystemName> test fixture");
    }

    // Helper members
    // <SystemName>* mp_system = nullptr;
};

// ============================================================================
// Construction/Destruction Tests
// ============================================================================

BOOST_FIXTURE_TEST_SUITE(<SystemName>TestSuite, <SystemName>Fixture)

BOOST_AUTO_TEST_CASE(TestConstruction)
{
    BOOST_TEST_MESSAGE("Testing <SystemName> construction");

    // Test default construction
    <SystemName> system;

    // Verify initial state
    // BOOST_CHECK_EQUAL(system.getSomeValue(), expectedValue);

    BOOST_TEST_MESSAGE("<SystemName> construction test passed");
}

BOOST_AUTO_TEST_CASE(TestDestruction)
{
    BOOST_TEST_MESSAGE("Testing <SystemName> destruction");

    // Create and destroy system
    {
        <SystemName> system;
        // Use system
    }

    // Verify proper cleanup (no leaks, resources released)
    BOOST_CHECK(true); // Placeholder

    BOOST_TEST_MESSAGE("<SystemName> destruction test passed");
}

// ============================================================================
// Basic Functionality Tests
// ============================================================================

BOOST_AUTO_TEST_CASE(TestBasicFunctionality)
{
    BOOST_TEST_MESSAGE("Testing <SystemName> basic functionality");

    <SystemName> system;

    // Test key functionality based on user input
    // Example:
    // system.initialize();
    // BOOST_CHECK(system.isInitialized());

    BOOST_TEST_MESSAGE("<SystemName> basic functionality test passed");
}

// ============================================================================
// Edge Cases
// ============================================================================

BOOST_AUTO_TEST_CASE(TestEdgeCases)
{
    BOOST_TEST_MESSAGE("Testing <SystemName> edge cases");

    <SystemName> system;

    // Test boundary conditions
    // Test null inputs
    // Test empty states
    // Test maximum values

    BOOST_CHECK(true); // Placeholder

    BOOST_TEST_MESSAGE("<SystemName> edge case test passed");
}

// ============================================================================
// Error Handling
// ============================================================================

BOOST_AUTO_TEST_CASE(TestErrorHandling)
{
    BOOST_TEST_MESSAGE("Testing <SystemName> error handling");

    <SystemName> system;

    // Test error conditions
    // Verify exceptions thrown correctly
    // Verify error codes returned

    // Example:
    // BOOST_CHECK_THROW(system.invalidOperation(), std::runtime_error);

    BOOST_TEST_MESSAGE("<SystemName> error handling test passed");
}

// ============================================================================
// Thread Safety Tests (if applicable)
// ============================================================================

// Only include if system is used in multi-threaded context
#ifdef THREAD_SAFETY_TESTS

BOOST_AUTO_TEST_CASE(TestThreadSafety)
{
    BOOST_TEST_MESSAGE("Testing <SystemName> thread safety");

    <SystemName> system;

    // Test concurrent access
    // Verify mutex protection
    // Check for race conditions

    BOOST_CHECK(true); // Placeholder - implement actual threading test

    BOOST_TEST_MESSAGE("<SystemName> thread safety test passed");
}

#endif

// ============================================================================
// Integration Tests (if applicable)
// ============================================================================

// Only include if system integrates with others
#ifdef INTEGRATION_TESTS

BOOST_AUTO_TEST_CASE(TestIntegrationWith<OtherSystem>)
{
    BOOST_TEST_MESSAGE("Testing <SystemName> integration with <OtherSystem>");

    <SystemName> system;
    // <OtherSystem> otherSystem;

    // Test interaction between systems
    // Verify data flow
    // Check synchronization

    BOOST_CHECK(true); // Placeholder

    BOOST_TEST_MESSAGE("<SystemName> integration test passed");
}

#endif

BOOST_AUTO_TEST_SUITE_END()

// ============================================================================
// Entry Point
// ============================================================================

// Boost.Test automatically generates main() with BOOST_TEST_MODULE
```

**Substitutions:**
- `<SystemName>` → User-provided class name (PascalCase)
- `<system>` → Lowercase system name
- `<OtherSystem>` → Integration dependency names (if applicable)

**Customization Based on User Input:**
- If "Integration Tests" selected, include `#define INTEGRATION_TESTS`
- If system is manager (multi-threaded), include `#define THREAD_SAFETY_TESTS`
- Generate specific test cases based on "Key Functionality" description

**Save to:**
```
$PROJECT_ROOT/tests/<system>_tests.cpp
```

### Step 4: Generate Benchmark Test Source (Optional)

**Only if user selects "Benchmark Tests"**

**Template:**

```cpp
/* Copyright (c) 2025 Hammer Forged Games
 * All rights reserved.
 * Licensed under the MIT License - see LICENSE file for details
*/

#define BOOST_TEST_MODULE <SystemName>Benchmark
#include <boost/test/included/unit_test.hpp>

#include "<SystemName>.hpp"
#include <chrono>
#include <iostream>
#include <fstream>

/**
 * @file <system>_benchmark.cpp
 * @brief Performance benchmarks for <SystemName>
 *
 * Benchmark Categories:
 * - Throughput Testing
 * - Latency Measurement
 * - Scaling Analysis
 * - Resource Usage
 */

// ============================================================================
// Benchmark Helpers
// ============================================================================

class BenchmarkTimer
{
public:
    void start()
    {
        m_start = std::chrono::high_resolution_clock::now();
    }

    double stop()
    {
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> duration = end - m_start;
        return duration.count();
    }

private:
    std::chrono::high_resolution_clock::time_point m_start;
};

void saveMetric(const std::string& name, double value, const std::string& unit)
{
    // NOTE: Requires PROJECT_ROOT environment variable
    const char* root = std::getenv("PROJECT_ROOT");
    std::string path = root ? std::string(root) + "/test_results/<system>/performance_metrics.txt"
                            : "test_results/<system>/performance_metrics.txt";
    std::ofstream file(path, std::ios::app);
    file << name << ": " << value << " " << unit << std::endl;
    std::cout << name << ": " << value << " " << unit << std::endl;
}

// ============================================================================
// Benchmark Fixture
// ============================================================================

struct <SystemName>BenchmarkFixture
{
    <SystemName>BenchmarkFixture()
    {
        BOOST_TEST_MESSAGE("Setting up <SystemName> benchmark fixture");
        // Create output directory (requires PROJECT_ROOT environment variable)
        system("mkdir -p \"$PROJECT_ROOT/test_results/<system>\"");
        // Clear previous metrics
        system("rm -f \"$PROJECT_ROOT/test_results/<system>/performance_metrics.txt\"");
    }

    ~<SystemName>BenchmarkFixture()
    {
        BOOST_TEST_MESSAGE("Tearing down <SystemName> benchmark fixture");
    }

    BenchmarkTimer timer;
    // <SystemName> system;
};

// ============================================================================
// Throughput Benchmarks
// ============================================================================

BOOST_FIXTURE_TEST_SUITE(<SystemName>BenchmarkSuite, <SystemName>BenchmarkFixture)

BOOST_AUTO_TEST_CASE(BenchmarkThroughput_1K)
{
    BOOST_TEST_MESSAGE("Benchmarking <SystemName> throughput (1K operations)");

    const int OPERATIONS = 1000;
    <SystemName> system;

    timer.start();
    for (int i = 0; i < OPERATIONS; i++)
    {
        // Perform operation
        // system.doOperation();
    }
    double elapsed = timer.stop();

    double throughput = OPERATIONS / (elapsed / 1000.0); // ops/sec
    saveMetric("Throughput_1K", throughput, "ops/sec");
    saveMetric("Latency_1K", elapsed / OPERATIONS, "ms/op");

    BOOST_TEST_MESSAGE("Throughput (1K): " << throughput << " ops/sec");
}

BOOST_AUTO_TEST_CASE(BenchmarkThroughput_10K)
{
    BOOST_TEST_MESSAGE("Benchmarking <SystemName> throughput (10K operations)");

    const int OPERATIONS = 10000;
    <SystemName> system;

    timer.start();
    for (int i = 0; i < OPERATIONS; i++)
    {
        // Perform operation
        // system.doOperation();
    }
    double elapsed = timer.stop();

    double throughput = OPERATIONS / (elapsed / 1000.0);
    saveMetric("Throughput_10K", throughput, "ops/sec");
    saveMetric("Latency_10K", elapsed / OPERATIONS, "ms/op");

    BOOST_TEST_MESSAGE("Throughput (10K): " << throughput << " ops/sec");
}

// ============================================================================
// Scaling Benchmarks
// ============================================================================

BOOST_AUTO_TEST_CASE(BenchmarkScaling)
{
    BOOST_TEST_MESSAGE("Benchmarking <SystemName> scaling characteristics");

    <SystemName> system;

    // Test scaling from 100 to 10000 operations
    std::vector<int> sizes = {100, 500, 1000, 5000, 10000};

    for (int size : sizes)
    {
        timer.start();
        for (int i = 0; i < size; i++)
        {
            // Perform operation
            // system.doOperation();
        }
        double elapsed = timer.stop();

        double throughput = size / (elapsed / 1000.0);
        std::string metricName = "Throughput_" + std::to_string(size);
        saveMetric(metricName, throughput, "ops/sec");
    }

    BOOST_TEST_MESSAGE("<SystemName> scaling benchmark completed");
}

// ============================================================================
// Resource Usage Benchmarks
// ============================================================================

BOOST_AUTO_TEST_CASE(BenchmarkMemoryUsage)
{
    BOOST_TEST_MESSAGE("Benchmarking <SystemName> memory usage");

    // Measure memory usage with different loads
    // This is a placeholder - actual implementation depends on system

    <SystemName> system;

    // Estimate memory per operation
    // For actual measurement, consider using valgrind massif

    saveMetric("Estimated_Memory_Per_Op", 0.0, "bytes"); // Placeholder

    BOOST_TEST_MESSAGE("<SystemName> memory usage benchmark completed");
}

BOOST_AUTO_TEST_SUITE_END()

// ============================================================================
// Benchmark Summary
// ============================================================================

struct BenchmarkSummaryFixture
{
    ~BenchmarkSummaryFixture()
    {
        const char* root = std::getenv("PROJECT_ROOT");
        std::string resultsPath = root ? std::string(root) + "/test_results/<system>/performance_metrics.txt"
                                        : "test_results/<system>/performance_metrics.txt";
        BOOST_TEST_MESSAGE("=== <SystemName> Benchmark Summary ===");
        BOOST_TEST_MESSAGE("Results saved to: " << resultsPath);
        BOOST_TEST_MESSAGE("Review metrics for performance analysis");
    }
};

BOOST_FIXTURE_TEST_SUITE(SummaryGeneration, BenchmarkSummaryFixture)

BOOST_AUTO_TEST_CASE(GenerateSummary)
{
    // Generate summary report
    const char* root = std::getenv("PROJECT_ROOT");
    std::string reportPath = root ? std::string(root) + "/test_results/<system>/performance_report.md"
                                   : "test_results/<system>/performance_report.md";
    std::ofstream report(reportPath);
    report << "# <SystemName> Performance Report\n\n";
    report << "**Date:** " << __DATE__ << " " << __TIME__ << "\n\n";
    report << "## Metrics\n\n";
    report << "See `performance_metrics.txt` for detailed metrics.\n\n";
    report << "## Analysis\n\n";
    report << "TODO: Add performance analysis\n";
    report.close();

    BOOST_CHECK(true);
}

BOOST_AUTO_TEST_SUITE_END()
```

**Save to:**
```
$PROJECT_ROOT/tests/<system>_benchmark.cpp
```

### Step 5: Update CMakeLists.txt

**Read CMakeLists.txt:**
```bash
Read: $PROJECT_ROOT/CMakeLists.txt
```

**Add Test Executables:**

Find the section with test executable definitions (look for pattern like `add_executable(<test_name> tests/...)`).

**Add entries:**

```cmake
# <SystemName> Tests
add_executable(<system>_tests
    tests/<system>_tests.cpp
    # Add source files being tested
    src/managers/<SystemName>.cpp  # Adjust path as needed
)
target_link_libraries(<system>_tests PRIVATE ${SDL3_LIBRARY} Boost::unit_test_framework)
set_target_properties(<system>_tests PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/../bin/${CMAKE_BUILD_TYPE_LOWER}"
)

# <SystemName> Benchmark (if applicable)
add_executable(<system>_benchmark
    tests/<system>_benchmark.cpp
    src/managers/<SystemName>.cpp
)
target_link_libraries(<system>_benchmark PRIVATE ${SDL3_LIBRARY} Boost::unit_test_framework)
set_target_properties(<system>_benchmark PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/../bin/${CMAKE_BUILD_TYPE_LOWER}"
)
```

**Use Edit tool to add these entries after existing test definitions.**

### Step 6: Update Master Test Runner

**Read run_all_tests.sh:**
```bash
Read: $PROJECT_ROOT/run_all_tests.sh
```

**Add test to appropriate section:**

**For Functional Tests (--core-only section):**
```bash
# Add after existing core tests
echo -e "${BLUE}Running <SystemName> Tests...${RESET}"
./tests/test_scripts/run_<system>_tests.sh
check_status $? "<SystemName> Tests"
```

**For Benchmark Tests (--benchmarks-only section):**
```bash
# Add after existing benchmarks
echo -e "${BLUE}Running <SystemName> Benchmark...${RESET}"
./tests/test_scripts/run_<system>_benchmark.sh
check_status $? "<SystemName> Benchmark"
```

**Use Edit tool to add these entries in appropriate sections.**

### Step 7: Create Output Directory Structure

**Create directories:**
```bash
mkdir -p "$PROJECT_ROOT/test_results/<system>"
touch "$PROJECT_ROOT/test_results/<system>/.gitkeep"
```

### Step 8: Generate Documentation Stub

**Create test documentation:**

```markdown
# <SystemName> Testing

## Overview

Tests for <SystemName> functionality and performance.

## Test Suites

### Functional Tests
- **Location:** `tests/<system>_tests.cpp`
- **Runner:** `tests/test_scripts/run_<system>_tests.sh`
- **Coverage:**
  - Construction/Destruction
  - Basic Functionality
  - Edge Cases
  - Error Handling
  - Thread Safety (if applicable)

### Benchmark Tests
- **Location:** `tests/<system>_benchmark.cpp`
- **Runner:** `tests/test_scripts/run_<system>_benchmark.sh`
- **Metrics:**
  - Throughput (ops/sec)
  - Latency (ms/op)
  - Scaling characteristics
  - Resource usage

## Running Tests

```bash
# Functional tests
./tests/test_scripts/run_<system>_tests.sh --verbose

# Benchmarks
./tests/test_scripts/run_<system>_benchmark.sh --verbose

# All tests (included in master runner)
./run_all_tests.sh --core-only
./run_all_tests.sh --benchmarks-only
```

## Test Results

Results are saved to:
- `test_results/<system>/<system>_test_results.txt`
- `test_results/<system>/performance_metrics.txt`
- `test_results/<system>/performance_report.md`

## Adding New Tests

1. Add test case to `tests/<system>_tests.cpp`
2. Use `BOOST_AUTO_TEST_CASE` macro
3. Follow existing test patterns
4. Run tests to verify

## Performance Baselines

TODO: Document expected performance baselines for benchmarks.

## Known Issues

TODO: Document any known test issues or limitations.
```

**Save to:**
```
$PROJECT_ROOT/tests/docs/<SystemName>_Testing.md
```

### Step 9: Verification Build

**Build new test executables:**

```bash
cd $PROJECT_ROOT
cmake -B build/ -G Ninja -DCMAKE_BUILD_TYPE=Debug && ninja -C build
```

**Verify executables created:**
```bash
ls -lh bin/debug/<system>_tests
ls -lh bin/debug/<system>_benchmark  # if benchmark created
```

**Run initial test:**
```bash
./tests/test_scripts/run_<system>_tests.sh --verbose
```

## Output Summary

**Report to user:**

```markdown
# Test Suite Generated Successfully

## Files Created

### Test Scripts
- ✓ `tests/test_scripts/run_<system>_tests.sh`
- ✓ `tests/test_scripts/run_<system>_benchmark.sh` (if applicable)

### Test Source Files
- ✓ `tests/<system>_tests.cpp`
- ✓ `tests/<system>_benchmark.cpp` (if applicable)

### Documentation
- ✓ `tests/docs/<SystemName>_Testing.md`

### Directory Structure
- ✓ `test_results/<system>/`

## Files Modified

- ✓ `CMakeLists.txt` - Added test executable targets
- ✓ `run_all_tests.sh` - Added test to master runner

## Next Steps

1. **Implement Test Cases:**
   - Edit `tests/<system>_tests.cpp`
   - Replace placeholder tests with actual functionality tests
   - Based on: <user-provided-key-functionality>

2. **Build Tests:**
   ```bash
   cmake -B build/ -G Ninja -DCMAKE_BUILD_TYPE=Debug && ninja -C build
   ```

3. **Run Tests:**
   ```bash
   ./tests/test_scripts/run_<system>_tests.sh --verbose
   ```

4. **Customize Benchmarks** (if applicable):
   - Edit `tests/<system>_benchmark.cpp`
   - Add performance-specific test cases
   - Define performance baselines

5. **Add to CI/CD:**
   - Tests are automatically included in `run_all_tests.sh`
   - Will run with `--core-only` flag

## Test Executable Locations

- Debug: `bin/debug/<system>_tests`
- Release: `bin/release/<system>_tests`
- Benchmark: `bin/debug/<system>_benchmark`

## Running Generated Tests

```bash
# Individual test
./tests/test_scripts/run_<system>_tests.sh

# With verbose output
./tests/test_scripts/run_<system>_tests.sh --verbose

# As part of full suite
./run_all_tests.sh --core-only

# Benchmarks
./tests/test_scripts/run_<system>_benchmark.sh
./run_all_tests.sh --benchmarks-only
```

## Verification

Build status: <SUCCESS/FAILED>
Initial test run: <PASSED/FAILED/SKIPPED>

---

**Generated by:** hammer-test-suite-generator Skill
**Time saved:** ~30-45 minutes of manual scaffolding
```

## Usage Examples

When the user says:
- "generate tests for NewManager"
- "create test suite for AnimationSystem"
- "set up testing for SoundManager"
- "scaffold tests for new system"

Activate this Skill automatically.

## Important Notes

1. **Always ask for user input** before generating
2. **Verify class exists** in codebase before generating
3. **Follow naming conventions** (PascalCase classes, snake_case files)
4. **Include copyright headers** on all generated files
5. **Make scripts executable** after creation
6. **Verify CMake syntax** after modifications
7. **Test build** after generation to catch errors early

## Error Handling

**If system already has tests:**
- Ask user if they want to regenerate (will overwrite)
- Offer to add additional test cases instead

**If CMakeLists.txt modification fails:**
- Show generated CMake snippet
- Instruct user to add manually

**If build fails:**
- Show compilation errors
- Suggest fixes for common issues
- Offer to help debug

## Integration with Development Workflow

Use this Skill when:
- Adding new manager to project
- Creating new game system
- Implementing new feature that needs testing
- Standardizing existing tests to match project conventions

## Time Savings

**Manual Process:** ~30-45 minutes
- Write test script: 10-15 min
- Write test source: 15-20 min
- Update CMake: 5 min
- Update master runner: 3 min
- Create directories: 2 min
- Debug issues: 5-10 min

**With This Skill:** ~2-5 minutes
- Answer questions: 1-2 min
- Review generated code: 1-2 min
- Customize tests: 1 min

**Total Time Saved:** ~25-40 minutes per system
