---
name: mojo-simd-optimize
description: "Apply SIMD optimizations to Mojo code for parallel computation. Use when optimizing performance-critical tensor and array operations."
mcp_fallback: none
category: mojo
agent: test-engineer
user-invocable: false
---

# SIMD Optimization Skill

Parallelize tensor and array operations using SIMD.

## When to Use

- Optimizing tensor operations
- Vectorizing element-wise computations
- Performance-critical loops (>1000 elements)
- Benchmark results show optimization potential

## Quick Reference

```mojo
from sys.info import simdwidthof

comptime width = simdwidthof[DType.float32]()

# SIMD vector add
for i in range(0, size, width):
    result.store(i, a.load[width](i) + b.load[width](i))
```

## Workflow

1. **Identify bottleneck** - Profile code to find hot loops
2. **Get SIMD width** - Use `simdwidthof[dtype]()`
3. **Vectorize loop** - Process `width` elements per iteration
4. **Handle remainder** - Process leftover elements
5. **Benchmark** - Verify performance improvement (4x-8x expected)

## Mojo-Specific Notes

- SIMD width varies by CPU and dtype (usually 8-16 for float32)
- Always handle remainder elements with scalar loop
- Prefer `alias` for compile-time SIMD width constants
- Test on target hardware - SIMD width is platform-specific

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Out of bounds` | Remainder not handled | Add scalar remainder loop |
| `No speedup` | Wrong SIMD width | Use `simdwidthof[dtype]()` |
| `Compilation fails` | Type mismatch | Check load/store types match |
| `Segfault` | Misaligned access | Ensure stride is correct |

## References

- `.claude/shared/mojo-guidelines.md` - SIMD patterns section
- Mojo manual: SIMD documentation
