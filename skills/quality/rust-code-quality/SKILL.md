---
name: rust-code-quality
description: Perform comprehensive Rust code quality reviews against best practices for async Rust, error handling, testing, and project structure
---

# Rust Code Quality Review Skill

Systematically review Rust code quality against industry best practices, focusing on async/Tokio patterns, error handling, module organization, testing, and documentation.

## Purpose

Ensure the Rust self-learning memory project follows:
- **Rust idioms** and best practices
- **Clean code principles** (readable, maintainable, testable)
- **Async/await patterns** with Tokio
- **Error handling** with Result types
- **Module organization** (<500 LOC per file)
- **Testing** (unit, integration, benchmarks)
- **Documentation** (rustdoc, examples)
- **Performance** (zero-copy, minimal allocations)
- **Security** (memory safety, input validation)

## Quick Reference

- **[Quality Dimensions](quality-dimensions.md)** - Detailed criteria, checks, and best practices for all 8 dimensions

## Quality Dimensions Overview

### 1. Project Structure & Organization
- Workspace organization
- Crate separation
- File size limits (<500 LOC)
- Module hierarchy

### 2. Error Handling
- Custom Error enum with thiserror
- Result<T> for fallible operations
- No unwrap() in production
- Meaningful error messages

### 3. Async/Await Patterns
- Proper async fn usage
- spawn_blocking for sync/CPU work
- No blocking in async context
- Concurrent operations

### 4. Memory & Performance
- Minimize allocations
- Borrowing over cloning
- Zero-copy where possible
- Streaming large datasets

### 5. Testing
- Unit tests (>90% coverage)
- Integration tests
- Benchmarks
- Property-based tests

### 6. Documentation
- Crate and module docs
- Function docs with examples
- Public API 100% documented
- README and CONTRIBUTING

### 7. Type Safety & API Design
- Strong typing (newtypes)
- Builder pattern
- Sealed traits
- Default implementations

### 8. Security & Safety
- No unsafe (unless necessary)
- Input validation
- SQL parameterization
- Environment secrets

See **[quality-dimensions.md](quality-dimensions.md)** for detailed criteria, check commands, and best practices for each dimension.

## Analysis Workflow

### Step 1: Project Structure Analysis
```bash
# Check workspace
cat Cargo.toml

# Verify crate organization
ls -la memory-*/

# Check file sizes
find . -name "*.rs" -not -path "*/target/*" -exec wc -l {} + | sort -rn
```

### Step 2: Code Pattern Analysis
```bash
# Error handling
rg "Result<|Error::" --glob "*.rs" | wc -l
rg "unwrap\(\)" --glob "!*/tests/*" --glob "*.rs"

# Async patterns
rg "async fn|spawn_blocking|tokio::" --glob "*.rs"

# Performance patterns
rg "clone\(\)|to_string\(\)|Arc<|Rc<" --glob "*.rs"
```

### Step 3: Testing Analysis
```bash
# Run all tests
cargo test --all -- --nocapture

# Coverage
cargo tarpaulin --out Html

# Benchmarks
cargo bench --no-run
```

### Step 4: Documentation Analysis
```bash
# Generate docs
cargo doc --no-deps

# Check for missing docs
cargo rustdoc -- -D missing_docs
```

### Step 5: Linting & Formatting
```bash
# Format check
cargo fmt -- --check

# Clippy (strict mode)
cargo clippy --all-targets --all-features -- -D warnings

# Audit dependencies
cargo audit
```

## Output Format

```markdown
# Rust Code Quality Report
**Generated**: [Date]
**Project**: rust-self-learning-memory

## Executive Summary
- **Overall Score**: X/100
- **Critical Issues**: N
- **Warnings**: M
- **Best Practices**: P/Q met

## Quality Dimensions

### 1. Project Structure: 8/10 ⭐⭐⭐⭐
✅ Good workspace organization
✅ Clear crate separation
⚠️ Some files exceed 500 LOC limit
  - memory-core/src/memory.rs: 623 lines (target: <500)

### 2. Error Handling: 9/10 ⭐⭐⭐⭐⭐
✅ Custom Error enum with thiserror
✅ Consistent Result<T> usage
✅ Minimal unwrap() usage (only in tests)
⚠️ Missing error context in 2 locations
  - memory-storage-turso/src/storage.rs:145

### 3. Async Patterns: 7/10 ⭐⭐⭐⭐
✅ Proper async fn usage
✅ spawn_blocking for redb
❌ Blocking call found in async context
  - memory-core/src/sync.rs:89 - std::fs::read

### 4. Memory & Performance: 8/10 ⭐⭐⭐⭐
✅ Good use of borrowing
✅ Minimal allocations
⚠️ Unnecessary clones in 3 locations
  - memory-core/src/extraction.rs:234

### 5. Testing: 6/10 ⭐⭐⭐
⚠️ Test coverage: 78% (target: >90%)
✅ Good unit test coverage
❌ Missing integration tests for:
  - Full sync cycle
  - Concurrent episode operations
  - Error recovery scenarios

### 6. Documentation: 9/10 ⭐⭐⭐⭐⭐
✅ Crate-level docs complete
✅ Most public APIs documented
⚠️ Missing examples in 2 functions
  - memory-core/src/extraction.rs:extract_patterns

### 7. Type Safety: 9/10 ⭐⭐⭐⭐⭐
✅ Strong typing with Uuid
✅ Good use of newtypes
✅ Builder pattern where appropriate

### 8. Security: 8/10 ⭐⭐⭐⭐
✅ No unsafe code
✅ Parameterized SQL queries
✅ Input validation present
⚠️ Resource limits not enforced in 1 location
  - memory-mcp/src/sandbox.rs:123

## Detailed Findings

### Critical Issues (Must Fix)
1. **Blocking call in async context**
   - File: memory-core/src/sync.rs:89
   - Issue: std::fs::read blocks the Tokio runtime
   - Fix: Use tokio::fs::read

### Warnings (Should Fix)
1. **File size exceeds limit**
   - File: memory-core/src/memory.rs (623 lines)
   - Target: <500 lines
   - Recommendation: Split into submodules

2. **Test coverage below target**
   - Current: 78%
   - Target: >90%
   - Missing coverage in: pattern extraction, sync logic

### Recommendations (Nice to Have)
1. Add property-based tests with proptest
2. Implement more comprehensive benchmarks
3. Add rustdoc examples for all public APIs

## Action Items

### High Priority
- [ ] Fix blocking call in sync.rs
- [ ] Increase test coverage to 90%
- [ ] Enforce resource limits in sandbox

### Medium Priority
- [ ] Refactor memory.rs (split into submodules)
- [ ] Add missing integration tests
- [ ] Add examples to all public APIs

### Low Priority
- [ ] Reduce unnecessary clones
- [ ] Add property-based tests
- [ ] Improve benchmark coverage
```

## Best Practices Checklist

Use this checklist when reviewing code:

**Project Structure**:
- [ ] Files <500 LOC
- [ ] Clear module hierarchy
- [ ] Consistent naming

**Error Handling**:
- [ ] Custom Error enum
- [ ] Result<T> for fallible ops
- [ ] No unwrap() in production
- [ ] Meaningful error messages

**Async/Await**:
- [ ] async fn for IO operations
- [ ] spawn_blocking for sync/CPU work
- [ ] No blocking calls in async
- [ ] Concurrent operations optimized

**Testing**:
- [ ] Unit tests (>90% coverage)
- [ ] Integration tests
- [ ] Benchmarks
- [ ] Test utilities

**Documentation**:
- [ ] Crate docs
- [ ] Module docs
- [ ] Function docs with examples
- [ ] README and CONTRIBUTING

**Performance**:
- [ ] Minimize allocations
- [ ] Use borrowing
- [ ] Zero-copy where possible

**Security**:
- [ ] No unsafe (unless justified)
- [ ] Input validation
- [ ] Parameterized queries
- [ ] Resource limits

## Example Usage

When invoked, this skill will:
1. Analyze project structure and organization
2. Review error handling patterns
3. Check async/await usage
4. Assess testing quality and coverage
5. Evaluate documentation completeness
6. Identify performance anti-patterns
7. Verify security practices
8. Generate comprehensive quality report with actionable items
