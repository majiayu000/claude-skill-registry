---
name: cuda-kernels
description: Develop, test, and optimize custom CUDA kernels in the candle framework for qwen3-tts-rs. Use when writing CUDA kernels, debugging GPU code, integrating kernels with candle, optimizing throughput, profiling with nsys/ncu, analyzing roofline, or investigating register pressure and occupancy.
---

# CUDA Kernel Development & Optimization

Skill for developing and optimizing custom CUDA kernels in the candle framework for `qwen3-tts-rs`.

## Trigger Words

cuda kernel, custom kernel, fused op, write kernel, ptx, kernel launch, CustomOp, nsys, ncu, profiling, roofline, occupancy, register pressure

## Candle Custom Op Patterns

### CustomOp1 (single input tensor)

```rust
use candle_core::{CustomOp1, Layout, Shape, DType, backend::BackendStorage, CudaStorage};

struct MyFusedOp { /* params */ }

impl CustomOp1 for MyFusedOp {
    fn name(&self) -> &'static str { "my_fused_op" }

    fn cpu_fwd(&self, storage: &CpuStorage, layout: &Layout) -> candle_core::Result<(CpuStorage, Shape)> {
        // CPU fallback (can panic/unimplemented for CUDA-only ops)
        todo!("CPU fallback")
    }

    #[cfg(feature = "cuda")]
    fn cuda_fwd(&self, storage: &CudaStorage, layout: &Layout) -> candle_core::Result<(CudaStorage, Shape)> {
        // Launch PTX kernel here
    }
}

// Usage: tensor.apply_op1(MyFusedOp { ... })?
```

### CustomOp2 (two input tensors)

```rust
impl CustomOp2 for FusedSiluMul {
    fn name(&self) -> &'static str { "fused_silu_mul" }

    fn cpu_fwd(&self, s1: &CpuStorage, l1: &Layout, s2: &CpuStorage, l2: &Layout)
        -> candle_core::Result<(CpuStorage, Shape)> { todo!() }

    #[cfg(feature = "cuda")]
    fn cuda_fwd(&self, s1: &CudaStorage, l1: &Layout, s2: &CudaStorage, l2: &Layout)
        -> candle_core::Result<(CudaStorage, Shape)> {
        // Launch PTX kernel
    }
}

// Usage: tensor_a.apply_op2(tensor_b, FusedSiluMul)?
```

### InplaceOp1 (mutate tensor in place)

```rust
impl candle_core::InplaceOp1 for MyInplaceOp {
    fn name(&self) -> &'static str { "my_inplace" }

    fn cpu_fwd(&self, storage: &mut CpuStorage, layout: &Layout) -> candle_core::Result<()> { todo!() }

    #[cfg(feature = "cuda")]
    fn cuda_fwd(&self, storage: &mut CudaStorage, layout: &Layout) -> candle_core::Result<()> {
        // Modify storage in place — no allocation
    }
}

// Usage: tensor.inplace_op1(&MyInplaceOp { ... })?
```

## PTX Kernel Embedding

Write `.cu` files in `kernels/`, compile to PTX, embed via `include_str!`:

```rust
use candle_core::cuda_backend::cudarc::driver::{LaunchConfig, LaunchAsync};
use candle_core::cuda_backend::WrapErr;

const PTX_SRC: &str = include_str!("../../kernels/my_kernel.ptx");

// Inside cuda_fwd():
let dev = storage.device();
let func = dev.get_or_load_func("my_kernel_name", PTX_SRC)?;
let cfg = LaunchConfig::for_num_elems(num_elements as u32);
unsafe { func.launch(cfg, (input_ptr, output_ptr, num_elements)) }.w()?;
```

### Compiling .cu → .ptx

```bash
nvcc -ptx -arch=sm_80 -o kernels/my_kernel.ptx kernels/my_kernel.cu
```

Or in `build.rs` for automatic compilation.

## Docker Dev Loop

All CUDA compilation and testing happens in Docker (NGC PyTorch base image):

```bash
# Quick kernel unit test
./scripts/test-kernel.sh fused_rmsnorm

# Full e2e benchmark
make profile-chrome MODEL_DIR=test_data/models/1.7B-CustomVoice

# Count kernel launches per frame
./scripts/count-kernels.sh
```

## Testing Pattern

Unit tests use synthetic tensors (no model weights needed):

```rust
#[test]
fn test_fused_vs_sequential() {
    let device = candle_core::Device::cuda_if_available(0).unwrap();
    let a = Tensor::randn(0., 1., (1, 2048), &device).unwrap();

    let sequential = a.silu().unwrap().mul(&b).unwrap();
    let fused = a.apply_op2(&b, FusedSiluMul).unwrap();

    let diff = (sequential - fused).unwrap().abs().unwrap().max(0).unwrap().to_scalar::<f32>().unwrap();
    assert!(diff < 1e-5, "fused vs sequential diff: {diff}");
}
```

Run with: `cargo test --lib -- fused_silu_mul`

## Project-Specific Notes

- Compute dtype: BF16 on CUDA, F32 on CPU
- Decoder and speaker encoder always F32
- Profiling spans gated behind `#[cfg(feature = "profiling")]`
- GPU sync audit: `make audit-gpu-syncs`
- Kernel plan: `docs/CUSTOM_CUDA_KERNELS_PLAN.md`
- 33 layers total per frame (28 talker + 5 code predictor)
- Target: reduce ~700 kernel launches/frame to ~545

---

## Optimization & Profiling

**One change per cycle:** baseline → profile → classify → optimize → verify → compare → loop. Multiple simultaneous changes make it impossible to attribute improvement. Revert on regression.

See `REFERENCE.md` for the full profiling reference (nsys, ncu, SASS inspection, bottleneck classification, optimization strategies).
