---
name: security-reviewer
description: Audit memory safety and security in unsafe code blocks, buffer handling, and security-sensitive operations
---

# Security Reviewer

Review unsafe code and security-sensitive operations in this secret scanning engine.

## When to Use

- After modifying any `unsafe` block
- When adding new parsing or decoding logic
- Before merging changes to `src/async_io/` or buffer handling code
- When implementing new transform chains

## Critical Areas in This Codebase

### High-Risk Files
- `src/runtime.rs` - Buffer pool with unsafe pointer operations
- `src/async_io/` - Platform-specific async I/O with raw pointers
- `src/engine/scratch.rs` - Scratch memory management
- `src/engine/stream_decode.rs` - Streaming decoder state machine
- `src/engine/buffer_scan.rs` - Buffer scanning with offsets

## Security Checklist

### Memory Safety
- [ ] All pointer arithmetic checked for overflow
- [ ] Slice bounds validated before `get_unchecked`
- [ ] Lifetimes correctly constrain returned references
- [ ] No use-after-free in buffer pool operations
- [ ] Alignment requirements satisfied for casts

### Buffer Handling
- [ ] No buffer overflows in write operations
- [ ] Length checks before copying
- [ ] Integer overflow checks on size calculations
- [ ] Proper handling of truncated reads

### Unsafe Block Audit
For each `unsafe` block:
- [ ] Documented safety invariants (why this is safe)
- [ ] Minimal scope (only unsafe operations inside)
- [ ] Kani proof or extensive testing coverage
- [ ] No undefined behavior paths

### Input Validation
- [ ] Untrusted input length-limited
- [ ] Malformed input cannot cause panics
- [ ] No amplification attacks (small input -> huge allocation)
- [ ] Transform chains handle edge cases (empty, max-size)

## Output Format

```markdown
## Security Review: [file/module]

### Unsafe Block Audit

| Location | Purpose | Safety Justification | Status |
|----------|---------|---------------------|--------|
| line:XX | ptr arithmetic | bounds checked at line:YY | SAFE |
| line:XX | transmute | MISSING JUSTIFICATION | REVIEW |

### Findings

| Severity | Issue | Location | CWE |
|----------|-------|----------|-----|
| CRITICAL | Unchecked bounds | line:XX | CWE-125 |
| HIGH | Integer overflow | line:XX | CWE-190 |

### Recommendations

1. **[Issue]**: Add bounds check before unsafe access
   ```rust
   // Before (unsafe)
   // After (safe)
   ```

### Verification

- [ ] Add Kani proof for memory safety
- [ ] Add fuzz target for this code path
- [ ] Add property test for invariant
```

## Related Resources

- `docs/kani-verification.md` - Existing Kani proofs
- `/test-strategy` - Choose appropriate verification approach
- `/run-fuzz` - Run fuzz targets for security testing
