---
name: run-full-test-suite
description: Executes comprehensive test suite across unit, integration, E2E, database, protocols, and intelligence algorithms
user-invocable: true
---

# Run Full Test Suite Skill

## Purpose
Executes comprehensive test suite across all categories: unit, integration, E2E, database, protocols, and intelligence algorithms.

## CLAUDE.md Compliance
- ✅ Runs all deterministic tests
- ✅ Uses synthetic data (no external dependencies)
- ✅ Tests both success and error paths
- ✅ Validates code quality

## Usage
Run this skill:
- Before committing code
- Before pull requests
- Before releases
- After major refactoring
- Daily CI validation

## Prerequisites
- Cargo and Rust toolchain
- Test dependencies installed

## Commands

### Full Test Suite
```bash
# Run ALL tests (unit + integration + doc tests)
cargo test --all-features
```

### Full CI Suite
```bash
# Run the full CI validation suite
./scripts/ci/lint-and-test.sh
```

### Specific Test Categories

#### Unit Tests
```bash
# All library unit tests
cargo test --lib -- --quiet
```

#### Integration Tests
```bash
# All integration tests
cargo test --test '*' -- --quiet

# Specific integration test
cargo test --test mcp_multitenant_complete_test -- --nocapture
```

#### Doc Tests
```bash
# Documentation example tests
cargo test --doc -- --quiet
```

#### Intelligence Tests
```bash
# Basic intelligence algorithms
cargo test --test intelligence_tools_basic_test -- --nocapture

# Advanced intelligence algorithms
cargo test --test intelligence_tools_advanced_test -- --nocapture
```

#### Protocol Tests
```bash
# MCP protocol tests
cargo test protocol -- --quiet

# OAuth tests
cargo test oauth -- --quiet

# Authentication tests
cargo test auth -- --quiet
```

#### Database Tests
```bash
# Database abstraction layer
cargo test database --lib -- --quiet

# Database plugins (SQLite)
cargo test --test database_plugins_comprehensive_test --features sqlite

# PostgreSQL (requires Docker)
./scripts/testing/test-postgres.sh
```

### Performance Testing
```bash
# Run benchmarks (if configured)
cargo bench --bench '*' || echo "No benchmarks configured"
```

### Parallel vs Sequential
```bash
# Parallel execution (default, faster)
cargo test --all-features

# Sequential execution (for database tests with shared state)
cargo test --all-features -- --test-threads=1
```

## Test Output Modes

### Quiet Mode (Summary Only)
```bash
# Show only pass/fail summary
cargo test --all-features --quiet
```

### Verbose Mode (Show Output)
```bash
# Show println! and debug output
cargo test --all-features -- --nocapture
```

### Show Only Failures
```bash
# Run tests and show only failures
cargo test --all-features 2>&1 | grep -A 10 "FAILED"
```

## Test Filtering

### By Name
```bash
# Run specific test
cargo test test_vdot_calculation

# Run tests matching pattern
cargo test multitenant

# Run tests in specific module
cargo test intelligence::algorithms
```

### By Feature Flag
```bash
# Test with specific features
cargo test --features sqlite
cargo test --features postgresql
cargo test --features testing
```

### Exclude Tests
```bash
# Skip expensive tests
cargo test --all-features -- --skip test_expensive_operation

# Skip integration tests
cargo test --lib
```

## Success Criteria
- ✅ All unit tests pass (>100 tests)
- ✅ All integration tests pass (>50 tests)
- ✅ All doc tests pass
- ✅ No flaky tests
- ✅ No ignored tests without explanation
- ✅ Test coverage > 80%
- ✅ No test failures in CI
- ✅ All tests complete in < 5 minutes

## Quick Test Commands Cheat Sheet

```bash
# Fast check (unit tests only)
cargo test --lib --quiet

# Full test suite
cargo test --all-features

# Specific test with output
cargo test test_name -- --nocapture

# Multi-tenant isolation
cargo test --test mcp_multitenant_complete_test

# Intelligence algorithms
cargo test --test intelligence_tools_basic_test

# Database tests
cargo test database

# Protocol compliance
cargo test protocol

# Authentication
cargo test auth oauth

# Full CI validation
./scripts/ci/lint-and-test.sh
```

## Related Files
- `scripts/ci/lint-and-test.sh` - Full CI validation suite
- `tests/` - Integration tests directory
- `tests/common.rs` - Shared test utilities

## Related Skills
- `test-multitenant-isolation` - Multi-tenant testing
- `test-intelligence-algorithms` - Algorithm validation
- `test-mcp-compliance` - Protocol compliance
