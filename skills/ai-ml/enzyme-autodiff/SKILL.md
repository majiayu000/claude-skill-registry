---
name: enzyme-autodiff
description: Enzyme.jl Automatic Differentiation Skill
version: 1.0.0
---

# Enzyme.jl Automatic Differentiation Skill

Enzyme.jl provides LLVM-level automatic differentiation for Julia, enabling high-performance gradient computation for both CPU and GPU code.

## Type Annotations

Type annotations control how arguments are treated during differentiation:

| Annotation | Description | Usage |
|------------|-------------|-------|
| `Const(x)` | Constant, not differentiated | Parameters, hyperparameters |
| `Active(x)` | Scalar to differentiate (reverse mode only) | Scalar inputs |
| `Duplicated(x, ∂x)` | Mutable with shadow accumulator | Arrays, mutable structs |
| `DuplicatedNoNeed(x, ∂x)` | Like Duplicated, may skip primal | Performance optimization |
| `BatchDuplicated(x, ∂xs)` | Batched shadows (tuple) | Multiple derivatives at once |
| `MixedDuplicated(x, ∂x)` | Mixed active/duplicated data | Custom rules with mixed types |

```julia
using Enzyme

# Active for scalars (reverse mode)
f(x) = x^2
autodiff(Reverse, f, Active, Active(3.0))  # Returns ((6.0,),)

# Duplicated for arrays
A = [1.0, 2.0, 3.0]
dA = zeros(3)
g(A) = sum(A .^ 2)
autodiff(Reverse, g, Active, Duplicated(A, dA))
# dA now contains [2.0, 4.0, 6.0]

# Const for non-differentiated arguments
h(x, c) = c * x^2
autodiff(Reverse, h, Active, Active(2.0), Const(3.0))  # Only differentiates x
```

## Differentiation Modes

| Mode | Direction | Returns | Use Case |
|------|-----------|---------|----------|
| `Forward` | Tangent propagation | Derivative | Single input, many outputs |
| `ForwardWithPrimal` | Forward + primal | (primal, derivative) | Need both values |
| `Reverse` | Adjoint propagation | Gradient tuple | Many inputs, scalar output |
| `ReverseWithPrimal` | Reverse + primal | (primal, gradients) | Need both values |
| `ReverseSplitWithPrimal` | Separated passes | (forward_fn, reverse_fn) | Custom control flow |

```julia
# Forward mode: use Duplicated, not Active
autodiff(Forward, x -> x^2, Duplicated(3.0, 1.0))  # Returns (6.0,)

# Forward with primal
autodiff(ForwardWithPrimal, x -> x^2, Duplicated(3.0, 1.0))  # Returns (9.0, 6.0)

# Reverse mode: scalar outputs, use Active
autodiff(Reverse, x -> x^2, Active, Active(3.0))  # Returns ((6.0,),)
```

## autodiff and autodiff_thunk

### autodiff
Primary differentiation interface:
```julia
autodiff(mode, func, return_annotation, arg_annotations...)
```

### autodiff_thunk
Returns compiled forward/reverse thunks for repeated use:
```julia
# Split mode returns separate forward and reverse functions
forward, reverse = autodiff_thunk(
    ReverseSplitWithPrimal,
    Const{typeof(f)},
    Active,
    Duplicated{typeof(A)},
    Active{typeof(v)}
)

# Forward pass returns (tape, primal, shadow)
tape, primal, shadow = forward(Const(f), Duplicated(A, dA), Active(v))

# Reverse pass uses tape
reverse(Const(f), Duplicated(A, dA), Active(v), 1.0, tape)
```

## LLVM Integration

Enzyme operates at LLVM IR level, providing:
- Direct LLVM transformation without Julia overhead
- Optimal derivative code generation
- Integration with GPUCompiler.jl for GPU support

```julia
# Enzyme uses LLVM-level activity analysis
# to determine which values need differentiation
using Enzyme.API
API.typeWarning!(false)  # Suppress type warnings
API.strictAliasing!(true)  # Enable strict aliasing optimizations
```

## Rule System (EnzymeRules)

Define custom derivatives when automatic differentiation is insufficient:

```julia
using EnzymeRules
using EnzymeCore

# Custom forward rule
function EnzymeRules.forward(
    ::Const{typeof(my_func)},
    RT::Type{<:Union{Duplicated, DuplicatedNoNeed}},
    x::Duplicated
)
    primal = my_func(x.val)
    derivative = custom_derivative(x.val) * x.dval
    return Duplicated(primal, derivative)
end

# Custom reverse rule: augmented_primal + reverse
function EnzymeRules.augmented_primal(
    config,
    ::Const{typeof(my_func)},
    RT::Type{<:Active},
    x::Active
)
    primal = my_func(x.val)
    tape = (x.val,)  # Store for reverse pass
    return AugmentedReturn(primal, nothing, tape)
end

function EnzymeRules.reverse(
    config,
    ::Const{typeof(my_func)},
    dret::Active,
    tape,
    x::Active
)
    x_val = tape[1]
    dx = custom_derivative(x_val) * dret.val
    return (dx,)
end
```

### Import ChainRules
```julia
using Enzyme
using ChainRulesCore

# Import existing ChainRules as Enzyme rules
@import_rrule typeof(special_func) Float64
@import_frule typeof(special_func) Float64
```

## CUDA.jl Integration (EnzymeCoreExt)

Differentiate GPU kernels with `autodiff_deferred`:

```julia
using CUDA
using Enzyme

# GPU kernel
function mul_kernel!(A, B, C)
    i = threadIdx().x
    C[i] = A[i] * B[i]
    return nothing
end

# Differentiate within kernel
function grad_kernel!(A, dA, B, dB, C, dC)
    autodiff_deferred(
        Reverse,
        mul_kernel!,
        Const,
        Duplicated(A, dA),
        Duplicated(B, dB),
        Duplicated(C, dC)
    )
    return nothing
end

# Launch differentiated kernel
A = CUDA.rand(32)
dA = CUDA.zeros(32)
B = CUDA.rand(32)
dB = CUDA.zeros(32)
C = CUDA.zeros(32)
dC = CUDA.ones(32)  # Seed adjoint

@cuda threads=32 grad_kernel!(A, dA, B, dB, C, dC)
```

### GPUCompiler Integration
```julia
using EnzymeCore

# Enzyme uses compiler_job_from_backend for GPU compilation
# This is automatically configured when CUDA.jl is loaded
function EnzymeCore.compiler_job_from_backend(::CUDABackend, F, TT)
    return GPUCompiler.CompilerJob(
        CUDA.compiler_config(CUDA.device()),
        F, TT
    )
end
```

## Common Patterns

### Gradient of loss function
```julia
function loss(params, data)
    predictions = model(params, data.x)
    return sum((predictions .- data.y).^2)
end

dparams = zero(params)
autodiff(Reverse, loss, Active, Duplicated(params, dparams), Const(data))
# dparams now contains ∇loss
```

### Jacobian-vector product (JVP)
```julia
function f(x)
    return [x[1]^2 + x[2], x[1] * x[2]]
end

x = [2.0, 3.0]
v = [1.0, 0.0]  # Direction vector
dx = copy(v)
dy = zeros(2)

autodiff(Forward, f, Duplicated(x, dx))  # Returns JVP
```

### Vector-Jacobian product (VJP)
```julia
function f!(y, x)
    y[1] = x[1]^2 + x[2]
    y[2] = x[1] * x[2]
    return nothing
end

x = [2.0, 3.0]
dx = zeros(2)
y = zeros(2)
dy = [1.0, 0.0]  # Adjoint seed

autodiff(Reverse, f!, Const, Duplicated(y, dy), Duplicated(x, dx))
# dx now contains VJP
```

---

## MaxEnt Triad Testing Protocol

Three agents maximize mutual information through complementary verification:

| Agent | Role | Verifies |
|-------|------|----------|
| julia-gpu-kernels | Input provider | @kernel functions to differentiate |
| enzyme-autodiff | Differentiator | Correct gradient computation |
| julia-tempering | Seed provider | Reproducible differentiation |

### Information Flow
```
julia-tempering ──seed──▶ julia-gpu-kernels ──kernel──▶ enzyme-autodiff
       │                                                      │
       └──────────────────── verify ◀─────────────────────────┘
```

### Test 1: Reverse Mode Scalar Differentiation
```julia
using Enzyme

# Polynomial differentiation
f(x) = x^2 + 2x + 1
∂f_∂x = autodiff(Reverse, f, Active, Active(3.0))[1][1]
@assert ∂f_∂x ≈ 8.0  # 2x + 2 at x=3
```

### Test 2: Forward Mode with Primal
```julia
using Enzyme

g(x) = exp(x) * sin(x)
primal, derivative = autodiff(ForwardWithPrimal, g, Duplicated(1.0, 1.0))
# derivative = exp(x)(sin(x) + cos(x)) at x=1
@assert derivative ≈ exp(1.0) * (sin(1.0) + cos(1.0))
```

### Test 3: GPU Kernel Differentiation (julia-gpu-kernels provides)
```julia
using CUDA, Enzyme

# Kernel from julia-gpu-kernels agent
function saxpy_kernel!(Y, a, X)
    i = threadIdx().x
    Y[i] += a * X[i]
    return nothing
end

# enzyme-autodiff differentiates
function grad_saxpy!(Y, dY, a, X, dX)
    autodiff_deferred(Reverse, saxpy_kernel!,
        Const,
        Duplicated(Y, dY),
        Active(a),
        Duplicated(X, dX))
    return nothing
end

# julia-tempering provides reproducible seed
seed = 42
CUDA.seed!(seed)
X = CUDA.rand(Float32, 256)
Y = CUDA.zeros(Float32, 256)
dY = CUDA.ones(Float32, 256)
dX = CUDA.zeros(Float32, 256)

@cuda threads=256 grad_saxpy!(Y, dY, 2.0f0, X, dX)
@assert all(Array(dX) .≈ 2.0f0)  # ∂(aX)/∂X = a
```

### Test 4: Reproducibility Verification
```julia
using Enzyme, Random

# julia-tempering seed ensures reproducibility
function reproducible_test(seed::UInt64)
    Random.seed!(seed)
    x = randn()
    
    f(x) = x^3 - 2x^2 + x
    grad = autodiff(Reverse, f, Active, Active(x))[1][1]
    
    # Derivative: 3x² - 4x + 1
    expected = 3x^2 - 4x + 1
    return (x=x, grad=grad, expected=expected, match=isapprox(grad, expected))
end

# Same seed → same results across agents
result = reproducible_test(0x7f4a3c2b1d0e9a8f)
@assert result.match
```

### Triad Verification Matrix

| Test | julia-gpu-kernels | enzyme-autodiff | julia-tempering |
|------|-------------------|-----------------|-----------------|
| Scalar AD | - | Reverse/Forward | RNG seed |
| Array AD | - | Duplicated | Array seed |
| GPU kernel | @cuda kernel | autodiff_deferred | CUDA.seed! |
| Batched | - | BatchDuplicated | Batch seeds |
| Custom rules | Complex kernel | EnzymeRules | Deterministic tape |

### Agent Communication Protocol
```julia
# Message format between agents
struct TriadMessage
    from::Symbol      # :gpu_kernels, :enzyme, :tempering
    to::Symbol
    payload::Any
    seed::UInt64      # For reproducibility
end

# Example flow
msg1 = TriadMessage(:tempering, :gpu_kernels, seed, seed)
msg2 = TriadMessage(:gpu_kernels, :enzyme, kernel_fn, seed)
msg3 = TriadMessage(:enzyme, :tempering, gradients, seed)  # Verification
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Autodiff
- **jax** [○] via bicomodule
  - Hub for autodiff/ML

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.