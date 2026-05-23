---
name: makefile
description: Makefile skill for the ikigai project
---

# Makefile

## Description

Build system for ikigai Linux coding agent with comprehensive testing, dynamic analysis, code quality, and multi-distribution packaging support.

## Check Target Requirements

**FUNDAMENTAL REQUIREMENT:** All check targets must have consistent, minimal output.

**Output format:**
- **Success**: Green circle (🟢) + filename
- **Failure**: Red circle (🔴) + filename
- **No other output**: No progress messages, no verbose logs, no noise

**The 10 check targets:**
1. `check-compile` - Compile all .c files to .o files
2. `check-link` - Link all binaries (main, tests, tools)
3. `check-filesize` - Verify files are under size limits
4. `check-unit` - Run unit tests
5. `check-integration` - Run integration tests
6. `check-complexity` - Check cyclomatic complexity and nesting depth
7. `check-sanitize` - Run tests with AddressSanitizer and UndefinedBehaviorSanitizer
8. `check-tsan` - Run tests with ThreadSanitizer
9. `check-valgrind` - Run tests under Valgrind Memcheck
10. `check-helgrind` - Run tests under Valgrind Helgrind

All checks must behave identically in output format.

## Build

- `make all` - Build the ikigai client binary with default debug configuration.
- `make release` - Clean and rebuild the client in release mode with optimizations.
- `make clean` - Remove all build artifacts, coverage data, reports, and distribution packages.
- `make check-compile` - Compile all .c files (src + tests) to .o files. Emits 🟢/🔴 per file.
- `make check-compile FILE=src/foo.c` - Compile only the specified file + dependencies.
- `make check-link` - Link all binaries (client, tests, tools). Emits 🟢/🔴 per binary.
- `make check-link FILE=build/debug/tests/unit/foo_test` - Link only the specified binary.

## Installation

- `make install` - Install the ikigai binary and config files to PREFIX (default /usr/local).
- `make uninstall` - Remove installed binary and configuration files from the system.
- `make install-deps` - Install build dependencies using the system package manager.

## Testing

- `make check` - Build and run all tests in parallel (unit and integration).
- `make check TEST=name` - Build and run a single test matching the specified name.
- `make check-unit` - Build and run only unit tests in parallel.
- `make check-integration` - Build and run only integration and database tests.

## Mock Verification

- `make verify-mocks` - Verify OpenAI mock fixtures against real API responses.
- `make verify-mocks-anthropic` - Verify Anthropic mock fixtures against real API responses.
- `make verify-mocks-google` - Verify Google mock fixtures against real API responses.
- `make verify-mocks-all` - Verify all provider mock fixtures against real APIs.
- `make verify-credentials` - Validate API keys in ~/.config/ikigai/credentials.json.

## VCR Recording

- `make vcr-record-openai` - Re-record OpenAI VCR fixtures with real API calls.
- `make vcr-record-anthropic` - Re-record Anthropic VCR fixtures with real API calls.
- `make vcr-record-google` - Re-record Google VCR fixtures with real API calls.
- `make vcr-record-all` - Re-record all provider VCR fixtures.

## Dynamic Analysis

- `make check-sanitize` - Run all tests with AddressSanitizer and UndefinedBehaviorSanitizer.
- `make check-valgrind` - Run all tests under Valgrind Memcheck for memory leak detection.
- `make check-helgrind` - Run all tests under Valgrind Helgrind for thread error detection.
- `make check-tsan` - Run all tests with ThreadSanitizer for race condition detection.
- `make check-dynamic` - Run all dynamic analysis checks sequentially (or parallel with PARALLEL=1).

## Quality Assurance

- `make check-coverage` - Generate code coverage report and enforce coverage thresholds.
- `make coverage-map` - Generate source file to test mapping for targeted coverage runs.
- `make lint` - Run all lint checks (complexity and filesize).
- `make check-complexity` - Check cyclomatic complexity and nesting depth against thresholds.
- `make check-filesize` - Verify all source and documentation files are below size limits.
- `make ci` - Run complete CI pipeline (lint, coverage, all tests, all dynamic analysis).

## Code Formatting

- `make fmt` - Format all source code using uncrustify with project style guide.
- `make tags` - Generate ctags index for source code navigation.
- `make cloc` - Count lines of code in source, tests, and Makefile.

## Distribution

- `make dist` - Create source distribution tarball for packaging.
- `make distro-images` - Build Docker images for all supported distributions.
- `make distro-images-clean` - Remove all Docker images for supported distributions.
- `make distro-clean` - Clean build artifacts using Docker container.
- `make distro-check` - Run full CI checks on all supported distributions via Docker.
- `make distro-package` - Build distribution packages (deb, rpm) for all supported distributions.

## Utility

- `make help` - Display detailed help for all available targets and build modes.
- `make clean-test-runs` - Remove test run sentinel files used for parallel execution.

## Build Modes

| Mode | Flags | Purpose |
|------|-------|---------|
| `BUILD=debug` | `-O0 -g3 -DDEBUG` | Default build with full debug symbols and no optimization |
| `BUILD=release` | `-O2 -g -DNDEBUG -D_FORTIFY_SOURCE=2` | Optimized production build with security hardening |
| `BUILD=sanitize` | `-O0 -g3 -fsanitize=address,undefined` | Debug build with address and undefined behavior sanitizers |
| `BUILD=tsan` | `-O0 -g3 -fsanitize=thread` | Debug build with thread sanitizer for race detection |
| `BUILD=valgrind` | `-O0 -g3 -fno-omit-frame-pointer` | Debug build optimized for Valgrind analysis |

## Common Workflows

```bash
# Development workflow
make clean && make all               # Clean build in debug mode
make check                           # Run all tests
make fmt                             # Format code before commit

# Single test execution
make check TEST=config_test          # Run only config_test

# Quality assurance
make lint                            # Check complexity and file sizes
make check-coverage                  # Generate coverage report
make check-dynamic                   # Run all sanitizers and Valgrind

# Release workflow
make release                         # Build optimized release binary
make ci                              # Run full CI pipeline

# Distribution workflow
make dist                            # Create source tarball
make distro-images                   # Build Docker images
make distro-package                  # Build deb/rpm packages

# Custom builds
make all BUILD=release               # Build in release mode
make check BUILD=sanitize            # Run tests with sanitizers
make check-coverage COVERAGE_THRESHOLD=95  # Require 95% coverage

# Distribution testing
make distro-check DISTROS="debian"   # Test only on Debian
make distro-package DISTROS="fedora ubuntu"  # Build packages for specific distros

# Parallel execution
make -j8 check                       # Run tests with 8 parallel jobs
make check-dynamic PARALLEL=1        # Run sanitizers in parallel

# VCR fixture recording
VCR_RECORD=1 make check-unit         # Re-record fixtures during test run
make vcr-record-openai               # Re-record all OpenAI fixtures
```

## Tool Build Pattern

```makefile
tool_name_tool: libexec/ikigai/tool-name-tool

libexec/ikigai/tool-name-tool: src/tools/tool_name/main.c $(TOOL_COMMON_SRCS) | libexec/ikigai
	@$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ -ltalloc && echo "🔗 $@" || (echo "🔴 $@" && exit 1)
```

**Critical:** `$(LDFLAGS)` must come before `-o $@ $^`, not after. Libraries go at the end.

## Test File Naming Convention

**CRITICAL:** Only two file endings are allowed in the `tests/` directory:

1. **`*_test.c`** - Test files that build into test binaries
2. **`*_helper.c`** - Helper files used by tests (stubs, mocks, utilities)

Any other naming pattern is invalid and must be renamed to match one of these patterns.

## Important Notes

- Never run parallel make with different targets - different BUILD modes use incompatible flags.
- Always stay in project root - use relative paths instead of changing directories.
- Default BUILD mode is debug; specify BUILD=release for optimized builds.
- Coverage requires 90% line, function, and branch coverage by default.
- Maximum file size is 16384 bytes for all non-vendor source and documentation files.
- Cyclomatic complexity threshold is 15, nesting depth threshold is 5.
- Vendor files (yyjson, fzy) compile with relaxed warnings.
- Test binaries support parallel execution using .run sentinel files.
- Signal tests are skipped when running with sanitizers (SKIP_SIGNAL_TESTS=1).
