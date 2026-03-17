---
name: security/memory-safety
description: Memory Safety security skill
---

# Memory Safety

C's primary vulnerability class. Buffer overflows, use-after-free, and integer issues remain the top attack vectors in native code.

## ikigai Application

**talloc mitigates but doesn't eliminate:** Hierarchical ownership prevents leaks but not overflows or UAF within a context's lifetime.

**Critical patterns:**
- Bounds check ALL array access before use
- Validate sizes before allocation: `if (n > SIZE_MAX / elem_size) return ERR(...)`
- Never trust size values from external sources
- Use `talloc_array()` not manual multiplication

**Integer overflow risks:**
- `size_t` multiplication for buffer sizes
- Signed/unsigned conversion in comparisons
- Off-by-one in loop bounds

**Detection tools:**
- ASan (`make BUILD=sanitize`) - buffer overflow, UAF
- UBSan - undefined behavior, integer overflow
- Valgrind - memory errors, leaks

**Review red flags:** Manual pointer arithmetic, `memcpy` with computed sizes, array indexing without bounds check.
