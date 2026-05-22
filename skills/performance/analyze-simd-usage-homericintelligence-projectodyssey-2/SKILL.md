---
name: analyze-simd-usage
description: "Analyze SIMD usage opportunities in Mojo code. Use to find performance optimization opportunities."
category: mojo
mcp_fallback: none
agent: test-engineer
user-invocable: false
---

# Analyze SIMD Usage Opportunities

Identify where SIMD (Single Instruction Multiple Data) can improve performance.

## When to Use

- Performance-critical tensor operations
- Element-wise operations on large arrays
- Vectorization of loops processing multiple elements
- Optimizing matrix/vector operations
- Finding performance bottlenecks in ML code

## Quick Reference

```bash
# Find loops processing arrays/tensors
grep -n "for.*in.*range\|@unroll\|@vectorize" *.mojo

# Find element-wise operations
grep -n "\.load\|\.store\|\.broadcast" *.mojo

# Check for SIMD parameters
grep -n "simd_width\|nelems\|\[.*:\]" *.mojo

# Identify candidates
grep -n "for i in range.*:" -A 10 *.mojo | grep -E "array\[i\]|tensor\[i\]"
```

## SIMD Optimization Opportunities

**Vectorizable Patterns**:

- ✅ Element-wise addition: `a[i] + b[i]` for all i
- ✅ Scalar multiplication: `a[i] * scalar` for all i
- ✅ Unary operations: `sin(a[i])`, `exp(a[i])` for all i
- ✅ Reduction operations: sum, max, min over array
- ❌ Dependent iterations: `a[i] = a[i-1] + value` (sequential)
- ❌ Conditional branches: `if a[i] > threshold:` (hard to vectorize)
- ❌ Function calls: unpredictable latency (avoid in tight loops)

**SIMD Width Selection**:

- `@parameter fn[simd_width: Int]` - Generic SIMD width
- `simd_width=4` - Typically good for float32
- `simd_width=8` - Optimal for many operations
- `simd_width=16+` - For int32 or specialized ops
- Match hardware capabilities (AVX2=4-8, AVX512=8-16)

**Vectorization Patterns**:

- ✅ `@vectorize` decorator for simple loops
- ✅ `@unroll` for small loops (2-4 iterations)
- ✅ Manual SIMD with `.load[]` and `.store[]`
- ✅ Tensor operations with SIMD dimensions

## Analysis Workflow

1. **Profile code**: Identify bottlenecks using time/memory metrics
2. **Find loops**: Locate loops processing large amounts of data
3. **Check vectorizability**: Verify no loop-carried dependencies
4. **Estimate speedup**: SIMD could provide 4-16x improvement
5. **Implement SIMD**: Use @vectorize, @unroll, or manual SIMD
6. **Measure performance**: Verify improvement with benchmarks
7. **Document changes**: Note what was optimized and why

## Output Format

Report SIMD analysis with:

1. **Hotspots** - Functions/loops using most CPU time
2. **Vectorization Potential** - Operations that could use SIMD
3. **Estimated Speedup** - Expected performance improvement
4. **Implementation Priority** - High/medium/low impact
5. **Technical Approach** - How to implement SIMD
6. **Risks** - Potential issues with vectorization
7. **Recommendations** - Which optimizations to pursue first

## Optimization Examples

**Example 1: Element-wise Addition**

```mojo
# Before: scalar loop
fn add_scalar(a: Tensor, b: Tensor) -> Tensor:
    var result = Tensor(a.shape)
    for i in range(a.num_elements()):
        result._data[i] = a._data[i] + b._data[i]
    return result

# After: vectorized
@vectorize
fn add_simd[simd_width: Int](i: Int):
    result._data.store[simd_width](i,
        a._data.load[simd_width](i) + b._data.load[simd_width](i))

def add_vectorized(a: Tensor, b: Tensor) -> Tensor:
    var result = Tensor(a.shape)
    # 4x-8x speedup typical
    return result
```

**Example 2: Reduction (Sum)**

```mojo
# Before: scalar loop
fn sum_scalar(tensor: Tensor) -> Float32:
    var total: Float32 = 0
    for i in range(tensor.num_elements()):
        total += tensor._data[i]
    return total

# After: SIMD reduction
fn sum_simd[simd_width: Int](tensor: Tensor) -> Float32:
    # Process simd_width elements at a time
    # Then reduce results - can be much faster
    return total
```

## Error Handling

| Problem | Solution |
|---------|----------|
| Vectorization causes wrong results | Check for loop-carried dependencies |
| Segment fault with SIMD | Verify alignment and bounds |
| Minimal speedup | May not be vectorizable, profile to confirm |
| Complex logic | Break into simpler vectorizable operations |
| Type mismatches | Ensure SIMD width compatible with element type |

## SIMD Decision Tree

- Does loop process large arrays? → YES → Check vectorizability
- Loop-carried dependencies? → YES → Can't vectorize, optimize differently
- Simple operations on many elements? → YES → Use @vectorize or @unroll
- Critical path (hot loop)? → YES → Worth optimizing
- Implement → Measure → Iterate

## References

- See mojo-simd-optimize for implementation guidance
- See CLAUDE.md for SIMD code patterns
- See performance section in module documentation
