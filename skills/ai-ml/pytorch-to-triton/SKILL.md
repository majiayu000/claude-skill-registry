---
name: pytorch-to-triton
description: Translate PyTorch implementations to Triton GPU kernels incrementally. Use when converting PyTorch code to Triton, optimizing GPU kernels, auditing/reviewing existing Triton code, or when user says "triton", "convert to triton", "gpu kernel", "pytorch to triton", "audit triton", or "review kernel".
---

# PyTorch to Triton Conversion

A skill for incrementally translating PyTorch implementations to Triton GPU kernels, progressing from simple/correct to optimized/efficient.

## Quick Start

When invoked:
1. First, ensure Triton documentation is cached locally (see [triton-docs.md](triton-docs.md))
2. Identify the PyTorch code to convert
3. Follow the 3-stage incremental conversion process
4. Validate correctness at each stage before optimizing

## Prerequisites: Triton Documentation

Before starting any conversion, ensure documentation is available:

```bash
# Check if docs exist
ls docs/.triton_docs/

# If not present, create and fetch (see triton-docs.md for details)
mkdir -p docs/.triton_docs
```

Use WebFetch to download and cache key Triton documentation to `docs/.triton_docs/`:
- `triton-lang-guide.md` - Core language reference
- `triton-tutorials.md` - Official tutorials (vector add, matmul, softmax, etc.)
- `triton-best-practices.md` - Optimization patterns

See [triton-docs.md](triton-docs.md) for complete fetching instructions.

## The 3-Stage Conversion Process

### Stage 1: Naive/Correct Implementation

**Goal**: Get a working Triton kernel that produces correct results.

**Approach**:
- Direct translation of PyTorch logic to Triton
- Use simple, readable patterns
- Prioritize correctness over performance
- Use explicit loops where helpful for clarity
- Minimal memory optimization

**Checklist**:
- [ ] Kernel compiles without errors
- [ ] Output matches PyTorch reference exactly (within float tolerance)
- [ ] Handles edge cases (empty inputs, boundary conditions)
- [ ] Works for all supported input shapes

**Example pattern** (from this codebase's `triton_scan.py`):
```python
@triton.jit
def naive_kernel(
    input_ptr, output_ptr,
    N: tl.constexpr,
    BLOCK_SIZE: tl.constexpr,
):
    # Simple 1:1 translation from PyTorch
    pid = tl.program_id(0)
    offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offsets < N

    # Load, compute, store - straightforward
    x = tl.load(input_ptr + offsets, mask=mask)
    y = x * 2  # Your computation
    tl.store(output_ptr + offsets, y, mask=mask)
```

**Validation**:
```python
# Always validate against PyTorch reference
def test_stage1():
    x = torch.randn(1024, device='cuda')
    ref = pytorch_implementation(x)
    out = triton_implementation(x)
    torch.testing.assert_close(ref, out, rtol=1e-5, atol=1e-5)
```

### Stage 2: Basic Optimizations

**Goal**: Apply standard Triton optimizations for better performance.

**Approach**:
- Proper memory coalescing (sequential thread access patterns)
- Power-of-2 block sizes for tl.arange
- Reduce global memory traffic
- Use appropriate dtypes
- Add @triton.autotune for block size selection

**Key Optimizations**:

1. **Memory coalescing**: Threads in a warp access consecutive memory
```python
# Good: Coalesced access
offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)

# Bad: Strided access
offsets = tl.arange(0, BLOCK_SIZE) * stride
```

2. **Block size tuning**:
```python
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_SIZE': 64}),
        triton.Config({'BLOCK_SIZE': 128}),
        triton.Config({'BLOCK_SIZE': 256}),
        triton.Config({'BLOCK_SIZE': 512}),
    ],
    key=['N'],
)
@triton.jit
def optimized_kernel(...):
    ...
```

3. **Reduce intermediate storage**:
```python
# Instead of storing intermediate tensors, compute inline
# Stage 1: result = tl.load(temp_ptr)  # extra memory traffic
# Stage 2: result = compute_inline(x)   # keep in registers
```

4. **Use constexpr for known dimensions**:
```python
def kernel(
    N: tl.constexpr,  # Compile-time constant, enables optimizations
    K: tl.constexpr,
):
```

**Checklist**:
- [ ] Still produces correct results (re-validate!)
- [ ] Memory access patterns are coalesced
- [ ] Block sizes are powers of 2
- [ ] Added autotune decorator
- [ ] Benchmark shows improvement over Stage 1

### Stage 3: Advanced Tuning

**Goal**: Maximum performance through advanced techniques.

**Approach**:
- Fused operations (combine multiple kernels)
- Shared memory / L1 cache utilization
- Register pressure optimization
- Pipelining and async memory operations
- Hardware-specific tuning

**Advanced Techniques**:

1. **Operation fusion**:
```python
# Before: 3 kernel launches
y = kernel1(x)
z = kernel2(y)
out = kernel3(z)

# After: 1 fused kernel
@triton.jit
def fused_kernel(...):
    x = tl.load(...)
    y = compute1(x)
    z = compute2(y)
    out = compute3(z)
    tl.store(...)
```

2. **Shared memory for data reuse** (see Semi-CRF ring buffer pattern):
```python
# From triton_scan.py - ring buffer stays in L1/L2 cache
ring_buffer = torch.empty((batch, K, C_PAD), device=device, dtype=dtype)
# Small buffer, reused across iterations
```

3. **Numerical stability in reductions**:
```python
# Stable logsumexp
max_val = tl.max(x, axis=0)
exp_x = tl.exp(x - max_val)
result = max_val + tl.log(tl.sum(exp_x, axis=0))
```

4. **2D block patterns for matrices**:
```python
@triton.jit
def matmul_kernel(
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_K: tl.constexpr,
):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)
    # Tile-based computation
```

**Checklist**:
- [ ] Still produces correct results (re-validate after EVERY change!)
- [ ] Profiled with `triton.testing.do_bench`
- [ ] Compared against torch.compile baseline
- [ ] Memory bandwidth utilization analyzed
- [ ] No unnecessary synchronization points

## Validation Framework

Always maintain a validation suite:

```python
def validate_triton_kernel(pytorch_fn, triton_fn, test_cases):
    """Validate Triton kernel against PyTorch reference."""
    for name, inputs in test_cases.items():
        ref = pytorch_fn(*inputs)
        out = triton_fn(*inputs)
        try:
            torch.testing.assert_close(ref, out, rtol=1e-4, atol=1e-4)
            print(f"  {name}: PASSED")
        except AssertionError as e:
            print(f"  {name}: FAILED - {e}")

# Standard test cases
test_cases = {
    "small": (torch.randn(64, device='cuda'),),
    "medium": (torch.randn(4096, device='cuda'),),
    "large": (torch.randn(1048576, device='cuda'),),
    "edge_empty": (torch.randn(0, device='cuda'),),
    "edge_single": (torch.randn(1, device='cuda'),),
}
```

## Benchmarking

```python
import triton

def benchmark_kernel(fn, *args, warmup=25, rep=100):
    """Benchmark a kernel using Triton's timing utilities."""
    ms = triton.testing.do_bench(lambda: fn(*args), warmup=warmup, rep=rep)
    return ms

# Compare implementations
pytorch_ms = benchmark_kernel(pytorch_fn, x)
triton_ms = benchmark_kernel(triton_fn, x)
speedup = pytorch_ms / triton_ms
print(f"Speedup: {speedup:.2f}x")
```

## Reference Implementation

See [triton_scan.py](../../src/torch_semimarkov/triton_scan.py) for a complete example of:
- PyTorch reference implementation (`semi_crf_forward_pytorch`)
- Optimized Triton kernel (`semi_crf_scan_kernel`)
- Hybrid dispatch (Triton for inference, torch.compile for training)
- Proper autograd integration via `torch.autograd.Function`

## Common Patterns

### Ring Buffer (from this codebase)
```python
# Maintain O(K) state instead of O(N) by using circular buffer
ring_buffer[head] = new_value
head = (head + 1) % K
prev_value = ring_buffer[(head - offset) % K]
```

### Masked Operations
```python
# Power-of-2 padding with masking
C_PAD = next_power_of_2(C)
c_idx = tl.arange(0, C_PAD)
c_mask = c_idx < C
value = tl.load(ptr + c_idx, mask=c_mask, other=0.0)
```

### Semiring Abstraction
```python
# Log semiring: logsumexp
result = max_val + tl.log(tl.sum(tl.exp(x - max_val)))

# Max semiring: max
result = tl.max(x)
```

## Instructions for Claude

When converting PyTorch to Triton:

1. **Read the PyTorch code thoroughly** - Understand the algorithm completely

2. **Check for cached docs** - Ensure `docs/.triton_docs/` exists and contains documentation. If not, fetch it first using the instructions in [triton-docs.md](triton-docs.md)

3. **Start with Stage 1** - Always begin with a naive, correct implementation

4. **Validate obsessively** - Test against PyTorch reference after EVERY change

5. **Progress incrementally** - Only move to next stage after current stage is validated

6. **Document assumptions** - Note tensor shapes, dtypes, and device requirements

7. **Consider backward pass** - For training, decide between:
   - Custom backward kernel (maximum performance, more work)
   - `torch.autograd.Function` with checkpointing (easier, moderate performance)
   - `torch.compile` on PyTorch reference (easiest, good performance)

8. **Use existing patterns** - Reference `triton_scan.py` for patterns used in this codebase

## Example Invocations

```
/pytorch-to-triton src/torch_semimarkov/helpers.py:compute_log_potentials

Convert the attention mechanism in model.py to a Triton kernel

Help me optimize my Triton kernel - it's slower than PyTorch

Translate this logsumexp reduction to Triton with numerical stability

Audit my Triton kernel for performance issues

Review the triton_scan.py implementation
```

---

## Audit Mode: Reviewing Existing Triton Code

Use audit mode to review existing Triton kernels for correctness, performance issues, and optimization opportunities.

### When to Audit

- After completing any stage of conversion
- When a Triton kernel is slower than expected
- Before merging Triton code to main branch
- When debugging numerical discrepancies
- Periodic review of production kernels

### Audit Workflow

```
1. Identify kernel(s) to audit
2. Locate PyTorch reference (if available)
3. Run full audit checklist
4. Generate audit report with findings
5. Prioritize fixes by impact
```

### Full Audit Checklist

#### 1. Correctness Audit

**Goal**: Verify the kernel produces correct results across all inputs.

```python
def audit_correctness(triton_fn, pytorch_fn, test_suite):
    """Run comprehensive correctness audit."""
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }

    for name, inputs in test_suite.items():
        ref = pytorch_fn(*inputs)
        out = triton_fn(*inputs)

        # Strict check
        try:
            torch.testing.assert_close(ref, out, rtol=1e-5, atol=1e-5)
            results["passed"].append(name)
        except AssertionError as e:
            # Check if within looser tolerance (numerical precision issue)
            try:
                torch.testing.assert_close(ref, out, rtol=1e-3, atol=1e-3)
                results["warnings"].append((name, "Passed with loose tolerance"))
            except:
                results["failed"].append((name, str(e)))

    return results

# Comprehensive test suite for audit
audit_test_suite = {
    # Size variations
    "tiny": make_inputs(size=1),
    "small": make_inputs(size=64),
    "medium": make_inputs(size=4096),
    "large": make_inputs(size=1048576),
    "non_power_of_2": make_inputs(size=1000),

    # Edge cases
    "zeros": make_inputs(fill=0.0),
    "ones": make_inputs(fill=1.0),
    "large_values": make_inputs(fill=1e6),
    "small_values": make_inputs(fill=1e-6),
    "negative": make_inputs(fill=-1.0),
    "mixed_signs": make_inputs(pattern="alternating"),

    # Numerical edge cases
    "near_overflow": make_inputs(fill=1e38),  # float32 max ~3.4e38
    "near_underflow": make_inputs(fill=1e-38),
    "inf_values": make_inputs(special="inf"),
    "nan_handling": make_inputs(special="nan"),

    # Batch variations
    "batch_1": make_inputs(batch=1),
    "batch_odd": make_inputs(batch=7),
    "batch_large": make_inputs(batch=256),
}
```

**Correctness Red Flags**:
- [ ] Results differ by more than 1e-5 relative tolerance
- [ ] NaN or Inf in output when not in input
- [ ] Different results on repeated runs (race condition)
- [ ] Boundary values handled differently than PyTorch

#### 2. Performance Audit

**Goal**: Identify performance bottlenecks and optimization opportunities.

```python
def audit_performance(triton_fn, pytorch_fn, baselines, sizes):
    """Run performance audit across input sizes."""
    import triton

    results = []
    for size in sizes:
        inputs = make_inputs(size=size)

        # Benchmark all implementations
        triton_ms = triton.testing.do_bench(lambda: triton_fn(*inputs))
        pytorch_ms = triton.testing.do_bench(lambda: pytorch_fn(*inputs))

        # Compare to baselines if provided
        baseline_ms = {}
        for name, fn in baselines.items():
            baseline_ms[name] = triton.testing.do_bench(lambda: fn(*inputs))

        # Calculate metrics
        speedup_vs_pytorch = pytorch_ms / triton_ms

        # Estimate theoretical peak (memory bandwidth limited)
        bytes_moved = estimate_memory_traffic(inputs)  # implement per-kernel
        theoretical_ms = bytes_moved / (GPU_BANDWIDTH_GB_S * 1e6)
        efficiency = theoretical_ms / triton_ms

        results.append({
            "size": size,
            "triton_ms": triton_ms,
            "pytorch_ms": pytorch_ms,
            "speedup": speedup_vs_pytorch,
            "hw_efficiency": efficiency,
            "baselines": baseline_ms,
        })

    return results
```

**Performance Audit Report Template**:
```
## Performance Audit: {kernel_name}

| Size | Triton (ms) | PyTorch (ms) | Speedup | HW Efficiency |
|------|-------------|--------------|---------|---------------|
| 1K   | 0.02        | 0.15         | 7.5x    | 45%           |
| 64K  | 0.08        | 0.42         | 5.2x    | 62%           |
| 1M   | 0.95        | 4.20         | 4.4x    | 78%           |

### Findings:
- [ ] Speedup < 1x for any size (CRITICAL)
- [ ] HW efficiency < 50% (optimization opportunity)
- [ ] Performance degrades at large sizes (memory bound)
- [ ] Performance degrades at small sizes (launch overhead)
```

**Performance Red Flags**:
- [ ] Slower than PyTorch at any input size
- [ ] Slower than `torch.compile` baseline
- [ ] Hardware efficiency below 50%
- [ ] Non-linear scaling with input size
- [ ] High variance in timing (> 10%)

#### 3. Memory Access Pattern Audit

**Goal**: Identify non-coalesced accesses and cache inefficiency.

**Checklist**:
```
Memory Coalescing:
- [ ] Consecutive threads access consecutive memory addresses
- [ ] No strided access patterns (stride > 1 between threads)
- [ ] Load/store addresses aligned to 128-byte boundaries

Cache Utilization:
- [ ] Working set fits in L1/L2 when possible
- [ ] Data reuse patterns exploit cache
- [ ] No unnecessary round-trips to global memory

Memory Traffic:
- [ ] Each element loaded/stored minimum times
- [ ] Intermediate results kept in registers
- [ ] No redundant loads of same data
```

**Pattern Analysis**:
```python
def analyze_memory_pattern(kernel_source):
    """Static analysis of memory access patterns."""
    issues = []

    # Check for strided access
    if re.search(r'tl\.arange.*\*.*stride', kernel_source):
        issues.append("WARN: Potential strided access pattern")

    # Check for non-power-of-2 arange
    aranges = re.findall(r'tl\.arange\((\d+),\s*(\d+)\)', kernel_source)
    for start, end in aranges:
        size = int(end) - int(start)
        if size & (size - 1) != 0:
            issues.append(f"ERROR: Non-power-of-2 arange size: {size}")

    # Check for multiple loads of same pointer
    loads = re.findall(r'tl\.load\(([^,]+)', kernel_source)
    if len(loads) != len(set(loads)):
        issues.append("WARN: Same pointer loaded multiple times")

    return issues
```

#### 4. Numerical Stability Audit

**Goal**: Identify potential overflow, underflow, and precision issues.

**Checklist**:
```
Overflow/Underflow:
- [ ] Large exponentials use log-space (logsumexp pattern)
- [ ] Products of many terms use log-sum instead
- [ ] Small denominators checked before division

Precision:
- [ ] Accumulations use higher precision (fp32 for fp16 inputs)
- [ ] Reductions use numerically stable algorithms
- [ ] Subtraction of similar values avoided (catastrophic cancellation)

Stability Patterns:
- [ ] logsumexp uses max-subtraction trick
- [ ] softmax computed as exp(x - max(x)) / sum
- [ ] Variance computed with Welford's algorithm for large N
```

**Stability Test Suite**:
```python
stability_tests = {
    # Overflow scenarios
    "exp_overflow": torch.tensor([100.0, 200.0, 300.0]),  # exp(300) overflows
    "product_overflow": torch.full((1000,), 2.0),  # 2^1000 overflows

    # Underflow scenarios
    "exp_underflow": torch.tensor([-100.0, -200.0, -300.0]),
    "small_product": torch.full((1000,), 0.5),

    # Cancellation scenarios
    "similar_values": torch.tensor([1e10, 1e10 + 1]),
    "alternating_sum": torch.tensor([1e8, -1e8, 1.0]),
}
```

**Numerical Red Flags**:
- [ ] `tl.exp()` on values > 80 without max subtraction
- [ ] Division without checking for near-zero denominator
- [ ] Accumulation in fp16 without upcasting
- [ ] Subtraction of values with similar magnitude

#### 5. Best Practices Audit

**Goal**: Check adherence to Triton best practices and patterns.

**Code Quality Checklist**:
```
Kernel Structure:
- [ ] Uses tl.constexpr for compile-time constants
- [ ] Block sizes are powers of 2
- [ ] Grid dimensions computed correctly
- [ ] Proper masking for boundary conditions

Optimization Patterns:
- [ ] @triton.autotune with multiple configs
- [ ] Autotune key includes relevant dimensions
- [ ] num_warps tuned for workload
- [ ] num_stages set for pipelining (if applicable)

Maintainability:
- [ ] PyTorch reference implementation exists
- [ ] Clear docstring with tensor shapes
- [ ] Validation test included
- [ ] Benchmark comparing to baseline
```

**Anti-Pattern Detection**:
```python
def detect_antipatterns(kernel_source):
    """Detect common Triton anti-patterns."""
    antipatterns = []

    # Missing constexpr
    params = re.findall(r'def \w+\([^)]+\)', kernel_source)
    if 'tl.constexpr' not in kernel_source:
        antipatterns.append("WARN: No tl.constexpr parameters found")

    # Hardcoded magic numbers
    if re.search(r'tl\.arange\(0,\s*\d+\)', kernel_source):
        antipatterns.append("WARN: Hardcoded arange size (use BLOCK_SIZE constexpr)")

    # Missing mask on boundary
    loads = re.findall(r'tl\.load\([^)]+\)', kernel_source)
    for load in loads:
        if 'mask=' not in load:
            antipatterns.append(f"WARN: Load without mask: {load[:50]}...")

    # Break in loop (unsupported)
    if 'break' in kernel_source:
        antipatterns.append("ERROR: 'break' not supported in Triton loops")

    # Python conditionals on runtime values
    if re.search(r'if\s+\w+\s*[<>=]', kernel_source):
        if 'tl.where' not in kernel_source:
            antipatterns.append("WARN: Python if on runtime value (use tl.where)")

    return antipatterns
```

### Audit Report Template

Generate a structured report after auditing:

```markdown
# Triton Kernel Audit Report

**Kernel**: `{kernel_name}`
**File**: `{file_path}`
**Date**: {date}
**Auditor**: Claude (pytorch-to-triton skill)

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Correctness | ✅ PASS | 0 |
| Performance | ⚠️ WARN | 2 |
| Memory Patterns | ✅ PASS | 0 |
| Numerical Stability | ✅ PASS | 0 |
| Best Practices | ⚠️ WARN | 1 |

## Detailed Findings

### Performance
1. **[MEDIUM]** Hardware efficiency is 45% at size 1K - consider fusing with adjacent operations
2. **[LOW]** No autotune decorator - performance may vary across GPU architectures

### Best Practices
1. **[LOW]** Missing tl.constexpr on N parameter - prevents some compiler optimizations

## Recommendations

1. Add @triton.autotune with configs for BLOCK_SIZE in [64, 128, 256]
2. Mark N as tl.constexpr if known at compile time
3. Consider fusing with downstream softmax for better cache utilization

## Test Commands

```bash
# Run correctness tests
pytest tests/test_triton_kernel.py -v

# Run benchmarks
python benchmarks/bench_kernel.py --sizes 1024,65536,1048576
```
```

### Audit Invocation Examples

```
# Audit a specific kernel
Audit the semi_crf_scan_kernel in triton_scan.py

# Audit with focus area
Review triton_scan.py for numerical stability issues

# Compare implementations
Audit my_kernel.py against the PyTorch reference in reference.py

# Full audit before merge
Run a full audit on all Triton code in src/
```
