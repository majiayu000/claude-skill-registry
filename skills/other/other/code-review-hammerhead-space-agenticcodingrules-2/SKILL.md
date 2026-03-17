---
name: code-review
description: Review Julia code for correctness, performance, numerical stability, AD compatibility, and maintainability. Use when reviewing pull requests, examining code changes, auditing performance, or when the user asks for a code review.
---

# Code Review

## Purpose

Review code for correctness, performance, and maintainability with attention to the specific concerns of scientific/numerical Julia code.

## Review Checklist

### Correctness
- [ ] Logic is correct and handles edge cases (singularities, zero vectors, degenerate orbits)
- [ ] Numerical stability: no catastrophic cancellation, overflow, or division by near-zero
- [ ] Units are consistent (km, km/s, radians) and conversions are correct
- [ ] Frame conventions are respected (J2000 ECI, ECEF, body-fixed)
- [ ] Mathematical formulation matches cited reference (paper, textbook)

### Performance
- [ ] Hot-path functions return `SVector`/`SMatrix`, not heap-allocated arrays
- [ ] No unnecessary allocations (verify with `@check_allocs` or `@allocated`)
- [ ] `@inline` on performance-critical functions
- [ ] No type instabilities (`@code_warntype` clean)
- [ ] Promotion via `promote_type` rather than implicit conversion

### AD Compatibility
- [ ] No mutation of arrays that AD needs to track (return new values instead)
- [ ] No branching on floating-point values in differentiable paths
- [ ] Uses `promote_type(T, V)` for mixed numeric types
- [ ] Safe handling of norm-near-zero (no NaN gradients)
- [ ] Tested with ForwardDiff at minimum; ideally multiple backends

### Style & Maintainability
- [ ] `using`/`import` only in module file or `runtests.jl`, not in `include`-d files
- [ ] `export` at the top of the file where symbols are defined
- [ ] Packages added via Pkg.jl, not by editing Project.toml directly
- [ ] Docstrings with `# Arguments`, `# Returns`, `# References`
- [ ] Functions are focused (single responsibility)
- [ ] Consistent naming: PascalCase types, snake_case functions, Unicode for physics

### Testing
- [ ] Correctness tests against known reference values
- [ ] Edge cases tested (circular, equatorial, hyperbolic, near-singularity)
- [ ] AD tests comparing against FiniteDiff
- [ ] Allocation tests on hot-path functions

## Feedback Format

Categorize each finding:
- **Critical**: Must fix -- correctness bug, numerical instability, or silent wrong answer
- **Performance**: Allocation, type instability, or avoidable overhead
- **Suggestion**: Improvement to clarity, style, or maintainability
- **Nitpick**: Minor style preference, optional

For each finding, provide:
1. The specific location (file and line)
2. What the issue is
3. A concrete fix or alternative
